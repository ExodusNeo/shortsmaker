"""Drawn openers (owner, 2026-10-30): scene 1 of an `opener: animated` Short as a hand-drawn brush-ink + watercolour
animation of the strangest moment, coded by the AI against the kit in drawn/ (KIT.md is its manual; claude-animation,
MIT, vendored in drawn/lib). The coder writes the scene, a preview sheet is rendered, the AI looks at it as an art
director and the coder fixes what it found, up to FIXES times; then the clip is rendered. Anything that fails returns
(None, why): the motion-graphic opener plays instead (short_render.use_opener). The owner approved the look on the
Dexter test (test_renders/drawn_opener_dexter)."""

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from shortsmaker import llm, plan_rules, session
from shortsmaker.config import FPS, ROOT, XFADE

DRAWN = ROOT / "drawn"
FIXES = 2  # look-and-fix rounds after the first draft (owner: a few fixes, then the next opener in line)
# The art director's score (1-10) a draft needs. A list of flaws alone never passed: on the first live runs
# (2026-10-31) it found some in every draft, good ones included, and all 6 Shorts fell back to the motion graphic.
PASS = 7
TIMEOUT = 600  # one node run (a 4 s render takes ~20 s)
# The scene runs as code on this PC and its writer has read Wikipedia text: only kit calls and plain JavaScript.
# node also runs with --disallow-code-generation-from-strings (no eval / Function at run time).
FORBIDDEN = re.compile(r"\b(import|require|process|fs|fetch|eval|Function|globalThis|global|this|Date|Buffer|"
                       r"constructor|prototype|__proto__|child_process|XMLHttpRequest|WebAssembly|Reflect|Proxy)\b"
                       r"|Math\.random|\.(ctx|pen)\b")
# comments and plain '...' / "..." strings can't run: they are left out of the check (template literals stay in)
INERT = re.compile(r"""//[^\n]*|/\*.*?\*/|"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'""", re.S)
DEFAULT_RULES = """Animate the story's strangest moment, the one the hook line describes, as one clear picture that
moves: a stranger scrolling past must understand what is strange from the first frame, before any word is heard.
Real facts only: the people, things, place and era of the story (period clothes and hats; nothing modern in an old
story). No gore, no blood, no weapons hurting anyone; a death is shown by what is left behind, never the act.
Faces stay simple (the kit's dot eyes). At most 3 people, unless a crowd IS the strange thing."""


def available() -> str | None:
    """Why a drawn opener can't be made on this PC, or None."""
    if not shutil.which("node"):
        return "node is not installed"
    if not (DRAWN / "node_modules" / "@napi-rs" / "canvas").exists():
        return r"the drawing library isn't installed (run: cd drawn && npm install)"
    return None


def lint(code: str) -> list[str]:
    """Rule breaks in an AI-written scene (KIT.md's code rules). Empty = clean."""
    live = INERT.sub('""', code)
    found = [f"uses `{w}`: only k.* calls, Math and plain JavaScript are allowed"
             for w in dict.fromkeys(m.group(0) for m in FORBIDDEN.finditer(live))]
    if not re.search(r"export\s+default\s+function\s+scene\s*\(\s*k\s*,\s*t\s*\)", code):
        found.append("missing `export default function scene(k, t)`")
    if len(code) > 20000:
        found.append("the scene is too long: draw fewer, bigger things")
    return found


