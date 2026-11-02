"""Opener preview repairs must be seen, archived and compared before adoption. No AI/network."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import llm, motion, remotion_render, review

CODE = "import React from 'react'; export const Custom0 = () => <Paper>original</Paper>;\n"
FIX = CODE.replace('original', 'repaired')


def verdict(score=7, **changes):
    return dict(score=score, issues=[], reveals_answer=False, why='full review ' * 40, **changes)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.target = self.work / 'src/full/generated/Custom0.tsx'
        self.target.parent.mkdir(parents=True)
        example = self.work / 'src/full/examples/ExampleOpenerAction.tsx'
        example.parent.mkdir()
        example.write_text((motion.REMOTION / 'src/full/examples/ExampleOpenerAction.tsx').read_text())
        self.short = {'title': 'A sled stops', 'hook_text': 'WILL HE SEE AGAIN?',
                      'story_read': {'question': 'Will his sight return?'},
                      'scenes': [{'narration': 'The rider goes blind.', 'full_rescued': 'motion-graphic opener',
                                  'full': {'type': 'custom'}}, {'narration': 'His sight returns.'}]}
        self.scene = {'start': 0, 'end': 3, 'full': {'type': 'custom', 'slot': 0}}
        self.props = {'hook': 'WILL HE SEE AGAIN?', 'words': [{'text': 'blind'}], 'scenes': [self.scene]}
        self.seen = []

    def preview(self, short, scene, slot, work, props=None):
        self.assertIs(props, self.props)
        self.seen.append(self.target.read_text())
        folder = work / 'look'
        folder.mkdir()
        (folder / 'sheet.jpg').write_bytes(b'preview')
        (folder / 'props.json').write_text(json.dumps(props))
        return folder / 'sheet.jpg'

    def run_loop(self, replies, compiler=None, preview=None):
        with patch.object(motion, 'REMOTION', self.work), \
             patch.object(motion, 'preview_custom', side_effect=preview or self.preview), \
             patch.object(motion, 'tsc_check', return_value=compiler), \
             patch.object(llm, 'ask_ai', side_effect=replies):
            return motion.opener_preflight(self.short, self.scene, 0, CODE, self.work, props=self.props)

    def test_repair_is_rendered_and_complete_reviews_are_saved(self):
        self.assertEqual(self.run_loop([verdict(5), {'code': FIX}, verdict(8)]), FIX)
        self.assertEqual(self.seen, [CODE, FIX])
        records = sorted((self.work / 'opener-attempts').glob('*/review.json'))
        self.assertEqual(len(records), 2)
        self.assertGreater(len(json.loads(records[0].read_text())['verdict']['why']), 160)
        self.assertEqual(self.short['opener_preflight']['status'], 'Passed')

    def test_worse_repair_restores_best_source_and_status(self):
        self.assertEqual(self.run_loop([verdict(6), {'code': FIX}, verdict(4)]), CODE)
        self.assertEqual(self.target.read_text(), CODE)
        self.assertEqual(self.short['opener_preflight']['score'], 6)

    def test_compile_failure_does_not_adopt_unseen_code(self):
        self.assertEqual(self.run_loop([verdict(6), {'code': FIX}], compiler='syntax error'), CODE)
        self.assertEqual(self.seen, [CODE])
        self.assertTrue(list((self.work / 'opener-attempts').glob('*/repair-error.txt')))

    def test_missing_review_is_explicit_and_does_not_trigger_repairs(self):
        self.assertEqual(self.run_loop([None]), CODE)
        self.assertEqual(self.short['opener_preflight']['status'], 'Not reviewed')
        self.assertEqual(len(self.seen), 1)

    def test_render_failure_is_unreviewed(self):
        self.assertEqual(self.run_loop([], preview=lambda *a, **kw: None), CODE)
        self.assertEqual(self.short['opener_preflight']['status'], 'Not reviewed')

    def test_high_scoring_spoiler_cannot_pass(self):
        spoiler = verdict(9)
        spoiler['reveals_answer'] = True
        self.run_loop([spoiler, {'code': FIX}, verdict(7)])
        self.assertEqual(self.short['opener_preflight']['score'], 7)
        self.assertEqual(self.target.read_text(), FIX)

    def test_blocking_composition_defect_cannot_pass(self):
        blocked = verdict(9)
        blocked['issues'] = [{'severity': 'blocking', 'time': 0, 'region': 'center', 'problem': 'tiny rider'}]
        self.run_loop([blocked, {'code': FIX}, verdict(7)])
        self.assertEqual(self.short['opener_preflight']['score'], 7)

    def test_opener_allows_action_without_duplicate_banner(self):
        self.assertEqual(motion.lint_custom_code(CODE, opener=True), [])
        self.assertTrue(motion.lint_custom_code(CODE))
        self.assertIn('0.2-0.6s', motion.custom_rules(0, opener=True))

    def test_cached_external_redraw_is_previewed_and_can_restore_previous_winner(self):
        with patch.object(motion, 'REMOTION', self.work), \
             patch.object(motion, 'preview_custom', side_effect=self.preview), \
             patch.object(motion, 'tsc_check', return_value=None), \
             patch.object(llm, 'ask_ai', side_effect=[{'code': CODE}, verdict(8), verdict(5)]):
            motion.code_custom_scenes(self.short, [self.scene], self.work, props=self.props)
            cached = self.work / 'Custom0.tsx'
            signature = cached.read_text().partition('\n')[0]
            cached.write_text(signature + '\n' + FIX)
            self.short['opener_preflight_pending'] = True
            self.short['opener_preflight_baseline'] = self.short['opener_preflight']
            motion.code_custom_scenes(self.short, [self.scene], self.work, props=self.props)
        self.assertEqual(self.seen, [CODE, FIX])
        self.assertEqual(self.short['opener_preflight']['score'], 8)
        self.assertEqual(cached.read_text().partition('\n')[2], CODE)

    def test_final_opening_reviews_keep_prior_frames_and_full_explanations(self):
        short = {'title': 'x', 'scenes': [{'narration': 'A sled stops.', 'full': None}]}
        board = self.work / 'storyboard.jpg'
        board.write_bytes(b'board')
        def ffmpeg(*args, cwd):
            (cwd / 'first.jpg').write_bytes(b'frames')
        with patch.object(review.media_tools, 'ffmpeg', side_effect=ffmpeg), \
             patch.object(review.session, 'RULES', {'First-second check': 'judge'}), \
             patch.object(llm, 'ask_ai', return_value={'score': 6, 'why': 'long reason ' * 50}):
            for _ in range(2):
                review.first_second_check(self.work / 'short.mp4', short, [{}], board, self.work)
        self.assertEqual(len(list((self.work / 'opening-reviews').glob('*.json'))), 2)
        self.assertEqual(len(list((self.work / 'opening-reviews').glob('*-first.jpg'))), 2)
        self.assertGreater(len(short['first_second']), 160)

    def test_full_video_failure_supersedes_earlier_preview_pass(self):
        (self.work / 'Custom0.tsx').write_text('// signature\n' + CODE)
        self.target.write_text(CODE)
        self.short['opener_preflight'] = {'status': 'Passed', 'score': 9, 'rank_score': 9}
        with patch.object(motion, 'REMOTION', self.work), \
             patch.object(remotion_render, 'REMOTION', self.work), \
             patch.object(motion, 'tsc_check', return_value=None), \
             patch.object(llm, 'ask_ai', return_value={'code': FIX}):
            self.assertTrue(remotion_render.redraw_custom(self.short, 0, 0, 'rider too small', self.work))
        self.assertTrue(self.short['opener_preflight_pending'])
        self.assertEqual(self.short['opener_preflight_baseline']['status'], 'Problems found')
        self.assertLess(self.short['opener_preflight_baseline']['score'], 7)


if __name__ == '__main__':
    unittest.main()
