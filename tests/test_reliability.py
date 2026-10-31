"""Interruption recovery, narration reuse, honest review failures and bounded media recovery."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import checkpoints, cli, drawn_opener, gpu, llm, logbook, media_tools, picker, review, scene_repair, session, short_render, voice_cache


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'test' / 'short'
        self.work = self.folder / 'work'
        self.work.mkdir(parents=True)
        self.short = {'title': 'Short', 'topic': 'A topic', 'scenes': [{'narration': 'A door opened.'}]}

    def test_pending_progress_is_atomic_and_completed_work_is_not_offered(self):
        with patch.object(checkpoints, 'OUTPUT', self.root):
            checkpoints.begin(self.folder, self.short, 'codex-only')
            self.assertEqual(checkpoints.pending(), [self.folder])
            checkpoints.update(self.work, 'pictures', self.short)
            cli.record_failure(self.folder, RuntimeError('interrupted'))
            self.assertEqual(checkpoints.read(self.work / 'progress.json')['stage'], 'pictures')
            self.assertFalse((self.work / 'progress.tmp').exists())
            with self.assertRaises(RuntimeError):
                checkpoints.begin(self.folder, self.short, 'codex-only')
            checkpoints.update(self.work, 'complete')
            self.assertEqual(checkpoints.pending(), [])

    def test_render_context_restores_photos_paths_and_integer_clip_keys(self):
        data = {'clips': {3: Path('clip.mp4')}, 'emphasis': {1.2}, 'flashes': {2.3},
                'cues': [{'photo': b'photo bytes'}]}
        checkpoints.save_context(self.work, data)
        self.assertEqual(checkpoints.context(self.work), data)

    def test_unfinished_files_survive_normal_pruning(self):
        checkpoints.begin(self.folder, self.short, 'codex-only')
        os.utime(self.work, (0, 0))
        with patch.object(short_render, 'OUTPUT', self.root):
            short_render.prune_work()
        self.assertTrue(self.work.exists())

    def test_voice_cache_reuses_audio_but_invalidates_changed_text_voice_or_files(self):
        sound = self.work / '0.wav'
        sound.write_bytes(b'valid saved voice fixture')
        voices = [(sound, [(0, .4, 'A'), (.4, .8, 'door'), (.8, 1.2, 'opened.')])]
        ch = {'voice': 'voice-one'}
        voice_cache.save(self.short, ch, self.work, voices)
        self.assertEqual(voice_cache.load(self.short, ch, self.work)[0][1], voices[0][1])
        self.short['scenes'][0]['graphic'] = {'style': 'mark', 'text': 'DOOR'}
        self.assertIsNotNone(voice_cache.load(self.short, ch, self.work))
        self.assertIsNone(voice_cache.load(self.short, {'voice': 'other'}, self.work))
        self.short['scenes'][0]['narration'] = 'Changed text.'
        self.assertIsNone(voice_cache.load(self.short, ch, self.work))
        self.short['scenes'][0]['narration'] = 'A door opened.'
        (self.work / 'voice-cache/scene0.wav').write_bytes(b'corrupted')
        self.assertIsNone(voice_cache.load(self.short, ch, self.work))

    def test_batch_keeps_failed_folder_and_queues_all_scripts_before_rendering(self):
        shorts = [self.short, {**self.short, 'title': 'Second'}]
        def fail(*args, **kw):
            self.assertEqual(len(list(self.root.glob('test/*/work/progress.json'))), 2)
            raise RuntimeError('fake render interruption')
        with patch.object(sys, 'argv', ['make_shorts.py', '2', 'test', 'codex-only']), \
             patch.object(cli, 'OUTPUT', self.root), patch.object(cli.rules, 'require_rules'), \
             patch.object(cli.channel_profiles, 'use_channel'), \
             patch.object(cli.channel_profiles, 'load_channel', return_value={'done_topics': []}), \
             patch.object(cli.picture_pool, 'prune_cache'), patch.object(cli.short_render, 'prune_work'), \
             patch.object(cli.writing, 'write_scripts', return_value=shorts), patch.object(cli.seo, 'seo_pass'), \
             patch.object(cli.short_render, 'render', side_effect=fail):
            cli.main()
        records = list(self.root.glob('test/*/work/progress.json'))
        self.assertEqual(len(records), 2)
        self.assertTrue(all(checkpoints.read(path)['stage'] == 'planned' for path in records))

    def test_resume_rendered_stage_does_not_render_or_generate_voice(self):
        checkpoints.begin(self.folder, self.short, 'codex-only')
        checkpoints.update(self.work, 'rendered')
        (self.work / 'state.json').write_text('{}')
        (self.folder / 'short.mp4').write_bytes(b'video fixture')
        checkpoints.save_context(self.work, {'total': 2, 'clips': {}, 'emphasis': [], 'flashes': []})
        with patch.object(cli.rules, 'require_rules'), patch.object(cli.channel_profiles, 'use_channel'), \
             patch.object(cli.channel_profiles, 'load_channel', return_value={}), \
             patch.object(short_render, 'load_state', return_value={'short': self.short}), \
             patch.object(short_render.media_tools, 'duration', return_value=2), \
             patch.object(short_render, 'finish_render') as finish, patch.object(short_render, 'render') as render, \
             patch.object(gpu, 'local_voice') as voice, patch.object(cli, 'finish_short'):
            cli.resume_runs(self.folder)
        finish.assert_called_once()
        render.assert_not_called()
        voice.assert_not_called()

    def test_visual_review_failure_is_not_a_pass_and_success_replaces_status(self):
        def sheet(*args, cwd):
            (cwd / 'sheet1.jpg').write_bytes(b'preview')
        for reply, expected in ((None, 'Not reviewed'), ({}, 'Not reviewed'),
                                ({'problems': [None]}, 'Not reviewed'), ({'problems': []}, 'Passed'),
                                ({'problems': [{'what': 'Bad image', 'scene': 1}]}, 'Problems found')):
            with patch.object(media_tools, 'ffmpeg', side_effect=sheet), patch.object(llm, 'ask_ai', return_value=reply):
                found, _ = review.visual_review(self.folder / 'short.mp4', self.short, [0, 2], ['photo'], self.work)
            self.assertEqual(self.short['review_status']['Visual review']['status'], expected)
            if expected == 'Not reviewed':
                self.assertTrue(found[0].startswith('NOT REVIEWED:'))

    def test_preview_failure_does_not_call_reviewer(self):
        with patch.object(media_tools, 'ffmpeg', side_effect=subprocess.CalledProcessError(1, 'ffmpeg')), \
             patch.object(llm, 'ask_ai') as ask:
            found, _ = review.visual_review(self.folder / 'x.mp4', self.short, [0, 2], ['photo'], self.work)
        self.assertIn('NOT REVIEWED:', found[0])
        ask.assert_not_called()

    def test_download_retry_is_bounded_and_preserves_wikimedia_backoff(self):
        with patch.object(picker.image_sources, 'get_image', side_effect=[None, b'ok']) as download:
            self.assertEqual(picker.download_picture('https://museum/photo'), b'ok')
            self.assertEqual(download.call_count, 2)
        with patch.object(picker.image_sources, 'get_image', return_value=None) as download:
            self.assertIsNone(picker.download_picture('https://upload.wikimedia.org/photo'))
            self.assertEqual(download.call_count, 1)

    def test_recovery_uses_only_reviewed_unused_candidates_and_retains_credit(self):
        short = {'character': '', 'catalog': [{'n': 1, 'era_ok': True, 'sharp': 3, 'what': 'door'},
                                              {'n': 2, 'era_ok': False, 'sharp': 3, 'what': 'wrong era'}],
                 'scenes': [{'narration': 'The door opened.', 'shot': 'door', 'animate': True, 'motion': 'old motion'}]}
        cands = [{'url': 'u1', 'title': 'Door', 'credit': 'CC BY owner'},
                 {'url': 'u2', 'title': 'Wrong door', 'credit': None}]
        chosen, taken = [{'bg': None, 'person': None}], set()
        with patch.object(llm, 'ask_ai', return_value={'picks': [{'scene': 1, 'bg': 2}, {'scene': 1, 'bg': 1}]}), \
             patch.object(picker, 'download_picture', return_value=b'image') as download:
            picker.recover_downloads(short, chosen, cands, taken, [0])
        download.assert_called_once_with('u1')
        self.assertEqual(chosen[0]['bg'], (b'image', 'Door', 'CC BY owner'))
        self.assertEqual(taken, {'u1'})
        self.assertFalse(short['scenes'][0]['animate'])

    def test_duplicate_finalization_does_not_duplicate_logbook_entries(self):
        log = self.root / 'log.md'
        folder = logbook.ROOT / 'output/test/resume-fixture'
        with patch.object(session, 'LOG', log), patch.object(media_tools, 'duration', return_value=2):
            logbook.log_short(self.short, folder)
            logbook.log_short(self.short, folder)
        self.assertEqual(log.read_text().count('\n## Short'), 1)

    def test_long_node_errors_keep_the_actual_error_headline(self):
        message = 'file:///' + 'long-folder/' * 80 + '\nTypeError: k.nothing is not a function\n at stack'
        result = type('Reply', (), {'stderr': message, 'stdout': '', 'returncode': 1})()
        with patch.object(drawn_opener.subprocess, 'run', return_value=result):
            error = drawn_opener.node_run({}, self.work)
        self.assertTrue(error.startswith('TypeError: k.nothing is not a function'))
        self.assertLessEqual(len(error), 600)

    def test_stale_repair_preview_cannot_overwrite_video(self):
        repair = self.work / 'repairs' / 'test'
        repair.mkdir(parents=True)
        media_tools.write_json(repair / 'repair.json', {'index': 0, 'start': 0, 'end': 29, 'graphic': {'x': .5}})
        with patch.object(media_tools, 'ffmpeg') as ffmpeg, self.assertRaises(ValueError):
            scene_repair.apply(self.folder, {'short': self.short}, repair / 'preview.mp4')
        ffmpeg.assert_not_called()


if __name__ == '__main__':
    unittest.main()
