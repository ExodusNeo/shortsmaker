"""Opening answer protection across planning, preview review and final drawn-opener repairs. No AI/network."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import drawn_opener, frame_render, llm, media_tools, opening_rules, picker, review, session, short_render
from shortsmaker.config import ROOT


def bobby():
    return {'title': 'The survivor slips', 'topic': 'Bobby Leach survived Niagara but an orange peel tripped him.',
            'character': 'Bobby Leach', 'palette': 'parchment', 'hook_text': 'ONE DEADLY STEP', 'thumbnail_text': 'A SLIP',
            'opener_used': True, 'opener_graphic': 'motion graphic: a slip',
            'drawn': {'moment': 'A man slips beside a labelled orange peel',
                      'code': 'export default function scene(k, t) { k.text("ORANGE PEEL", 200, 400); }'},
            'story_read': {'question': 'What tripped the survivor?'},
            'scenes': [{'narration': 'A Niagara survivor slips in the street,', 'full': None, 'graphic': None, 'person': None},
                       {'narration': 'but what could have tripped him?', 'full': None, 'graphic': None, 'person': None},
                       {'narration': 'An orange peel under his foot.', 'full': None, 'graphic': None, 'person': None}]}


class OpeningRulesTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / '.superpowers' / 'opening-tests'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def check_first(self, short, reply):
        board = self.root / 'storyboard.jpg'
        board.write_bytes(b'fixture')
        def fake_ffmpeg(*args, cwd):
            (Path(cwd) / args[-1]).write_bytes(b'fixture')
        with patch.object(media_tools, 'ffmpeg', side_effect=fake_ffmpeg), \
             patch.object(session, 'RULES', {'First-second check': 'preserve the question'}), \
             patch.object(llm, 'ask_ai', return_value=reply):
            return review.first_second_check(self.root / 'short.mp4', short,
                                             [{'bg': None} for _ in short['scenes']], board, self.root)

    def test_brief_uses_final_narration_and_protects_only_new_information(self):
        short = bobby()
        short['lines'] = ['old draft with a different ending']
        brief = opening_rules.opening_brief(short)
        self.assertIn('An orange peel under his foot.', brief)
        self.assertNotIn('different ending', brief)
        self.assertIn('What tripped the survivor?', brief)
        self.assertIn('Do not hide the person, place, object or fact that the opening already states', brief)

    def test_brief_supports_pre_director_lines_and_other_channels(self):
        for lines in [['A bridge twists in the wind.', 'A cable clamp slipped loose.'],
                      ['This company paid him to fly.', 'A clause let him sell the tickets.']]:
            brief = opening_rules.opening_brief({'lines': lines})
            self.assertIn(lines[0], brief)
            self.assertIn(lines[-1], brief)
            self.assertIn('labels', brief)

    def test_drawn_art_director_cannot_pass_a_pretty_spoiler(self):
        with patch.object(llm, 'ask_ai', return_value={'score': 9, 'reveals_answer': True,
                                                      'answer_why': 'ORANGE PEEL label', 'problems': []}) as ask:
            score, problems = drawn_opener.review(bobby(), bobby()['drawn'], self.root / 'sheet.png', 2)
        self.assertLess(score, drawn_opener.PASS)
        self.assertIn('ORANGE PEEL', problems[0])
        # the art director's prompt (the first call; the sound-off test's stranger is asked after it)
        self.assertIn('An orange peel under his foot.', ask.call_args_list[0].args[0])

    def test_drawn_known_subject_can_still_pass(self):
        with patch.object(llm, 'ask_ai', return_value={'score': 9, 'reveals_answer': False, 'problems': []}):
            self.assertEqual(drawn_opener.review(bobby(), bobby()['drawn'], self.root / 'sheet.png', 2), (9.0, []))

    def test_final_review_cannot_pass_a_high_scoring_spoiler(self):
        short = bobby()
        issues, swap = self.check_first(short, {'score': 9, 'why': 'good drawing', 'reveals_answer': True,
                                                'answer_why': 'The ORANGE PEEL label identifies the cause.'})
        self.assertIn('6/10', short['first_second'])
        self.assertIn('ORANGE PEEL', short['opening_answer_reveal'])
        self.assertEqual(short['review_status']['Opening review']['status'], 'Problems found')
        self.assertIsNone(swap)
        self.assertTrue(issues)
        self.assertTrue(review.drawn_answer_problem(short))

    def test_new_review_clears_previous_spoiler_verdict(self):
        short = bobby()
        short['opening_answer_reveal'] = 'old label'
        self.check_first(short, {'score': 8, 'why': 'cause stays outside frame', 'reveals_answer': False})
        self.assertNotIn('opening_answer_reveal', short)
        self.assertIsNone(review.drawn_answer_problem(short))

    def test_failed_preview_clears_previous_spoiler_verdict(self):
        short = bobby()
        short['opening_answer_reveal'] = 'old label'
        with patch.object(media_tools, 'ffmpeg', side_effect=OSError('preview failed')):
            result = review.first_second_check(self.root / 'short.mp4', short, [], self.root / 'board.jpg', self.root)
        self.assertNotIn('opening_answer_reveal', short)
        self.assertTrue(result[0][0].startswith('NOT REVIEWED:'))

    def test_drawn_repair_is_bounded_and_restores_graphic_fallback(self):
        short = bobby()
        short['opening_answer_reveal'] = 'ORANGE PEEL label'
        def fallback(s, weak=''):
            s['scenes'][0]['full'] = {'type': 'custom', 'kind': 'diagram', 'title': 'A SLIP', 'brief': 'Cause outside frame'}
            return 'motion graphic: a slip without its cause'
        with patch.object(picker, 'opener_graphic', side_effect=fallback):
            notes = review.fix_drawn_answer({'short': short}, self.root, short['opening_answer_reveal'])
            self.assertTrue(notes)
            self.assertIn('ORANGE PEEL label', short['drawn_repair'])
            self.assertIsNotNone(short['scenes'][0]['full'])
            self.assertIsNone(review.drawn_answer_problem(short))
            self.assertEqual(review.fix_drawn_answer({'short': short}, self.root, 'again'), [])

    def test_marked_drawn_plan_is_rewritten_instead_of_reusing_cached_bad_clip(self):
        short = bobby()
        short['drawn_repair'] = 'Remove the ORANGE PEEL label and keep the cause outside the frame.'
        folder = self.root / 'drawn'
        folder.mkdir()
        (folder / 'opener.mp4').write_bytes(b'old clip')
        new_code = 'export default function scene(k, t) { k.text("A SLIP", 200, 400); }'
        prompts = []
        def fake_ai(prompt, **kwargs):
            prompts.append(prompt)
            return ({'moment': 'A man loses balance with the cause out of frame', 'code': new_code}
                    if prompt.startswith('You animate') else {'score': 8, 'reveals_answer': False, 'problems': []})
        def fake_node(job, dest):
            (dest / ('sheet.png' if job['mode'] == 'sheet' else 'opener.mp4')).write_bytes(b'new clip')
            return None
        with patch.object(drawn_opener, 'available', return_value=None), patch.object(drawn_opener, 'node_run', side_effect=fake_node), \
             patch.object(llm, 'ask_ai', side_effect=fake_ai):
            clip, why = drawn_opener.make_opener(short, [], 2, self.root)
        self.assertIsNone(why)
        self.assertEqual(clip.read_bytes(), b'new clip')
        self.assertIn('Remove the ORANGE PEEL label', prompts[0])
        self.assertIn('A SLIP', short['drawn']['code'])
        self.assertNotIn('drawn_repair', short)

    def test_motion_graphic_planning_receives_ending_protection(self):
        short = bobby()
        short['research'] = {'Bobby Leach': 'Survived Niagara, later slipped on a peel.'}
        reply = {'full': {'type': 'custom', 'kind': 'diagram', 'title': 'A SLIP',
                          'brief': 'A man losing balance, cause outside frame.'}, 'why': 'preserves the question'}
        with patch.object(llm, 'ask_ai', return_value=reply) as ask:
            picker.opener_graphic(short)
        self.assertIn(opening_rules.GUIDANCE, ask.call_args.args[0])
        self.assertIn('An orange peel under his foot.', ask.call_args.args[0])

    def test_failed_rewrite_never_reuses_the_known_spoiler_clip(self):
        short = bobby()
        short['drawn_repair'] = 'Remove the ORANGE PEEL label.'
        folder = self.root / 'drawn'
        folder.mkdir()
        (folder / 'opener.mp4').write_bytes(b'old clip')
        (folder / 'done.txt').write_text(drawn_opener.fingerprint(short['drawn']['code'], 2.3), encoding='utf-8')
        with patch.object(drawn_opener, 'available', return_value=None), \
             patch.object(llm, 'ask_ai', return_value=None), patch.object(drawn_opener, 'node_run') as node:
            clip, why = drawn_opener.make_opener(short, [], 2, self.root)
        self.assertIsNone(clip)
        self.assertTrue(why)
        self.assertIn('drawn_failed', short)
        node.assert_not_called()

    def test_final_render_routes_drawn_spoiler_into_fix_flow(self):
        short = bobby()
        state = {'short': short, 'choices': [{'bg': None, 'person': None} for _ in short['scenes']], 'by_gemini': []}
        (self.root / 'work').mkdir()
        def judge(*args):
            short['opening_answer_reveal'] = 'ORANGE PEEL label'
            return ['FIRST SECOND: 6/10: opening reveals the answer'], None
        with patch.object(short_render, 'load_state', return_value=state), patch.object(short_render, 'save_state'), \
             patch.object(review, 'storyboard'), patch.object(short_render.editplan, 'edit_plan'), \
             patch.object(review, 'quality_check', return_value=[]), patch.object(review, 'visual_review', return_value=([], {})), \
             patch.object(review, 'first_second_check', side_effect=judge), patch.object(frame_render, 'thumbnail'), \
             patch.object(review, 'apply_review_fixes', return_value=[]), patch.object(review, 'fix_drawn_answer', return_value=['redraw']) as fix, \
             patch.object(short_render, 'render') as render, patch('builtins.input', return_value=''):
            short_render.finish_render(short, {}, self.root, bounds=[0, 2, 4, 6], sources=['drawn'] * 3,
                                       cues=[{}, {}, {}], events=[], music=None, n_graphics=0, clips={},
                                       opener_check=None, drawn=False, total=6, emphasis=set(), flashes=set(),
                                       by_gemini=set(), renderer='remotion', build_timeline=False)
        fix.assert_called_once()
        render.assert_called_once()
        self.assertEqual(render.call_args.args[-1], 1)


if __name__ == '__main__':
    unittest.main()
