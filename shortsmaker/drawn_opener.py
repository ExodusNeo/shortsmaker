"""Drawn openers (owner, 2026-10-30): scene 1 of an `opener: animated` Short as a hand-drawn brush-ink + watercolour
animation of the strangest moment, coded by the AI against the kit in drawn/ (KIT.md is its manual; claude-animation,
MIT, vendored in drawn/lib). The coder writes the scene, a preview sheet is rendered, the AI looks at it as an art
director and the coder fixes what it found, up to FIXES times; then the clip is rendered. Anything that fails returns
(None, why): the motion-graphic opener plays instead (short_render.use_opener). The owner approved the look on the
Dexter test (test_renders/drawn_opener_dexter). Since 2026-11-03 the same machinery can draw the reveal (scene i > 0,
PAYOFF_RULES) in place of a custom diagram (short_render.drawn_payoff): Clever Hans's reveal was two small outlines."""

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from shortsmaker import llm, opening_rules, plan_rules, session
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
PAYOFF_RULES = """This scene is the REVEAL: show the answer the whole Short has been building to, exactly as its narration
says it, happening in front of the viewer. One big clear subject doing the one change the reveal is about (the
questioner's shoulders dropping as the hoof stops; the trap springing shut), on its spoken word, then held so it
lands. The viewer has heard the story so far: no need to set it up again. Real facts only, the story's era; no gore.
Faces stay simple (the kit's dot eyes). At most 3 people."""


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


# The kit's animals and the words that name them. The Clever Hans opener (2026-11-03) built its horse from boxes
# instead of k.horse, and the art director passed it at 7/10.
KIT_ANIMALS = {"horse": ("horse", "stallion", "mare", "pony", "colt"), "dog": ("dog", "hound", "puppy"),
               "chicken": ("chicken", "hen", "rooster", "cockerel"), "cow": ("cow", "bull", "ox", "cattle"),
               "pig": ("pig", "hog", "sow", "boar"), "cat": ("cat", "kitten", "tomcat"),
               "rabbit": ("rabbit", "rabbits", "bunny", "hare"), "bear": ("bear", "bears", "cub")}


# Story objects: words in the moment/narration that need a kit part on screen. The 3D McLean opener (2026-11-05)
# showed a messenger with nothing in his hands, knocking on an open door; the owner caught both.
KIT_OBJECTS = {"letter": ("letter", "telegram", "envelope", "messenger", "courier", "postman", "mailman",
                          "dispatch"),
               "door": ("knock", "knocks", "knocked", "knocking"),  # a knock needs its door; a house already has one
               "phone": ("phone", "telephone", "telephoned"), "radio": ("radio", "wireless")}
KNOCK = {"knock", "knocks", "knocked", "knocking"}
OPEN_DOOR = re.compile(r"k\.door\([^;]*?\bopen\s*:\s*(0?\.\d+|1(?:\.0+)?)")


def missing_parts(plan: dict, narration: str = "", props: set[str] = frozenset(), open_doors: list[float] = ()) -> list[str]:
    """Animals and story objects the planned moment or the opener's narration names that the code doesn't draw with
    the kit's own part (the Clever Hans plan said only "Clever Hans taps a hoof"; its narration said "this horse"),
    plus a knock on an open door. `props` / `open_doors`: a 3D stage's prop types and its 3D doors' `open` values."""
    said = set(re.findall(r"[a-z]+", f"{plan.get('moment') or ''} {narration}".lower()))
    live = INERT.sub('""', plan.get("code") or "")
    found = [f"the moment shows a {part} but the code never calls k.{part}(...): draw it with the kit's part "
             f"(KIT.md, Animals), never from your own shapes" for part, names in KIT_ANIMALS.items()
             if said & set(names) and f"k.{part}(" not in live]
    found += [f"the story needs a {part} on screen ({', '.join(sorted(said & set(names)))}) but nothing draws one: "
              f"call k.{part}(...) (held in the hand the kit returns{', or a 3D door prop' if part == 'door' else ''})"
              for part, names in KIT_OBJECTS.items() if said & set(names) and f"k.{part}(" not in live and part not in props
              and not (part == "door" and "k.knock(" in live)
              and not re.search(rf"""hold\s*:\s*\[[^\]]*['"]{part}['"]""", plan.get("code") or "")]
    if said & KNOCK and (any(float(v) > .15 for v in OPEN_DOOR.findall(live)) or any(v > .15 for v in open_doors)):
        found.append("someone knocks on an OPEN door: a knock needs a closed door (open: 0), the knocker on one side "
                     "and the person answering on the other")
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


