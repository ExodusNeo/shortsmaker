"""Word matching for the Qwen voice's captions (no GPU, no models).
Run: local_ai\\qwen_venv\\Scripts\\python.exe tests\\test_qwen_voice.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "local_ai"))
from qwen_voice import align_words, say_number  # noqa: E402


def test_numbers():
    assert say_number("1932").split() == ["nineteen", "thirty-two"]
    assert say_number("20,000").split() == ["twenty", "thousand"]
    assert say_number("1880s").split() == ["eighteen", "eighties"]
    assert say_number("$10,000").split() == ["ten", "thousand", "dollars"]
    assert say_number("3rd").split() == ["third"]
    assert say_number("40%").split() == ["forty", "percent"]
    assert "point" in say_number("3.5")


def test_caption_words_keep_what_is_written():
    got = align_words("In 1932, the army didn't win - Köpenick & co.")
    assert [w for w, _ in got] == ["In", "1932,", "the", "army", "didn't", "win -", "Köpenick", "&", "co."]
    parts = dict(got)
    assert parts["1932,"] == ["nineteen", "thirty", "two"]
    assert parts["didn't"] == ["didn't"]
    assert parts["Köpenick"] == ["kopenick"]
    assert parts["&"] == ["and"]


def test_every_aligned_word_is_in_the_aligner_alphabet():
    allowed = set("abcdefghijklmnopqrstuvwxyz'")
    for _, parts in align_words("Emu War: 'The gun jammed!' 12 kills — 1,000 emus; Meredith's “army”."):
        assert parts and all(p and set(p) <= allowed for p in parts), parts


COUNTED = {  # shortsmaker/gpu.py spoken_count() must give the same counts (tests/test_story.py checks that side)
    "In 1932, the army didn't win - Köpenick & co.": 9,
    "Emu War: 'The gun jammed!' 12 kills — 1,000 emus; Meredith's “army”.": 11,
    "He paid $4,500 - a fortune - in the 1880s.": 8,
}


def test_caption_word_counts_match_the_scene_splitter():
    for text, n in COUNTED.items():
        assert len(align_words(text)) == n, (text, len(align_words(text)))


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"{len(tests)}/{len(tests)} passed")
