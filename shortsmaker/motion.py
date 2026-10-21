"""Full-screen motion-graphic scenes and the AI-coded Custom scenes (with their look-and-fix check)."""

import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image

from shortsmaker import llm, media_tools
from shortsmaker.config import FPS, PALETTES, REMOTION, XFADE


def graphics_count(short: dict, cues: list[dict]) -> int:
    return (sum(1 for sc in short["scenes"] if sc["graphic"] or sc.get("full"))
            + sum(1 for c in cues if c.get("card")))


def full_summary(f: dict) -> str:
    """One plain line for edit_plan.txt saying what a full-screen motion graphic shows."""
    if f["type"] == "journey":
        return f"map journey: {' -> '.join(s['name'] for s in f['stops'])}" + (f", {f['note']}" if f.get("note") else "")
    if f["type"] == "number":
        if f.get("compare"):
            c = f["compare"]
            return f"big number: {f['label']}: {c['a_label']} {c['a_value']:,.10g} vs {c['b_label']} {c['b_value']:,.10g} (two bars)"
        painted = f", painted '{f['thing']}' figure" if f.get("figure") and Path(f["figure"]).exists() else ""
        return f"big number: {f['show']} {f['label']} ({f['figures']} figures, each = {f['each']:,.10g}{painted})"
    if f["type"] == "board":
        return "evidence board: " + " / ".join(it["label"] for it in f["items"])
    if f["type"] == "custom":
        return f"custom animation ({f.get('kind', 'diagram')}): {f.get('title', 'SCENE')} — {f.get('brief', '')}"
    return (f"document ({f['kind']}): \"{f['key_line']}\" underlined"
            + (f", masthead {f['paper']}" if f.get("paper") else ""))


def full_props(sc: dict, cue: dict, i: int, pics: list | None, job: Path,
               skin: str = "parchment", slot: int = 0) -> dict | None:
    """The `full` object Remotion draws for scene i: the plan's data, its word timings, and its pictures copied
    into the job folder. None when it can't be drawn (a board needs 3 photos)."""
    f, c = sc.get("full"), cue.get("full")
    if not f or not c:
        return None
    out = {k: v for k, v in f.items() if k not in ("word", "words", "find", "photos")}
    out["seed"] = i + 1
    out.setdefault("skin", skin)

    def put(k: int, pic: tuple) -> tuple[str, float]:
        path = job / f"full{i}_{k}.jpg"
        path.write_bytes(pic[0])
        with Image.open(path) as im:
            return f"job/{path.name}", im.width / im.height

    if f["type"] == "journey":
        out["stops"] = [{**{k: v for k, v in st.items() if k != "word"}, "at": t} for st, t in zip(f["stops"], c["times"])]
        out["noteAt"] = c.get("noteAt")
    elif f["type"] == "board":
        if not pics or len(pics) < 3:
            return None
        out["items"] = []
        for k, (it, pic, t) in enumerate(zip(f["items"], pics, c["times"])):
            image, aspect = put(k, pic)
            out["items"].append({"image": image, "aspect": aspect, "label": it["label"], "at": t})
    elif f["type"] == "number":
        out["at"] = c["at"]
        fig = Path(out.pop("figure", "") or "")
        if fig.name and fig.exists():  # Gemini's ink silhouette of the counted thing (else the built-in icon)
            shutil.copy(fig, job / f"fig{i}.png")
            out["image"] = f"job/fig{i}.png"
    elif f["type"] == "custom":
        cues_list = c.get("cues") or [0.5, 1.8, 3.0]
        out.update(slot=slot, cues=cues_list, photos=[])
        for k, (it, pic) in enumerate(zip(f.get("photos") or [], pics or [])):
            image, aspect = put(k, pic)
            out["photos"].append({"image": image, "aspect": aspect, "label": it["label"],
                                  "at": cues_list[min(k, len(cues_list) - 1)]})
    else:
        out.update(at=c["at"], lineEnd=c["lineEnd"])
        if pics:
            out["image"], out["aspect"] = put(0, pics[0])
    return out