def opener_role(short: dict, words: list, seconds: float) -> str:
    """The opener brief both opener coders get (this drawn one and opener3d): the hook, its timing, the rules."""
    scenes = short["scenes"]
    timing = ", ".join(f"{w} {s:.2f}s" for s, _, w in words) or "not known"
    return f"""You animate the opener of a YouTube Short: "{short['title']}" (story: {short.get('topic') or short['title']}).
Scene 1 is the hook. Its voice plays over your animation: "{scenes[0]['narration']}"
It lasts {seconds:.2f} s; each spoken word starts at: {timing}.
The rest of the story, for context only (don't show it): {json.dumps([sc['narration'] for sc in scenes[1:]], ensure_ascii=False)}
Main character: {short.get('character') or 'not named'}.
{session.RULES.get("Opener") or DEFAULT_RULES}
{opening_rules.opening_brief(short)}"""


def write(short: dict, words: list, seconds: float, old: dict | None = None, problems: list[str] | None = None,
          sheet: Path | None = None, i: int = 0) -> dict | None:
    """The coder's scene: {"moment": what it shows, "code": the module}; with `old` and `problems`, the fix of the
    last draft (it may look at that draft's preview `sheet`). `i` > 0 draws that scene as the reveal. None when the
    reply is unusable."""
    scenes = short["scenes"]
    timing = ", ".join(f"{w} {s:.2f}s" for s, _, w in words) or "not known"
    fix = ""
    if old:
        fix = (f"\nYour last draft (below) had these problems:\n- " + "\n- ".join(problems or []) +
               (f"\nIts preview: open {sheet} (6 frames left to right, times on each)." if sheet else "") +
               f"\nRewrite it to fix every one of them. Last draft:\n{old['code']}\n")
    if i == 0:
        role = opener_role(short, words, seconds)
    else:
        look = f" ({short['character_look']})" if short.get("character_look") else ""
        role = f"""You animate scene {i + 1} of a YouTube Short: "{short['title']}" (story: {short.get('topic') or short['title']}).
Its voice plays over your animation: "{scenes[i]['narration']}"
It lasts {seconds:.2f} s; each spoken word starts at: {timing}.
The story the viewer has heard so far: {json.dumps([sc['narration'] for sc in scenes[:i]], ensure_ascii=False)}
After this scene: {json.dumps([sc['narration'] for sc in scenes[i + 1:]], ensure_ascii=False)}
Main character: {short.get('character') or 'not named'}{look}.
{PAYOFF_RULES}"""
    data = llm.ask_ai(f"""{role}
Write the scene with the kit below.
{(DRAWN / "KIT.md").read_text(encoding="utf-8")}{fix}
Reply with ONLY JSON: {{"moment": "one sentence: what the animation shows", "code": "export const camera = ...\\nexport default function scene(k, t) {{ ... }}"}}""",
                      fatal=False, read_dir=sheet.parent if sheet else None)
    code = clean_code((data or {}).get("code")) if isinstance(data, dict) else None
    if not code:
        return None
    return {"moment": str(data.get("moment") or "the strangest moment").strip()[:200], "code": code}


