"""Titles, descriptions and tags from YouTube autocomplete; the .srt captions file."""

import json
import re
import urllib.parse
from pathlib import Path

from shortsmaker import channel_profiles, llm, logbook, media_tools, plan_rules, retention, session


def search_suggestions(query: str) -> list[str]:
    """YouTube query predictions (not search volumes or a popularity ranking)."""
    try:
        url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q="
               + urllib.parse.quote(query))
        rows = json.loads(media_tools.fetch(url, timeout=15))[1]
        return [s.strip() for s in rows if isinstance(s, str) and s.strip()][:10] if isinstance(rows, list) else []
    except Exception:
        return []


def clean_title(value) -> str:
    """Remove decoration without cutting off a title's promise."""
    if not isinstance(value, str):
        return ""
    title = re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]", "", value)
    title = re.sub(r"(?<!\w)#\w+", "", title)
    title = " ".join(title.split())
    if " | " in title and len(title.split(" | ")[0]) >= 20:
        title = title.split(" | ")[0].strip()
    return title


def clean_tags(value) -> list[str]:
    """Whole, unique tags within the upload budget; never slice through a tag."""
    if not isinstance(value, list):
        return []
    tags, seen = [], set()
    for item in value:
        if not isinstance(item, str):
            continue
        tag = " ".join(item.strip().strip("#").split())
        if not tag or len(tag) > 80 or "," in tag or tag.casefold() in seen:
            continue
        if len(", ".join(tags + [tag])) > 450:
            continue
        tags.append(tag)
        seen.add(tag.casefold())
        if len(tags) == 15:
            break
    return tags


def apply_metadata(short: dict, reply: dict | None) -> None:
    """Accept each usable field independently; malformed metadata cannot erase a draft."""
    reply = reply if isinstance(reply, dict) else {}
    notes = []
    title = clean_title(reply.get("title"))
    if title and len(title) < 60:
        short["title"] = title
    else:
        if reply.get("title"):
            notes.append("SEO title was empty after cleaning or too long; kept the draft")
        short["title"] = clean_title(short.get("title"))
        if len(short["title"]) >= 60:
            notes.append("draft title exceeds the 59-character target; review its wording")
    for key, limit in (("description", 2000), ("pinned_comment", 500)):
        value = reply.get(key)
        if isinstance(value, str) and value.strip() and len(value.strip()) <= limit:
            short[key] = value.strip()
        elif value is not None:
            notes.append(f"SEO {key} was unusable; kept the draft field")
    short["tags"] = clean_tags(reply.get("tags")) or clean_tags(short.get("tags"))
    if reply.get("tags") is not None and not clean_tags(reply["tags"]):
        notes.append("SEO tags were unusable; kept the draft tags")
    if not reply:
        notes.append("SEO did not return usable metadata; kept the draft")
    short["seo_notes"] = notes


