"""Tests for a Blender channel's run (2026-10-22): every scene drawn (no picture picking), the real photo of the
structure on the thumbnail (else a drawing, said in a CHECK line), the review told the drawings are deliberate, and
a Blender failure keeping that Short's files while the batch goes on. No AI usage, no Blender.
Run: .venv\\Scripts\\python.exe tests\\test_blender_run.py"""
import io
import json
import sys
import tempfile
import traceback
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import (  # noqa: E402
    blender_plan, blender_render, channel_profiles, cli, image_sources, llm, logbook, media_tools, picture_pool, review,
    rules, seo, short_render, writing,
)

USABLE = {"era_ok": True, "sharp": 3, "reject": None, "what": "the bridge"}


def jpeg() -> bytes:
    b = io.BytesIO()
    Image.new("RGB", (640, 480), (90, 90, 90)).save(b, "JPEG")
    return b.getvalue()


def drawn_short(d: Path, catalog: list, credit=None) -> dict:
    pool = d / "pool"
    pool.mkdir()
    rows = [{"title": f"File:Bridge {k}.jpg", "url": f"https://upload.wikimedia.org/x{k}.jpg", "credit": credit,
             "small": "", "source": "Wikipedia", "size": 1} for k in range(3)]
    (pool / "pool.json").write_text(json.dumps(rows), encoding="utf-8")
    frames = d / "work" / "blender_frames"
    frames.mkdir(parents=True)
    for f in range(1, 91):
        Image.new("RGB", (108, 192), (200, 30, 30)).save(frames / f"f_{f:04d}.png")
    return {"build": blender_plan.default_build(3), "pool_dir": str(pool), "catalog": catalog,
            "scenes": [{"narration": "x"} for _ in range(3)]}


def test_drawn_choices_have_no_pictures():
    choices = short_render.drawn_choices({"scenes": [{}, {}, {}]})
    assert choices == [{"bg": None, "person": None, "film": None}] * 3


def test_thumbnail_uses_the_real_photo():
    old = image_sources.get_image
    image_sources.get_image = lambda url, what: jpeg() if url.endswith("x1.jpg") else None
    try:
        with tempfile.TemporaryDirectory() as d:
            s = drawn_short(Path(d), [{"n": 2, "hook": True, **USABLE}], credit="Jane Doe")
            pic, credit, check = short_render.drawn_thumbnail(s, Path(d) / "work", [0.0, 1.0, 2.0, 3.0])
            assert pic.name == "thumb_photo.jpg" and pic.exists() and check is None
            assert credit == "Bridge 1 by Jane Doe (Wikimedia Commons)", credit
    finally:
        image_sources.get_image = old


def test_no_photo_uses_a_drawing_and_says_so():
    with tempfile.TemporaryDirectory() as d:
        s = drawn_short(Path(d), [])
        pic, credit, check = short_render.drawn_thumbnail(s, Path(d) / "work", [0.0, 1.0, 2.0, 3.0])
        zoom = s["build"]["beats"].index("zoom")
        assert pic == Path(d) / "work" / "blender_frames" / f"f_{blender_render.scene_frames([0.0, 1.0, 2.0, 3.0])[zoom][1]:04d}.png"
        assert credit is None and "drawing" in check


def test_review_is_told_the_drawings_are_deliberate():
    seen = []
    old_ff, old_ask = media_tools.ffmpeg, llm.ask_ai
    media_tools.ffmpeg = lambda *a, cwd: (Path(cwd) / "sheet1.jpg").write_bytes(b"jpg")
    llm.ask_ai = lambda prompt, fatal=True, read_dir=None, brain=None, bulk=False: seen.append(prompt) or {"issues": []}
    try:
        with tempfile.TemporaryDirectory() as d:
            short = {"title": "T", "scenes": [{"narration": "a"}]}
            review.visual_review(Path(d) / "v.mp4", short, [0.0, 1.0], ["drawn in Blender: wide"], Path(d), drawn=True)
            review.visual_review(Path(d) / "v.mp4", short, [0.0, 1.0], ["photo"], Path(d))
    finally:
        media_tools.ffmpeg, llm.ask_ai = old_ff, old_ask
    assert "deliberate ink drawing" in seen[0] and "deliberate ink drawing" not in seen[1]


