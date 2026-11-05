"""3D openers (owner, 2026-11-05, after liking the 3D test of the wooden-eagle opener): scene 1 as flat drawn cut-outs
standing in a lit three.js set (remotion/src/Opener3D.tsx), filmed by a moving camera. The AI writes only a stage
description against a fixed set and prop library (drawn/STAGE3D.md) and draws the cut-outs with the drawing kit
(drawn/cutouts.mjs paints them); this file checks it, renders it, and runs the same art-director loop as the drawn
opener (drawn_opener.review, PASS, FIXES). drawn_opener.make_opener tries this first; when it fails, the drawn
opener is made instead. Lesson from the removed Blender openers (2026-10-30): the AI building scenes freely was
inconsistent, so it only places and frames fixed parts here."""

import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from shortsmaker import drawn_opener, llm, media_tools
from shortsmaker.config import FPS, ROOT

REMOTION = ROOT / "remotion"
STAGE = ROOT / "drawn" / "STAGE3D.md"
PUBLIC = REMOTION / "public" / "opener3d" / "job"  # Remotion loads images only from its public folder
TIMEOUT = 900
PLACES, MOODS = ("room", "street", "outdoors"), ("day", "golden", "dusk", "night", "interior")
PROPS = {"desk", "table", "chair", "door", "window", "frame", "shelf", "lamp", "bed", "rug", "crate", "barrel", "cabinet",
         "counter", "fireplace", "house", "shopfront", "tree", "rock", "fence", "lamppost"}
EFFECTS = {"rings", "dust", "shafts", "burst", "shake", "rain", "snow"}
MOVES = {"cut", "whip", "push"}
NAME = re.compile(r"^[a-z][a-z0-9_]{0,19}$")
COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
DRAW = re.compile(r"export\s+default\s+function\s+draw\s*\(\s*k\s*,\s*f\s*\)")


def available() -> str | None:
    """Why a 3D opener can't be made on this PC, or None."""
    return drawn_opener.available() or (
        None if shutil.which("npx") and (REMOTION / "node_modules" / "@remotion" / "three").exists()
        else r"the 3D library isn't installed (run: cd remotion && npm install)")


def word_time(words: list, w, fallback: float) -> float:
    """A time given as seconds or as a spoken word (its start; the same rule as the kit's k.word)."""
    if isinstance(w, (int, float)) and not isinstance(w, bool):
        return float(w)
    want = re.sub(r"[^a-z0-9']", "", str(w).lower())
    hit = next((s for s, _, txt in words if want and re.sub(r"[^a-z0-9']", "", str(txt).lower()).startswith(want)), None)
    return float(hit) if hit is not None else fallback


def num(v, lo: float, hi: float, default: float) -> float:
    return min(hi, max(lo, float(v))) if isinstance(v, (int, float)) and not isinstance(v, bool) else default


def xz(v, default=(0.0, -1.5)) -> list[float]:
    return [num(v[0], -40, 40, default[0]), num(v[1], -60, 10, default[1])] if isinstance(v, list) and len(v) == 2 else list(default)


def lint_cutout(code: str) -> list[str]:
    """Rule breaks in an AI-written cut-out module (the drawn opener's code rules, with draw(k, f))."""
    found = [p for p in drawn_opener.lint(code) if "export default function scene" not in p]
    if not DRAW.search(code):
        found.append("missing `export default function draw(k, f)`")
    return found


