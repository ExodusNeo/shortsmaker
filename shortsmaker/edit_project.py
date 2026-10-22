"""A Shotcut timeline of a finished Short, for fixing by hand what the automatic fix rounds left (the CHECK lines).
Shotcut (open source, github.com/mltframework/shotcut, portable copy in D:\\Shotcut) opens MLT XML directly."""

import re
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from shortsmaker import media_tools
from shortsmaker.config import FPS, H, SHOTCUT, W

LUFS = -14  # same target as the final mix in render()
SOUNDS = (("A1 voice", "voice.wav"), ("A2 music", "music.wav"), ("A3 sounds", "sfx.wav"))  # render() writes these in work/


def caption_layer(work: Path, total: float) -> None:
    """work/captions.mov: the captions alone on a see-through background, from the same captions.ass the Python
    renderer burns in (it mirrors Remotion's captions), so a scene replaced in Shotcut keeps its words."""
    media_tools.ffmpeg("-f", "lavfi", "-i", f"color=c=black@0:s={W}x{H}:r={FPS}:d={total:.3f},format=rgba",
                       "-vf", "subtitles=captions.ass:alpha=1", "-c:v", "qtrle", "captions.mov", cwd=work)


def master_gain(tracks: list[Path]) -> float:
    """dB that brings the tracks played together to LUFS, like the final mix's loudness pass; 0 if unmeasurable."""
    args = [a for t in tracks for a in ("-i", str(t))]
    out = subprocess.run(["ffmpeg", "-hide_banner", *args, "-filter_complex",
                          f"amix=inputs={len(tracks)}:normalize=0,ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    found = re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", out, re.M)
    return LUFS - float(found[-1]) if found and float(found[-1]) > -70 else 0.0


def project_xml(videos: list[tuple[str, Path]], captions: Path, sounds: list[tuple[str, Path]], gain_db: float,
                bounds: list[float], issues: list[str]) -> str:
    """The video tracks bottom-up (pictures, then graphics drawn over them), each cut into one clip per scene, the
    captions above them, A1.. = voice, music, sounds; on the output a gain to the Short's loudness and a -1.5 dB
    limiter; one marker per scene, red and carrying the CHECK lines that name it (lines naming no scene go on scene 1)."""
    f = lambda t: round(t * FPS)
    end = f(bounds[-1]) - 1
    notes: dict[int, list[str]] = {}
    for issue in issues:
        m = re.search(r"scene (\d+)", issue)
        notes.setdefault(int(m.group(1)) - 1 if m else 0, []).append(issue)

    def chain(cid: str, path: Path) -> str:
        return (f'<chain id="{cid}" out="{end}"><property name="resource">{escape(path.as_posix())}</property>'
                f'<property name="mlt_service">avformat-novalidate</property></chain>')

    def prop(name: str, value) -> str:
        return f'<property name="{name}">{escape(str(value))}</property>'

    def clock(frame: int) -> str:
        return f"{frame // FPS // 3600:02d}:{frame // FPS // 60 % 60:02d}:{frame // FPS % 60:02d}.{round(frame % FPS * 1000 / FPS):03d}"

    n, nv = len(bounds) - 1, len(videos) + 1  # nv: video tracks incl. captions
    tracks = "".join(
        f'<playlist id="V{v}">{prop("shotcut:video", 1)}{prop("shotcut:name", name)}'
        + "".join(f'<entry producer="v{v}s{i}" in="{f(bounds[i])}" out="{f(bounds[i + 1]) - 1}"/>' for i in range(n))
        + "</playlist>" for v, (name, _) in enumerate(videos))
    markers = "".join(
        f'<properties name="{i}">{prop("text", " | ".join([f"Scene {i + 1}", *notes.get(i, [])]))}'
        f'{prop("start", clock(f(bounds[i])))}{prop("end", clock(f(bounds[i])))}'
        f'{prop("color", "#E53935" if i in notes else "#9E9E9E")}</properties>' for i in range(n))
    audio = "".join(f'<playlist id="A{k}">{prop("shotcut:audio", 1)}{prop("shotcut:name", name)}'
                    f'<entry producer="sound{k}" in="0" out="{end}"/></playlist>' for k, (name, _) in enumerate(sounds))
    mix = "".join(f'<transition>{prop("a_track", 0)}{prop("b_track", k)}{prop("mlt_service", "mix")}'
                  f'{prop("always_active", 1)}{prop("sum", 1)}</transition>' for k in range(1, 1 + nv + len(sounds)))
    # like Shotcut's own: every upper video track blends onto V1 (the bottom one); V1's (onto the background) stays off
    blend = "".join(f'<transition>{prop("a_track", min(k - 1, 1))}{prop("b_track", k)}{prop("mlt_service", "qtblend")}'
                    f'{prop("threads", 0)}{prop("disable", int(k == 1))}</transition>' for k in range(1, 1 + nv))
    output = (f'<filter>{prop("mlt_service", "volume")}{prop("level", f"{gain_db:.2f}")}{prop("shotcut:filter", "audioGain")}</filter>'
              f'<filter>{prop("mlt_service", "ladspa.1913")}{prop("0", 0)}{prop("1", -1.5)}{prop("2", 0.51)}</filter>')
    return f"""<?xml version="1.0" encoding="utf-8"?>
<mlt LC_NUMERIC="C" version="7.41.0" title="ShortsMaker" producer="main_bin">
<profile description="Short 1080x1920 {FPS} fps" width="{W}" height="{H}" progressive="1" sample_aspect_num="1" sample_aspect_den="1" display_aspect_num="9" display_aspect_den="16" frame_rate_num="{FPS}" frame_rate_den="1" colorspace="709"/>
<playlist id="main_bin">{prop("xml_retain", 1)}</playlist>
<producer id="black" in="0" out="{end}">{prop("length", end + 1)}{prop("eof", "pause")}{prop("resource", 0)}{prop("mlt_service", "color")}{prop("mlt_image_format", "rgba")}{prop("set.test_audio", 0)}</producer>
<playlist id="background"><entry producer="black" in="0" out="{end}"/></playlist>
{"".join(chain(f"v{v}s{i}", path) for v, (_, path) in enumerate(videos) for i in range(n))}
{chain("captions", captions)}
{"".join(chain(f"sound{k}", path) for k, (_, path) in enumerate(sounds))}
{tracks}
<playlist id="V{nv - 1}">{prop("shotcut:video", 1)}{prop("shotcut:name", f"V{nv} captions")}<entry producer="captions" in="0" out="{end}"/></playlist>
{audio}
<tractor id="tractor0" title={quoteattr("ShortsMaker")} in="0" out="{end}">{prop("shotcut", 1)}{prop("shotcut:projectAudioChannels", 2)}<properties name="shotcut:markers">{markers}</properties>
<track producer="background"/>{"".join(f'<track producer="V{v}"/>' for v in range(nv))}{"".join(f'<track producer="A{k}" hide="video"/>' for k in range(len(sounds)))}
{mix}{blend}{output}
</tractor>
</mlt>
"""


def make(folder: Path, work: Path, bounds: list[float], issues: list[str], videos: list[tuple[str, Path]]) -> None:
    """folder/edit.mlt + edit_in_shotcut.bat for a finished Short. `videos` = (track name, file) bottom-up, without
    captions; they and the SOUNDS must already exist."""
    caption_layer(work, bounds[-1])
    sounds = [(name, work / file) for name, file in SOUNDS if (work / file).exists()]
    (folder / "edit.mlt").write_text(project_xml(videos, work / "captions.mov", sounds,
                                                 master_gain([p for _, p in sounds]), bounds, issues), encoding="utf-8")
    # portable settings next to Shotcut, on D: like everything else
    (folder / "edit_in_shotcut.bat").write_text(
        f'@echo off\r\nstart "" "{SHOTCUT}" --appdata "{SHOTCUT.parent / "appdata"}" "%~dp0edit.mlt"\r\n', encoding="utf-8")


def remove(folder: Path) -> None:
    """A re-render with nothing left to fix: an old timeline would no longer match the new video."""
    for name in ("edit.mlt", "edit_in_shotcut.bat"):
        (folder / name).unlink(missing_ok=True)