def fallback_custom_tsx(slot: int, narration: str, brief: str) -> str:
    """Guaranteed-valid Remotion component for slot 0..3 if the AI coder fails or leaves a TypeScript error."""
    parts = [p.strip() for p in re.split(r"[,;:.—–-]+|\band\b|\bthen\b", narration) if p.strip()][:3]
    while len(parts) < 3:
        parts.append(brief[:42] or "KEY MOMENT")
    cards = [json.dumps(p[:36]) for p in parts[:3]]
    stamp = json.dumps(" ".join(parts[-1].upper().split()[:2])[:16] or "VERIFIED")
    return f"""import React from 'react';
import {{Card, Connect, CustomFull, FullProps, Paper, StampBadge, TitleBanner, cueAt, focusCam, layoutColumn, skinOf}} from '../toolkit';

export const Custom{slot}: React.FC<FullProps<CustomFull>> = ({{full, t, start, end}}) => {{
	const sk = skinOf(full.skin);
	const boxes = layoutColumn(3, {{w: 680, bottom: 900}});
	const c = [0, 1, 2].map((i) => cueAt(full, i, start, end, 3));
	const titles = [{', '.join(cards)}];
	return (
		<Paper t={{t}} start={{start}} seed={{full.seed}} cam={{focusCam(540, 630, 1)}} skin={{full.skin}}>
			<TitleBanner title={{full.title || 'CASE FILE'}} sub={{{json.dumps(brief[:48].upper())}}} t={{t}} at={{start + 0.05}} skin={{full.skin}} />
			{{boxes.map((b, i) => (
				<Card key={{i}} box={{b}} step={{i === 2 ? 'Outcome' : `Step 0${{i + 1}}`}} title={{titles[i]}} t={{t}} at={{c[i]}} skin={{full.skin}} highlight={{i === 1}} />
			))}}
			<Connect from={{boxes[0]}} to={{boxes[1]}} avoid={{boxes}} t={{t}} at={{c[1] - 0.3}} skin={{full.skin}} />
			<Connect from={{boxes[1]}} to={{boxes[2]}} avoid={{boxes}} t={{t}} at={{c[2] - 0.3}} skin={{full.skin}} />
			<StampBadge text={{{stamp}}} x={{540}} y={{965}} rot={{-7}} t={{t}} at={{c[2] + 0.5}} color={{sk.accent}} />
		</Paper>
	);
}};
"""


def clean_tsx_code(raw: str, slot: int) -> str | None:
    """Extract clean TypeScript/React code exporting Custom{slot} from an AI reply."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    code = raw.strip()
    fence = re.search(r"```(?:tsx|typescript|ts|jsx|js)?\s*\n(.*?)```", code, re.S)
    if fence:
        code = fence.group(1).strip()
    if f"export const Custom{slot}" not in code and f"export function Custom{slot}" not in code:
        return None
    return code + "\n"


def code_custom_scenes(short: dict, scenes: list[dict], work: Path) -> None:
    """Motion Graphics Agent: writes bespoke React/SVG Remotion code for each `type: 'custom'` scene in `scenes`,
    type-checks with `npx tsc -p .`, retries once on compiler errors, and falls back cleanly if needed."""
    npx = shutil.which("npx")
    gen_dir = REMOTION / "src" / "full" / "generated"
    customs = [(i, sc) for i, sc in enumerate(scenes) if (sc.get("full") or {}).get("type") == "custom"]
    if not customs:
        return
    for i, sc in customs:
        f = sc["full"]
        slot = int(f.get("slot") or 0)
        target = gen_dir / f"Custom{slot}.tsx"
        cached = work / f"Custom{slot}.tsx"
        narration = short["scenes"][i]["narration"]
        brief = short["scenes"][i]["full"].get("brief", "")
        sig = f"// Custom{slot}: {f.get('title')} | {f.get('kind')} | {f.get('skin')} | {brief[:80]}"
        if cached.exists() and cached.read_text(encoding="utf-8", errors="ignore").startswith(sig):
            target.write_text(cached.read_text(encoding="utf-8"), encoding="utf-8")
            continue
        print(f"    coding custom motion graphic for scene {i + 1} ({f.get('kind')}, {f.get('skin')} skin)...")
        prompt = f"""You are the Motion Graphics Coder for a vertical 1080x1920 YouTube Short: "{short['title']}".
