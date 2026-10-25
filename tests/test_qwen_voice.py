"""Word matching for the Qwen voice's captions (no GPU, no models).
Run: local_ai\\qwen_venv\\Scripts\\python.exe tests\\test_qwen_voice.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "local_ai"))
from qwen_voice import align_words, say_number, spoken_sentence  # noqa: E402


def test_numbers():
    assert say_number("1932").split() == ["nineteen", "thirty-two"]
    assert say_number("20,000").split() == ["twenty", "thousand"]
    assert say_number("1880s").split() == ["eighteen", "eighties"]
    assert say_number("$10,000").split() == ["ten", "thousand", "dollars"]
    assert say_number("$1").split() == ["one", "dollar"]
    assert say_number("$800M").split() == ["eight", "hundred", "million", "dollars"]
    assert say_number("$800-million").split() == ["eight", "hundred", "million", "dollars"]
    assert say_number("3rd").split() == ["third"]
    assert say_number("40%").split() == ["forty", "percent"]
    assert "point" in say_number("3.5")


def test_dollar_scale_word_order():
    assert spoken_sentence("Two owners made $800 million folding their team.") == (
        "Two owners made eight hundred million dollars folding their team.")
    assert spoken_sentence("They paid $1.5 million, buying the club.") == (
        "They paid one point five million dollars, buying the club.")
    assert spoken_sentence("TV deals sent $17.45 million yearly.") == (
        "TV deals sent seventeen point four five million dollars yearly.")
    got = dict(align_words("Two owners made $800 million folding their team."))
    assert got["$800"] == ["eight", "hundred"]
    assert got["million"] == ["million", "dollars"]


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
