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
from shortsmaker import checkpoints, cli, gpu, llm, media_tools, picker, review, session, short_render


class RenderResumeTests(unittest.TestCase):
    def test_real_video_reuses_voice_and_resumes_reports_without_rendering(self):
        base = Path(__file__).resolve().parents[1] / '.superpowers' / 'reliability-verification'
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as tmp:
            root = Path(tmp)
            folder, work = root / 'test' / 'short', root / 'test' / 'short' / 'work'
            work.mkdir(parents=True)
            music = root / 'music'
            music.mkdir()
            short = {'title': 'Test', 'topic': 'Door', 'palette': 'parchment', 'hook_text': 'THE DOOR',
                     'hook_options': [], 'thumbnail_prompt': '', 'scenes': [
                         {'narration': 'A door opened.', 'shot': 'A door', 'image_search': 'door', 'ai_image': '',
                          'full': None, 'person': None, 'graphic': None, 'sound': None, 'animate': False,
                          'move': 'in', 'transition': 'cut', 'look': None, 'emphasis': None}]}
            ch = {'voice': 'fixture', 'done_topics': []}
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
                 patch.object(short_render.remotion_render, 'wants_remotion', return_value=False), 
                 patch.object(picker, 'choose_images', return_value=choices), patch.object(picker, 'rescue_graphics'), 
                 patch.object(short_render.plan_rules, 'mark_details'), 
                 patch.object(gpu, 'local_voice', side_effect=voice), 
                 patch.object(gpu, 'moss_images', return_value=set()), patch.object(gpu, 'gemini_images', return_value=set()), 
                 patch.object(gpu, 'local_clips', return_value={}), patch.object(short_render, 'use_opener', return_value=None), 
                 patch.object(short_render.audio_mix, 'sfx_events', return_value=[]), 
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


if __name__ == '__main__':
    unittest.main()