Write a bespoke Remotion React/TypeScript component `Custom{slot}` for Scene {i + 1}.
- Scene narration: {narration!r}
- Scene time window: start={sc['start']:.2f}s, end={sc['end']:.2f}s
- Spoken beat timestamps (`full.cues`): {f.get('cues')}
- Visual skin (`full.skin`): {f.get('skin')!r}
- Category (`full.kind`): {f.get('kind')!r}
- Title (`full.title`): {f.get('title')!r}
- Visual brief to draw & animate: {brief!r}
- Available real photos in `full.photos`: {json.dumps(f.get('photos') or [], ensure_ascii=False)}

{custom_rules(slot)}
Reply with ONLY JSON: {{"code": "import React from 'react';\\n..."}}"""
        data = llm.ask_ai(prompt, fatal=False)
        code = clean_tsx_code((data or {}).get("code"), slot)
        ok = False
        for attempt in range(2):
            if not code:
                break
            target.write_text(sig + "\n" + code, encoding="utf-8")
            broken = lint_custom_code(code)
            err = "\n".join(broken) if broken else tsc_check() if npx else None
            if err is None:
                ok = True
                break
            if attempt == 0:
                print(f"      the check found an issue in Custom{slot}.tsx, repairing...")
                fix_data = llm.ask_ai(f"""Fix the problems in `Custom{slot}.tsx` below (compiler errors or broken scene rules).
Keep the same imports from `'../toolkit'` and export `Custom{slot}`.
{custom_rules(slot)}
Problems:
{err}

Broken code:
{code}

