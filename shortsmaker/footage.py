"""Real film clips (Commons, Internet Archive, NASA, Pixabay) and their ffmpeg crops."""

import hashlib
import io
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path

from PIL import Image

from shortsmaker import image_sources, media_library, media_tools, plan_rules
from shortsmaker.config import H, ROOT, W


FILM_UA = "ShortsMaker/1.0 (personal video script)"  # non-Wikimedia sites don't get the contact email
PIXABAY_KEY_FILE = ROOT / "pixabay_key.txt"  # the owner's free Pixabay API key (stock video); optional
# Legacy crop is opt-in for old source notes. New sources retain their whole frame;
# uploader overlays are rejected by the visual editor rather than hidden by cropping.
FILM_CROP = "crop=trunc(iw*0.92/2)*2:trunc(ih*0.74/2)*2:trunc(iw*0.04/2)*2:trunc(ih*0.06/2)*2"
# Horizontal clips fit within this foreground band, above a blurred/darkened background.
FILM_BAND = 1100
# Keep the complete original frame in the foreground: prices, brand marks and ad slogans are evidence.
FILM_VF = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=30,"
           f"colorchannelmixer=rr=0.55:gg=0.55:bb=0.55[bg];"
           f"[b]scale={W}:{FILM_BAND}:force_original_aspect_ratio=decrease[fg];"
           "[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p")
# Already-vertical clips (9:16 Veo clips or vertical stock footage) fill the whole 1080x1920 frame.
FILL_VF = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p"


def nasa_films(query: str, limit: int = 2, names=()) -> list[dict]:
    """NASA videos (public domain), as their medium/small MP4 renditions."""
    found = []
    for it in image_sources.nasa_search(query, "video"):
        d = (it.get("data") or [{}])[0]
        if len(found) >= limit or not image_sources.on_topic(f"{d.get('title', '')} {str(d.get('description', ''))[:300]}", query, names):
            continue
        try:
            files = [a["href"] for a in json.loads(media_tools.fetch(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(d['nasa_id'])}",
                                                        30, FILM_UA))["collection"]["items"]]
            src = next(f for tag in ("~medium.mp4", "~small.mp4", "~mobile.mp4") for f in files if f.endswith(tag))
            src = src.replace("http://", "https://")
            dur = media_tools.duration(src)
        except Exception:
            continue
        if 3 <= dur <= 1800:
            found.append({"title": f"{d.get('title')} (NASA {d['nasa_id']})", "credit": image_sources.nasa_credit(d), "src": src, "dur": dur, "site": "NASA"})
    return found


def pixabay_films(query: str, limit: int = 2, names=()) -> list[dict]:
    """Pixabay stock video: free to use in videos, no credit needed (Pixabay Content License).
    AI-generated clips are skipped (they would pass as real footage). Search replies are cached for
    a day, as Pixabay's API terms ask. [] without a key in pixabay_key.txt."""
    if not PIXABAY_KEY_FILE.exists():
        return []
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": PIXABAY_KEY_FILE.read_text(encoding="utf-8").strip(), "q": query[:100], "per_page": 10, "safesearch": "true"})
    cached = image_sources.CACHE / f"pixabay-{hashlib.sha1(url.encode()).hexdigest()}.json"
    try:
        if cached.exists() and time.time() - cached.stat().st_mtime < 86400:
            raw = cached.read_bytes()
        else:
            raw = media_tools.fetch(url, 30, FILM_UA)
            image_sources.CACHE.mkdir(exist_ok=True)
            cached.write_bytes(raw)
        hits = json.loads(raw).get("hits", [])
    except Exception as e:  # the message never includes the URL, so the key isn't printed
        print(f'    Pixabay search "{query}" failed ({type(e).__name__})')
        return []
    found = []
    for h in hits:
        tags = str(h.get("tags", "")).lower()
        v = (h.get("videos") or {}).get("small") or {}  # 1920x1080, ~5 MB
        if ("ai generated" in tags or not v.get("url") or not 3 <= (h.get("duration") or 0) <= 120
                or not image_sources.on_topic(tags, query, names, strict=True)):  # Pixabay answers anything with modern stock
            continue
        found.append({"title": f"{tags[:60]} (pixabay.com, video {h.get('id')})", "credit": None, "src": v["url"],
                      "dur": float(h["duration"]), "site": "Pixabay"})
    return found[:limit]


