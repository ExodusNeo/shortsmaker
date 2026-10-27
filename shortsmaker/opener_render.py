"""Scene 1 as a Blender opener (2026-10-27): once the voice has set scene 1's length, the Short's staging plan
(opener_plan.py) gets its models (the library, else fetched through the owner's Blender), headless Blender builds,
checks and renders it (blender/opener_scene.py), the AI looks at a strip of frames, and failures go back to the
planner for up to 2 fix rounds. Success: work/opener.mp4 plays as scene 1. Anything else: (None, "opener failed:
...") and scene 1 stays as it is today, with that CHECK line. An unchanged plan and code reuse the last clip."""

import copy
import hashlib
import json
import math
import shutil
from pathlib import Path

from shortsmaker import blender_link, blender_render, config, llm, media_tools, opener_plan, session

SCRIPT = config.ROOT / "blender" / "opener_scene.py"
FPS = 30
TIMEOUT = 10 * 60
FIX_ROUNDS = 2


def scale_beats(plan: dict, seconds: float) -> dict:
    """Beat times squeezed into the real scene 1 (the voice can make it shorter than planned), order kept."""
    out = copy.deepcopy(plan)
    last = max(b["at"] for b in out["beats"])
    k = min(1.0, (seconds - 1 / FPS) / last) if last > 0 else 1.0
    for b in out["beats"]:
        b["at"] = math.floor(b["at"] * k * 10000) / 10000  # rounded down: never past the end
    return out


def pick_model(find: str, hits: list[dict]) -> dict | None:
    """One AI call picks the library result that is really `find` (by title), or none."""
    hits = hits[:10]
    if not hits:
        return None
    data = llm.ask_ai(f"""We need a free 3D model of: "{find}", for a short low-poly animation.
Search results: {json.dumps([{"n": i + 1, "title": h["title"]} for i, h in enumerate(hits)], ensure_ascii=False)}
Pick the one that is clearly this thing (not a statue, toy, sign or a different thing with the same word), or none.
Reply with ONLY JSON: {{"pick": 2}} or {{"pick": null}}""", fatal=False)
    n = data.get("pick") if isinstance(data, dict) else None
    return hits[n - 1] if isinstance(n, int) and not isinstance(n, bool) and 1 <= n <= len(hits) else None


def resolve_models(plan: dict) -> tuple[dict, str | None]:
    """{actor id, "<person id>:hat" / ":prop" or "backdrop:N": .blend path}, or ({}, why not). People come from the
    packed people library, which must be on D:."""
    people = [a for a in plan["actors"] if "person" in a]
    if people and not (config.PEOPLE_JSON.exists() and config.PEOPLE_BLEND.exists()):
        return {}, "people library missing"
    wanted = [(a["id"], a["find"], a["size_m"]) for a in plan["actors"] if "person" not in a]
    for a in people:  # a person's hat (from the role) and prop are models like any other
        role = opener_plan.ROLES[a["person"]]
        if role.get("hat"):
            wanted.append((f"{a['id']}:hat", role["hat"], 0.3))
        if a.get("prop"):
            wanted.append((f"{a['id']}:prop", a["prop"], a.get("prop_size_m") or role["height_m"] / 2))
    wanted += [(f"backdrop:{i}", b["find"], b["size_m"]) for i, b in enumerate(plan["set"].get("backdrop") or [])]
    models, online, unfound = {}, None, []
    for key, find, size in wanted:
        blend = blender_link.in_library(find)
        if blend is None:
            online = blender_link.ping() if online is None else online
            if not online:
                return {}, f"model '{find}' not in the library and Blender is off"
            try:
                hits = blender_link.search(find)
            except blender_link.LinkError as e:  # e.g. Poly Pizza switched off in the owner's open scene
                return {}, f"model '{find}' could not be searched ({e})"
            hit = pick_model(find, hits)
            if hit is None:  # every miss is named at once, so one fix round can replace them all
                unfound.append(find)
                continue
            blend, why = blender_link.fetch_model(hit, find, size)
            if blend is None:
                return {}, f"model '{find}' could not be fetched ({why})"
        models[key] = str(blend)
    if unfound:
        return {}, "no fitting model for " + ", ".join(f"'{f}'" for f in unfound)
    return models, None


def fingerprint(job: dict) -> str:
    h = hashlib.sha1(json.dumps(job, sort_keys=True).encode("utf-8"))
    for f in sorted((config.ROOT / "blender").glob("*.py")) + [config.ROOT / "blender" / "opener_tables.json"]:
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


def review_frames(report: dict, n: int) -> list[int]:
    """The frames the reviewer sees: 8 spread over the clip plus 3 around every key moment (a stroke's contact, the
    first frame something moves). Evenly spaced frames alone skipped a 0.3-second chop in the sixth live run."""
    even = sorted({1 + round(k * (n - 1) / 7) for k in range(8)})
    keys = sorted({min(max(f + d, 1), n) for k in report.get("key_frames") or [] for f in [k] for d in (-2, 0, 3)})
    picked = sorted(set(even) | set(keys))
    while len(picked) > 12:  # drop evenly spaced frames that sit close to a key moment first
        spare = [f for f in picked if f not in keys and f not in (1, n)]
        if not spare:
            break
        picked.remove(min(spare, key=lambda f: min(abs(f - k) for k in keys)))
    return picked


