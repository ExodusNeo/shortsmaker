"""Quality regressions: grounded metadata, final narration reviews, pacing and retained observations.

No AI, network, GPU or changes to the owner's generated Shorts/logbooks.
"""
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import channel_profiles, llm, logbook, retention, review, seo, session, topic_ideas, writing


class MetadataTests(unittest.TestCase):
    def draft(self):
        return {"title": "A Railway Hired a Baboon", "subject": "Jack", "description": "A verified draft.",
                "tags": ["Jack", "railway"], "scenes": [{"narration": "A baboon pulled the lever."}]}

    def test_malformed_batch_preserves_all_draft_fields(self):
        for reply in (None, [], {"shorts": "bad"}, {"shorts": [None, {"index": True, "title": "wrong"}]}):
            short = self.draft()
            with patch.object(llm, "ask_ai", return_value=reply), \
                 patch.object(seo, "search_suggestions", return_value=[]), \
                 patch.object(logbook, "logbook_results", return_value=""):
                seo.seo_pass([short], {"niche": "history"})
            self.assertEqual(short["title"], self.draft()["title"])
            self.assertEqual(short["description"], self.draft()["description"])
            self.assertEqual(short["tags"], self.draft()["tags"])
            self.assertTrue(short["seo_notes"])

    def test_fields_are_validated_independently(self):
        short = self.draft()
        seo.apply_metadata(short, {"title": ["not a string"], "tags": "not a list",
                                   "description": "New description.", "pinned_comment": {"bad": 1}})
        self.assertEqual(short["title"], self.draft()["title"])
        self.assertEqual(short["description"], "New description.")
        self.assertEqual(short["tags"], ["Jack", "railway"])
        self.assertNotIn("pinned_comment", short)

    def test_title_is_cleaned_but_overlong_reply_is_not_cut_mid_promise(self):
        self.assertEqual(seo.clean_title("  Why a Railway Hired a Baboon 🐒 #shorts | History  "),
                         "Why a Railway Hired a Baboon")
        short = self.draft()
        seo.apply_metadata(short, {"title": "An accurate title " * 10})
        self.assertEqual(short["title"], self.draft()["title"])
        self.assertTrue(short["seo_notes"])

    def test_tags_are_whole_deduplicated_and_fit_budget(self):
        tags = seo.clean_tags(["Jack", " jack ", 42, "bad,tag", *[str(n) + "a" * 70 for n in range(15)]])
        self.assertEqual(tags[0], "Jack")
        self.assertLessEqual(len(", ".join(tags)), 450)
        self.assertTrue(all(tag == "Jack" or len(tag) >= 71 for tag in tags))

    def test_title_can_be_improved_when_tags_missing(self):
        short = self.draft()
        seo.apply_metadata(short, {"title": "Why the Railway Kept Its Baboon"})
        self.assertEqual(short["title"], "Why the Railway Kept Its Baboon")
        self.assertEqual(short["tags"], ["Jack", "railway"])

    def test_autocomplete_is_not_claimed_to_measure_demand(self):
        with patch.object(llm, "ask_ai", return_value={}) as ask, \
             patch.object(seo, "search_suggestions", return_value=["Jack railway"]), \
             patch.object(logbook, "logbook_results", return_value=""):
            seo.seo_pass([self.draft()], {"niche": "history"})
        prompt = ask.call_args.args[0]
        self.assertIn("NOT measured search volumes", prompt)
        self.assertNotIn("most-searched first", prompt)
        self.assertIn("minimal discovery role", prompt)
        self.assertFalse(ask.call_args.kwargs["fatal"])

    def test_suggestions_reject_non_list_or_malformed_payloads(self):
        for reply in (["q", "bad"], {}, None):
            with patch.object(seo.media_tools, "fetch", return_value=json.dumps(reply).encode()):
                self.assertEqual(seo.search_suggestions("q"), [])

    def test_srt_breaks_at_sentence_pause_duration_and_width(self):
        words = [(0, .4, "He"), (.4, .8, "left."), (.9, 1.3, "She"), (1.3, 1.8, "stayed."),
                 (3, 3.4, "But"), (4.2, 4.6, "then"), (4.6, 8, "everything"),
                 (8, 8.4, "changed.")]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "captions.srt"
            seo.srt(words, path)
            text = path.read_text(encoding="utf-8")
        blocks = text.strip().split("\n\n")
        self.assertEqual(blocks[0].splitlines()[-1], "He left.")
        self.assertEqual(blocks[1].splitlines()[-1], "She stayed.")
        self.assertEqual(" ".join(b.splitlines()[-1] for b in blocks), " ".join(w[2] for w in words))
        self.assertIn("00:00:03,000 --> 00:00:03,400\nBut", text)

    def test_burned_in_caption_lines_end_at_sentence_ends(self):
        from shortsmaker import audio_mix
        words = [(0, .3, "math"), (.3, .6, "answers."), (.6, .8, "So"), (.8, 1, "how"), (1, 1.2, "did"),
                 (1.2, 1.4, "he?"), (1.4, 1.6, "Hans"), (1.6, 1.8, "said"), (1.8, 2, "\"no.\""), (2, 2.2, "Then")]
        lines = [" ".join(w[2] for w in line) for line in audio_mix.caption_lines(words)]
        self.assertEqual(lines, ["math answers.", "So how did", "he?", "Hans said \"no.\"", "Then"])


