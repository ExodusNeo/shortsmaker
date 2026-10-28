"""Tests for our own topic research (topic_ideas.py, 2026-10-28, owner: "research our own topics instead of copying
the titles"): story ideas from Wikipedia's Unusual articles pages, and proven channels' recent Shorts used only as
a list of stories to stay away from. The network and the AI are faked. No AI usage.
Run: .venv\\Scripts\\python.exe tests\\test_topic_ideas.py"""
import json
import random
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
from shortsmaker import channel_profiles, image_sources, logbook, seo, session, topic_ideas, writing  # noqa: E402
from test_pictures_first import fake_ai, passing, planning  # noqa: E402

WIKITEXT = """{| class="wikitable"
|-
| '''[[Pope Benedict IX]]'''
| He became pope at twenty, and later sold the papacy. He was pope three times.
|-
| {{icon|FA}} '''[[Pre-Columbian transoceanic contact theories|Contact theories]]'''
| Native Americans are among the [[Ten Lost Tribes]]? The [[Zuni people|Zuni]] are related to Japanese peasants?
|-
| '''[[Roland the Farter]]'''
| If only we were all a jump, whistle & fart away from prosperity!{{citation needed}}
|}"""


def test_parse_ideas():
    assert topic_ideas.parse_ideas(WIKITEXT) == [
        {"title": "Pope Benedict IX", "why": "He became pope at twenty, and later sold the papacy. He was pope three times."},
        {"title": "Pre-Columbian transoceanic contact theories",
         "why": "Native Americans are among the Ten Lost Tribes? The Zuni are related to Japanese peasants?"},
        {"title": "Roland the Farter", "why": "If only we were all a jump, whistle & fart away from prosperity!"},
    ]


def test_clash_needs_every_name_word():
    titles = ["The True Story of Mike the Headless Chicken", "Emperor Norton's crazy reign", "WW2's weirdest soldier"]
    assert topic_ideas.clash("Mike the Headless Chicken", titles) == titles[0]
    assert topic_ideas.clash("mike, the headless CHICKEN!", titles) == titles[0]  # case and punctuation
    assert topic_ideas.clash("Joshua Norton", titles) is None  # "joshua" is not in any title
    assert topic_ideas.clash("Emperor Norton", titles) == titles[1]  # "Norton's" counts as Norton
    assert topic_ideas.clash("The War", titles) is None  # too few real words to judge
    assert topic_ideas.clash("", titles) is None


def test_pages_setting():
    saved = dict(session.RULE_SETTINGS)
    try:
        session.RULE_SETTINGS.clear()
        assert topic_ideas.pages() == topic_ideas.DEFAULT_PAGES
        session.RULE_SETTINGS["idea_pages"] = "Society, economy and law; History"
        assert topic_ideas.pages() == ["Society, economy and law", "History"]
        session.RULE_SETTINGS["idea_pages"] = "society, economy and law; history"  # the rules parser lowercases values
        assert topic_ideas.pages() == ["Society, economy and law", "History"]
    finally:
        session.RULE_SETTINGS.clear()
        session.RULE_SETTINGS.update(saved)


def test_fetch_is_cached():
    calls = []
    saved = (image_sources.wm_get, topic_ideas.CACHE)
    d = Path(tempfile.mkdtemp())
    topic_ideas.CACHE = d
    image_sources.wm_get = lambda url, what: calls.append(url) or json.dumps({"parse": {"wikitext": {"*": WIKITEXT}}})
    try:
        assert len(topic_ideas.fetch_ideas(["History"])) == 3
        assert len(topic_ideas.fetch_ideas(["History"])) == 3 and len(calls) == 1  # second time from the cache
        assert "Unusual_articles%2FHistory" in calls[0] or "Unusual%20articles%2FHistory" in calls[0], calls[0]
        image_sources.wm_get = lambda url, what: None  # Wikipedia down and nothing cached: no ideas, no crash
        assert topic_ideas.fetch_ideas(["Food"]) == []
    finally:
        image_sources.wm_get, topic_ideas.CACHE = saved
        shutil.rmtree(d, ignore_errors=True)


