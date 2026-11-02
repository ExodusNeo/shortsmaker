"""Render the opener composition study with the real hook/captions; restore the generated slot afterwards."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import motion, remotion_render
from shortsmaker.config import REMOTION, ROOT


def main():
    target = REMOTION / 'src/full/generated/Custom0.tsx'
    before = target.read_bytes()
    source = (REMOTION / 'src/full/examples/ExampleOpenerAction.tsx').read_text(encoding='utf-8')
    sc = {'start': 0, 'end': 3, 'image': '', 'move': 'in', 'transition': 'cut', 'graphic': None,
          'card': None, 'clip': None, 'full': {'type': 'custom', 'slot': 0, 'seed': 1, 'skin': 'parchment',
                                            'kind': 'diagram', 'title': '', 'cues': [0, .45], 'photos': []}}
    line = 'A rocket sled stops and its rider goes blind'.split()
    props = {'fps': 30, 'total': 3, 'xfade': .3, 'hook': 'SIGHT GONE FOREVER?', 'scenes': [sc],
             'flashes': [], 'cta': None, 'ctaLine': '',
             'words': [{'start': i * .29, 'end': (i + 1) * .29, 'text': word, 'line': i // 3,
                        'emphasis': False} for i, word in enumerate(line)]}
    try:
        target.write_text(source.replace('ExampleOpenerAction', 'Custom0'), encoding='utf-8')
        error = motion.tsc_check()
        if error:
            raise RuntimeError(error)
        remotion_render.make_paper(REMOTION / 'public/paper')
        sheet = motion.preview_custom({'title': 'Opener composition study'}, sc, 0,
                                      ROOT / 'test_renders/opener-preflight', props=props)
        if not sheet:
            raise RuntimeError('Opener preview did not render')
        print(sheet)
    finally:
        target.write_bytes(before)


if __name__ == '__main__':
    main()