def test_blender_failure_is_reported_and_the_batch_goes_on():
    made = []

    def render(short, ch, folder, state=None, fix_round=0):
        folder.mkdir(parents=True)
        (folder / "work").mkdir()
        made.append(folder)
        if short["title"] == "First":
            raise blender_render.BlenderFailed("exit code 1: boom")

    saved = (sys.argv, writing.write_scripts, seo.seo_pass, short_render.render, short_render.prune_work,
             picture_pool.prune_cache, channel_profiles.save_channel, channel_profiles.use_channel, logbook.log_short,
             logbook.vault_page, cli.OUTPUT, rules.require_rules, channel_profiles.load_channel)
    with tempfile.TemporaryDirectory() as d:
        sys.argv = ["make_shorts.py", "2", "strange-history", "claude"]
        writing.write_scripts = lambda ch, n, topics=None, pools=None: [
            {"title": t, "topic": t, "shape": "", "scenes": []} for t in ("First", "Second")]
        seo.seo_pass = lambda shorts, ch: None
        short_render.render = render
        short_render.prune_work = picture_pool.prune_cache = lambda: None
        channel_profiles.save_channel = channel_profiles.use_channel = lambda *a: None
        logbook.log_short = logbook.vault_page = lambda *a: None
        cli.OUTPUT = Path(d)
        rules.require_rules = lambda name: None
        channel_profiles.load_channel = lambda: {"brain": "claude", "done_topics": []}
        try:
            cli.main()
        finally:
            (sys.argv, writing.write_scripts, seo.seo_pass, short_render.render, short_render.prune_work,
             picture_pool.prune_cache, channel_profiles.save_channel, channel_profiles.use_channel, logbook.log_short,
             logbook.vault_page, cli.OUTPUT, rules.require_rules, channel_profiles.load_channel) = saved
        assert len(made) == 2 and not made[0].exists() and made[1].exists()  # nothing half-made is left behind


def test_film_opener_is_skipped_and_bad_bytes_fall_back():
    old, asked = image_sources.get_image, []

    def get(url, what):
        asked.append(url)
        return b"not an image" if url.endswith("x2.jpg") else jpeg()
    image_sources.get_image = get
    try:
        with tempfile.TemporaryDirectory() as d:
            s = drawn_short(Path(d), [{"n": 1, "hook": True, **USABLE}, {"n": 3, "hook": True, **USABLE},
                                      {"n": 2, "hook": False, **USABLE}])
            rows = json.loads((Path(s["pool_dir"]) / "pool.json").read_text(encoding="utf-8"))
            rows[0]["film"] = {"src": rows[0]["url"], "t": 4}  # picture 1 is a film frame
            (Path(s["pool_dir"]) / "pool.json").write_text(json.dumps(rows), encoding="utf-8")
            pic, _, check = short_render.drawn_thumbnail(s, Path(d) / "work", [0.0, 1.0, 2.0, 3.0])
            assert pic.name == "thumb_photo.jpg" and check is None  # picture 3 failed to open, picture 2 is used
            Image.open(pic).verify()
            assert not any(u.endswith("x0.jpg") for u in asked), asked  # the film frame is never downloaded
            assert asked[-1].endswith("x1.jpg"), asked
    finally:
        image_sources.get_image = old


def test_fix_bat_explains_a_drawn_short():
    rendered = []
    with tempfile.TemporaryDirectory() as d:
        work = Path(d) / "out" / "engineering-failures" / "2026-10-22_x" / "work"
        work.mkdir(parents=True)
        (work / "state.json").write_text("{}", encoding="utf-8")
        saved = (cli.OUTPUT, short_render.prune_work, short_render.load_state, channel_profiles.ask_number,
                 rules.require_rules, short_render.render)
        cli.OUTPUT = Path(d) / "out"
        short_render.prune_work = lambda: None
        short_render.load_state = lambda w: {"short": {"build": {"beats": ["wide"]}, "scenes": [{"narration": "a"}]},
                                             "choices": [{}]}
        channel_profiles.ask_number = lambda q, n, default=None: 1
        rules.require_rules = lambda name: None
        short_render.render = lambda *a, **k: rendered.append(a)
        try:
            cli.fix_short()
        finally:
            (cli.OUTPUT, short_render.prune_work, short_render.load_state, channel_profiles.ask_number,
             rules.require_rules, short_render.render) = saved
    assert rendered == []

if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_") and (len(sys.argv) < 2 or n in sys.argv[1:])]
    failed = 0
    for n in names:
        try:
            globals()[n]()
            print(f"PASS {n}")
        except Exception:
            failed += 1
            print(f"FAIL {n}")
            traceback.print_exc()
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(1 if failed else 0)
