"""Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with licences and
on-screen credits."""

import hashlib
import json
import re
import subprocess
import threading
import time
import urllib.error
import urllib.parse

from PIL import Image, ImageDraw, ImageFont

from shortsmaker import footage, media_tools, plan_rules
from shortsmaker.config import ROOT


_last_wm = 0.0
_wm_lock = threading.Lock()
# Wikimedia's User-Agent policy wants contact info; without it nearly every request gets a 429.
WM_UA = "ShortsMaker/1.0 (gutierrezdishann@gmail.com) python-urllib"
CACHE = ROOT / "cache"  # downloaded Wikimedia images, pruned after 30 days
POOLS = CACHE / "pools"  # per topic: the pictures gathered before writing + their AI picture list
IMG_PROPS = "&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiextmetadatafilter=LicenseShortName|Artist|Credit"
# Wikimedia serves thumbnails only at these widths; anything else (or bulk original files) gets
# rate-limited with a 10-minute ban (mediawiki.org/wiki/Common_thumbnail_sizes).
THUMB_STEPS = [330, 500, 960, 1280, 1920]
# File-title words that mean "not a scene image": signatures, heraldry, site furniture, diagrams, Wiki icons.
JUNK = {"signature", "autograph", "logo", "icon", "coat", "arms", "flag", "seal", "symbol", "emblem",
        "blank", "placeholder", "stub", "diagram", "chart", "graph", "plaque", "barnstar", "wikipedia",
        "cscr", "oojs", "shackle", "padlock", "ambox", "portal", "nuvola", "wpvg"}
STOPWORDS = {"the", "and", "for", "with", "from", "that", "this", "into", "over", "under", "about",
             "how", "why", "who", "what", "when", "where", "was", "were", "are", "his", "her", "its",
             "out", "old", "new", "one", "two", "first", "last", "most", "more", "some", "any"}
JUNK_VIDEO = {"reaction", "reacts", "podcast", "tierlist", "unboxing", "lyric", "lyrics", "karaoke",
              "livestream", "asmr", "reupload", "compilation", "parody", "animated", "animation",
              "cartoon", "gmod", "sfm", "meme", "memes", "soundtrack", "ost", "remix", "lego"}


def wm_get(url: str, what: str = "Wikimedia request", gap: float = 1.0) -> bytes | None:
    """GET from Wikimedia, spaced `gap` seconds apart, with a short backoff on rate limits (HTTP 429).
    Long bans are not waited out: that one request is skipped. Image files are cached on disk, so
    nothing is downloaded twice. None on failure."""
    global _last_wm
    cached = CACHE / hashlib.sha1(url.encode()).hexdigest() if "upload.wikimedia.org" in url else None
    if cached and cached.exists():
        return cached.read_bytes()
    for attempt in range(3):
        with _wm_lock:
            time.sleep(max(0.0, _last_wm + gap - time.time()))
            _last_wm = time.time()
        try:
            data = media_tools.fetch(url, ua=WM_UA)
            if cached:
                CACHE.mkdir(exist_ok=True)
                cached.write_bytes(data)
            return data
        except urllib.error.HTTPError as e:
            wait = int(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1)
            if e.code != 429 or attempt == 2 or wait > 30:
                print(f"    {what} failed ({e.code}), skipping it")
                return None
            print(f"    Wikimedia busy, waiting {wait}s...")
            time.sleep(wait)
        except Exception as e:
            print(f"    {what} failed ({e})")
            return None
    return None


def thumb_url(original: str, width: int, orig_w: int) -> str:
    """URL of a standard-size Wikimedia thumbnail: the largest allowed step that fits in the image
    (capped at `width`), or the original file if it's smaller than every step."""
    original = original.split("?", 1)[0]  # the API adds tracking parameters to file URLs
    w = max((st for st in THUMB_STEPS if st <= width and st < orig_w), default=0)
    if not w or "/thumb/" in original:
        return original
    site, _, rest = original.partition("/wikipedia/")
    project, _, path = rest.partition("/")
    return f"{site}/wikipedia/{project}/thumb/{path}/{w}px-{path.rsplit('/', 1)[-1]}"