def clean_code(raw) -> str | None:
    """The scene module from an AI reply (fences stripped), or None."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    fence = re.search(r"```(?:js|javascript|mjs)?\s*\n(.*?)```", raw, re.S)
    return (fence.group(1) if fence else raw).strip() + "\n"


def node_run(job: dict, folder: Path) -> str | None:
    """Runs drawn/run.mjs on one job; None when it worked, else what went wrong (trimmed)."""
    (folder / "job.json").write_text(json.dumps(job), encoding="utf-8")
    for attempt in range(2):  # a crash with no message once came and went (two runs at once): tried once more
        try:
            r = subprocess.run(["node", "--disallow-code-generation-from-strings", str(DRAWN / "run.mjs"), str(folder / "job.json")],
                               cwd=DRAWN, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            return f"it took longer than {TIMEOUT} s"
        if r.returncode == 0:
            return None
        err = [line.strip() for line in (r.stderr or r.stdout).splitlines()
               if line.strip() and "node:internal" not in line and not set(line.strip()) <= {"^", "~"}]
        if err:
            headline = next((line for line in err if re.match(r"(?:\w*Error|Error):", line)), None)
            return " | ".join(([headline] if headline else []) + [line for line in err if line != headline])[:600]
    return f"node stopped with exit code {r.returncode} and no message"


def sheet_times(seconds: float) -> list[float]:
    """Six frames across the opener for the preview, the first and the last included."""
    return [round(seconds * k / 5 - (0.05 if k == 5 else 0), 2) for k in range(6)]


def write(short: dict, words: list, seconds: float, old: dict | None = None, problems: list[str] | None = None,
          sheet: Path | None = None) -> dict | None:
    """The coder's scene: {"moment": what it shows, "code": the module}; with `old` and `problems`, the fix of the
    last draft (it may look at that draft's preview `sheet`). None when the reply is unusable."""
    scenes = short["scenes"]
    timing = ", ".join(f"{w} {s:.2f}s" for s, _, w in words) or "not known"
    fix = ""
    if old:
        fix = (f"\nYour last draft (below) had these problems:\n- " + "\n- ".join(problems or []) +
               (f"\nIts preview: open {sheet} (6 frames left to right, times on each)." if sheet else "") +
               f"\nRewrite it to fix every one of them. Last draft:\n{old['code']}\n")
    data = llm.ask_ai(f"""You animate the opener of a YouTube Short: "{short['title']}" (story: {short.get('topic') or short['title']}).
Scene 1 is the hook. Its voice plays over your animation: "{scenes[0]['narration']}"
It lasts {seconds:.2f} s; each spoken word starts at: {timing}.
The rest of the story, for context only (don't show it): {json.dumps([sc['narration'] for sc in scenes[1:]], ensure_ascii=False)}
Main character: {short.get('character') or 'not named'}.
{session.RULES.get("Opener") or DEFAULT_RULES}
Write the scene with the kit below.
{(DRAWN / "KIT.md").read_text(encoding="utf-8")}{fix}
Reply with ONLY JSON: {{"moment": "one sentence: what the animation shows", "code": "export const camera = ...\\nexport default function scene(k, t) {{ ... }}"}}""",
                      fatal=False, read_dir=sheet.parent if sheet else None)
    code = clean_code((data or {}).get("code")) if isinstance(data, dict) else None
    if not code:
        return None
    return {"moment": str(data.get("moment") or "the strangest moment").strip()[:200], "code": code}


def review(short: dict, plan: dict, sheet: Path, seconds: float) -> tuple[float | None, list[str]]:
    """The art director's score (1-10) of a draft's preview sheet and what to fix. None = no verdict (a failed call):
    make_opener keeps the draft and the final check says it was never judged."""
    data = llm.ask_ai(f"""You are the art director of a YouTube Short: "{short['title']}". Open {sheet}: six frames of its
hand-drawn opener across {seconds:.1f} s, left to right (the time is on each). The voice over it says:
"{short['scenes'][0]['narration']}". The animator meant it to show: {plan['moment']}.
A stranger scrolling the Shorts feed sees the first frame for one second. Look for these problems:
- frame 0 doesn't already show the subject and what is strange about it, or you can't tell what is happening;
- the main thing is too small to read on a phone, or crowded out by background;
- something doesn't look like what it should be (name it), or looks wrong for the story's era or place;
- things float, sink into each other or overlap wrongly (a person inside a wall, a held thing away from the hand);
- the picture doesn't fill the vertical frame (a big empty band, the main things drawn small in one part of it),
  or something important is cut off by the frame edge;
- a face or a word sits behind the title band (y 74-170, first 1.8 s) or the captions (y 1170-1300); bodies,
  limbs and props crossing those bands are fine;
- text is misspelled, unreadable or not something the story says;
- nothing moves, or the moving parts glitch or jump between frames;
- gore, blood or a weapon hurting someone.
The hand-drawn cartoon look itself (dot eyes, stick limbs, brush lines, watercolour) is intended: don't report it.
Score it 1-10: would that stranger understand the strange moment at a glance and stop scrolling? {PASS} = good
enough to post: small flaws are fine. Below {PASS}, list the problems that stop it working, the worst first.
Reply with ONLY JSON: {{"score": 7, "problems": ["...", "..."]}}""", fatal=False, read_dir=sheet.parent)
    score = data.get("score") if isinstance(data, dict) else None
    if not plan_rules.is_num(score) or not 1 <= score <= 10:
        return None, []
    found = [str(p).strip()[:240] for p in data.get("problems") or [] if str(p).strip()]
    return float(score), found[:8] or ([] if score >= PASS else ["the art director gave a low score without saying why"])


def fingerprint(code: str, seconds: float) -> str:
    kit = "".join((DRAWN / f).read_text(encoding="utf-8") for f in ("kit.mjs", "run.mjs"))
    return hashlib.sha1(f"{code}|{seconds:.3f}|{kit}".encode()).hexdigest()


def make_opener(short: dict, words: list, seconds: float, work: Path) -> tuple[Path | None, str | None]:
    """Scene 1's drawn opener clip (work/drawn/opener.mp4, scene 1 + the crossfade long), or (None, why). The plan
    is kept in short["drawn"] (state.json), so fix rounds and fix.bat reuse the clip; a failure is kept in
    short["drawn_failed"] and never retried for this Short."""
    if short.get("drawn_failed"):
        return None, short["drawn_failed"]
    why = available()
    if why:
        return None, why
    folder = work / "drawn"
    folder.mkdir(parents=True, exist_ok=True)
    seconds = round((seconds + XFADE) * FPS) / FPS
    scene, clip, done = folder / "scene.mjs", folder / "opener.mp4", folder / "done.txt"
    plan = short.get("drawn")
    base = {"scene": str(scene), "seconds": seconds, "words": words, "out": str(folder), "name": "opener"}

    def fail(why: str) -> tuple[None, str]:
        short["drawn_failed"] = why
        return None, why

    if not plan:
        print("  drawing the opener: the strangest moment as a hand-drawn animation...")
        problems, sheet, score = [], None, 0.0
        for attempt in range(FIXES + 1):
            draft = write(short, words, seconds, plan, problems, sheet)
            if not draft:
                if plan is None:
                    return fail("the AI wrote no usable scene")
                break  # keep the last draft's problems
            plan, sheet, score = draft, None, 0.0
            problems = lint(plan["code"])
            if not problems:
                scene.write_text(plan["code"], encoding="utf-8")
                err = node_run({**base, "mode": "sheet", "times": sheet_times(seconds), "scale": 0.3}, folder)
                if err:
                    problems = [f"the scene crashed when it ran: {err}"]
                else:
                    sheet = folder / f"sheet{attempt + 1}.png"
                    (folder / "sheet.png").replace(sheet)
                    score, problems = review(short, plan, sheet, seconds)
                    if score is None:  # no verdict: kept as it is, flagged (audit 2026-10-31: it used to pass silently)
                        score, plan["unreviewed"] = PASS, True
            if score >= PASS:
                break
            print(f"    opener draft {attempt + 1} ({score:g}/10): " + "; ".join(problems)[:300])
        if score < PASS:
            return fail(f"the drawn opener's last draft scored {score:g}/10 after {FIXES} fixes: "
                        f"{'; '.join(problems)[:300]}")
        short["drawn"] = plan
    scene.write_text(plan["code"], encoding="utf-8")
    mark = fingerprint(plan["code"], seconds)
    if clip.exists() and done.exists() and done.read_text(encoding="utf-8") == mark:
        return clip, None
    err = node_run({**base, "mode": "render"}, folder)
    if err or not clip.exists():
        return fail(f"the drawn opener didn't render: {err or 'no clip came out'}")
    done.write_text(mark, encoding="utf-8")
    return clip, None