def commons_films(query: str, limit: int = 2, names=()) -> list[dict]:
    """Videos on Wikimedia Commons, as their 480p-720p WebM transcodes (seekable)."""
    api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6"
           f"&gsrlimit=10&gsrsearch={urllib.parse.quote(query + ' filetype:video')}&prop=videoinfo"
           "&viprop=url|size|mime|extmetadata|derivatives&viextmetadatafilter=LicenseShortName|Artist|Credit")
    raw = image_sources.wm_get(api, f'Commons film search "{query}"')
    found = []
    for p in json.loads(raw).get("query", {}).get("pages", {}).values() if raw else []:
        info = (p.get("videoinfo") or [{}])[0]
        ok, credit = image_sources.usable_license(info.get("extmetadata", {}))
        webm = [d for d in info.get("derivatives", []) if "/transcoded/" in d.get("src", "")
                and d.get("type", "").startswith("video/webm") and 0 < d.get("height", 0) <= 720]
        if ok and webm and 3 <= (info.get("duration") or 0) <= 1800 and image_sources.on_topic(p["title"], query, names):
            found.append({"title": p["title"], "credit": credit, "src": max(webm, key=lambda d: d["height"])["src"],
                          "dur": info["duration"], "site": "Wikimedia Commons"})
    return found[:limit]


def archive_films(query: str, limit: int = 2, names=(), advertising: bool = False,
                  collection: str | None = None) -> list[dict]:
    """Videos across the entire Internet Archive (historical film, retro gaming, commercials, tech,
    broadcasts, documentaries), ranked by downloads. Non-public-domain uploads credit their creator."""
    clean = " ".join(w for w in plan_rules.words_of(query) if w not in image_sources.STOPWORDS) or re.sub(r"[^\w\s]", " ", query).strip()
    if not clean:
        return []
    clean = re.sub(r"\bmcdonald s\b|\bmcdonalds\b", "mcdonald*", clean, flags=re.I)
    extra = (" AND (title:(commercial OR advertisement OR advertising) OR subject:(commercial OR advertisement OR advertising))"
             if advertising and not collection else "")
    collection_filter = (f" AND collection:{collection}" if collection else
                         "" if advertising else " AND NOT collection:(opensource_audio OR audio OR tv OR television)")
    search = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": f"(title:({clean}) OR subject:({clean})) AND mediatype:movies{extra}{collection_filter}",
         "fl[]": ["identifier", "title", "creator", "licenseurl"], "sort[]": "downloads desc", "rows": 16 if advertising or collection else 6, "output": "json"},
        doseq=True)
    found = []
    try:
        for doc in json.loads(media_tools.fetch(search, 30, FILM_UA)).get("response", {}).get("docs", []):
            if len(found) >= limit:
                break
            ident = doc.get("identifier")
            # "youtube-<id>" items are re-uploads of other creators' YouTube videos (dropped 2026-10-16)
            if not ident or ident.lower().startswith("youtube-"):
                continue
            meta = json.loads(media_tools.fetch(f"https://archive.org/metadata/{urllib.parse.quote(ident)}", 30, FILM_UA))
            md = meta.get("metadata", {})
            if "youtube" in f"{md.get('collection', '')} {md.get('source', '')} {md.get('originalurl', '')}".lower():
                continue
            title = str(md.get("title") or doc.get("title") or ident)
            if not image_sources.on_topic(title, query, names):  # not the uploader's subject list: spam stuffs it with any words
                continue
            mp4 = [f for f in meta.get("files", [])
                   if (f.get("format") in ("h.264", "MPEG4", "h.264 IA") or str(f.get("name", "")).lower().endswith(".mp4"))
                   and f.get("length") and not str(f.get("name", "")).startswith("_")]
            mp4.sort(key=lambda f: ("512kb" not in f.get("name", "").lower(),
                                    (f.get("format") or "").lower() in ("h.264", "h.264 ia")), reverse=True)
            thumbs = sorted((int(m.group(1)), f["name"]) for f in meta.get("files", [])
                            if f.get("format") == "Thumbnail" and (m := re.search(r"_(\d+)\.jpg$", f["name"])))
            try:
                dur = float(mp4[0]["length"]) if mp4 else 0.0
            except ValueError:
                dur = 0.0
            if mp4 and 3 <= dur <= 2400:
                lic = str(md.get("licenseurl") or doc.get("licenseurl") or "").lower()
                creator = md.get("creator") or doc.get("creator") or md.get("uploader") or "Internet Archive"
                if isinstance(creator, list):
                    creator = ", ".join(str(x) for x in creator)
                credit = (None if ("publicdomain" in lic or "cc0" in lic or "zero" in lic) else
                          f"{str(creator).split('@')[0].strip()[:50]}; {lic or 'Rights not specified'}; https://archive.org/details/{ident}")
                base = f"https://archive.org/download/{urllib.parse.quote(ident)}/"
                found.append({"title": f"{title} (archive.org/details/{ident})", "credit": credit,
                              "src": base + urllib.parse.quote(mp4[0]["name"]), "dur": dur,
                              "site": "Duke AdViews" if collection == "adviews" else "Internet Archive",
                              "category": "advertisement" if advertising or collection else "archival",
                              "crop": "preserve", "source_page": f"https://archive.org/details/{ident}",
                              "thumbs": [(t, base + urllib.parse.quote(n)) for t, n in thumbs] if len(thumbs) >= 4 else []})
    except Exception as e:
        print(f'    Internet Archive video search "{query}" failed ({e})')
    return found