def usable_license(meta: dict) -> tuple[bool, str | None]:
    """(ok, credit). Public domain/CC0 need no credit; all other Wikimedia/Wikipedia media (CC BY,
    CC BY-SA, Attribution, GFDL, Fair use screenshots/covers) is allowed and credited on screen + in upload.txt."""
    lic = re.sub(r"<[^>]+>", "", meta.get("LicenseShortName", {}).get("value", "")).strip()
    low = lic.lower()
    if "public domain" in low or "cc0" in low or low.startswith("pd"):
        return True, None
    raw_artist = meta.get("Artist", {}).get("value", "") or meta.get("Credit", {}).get("value", "")
    artist = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw_artist)).strip()
    if artist and lic:
        return True, f"{artist[:55]}, {lic[:20]}"
    return True, (artist[:60] or lic[:40] or "Wikimedia")


def wm_files(api_url: str, source: str) -> list[dict]:
    """Usable images from a Wikimedia/Wikipedia API query: photos, screenshots, paintings and art,
    big enough (250px+ so retro game screenshots and portraits qualify), not a thin strip or icon."""
    raw = wm_get(api_url, f"{source} lookup")
    if not raw:
        return []
    found = []
    for p in json.loads(raw).get("query", {}).get("pages", {}).values():
        info = (p.get("imageinfo") or [{}])[0]
        ok, credit = usable_license(info.get("extmetadata", {}))
        w, h = info.get("width", 0), info.get("height", 1) or 1
        if (ok and info.get("mime") in ("image/jpeg", "image/png") and w >= 250 and 0.33 <= w / h <= 3
                and not JUNK & set(plan_rules.words_of(p["title"]))):
            found.append({"title": p["title"], "url": thumb_url(info["url"], 1920, w), "credit": credit,
                          "small": thumb_url(info["url"], 330, w), "source": source, "size": w * h})
    return sorted(found, key=lambda c: -c["size"])


def commons_search(query: str, limit: int = 4) -> list[dict]:
    api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
           f"&gsrsearch={urllib.parse.quote(query + ' filetype:bitmap')}&gsrnamespace=6&gsrlimit=20" + IMG_PROPS)
    return wm_files(api, f'Commons search "{query}"')[:limit]


def article_images(title: str, limit: int = 12) -> list[dict]:
    """Images used in an English Wikipedia article: chosen by editors, so almost always on topic."""
    api = ("https://en.wikipedia.org/w/api.php?action=query&format=json&redirects=1&generator=images"
           f"&gimlimit=60&titles={urllib.parse.quote(title)}" + IMG_PROPS)
    return wm_files(api, f'Wikipedia "{title}"')[:limit]


_last_ov = 0.0
_ov_lock = threading.Lock()


def ov_get(url: str) -> bytes | None:
    """GET from Openverse, spaced to its anonymous limit (20 requests a minute). None on failure."""
    global _last_ov
    with _ov_lock:
        time.sleep(max(0.0, _last_ov + 3.1 - time.time()))
        _last_ov = time.time()
    try:
        return media_tools.fetch(url, 30, footage.FILM_UA)
    except Exception as e:
        print(f"    Openverse request failed ({e})")
        return None


def get_image(url: str, what: str) -> bytes | None:
    """Wikimedia files via wm_get() (contact User-Agent, spacing, cache), Openverse via its rate
    limit, Internet Archive services/img upgraded to the full-res item file on full downloads,
    anything else (museums, NASA) as a plain download. None on failure."""
    if "wikimedia.org" in url:
        return wm_get(url, what)
    if "api.openverse.org" in url:
        return ov_get(url)
    if url.startswith("https://archive.org/services/img/") and what != "thumbnail":
        ident = url.removeprefix("https://archive.org/services/img/").split("?")[0]
        cached = CACHE / f"ia-{hashlib.sha1(ident.encode()).hexdigest()}"
        if cached.exists():
            return cached.read_bytes()
        try:
            meta = json.loads(media_tools.fetch(f"https://archive.org/metadata/{ident}", 15, footage.FILM_UA))
            host, folder = meta.get("d1") or meta.get("d2"), meta.get("dir")
            name = next((f["name"] for f in meta.get("files", [])
                         if str(f.get("name", "")).lower().endswith((".jpg", ".jpeg", ".png"))
                         and not str(f["name"]).endswith("_thumb.jpg") and f["name"] != "__ia_thumb.jpg"), None)
            if host and folder and name:
                data = media_tools.fetch(f"https://{host}{folder}/{urllib.parse.quote(name)}", 30, footage.FILM_UA)
                CACHE.mkdir(exist_ok=True)
                cached.write_bytes(data)
                return data
        except Exception:
            pass
    try:
        return media_tools.fetch(url, 60, footage.FILM_UA)
    except Exception as e:
        print(f"    {what} failed ({e})")
        return None