def test_pick_skips_done_and_taken():
    ideas = [{"title": f"Idea {k} Zebra{k}", "why": "x"} for k in range(100)]
    ideas += [{"title": "Mike the Headless Chicken", "why": "a rooster lived 18 months"},
              {"title": "Douglas Bader", "why": "legless ace"}]
    saved = topic_ideas.fetch_ideas
    topic_ideas.fetch_ideas = lambda pages: ideas
    try:
        ch = {"done_topics": ["In 1941, Royal Air Force fighter ace Douglas Bader ... lost a leg"]}
        got = topic_ideas.pick_ideas(ch, ["The True Story of Mike the Headless Chicken"], 40, random.Random(1))
    finally:
        topic_ideas.fetch_ideas = saved
    titles = [i["title"] for i in got]
    assert len(got) == 40 and len(set(titles)) == 40
    assert "Mike the Headless Chicken" not in titles and "Douglas Bader" not in titles


TRENDS = [{"title": "The True Story of Mike the Headless Chicken", "views": 2_000_000, "channel": "Voggle"}]


def topic_prompt(pl) -> str:
    return next(p for p in pl.ai.prompts if "You choose stories" in p)


def test_topic_prompt_uses_our_ideas_and_lists_taken_stories():
    ideas = [{"title": "Roland the Farter", "why": "a jester paid in land to fart"}]
    with planning(passing({"Topic 1"}), pick_ideas=lambda ch, taken, k=60, rng=None: ideas) as pl:
        channel_profiles.trend_research = lambda ch: TRENDS
        writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
    prompt = topic_prompt(pl)
    assert "Roland the Farter" in prompt and "a jester paid in land to fart" in prompt
    assert "Mike the Headless Chicken" in prompt and "never pick" in prompt.lower()
    assert "WHAT'S WORKING NOW" not in prompt and "proven demand" not in prompt
    writer = next(p for p in pl.ai.prompts if "You write YouTube Shorts narration" in p)
    assert "Mike the Headless Chicken" not in writer and "Roland the Farter" not in writer


def test_topic_a_proven_channel_just_posted_is_dropped():
    def ai(prompt):
        if "You choose stories" in prompt:
            return {"shorts": [{"topic": "A rooster lived without a head", "subject": "Mike the Headless Chicken",
                                "character": "Mike"},
                               {"topic": "Topic 2", "subject": "Subject 2"}, {"topic": "Topic 3", "subject": "Subject 3"}]}
        from test_pictures_first import planning_ai
        return planning_ai(prompt)
    with planning(passing({"A rooster lived without a head", "Topic 2"}), pick_ideas=lambda *a, **k: []) as pl:
        pl.ai.reply = ai
        channel_profiles.trend_research = lambda ch: TRENDS
        shorts = writing.write_scripts({"niche": "history", "done_topics": [], "myths": []}, 1)
    assert [s["topic"] for s in shorts] == ["Topic 2"]
    assert any("Mike the Headless Chicken" in d and "posted" in d for d in shorts[0]["dropped_topics"]), shorts[0]["dropped_topics"]


def test_seo_never_sees_competitor_titles():
    short = {"title": "T", "subject": "Mike", "scenes": [{"narration": "A rooster lived."}], "description": ""}
    saved = (seo.search_suggestions, channel_profiles.trend_research, logbook.logbook_results)
    seo.search_suggestions, channel_profiles.trend_research, logbook.logbook_results = (
        (lambda q: []), (lambda ch: TRENDS), (lambda: ""))
    try:
        with fake_ai(lambda p: {"shorts": []}) as ai:
            seo.seo_pass([dict(short)], {"niche": "history"})
    finally:
        seo.search_suggestions, channel_profiles.trend_research, logbook.logbook_results = saved
    assert ai.prompts and "Mike the Headless Chicken" not in ai.prompts[0]


if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_") and (len(sys.argv) < 2 or n in sys.argv[1:])]
    failed = 0
    for n in names:
        try:
            globals()[n]()
            print(f"PASS {n}")
        except Exception:
            failed += 1
            print(f"FAIL {n}")
            traceback.print_exc()
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(1 if failed else 0)
