"""Media adapters and selection invariants, plus small real FFmpeg checks. No network/AI calls."""

import io
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import audio_library, audio_mix, extra_sources, footage, frame_render, image_sources, media_library, media_menu, media_tools, photo_prep, picture_pool
from shortsmaker.config import ROOT


class MediaTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / ".superpowers" / "media-tests"
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        status = patch.object(media_library, "STATUS", self.root / "source_status.json")
        status.start()
        self.addCleanup(status.stop)

    def picture(self):
        img = Image.new("RGB", (600, 300), "white")
        draw = ImageDraw.Draw(img)
        for x in range(0, 600, 23):
            draw.rectangle((x, 0, x + 10, 250), fill=(x % 255, (x * 3) % 255, (x * 5) % 255))
        return img

    def blob(self, img):
        stream = io.BytesIO()
        img.save(stream, "JPEG")
        return stream.getvalue()

    def test_later_sources_get_space_and_limit_is_respected(self):
        rows = [{"site": "Wiki", "url": str(i)} for i in range(100)] + [{"site": "Archive"}, {"site": "Wellcome"}]
        selected = picture_pool.balanced_candidates(rows, 5)
        self.assertEqual([row["site"] for row in selected[:3]], ["Wiki", "Archive", "Wellcome"])
        self.assertEqual(len(selected), 5)
        self.assertEqual(picture_pool.balanced_candidates(rows, 0), [])

    def test_visual_copies_from_two_websites_are_one_candidate(self):
        img = self.picture()
        rows = [{"url": "a", "thumb": self.blob(img)}, {"url": "b", "thumb": self.blob(img.resize((300, 150)))}]
        self.assertEqual(len(picture_pool.visual_unique(rows)), 1)

    def test_focal_crop_keeps_off_centre_subject(self):
        img = Image.new("RGB", (600, 300), "black")
        ImageDraw.Draw(img).rectangle((0, 0, 150, 300), fill="red")
        centred = photo_prep.vertical_image(img, (0.5, 0.5), (90, 160))
        left = photo_prep.vertical_image(img, (0.1, 0.5), (90, 160))
        self.assertLess(centred.getpixel((45, 80))[0], 20)
        self.assertGreater(left.getpixel((45, 80))[0], 230)

    def test_portrait_ads_are_not_mistaken_for_nine_by_sixteen(self):
        with patch.object(frame_render.subprocess, 'run', return_value=SimpleNamespace(stdout='1080,1350')):
            self.assertFalse(frame_render.fills_frame(self.root / 'ad.mp4'))
        with patch.object(frame_render.subprocess, 'run', return_value=SimpleNamespace(stdout='1080,1920')):
            self.assertTrue(frame_render.fills_frame(self.root / 'ad.mp4'))

    def test_preflight_rejects_broken_original_and_recovers_later(self):
        entries = [{"n": 1, "era_ok": True, "sharp": 3, "reject": None}]
        with patch.object(image_sources, "get_image", return_value=b"not a picture"):
            picture_pool.preflight_pictures([{"url": "broken"}], entries, self.root)
        self.assertTrue(entries[0]["reject"])
        with patch.object(image_sources, "get_image", return_value=self.blob(self.picture())):
            picture_pool.preflight_pictures([{"url": "broken"}], entries, self.root)
        self.assertIsNone(entries[0]["reject"])

    def test_import_keeps_original_and_source_notes(self):
        original = self.root / "advert.jpg"
        original.write_bytes(self.blob(self.picture()))
        with patch.object(media_library, "LIBRARY", self.root / "library"):
            saved = media_library.import_media(original, "Big Mac ad", "McDonalds 1990 USA", "https://brand.test/ad", "Brand; terms")
            found = media_library.local_assets("McDonalds 1990")
        self.assertEqual(original.read_bytes(), saved.read_bytes())
        self.assertEqual(len(found), 1)
        self.assertIn("https://brand.test/ad", found[0]["credit"])
        self.assertEqual(image_sources.get_image(found[0]["url"], "image download"), original.read_bytes())

    def test_europeana_missing_key_does_not_make_a_request(self):
        with patch.object(media_library, "optional_key", return_value=""), \
             patch.object(media_library, "source_status"), patch.object(extra_sources, "source_json") as fetch:
            self.assertEqual(extra_sources.europeana_images("poster"), [])
        fetch.assert_not_called()

    def test_rate_limited_source_cools_down_without_exposing_query_keys(self):
        failure = urllib.error.HTTPError('https://source.test/?key=SECRET', 429, 'busy', {}, None)
        with patch.object(image_sources, 'CACHE', self.root), patch.object(extra_sources, '_unavailable_until', {}), \
             patch.object(media_library, 'source_enabled', return_value=True), patch.object(media_tools, 'fetch', side_effect=failure) as fetch:
            self.assertEqual(extra_sources.source_json('fixture', 'https://source.test/?key=SECRET'), {})
            self.assertEqual(extra_sources.source_json('fixture', 'https://source.test/?key=SECRET'), {})
        self.assertEqual(fetch.call_count, 1)
        self.assertNotIn('SECRET', media_library.STATUS.read_text(encoding='utf-8'))

    def test_collection_parsers_preserve_item_rights_and_source_page(self):
        loc = {"results": [{"title": "Restaurant", "image_url": ["https://img/s.jpg", "https://img/l.jpg"],
                            "id": "https://loc.gov/item/1", "rights": "Rights advisory"}]}
        with patch.object(extra_sources, "source_json", return_value=loc):
            row = extra_sources.loc_images("restaurant")[0]
        self.assertEqual(row["url"], "https://img/l.jpg")
        self.assertIn("Rights advisory", row["credit"])
        self.assertIn("https://loc.gov/item/1", row["credit"])
        wellcome = {"results": [{"id": "123", "title": "Engraving", "thumbnail": {"url": "https://iiif/s.jpg"},
                                 "items": [{"locations": [{"locationType": {"id": "iiif-image"},
                                            "url": "https://iiif/id/info.json", "license": {"label": "CC BY 4.0"}}]}]}]}
        with patch.object(extra_sources, "source_json", return_value=wellcome):
            row = extra_sources.wellcome_images("engraving")[0]
        self.assertEqual(row["url"], "https://iiif/id/full/1920,/0/default.jpg")
        self.assertIn("CC BY 4.0", row["credit"])

    def test_smithsonian_uses_image_rights_not_metadata_rights(self):
        data = {"response": {"rows": [{"title": "Poster", "content": {"descriptiveNonRepeating": {
            "record_link": "https://si.edu/1", "metadata_usage": {"access": "CC0"},
            "online_media": {"media": [{"type": "Images", "usage": {"access": "restricted"},
                                       "content": "https://img/l.jpg", "thumbnail": "https://img/s.jpg"}]}}}}]}}
        with patch.object(extra_sources, "source_json", return_value=data), patch.object(media_library, "optional_key", return_value="fixture"):
            row = extra_sources.smithsonian_images("poster")[0]
        self.assertEqual(row["license"], "restricted")

    def test_brand_parser_keeps_genuine_brand_images(self):
        brands = {"brands": [{"name": "McDonald's", "aliases": ["mcdonald"], "pages": ["https://brand.test/media"]}]}
        html = b'<img src="https://cdn.test/bigmac.jpg" alt="Big Mac"><img src="https://cdn.test/favicon.png">'
        with patch.object(media_library, "settings", return_value=brands), patch.object(media_tools, "fetch", return_value=html):
            found = extra_sources.brand_images("mcdonald commercial")
        self.assertEqual(len(found), 1)
        self.assertIn("Big Mac", found[0]["title"])

    def test_empty_music_mood_never_gets_a_different_mood(self):
        music = self.root / "music"
        (music / "playful").mkdir(parents=True)
        (music / "playful" / "fun.mp3").write_bytes(b"fixture")
        short = {"music_mood": "somber"}
        with patch.object(audio_library, "MUSIC", music):
            self.assertIsNone(audio_library.select_music(short))
        self.assertIn("somber", short["music_note"])

    def test_music_avoids_pending_repeats_and_matches_intensity(self):
        music = self.root / "music"
        (music / "tense").mkdir(parents=True)
        paths = [music / "tense" / f"{i}.mp3" for i in range(4)]
        for path in paths:
            path.write_bytes(b"fixture")
        audio_library.set_audio_metadata(paths[1], approved=False)
        audio_library.set_audio_metadata(paths[2], intensity="low", instruments=["piano"])
        audio_library.set_audio_metadata(paths[3], intensity="high")
        history = music / "recent.json"
        with patch.object(audio_library, "MUSIC", music), patch.object(audio_library, "MUSIC_HISTORY", history):
            audio_library.record_audio(paths[0], music, history, "short-one")
            selected = audio_library.select_music({"music_mood": "tense", "music_intensity": "low", "music_instruments": ["piano"]})
            self.assertEqual(selected, paths[2])
            self.assertEqual(audio_library.select_music({"music_mood": "tense"}, paths[0]), paths[0])
            audio_library.record_audio(paths[2], music, history, "short-one")
            self.assertEqual(len(audio_library.history_read(history)), 1)

    def test_on_demand_music_downloads_only_selected_track_and_is_immediately_usable(self):
        rows = [{'id': 101, 'name': 'Soft piano', 'license': 'CC0', 'tags': ['piano']},
                {'id': 102, 'name': 'Another piano', 'license': 'CC0'}]
        short = {'music_mood': 'somber', 'music_instruments': ['piano']}
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(audio_library, 'MUSIC_HISTORY', self.root / 'recent.json'), \
             patch.object(media_library, 'settings', return_value={}), patch.object(audio_mix, 'freesound_results', return_value=rows) as search, \
             patch.object(audio_mix, 'freesound_preview', return_value=b'fixture audio') as download, \
             patch.object(media_tools, 'duration', return_value=40):
            selected = audio_library.source_music(short)
        self.assertEqual(selected, self.root / 'somber' / 'fs_101.mp3')
        self.assertEqual(download.call_count, 1)
        self.assertEqual(search.call_count, 1)
        self.assertIn('piano', search.call_args.args[0])
        self.assertTrue(audio_library.usable_audio(selected))
        self.assertEqual(audio_library.audio_metadata(selected)['review_status'], 'automatic')
        self.assertIn('https://freesound.org/s/101/', selected.with_suffix('.mp3.txt').read_text(encoding='utf-8'))
        self.assertFalse((selected.parent / 'fs_102.mp3').exists())

    def test_on_demand_music_reuses_saved_track_without_search(self):
        prior = self.root / 'saved.mp3'
        prior.write_bytes(b'fixture')
        with patch.object(audio_mix, 'freesound_results') as search:
            self.assertEqual(audio_library.source_music({'music_mood': 'tense'}, prior), prior)
        search.assert_not_called()

    def test_on_demand_music_reuses_cached_search_result_without_download(self):
        cached = self.root / 'tense' / 'fs_101.mp3'
        cached.parent.mkdir()
        cached.write_bytes(b'fixture')
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(audio_library, 'MUSIC_HISTORY', self.root / 'recent.json'), \
             patch.object(media_library, 'settings', return_value={}), \
             patch.object(audio_mix, 'freesound_results', return_value=[{'id': 101, 'license': 'CC0'}]), \
             patch.object(audio_mix, 'freesound_preview') as download:
            self.assertEqual(audio_library.source_music({'music_mood': 'tense'}), cached)
        download.assert_not_called()

    def test_on_demand_music_failed_search_keeps_local_fallback(self):
        local = self.root / 'playful' / 'owner.mp3'
        local.parent.mkdir()
        local.write_bytes(b'fixture')
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(audio_library, 'MUSIC_HISTORY', self.root / 'recent.json'), \
             patch.object(media_library, 'settings', return_value={}), patch.object(audio_mix, 'freesound_results', return_value=[]), \
             patch.object(audio_mix, 'freesound_preview') as download:
            self.assertEqual(audio_library.source_music({'music_mood': 'playful'}), local)
        download.assert_not_called()

    def test_on_demand_music_invalid_selected_audio_falls_back_without_bulk_retry(self):
        local = self.root / 'epic' / 'owner.mp3'
        local.parent.mkdir()
        local.write_bytes(b'fixture')
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(audio_library, 'MUSIC_HISTORY', self.root / 'recent.json'), \
             patch.object(media_library, 'settings', return_value={}), \
             patch.object(audio_mix, 'freesound_results', return_value=[{'id': 101, 'license': 'CC0'}, {'id': 102, 'license': 'CC0'}]), \
             patch.object(audio_mix, 'freesound_preview', return_value=b'bad audio') as download, \
             patch.object(media_tools, 'duration', return_value=1):
            self.assertEqual(audio_library.source_music({'music_mood': 'epic'}), local)
        self.assertEqual(download.call_count, 1)
        self.assertFalse((local.parent / 'fs_101.part.mp3').exists())
        self.assertFalse((local.parent / 'fs_101.mp3').exists())

    def test_on_demand_music_respects_rejection_and_avoids_recent_tracks(self):
        mood = self.root / 'mysterious'
        mood.mkdir()
        rejected = mood / 'fs_101.mp3'
        rejected.write_bytes(b'fixture')
        audio_library.set_audio_metadata(rejected, approved=False)
        recent = mood / 'fs_102.mp3'
        recent.write_bytes(b'fixture')
        history = self.root / 'recent.json'
        audio_library.record_audio(recent, self.root, history, 'previous-short')
        rows = [{'id': 101, 'license': 'CC0'}, {'id': 102, 'license': 'CC0'}, {'id': 103, 'license': 'CC0'}]
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(audio_library, 'MUSIC_HISTORY', history), \
             patch.object(media_library, 'settings', return_value={}), patch.object(audio_mix, 'freesound_results', return_value=rows), \
             patch.object(audio_mix, 'freesound_preview', return_value=b'fixture audio'), patch.object(media_tools, 'duration', return_value=40):
            self.assertEqual(audio_library.source_music({'music_mood': 'mysterious'}), mood / 'fs_103.mp3')
        self.assertFalse(audio_library.usable_audio(rejected))

    def test_on_demand_music_can_be_disabled_and_skips_unrecognized_mood(self):
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(media_library, 'settings', return_value={'music_online': False}), \
             patch.object(audio_mix, 'freesound_results') as search:
            self.assertIsNone(audio_library.source_music({'music_mood': 'somber'}))
            self.assertIsNone(audio_library.source_music({'music_mood': 'unknown'}))
        search.assert_not_called()

    def test_on_demand_music_prefers_fresh_local_track_when_online_matches_are_recent(self):
        mood = self.root / 'tense'
        mood.mkdir()
        recent, fresh = mood / 'fs_101.mp3', mood / 'owner.mp3'
        recent.write_bytes(b'fixture')
        fresh.write_bytes(b'fixture')
        history = self.root / 'recent.json'
        audio_library.record_audio(recent, self.root, history, 'previous-short')
        with patch.object(audio_library, 'MUSIC', self.root), patch.object(audio_library, 'MUSIC_HISTORY', history), \
             patch.object(media_library, 'settings', return_value={}), \
             patch.object(audio_mix, 'freesound_results', return_value=[{'id': 101, 'license': 'CC0'}]), \
             patch.object(audio_mix, 'freesound_preview') as download:
            self.assertEqual(audio_library.source_music({'music_mood': 'tense'}), fresh)
        download.assert_not_called()

    def test_sound_main_impact_is_aligned_and_long_overlap_loses(self):
        for name in ("story.wav", "stamp.wav"):
            (self.root / name).write_bytes(b"fixture")
        candidates = [{"sound": "story.wav", "t": 2, "gain": .3, "prio": 9, "what": "story sound: bell"},
                      {"sound": "stamp.wav", "t": 3, "gain": .6, "prio": 6, "what": "stamp"}]
        with patch.object(audio_mix, "SFX", self.root), patch.object(audio_library, "sound_profile", return_value={"impact": .4, "duration": 2}):
            events = audio_mix.schedule_sounds(candidates, 10)
        self.assertEqual(len(events), 1)
        self.assertAlmostEqual(events[0]["t"] + .4, 2)

    def test_sound_early_impact_uses_trim_instead_of_delaying_word(self):
        (self.root / "bell.wav").write_bytes(b"fixture")
        with patch.object(audio_mix, "SFX", self.root), patch.object(audio_library, "sound_profile", return_value={"impact": .4, "duration": 2}):
            event = audio_mix.schedule_sounds([{"sound": "bell.wav", "t": .1, "gain": .3, "prio": 9, "what": "story sound: bell"}], 4)[0]
        self.assertAlmostEqual(event["trim"], .3)
        self.assertEqual(event["t"], 0)

    def test_freesound_fetch_tries_next_preview(self):
        rows = [{"id": 1}, {"id": 2}]
        with patch.object(audio_mix, "freesound_results", return_value=rows), patch.object(audio_mix, "freesound_preview", side_effect=[None, b"audio"]):
            self.assertEqual(audio_mix.freesound_fetch("bell"), (b"audio", rows[1]))

    def test_new_downloads_wait_for_review_and_keep_credit(self):
        row = {"id": 15, "name": "Sad piano", "tags": ["piano"], "license": "CC0"}
        with patch.object(media_menu, "MUSIC", self.root), patch.object(audio_mix, "freesound_results", return_value=[row]), \
             patch.object(audio_mix, "freesound_preview", return_value=b"audio"):
            path = media_menu.download_audio_choices("sad piano", "somber")[0]
        self.assertFalse(audio_library.usable_audio(path))
        self.assertIn("freesound.org/s/15", path.with_suffix(".mp3.txt").read_text(encoding="utf-8"))
        audio_library.set_audio_metadata(path, approved=True)
        self.assertTrue(audio_library.usable_audio(path))

    def test_owner_audio_import_preserves_original_and_waits_for_approval(self):
        original = self.root / "owner-song.mp3"
        original.write_bytes(b"owner audio fixture")
        with patch.object(audio_library, "MUSIC", self.root / "music"):
            target = audio_library.import_audio_file(original, "Owner song", "somber", "Owner's recording")
        self.assertEqual(target.read_bytes(), original.read_bytes())
        self.assertFalse(audio_library.usable_audio(target))
        self.assertEqual(target.parent.name, "somber")

    def test_commercial_queries_preserve_product_year_and_country(self):
        queries = footage.commercial_queries(["McDonald's Arch Deluxe USA 1996", "old railway"])
        self.assertIn("McDonald's Arch Deluxe USA 1996", queries)
        self.assertIn("McDonald's", queries)

    def test_real_shot_detection_and_clip_keep_full_source_frame(self):
        path = self.root / "advert.mp4"
        media_tools.ffmpeg("-f", "lavfi", "-i", "color=red:s=320x240:r=10:d=1", "-f", "lavfi", "-i", "color=blue:s=320x240:r=10:d=1",
                           "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-c:v", "libx264", str(path), cwd=self.root)
        film = {"src": str(path), "dur": 2, "local_path": str(path), "site": "Local library", "t": .5}
        with patch.object(image_sources, "CACHE", self.root):
            moments = footage.shot_moments(film)
        self.assertEqual(len(moments), 2)
        result = footage.film_piece(film, self.root / "piece.mp4")
        self.assertIsNotNone(result)
        with Image.open(io.BytesIO(result[0])) as img:
            self.assertEqual(img.size, (320, 240))

    def test_real_music_preview_and_sound_profile(self):
        voice, music, output = self.root / "voice.wav", self.root / "music.wav", self.root / "preview.wav"
        media_tools.ffmpeg("-f", "lavfi", "-i", "sine=f=400:d=2", str(voice), cwd=self.root)
        media_tools.ffmpeg("-f", "lavfi", "-i", "sine=f=900:d=3", str(music), cwd=self.root)
        audio_library.preview_mix(voice, music, output)
        self.assertGreater(media_tools.duration(output), 1.9)
        profile = audio_library.sound_profile(voice)
        self.assertAlmostEqual(profile["duration"], 2, places=1)
        audio_library.set_audio_metadata(voice, impact_override=.2)
        # Explicit adjustments remain effective after profile invalidation.
        meta = audio_library.audio_metadata(voice)
        meta.pop("profile_stamp")
        media_tools.write_json(voice.with_suffix(".wav.json"), meta)
        self.assertAlmostEqual(audio_library.sound_profile(voice)["impact"], .2)

    def test_steady_sound_has_no_impact_but_a_hit_keeps_it(self):
        static, hit = self.root / "static.wav", self.root / "hit.wav"
        media_tools.ffmpeg("-f", "lavfi", "-i", "anoisesrc=d=3:a=0.3:seed=7", str(static), cwd=self.root)
        media_tools.ffmpeg("-f", "lavfi", "-i", "anoisesrc=d=2:a=0.02:seed=7", "-f", "lavfi", "-i", "sine=f=800:d=0.05",
                           "-filter_complex", "[1]adelay=1200,apad[b];[0][b]amix=inputs=2:normalize=0:duration=first",
                           str(hit), cwd=self.root)
        self.assertEqual(audio_library.sound_profile(static)["impact"], 0)
        self.assertAlmostEqual(audio_library.sound_profile(hit)["impact"], 1.2, delta=0.05)

    def test_sound_masking_flags_noise_under_the_voice_not_a_short_hit(self):
        from shortsmaker import review
        voice, noise, tap = self.root / "voice.wav", self.root / "noise.wav", self.root / "tap.wav"
        media_tools.ffmpeg("-f", "lavfi", "-i", "sine=f=300:d=6", "-af", "volume=0.5", str(voice), cwd=self.root)
        media_tools.ffmpeg("-f", "lavfi", "-i", "anoisesrc=d=2:a=0.2:seed=3", "-af", "adelay=2000,apad=whole_dur=6",
                           str(noise), cwd=self.root)
        media_tools.ffmpeg("-f", "lavfi", "-i", "anoisesrc=d=0.3:a=0.2:seed=3", "-af", "adelay=2000,apad=whole_dur=6",
                           str(tap), cwd=self.root)
        found = review.sound_masking(voice, noise, [0, 3, 6])
        self.assertEqual(len(found), 1, found)
        self.assertIn("at 0:02.0 (scene 1)", found[0])
        self.assertEqual(review.sound_masking(voice, tap, [0, 3, 6]), [])
        self.assertEqual(review.sound_masking(voice, self.root / "none.wav", [0, 6]), [])


if __name__ == "__main__":
    unittest.main()