def archive_ad_films(query: str, limit: int = 3, names=()) -> list[dict]:
    return archive_films(query, limit, names, advertising=True)


def duke_films(query: str, limit: int = 3, names=()) -> list[dict]:
    if not media_library.source_enabled("duke"):
        return []
    return archive_films(query, limit, names, collection="adviews")


def commercial_queries(queries: list[str]) -> list[str]:
    """Retain product/year/country details from the director; also search the recognized brand alone."""
    out = []
    for query in queries:
        if re.search(r"\b(commercial|advert|advertisement|advertising|campaign|brand|product|menu|packaging)\b", query, re.I):
            out.append(query)
        for brand in media_library.settings().get("brands", []):
            if any(alias.lower() in query.lower() for alias in brand.get("aliases", [])):
                out.extend((query, brand["name"]))
    return list(dict.fromkeys(out))[:3]


def crop_filter(film: dict) -> str:
    return FILM_CROP if film.get("crop") == "legacy" else "null"


def shot_moments(film: dict, maximum: int = 12) -> list[float]:
    """Detect cuts in short ads/local files; bounded work and cached results for network films."""
    if not (film.get("local_path") or film.get("category") == "advertisement") or film["dur"] > 600:
        return []
    cache = image_sources.CACHE / ("shots-" + hashlib.sha256(str(film["src"]).encode()).hexdigest() + ".json")
    if not film.get("local_path"):
        # One bounded stream copy instead of seeking across the internet once per camera shot.
        local = cache.with_suffix(".mkv")
        if not local.exists():
            local.parent.mkdir(parents=True, exist_ok=True)
            temp = local.with_name(local.stem + ".partial.mkv")
            result = image_sources.film_ffmpeg(film, [], ["-t", str(film["dur"]), "-an", "-c:v", "copy", str(temp)], 45)
            if result.returncode or not temp.exists():
                temp.unlink(missing_ok=True)
                return []
            temp.replace(local)
        film["sample_path"] = str(local)
    if cache.exists():
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    result = image_sources.film_ffmpeg(film, ["-loglevel", "info"], ["-an", "-vf", "scale=320:-2,select='gt(scene,0.28)',showinfo",
                                                 "-f", "null", "-"], 45)
    if result.returncode:
        return []
    cuts = [0.0] + [float(t) for t in re.findall(rb"pts_time:([\d.]+)", result.stderr)] + [film["dur"]]
    spans = [(a, b) for a, b in zip(cuts, cuts[1:]) if b - a >= 0.45]
    if len(spans) > maximum:
        spans = [spans[round(k * (len(spans) - 1) / (maximum - 1))] for k in range(maximum)]
    moments = [round((a + b) / 2, 3) for a, b in spans]
    cache.parent.mkdir(parents=True, exist_ok=True)
    media_tools.write_json(cache, moments)
    return moments


