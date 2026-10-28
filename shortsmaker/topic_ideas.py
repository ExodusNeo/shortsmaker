"""Our own topic research (2026-10-28, owner: "research our own topics instead of copying the titles"): story ideas
from Wikipedia's "Unusual articles" pages (true, sourced, little-known: each a linked article plus one line on why
it is odd), given to the topic picker instead of proven channels' titles. Those channels' recent Shorts are only a
list of stories to stay away from (`clash`): Voggle's Mike the Headless Chicken had 2M views against our 1.2K, so a
story a big channel just told is one we lose. Pages per channel: `idea_pages` in the rules file's Settings."""

import json
import random
import re
import time
import urllib.parse

from shortsmaker import config, image_sources

CACHE = config.ROOT / "cache" / "ideas"
REFRESH_DAYS = 30
DEFAULT_PAGES = ["History", "Military", "Death", "Science", "Society, economy and law",
                 "Technology, inventions and products", "Food", "Places and infrastructure", "Sports", "Folklore"]
STOP = {"the", "and", "for", "with", "from", "that", "this", "was", "his", "her", "who", "how", "why", "what"}


def parse_ideas(text: str) -> list[dict]:
    """[{"title": article, "why": its one line}] from an Unusual articles page's wikitext (table rows)."""
    out = []
    for row in text.split("\n|-"):
        m = re.search(r"'''\[\[([^\]|]+)[^\]]*\]\]'''[^\n]*\n\|(.+)", row)
        if not m:
            continue
        why = re.sub(r"\{\{[^{}]*\}\}", "", m[2])
        why = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", why).replace("'''", "").replace("''", "")
        out.append({"title": m[1].strip(), "why": " ".join(why.split())})
    return out


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) >= 3 and w not in STOP}


def clash(name: str, texts: list[str]) -> str | None:
    """The first text that holds every real word of `name` ("Mike the Headless Chicken" in "The True Story of Mike
    the Headless Chicken"), else None. A name of fewer than 2 real words never clashes: one word ("War") is too
    common to judge by."""
    want = _words(name)
    if len(want) < 2:
        return None
    return next((t for t in texts if want <= _words(t)), None)


def pages() -> list[str]:
    """The channel's Unusual articles pages (`idea_pages: History; Military` in Settings), else DEFAULT_PAGES."""
    from shortsmaker import session
    raw = session.RULE_SETTINGS.get("idea_pages", "")
    # the rules parser lowercases values; the pages are named in sentence case ("Society, economy and law")
    return [p.strip()[0].upper() + p.strip()[1:] for p in raw.split(";") if p.strip()] or DEFAULT_PAGES


def fetch_ideas(names: list[str]) -> list[dict]:
    """Every idea on these pages, each page cached for REFRESH_DAYS (a stale copy is used when Wikipedia is down)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    ideas = []
    for name in names:
        path = CACHE / (re.sub(r"[^a-z0-9]+", "_", name.lower()) + ".json")
        cached = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        if not cached or time.time() - cached["fetched"] > REFRESH_DAYS * 86400:
            page = urllib.parse.quote(f"Wikipedia:Unusual articles/{name}", safe="")
            raw = image_sources.wm_get("https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=wikitext"
                                       f"&page={page}", f"Unusual articles: {name}")
            text = (json.loads(raw).get("parse") or {}).get("wikitext", {}).get("*", "") if raw else ""
            if text:
                cached = {"fetched": time.time(), "ideas": parse_ideas(text)}
                path.write_text(json.dumps(cached, ensure_ascii=False), encoding="utf-8")
        ideas += (cached or {}).get("ideas", [])
    return ideas


def pick_ideas(ch: dict, taken: list[str], k: int = 60, rng: random.Random | None = None) -> list[dict]:
    """k ideas for today's topic picker: none we already made (done_topics) or a proven channel just posted (taken)."""
    seen, fresh = set(), []
    for idea in fetch_ideas(pages()):
        if idea["title"] in seen or clash(idea["title"], ch.get("done_topics") or []) or clash(idea["title"], taken):
            continue
        seen.add(idea["title"])
        fresh.append(idea)
    return (rng or random.Random()).sample(fresh, min(k, len(fresh)))