def clean(raw, words: list, seconds: float) -> tuple[dict | None, list[str]]:
    """The AI's stage, checked and made safe for Remotion (word times resolved, numbers clamped), and what was wrong
    with it. A stage with problems goes back to the coder."""
    if not isinstance(raw, dict):
        return None, ["the reply was not a JSON object"]
    bad: list[str] = []
    place = raw.get("place") if raw.get("place") in PLACES else "room"
    mood = raw.get("mood") if raw.get("mood") in MOODS else "interior"
    colors = {k: v for k, v in (raw.get("colors") or {}).items() if k in ("wall", "floor", "ground", "sky", "trim")
              and isinstance(v, str) and COLOR.match(v)} if isinstance(raw.get("colors"), dict) else {}
    props = []
    for p in raw.get("props") or []:
        if not isinstance(p, dict) or p.get("type") not in PROPS:
            bad.append(f"unknown prop {p.get('type') if isinstance(p, dict) else p!r}: use only the listed props")
            continue
        q = {"type": p["type"], "at": xz(p.get("at")), "turn": num(p.get("turn"), -360, 360, 0), "size": num(p.get("size"), 0.2, 4, 1)}
        for k in ("wall", "lit"):
            if isinstance(p.get(k), bool):
                q[k] = p[k]
        if q.get("wall"):
            q["at"] = [num((p.get("at") or [0, 2])[0], -3.8, 3.8, 0), num((p.get("at") or [0, 2])[1], 0.3, 4.2, 2)]
        for k, lo, hi in (("y", 0, 4), ("open", 0, 1), ("length", 0.5, 20)):
            if k in p:
                q[k] = num(p[k], lo, hi, 0)
        if isinstance(p.get("color"), str) and COLOR.match(p["color"]):
            q["color"] = p["color"]
        if isinstance(p.get("id"), str) and NAME.match(p["id"]):
            q["id"] = p["id"]
        props.append(q)
    cutouts, names = [], set()
    for c in raw.get("cutouts") or []:
        if not isinstance(c, dict) or not isinstance(c.get("name"), str) or not NAME.match(c["name"]) or c["name"] in names:
            bad.append("each cut-out needs a unique lowercase `name` (letters, digits, _)")
            continue
        code = drawn_opener.clean_code(c.get("code"))
        problems = lint_cutout(code) if code else ["no code"]
        if problems:
            bad += [f"cut-out {c['name']}: {p}" for p in problems]
            continue
        w, h = int(num(c.get("w"), 100, 1400, 700)), int(num(c.get("h"), 100, 1400, 1100))
        q = {"name": c["name"], "w": w, "h": h, "aspect": w / h, "frames": int(num(c.get("frames"), 1, 4, 1)),
             "height": num(c.get("height"), 0.1, 6, 1.75), "at": xz(c.get("at")), "y": num(c.get("y"), 0, 4, 0),
             "flip": c.get("flip") is True, "wall": c.get("wall") is True, "fps": num(c.get("fps"), 2, 12, 7), "code": code}
        if q["wall"]:
            q["at"] = [num((c.get("at") or [0, 2])[0], -3.8, 3.8, 0), num((c.get("at") or [0, 2])[1], 0.3, 4.2, 2)]
        if isinstance(c.get("talk"), list) and len(c["talk"]) == 2:
            q["talk"] = [word_time(words, c["talk"][0], 0), word_time(words, c["talk"][1], seconds)]
        if isinstance(c.get("path"), list):
            q["path"] = sorted([[word_time(words, k[0], 0), num(k[1], -40, 40, 0), num(k[2], -60, 10, -1.5)]
                                for k in c["path"] if isinstance(k, list) and len(k) == 3])
        names.add(c["name"])
        cutouts.append(q)
    if not cutouts:
        bad.append("no usable cut-out: the subject must be a drawn cut-out")
    ids = names | {p["id"] for p in props if p.get("id")}
    shots = []
    for sh in raw.get("shots") or []:
        tg = sh.get("target") if isinstance(sh, dict) else None
        names = tg if isinstance(tg, list) else [tg]  # a list frames them all
        if not names or len(names) > 4 or any(not isinstance(n, str) or n not in ids for n in names):
            bad.append(f"a shot aims at {tg!r}: use cut-out names or prop ids (a list of up to 4 frames them all)")
            continue
        shots.append({"at": num(word_time(words, sh.get("at", 0), 0), 0, seconds, 0), "target": tg,
                      "distance": num(sh.get("distance"), 0.6, 14, 3.5), "height": num(sh.get("height"), -3, 6, 0),
                      "turn": num(sh.get("turn"), -170, 170, 0), "fov": num(sh.get("fov"), 28, 72, 50),
                      "move": sh.get("move") if sh.get("move") in MOVES else "cut"})
    shots.sort(key=lambda s: s["at"])
    if not shots:
        bad.append("no usable shot")
    effects = [{"type": e["type"], "at": word_time(words, e.get("at", 0), 0), **({"on": e["on"]} if e.get("on") in ids else {})}
               for e in raw.get("effects") or [] if isinstance(e, dict) and e.get("type") in EFFECTS]
    stage = {"moment": str(raw.get("moment") or "the strangest moment").strip()[:200], "place": place, "mood": mood,
             "colors": colors, "props": props[:24], "cutouts": cutouts[:6], "shots": shots[:5], "effects": effects[:8]}
    return stage, bad


def write(short: dict, words: list, seconds: float, old: dict | None = None, problems: list[str] | None = None,
          sheet: Path | None = None):
    """The coder's stage (raw JSON from the AI); with `old` and `problems`, the fix of the last draft. Problems with no
    draft yet (a final review's spoiler finding sent the opener back) are things the first draft must avoid."""
    fix = ("\nThe last opener was sent back. Avoid this in yours:\n- " + "\n- ".join(problems) + "\n") if problems and not old else ""
    if old:
        fix = ("\nYour last draft (below) had these problems:\n- " + "\n- ".join(problems or []) +
               (f"\nIts preview: open {sheet} (6 frames left to right, times on each)." if sheet else "") +
               f"\nRewrite it to fix every one of them. Last draft:\n{json.dumps(old, ensure_ascii=False)}\n")
    return llm.ask_ai(f"""{drawn_opener.opener_role(short, words, seconds)}
Stage it in 3D with the stage manual below; draw its cut-outs with the drawing kit after it (for cut-outs use only
its people, animals, props and shapes: the 3D set does the backgrounds, camera, light and depth).
{STAGE.read_text(encoding="utf-8")}
--- The drawing kit (for the cut-outs' code) ---
{(drawn_opener.DRAWN / "KIT.md").read_text(encoding="utf-8")}{fix}
Reply with ONLY the stage JSON.""", fatal=False, read_dir=sheet.parent if sheet else None)