def openverse_images(query: str, limit: int = 4) -> list[dict]:
    """Images from museums, archives and photographers through Openverse (no key), including CC BY,
    CC BY-SA and Flickr; Wikimedia is searched directly. Creators are credited on screen + in upload.txt."""
    raw = ov_get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": query, "license": "cc0,pdm,by,by-sa,by-nc,by-nc-sa", "excluded_source": "wikimedia", "page_size": 20}))
    found = []
    for r in (json.loads(raw).get("results", []) if raw else []):
        w, h = r.get("width"), r.get("height")
        lic = str(r.get("license") or "").lower()
        if not r.get("url") or (w and h and (w < 300 or not 0.33 <= w / h <= 3)):
            continue
        credit = None if lic in ("cc0", "pdm") else (
            f"{str(r.get('creator') or r.get('source') or 'unknown')[:60]}, CC {lic.upper()} {r.get('license_version') or ''}".strip())
        found.append({"title": f"{r.get('title') or 'untitled'} ({r.get('source')})", "url": r["url"],
                      "small": r.get("thumbnail") or r["url"], "credit": credit, "source": f"Openverse: {r.get('source')}",
                      "site": "Openverse"})
    return found[:limit]


def nasa_search(query: str, media: str) -> list[dict]:
    try:
        return json.loads(media_tools.fetch("https://images-api.nasa.gov/search?" + urllib.parse.urlencode(
            {"q": query, "media_type": media}), 30, footage.FILM_UA))["collection"]["items"]
    except Exception as e:
        print(f'    NASA search "{query}" failed ({e})')
        return []


def nasa_images(query: str, limit: int = 3) -> list[dict]:
    """NASA photos (public domain), when the story touches space, flight or science."""
    found = []
    for it in nasa_search(query, "image"):
        d = (it.get("data") or [{}])[0]
        preview = next((l["href"] for l in it.get("links", []) if l.get("render") == "image"), None)
        if preview and on_topic(f"{d.get('title', '')} {str(d.get('description', ''))[:300]}", query):
            found.append({"title": f"{d.get('title')} (NASA {d.get('nasa_id')})", "url": preview.replace("~thumb", "~large"),
                          "small": preview, "credit": None, "source": "NASA", "site": "NASA"})
    return found[:limit]


CREDIT_SECONDS = 2.8  # the on-screen credit tag shows this long at the start of its scene, then fades
# owner (2026-10-19): credits at the bottom, just above YouTube's channel name/title (lower is covered by the app)
CREDIT_Y = 1500
CREDIT_ORGS = {"library", "museum", "archive", "archives", "studies", "collection", "university", "society", "government",
               "department", "office", "agency", "news", "service", "institute", "commons", "user"}


def short_credit(credit: str, film: bool = False, max_len: int = 44) -> str:
    """The on-screen credit tag: kind, a short name and the licence ("Photo: E. Mariz · CC BY 2.0"). The full
    credit stays in upload.txt. A long name loses whole words from its end, never letters mid-word."""
    credit = re.sub(r"https?://(?:www\.)?([^/\s,]+)[^\s,]*(?:\s+https?://[^\s,]*)*", r"\1", credit)  # links -> first domain
    lic = re.search(r",\s*((?:CC[ -]?(?:BY|0)[A-Z-]*|public domain|GFDL)(?:[ -][\d.]+)?)\s*$", credit, re.I)
    name = re.split(r"\s+from\s+|,", credit[:lic.start()] if lic else credit)[0].strip()
    words = name.split()
    if 2 <= len(words) <= 3 and all(w[:1].isupper() for w in words) and not CREDIT_ORGS & {w.lower() for w in words}:
        name = f"{words[0][0]}. {' '.join(words[1:])}"  # a person: initial + surname
    head, tail = ("Video: " if film else "Photo: "), (f" · {lic.group(1)}" if lic else "")
    while len(head + name + tail) > max_len and " " in name:
        name = name.rsplit(" ", 1)[0]
    return head + name + tail