Reply with ONLY JSON: {{"code": "import React from 'react';\\n..."}}""", fatal=False)
                code = clean_tsx_code((fix_data or {}).get("code"), slot)
        if ok and npx:  # look at the scene before the real render, fix it once if it looks wrong
            better = look_and_fix(short, sc, slot, code, work)
            if better != code:
                target.write_text(sig + "\n" + better, encoding="utf-8")
                if tsc_check() is not None:  # the fix broke the build: keep the version that compiled
                    target.write_text(sig + "\n" + code, encoding="utf-8")
        if not ok:
            print(f"      using clean fallback layout for Custom{slot}.tsx")
            target.write_text(sig + "\n" + fallback_custom_tsx(slot, narration, brief), encoding="utf-8")
        cached.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")


def custom_rules(slot: int) -> str:
    """The rules every custom motion-graphic scene follows, plus two worked examples (real, compiling scenes in
    remotion/src/full/examples/). Shared by the coder, its repair, the look check and the review's redraw."""
    examples = "\n\n".join(f"// ===== {p.name} =====\n{p.read_text(encoding='utf-8')}"
                             for p in sorted((REMOTION / "src" / "full" / "examples").glob("*.tsx")))
    return f"""RULES (a scene that breaks one is rejected and rewritten):
1. Import ONLY from 'react' and '../toolkit'. Export `export const Custom{slot}: React.FC<FullProps<CustomFull>> = ({{full, t, start, end}}) => {{...}};`
2. Root element `<Paper t={{t}} start={{start}} seed={{full.seed}} cam={{focusCam(fx, fy, fScale)}} skin={{full.skin}}>`, first child
   `<TitleBanner title={{full.title}} sub="..." t={{t}} at={{start + 0.05}} skin={{full.skin}} />`. focusCam within fx 400..680, fy 550..650,
   fScale 0.95..1.14.
3. THE STAGE: everything (cards, photos, drawings, labels, stamps) inside x 110..970, y 260..1020 (SAFE). The title banner sits
   above it and the captions below it.
4. BOXES: every card is `<Card box={{...}}>` with a box from layoutRow / layoutColumn / layoutGrid / boxAt (fixed size, text
   always fits). A photo's outline is photoBox(...). Never FlowCard. Nothing may overlap anything else: leave room for
   stamps and labels on purpose (e.g. layoutColumn(3, {{bottom: 900}}) frees y 900..1020).
5. ARROWS: only `<Connect from={{boxA}} to={{boxB}} avoid={{everyBoxOnStage}} .../>`. It routes edge to edge and never
   crosses a box listed in avoid. Never FlowArrow, never hand-drawn arrow lines or arrowheads (<marker>).
6. MOVEMENT: anything that moves across the stage uses travel(t, at, from, to): it never goes faster than MIN_MOVE
   (0.9 s). No quick hops or zips; things land, then hold still while they are read.
7. TIMING: each element appears on a spoken beat (cueAt(full, i, start, end, n)); one idea per scene, at most ~6
   elements; text never smaller than the Card's own sizing. Animate only with interpolate / spring / appear / popIn /
   travel driven by `t`: CSS transition, animation and @keyframes don't render.
8. Be inventive inside these rules: your own <svg> drawings (a cross-section, a gauge, a route, a scale, a timeline),
   PhotoCutout for real photos in full.photos, ClockDial, CalloutTag, StampBadge, the skin's colours (skinOf(full.skin)).
9. TASTE (numbers from claude-motion's motion-design skill): arrivals ease out Easing.bezier(0.16, 1, 0.3, 1), exits ease
   in Easing.bezier(0.6, 0, 0.9, 0.35) in about half the entrance time, moves between two states Easing.bezier(0.65, 0,
   0.35, 1); linear only for continuous drift, rotation or ticking. Springs: settle {{damping: 14, stiffness: 140, mass:
   0.8}}, stamps/callouts pop {{damping: 10, stiffness: 220, mass: 0.7}}, at most ONE elastic accent {{damping: 8,
   stiffness: 200}} per scene. Stagger words ~0.09 s, list items ~0.2 s; never everything at once with one duration.
   One focal point per frame; the skin's accent colour marks the point, not decoration. Text never moves while it is
   read: it settles and holds >= 1 s (+0.25 s per word past three).
TWO WORKED EXAMPLES (copy their care, not their content):
{examples}"""


def lint_custom_code(code: str) -> list[str]:
    """Rule breaks a compiler can't see in an AI-coded custom scene (see custom_rules). Empty = clean."""
    found = []
    for mod in re.findall(r"""\bfrom\s+['"]([^'"]+)['"]""", code):
        if mod not in ("react", "../toolkit"):
            found.append(f"imports from '{mod}': import only from 'react' and '../toolkit'")
    checks = [(r"<FlowArrow\b", "draws an arrow by hand (FlowArrow): use <Connect from={box} to={box} avoid={allBoxes}>"),
              (r"<FlowCard\b", "uses FlowCard (it grows and overlaps): use <Card box={...}> with a box from layoutRow/layoutColumn/layoutGrid/boxAt"),
              (r"<marker\b|markerEnd|marker-end", "hand-made arrowheads: use <Connect>"),
              (r"\btransition\s*:|\banimation\s*:|@keyframes", "CSS transition/animation doesn't render in Remotion: animate with interpolate/travel")]
    found += [why for pattern, why in checks if re.search(pattern, code)]
    found += [f"missing <{tag}>" for tag in ("Paper", "TitleBanner") if f"<{tag}" not in code]
    return found


def preview_custom(short: dict, sc: dict, slot: int, work: Path) -> Path | None:
    """Renders just this custom scene small (its pictures are already in remotion/public/job) and returns a contact
    sheet of 8 frames across it, for the coder to look at before the real render. None if anything fails."""
    props = {"fps": FPS, "total": sc["end"] + 0.05, "xfade": XFADE, "hook": "", "palette": PALETTES.get(short.get("palette"), None),
             "scenes": [sc], "flashes": [], "words": [], "cta": None, "ctaLine": ""}
    return preview_sheet(props, sc["start"], sc["end"], work)


