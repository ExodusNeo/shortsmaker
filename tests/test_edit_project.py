"""Tests for the Shotcut timeline made when CHECK lines are left. No AI usage; renders a 3 s project with Shotcut's
melt (skipped if Shotcut isn't installed). Run: .venv\\Scripts\\python.exe tests\\test_edit_project.py"""
import re
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shortsmaker import edit_project, media_tools  # noqa: E402
from shortsmaker.config import SHOTCUT  # noqa: E402

BOUNDS = [0.0, 1.2, 3.0]
ISSUES = ["LOOK at 0:01.5 (scene 2): garbled text", "loudness -18.0 LUFS, target is -14 (too quiet)"]


def short_folder(d: Path) -> Path:
    """A finished Short's work/ in miniature: grey pictures, a see-through graphics layer with a red box at the top
    (ProRes 4444, like Remotion's), voice, music and sounds tracks, one caption line."""
    work = d / "work"
    work.mkdir()
    media_tools.ffmpeg("-f", "lavfi", "-i", "color=gray:s=1080x1920:r=30:d=3", "pictures.mp4", cwd=work)
    media_tools.ffmpeg("-f", "lavfi", "-i", "color=c=black@0:s=1080x1920:r=30:d=3,format=rgba,"
                       "drawbox=x=340:y=200:w=400:h=200:color=red@1:t=fill:replace=1", "-c:v", "prores_ks", "-profile:v", "4444",
                       "-pix_fmt", "yuva444p10le", "graphics.mov", cwd=work)
    media_tools.ffmpeg("-f", "lavfi", "-i", "sine=f=220:d=3", "-ac", "2", "voice.wav", cwd=work)
    media_tools.ffmpeg("-f", "lavfi", "-i", "sine=f=440:d=3", "-ac", "2", "-af", "volume=0.1", "music.wav", cwd=work)
    media_tools.ffmpeg("-f", "lavfi", "-i", "sine=f=880:d=0.3", "-ac", "2", "-af", "adelay=1000:all=1", "sfx.wav", cwd=work)
    (work / "captions.ass").write_text(
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV\nStyle: Default,Impact,120,&H00FFFFFF,&H00000000,&H90000000,0,1,8,4,2,60,60,620\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Text\nDialogue: 0,0:00:00.00,0:00:03.00,Default,HELLO\n", encoding="utf-8")
    return d


def videos(folder: Path) -> list[tuple[str, Path]]:
    return [("V1 pictures", folder / "work" / "pictures.mp4"), ("V2 graphics", folder / "work" / "graphics.mov")]


def test_timeline_has_scenes_captions_sound_and_markers():
    with tempfile.TemporaryDirectory() as d:
        folder = short_folder(Path(d))
        edit_project.make(folder, folder / "work", BOUNDS, ISSUES, videos(folder))
        root = ET.parse(folder / "edit.mlt").getroot()
        names = [p.find("property[@name='shotcut:name']").text for p in root.findall("playlist") if p.get("id").startswith("V")]
        assert names == ["V1 pictures", "V2 graphics", "V3 captions"], names
        for v in ("V0", "V1"):  # pictures and graphics: one clip per scene, so one scene can be resized alone
            entries = root.findall(f"playlist[@id='{v}']/entry")
            assert [(e.get("in"), e.get("out")) for e in entries] == [("0", "35"), ("36", "89")]
        assert root.find("playlist[@id='V2']/entry").get("producer") == "captions"
        blends = [(t.find("property[@name='a_track']").text, t.find("property[@name='b_track']").text)
                  for t in root.findall("tractor/transition") if t.find("property[@name='mlt_service']").text == "qtblend"]
        assert blends == [("0", "1"), ("1", "2"), ("1", "3")], blends  # Shotcut blends every upper track onto V1
        sounds = [p.find("property[@name='shotcut:name']").text for p in root.findall("playlist") if p.get("id").startswith("A")]
        assert sounds == ["A1 voice", "A2 music", "A3 sounds"], sounds
        assert all(root.find(f"tractor/track[@producer='A{k}']").get("hide") == "video" for k in range(3))
        services = [f.find("property[@name='mlt_service']").text for f in root.findall("tractor/filter")]
        assert services == ["volume", "ladspa.1913"], services  # output: gain to -14 LUFS, then the limiter
        markers = root.findall("tractor/properties[@name='shotcut:markers']/properties")
        texts = [m.find("property[@name='text']").text for m in markers]
        colors = [m.find("property[@name='color']").text for m in markers]
        assert texts == ["Scene 1 | loudness -18.0 LUFS, target is -14 (too quiet)", f"Scene 2 | {ISSUES[0]}"], texts
        assert colors == ["#E53935", "#E53935"]
        assert markers[1].find("property[@name='start']").text == "00:00:01.200"
        assert "edit.mlt" in (folder / "edit_in_shotcut.bat").read_text()
        edit_project.remove(folder)
        assert not (folder / "edit.mlt").exists() and not (folder / "edit_in_shotcut.bat").exists()


def test_melt_plays_it_with_the_captions_on_top():
    melt = SHOTCUT.with_name("melt.exe")
    if not melt.exists():
        print("  (skipped: Shotcut not installed)")
        return
    with tempfile.TemporaryDirectory() as d:
        folder = short_folder(Path(d))
        edit_project.make(folder, folder / "work", BOUNDS, [], videos(folder))
        subprocess.run([str(melt), "edit.mlt", "-consumer", "avformat:out.mp4", "vcodec=libx264", "acodec=aac"],
                       cwd=folder, capture_output=True, check=True, timeout=300)
        assert abs(media_tools.duration(folder / "out.mp4") - 3.0) < 0.1
        log = subprocess.run(["ffmpeg", "-hide_banner", "-i", "out.mp4", "-af", "ebur128", "-f", "null", "-"], cwd=folder,
                             capture_output=True, text=True).stderr
        lufs = float(re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", log, re.M)[-1])
        assert abs(lufs - edit_project.LUFS) < 1.0, lufs  # voice + music + sounds together, at the Short's loudness
        # the caption's white letters (HELLO, bottom 620) must be drawn over the grey picture
        px = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1", "-i", "out.mp4", "-frames:v", "1", "-vf",
                             "crop=1080:300:0:1100,format=gray", "-f", "rawvideo", "-"], cwd=folder, capture_output=True).stdout
        assert max(px) > 230, max(px)
        # the graphics layer's red box shows over the picture, and the picture shows around it (alpha kept)
        rgb = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1", "-i", "out.mp4", "-frames:v", "1", "-vf",
                              "scale=108:192", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], cwd=folder, capture_output=True).stdout
        pixel = lambda x, y: tuple(rgb[(y * 108 + x) * 3:(y * 108 + x) * 3 + 3])
        r, g, b = pixel(54, 30)  # inside the box
        assert r > 200 and g < 60 and b < 60, (r, g, b)
        assert all(abs(c - 128) < 20 for c in pixel(54, 100)), pixel(54, 100)  # grey picture below the box


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