def review(short: dict, plan: dict, sheet: Path, seconds: float, i: int = 0) -> tuple[float | None, list[str]]:
    """The art director's score (1-10) of a draft's preview sheet and what to fix. None = no verdict (a failed call):
    make_opener keeps the draft and the final check says it was never judged. `i` > 0: the scene is the reveal."""
    opener = i == 0
    what = "animated opener" if opener else f"hand-drawn reveal (scene {i + 1}, near the end)"
    if opener:
        first = ("A stranger scrolling the Shorts feed sees the first frame for one second. Look for these problems:\n"
                 "- frame 0 doesn't already show the subject and what is strange about it, or you can't tell what is happening;")
        answer = "\n- an answer object or any visible label/sign gives away the ending before the narrator reveals it;"
        verdict = f"""Score it 1-10: would that stranger understand the strange moment at a glance and stop scrolling? {PASS} = good
enough to post: small flaws are fine. Below {PASS}, list the problems that stop it working, the worst first.
Also return reveals_answer=true if any frame identifies the withheld answer; give the exact visible object/text
in answer_why. An opening that reveals the answer cannot pass, even if the drawing and animation look excellent."""
    else:
        first = ("The viewer has heard the story up to here and waits for the answer. Look for these problems:\n"
                 "- the reveal's change isn't big and unmistakable on a phone (a subtle shift, a tiny figure), or it "
                 "happens off its spoken word, or you can't tell what is happening;")
        answer = ""
        verdict = f"""Score it 1-10: does the viewer SEE the answer happen, at a glance, on a phone? {PASS} = good enough to post:
small flaws are fine. Below {PASS}, list the problems that stop it working, the worst first. reveals_answer is false here."""
    data = llm.ask_ai(f"""You are the art director of a YouTube Short: "{short['title']}". Open {sheet}: six frames of its
{what} across {seconds:.1f} s, left to right (the time is on each). The voice over it says:
"{short['scenes'][i]['narration']}". The animator meant it to show: {plan['moment']}.
{opening_rules.opening_brief(short) if opener else ""}
{first}
- the main thing is too small to read on a phone, or crowded out by background; or one wide shot stays the whole
  time with the subject small (the camera should cut close to the strange detail on its word);
- a label, sign, speech bubble or caption-like word in the picture names or explains a thing ("WOODEN EAGLE",
  "GROCER", "BORROW ROOM?"): the picture must explain itself; this is never a small flaw;
- something doesn't look like what it should be (name it), or looks wrong for the story's era or place; an
  animal or person assembled from plain boxes and blocks counts (a horse must read as a horse at a glance);
- things float, sink into each other or overlap wrongly (a person inside a wall, a held thing away from the hand):
  a hand, arm or body passing through a door, wall or another person is never a small flaw (the McLean messenger's
  fist went through the door it knocked on); nor is a beard, prop or label covering a face like a mask, or people
  inside and outside a building with no wall between them;
- an action that makes no physical sense or misses the thing the story needs: knocking on an open door or on air,
  a messenger or delivery with nothing in hand, someone answering a door that isn't there, a rider with no horse.
  Name what is missing or wrong; this is never a small flaw;
- the subject blends into what is behind it (a brown coat on a brown wall, a dark figure in a dark room): it must
  stand out by colour and brightness;
- circles, rings or bursts lying over the picture like an on-screen overlay, covering faces;
- the picture doesn't fill the vertical frame (a big empty band, the main things drawn small in one part of it),
  or something important is cut off by the frame edge;
- a face sits behind the captions (y 1170-1300) in any frame; bodies, limbs and props crossing that band are fine;
- text is misspelled, unreadable or not something the story says;{answer}
- nothing moves, or the moving parts glitch or jump between frames (a 3D opener's people cycle 2-6 drawings several
  times a second: a pose that differs between frames IS moving; call it frozen only when frames are identical);
- gore, blood or a weapon hurting someone.
The hand-drawn cartoon look itself (dot eyes, stick limbs, brush lines, watercolour; or flat drawn cut-outs standing
in a simple 3D set), a soft hazy background, the light grade and the motion blur of a fast camera swing are
intended: don't report them.
{verdict}
Reply with ONLY JSON: {{"score": 7, "reveals_answer": false, "answer_why": "", "problems": ["...", "..."]}}""", fatal=False, read_dir=sheet.parent)
    score = data.get("score") if isinstance(data, dict) else None
    if not plan_rules.is_num(score) or not 1 <= score <= 10:
        return None, []
    found = [str(p).strip()[:240] for p in data.get("problems") or [] if str(p).strip()]
    if opener and data.get("reveals_answer") is True:
        score = min(score, PASS - 1)
        found.insert(0, "Opening reveals the answer: " + str(data.get("answer_why") or "withhold the ending's answer object and labels")[:200])
    return float(score), found[:8] or ([] if score >= PASS else ["the art director gave a low score without saying why"])


def fingerprint(code: str, seconds: float, three: bool = False) -> str:
    """Changes when the plan or the code that renders it changes (a 3D plan also depends on its stage and cut-outs)."""
    files = [DRAWN / "kit.mjs"] + ([DRAWN / "cutouts.mjs", ROOT / "remotion" / "src" / "Opener3D.tsx"] if three else [DRAWN / "run.mjs"])
    kit = "".join(f.read_text(encoding="utf-8") for f in files)
    return hashlib.sha1(f"{code}|{seconds:.3f}|{kit}".encode()).hexdigest()


