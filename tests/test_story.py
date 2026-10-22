"""Tests for how stories are told (2026-10-22): one voice take per sentence cut back into scenes, the checkable story
rules, and the editor's second pass. No AI usage, no GPU. Run: .venv\\Scripts\\python.exe tests\\test_story.py"""
import json
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import gpu, llm, media_tools, session, writing  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_qwen_voice import COUNTED  # noqa: E402  (no qwen imports at module level: plain dict)
from shortsmaker import rules  # noqa: E402

rules.load_rules("strange-history")  # the prompts read the channel's rules file


def scenes(*lines):
    return [{"narration": t} for t in lines]


def test_word_counts_match_the_aligner():
    for text, n in COUNTED.items():
        assert gpu.spoken_count(text) == n, (text, gpu.spoken_count(text))


def test_sentences_running_across_cuts_are_one_take():
    sc = scenes("A passenger looked out the train window", "and saw a baboon working the signals.",
                "He complained.", "So the railway sent officials", "to investigate")
    assert gpu.sentence_groups(sc) == [[0, 1], [2], [3, 4]]  # the last scene ends its run even without a full stop
    assert gpu.sentence_groups(scenes('He said "no."', "Then left.")) == [[0], [1]]  # quote after the full stop


def test_a_take_is_cut_between_the_scenes_words():
    sc = scenes("One two three", "four five.")
    with tempfile.TemporaryDirectory() as d:
        work = Path(d)
        media_tools.ffmpeg("-f", "lavfi", "-i", "sine=d=3", "-ar", "44100", "take0.wav", cwd=work)
        words = [[0.1, 0.4, "One"], [0.5, 0.8, "two"], [0.9, 1.2, "three"], [1.6, 2.0, "four"], [2.1, 2.6, "five."]]
        out = gpu.split_takes([{"out": str(work / "take0.wav"), "words": words}], [[0, 1]], sc, work)
        (a, wa), (b, wb) = out
        assert abs(media_tools.duration(a) - 1.4) < 0.03, media_tools.duration(a)  # cut halfway through the 1.2-1.6 pause
        assert abs(media_tools.duration(b) - 1.6) < 0.03, media_tools.duration(b)
        assert [w[2] for w in wa] == ["One", "two", "three"] and wb[0][2] == "four"
        assert abs(wb[0][0] - 0.2) < 1e-6  # timings start at the scene's own audio
        # words that don't add up to the scenes: no guessing, the caller falls back
        assert gpu.split_takes([{"out": str(work / "take0.wav"), "words": words[:4]}], [[0, 1]], sc, work) is None


def test_story_problems():
    lines = ["A passenger looked out", "and saw a baboon at the signals.", "In 1880, he complained.",
             "So they tested Jack.", "He passed."]
    found = writing.story_problems(lines, 2, False)
    assert any("answered in scene 2 of 5" in p for p in found), found
    assert any("scene 3 starts with a date" in p for p in found), found
    assert writing.story_problems(lines[:2] + lines[3:], 4, False) == []  # second-to-last scene is fine
    assert writing.story_problems(lines[:2] + lines[3:], None, None) == []  # no verdict, nothing to judge
    long_first = ["One two three four five six seven", "eight nine ten eleven twelve thirteen."]
    assert any("13 words" in p for p in writing.story_problems(long_first, None, None))
    assert any("list of facts" in p for p in writing.story_problems(["Jack worked.", "He passed."], None, True))
    for date in ("1932: the emus came.", "By the 1850s it stank.", "On 16 October", "In the late 1800s, they"):
        assert writing.DATE_FIRST.match(date), date
    for fine in ("Twenty thousand emus came.", "In nine years, he never slipped.", "The 1932 war"):
        assert not writing.DATE_FIRST.match(fine), fine


def test_editor_gets_one_second_pass_for_broken_rules():
    good = ["A passenger looked out", "and saw a baboon at the signals.", "So the railway tested him,",
            "and he passed.", "But they paid him in beer.", "Twenty cents a day too.", "He never made one mistake,",
            "not in nine years.", "That baboon kept the job,", "and a passenger kept riding."]
    early = good[:2] + ["In 1881, he passed the test."] + good[3:]
    prompts, replies = [], [
        {"shorts": [{"index": 0, "scenes": early, "payoff_scene": 3, "list_like": False, "notes": ["first"]}]},
        {"shorts": [{"index": 0, "scenes": good, "payoff_scene": 10, "list_like": False, "notes": ["fixed"]}]},
    ]
    old_ask, old_brain = llm.ask_ai, session.BRAIN

    def fake(prompt, fatal=True, read_dir=None, brain=None, bulk=False):
        prompts.append(prompt)
        session.LAST_AI = brain or "claude"
        return replies[len(prompts) - 1]
    llm.ask_ai, session.BRAIN = fake, "claude"
    old_plan = writing.length_plan
    writing.length_plan = lambda: (40, 125, 8, 16, "40-50")
    try:
        s = {"topic": "Jack", "title": "Jack", "lines": list(good)}
        writing.edit_scripts([s], {"niche": "history", "tone": "friend at a bar"})
    finally:
        llm.ask_ai, session.BRAIN, writing.length_plan = old_ask, old_brain, old_plan
    assert len(prompts) == 2 and "SECOND PASS" in prompts[1] and "answered in scene 3 of 10" in prompts[1]
    assert "OPEN INSIDE THE STORY'S STRANGEST MOMENT" in prompts[0] and "SECOND PASS" not in prompts[0]
    assert s["lines"] == good
    assert not any(n.startswith("STILL") for n in s["editor_notes"]), s["editor_notes"]
    assert any("first" in n for n in s["editor_notes"]) and any("fixed" in n for n in s["editor_notes"])


def test_writer_prompt_has_the_story_rules_and_cut_rule():
    text = json.dumps([session.RULES["Story rules"], writing.SCENE_CUTS])
    assert "never \\\"and then\\\"" in text and "payoff LAST" in text and "in the middle of a" in text


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
