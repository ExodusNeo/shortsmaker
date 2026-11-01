"""A real FFmpeg/Python render with fake AI verifies stage saves, voice reuse and post-render resume."""
import io
from contextlib import ExitStack
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import audio_library, audio_mix, checkpoints, cli, gpu, llm, media_tools, picker, review, session, short_render


class RenderResumeTests(unittest.TestCase):
    def test_real_video_reuses_voice_and_resumes_reports_without_rendering(self):
        self.render_fixture(False)

    def test_real_video_with_music_offset_and_story_sound_keeps_mix_and_resume(self):
        self.render_fixture(True)

    def render_fixture(self, with_audio):
        base = Path(__file__).resolve().parents[1] / '.superpowers' / 'reliability-verification'
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as tmp:
            root = Path(tmp)
            folder, work = root / 'test' / 'short', root / 'test' / 'short' / 'work'
            work.mkdir(parents=True)
            music = root / 'music'
            music.mkdir()
            sfx = root / 'sfx'
            sfx.mkdir()
            if with_audio:
                (music / 'playful').mkdir()
                track = music / 'playful' / 'fixture.wav'
                media_tools.ffmpeg('-f', 'lavfi', '-i', 'sine=frequency=900:duration=4', str(track), cwd=work)
                audio_library.set_audio_metadata(track, start=.5)
                media_tools.ffmpeg('-f', 'lavfi', '-i', 'sine=frequency=1400:duration=0.4', str(sfx / 'bell.wav'), cwd=work)
            short = {'title': 'Test', 'topic': 'Door', 'palette': 'parchment', 'hook_text': 'THE DOOR',
                     'hook_options': [], 'thumbnail_prompt': '', 'scenes': [
                         {'narration': 'A door opened.', 'shot': 'A door', 'image_search': 'door', 'ai_image': '',
                          'full': None, 'person': None, 'graphic': None, 'sound': None, 'animate': False,
                          'move': 'in', 'transition': 'cut', 'look': None, 'emphasis': None}]}
            ch = {'voice': 'fixture', 'done_topics': []}
            short['music_mood'] = 'playful' if with_audio else ''
            if with_audio:
                short['scenes'][0]['sound'] = {'sound': 'bell', 'word': 'door', 'file': 'bell.wav'}
            picture = io.BytesIO()
            Image.new('RGB', (320, 600), (70, 90, 130)).save(picture, 'JPEG')
            choices = [{'bg': (picture.getvalue(), 'Photo', None), 'person': None}]

            def voice(*args):
                media_tools.ffmpeg('-f', 'lavfi', '-i', 'sine=frequency=440:duration=1.2', '0.wav', cwd=work)
                return [(work / '0.wav', [(.05, .3, 'A'), (.3, .7, 'door'), (.7, 1.1, 'opened.')])]

            with ExitStack() as stack:
                for context in [
patch.object(session, 'RULE_SETTINGS', {}), patch.object(session, 'RULES', {}), 
                 patch.object(session, 'SHORT_FORM', False), patch.object(session, 'VEO_HANDOFF', False), 
                 patch.object(short_render, 'MUSIC', music),
                 patch.object(short_render, 'SFX', sfx), patch.object(audio_mix, 'SFX', sfx),
                 patch.object(audio_library, 'MUSIC', music), patch.object(audio_library, 'MUSIC_HISTORY', music / 'recent.json'),
                 patch.object(audio_library, 'SOUND_HISTORY', sfx / 'recent.json'),
                 patch.object(short_render.remotion_render, 'wants_remotion', return_value=False), 
                 patch.object(picker, 'choose_images', return_value=choices), patch.object(picker, 'rescue_graphics'), 
                 patch.object(short_render.plan_rules, 'mark_details'), 
                 patch.object(gpu, 'local_voice', side_effect=voice), 
                 patch.object(gpu, 'moss_images', return_value=set()), patch.object(gpu, 'gemini_images', return_value=set()), 
                 patch.object(gpu, 'local_clips', return_value={}), patch.object(short_render, 'use_opener', return_value=None), 
                 patch.object(short_render.audio_mix, 'sfx_events', side_effect=audio_mix.sfx_events if with_audio else lambda *a: []),
                 patch.object(short_render.audio_mix, 'make_sfx'), 
                 patch.object(media_tools, 'video_encoder', return_value=['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28']), 
                 patch.object(review, 'quality_check', return_value=[]), 
                 patch.object(review, 'visual_review', return_value=([], {})), 
                 patch.object(review, 'first_second_check', return_value=([], None)), 
                 patch.object(llm, 'ask_ai', side_effect=AssertionError('No AI calls expected'))
                ]:
                    stack.enter_context(context)
                make_voice = gpu.local_voice
                checkpoints.begin(folder, short, 'codex-only')
                short_render.render(short, ch, folder)
                self.assertTrue((folder / 'short.mp4').is_file())
                self.assertEqual(checkpoints.read(work / 'progress.json')['stage'], 'rendered')
                self.assertTrue((work / 'render-context.json').is_file())
                if with_audio:
                    self.assertTrue((folder / 'music_preview.wav').is_file())
                    self.assertTrue((work / 'music.wav').is_file())
                    self.assertTrue((work / 'sfx.wav').is_file())
                    self.assertEqual(short['music_start'], .5)
                short_render.render(short, ch, folder, short_render.load_state(work))
                self.assertEqual(make_voice.call_count, 1)
                self.assertGreater(media_tools.duration(folder / 'short.mp4'), 1)
                # Simulate a crash after encoding, before the batch finalized the Short.
                with patch.object(cli.rules, 'require_rules'), patch.object(cli.channel_profiles, 'use_channel'), \
                     patch.object(cli.channel_profiles, 'load_channel', return_value=ch), \
                     patch.object(cli, 'finish_short'), patch.object(short_render, 'render') as render:
                    cli.resume_runs(folder)
                render.assert_not_called()
                self.assertTrue((folder / 'upload.txt').is_file())
                self.assertTrue((folder / 'edit_plan.txt').is_file())
                if with_audio:
                    self.assertEqual(short_render.load_state(work)['short']['music_start'], .5)
                    self.assertEqual(len(audio_library.history_read(music / 'recent.json')), 1)


if __name__ == '__main__':
    unittest.main()