def make_opener(short: dict, words: list, seconds: float, work: Path, i: int = 0) -> tuple[Path | None, str | None]:
    """Scene 1's opener clip (work/drawn/opener.mp4, scene 1 + the crossfade long), or (None, why): a 3D opener
    (opener3d, owner 2026-11-05) when one passes its review, else the hand-drawn one. The plan
    is kept in short["drawn"] (state.json), so fix rounds and fix.bat reuse the clip; a failure is kept in
    short["drawn_failed"] and never retried for this Short. `i` > 0 draws that scene as the reveal instead
    (work/drawn_{i}/, short["drawn_{i}"], short["drawn_failed_{i}"]); `words` are timed from that scene's start."""
    key, failed = ("drawn", "drawn_failed") if i == 0 else (f"drawn_{i}", f"drawn_failed_{i}")
    if short.get(failed):
        return None, short[failed]
    why = available()
    if why:
        return None, why
    folder = work / ("drawn" if i == 0 else f"drawn_{i}")
    folder.mkdir(parents=True, exist_ok=True)
    seconds = round((seconds + XFADE) * FPS) / FPS
    scene, clip, done = folder / "scene.mjs", folder / "opener.mp4", folder / "done.txt"
    plan = short.get(key)
    base = {"scene": str(scene), "seconds": seconds, "words": words, "out": str(folder), "name": "opener"}

    def fail(why: str) -> tuple[None, str]:
        short[failed] = why
        return None, why

    name = "opener" if i == 0 else "reveal"
    repair = short.pop("drawn_repair", None) if i == 0 else None
    if (not plan or repair) and i == 0:
        from shortsmaker import opener3d  # it uses this module's review and coder brief
        why3d = opener3d.available()
        made, why3d = opener3d.plan(short, words, seconds, folder, repair) if not why3d else (None, why3d)
        if made:  # its clip was rendered for the review: remember that it is current
            plan, repair, short[key] = made, None, made
            done.write_text(fingerprint(json.dumps(made, sort_keys=True), seconds, three=True), encoding="utf-8")
        else:
            short["opener3d_failed"] = why3d
            print(f"    no 3D opener ({why3d}): drawing it instead")
            plan = None if (plan or {}).get("kind") == "3d" else plan
    if not plan or repair:
        print("  drawing the opener: the strangest moment as a hand-drawn animation..." if i == 0 else
              f"  drawing scene {i + 1}, the reveal, as a hand-drawn animation...")
        problems, sheet, score = ([repair] if repair else []), None, 0.0
        for attempt in range(FIXES + 1):
            draft = write(short, words, seconds, plan, problems, sheet, i=i)
            if not draft:
                if plan is None:
                    return fail("the AI wrote no usable scene")
                break  # keep the last draft's problems
            plan, sheet, score = draft, None, 0.0
            problems = lint(plan["code"]) + missing_parts(plan, short["scenes"][i]["narration"])
            if not problems:
                scene.write_text(plan["code"], encoding="utf-8")
                err = node_run({**base, "mode": "sheet", "times": sheet_times(seconds), "scale": 0.3}, folder)
                if err:
                    problems = [f"the scene crashed when it ran: {err}"]
                else:
                    sheet = folder / f"sheet{attempt + 1}.png"
                    (folder / "sheet.png").replace(sheet)
                    score, problems = review(short, plan, sheet, seconds, i=i)
                    if score is None:  # no verdict: kept as it is, flagged (audit 2026-10-31: it used to pass silently)
                        score, plan["unreviewed"] = PASS, True
            if score >= PASS:
                break
            print(f"    {name} draft {attempt + 1} ({score:g}/10): " + "; ".join(problems)[:300])
        if score < PASS:
            return fail(f"the drawn {name}'s last draft scored {score:g}/10 after {FIXES} fixes: "
                        f"{'; '.join(problems)[:300]}")
        short[key] = plan
    if plan.get("kind") == "3d":
        from shortsmaker import opener3d
        mark = fingerprint(json.dumps(plan, sort_keys=True), seconds, three=True)
        if clip.exists() and done.exists() and done.read_text(encoding="utf-8") == mark:
            return clip, None
        err = opener3d.render(plan, seconds, folder)
        if err or not clip.exists():
            return fail(f"the 3D opener didn't render: {err or 'no clip came out'}")
        done.write_text(mark, encoding="utf-8")
        return clip, None
    scene.write_text(plan["code"], encoding="utf-8")
    mark = fingerprint(plan["code"], seconds)
    if clip.exists() and done.exists() and done.read_text(encoding="utf-8") == mark:
        return clip, None
    err = node_run({**base, "mode": "render"}, folder)
    if err or not clip.exists():
        return fail(f"the drawn {name} didn't render: {err or 'no clip came out'}")
    done.write_text(mark, encoding="utf-8")
    return clip, None