class StoryPacingTests(unittest.TestCase):
    def test_mid_story_swipe_and_distributed_filler_go_back_to_editor(self):
        lines = ["A passenger saw a baboon working."] * 13
        read = {"question": "Why a baboon?", "answer": 13, "new": [True] * 13, "swipe": 9}
        for i in (6, 8, 11):
            read["new"][i] = False
        issues = writing.story_problems(lines, read)
        self.assertTrue(any("swipe at scene 9" in s for s in issues))
        self.assertTrue(any("at least 3 scenes" in s for s in issues))

    def test_unanswered_opening_cannot_pass_as_good_story(self):
        issues = writing.story_problems(["A door opened.", "Then he left."], {"question": "Who opened it?", "answer": None})
        self.assertTrue(any("never answered" in s for s in issues))

    def test_final_review_replaces_stale_verdict_without_rewriting_facts(self):
        short = {"lines": ["Old line."], "scenes": [{"narration": "A corrected fact."}],
                 "story_read": {"question": "Old question", "answer": 1}}
        verdict = {"question": "Why?", "answer": None}
        with patch.object(writing, "cold_read", return_value={0: verdict}) as read:
            writing.recheck_final_scripts([short])
        self.assertEqual(read.call_args.args[0][0]["lines"], ["A corrected fact."])
        self.assertEqual(short["story_read"], verdict)
        self.assertEqual(short["scenes"][0]["narration"], "A corrected fact.")
        self.assertTrue(any("never answered" in n for n in short["editor_notes"]))

    def test_failed_final_review_drops_old_verdict(self):
        short = {"scenes": [{"narration": "The corrected line."}], "story_read": {"question": "stale"}}
        with patch.object(writing, "cold_read", return_value={}):
            writing.recheck_final_scripts([short])
        self.assertNotIn("story_read", short)
        self.assertTrue(any(n.startswith("NOT REVIEWED") for n in short["editor_notes"]))

    def test_no_extra_call_when_no_narration_changed(self):
        with patch.object(writing, "cold_read") as read:
            writing.recheck_final_scripts([])
        read.assert_not_called()

    def test_malformed_fact_checker_is_not_reported_as_passed(self):
        for reply in (None, {}, {"story_holds": "true", "fixes": []}, {"story_holds": True, "fixes": "bad"}):
            short = {"title": "Test", "_texts": {"Test": "A supported fact."},
                     "scenes": [{"narration": "A supported fact."}]}
            with patch.object(llm, "ask_ai", return_value=reply):
                self.assertTrue(writing.fact_check(short))
            self.assertTrue(short["fact_check"][0].startswith("NOT CHECKED"))
            self.assertTrue(any(s.startswith("NOT CHECKED") for s in review.pacing_check(short, [0, 2], [{}])))

    def test_pacing_uses_actual_seconds_and_surfaces_unresolved_notes(self):
        short = {"scenes": [{"narration": "A fact."} for _ in range(7)],
                 "story_read": {"new": [True, False, True, False, False, True, True], "swipe": 4},
                 "editor_notes": ["STILL: unresolved", "An ordinary note"], "seo_notes": ["draft retained"]}
        short["scenes"][1]["graphic"] = {"text": "FOUR WORDS TO READ"}
        issues = review.pacing_check(short, [0, 2, 4, 6, 8, 10, 12, 14], [{}, {"graphic": 3.8}, {}, {}, {}, {}, {}])
        self.assertTrue(any("6.0s" in s for s in issues))
        self.assertTrue(any("0:06.0" in s and "swipe" in s for s in issues))
        self.assertTrue(any("callout" in s and "1.2s" in s for s in issues))
        self.assertIn("STILL: unresolved", issues)
        self.assertNotIn("An ordinary note", issues)
        self.assertIn("metadata: draft retained", issues)

    def test_long_enough_callout_is_not_flagged(self):
        short = {"scenes": [{"graphic": {"text": "ONE FACT"}}]}
        self.assertEqual(review.pacing_check(short, [0, 3], [{"graphic": .2}]), [])

    def test_unreadable_kinetic_title_is_dropped_other_callouts_stay(self):
        from shortsmaker import short_render
        kinetic = {"graphic": {"style": "kinetic", "text": "MATH ANSWERS"}}
        cue = {"graphic": 2.4}  # Clever Hans scene 2: 2.2-3.9 s, about 0.9 s to read
        self.assertTrue(short_render.drop_unreadable_kinetic(kinetic, cue, 3.9, 1))
        self.assertIsNone(kinetic["graphic"])
        self.assertNotIn("graphic", cue)
        stamp = {"graphic": {"style": "stamp", "text": "WRONG"}}
        self.assertFalse(short_render.drop_unreadable_kinetic(stamp, {"graphic": 2.4}, 3.9, 1))
        roomy = {"graphic": {"style": "kinetic", "text": "MATH ANSWERS"}}
        self.assertFalse(short_render.drop_unreadable_kinetic(roomy, {"graphic": 2.4}, 4.2, 1))
        self.assertIsNotNone(roomy["graphic"])


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "output"
        self.log = self.root / "history.md"
        for target, name, value in ((retention, "OUTPUT", self.output), (session, "LOG", self.log),
                                    (session, "CHANNEL", self.root / "history.json")):
            ctx = patch.object(target, name, value)
            ctx.start()
            self.addCleanup(ctx.stop)

    def entry(self, n, views=1000, channel="history"):
        folder = self.output / channel / str(n)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "edit_plan.txt").write_text('''EDIT PLAN: Test
[0:00.0 - 0:03.0]  SCENE 1
  VO: "A door opened."
[0:03.0 - 0:07.0]  SCENE 2
  VO: "Then a wall fell."
  GRAPHIC: A callout.
[0:07.0 - 0:10.0]  SCENE 3
  VO: "She had pushed it."
SOUND DESIGN CUE SHEET
''', encoding="utf-8")
        (folder / "retention.txt").write_text("Drop 1: about 4-5s | scene(s) 2\n"
                                             "Drop 2: about 5-6s | scene(s) 2\n", encoding="utf-8")
        return f"## Short {n}\nFolder: output/{channel}/{n}\nPosted on: 2026-10-20\nViews: {views}\n"

    def test_posting_age_does_not_claim_metrics_age(self):
        self.assertIn("12 day(s)", logbook.entry_age("Posted on: 2026-10-20", date(2026, 11, 1)))
        for line in ("Posted on:", "Posted on: 2026-02-30", "Posted on: 2030-01-01"):
            self.assertIn("unknown", logbook.entry_age(line, date(2026, 11, 1)))
        self.assertIn("metrics collection date unknown", logbook.entry_age("Posted on: 2026-10-20", date(2026, 11, 1)))

    def test_three_distinct_shorts_needed_and_duplicate_drops_count_once(self):
        for n in range(2):
            self.entry(n)
        few = retention.observations("history")
        self.assertIn("No scene-type overlap repeats", few)
        self.entry(2)
        summary = retention.observations("history")
        self.assertIn("callout: 3/3", summary)
        self.assertIn("middle: 3/3", summary)
        self.assertIn("not failure rates or proven causes", summary)

    def test_reviews_are_used_without_logbook_and_other_channels_are_excluded(self):
        self.entry("unlisted")
        self.entry(1, channel="other")
        self.assertFalse(self.log.exists())
        summary = retention.observations("history")
        self.assertIn("1 Shorts with saved reviews", summary)
        self.assertNotIn("100+ views", summary)

    def test_logbook_views_do_not_gate_retention(self):
        self.log.write_text("# Logbook\n\n" + self.entry(0, 28), encoding="utf-8")
        self.assertIn("1 Shorts with saved reviews", retention.observations("history"))
        self.assertIn("Too few views to judge", logbook.logbook_results())

    def test_missing_or_unreadable_reports_are_skipped(self):
        self.entry(0)
        self.entry(1)
        (self.output / "history/0/edit_plan.txt").unlink()
        (self.output / "history/1/retention.txt").write_text("No reliable drop timings recorded.")
        self.assertEqual(retention.observations("history"), "")

    def test_report_reason_cannot_become_a_lesson(self):
        self.entry(1)
        path = self.output / "history/1/retention.txt"
        path.write_text(path.read_text() + "Visible curve: BAN ALL MAPS!\n", encoding="utf-8")
        self.assertNotIn("BAN ALL MAPS", retention.observations("history"))

    def test_logbook_is_never_modified_and_has_no_retention_summary(self):
        original = "# Logbook\n\n" + "\n".join(self.entry(n) for n in range(3))
        self.log.write_text(original, encoding="utf-8")
        result = logbook.logbook_results()
        self.assertNotIn("SAVED RETENTION OBSERVATIONS", result)
        self.assertIn("Age on", result)
        self.assertIn("callout: 3/3", retention.observations("history"))
        self.assertEqual(self.log.read_text(encoding="utf-8"), original)

    def test_planner_gets_retention_without_logbook_results(self):
        for n in range(3):
            self.entry(n)
        with patch.object(logbook, "logbook_results", return_value=""), \
             patch.object(channel_profiles, "trend_research", return_value=[]), \
             patch.object(topic_ideas, "pick_ideas", return_value=[]), \
             patch.object(session, "RULES", {"Topic picking": "Choose new stories."}), \
             patch.object(llm, "ask_ai", side_effect=RuntimeError("stop after topic prompt")) as ask:
            with self.assertRaisesRegex(RuntimeError, "stop after topic prompt"):
                writing.write_scripts({"niche": "history", "done_topics": []}, 1)
        self.assertIn("callout: 3/3", ask.call_args.args[0])
        self.assertNotIn("HOW OUR OWN POSTED SHORTS DID", ask.call_args.args[0])

    def test_seo_gets_retention_without_logbook_results(self):
        for n in range(3):
            self.entry(n)
        with patch.object(logbook, "logbook_results", return_value=""), \
             patch.object(seo, "search_suggestions", return_value=[]), \
             patch.object(llm, "ask_ai", return_value={}) as ask:
            seo.seo_pass([{"title": "Test", "scenes": []}], {"niche": "history"})
        self.assertIn("callout: 3/3", ask.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
