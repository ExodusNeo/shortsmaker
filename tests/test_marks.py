"""Detail coordinates must be chosen on the framing that MarkCard actually displays."""
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import llm, photo_prep, plan_rules


class MarkTests(unittest.TestCase):
    def test_grid_uses_cleaned_framing_without_replacing_source(self):
        raw, cleaned = io.BytesIO(), io.BytesIO()
        Image.new('RGB', (500, 800), 'white').save(raw, 'JPEG')
        Image.new('RGB', (300, 600), 'navy').save(cleaned, 'JPEG')
        source = raw.getvalue()
        scene = {'narration': 'A rabbit on the page.', 'graphic': None, 'person': None}
        short = {'title': 'A page', 'scenes': [dict(scene), scene]}
        choices = [{'bg': None}, {'bg': (source, 'scan', None)}]

        def choose(prompt, **kwargs):
            with Image.open(kwargs['read_dir'] / 'scene2.jpg') as grid:
                self.assertEqual(grid.size, (300, 600))
                self.assertLess(grid.getpixel((145, 345))[0], 40)
            return {'marks': [{'scene': 2, 'cell': 'F3', 'label': 'RABBIT'}]}

        with tempfile.TemporaryDirectory() as directory, \
             patch.object(photo_prep, 'clean_photo', return_value=cleaned.getvalue()) as clean, \
             patch.object(llm, 'ask_ai', side_effect=choose):
            plan_rules.mark_details(short, choices, Path(directory))
        clean.assert_called_once_with(source)
        self.assertEqual(scene['graphic']['x'], .55)
        self.assertEqual(scene['graphic']['y'], .25)
        self.assertEqual(choices[1]['bg'][0], source)


if __name__ == '__main__':
    unittest.main()