def review(short: dict, frames: Path, seconds: float, work: Path, report: dict | None = None) -> list[str]:
    """The AI looks at 8 frames: does the action make physical sense, and does frame 0 show the subject and the
    threat? Its problems, or [] (a failed or unreadable reply never blocks an opener the checks passed)."""
    from PIL import Image
    look = work / "opener_look"
    shutil.rmtree(look, ignore_errors=True)
    look.mkdir(parents=True)
    n = len(list(frames.glob("f_*.png")))
    picked = review_frames(report or {}, n)
    tiles = [Image.open(frames / f"f_{f:04d}.png").convert("RGB") for f in picked]
    tiles = [t.resize((270, round(270 * t.height / t.width))) for t in tiles]
    strip = Image.new("RGB", (270 * len(tiles), tiles[0].height))
    for i, t in enumerate(tiles):
        strip.paste(t, (270 * i, 0))
    strip.save(look / "strip.jpg", quality=88)
    when = ", ".join(f"{(f - 1) / FPS:.2f}s" for f in picked)
    data = llm.ask_ai(f"""strip.jpg in this folder shows {len(picked)} frames, left to right, at {when} of a {seconds:.1f}-second 3D animation
that opens a YouTube Short. It should show: {short['opener']['moment']}.
There are no people in these animations: tools are swung by an unseen hand just off-screen (the owner's choice), so
a tool whose handle runs off the edge of the frame is fine; a tool floating in the middle of the shot is not.
This channel's opener rules, including what the owner has accepted (never report those as problems):
{session.RULES.get("Opener") or opener_plan.DEFAULT_RULES}
Judge it like a picky viewer: does every action make physical sense (tools hit with their edge, nothing passes through
anything, nothing floats, pieces are the right size), and does the FIRST frame already show the subject and the threat?
Reply with ONLY JSON: {{"ok": true, "problems": []}} or {{"ok": false, "problems": ["the axe hits the breast", ...]}}""",
                      fatal=False, read_dir=look)
    if isinstance(data, dict) and data.get("ok") is False:
        return [str(p)[:200] for p in data.get("problems") or ["the review found a problem"]][:5]
    return []


def render_opener(short: dict, seconds: float, work: Path, exe: Path | None = None) -> tuple[Path | None, str | None]:
    """Scene 1's opener clip, or (None, why). (None, None) when the Short has no opener plan."""
    if not short.get("opener"):
        return None, None
    seconds = round(seconds * FPS) / FPS  # whole frames: a voice a few ms longer still reuses the clip
    exe = exe or config.BLENDER
    work.mkdir(parents=True, exist_ok=True)
    clip, frames, report_path, done = (work / "opener.mp4", work / "opener_frames", work / "opener_report.json",
                                       work / "opener_done.txt")
    for round_no in range(FIX_ROUNDS + 1):
        plan = scale_beats(short["opener"], seconds)
        models, why = resolve_models(plan)
        if why and why.startswith("no fitting model for") and round_no < FIX_ROUNDS:
            # back to the planner like any failure: the first people run lost its whole opener to a "ww2 armored
            # car" no free library has (2026-10-27)
            failures = [f"model: {why}; use a more common thing that reads the same (a truck for an armoured car) "
                        "or leave it out"]
            print(f"    try {round_no + 1} failed: {failures[0]}")
            fixed = opener_plan.fix_plan(short, failures, seconds, plan)
            if fixed is None:
                return None, f"opener failed: {why} (the fix wasn't usable)"
            short["opener"] = fixed
            continue
        if why:
            return None, f"opener failed: {why}"
        short["opener_credits"] = list(dict.fromkeys(c for c in map(blender_link.credit, map(Path, models.values())) if c))
        job = {"plan": plan, "models": models, "seconds": seconds, "fps": FPS, "size": [1080, 1920],
               "frames_dir": str(frames), "report": str(report_path), "render": True, "render_failed": False,
               "render_scale": 100}
        if any("person" in a for a in plan["actors"]):
            job["people"] = {"blend": str(config.PEOPLE_BLEND), "json": str(config.PEOPLE_JSON)}
        print_ = fingerprint(job)
        if done.exists() and done.read_text(encoding="utf-8") == print_ and clip.exists():
            return clip, None
        shutil.rmtree(frames, ignore_errors=True)
        report_path.unlink(missing_ok=True)
        (work / "opener_job.json").write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
        print(f"  Blender opener: {plan['moment'][:80]} (try {round_no + 1})")
        crash = ""
        for attempt in range(2):
            crash = blender_render._run(exe, work / "opener_job.json", SCRIPT, TIMEOUT)
            if not crash and report_path.exists():
                break
            crash = crash or "no report"
        else:
            return None, f"opener failed: Blender failed ({crash})"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        failures = list(report.get("failures") or [])
        if report.get("ok") and not failures:
            failures = review(short, frames, seconds, work, report)
            if not failures:
                media_tools.ffmpeg("-y", "-framerate", str(FPS), "-i", str(frames / "f_%04d.png"),
                                   *media_tools.video_encoder(), "-pix_fmt", "yuv420p", clip.name, cwd=work)
                done.write_text(print_, encoding="utf-8")
                shutil.rmtree(frames, ignore_errors=True)  # ~100 MB of PNGs; the clip is kept
                return clip, None
        print(f"    try {round_no + 1} failed: " + "; ".join(failures)[:600])
        if round_no == FIX_ROUNDS:
            return None, f"opener failed: {failures[0]}"
        fixed = opener_plan.fix_plan(short, failures, seconds, plan)
        if fixed is None:
            return None, f"opener failed: {failures[0]} (the fix wasn't usable)"
        short["opener"] = fixed
    return None, "opener failed"
