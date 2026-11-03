"""Retention screenshot handling, grounded scene timing, and no automatic logbook edits. No AI calls."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import cli, llm, retention, session


PLAN = '''EDIT PLAN: A test Short
Length 0:10.0
[0:00.0 - 0:04.0]  SCENE 1  (hook)
  VO:      "A door opened."
  SHOT:    A painted doorway.
[0:04.0 - 0:07.0]  SCENE 2
  VO:      "Then the wall fell."
  GRAPHIC: A falling wall.
[0:07.0 - 0:10.0]  SCENE 3
  VO:      "She had pushed it."
SOUND DESIGN CUE SHEET
'''


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'test-channel' / 'test-short'
        self.folder.mkdir(parents=True)
        (self.folder / 'edit_plan.txt').write_text(PLAN, encoding='utf-8')
        self.picture = self.root / 'screenshot.png'
        Image.new('RGB', (320, 160), 'white').save(self.picture)

    def test_parse_real_edit_plan_format(self):
        scenes = retention.scenes_from_plan(PLAN)
        self.assertEqual([row['scene'] for row in scenes], [1, 2, 3])
        self.assertEqual(scenes[1]['narration'], 'Then the wall fell.')
        self.assertEqual(scenes[1]['visuals'], ['GRAPHIC: A falling wall.'])
        self.assertEqual(retention.seconds('1:02.5'), 62.5)

    def test_invalid_plan_stops_before_calling_ai(self):
        for text in ('no scenes', PLAN.replace('0:04.0 - 0:07.0', '0:03.0 - 0:07.0')):
            with self.assertRaises(ValueError):
                retention.scenes_from_plan(text)

    def test_drop_validation_rejects_invented_or_invalid_times(self):
        drops = [{'start': a, 'end': b, 'reason': 'visible drop'} for a, b in
                 ((-1, 3), (True, 3), (float('nan'), 3), (2, 11), (4, 2), (2, 4), (2, 4), (6, 8))]
        got = retention.normalize_reply({'readable': True, 'drops': drops}, 10)
        self.assertEqual([(row['start'], row['end']) for row in got['drops']], [(2, 4), (6, 8)])
        with self.assertRaises(ValueError):
            retention.normalize_reply({'drops': []}, 10)

    def test_unreadable_graph_never_uses_claimed_drops(self):
        got = retention.normalize_reply({'readable': False, 'drops': [{'start': 1, 'end': 4, 'reason': 'x'}],
                                         'limitations': ['Time axis is cropped.']}, 10)
        self.assertEqual(got['drops'], [])
        self.assertIn('Time axis is cropped.', got['limitations'])

    def test_report_matches_cross_scene_interval_and_includes_uncertainty(self):
        got = retention.normalize_reply({'readable': True, 'drops': [{'start': 3, 'end': 5, 'reason': 'steeper curve'}]}, 10)
        text = retention.report_text('Title', got, retention.scenes_from_plan(PLAN), 'graph.png', 'codex')
        self.assertIn('scene(s) 1, 2', text)
        self.assertIn('Then the wall fell.', text)
        self.assertIn('+/- 1-2 seconds', text)
        self.assertIn('Future planning reads saved retention reviews directly.', text)
        self.assertNotIn('My notes', text)
        self.assertNotIn('logbook', text.lower())
        self.assertNotIn('Scene 3 (', text)

    def test_only_screenshot_is_sent_and_report_is_saved_without_touching_logbook(self):
        log = self.root / 'log.md'
        log.write_text('Keep my notes', encoding='utf-8')
        def read(prompt, **kwargs):
            self.assertEqual(len(list(kwargs['read_dir'].iterdir())), 1)
            self.assertIn('readable=false', prompt)
            self.assertIn('A door opened.', prompt)
            return {'readable': True, 'drops': [{'start': 4, 'end': 7, 'reason': 'steep decline'}],
                    'limitations': ['Low resolution.']}
        with patch.object(llm, 'ask_ai', side_effect=read) as ask, patch.object(session, 'LOG', log):
            path = retention.analyze(self.folder, self.picture)
        self.assertEqual(ask.call_count, 1)
        text = path.read_text(encoding='utf-8')
        self.assertIn('scene(s) 2', text)
        self.assertIn('Low resolution.', text)
        self.assertTrue((self.folder / 'retention/graph.png').is_file())
        self.assertEqual(log.read_text(), 'Keep my notes')
        self.assertFalse(list(self.folder.glob('retention-review-*')))

    def test_failed_reply_preserves_previous_report(self):
        report = self.folder / 'retention.txt'
        report.write_text('Old valid review', encoding='utf-8')
        for reply in (None, [], {'readable': 'yes'}):
            with patch.object(llm, 'ask_ai', return_value=reply), self.assertRaises(ValueError):
                retention.analyze(self.folder, self.picture)
            self.assertEqual(report.read_text(), 'Old valid review')
        self.assertFalse((self.folder / 'retention').exists())

    def test_corrupt_screenshot_never_calls_ai(self):
        self.picture.write_bytes(b'not an image')
        with patch.object(llm, 'ask_ai') as ask, self.assertRaises(OSError):
            retention.analyze(self.folder, self.picture)
        ask.assert_not_called()

    def save_details(self, data):
        saved = self.folder / 'retention'
        saved.mkdir(exist_ok=True)
        (saved / 'metrics.json').write_text(json.dumps(data), encoding='utf-8')

    def test_manual_metrics_accept_studio_formats_and_keep_unknowns_distinct_from_zero(self):
        data = retention.normalize_metrics({'views': '1,234', 'stayed_to_watch_percentage': '72.5%',
            'average_percentage_viewed': '125.3%', 'average_view_duration_seconds': '0:24.5',
            'likes': 0, 'comments': '', 'posted_on': '2026-11-01', 'collected_on': '2026-11-03'})
        self.assertEqual(data['views'], 1234)
        self.assertEqual(data['stayed_to_watch_percentage'], 72.5)
        self.assertEqual(data['average_percentage_viewed'], 125.3)
        self.assertEqual(data['average_view_duration_seconds'], 24.5)
        self.assertEqual(data['likes'], 0)
        self.assertNotIn('comments', data)
        self.assertIn('Age when numbers were collected: 2 day(s)', retention.metrics_text(data))

    def test_invalid_metrics_and_reversed_dates_are_rejected(self):
        for data in ({'views': True}, {'views': '1,2'}, {'views': -1}, {'views': 2.5},
                     {'stayed_to_watch_percentage': 101}, {'average_percentage_viewed': 'NaN'},
                     {'average_view_duration_seconds': '0:99'}, {'likes': float('inf')},
                     {'posted_on': '2026-02-30'}, {'notes': 'x' * 1001},
                     {'posted_on': '2026-11-03', 'collected_on': '2026-11-01'}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                retention.normalize_metrics(data)

    def test_editor_keeps_skipped_values_clears_selected_fields_and_retries_bad_input(self):
        self.save_details({'views': 1200, 'likes': 5, 'notes': 'Old note'})
        with patch('builtins.input', side_effect=['', '101', '72%', '', '', '', '', '', '-', '', '', 'New note']), \
             patch.object(llm, 'ask_ai') as ask:
            data = retention.edit_metrics(self.folder)
        self.assertEqual(data, {'views': 1200, 'stayed_to_watch_percentage': 72.0, 'notes': 'New note'})
        self.assertEqual(retention.load_metrics(self.folder), data)
        self.assertFalse((self.folder / 'retention/metrics.json.tmp').exists())
        ask.assert_not_called()

    def test_details_only_menu_needs_no_graph_ai_or_logbook(self):
        with patch.object(retention.channel_profiles, 'ask_number', return_value=2), \
             patch('builtins.input', side_effect=['1200', '70%', '110%', '0:11', '', '', '', '', '', '', '']), \
             patch.object(llm, 'ask_ai') as ask, patch.object(retention, 'analyze') as analyze:
            retention.command([str(self.folder)])
        self.assertEqual(retention.load_metrics(self.folder)['views'], 1200)
        ask.assert_not_called()
        analyze.assert_not_called()
        self.assertFalse((self.folder / 'retention.txt').exists())
        with patch.object(retention, 'OUTPUT', self.root):
            self.assertIn('"views": 1200', retention.observations('test-channel'))

    def test_interactive_graph_review_can_skip_optional_details(self):
        (self.folder / 'retention.txt').write_text('saved review', encoding='utf-8')
        with patch.object(retention, 'OUTPUT', self.root), \
             patch.object(retention.channel_profiles, 'ask_number', side_effect=[1, 1]), \
             patch.object(retention.channel_profiles, 'ask_yes', return_value=False), \
             patch.object(retention.channel_profiles, 'ask_brain', return_value='codex-only'), \
             patch.object(retention.channel_profiles, 'configure_brain'), \
             patch('builtins.input', return_value=str(self.picture)), \
             patch.object(retention, 'analyze', return_value=self.folder / 'retention.txt') as analyze:
            retention.command([])
        analyze.assert_called_once_with(self.folder, self.picture)
        self.assertFalse((self.folder / 'retention/metrics.json').exists())

    def test_saved_details_reach_ai_report_and_future_planning(self):
        self.save_details({'views': 1500, 'average_percentage_viewed': 115.5,
                           'notes': 'I changed the opening captions.',
                           'posted_on': '2026-11-01', 'collected_on': '2026-11-03'})
        reply = {'readable': True, 'drops': [{'start': 4, 'end': 7, 'reason': 'visible decline'}]}
        with patch.object(llm, 'ask_ai', return_value=reply) as ask:
            path = retention.analyze(self.folder, self.picture)
        self.assertIn('"views": 1500', ask.call_args.args[0])
        self.assertIn('Views: 1500', path.read_text(encoding='utf-8'))
        self.assertIn('Average percentage viewed (can exceed 100%): 115.5', path.read_text(encoding='utf-8'))
        with patch.object(retention, 'OUTPUT', self.root):
            self.assertIn('"age_days_at_collection": 2', retention.observations('test-channel'))
        # Updating details is picked up without regenerating the graph report.
        self.save_details({'views': 2000, 'reporting_period': 'Since published'})
        with patch.object(retention, 'OUTPUT', self.root):
            summary = retention.observations('test-channel')
        self.assertIn('"views": 2000', summary)
        self.assertNotIn('"views": 1500', summary)
        self.assertIn('Since published', summary)

    def test_bad_details_do_not_remove_valid_drop_observations(self):
        self.save_details({'views': 'wrong'})
        (self.folder / 'retention.txt').write_text('Drop 1: about 4-7s | scene(s) 2\n', encoding='utf-8')
        with patch.object(retention, 'OUTPUT', self.root):
            summary = retention.observations('test-channel')
        self.assertIn('1 Shorts with saved reviews', summary)
        self.assertNotIn('wrong', summary)

    def test_failed_ai_reply_preserves_manual_details(self):
        self.save_details({'views': 1500, 'notes': 'Keep this'})
        original = (self.folder / 'retention/metrics.json').read_bytes()
        with patch.object(llm, 'ask_ai', return_value=None), self.assertRaises(ValueError):
            retention.analyze(self.folder, self.picture)
        self.assertEqual((self.folder / 'retention/metrics.json').read_bytes(), original)

    def test_command_reads_profile_mode_without_updating_profile(self):
        profiles = self.root / 'channels'
        profiles.mkdir()
        profile = profiles / 'test-channel.json'
        original = json.dumps({'brain': 'codex-only'})
        profile.write_text(original)
        (self.folder / 'retention.txt').write_text('report')
        with patch.object(retention, 'CHANNELS', profiles), \
             patch.object(retention, 'analyze', return_value=self.folder / 'retention.txt'), \
             patch.object(retention.channel_profiles, 'ask_brain', return_value='codex-only') as menu, \
             patch.object(retention.channel_profiles, 'configure_brain') as configure:
            retention.command([str(self.folder), str(self.picture)])
        menu.assert_called_once_with('codex-only')
        configure.assert_called_once_with('codex-only')
        self.assertEqual(profile.read_text(), original)

    def test_cli_routes_retention_before_normal_batch(self):
        with patch.object(sys, 'argv', ['make_shorts.py', 'retention', 'folder', 'graph.png']), \
             patch.object(retention, 'command') as command:
            cli.main()
        command.assert_called_once_with(['folder', 'graph.png'])


if __name__ == '__main__':
    unittest.main()