def render(stage: dict, seconds: float, folder: Path) -> str | None:
    """Paints the cut-outs and renders folder/opener.mp4; None when it worked, else what went wrong."""
    for c in stage["cutouts"]:
        (folder / f"cut_{c['name']}.mjs").write_text(c["code"], encoding="utf-8")
    job = {"out": str(folder / "cutouts"), "cutouts": [{**{k: c[k] for k in ("name", "w", "h", "frames")},
                                                         "module": str(folder / f"cut_{c['name']}.mjs")} for c in stage["cutouts"]]}
    (folder / "cutouts.json").write_text(json.dumps(job), encoding="utf-8")
    try:  # the cut-outs' code was written by the AI: same locked-down node as the drawn opener
        r = subprocess.run(["node", "--disallow-code-generation-from-strings", str(drawn_opener.DRAWN / "cutouts.mjs"),
                            str(folder / "cutouts.json")], cwd=drawn_opener.DRAWN, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
    except subprocess.TimeoutExpired:
        return "painting the cut-outs took too long"
    if r.returncode:
        return "a cut-out crashed when it ran: " + " | ".join(line.strip() for line in (r.stderr or r.stdout).splitlines()
                                                              if line.strip() and "node:internal" not in line)[:500]
    shutil.rmtree(PUBLIC, ignore_errors=True)
    shutil.copytree(folder / "cutouts", PUBLIC)
    props = {"fps": FPS, "seconds": seconds, "dir": "opener3d/job", **{k: v for k, v in stage.items() if k != "moment"},
             "cutouts": [{k: v for k, v in c.items() if k not in ("code", "w", "h")} for c in stage["cutouts"]]}
    (folder / "props.json").write_text(json.dumps(props), encoding="utf-8")
    try:
        r = subprocess.run([shutil.which("npx") or "npx", "remotion", "render", "src/index.ts", "Opener3D", str(folder / "opener.mp4"),
                            f"--props={folder / 'props.json'}", "--log=error", "--gl=angle", "--concurrency=4"],
                           cwd=REMOTION, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"the 3D render took longer than {TIMEOUT} s"
    finally:
        shutil.rmtree(PUBLIC, ignore_errors=True)
    if r.returncode or not (folder / "opener.mp4").exists():
        return "the 3D render failed: " + (r.stderr or r.stdout or "no message").strip()[-500:]
    return None


def sheet(clip: Path, seconds: float, out: Path) -> Path:
    """Six frames of the clip side by side, the time on each (the art director's preview)."""
    tiles = []
    for k, t in enumerate(drawn_opener.sheet_times(seconds)):
        media_tools.ffmpeg("-y", "-ss", f"{t:.2f}", "-i", str(clip), "-frames:v", "1", "-vf", "scale=324:576", f"f{k}.png", cwd=out.parent)
        im = Image.open(out.parent / f"f{k}.png").convert("RGB")
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 86, 26), fill=(0, 0, 0))
        d.text((6, 6), f"{t:.2f}s", fill="white")
        tiles.append(im)
    S = Image.new("RGB", (324 * len(tiles), 576))
    for k, im in enumerate(tiles):
        S.paste(im, (324 * k, 0))
    S.save(out)
    return out


def plan(short: dict, words: list, seconds: float, folder: Path, repair: str | None = None) -> tuple[dict | None, str | None]:
    """Draft, render, review, fix (up to drawn_opener.FIXES times). Returns (the passed stage, marked "kind": "3d",
    whose clip is folder/opener.mp4) or (None, why it failed). `seconds` already includes the crossfade."""
    folder.mkdir(parents=True, exist_ok=True)
    print("  staging the opener in 3D: drawn cut-outs in a lit set...")
    old, problems, preview, score = None, ([repair] if repair else []), None, 0.0
    for attempt in range(drawn_opener.FIXES + 1):
        raw = write(short, words, seconds, old, problems, preview)
        stage, problems = clean(raw, words, seconds)
        if stage:  # an animal the moment names must be the kit's own part, as in the drawn opener
            problems += drawn_opener.missing_parts({"moment": stage["moment"], "code": "\n".join(c["code"] for c in stage["cutouts"])},
                                                   short["scenes"][0]["narration"])
        old, preview, score = raw if isinstance(raw, dict) else old, None, 0.0
        if stage and not problems:
            err = render(stage, seconds, folder)
            if err:
                problems = [err]
            else:
                preview = sheet(folder / "opener.mp4", seconds, folder / f"sheet3d{attempt + 1}.png")
                score, problems = drawn_opener.review(short, {"moment": stage["moment"]}, preview, seconds)
                if score is None:
                    score, stage["unreviewed"] = drawn_opener.PASS, True
        if score >= drawn_opener.PASS:
            return {**stage, "kind": "3d"}, None
        print(f"    3D opener draft {attempt + 1} ({score:g}/10): " + "; ".join(problems)[:300])
    return None, f"the 3D opener's last draft scored {score:g}/10 after {drawn_opener.FIXES} fixes: {'; '.join(problems)[:300]}"