def preview_sheet(props: dict, start: float, end: float, work: Path) -> Path | None:
    """Renders seconds start..end of a small Short (`props`; its pictures already in remotion/public/job) at 40 %
    size and returns a contact sheet of 8 frames across it (work/look/sheet.jpg, next to preview.mp4), for an AI
    to look at before the real render. None if anything fails."""
    look = work / "look"
    shutil.rmtree(look, ignore_errors=True)
    look.mkdir(parents=True)
    a, b = int(start * FPS), max(int(start * FPS), int(end * FPS) - 1)
    (look / "props.json").write_text(json.dumps({k: v for k, v in props.items() if v is not None or k == "cta"}), encoding="utf-8")
    try:
        subprocess.run([shutil.which("npx") or "npx", "remotion", "render", "src/index.ts", "Short", str(look / "preview.mp4"),
                        f"--props={look / 'props.json'}", f"--frames={a}-{b}", "--scale=0.4", "--log=error", "--gl=angle",
                        "--concurrency=4", "--x264-preset=ultrafast"], cwd=REMOTION, check=True, timeout=600,
                       capture_output=True)
        step = max(1, (b - a + 1) // 8)
        media_tools.ffmpeg("-i", "preview.mp4", "-vf", f"select='not(mod(n\\,{step}))',scale=300:-1,tile=4x2", "-frames:v", "1",
               "-fps_mode", "vfr", "sheet.jpg", cwd=look)
    except (subprocess.SubprocessError, OSError):
        return None
    return look / "sheet.jpg" if (look / "sheet.jpg").exists() else None


def look_and_fix(short: dict, sc: dict, slot: int, code: str, work: Path) -> str:
    """The coder looks at 8 frames of its own scene before the real render and rewrites it once if something is wrong
    (overlaps, an arrow through a box, off the stage, unreadable, too fast). Returns the code to use: the rewrite
    only when it follows the rules (the caller compile-checks it), else the original."""
    sheet = preview_custom(short, sc, slot, work)
    if not sheet:
        return code
    print(f"      looking at the custom scene before rendering...")
    data = llm.ask_ai(f"""You coded `Custom{slot}` (below) for the YouTube Short "{short['title']}". Open {sheet} and look at it: 8 frames
across the scene, left to right, top to bottom (the captions and title banner are drawn later, ignore their space).
Check, as a strict art director: does anything overlap anything else? does an arrow or line cross a card, photo or
text? is anything outside the stage (x 110..970, y 260..1020) or cut off? is any text too small to read on a phone?
does anything jump or move so fast it looks like a glitch between frames? is the stage badly balanced (all crammed
in one corner, big empty areas)? do two things compete for attention in one frame? is text still sliding or growing
in a frame where it should be read? does everything appear at once instead of one after another? If it is clean, reply {{"ok": true}}. If not, list the problems and give the fixed
code that still follows every rule.
{custom_rules(slot)}
Current code:
{code}
Reply with ONLY JSON: {{"ok": false, "problems": ["..."], "code": "import React from 'react';\\n..."}}""",
                  fatal=False, read_dir=sheet.parent)
    if not isinstance(data, dict) or data.get("ok") is not False:
        return code
    new = clean_tsx_code(data.get("code"), slot)
    if not new or lint_custom_code(new):
        return code
    print(f"      fixed: {'; '.join(str(x) for x in data.get('problems') or [])[:160]}")
    return new


def tsc_check() -> str | None:
    """Type-checks the Remotion project; None when it compiles, else the compiler's complaint (trimmed)."""
    chk = subprocess.run([shutil.which("npx") or "npx", "tsc", "-p", "."], cwd=REMOTION, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=120)
    return None if chk.returncode == 0 else (chk.stdout + "\n" + chk.stderr).strip()[:1500]
