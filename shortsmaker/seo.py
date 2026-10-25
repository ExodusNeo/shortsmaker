"""Titles, descriptions and tags from YouTube autocomplete; the .srt captions file."""

import json
import re
import urllib.parse
from pathlib import Path

from shortsmaker import channel_profiles, llm, logbook, media_tools, session


def search_suggestions(query: str) -> list[str]:
    """What people actually type into YouTube search (free autocomplete endpoint, no key)."""
    try:
        url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q="
               + urllib.parse.quote(query))
        return json.loads(media_tools.fetch(url, timeout=15))[1]
    except Exception:
        return []


def seo_pass(shorts: list[dict], ch: dict | None = None) -> None:
    """Rewrite title/description/tags around real YouTube search phrases; add a pinned comment."""
    if not shorts:
        return
    print("Researching search keywords...")
    ch = ch or (channel_profiles.load_channel() if session.CHANNEL.is_file() else {})
    niche = ch.get("niche", "")
    leaders = [t["title"] for t in channel_profiles.trend_research(ch)[:15]] if niche else []  # cached for the day
    results = logbook.logbook_results()
    research = []
    rseeds = ch.get("research_seeds") or {}
    ch_queries = (rseeds.get("queries", []) if isinstance(rseeds, dict)
                  else rseeds if isinstance(rseeds, list) else [])
    for i, s in enumerate(shorts):
        subject = s.get("subject") or s["title"]
        query_candidates = ([subject, f"{subject} explained", f"why {subject}"]
                            + (s.get("wiki_articles") or [])[1:3]
                            + (s.get("search_terms") or [])[:4]
                            + ch_queries[:2])
        seeds = dict.fromkeys([q.strip() for q in query_candidates if isinstance(q, str) and q.strip()])
        suggestions = {q: got for q in seeds if (got := search_suggestions(q))}  # each list: most-searched first
        first_narration = s["scenes"][0]["narration"].strip() if s.get("scenes") and s["scenes"][0].get("narration") else ""
        research.append({"index": i, "subject": subject, "title": s["title"], "description": s.get("description", ""),
                         "hook_sentence": re.split(r"(?<=[.!?])\s+", first_narration)[0] if first_narration else "",
                         "hook_text": s.get("hook_text"), "thumbnail_text": s.get("thumbnail_text"),
                         "script": " ".join(sc.get("narration", "") for sc in s.get("scenes", [])),
                         "fact_check_corrections": s.get("fact_check", []),
                         "youtube_search_suggestions": suggestions})
    data = llm.ask_ai(f"""You are a YouTube SEO & Shorts Feed strategist for a Shorts channel{f' in this niche: {niche}' if niche else ''}. For each Short
below you get its draft metadata, its script, what viewers see in the first second (hook_sentence
spoken, hook_text big on screen, thumbnail_text), and REAL YouTube autocomplete phrases, grouped by what
was typed, each list in YouTube's order: most-searched first (some are irrelevant, e.g. unrelated songs
or movies with the same name: ignore those).
{f"Titles of the top recent Shorts in this niche, by views per day (learn their patterns, never copy them):{chr(10)}{json.dumps(leaders, ensure_ascii=False)}{chr(10)}" if leaders else ""}{f"How our own posted Shorts did (title, views, notes):{chr(10)}{results}{chr(10)}" if results else ""}For each Short write:
- title: under 60 characters, and its first 40 characters must work alone (the Shorts player and shelf cut
  the rest). Lead with the scroll-stopping anomaly, dollar figure, or broadly famous anchor entity (e.g.
  "NBA", "Wall Street", "$800M", "U.S. Navy", "Fake Bonds")—NEVER start the title with an obscure person's
  or company's name that casual viewers don't already recognize, and NEVER use dry textbook phrasing ("The X
  of Y in 1923") or pipe suffixes ("| Match King"). Write a punchy human curiosity hook (e.g. "How a Dead
  Team Made $800M Off the NBA", "How the 'Match King' Bought Countries With Fake Bonds", "He Bought 98% of
  a Stock—So Wall Street Changed the Rules"). It must promise what the hook delivers without repeating
  hook_sentence, hook_text or thumbnail_text word-for-word. No "#shorts", no emoji, no clickbait that the
  video doesn't deliver.
- Title, description and pinned comment may only claim what the script says. fact_check_corrections
  lists claims our fact check removed as false or unproven: never bring one back.
- description: Sentence 1 MUST naturally include both the exact historical subject/person name (`subject`)
  and the main search phrase (it shows in search results and indexes exact-name queries); Sentence 2-3
  weaves in a broader category/mechanism search phrase (e.g. "short squeeze", "contract loophole",
  "financial fraud"); 2-3 sentences total; then a new line with 3 hashtags: the first 2 MUST be broad,
  high-traffic audience-cohort hashtags (e.g. #Economics, #Finance, #WallStreet, #SportsBusiness,
  #BusinessHistory, #History—NEVER an obscure proper-noun hashtag like #IvarKreuger), and #shorts last.
- tags: 12-15, combining exact proper nouns from the story, relevant YouTube autocomplete phrases, and
  broad high-volume niche category terms so YouTube's Shorts Feed matches the right viewer cohort.
- pinned_comment: one provocative debate question or moral dilemma about the character's choices or the situation (e.g. "Was the Navy right to let them walk free, or was the prank too humiliating to forgive?", "Would you trust a baboon to run a train line if he never made one mistake?"). Never generic "What do you think?" or "Did you know?" — give viewers an immediate reason to take a side in the comments.
Shorts: {json.dumps(research, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "title": "...", "description": "...",
"tags": ["..."], "pinned_comment": "..."}}]}}""")
    for r in data.get("shorts", []):  # keep the draft if the reply is incomplete
        i = r.get("index")
        if isinstance(i, int) and 0 <= i < len(shorts) and r.get("title") and r.get("tags"):
            shorts[i].update({k: r[k] for k in ("title", "description", "tags", "pinned_comment") if r.get(k)})
    for s in shorts:  # emoji & pipe suffixes in titles: no search value, off-tone; the pinned comment may keep emoji
        t = re.sub(r"\s{2,}", " ", re.sub(r"[\U0001F000-\U0001FAFF☀-➿️‍]", "", s["title"])).strip()
        if " | " in t and len(t.split(" | ")[0].strip()) >= 20:
            t = t.split(" | ")[0].strip()
        s["title"] = t


def srt(words: list[tuple[float, float, str]], path: Path) -> None:
    """Exact-narration caption file to upload in YouTube Studio (searchable, unlike burned-in text)."""
    def ts(t: float) -> str:
        ms = round(t * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    blocks = []
    for n, i in enumerate(range(0, len(words), 7), 1):
        chunk = words[i:i + 7]
        blocks.append(f"{n}\n{ts(chunk[0][0])} --> {ts(chunk[-1][1])}\n{' '.join(w[2] for w in chunk)}\n")
    path.write_text("\n".join(blocks), encoding="utf-8")
