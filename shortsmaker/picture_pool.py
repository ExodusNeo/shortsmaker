"""The pictures gathered for a topic before writing, their catalog, cache and contact sheets."""

import hashlib
import io
import json
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from shortsmaker import footage, image_sources, llm, media_tools, plan_rules, rules, session, writing
from shortsmaker.config import FONT


def pictures_of(s: dict) -> str:
    """The topic's usable pictures as prompt lines ("" without a picture list)."""
    cands = load_pool(Path(s["pool_dir"]), thumbs=False) if s.get("pool_dir") and s.get("catalog") else None
    return catalog_text(cands, s["catalog"]) if cands else ""


def clean_pics(s: dict, cands: list[dict]) -> None:
    """The director's `pic` numbers (scenes and evidence-board items), checked: a usable listed picture, never twice,
    at most 2 frames of one film. Anything else becomes None (the picture step then searches for that scene)."""
    ok = {e["n"] for e in s.get("catalog") or [] if is_usable(e)}
    used, per_film = set(), {}

    def check(n, still=False):
        if type(n) is not int or n not in ok or n in used or n > len(cands):
            return None
        f = cands[n - 1].get("film")
        if f and still:  # evidence boards pin prints, never film frames (full_pictures() skips them)
            return None
        if f and per_film.get(f["src"], 0) >= 2:
            return None
        used.add(n)
        if f:
            per_film[f["src"]] = per_film.get(f["src"], 0) + 1
        return n

    for sc in s["scenes"]:
        sc["pic"] = check(sc.get("pic"))
        for it in (sc.get("full") or {}).get("items") or [] if (sc.get("full") or {}).get("type") == "board" else []:
            it["pic"] = check(it.get("pic"), still=True)


def prepare_topic(s: dict, folder: Path | None = None) -> bool:
    """Before writing: the topic's Wikipedia research (`_texts`; fact_check() reuses it), its real pictures and
    footage (a cached pool, else gathered now) and their AI picture list. True when it has the channel's min_real_pictures usable ones (rules file)."""
    s["_texts"] = {t: writing.article_text(t)[:15000] for t in s["wiki_articles"][:4]}
    folder = folder or pool_folder(s["topic"])
    cands = load_pool(folder)
    if cands is None:
        cands = gather_pool(s["wiki_articles"], s.get("people", []), s.get("visual_terms", []), s.get("visual_terms", []))
        if len(cands) < rules.min_real_pictures():  # can't pass: no AI call, and not cached (a network blip may have caused it)
            s.update(catalog=[], pool_dir=None, picture_check=f"0 usable of {len(cands)}")
            return False
        save_pool(folder, cands)
    s["catalog"] = catalog_pool(s, cands, folder)
    good = usable(cands, s["catalog"])
    s["pool_dir"], s["picture_check"] = str(folder), f"{len(good)} usable of {len(cands)}"
    return len(good) >= rules.min_real_pictures()


TOPIC_BACKUPS = 2