def credit_tag_image(text: str) -> Image.Image:
    """Small credit label (bottom-left, CREDIT_Y) while credited material (YouTube channel, CC, Archive) is on screen."""
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    tw = int(font.getlength(text))
    img = Image.new("RGBA", (tw + 20, 34))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, tw + 20, 34), radius=8, fill=(0, 0, 0, 130))
    d.text((10, 5), text, font=font, fill=(255, 255, 255, 225))
    return img


def on_topic(title: str, query: str) -> bool:
    """Keep titles that share at least one meaningful word (including 2-3 letter terms like NES, N64,
    GTA, ET, UFO) with the query; the visual editor still inspects every frame."""
    q_words = {w for w in plan_rules.words_of(query) if len(w) >= 2 and w not in STOPWORDS} or set(plan_rules.words_of(query))
    return bool(q_words & set(plan_rules.words_of(title)))


def archive_images(query: str, limit: int = 3) -> list[dict]:
    """Still images, magazine/manual scans, art and archival photos from the Internet Archive."""
    clean = " ".join(w for w in plan_rules.words_of(query) if w not in STOPWORDS) or re.sub(r"[^\w\s]", " ", query).strip()
    if not clean:
        return []
    search = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": f"(title:({clean}) OR subject:({clean})) AND mediatype:image",
         "fl[]": ["identifier", "title", "creator", "licenseurl"], "sort[]": "downloads desc", "rows": 6, "output": "json"},
        doseq=True)
    found = []
    try:
        for doc in json.loads(media_tools.fetch(search, 30, footage.FILM_UA)).get("response", {}).get("docs", []):
            if len(found) >= limit:
                break
            ident = doc.get("identifier")
            if not ident:
                continue
            title = str(doc.get("title") or ident)
            if not on_topic(title, query) or JUNK & set(plan_rules.words_of(title)):
                continue
            lic = str(doc.get("licenseurl") or "").lower()
            creator = doc.get("creator") or "Internet Archive"
            if isinstance(creator, list):
                creator = ", ".join(str(x) for x in creator)
            credit = None if ("publicdomain" in lic or "cc0" in lic or "zero" in lic) else str(creator).split("@")[0].strip()[:50]
            thumb = f"https://archive.org/services/img/{urllib.parse.quote(ident)}"
            found.append({"title": f"{title} (archive.org/details/{ident})", "url": thumb, "small": thumb,
                          "credit": credit, "source": "Internet Archive", "site": "Internet Archive"})
    except Exception as e:
        print(f'    Internet Archive image search "{query}" failed ({e})')
    return found


def film_ffmpeg(film: dict, before: list[str], after: list[str], timeout: int) -> subprocess.CompletedProcess:
    """ffmpeg reading a film over HTTP. Wikimedia gets the contact User-Agent, the same 1s spacing as
    wm_get() and a short wait on rate limits (HTTP 429); a seek is several requests, so it trips them."""
    global _last_wm
    wiki = film["site"] == "Wikimedia Commons"
    for attempt in range(3):
        if wiki:
            with _wm_lock:
                time.sleep(max(0.0, _last_wm + 1.0 - time.time()))
                _last_wm = time.time()
        ua = film.get("ua") or (WM_UA if wiki else footage.FILM_UA)  # YouTube streams need yt-dlp's own User-Agent
        try:
            r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *before, "-user_agent", ua,
                                "-i", film["src"], *after], capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"    film fetch timed out after {timeout}s ({film.get('site', 'video')})")
            return subprocess.CompletedProcess(args=[], returncode=1, stdout=b"", stderr=b"timeout")
        except Exception as e:
            print(f"    film fetch error ({e})")
            return subprocess.CompletedProcess(args=[], returncode=1, stdout=b"", stderr=str(e).encode())
        if b"429" not in r.stderr or attempt == 2:
            return r
        print("    Wikimedia busy, waiting 10s...")
        time.sleep(10)
    return r