def seo_pass(shorts: list[dict], ch: dict | None = None) -> None:
    """Rewrite title/description/tags around real YouTube search phrases; add a pinned comment."""
    if not shorts:
        return
    print("Researching search keywords...")
    ch = ch or (channel_profiles.load_channel() if session.CHANNEL.is_file() else {})
    niche = ch.get("niche", "")
    results = logbook.logbook_results()
    observations = retention.observations(session.CHANNEL.stem)
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
        suggestions = {q: got for q in seeds if (got := search_suggestions(q))}
        research.append({"index": i, "subject": subject, "title": s["title"], "description": s.get("description", ""),
                         "hook_sentence": plan_rules.first_sentence([sc.get("narration", "") for sc in s.get("scenes", [])]),
                         "hook_text": s.get("hook_text"), "thumbnail_text": s.get("thumbnail_text"),
                         "script": " ".join(sc.get("narration", "") for sc in s.get("scenes", [])),
                         "fact_check_corrections": s.get("fact_check", []),
                         "youtube_search_suggestions": suggestions})
    data = llm.ask_ai(f"""You are a YouTube SEO & Shorts Feed strategist for a Shorts channel{f' in this niche: {niche}' if niche else ''}. For each Short
below you get its draft metadata, its script, what viewers see in the first second (hook_sentence
spoken, hook_text big on screen, thumbnail_text), and YouTube autocomplete predictions, grouped by what
was typed. These are wording ideas, NOT measured search volumes or a ranking of the most-searched terms.
Ignore unrelated songs, films, namesakes or queries the script does not answer. If predictions are absent,
use the script's own language; never invent keyword research or claim high traffic.
{f"How our own posted Shorts did (title, views, notes):{chr(10)}{results}{chr(10)}" if results else ""}{f"{observations}{chr(10)}" if observations else ""}For each Short write:
- title: under 60 characters, and its first 40 characters must work alone (the Shorts player and shelf cut
  the rest). Lead with the scroll-stopping anomaly or a broadly famous anchor (a place, institution, event
  or thing casual viewers already know)—NEVER start the title with an obscure person's or company's name
  that casual viewers don't already recognize, and NEVER use dry textbook phrasing ("The X of Y in 1923") or
  pipe suffixes. Write a punchy human curiosity hook. It must promise what the hook delivers without
  repeating hook_sentence, hook_text or thumbnail_text word-for-word. No "#shorts", no emoji, no clickbait
  that the video doesn't deliver.
- Title, description and pinned comment may only claim what the script says. fact_check_corrections
  lists claims our fact check removed as false or unproven: never bring one back.
- description: Sentence 1 MUST naturally include both the exact subject/person name (`subject`) and the main
  search phrase ONLY when the script actually answers it. Use 2-3 natural sentences explaining the real
  story, not generic promises such as "a twist you won't see coming". Then a new line with up to 3 relevant
  hashtags (including #shorts); no unrelated trending tags or invented traffic claims.
- tags: a small set of specific, relevant names, topic phrases and useful spelling variants; at most 15
  and 450 characters total. Tags play a minimal discovery role except for misspellings. Never pad to a quota
  or claim tags assign a Shorts Feed audience.
- pinned_comment: one specific, answerable question grounded in the story. Invite a thoughtful response;
  don't manufacture a moral dilemma, provoke outrage or add a claim absent from the narration.
- Preserve the opening question: don't reveal the withheld answer in the title or first description sentence.
  The title promises a concrete payoff, and the ending must deliver it. This is an editorial choice for our
  stories, not a claimed ranking factor.
{f"Examples for this channel (never reuse their wording):{chr(10)}{session.RULES['SEO']}{chr(10)}" if session.RULES.get("SEO") else ""}Shorts: {json.dumps(research, ensure_ascii=False)}
Reply with ONLY JSON: {{"shorts": [{{"index": 0, "title": "...", "description": "...",
"tags": ["..."], "pinned_comment": "..."}}]}}""", fatal=False)
    rows = data.get("shorts") if isinstance(data, dict) else None
    by_index = {}
    for row in rows if isinstance(rows, list) else []:
        i = row.get("index") if isinstance(row, dict) else None
        if type(i) is int and 0 <= i < len(shorts) and i not in by_index:
            by_index[i] = row
    for i, short in enumerate(shorts):
        apply_metadata(short, by_index.get(i))


def srt(words: list[tuple[float, float, str]], path: Path) -> None:
    """Exact-narration caption file to upload in YouTube Studio (searchable, unlike burned-in text)."""
    def ts(t: float) -> str:
        ms = round(t * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    chunks = []
    for word in words:
        chunk = chunks[-1] if chunks else []
        if chunk and (len(chunk) >= 7 or len(" ".join(w[2] for w in chunk + [word])) > 42
                      or word[1] - chunk[0][0] > 3.0 or word[0] - chunk[-1][1] > 0.5
                      or re.search(r'[.!?]["\u201d\u2019\']?$', chunk[-1][2])):
            chunk = []
        if not chunk:
            chunks.append(chunk)
        chunk.append(word)
    blocks = []
    for n, chunk in enumerate(chunks, 1):
        blocks.append(f"{n}\n{ts(chunk[0][0])} --> {ts(chunk[-1][1])}\n{' '.join(w[2] for w in chunk)}\n")
    path.write_text("\n".join(blocks), encoding="utf-8")