def contact_sheets(cands: list[dict], folder: Path, per_sheet: int = 24) -> list[Path]:
    """Numbered thumbnail grids (6x4) so Claude can look at every candidate at once."""
    folder.mkdir(parents=True, exist_ok=True)
    tile, cols, font = 300, 6, ImageFont.truetype(FONT, 46)
    sheets = []
    for s in range(0, len(cands), per_sheet):
        batch = cands[s:s + per_sheet]
        rows = (len(batch) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tile, rows * tile), (24, 24, 30))
        d = ImageDraw.Draw(sheet)
        for k, c in enumerate(batch):
            x, y = (k % cols) * tile, (k // cols) * tile
            if c.get("thumb"):
                try:
                    im = Image.open(io.BytesIO(c["thumb"])).convert("RGB")
                    im.thumbnail((tile - 12, tile - 12))
                    sheet.paste(im, (x + (tile - im.width) // 2, y + (tile - im.height) // 2))
                except Exception:
                    pass  # unreadable thumbnail: the tile stays blank and Claude skips it
            num = str(s + k + 1)
            d.rectangle((x + 4, y + 4, x + 18 + 26 * len(num), y + 58), fill=session.YELLOW)
            d.text((x + 11, y + 6), num, font=font, fill="black")
        path = folder / f"sheet{len(sheets) + 1}.png"
        sheet.save(path)
        sheets.append(path)
    return sheets


def gather_pool(articles: list[str], people: list[str], image_terms: list[str], video_terms: list[str],
                skip: set[str] = frozenset(), limit: int = 64, film_limit: int = 14) -> list[dict]:
    """Candidate pictures (with preview `thumb` bytes) and sampled real-film frames from every allowed source:
    Wikipedia article images, Commons, Openverse, Internet Archive, NASA stills, then Internet Archive, Commons,
    Pixabay and NASA videos (4 frames each). Only previews are fetched; full files download when picked.
    `skip`: picture urls and video sources already gathered (nothing is downloaded twice); at most `limit` stills
    and `film_limit` videos."""
    pool: dict[str, dict] = {}

    def add(cands: list[dict]) -> None:
        for c in cands:
            pool.setdefault(c["url"], c)

    names, scene_imgs, scene_vids = list(people), list(dict.fromkeys(image_terms)), list(dict.fromkeys(video_terms))
    articles = list(dict.fromkeys(list(articles) + names))[:7]

    for title in articles:
        add(image_sources.article_images(title))
    for q in scene_imgs:
        hits = image_sources.commons_search(q)
        if len(hits) < 2 and len(q.split()) > 2:
            hits += image_sources.commons_search(" ".join(q.split()[:2]), 2)
        add(hits)
    for name in dict.fromkeys(names):
        surname = plan_rules.words_of(name)[-1:]
        add([c for c in image_sources.commons_search(f"{name} portrait", 3) if plan_rules.contains(plan_rules.words_of(c["title"]), surname)])
    for q in list(dict.fromkeys(articles[:3] + scene_imgs[:4]))[:6]:  # Openverse (museums/Flickr/archives) + Internet Archive
        add(image_sources.openverse_images(q, 3) + image_sources.archive_images(q, 3))
    for q in articles[:2]:
        add(image_sources.nasa_images(q, 2))
    cands = [c for c in pool.values() if c["url"] not in skip][:limit]

    def load_thumb(c: dict) -> dict | None:
        c["thumb"] = image_sources.get_image(c["small"], "thumbnail") or (
            image_sources.get_image(c["url"], "thumbnail") if c["small"] != c["url"] else None)
        return c if c["thumb"] else None

    with ThreadPoolExecutor(4) as ex:
        cands = [c for c in ex.map(load_thumb, cands) if c]

    # Video footage research: Internet Archive, Wikimedia Commons, Pixabay and NASA. No other creators' YouTube
    # videos: since Oct 2026 YouTube cuts the Shorts reach of content re-uploaded from other creators.
    films: list[dict] = []
    other_queries = list(dict.fromkeys(articles[:3] + scene_vids[:5]))
    for search, cap, queries in ((footage.archive_films, 4, other_queries[:6]),
                                 (footage.commons_films, 4, other_queries[:5]),
                                 (footage.pixabay_films, 4, list(dict.fromkeys(scene_vids[:5] + scene_imgs[:4]))[:6]),
                                 (footage.nasa_films, 2, articles[:3])):
        got: dict[str, dict] = {}
        for q in queries:
            if len(got) < cap:
                got.update({f["src"]: f for f in search(q) if f["src"] not in skip})
        films += list(got.values())[:cap]
    films = films[:film_limit]

    if films:
        print(f"  sampling frames from {len(films)} archival/stock videos...")
        with ThreadPoolExecutor(4) as ex:
            sampled = list(ex.map(footage.film_frames, films))
        for f, frames in zip(films, sampled):
            cands += [{"title": f["title"], "url": f"{f['src']}#t={t:.0f}", "credit": f["credit"], "thumb": jpg,
                       "source": f"REAL FILM ({f['site']}: {f['credit'] or 'no credit needed'}), frame at {media_tools.clock(t)}",
                       "film": {**f, "t": t}, "site": f["site"]}
                      for t, jpg in frames]
    return cands


def pool_folder(topic: str) -> Path:
    return image_sources.POOLS / hashlib.sha1(topic.encode("utf-8")).hexdigest()[:12]


def save_pool(folder: Path, cands: list[dict]) -> None:
    """pool.json (the candidates without bytes) + thumb<k>.jpg; list positions are the picture numbers."""
    folder.mkdir(parents=True, exist_ok=True)
    for k, c in enumerate(cands):
        (folder / f"thumb{k}.jpg").write_bytes(c["thumb"])
    rows = [{key: v for key, v in c.items() if key != "thumb"} for c in cands]
    media_tools.write_json(folder / "pool.json", rows)


def load_pool(folder: Path, thumbs: bool = True) -> list[dict] | None:
    """The saved pool (None if missing or unreadable: it is gathered again); thumbs=False skips the preview bytes."""
    try:
        rows = json.loads((folder / "pool.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return [{**c, "thumb": (folder / f"thumb{k}.jpg").read_bytes()} if thumbs else c for k, c in enumerate(rows)]


def prune_cache() -> None:
    """Drop cached downloads and topic pools older than 30 days."""
    old = lambda p: time.time() - p.stat().st_mtime > 30 * 86400  # noqa: E731
    for f in image_sources.CACHE.glob("*") if image_sources.CACHE.exists() else []:
        if f.is_file() and old(f):
            f.unlink()
    for d in image_sources.POOLS.glob("*") if image_sources.POOLS.exists() else []:
        if d.is_dir() and old(d / "pool.json" if (d / "pool.json").exists() else d):
            shutil.rmtree(d, ignore_errors=True)


def catalog_pool(s: dict, cands: list[dict], folder: Path) -> list[dict]:
    """The picture list the writer, editor and director plan with: the AI looks at the topic's numbered contact
    sheets once and describes every picture. Reused from folder/catalog.json; both AIs are tried, and if neither
    answers, the run stops (owner, 2026-10-19: no Short without its picture list)."""
    try:
        return json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # missing or half-written: list it again
    if not cands:
        return []
    sheets = contact_sheets(cands, folder / "sheets")
    titles = [f"{k + 1}: {c['title']} ({c['source']})" for k, c in enumerate(cands)]
    print(f"  {session.BRAIN.capitalize()} is listing the {len(cands)} pictures/frames found for \"{s['subject']}\"...")
    prompt = f"""You are the picture researcher for a YouTube Short about: {s['topic']} (subject: {s['subject']}).
Before any script is written, describe every numbered candidate so the writer can build the story around the
real pictures that exist. Candidates whose source says REAL FILM are frames of real video footage.
Open and look at every contact sheet:
{chr(10).join(str(x) for x in sheets)}
For EVERY number give:
- what: what it really shows, 12 words or fewer (people, place, object, event; "film:" frames say what moves);
{session.RULES["Opening picture"]}
- reject: null, or why it must never be used: graphic violence, torture, executions, corpses or suffering; a
  watermark or channel logo; burned-in subtitles, captions or "subscribe" text (film frames already had their top
  6% and bottom 20% cropped); a printed caption naming a different event, place or person.
For reference, their file titles: {json.dumps(titles, ensure_ascii=False)}
Reply with ONLY JSON: {{"pictures": [{{"n": 1, "what": "...", "era_ok": true, "sharp": 3, "hook": false, "reject": null}}]}}"""
    data = llm.ask_ai(prompt, fatal=False, read_dir=folder / "sheets", bulk=True)
    out = catalog_entries(data, len(cands))
    if data is not None and not out:  # valid JSON but no usable entry: ask_ai only falls back on broken JSON
        if not session.SOLO:
            other = "gemini" if session.LAST_AI == "claude" else "claude"
            print(f"  {session.LAST_AI.capitalize()}'s picture list was empty, asking {other.capitalize()} instead")
            out = catalog_entries(llm.ask_ai(prompt, fatal=False, read_dir=folder / "sheets", brain=other, bulk=True), len(cands))
        else:
            print(f"  {session.LAST_AI.capitalize()}'s picture list was empty, retrying with {session.BRAIN.capitalize()}...")
            out = catalog_entries(llm.ask_ai(prompt, fatal=False, read_dir=folder / "sheets", brain=session.BRAIN, bulk=True), len(cands))
    if not out:
        sys.exit(f'Stopped: no picture list for "{s["topic"]}". The AI ({session.BRAIN.capitalize()}) did not give a usable answer '
                 "(their messages are above). Run again later." if session.SOLO else
                 f'Stopped: no picture list for "{s["topic"]}". Neither Claude nor Gemini gave a usable answer '
                 "(their messages are above). Run again later.")
    folder.mkdir(parents=True, exist_ok=True)
    media_tools.write_json(folder / "catalog.json", out)
    return out


def catalog_entries(data: dict | None, n_cands: int) -> list[dict]:
    """The valid entries of a picture-list reply (LLM output is untrusted)."""
    out, seen = [], set()
    for e in (data or {}).get("pictures") or [] if isinstance((data or {}).get("pictures"), list) else []:
        n = e.get("n") if isinstance(e, dict) else None
        sharp = e.get("sharp") if isinstance(e, dict) else None
        if not (type(n) is int and 1 <= n <= n_cands and n not in seen and type(sharp) is int and 1 <= sharp <= 3):
            continue
        seen.add(n)
        reject = str(e["reject"]).strip()[:120] if e.get("reject") else None
        out.append({"n": n, "what": str(e.get("what") or "").strip()[:100], "era_ok": e.get("era_ok") is True,
                    "sharp": sharp, "hook": e.get("hook") is True, "reject": reject})
    return out


def is_usable(e: dict) -> bool:
    return not e["reject"] and e["era_ok"] and e["sharp"] >= 2


def usable(cands: list[dict], catalog: list[dict]) -> list[dict]:
    """Usable list entries for the topic check: all frames of one video count once (its sharpest frame)."""
    best: dict[str, dict] = {}
    for e in sorted(filter(is_usable, catalog), key=lambda e: -e["sharp"]):
        f = cands[e["n"] - 1].get("film")
        best.setdefault(f["src"] if f else cands[e["n"] - 1]["url"], e)
    return sorted(best.values(), key=lambda e: e["n"])


def catalog_text(cands: list[dict], catalog: list[dict]) -> str:
    """The usable pictures as prompt lines: "#12 film: 1944 newsreel of rubber tanks [opener]"."""
    return "\n".join(f"#{e['n']} {'film' if cands[e['n'] - 1].get('film') else 'photo'}: {e['what']}"
                     + (" [opener]" if e["hook"] else "") for e in catalog if is_usable(e))