def crop_film_bytes(data: bytes) -> bytes:
    """Match FILM_CROP on downloaded thumbnail JPEGs (cut top 6%, bottom 20%, and 4% per side)."""
    try:
        im = Image.open(io.BytesIO(data)).convert("RGB")
        w, h = im.size
        im = im.crop((int(w * 0.04), int(h * 0.06), int(w * 0.96), int(h * 0.80)))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=92)
        return buf.getvalue()
    except Exception:
        return data


def film_frames(film: dict, n: int = 4) -> list[tuple[float, bytes]]:
    """Camera-shot samples for short ads/local videos; otherwise spread samples or Archive thumbnails.
    The original frame is preserved unless the source explicitly asks for the legacy crop."""
    try:
        moments = shot_moments(film)
        if film.get("thumbs") and not moments:
            picks = [film["thumbs"][round(k * (len(film["thumbs"]) - 1) / max(1, n - 1))] for k in range(n)]
            out = []
            for t, url in dict(picks).items():
                try:
                    data = media_tools.fetch(url, 30, FILM_UA)
                    out.append((float(t), crop_film_bytes(data) if film.get("crop") == "legacy" else data))
                except Exception:
                    pass
            if out:
                return out
        dur = film["dur"]
        times = list(moments or film.get("moments") or [])
        n = max(n, len(times))
        for k in range(n):
            if len(times) >= n:
                break
            t = dur * (0.15 + 0.70 * k / max(1, n - 1)) if dur > 90 else dur * (k + 0.5) / n
            if all(abs(t - x) > 4.0 for x in times):
                times.append(t)
        out = []
        for t in sorted(times[:n]):
            try:
                r = image_sources.film_ffmpeg(film, ["-ss", f"{t:.1f}"], ["-frames:v", "1", "-vf", crop_filter(film), "-f", "image2pipe", "-vcodec", "mjpeg", "-"], 25)
                if r.returncode == 0 and r.stdout:
                    out.append((t, r.stdout))
                elif b"timeout" in (r.stderr or b""):
                    break
            except Exception as e:
                print(f"    frame sampling error ({e})")
                break
        return out
    except Exception as e:
        print(f"    film sampling skipped ({film.get('site', 'video')}: {e})")
        return []


def film_piece(film: dict, out: Path) -> tuple[bytes, float] | None:
    """Download ~14s around the chosen moment with original framing and muted source audio.
    Return a full-size still plus its offset in the piece, or None on failure."""
    start = max(0.0, film["t"] - 3)
    try:
        r = image_sources.film_ffmpeg(film, ["-ss", f"{start:.1f}"], ["-t", "14", "-an", "-vf", crop_filter(film), "-c:v", "libx264",
                                                        "-preset", "veryfast", "-crf", "16", str(out)], 300)
        if r.returncode or not out.exists():
            print(f"    film download failed ({r.stderr.decode(errors='replace').strip()[-120:]})")
            return None
        still = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{film['t'] - start:.1f}", "-i", str(out),
                                "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-q:v", "2", "-"],
                               capture_output=True, timeout=60).stdout
        return (still, film["t"] - start) if still else None
    except Exception as e:
        print(f"    film download failed ({e})")
        return None


def shot_span(path: Path, at: float) -> tuple[float, float]:
    """Start and end of the camera shot containing time `at` (newsreels cut to title cards and other
    scenes every few seconds), found with ffmpeg's scene-change detection."""
    log = subprocess.run(["ffmpeg", "-i", str(path), "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    cuts = [float(t) for t in re.findall(r"pts_time:([\d.]+)", log)]
    return max([0.0] + [c for c in cuts if c <= at]), min([media_tools.duration(path)] + [c for c in cuts if c > at])
