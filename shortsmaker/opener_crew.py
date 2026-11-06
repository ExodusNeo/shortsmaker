"""The opener crew (owner, 2026-11-06): the 3D opener made by several focused AI calls instead of one that did
everything (it planned, drew, placed and framed in one ~100K-token prompt, thought 4-9 minutes a draft, and on the
live tests never passed: 36-51 minutes a run). Each member gets a short prompt about its one job:

  stager       plans the moment: place, light, people (look, hat, what they hold), animals, things, the action,
               the shots on their words. Kept in short["opener_staging"]; edit_plan.txt prints it.
  kit scout    (code) finds hats and things the staging needs that the kit doesn't have.
  part maker   one call per missing part, in parallel: draws that one hat or thing; the part checker looks at it on
               people (drawn/partsheet.mjs). Passed parts are kept in drawn/parts for every later Short; a failed
               one is replaced by the stager's named substitute.
  painters     one call per person or thing, in parallel: that cut-out's drawing code (drawn/CUTOUT.md). Animals
               come straight from the kit with no AI.
  layout       (code, `layout`; the placer AI until 2026-11-06, which kept spreading people apart) where
               everything stands and the shots, from the staging's beats.
  renderer     (code) opener3d.clean / render / sheet.
  checker      the art director and the sound-off test (drawn_opener.review); a painter redraws its own cut-out,
               every other problem sends the stager back to plan again. Up to drawn_opener.FIXES fix rounds,
               stopping when a fix doesn't help.

No posted Short is an example in any of these prompts (owner: they are already posted)."""

import json
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from shortsmaker import drawn_opener, llm, opener3d, session

DRAWN = drawn_opener.DRAWN
PARTS = Path(os.environ.get("SHORTSMAKER_PARTS") or DRAWN / "parts")
MAX_PARALLEL = 3  # AI calls at once: more would only queue on the same account's quota
VERBS = ("knocks", "hands", "holds", "shows", "points", "talks", "shouts", "reads", "writes", "stands", "walks",
         "runs", "rides", "falls", "looks", "listens", "waves", "drinks", "eats", "sleeps", "works", "digs", "throws",
         "dances", "jumps", "climbs", "carries", "pulls", "pushes", "fights", "sits", "kneels", "cries", "laughs")
# the kit pose a painter should use for the action (a live "dancing" plan said "walks": no dance verb, 2026-11-06)
POSES = {"dances": "`dance: u * 2 * Math.PI` (hops, sways, kicks, arms flung up), in every drawing",
         "walks": "`walk: u * 2 * Math.PI`", "runs": "`walk: u * 2 * Math.PI` with the arms swinging high",
         "jumps": "`dance: u * 2 * Math.PI` with both arms up", "waves": "one arm waving `arms: [12, 130 + 22 * Math.cos(u * 4 * Math.PI)], bend: [6, 30]`",
         "points": "one arm pointing `arms: [12, 95], bend: [6, 0]`", "shouts": "`face: 'open'` with an arm thrown up",
         "talks": "`face: f % 2 ? 'open' : 'flat'`", "knocks": "`k.knock` (the recipe)",
         "kneels": "`legs: [[10, 0], [-5, 100]], dip: 0` drawn 60 px lower (`k.person(w / 2, h - 20 + 60 * s / 4, ...)`): one knee on the ground"}
# what an animal can do in the kit (kit.mjs `does`); the stager picks one per animal (2026-11-06: the pig couldn't eat)
ANIMAL_DOES = {"stands": "", "walks": "walk: u * 2 * Math.PI", "runs": "walk: u * 2 * Math.PI, does: 'run'",
               "eats": "does: 'eat'", "jumps": "walk: u * 2 * Math.PI, does: 'jump'"}
HOLDABLE = ("letter", "paper", "cup", "bottle", "coin", "moneybag")  # kit.mjs HOLD: a hand grips them
ANIMALS = {  # kit animal: canvas w, h, metres tall, the call standing on the canvas's bottom centre
    "horse": (1300, 1100, 1.7, "k.horse(650, 1080, 2.8, o)"), "dog": (800, 620, .6, "k.dog(400, 600, 4.2, o)"),
    "cow": (1300, 1000, 1.5, "k.cow(650, 980, 2.6, o)"), "pig": (900, 640, .7, "k.pig(450, 620, 3.4, o)"),
    "cat": (600, 600, .35, "k.cat(300, 580, 4.4, o)"), "rabbit": (500, 600, .4, "k.rabbit(250, 580, 3.1, o)"),
    "bear": (1300, 900, 1.3, "k.bear(650, 880, 3.5, o)"), "chicken": (500, 560, .4, "k.chicken(250, 540, 3.4, o)")}
NAME = opener3d.NAME
PART_SIG = {"hat": re.compile(r"export\s+default\s+function\s+draw\s*\(\s*k\s*,\s*hy\s*,\s*o\s*\)"),
            "thing": re.compile(r"export\s+default\s+function\s+draw\s*\(\s*k\s*,\s*o\s*\)")}
PART_BANNED = re.compile(r"\bk\.(text|sign|bubble|sky|ground|room|house|shop|bank|factory|tower|hills|sea|island|depth|"
                         r"shadow|rays|dust|person|crowd)\(")


def kit_hats() -> list[str]:
    """The kit's own hats (kit.mjs HATS) plus the made ones in drawn/parts/hat."""
    text = (DRAWN / "kit.mjs").read_text(encoding="utf-8")
    own = re.findall(r'"(\w+)"', re.search(r"const HATS = \[(.*?)\];", text, re.S).group(1))
    return own + made("hat")


def made(kind: str) -> list[str]:
    return sorted(p.stem for p in (PARTS / kind).glob("*.mjs"))


def kit_text(*heads: str) -> str:
    """The KIT.md sections whose headings start with these words (a painter needs People, not Backgrounds)."""
    text = (DRAWN / "KIT.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(?=## )", text)
    return "\n".join(p for p in parts if any(p.startswith("## " + h) for h in heads)).strip()


def parallel(jobs: list) -> list:
    """Runs the zero-argument callables in `jobs`, MAX_PARALLEL at a time; their results in order."""
    if len(jobs) < 2:
        return [j() for j in jobs]
    with ThreadPoolExecutor(MAX_PARALLEL) as pool:
        return list(pool.map(lambda j: j(), jobs))


# ---- stager ----------------------------------------------------------------------------------------------------

def objects3d() -> list[str]:
    """Every 3D object a staging can use: the library's and the made 3D parts (owner, 2026-11-06: objects are 3D)."""
    return sorted(set(opener3d.OBJECTS) | set(opener3d.made3d()))


def check_staging(raw, words: list, allow_new: bool = True) -> tuple[dict | None, list[str]]:
    """The stager's plan, checked against what the kit and the 3D set can show; and what's wrong with it. A re-plan
    (`allow_new` False) can't add new parts: every bad potato part of the live runs came from a re-plan (2026-11-06)."""
    if not isinstance(raw, dict):
        return None, ["the reply was not a JSON object"]
    bad: list[str] = []
    new = [n for n in raw.get("new_parts") or [] if isinstance(n, dict) and n.get("kind") in ("hat", "thing")
           and isinstance(n.get("name"), str) and NAME.match(n["name"]) and str(n.get("looks") or "").strip()][:4]
    new = new if allow_new else []
    hats, things = set(kit_hats()), set(HOLDABLE) | set(objects3d())
    new_hats = {n["name"] for n in new if n["kind"] == "hat"}
    new_things = {n["name"] for n in new if n["kind"] == "thing"}
    st = {"place": raw.get("place") if raw.get("place") in opener3d.PLACES else "room",
          "light": raw.get("light") if raw.get("light") in opener3d.MOODS else "day",
          "people": [], "animals": [], "things": [], "new_parts": new}
    ids: set[str] = set()

    def take(x, kind: str) -> str | None:
        n = x.get("id") if isinstance(x, dict) else None
        if not isinstance(n, str) or not NAME.match(n) or n in ids:
            bad.append(f"each {kind} needs a unique lowercase `id` (letters, digits, _), got {n!r}")
            return None
        ids.add(n)
        return n

    for p in (raw.get("people") or [])[:3]:
        n = take(p, "person")
        if not n:
            continue
        hat, holds = str(p.get("hat") or "none"), str(p.get("holds") or "none")
        if hat not in hats | new_hats:
            bad.append(f"{n}'s hat {hat!r} isn't in the kit: use one of the hats listed, or add it to new_parts")
        if holds not in things | new_things | {"none"}:
            bad.append(f"{n} holds {holds!r}: a hand can hold {', '.join(sorted(things))}"
                       + (", or add it to new_parts as a thing" if allow_new else " (no new parts when planning again)"))
        st["people"].append({"id": n, "who": str(p.get("who") or n)[:80], "hat": hat, "holds": holds,
                             "coat": p["coat"] if opener3d.COLOR.match(str(p.get("coat") or "")) else None,
                             "doing": str(p.get("doing") or "")[:100]})
    for a in (raw.get("animals") or [])[:2]:
        n = take(a, "animal")
        if n and a.get("kind") in ANIMALS:
            # the kit's own colours: a live staging's historically black pig read as a dark blob (owner, 2026-11-06)
            st["animals"].append({"id": n, "kind": a["kind"], "color": None,
                                  "does": a["does"] if a.get("does") in ANIMAL_DOES else "stands"})
        elif n:
            bad.append(f"animal {n}: the kit's animals are {', '.join(ANIMALS)}")
    for t in (raw.get("things") or [])[:6]:
        n = take(t, "thing")
        kind = str((t or {}).get("kind") or "")
        if n and (kind in opener3d.PROPS or kind in new_things or kind in opener3d.made3d()):
            st["things"].append({"id": n, "kind": kind, "what": str(t.get("what") or kind)[:80]})
        elif n:
            bad.append(f"thing {n} ({kind!r}): use a 3D prop or object ({', '.join(sorted(set(opener3d.PROPS) | set(objects3d())))})"
                       + (", or add it to new_parts as a thing" if allow_new else " (no new parts when planning again)"))
    if not st["people"] and not st["animals"]:
        bad.append("the staging needs at least one person or animal: the subject is a drawn cut-out")
    held = {p["holds"] for p in st["people"]} - {"none"}
    for x in [x for x in st["things"] if x["kind"] in held]:  # held in a hand: not also standing in the set
        st["things"].remove(x)
    act = raw.get("action") if isinstance(raw.get("action"), dict) else {}
    st["action"] = {"who": act.get("who") if act.get("who") in ids else (st["people"] or st["animals"] or [{"id": None}])[0]["id"],
                    "does": act.get("does") if act.get("does") in VERBS else "stands",
                    "on": act.get("on") if act.get("on") in ids else None}
    if st["action"]["does"] == "knocks" and not any(t["kind"] in opener3d.BUILDINGS for t in st["things"]):
        bad.append("a knock needs a house or shopfront thing for the door (the knocker's cut-out holds the door)")
    beats = []
    for b in (raw.get("beats") or [])[:4]:
        on = [x for x in (b.get("on") if isinstance(b.get("on"), list) else [b.get("on")]) if x in ids] if isinstance(b, dict) else []
        if b and b.get("shot") in opener3d.SHOT_SIZES and on:
            beats.append({"at": b.get("at", 0), "shot": b["shot"], "on": on})
    if len(beats) < 2:
        bad.append(f"give 2-4 beats: a shot size ({', '.join(opener3d.SHOT_SIZES)}) on the ids it shows, at a spoken word")
    if beats and (beats[0]["shot"] not in ("medium", "close", "low") or len(beats[0]["on"]) > 2):
        # live reviews failed every opener that started on a wide or group shot: in a 9:16 frame it reads tiny
        bad.append("the first beat (at 0) must be medium, close or low on the main subject (one id, or two side by "
                   "side): a stranger must read it at a glance on a phone; a wide shot can come later")
    unseen = [p["id"] for p in st["people"] if not any(p["id"] in b["on"] for b in beats)]
    if beats and unseen:  # a live plan had a townsman no shot ever showed: the reviewer called him missing
        bad.append(f"{', '.join(unseen)} {'is' if len(unseen) == 1 else 'are'} in no beat: show every person in at least one shot, or leave them out")
    st["beats"] = beats
    st["moment"] = str(raw.get("moment") or "").strip()[:200]
    odd = raw.get("strange") if isinstance(raw.get("strange"), dict) else {}
    shows = [str(x).strip()[:160] for x in odd.get("shows") or [] if str(x).strip()][:4] if isinstance(odd.get("shows"), list) else []
    signs = []
    for e in (odd.get("effects") if isinstance(odd.get("effects"), list) else [])[:2]:
        kind, on = (e.get("type"), e.get("on")) if isinstance(e, dict) else (None, None)
        if kind not in opener3d.SIGN_EFFECTS or (kind != "aurora" and on not in ids):
            bad.append(f"strange effect {e!r}: type is one of {', '.join(opener3d.SIGN_EFFECTS)}, `on` an id above (not for aurora)")
        else:
            signs.append({"type": kind, **({"on": on} if kind != "aurora" else {})})
    st["strange"] = {"what": str(odd.get("what") or "").strip()[:160], "shows": shows, "effects": signs}
    if not st["strange"]["what"] or not shows:
        # the owner couldn't tell what a live Carrington opener was without the captions: nothing on screen said
        # "the battery is unplugged and it still works" (2026-11-06)
        bad.append("give `strange`: what (the one thing that makes this story strange) and shows (1-4 things a viewer "
                   "SEES with the sound off that make it unmistakable: an effect, a prop, a pose, a detail on a cut-out)")
    return st, bad


def strong() -> str | None:
    """Who does the stager's job: on a Gemini run whose Argon is out, Claude (Opus) instead of Flash
    (2026-11-06: Flash thought 1-10 min per call and its plans needed every fix round); else the run's own brain."""
    return "claude" if session.BRAIN == "gemini" and "claude" not in session.NO_QUOTA and llm.gemini_model() == llm.GEMINI_FALLBACK else None


def stage(short: dict, words: list, seconds: float, folder: Path, avoid: list[str] | None = None,
          last: dict | None = None) -> tuple[dict | None, str | None]:
    """The stager's plan (short["opener_staging"], reused when there is one), or (None, why). With `avoid` (and the
    `last` plan), the opener was sent back: plan again so those problems go away."""
    if isinstance(short.get("opener_staging"), dict) and not avoid:
        return short["opener_staging"], None
    short.pop("opener_staging", None)
    problems, raw = list(avoid or []), None
    for attempt in range(2):
        fix = ("\nYour last plan had these problems:\n- " + "\n- ".join(problems) +
               f"\nLast plan:\n{json.dumps(raw, ensure_ascii=False)}" if raw else
               ("\nThe last opener was sent back. Avoid this:\n- " + "\n- ".join(problems) +
                ("\nUse only the hats and objects listed: no new_parts this time." if last else "") +
                (f"\nYour last plan (change what these problems need; keep what works):\n{json.dumps(last, ensure_ascii=False)}"
                 if last else "") if problems else ""))
        raw = llm.ask_ai(f"""{drawn_opener.opener_role(short, words, seconds)}
You are the STAGER: you decide what the opener shows. The people are flat drawn stick figures (painters draw them);
every object is a 3D model in a 3D set. The code stands them in it (the one acting beside the main prop, small
objects on its top, everyone else beside the one acting) and films your beats. Plan ONE clear picture of the
strangest moment scene 1's narration says.
- place: "room" (an interior) | "street" (a town street) | "outdoors" (open ground, hills). light: "day" | "golden" | "dusk" | "night" | "interior".
- people (1-3; at most 3): id, who (one line: the person and their era), hat (one of: {', '.join(kit_hats())}),
  coat (a "#RRGGBB" that stands out from the place), holds (a drawn hand item: {', '.join(HOLDABLE)}; or a 3D
  object: {', '.join(objects3d())}; or "none"),
  doing (one line: their pose and action).
- animals (0-2): id, kind ({', '.join(ANIMALS)}), does ({' | '.join(ANIMAL_DOES)}: what it is doing in the moment).
- things (0-6): id, kind (a 3D prop or object: {', '.join(sorted(set(opener3d.PROPS) | set(objects3d())))}),
  what (one line). A held object is the person's `holds`, not a thing too.
- action: who (an id), does ({', '.join(VERBS)}), on (an id or null). A knock needs a "house", "shopfront" or "cabin" thing.
- beats (2-4): at (0 or a spoken word), shot ({', '.join(opener3d.SHOT_SIZES)}), on (the ids it shows). The first
  beat (at 0) is medium, close or low on the main subject (one or two ids): it must read at a glance on a phone.
  Cut close to the strange detail on its word; a wide shot, if any, comes later.
- strange: what (one line: the ONE thing that makes this story strange) and shows (1-4 things a viewer SEES with
  the sound off that make it unmistakable). A viewer watches muted with no captions: if the strange part is invisible
  (electricity, a disease, a law, a sound), show its visible signs: sparks ({', '.join(opener3d.SIGN_EFFECTS)} are
  effects in the set), a glowing or smoking thing, loose cut wires hanging from a held thing, a reaction pose, a
  telling object. "a man stands at a desk" is never enough. Every cue must be a person, thing, part or effect here.
  effects (0-2): {{"type": one of {', '.join(opener3d.SIGN_EFFECTS)}, "on": an id above (not for aurora)}}: they run
  from frame 0. Electricity, heat, fire, a sky event or any other invisible force MUST get one: a small moving part
  (a lever tapping, a needle twitching) can't be seen on a phone; sparks crackling off the machine can.
- new_parts (0-3): ONLY when the story needs a hat or an object the lists don't have (a pith helmet is there; a
  samurai helmet is not): kind ("hat": drawn on a person | "thing": a 3D object built from simple shapes), name
  (lowercase_id, used above as the hat/holds/kind), looks (one line: its telling shapes, colours and real size),
  instead (the nearest listed one, used if it can't be made). One object, never something "in a mouth" or "in a
  hand" (a hand holds through `holds`).
Real facts only: the people, things, clothes and era of the story.{fix}
Reply with ONLY JSON: {{"moment": "one sentence", "strange": {{"what": "...", "shows": ["..."], "effects": [...]}}, "place": "...", "light": "...",
"people": [...], "animals": [...], "things": [...], "action": {{...}}, "beats": [...], "new_parts": [...]}}""", fatal=False, brain=strong())
        st, problems = check_staging(raw, words, allow_new=last is None)
        if st and not problems:
            short["opener_staging"] = st
            return st, None
    return None, "the stager's plan didn't fit the kit: " + "; ".join(problems)[:300]


def staging_text(st: dict | None) -> str:
    """One readable line of the staging for edit_plan.txt."""
    if not isinstance(st, dict):
        return "none"
    who = "; ".join(f"{p['id']} ({p['who']}, {p['hat']} hat{', holding ' + p['holds'] if p['holds'] != 'none' else ''})"
                    for p in st.get("people", []))
    rest = ", ".join([f"{a['kind']} ({a.get('does', 'stands')})" for a in st.get("animals", [])] + [t["kind"] for t in st.get("things", [])])
    act = st.get("action") or {}
    beats = " / ".join(f"{b['shot']} on {'+'.join(b['on'])} at {b['at']}" for b in st.get("beats", []))
    odd = st.get("strange") or {}
    return (f"{st.get('place')}, {st.get('light')} light | {who}{' | ' + rest if rest else ''} | "
            f"{act.get('who')} {act.get('does')}{' ' + act['on'] if act.get('on') else ''} | shots: {beats}"
            + (f" | strange: {odd['what']} (shows: {'; '.join(odd.get('shows') or [])})" if odd.get("what") else ""))


# ---- parts -----------------------------------------------------------------------------------------------------

PART_FORMAT = {
    "hat": """export default function draw(k, hy, o) { ... } drawn in a person's head space: the head is a circle of radius
about 31 centred on (0, hy); the hat sits ON it (its brim near y = hy - 15, never lower than hy - 10 over the face).
About 60-140 wide, 30-90 tall. o.hatColor, if given, recolours it. Example (a kepi):
export default function draw(k, hy, o) { k.shape([[-28, hy - 18], [-25, hy - 62], [24, hy - 54], [28, hy - 18]], o.hatColor || k.C.navy); k.ink([[-30, hy - 16], [34, hy - 14]], { w: 7 }); }""",
    "thing": """export const grip = [x, y]; export default function draw(k, o) { ... } standing on (0, 0) (y up is negative), at the
scale of a person 245 tall: a lantern about 70 tall, a sword about 160 long, a basket about 60. `grip` is the point a
hand holds it by. Example (a lantern):
export const grip = [0, -78];
export default function draw(k, o) { k.shape(k.rect(-18, -60, 36, 56), "#F2C230"); k.shape(k.rect(-22, -66, 44, 8), "#2B2622"); k.shape(k.rect(-22, -6, 44, 6), "#2B2622"); k.ink([[-10, -66], [0, -78], [10, -66]], { w: 3 }); }"""}


def lint_part(code: str, kind: str) -> list[str]:
    live = drawn_opener.INERT.sub('""', code)
    found = [f"uses `{w}`: only k.* calls, Math and plain JavaScript are allowed"
             for w in dict.fromkeys(m.group(0) for m in drawn_opener.FORBIDDEN.finditer(live))]
    found += [f"calls k.{m}: a part is one hat or thing, no words or scenery" for m in dict.fromkeys(PART_BANNED.findall(live))]
    if not PART_SIG.get(kind, re.compile("^$")).search(code):
        found.append("missing the part's export line (see the format)")
    if len(code) > 6000:
        found.append("too long: a part is a few shapes")
    return found


def make_part(spec: dict, folder: Path) -> tuple[bool, str]:
    """Draws one new hat or thing, checks it by eye, keeps it in drawn/parts. (made, note for the log)."""
    kind, name = spec["kind"], spec["name"]
    out = folder / "parts"
    out.mkdir(parents=True, exist_ok=True)
    code, problems, began = None, [], time.monotonic()
    for attempt in range(2):
        fix = (f"\nYour last drawing had these problems:\n- " + "\n- ".join(problems) + f"\nLast code:\n{code}") if code else ""
        data = llm.ask_ai(f"""You draw ONE new part for a hand-drawn cartoon kit (flat colours, thick brush ink outlines, simple
shapes): a {kind} called {name}: {spec['looks']}.
Draw it with these kit calls only: k.shape(points, colour) (a painted shape with an ink outline; up to 6 points stay
sharp, more are smoothed), k.disc(x, y, r, colour), k.ink(points, {{w}}) (a brush line), k.oval(x, y, rx, ry) and
k.rect(x, y, w, h) (return points), k.at(x, y, s, rotation, () => {{...}}), colours k.C.ink, wood, brass, gold, navy,
red, white, plank, stone, leaf or "#RRGGBB". Only k.* calls, Math and plain JavaScript; no words.
Format: {PART_FORMAT[kind]}
Make it read as a {name} at a glance on a phone: its one or two telling shapes, big and clear.{fix}
Reply with ONLY JSON: {{"code": "..."}}""", fatal=False)
        code = drawn_opener.clean_code((data or {}).get("code")) if isinstance(data, dict) else None
        problems = lint_part(code, kind) if code else ["no code came back"]
        if problems:
            continue
        module, png = out / f"{name}.mjs", out / f"{name}.png"
        module.write_text(code, encoding="utf-8")
        (out / f"{name}.json").write_text(json.dumps({"kind": kind, "name": name, "module": str(module), "out": str(png)}), encoding="utf-8")
        try:
            r = subprocess.run(["node", "--disallow-code-generation-from-strings", str(DRAWN / "partsheet.mjs"), str(out / f"{name}.json")],
                               cwd=DRAWN, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            problems = ["drawing it took too long"]
            continue
        if r.returncode or not png.exists():
            problems = ["it crashed when it ran: " + (r.stderr or r.stdout).strip()[-300:]]
            continue
        look = drawn_opener.look_dir(png)
        verdict = llm.ask_ai(f"""You check one new part for a hand-drawn cartoon kit. Open {look / png.name}: a {kind} called {name}
({spec['looks']}), {'worn by three people' if kind == 'hat' else 'big on its own, on a table, and held in a hand'}.
Score 1-10: does it read as a {name} at a glance, in the same simple flat cartoon style as the people? 7 = good enough.
Problems that matter: it doesn't look like a {name}; {'it floats off the head, covers the face or sits inside the head' if kind == 'hat' else 'the hand does not hold it, or it is far too big or small next to the person'}; broken or messy shapes.
Reply with ONLY JSON: {{"score": 7, "problems": ["..."]}}""", fatal=False, read_dir=look)
        score = verdict.get("score") if isinstance(verdict, dict) else None
        if not isinstance(score, (int, float)) or score >= drawn_opener.PASS:  # no verdict: kept, as with openers
            (PARTS / kind).mkdir(parents=True, exist_ok=True)
            shutil.copy2(module, PARTS / kind / f"{name}.mjs")
            return True, f"made the {kind} {name} ({drawn_opener.minutes(began)}{', unreviewed' if score is None else f', {score:g}/10'})"
        problems = [str(p)[:200] for p in verdict.get("problems") or []] or [f"scored {score}/10"]
    return False, f"couldn't make the {kind} {name} ({'; '.join(problems)[:160]}): using {spec.get('instead') or 'none'}"


def make_part3d(spec: dict, folder: Path) -> tuple[bool, str]:
    """Builds one new 3D object from primitives, checks it by eye beside a person, keeps it in drawn/parts/thing3d.
    (made, note for the log)."""
    name, began = spec["name"], time.monotonic()
    out = folder / "parts3d"
    out.mkdir(parents=True, exist_ok=True)
    shapes, problems = None, []
    for attempt in range(2):
        fix = (f"\nYour last build had these problems:\n- " + "\n- ".join(problems) +
               f"\nLast build:\n{json.dumps({'shapes': shapes})}") if shapes else ""
        data = llm.ask_ai(f"""You build ONE object for a 3D cartoon set out of simple primitives, in a clean flat-shaded low-poly
style (like a toy model): a {name}: {spec['looks']}.
Metres; the origin is on the floor at the object's centre; y is up; its front faces +z (the camera). Real size: a
lantern about 0.35 tall, a 19th-century battery tray about 0.3 wide, a chair about 0.9 tall, a cart about 2 long.
Each primitive: {{"shape": "box" | "cylinder" | "sphere" | "cone" | "torus", "size": [x, y, z] (box: its sides;
cylinder and cone: [diameter, height, diameter], standing up; sphere: [diameter, diameter, diameter]; torus: a ring
standing up and facing the camera, [outer diameter, outer diameter, thickness]), "at": [x, y, z] (its centre),
"turn": [x, y, z] degrees (optional), "color": "#RRGGBB", "metal": true (brass, iron, copper; optional),
"glow": true (a lit lamp, a hot coal; optional)}}.
6-30 primitives: first the one or two telling shapes, big and clear, then a few details. Every piece touches
another; the lowest rests on y 0. No words or labels. Clear, saturated colours that read on a phone.{fix}
Reply with ONLY JSON: {{"shapes": [...]}}""", fatal=False)
        shapes, problems = opener3d.clean_shapes((data or {}).get("shapes") if isinstance(data, dict) else None)
        if problems or not shapes:
            problems = problems or ["no shapes came back"]
            continue
        png = out / f"{name}.png"
        err = opener3d.part_sheet(shapes, png)
        if err:
            problems = [err]
            continue
        look = drawn_opener.look_dir(png)
        verdict = llm.ask_ai(f"""You check one new 3D object for a cartoon set. Open {look / png.name}: left, the object (a {name}:
{spec['looks']}) on the floor beside a 1.75 m cartoon person; right, a close-up of it.
Score 1-10: does it read as a {name} at a glance, at a believable size next to the person? 7 = good enough.
Problems that matter: it doesn't look like a {name}; pieces floating apart; far too big or small; a mess of shapes.
Reply with ONLY JSON: {{"score": 7, "problems": ["..."]}}""", fatal=False, read_dir=look)
        score = verdict.get("score") if isinstance(verdict, dict) else None
        if not isinstance(score, (int, float)) or score >= drawn_opener.PASS:  # no verdict: kept, as with openers
            opener3d.PARTS3D.mkdir(parents=True, exist_ok=True)
            (opener3d.PARTS3D / f"{name}.json").write_text(json.dumps({"looks": spec["looks"], "shapes": shapes}), encoding="utf-8")
            return True, f"made the 3D thing {name} ({drawn_opener.minutes(began)}{', unreviewed' if score is None else f', {score:g}/10'})"
        problems = [str(x)[:200] for x in verdict.get("problems") or []] or [f"scored {score}/10"]
    return False, f"couldn't make the 3D thing {name} ({'; '.join(problems)[:160]}): using {spec.get('instead') or 'none'}"


def make_parts(st: dict, folder: Path, log: list[str]) -> None:
    """The kit scout and part makers: draws each new part the staging needs (in parallel); a part that fails is
    swapped for its substitute in the staging. In place."""
    todo = [n for n in st["new_parts"] if n["name"] not in (made("hat") + kit_hats() if n["kind"] == "hat" else objects3d())]
    results = parallel([lambda n=n: (make_part if n["kind"] == "hat" else make_part3d)(n, folder) for n in todo])
    for n, (ok, note) in zip(todo, results):
        log.append(note)
        print(f"    {note}")
        if ok:
            continue
        sub = n.get("instead") or "none"
        for p in st["people"]:
            if n["kind"] == "hat" and p["hat"] == n["name"]:
                p["hat"] = sub if sub in kit_hats() else "none"
            if n["kind"] == "thing" and p["holds"] == n["name"]:
                p["holds"] = sub if sub in HOLDABLE or sub in objects3d() else "none"
        st["things"] = [t if t["kind"] != n["name"] else {**t, "kind": sub} for t in st["things"]
                        if t["kind"] != n["name"] or sub in opener3d.PROPS or sub in objects3d()]


# ---- painters --------------------------------------------------------------------------------------------------

def default_cutout(p: dict, st: dict) -> dict:
    """A person's cut-out with no AI: the kit's person (or its knock) in the staging's hat, coat and held thing."""
    hold = f"[null, '{p['holds']}']" if p["holds"] in HOLDABLE else "[null, null]"  # a 3D object: the code puts it in the hand
    coat = f"'{p['coat']}'" if p.get("coat") else "k.C.navy"
    if st["action"]["does"] == "knocks" and st["action"]["who"] == p["id"]:
        hold = f"['{p['holds']}', null]" if p["holds"] in HOLDABLE else "[null, null]"
        return {"name": p["id"], "w": 1200, "h": 1100, "height": 2.3, "frames": 4, "fps": 8,
                "code": f"export default function draw(k, f, u) {{ k.knock(600, 1080, 3.4, {{phase: u, person: {{hat: '{p['hat']}', "
                        f"coat: {coat}, skin: k.SKIN[1], face: f % 2 ? 'open' : 'flat', hold: {hold}}}}}); }}"}
    return {"name": p["id"], "w": 700, "h": 1100, "height": 1.75, "frames": 2, "fps": 6,
            "code": f"export default function draw(k, f, u) {{ k.person(350, 1080, 4, {{hat: '{p['hat']}', coat: {coat}, "
                    f"skin: k.SKIN[1], face: f % 2 ? 'open' : 'flat', hold: {hold}, arms: [35, 43 + 5 * Math.sin(u * 2 * Math.PI)], bend: [-75, 30]}}); }}"}


def animal_cutout(a: dict) -> dict:
    w, h, height, call = ANIMALS[a["kind"]]
    o = "{" + ", ".join(x for x in (f"color: '{a['color']}'" if a.get("color") else "", ANIMAL_DOES[a.get("does") or "stands"]) if x) + "}"
    return {"name": a["id"], "w": w, "h": h, "height": height, "frames": 4, "fps": 6,
            "code": f"export default function draw(k, f, u) {{ const o = {o}; {call}; }}"}


def lint_person(code: str) -> list[str]:
    """A person cut-out is the kit's person and nothing pasted on it (owner, 2026-11-06: a painter's own skirt
    polygon read as "a weird red box", its hand-drawn fingers as weird hands): k.person / k.knock calls only."""
    calls = set(re.findall(r"\bk\.(\w+)\(", drawn_opener.INERT.sub('""', code)))
    other = sorted(calls - {"person", "knock"})
    return [f"draws its own shapes ({', '.join('k.' + c for c in other)}): a person is ONE k.person (or k.knock) call; "
            f"clothes are its options (`dress` for a skirt, `coat`, `hat`, `beard`), objects are 3D and not drawn"] if other else []


def paint(who: dict, st: dict, short: dict, folder: Path, problems: list[str] | None = None, old: dict | None = None) -> dict:
    """One painter: a person's cut-out ({name, w, h, height, frames, fps, code}), the kit's person only (every
    object is 3D). Falls back to the plain kit version (default_cutout) when the AI's code is unusable twice."""
    brief = f"{who['who']}: hat {who['hat']}, coat {who.get('coat') or 'your choice'}; {who['doing']}"
    held3d = who.get("holds") not in (None, "none") and who["holds"] not in HOLDABLE
    if held3d:  # the code puts the 3D object on the right hand (cutouts.mjs records it, Opener3D.tsx draws it there)
        brief += (f". Their RIGHT hand holds a 3D {who['holds']} that the code puts into that hand: pose the right arm to "
                  f"hold it where the story needs it (raised up to show it, held out, carried low); no `hold` for it")
    elif who.get("holds") not in (None, "none"):
        brief += f", holding the {who['holds']} (`hold: [null, '{who['holds']}']`)"
    act = st["action"]
    role = ("THE KNOCKER: use k.knock (the recipe), the door closed." if act["does"] == "knocks" and act["who"] == who["id"] else
            f"In the moment: {act['who']} {act['does']}{' ' + act['on'] if act.get('on') else ''}."
            + (f" Draw that with {POSES[act['does']]}." if act["who"] == who["id"] and act["does"] in POSES else ""))
    odd = st.get("strange") or {}
    if odd.get("what"):
        role += f"\nThe story's strange thing: {odd['what']}. Their pose and face must show it (a reaction, a gesture)."
    keep = (f" Keep everything the staging asks: {'the ' + who['hat'] + ' hat, ' if who.get('hat') not in (None, 'none') else ''}"
            f"the same clothes and colours.")
    fix = (f"\nYour last cut-out had these problems:\n- " + "\n- ".join(problems or []) +
           f"\nFix only those.{keep}\nLast one:\n{json.dumps(old, ensure_ascii=False)}") if old else ""
    for attempt in range(2):
        data = llm.ask_ai(f"""You are a PAINTER for the 3D opener of a YouTube Short: "{short['title']}".
Paint the person "{who['id']}": {brief}. {role}
The set: {st['place']}, {st['light']} light. Story era: {short.get('topic') or short['title']}.
A person is ONE k.person call (or k.knock for a knock) with its options, nothing else: no k.shape, k.ink, k.disc or
other drawing on top of it. Clothes are options (`dress` for a skirt or gown, `coat`, `hat`, `beard`); every object
in the scene is a 3D model the code adds.
{(DRAWN / 'CUTOUT.md').read_text(encoding='utf-8')}
--- The drawing kit (only these sections apply to a cut-out) ---
{kit_text('People')}{fix}
Reply with ONLY JSON: {{"w": ..., "h": ..., "height": ..., "frames": ..., "fps": ..., "code": "export default function draw(k, f, u) {{ ... }}"}}""",
                          fatal=False)
        cut = {"name": who["id"], **{k: data.get(k) for k in ("w", "h", "height", "frames", "fps")},
               "code": drawn_opener.clean_code(data.get("code"))} if isinstance(data, dict) else None
        bad = (opener3d.lint_cutout(cut["code"]) + lint_person(cut["code"])) if cut and cut["code"] else ["no code"]
        if not bad:
            return cut
        fix = "\nYour last cut-out broke these rules:\n- " + "\n- ".join(bad)
    print(f"    painter {who['id']}: no usable code, drawing the plain kit version")
    return default_cutout(who, st)


# ---- layout (code; was the placer AI) ---------------------------------------------------------------------------

SURFACES = ("desk", "table", "counter", "crate", "barrel", "cabinet", "fireplace", "bed")  # opener3d.TOPS kinds


def lum(color: str | None) -> float:
    """0 (black) .. 1 (white) of a "#RRGGBB" colour; .3 (a dark coat) when there is none."""
    if not color or not opener3d.COLOR.match(color):
        return .3
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return .2126 * r + .7152 * g + .0722 * b


def foot_of(kind: str) -> tuple[float, float, float] | None:
    """(width, depth, height) of a 3D prop, library object or made 3D part."""
    return opener3d.FOOT.get(kind) or (opener3d.load_part(kind) or {}).get("foot")


def layout(st: dict, cuts: list[dict], words: list) -> dict:
    """The stage the placer AI used to write, built from the staging by fixed rules (owner, 2026-11-06: the placer
    put the two subjects of a shot metres apart in every live run, and left the sign effects out). Every object is a
    3D prop: the main prop stands in the middle, small objects on its top (or by it), the one acting beside what they
    act on (at the door for a knock, in front of a desk or house), everyone else beside the one acting, animals in a
    garden or field; a person's 3D `holds` goes in their hand. The shots are the stager's beats in spoken order."""
    place, act = st["place"], st["action"]
    who, on = act.get("who"), act.get("on")
    names = {c["name"] for c in cuts}
    hung = [t for t in st["things"] if t["kind"] in ("window", "frame", "walllamp")]
    objs = [t for t in st["things"] if t not in hung and (f := foot_of(t["kind"])) and f[2] <= .5 and f[0] <= .7  # table-top size
            and t["kind"] not in SURFACES and t["kind"] not in opener3d.PATCHES]
    floor = [t for t in st["things"] if t not in hung and t not in objs]
    buildings = [t for t in floor if t["kind"] in opener3d.BUILDINGS]
    surfaces = [t for t in floor if t["kind"] in SURFACES]
    patches = [t for t in floor if t["kind"] in opener3d.PATCHES - {"rug"}]
    main = next((t for t in floor if t["id"] == on), None) or next(iter(buildings or surfaces or patches or floor), None)
    props = []
    if main:
        props.append({"type": main["kind"], "id": main["id"], "place": {"mark": "centre"}})
    for i, t in enumerate(x for x in floor if x is not main):  # the rest behind, out of the way of the action
        props.append({"type": t["kind"], "id": t["id"], "place": {"mark": ("back-right", "back-left", "back")[i % 3]}})
    surface = main if main in surfaces else next(iter(surfaces), None)
    for i, t in enumerate(objs):  # small objects: on the desk or table (toward the one acting), else by the main prop
        spec = ({"on": surface["id"], "side": ("left", "right", "centre")[i % 3]} if surface else
                {"beside": main["id"], "side": ("right", "left")[i % 2]} if main else
                {"mark": ("centre", "front-right", "front-left")[i % 3]})
        props.append({"type": t["kind"], "id": t["id"], "place": spec})
    sides = iter(("right", "left") * 3)
    for t in hung:
        if place == "room":
            props.append({"type": t["kind"], "id": t["id"], "place": {"wall": next(sides)}})
    odd = st.get("strange") or {}
    if place == "room" and any(e["type"] == "aurora" for e in odd.get("effects") or []) and not any(t["kind"] == "window" for t in hung):
        props.append({"type": "window", "id": "window", "place": {"wall": "left"}})  # the sky shows through it
    knocker = act.get("does") == "knocks"
    lead = who if who in names else next(iter(names), None)
    held = {p["id"]: p["holds"] for p in st["people"] if p["holds"] not in ("none", *HOLDABLE)}
    cutouts, effects, placed = [], [], set()

    def put(name: str, spec: dict, **more) -> None:
        cutouts.append({"name": name, "place": spec, **({"held": held[name]} if name in held else {}), **more})
        placed.add(name)

    animals = {a["id"] for a in st["animals"]}
    obj = next((t for t in objs if t["id"] == on), None)  # the small object the action is on

    def place_animal(n: str, near: str | None) -> None:
        put(n, {"in": patches[0]["id"], "side": "centre"} if patches else {"beside": near, "side": "right"} if near
            else {"front": main["id"]} if main else {"mark": "centre"})

    # the person or animal acted on stands first and the one acting right beside it (live 2026-11-06: the farmer
    # stood at the garden's edge, the pig in its middle, too far apart for one shot)
    target = on if on in names and on != lead else None
    if target:
        place_animal(target, None) if target in animals else put(target, {"mark": "centre"})
    if lead:
        if knocker and buildings:
            hits = [w[0] for w in words if str(w[2]).lower().startswith("knock")][:2] or [.6, 1.4]
            put(lead, {"door": buildings[0]["id"]}, hits=hits)
            effects += [{"type": kind, "at": h, "on": lead} for h in hits for kind in ("jolt", "puff")]
        elif target:
            put(lead, {"beside": target, "side": "left"})
        elif lead in animals and main in patches:  # a pig eating the potatoes stands IN the garden (2026-11-06)
            place_animal(lead, None)
        elif obj and not surface:
            put(lead, {"beside": obj["id"], "side": "left"})
        elif main and (main["kind"] in opener3d.BUILDINGS or main in surfaces):
            # in front of a house (beside it she went behind its walls) or of the desk he works at (beside a 2.3 m
            # desk he stood 2 m from its middle, and a shot on both filmed him tiny, live 2026-11-06)
            put(lead, {"front": main["id"]})
        elif main:
            put(lead, {"beside": main["id"], "side": "left"})
        else:
            put(lead, {"mark": "centre"})
    for i, n in enumerate(c["name"] for c in cuts if c["name"] not in placed):  # the rest: next to the one acting
        if n in animals:
            place_animal(n, lead)
        else:
            put(n, {"beside": lead, "side": "right" if i % 2 == 0 else "left"} if lead else {"mark": ("left", "right")[i % 2]})
    # a beat may name an object someone holds (it isn't a prop): it frames the one holding it
    holder = next(iter(held), None)
    known = names | {t["id"] for t in st["things"]} | ({"window"} if any(x["id"] == "window" for x in props) else set())
    shots = []
    # in spoken order, as clean sorts them: assemble matches its shots to these by position
    beats = sorted(st["beats"], key=lambda b: opener3d.word_time(words, b["at"], 0))
    for i, b in enumerate(beats):
        # aim at the people and small objects a beat names, not the furniture or garden around them (a shot on the
        # operator and a 2.3 m desk, or on a pig and its 3 m garden, backed off until both were tiny, 2026-11-06)
        ids = list(dict.fromkeys(x if x in known else holder for x in b["on"] if x in known or holder))
        on = [x for x in ids if x in names or any(o["id"] == x for o in objs)] or ids
        target = on if len(on) > 1 else on[0]
        size = b["shot"]
        if shots and shots[-1]["shot"] == size and shots[-1]["target"] == target:  # never the same framing twice
            size = "close" if size != "close" else "medium"
        shots.append({"at": b["at"], "target": target, "shot": size, "turn": (15, -15, 12, -12)[i % 4],
                      "move": "cut" if i == 0 else "whip"})
    coat = next((p.get("coat") for p in st["people"] if p["id"] == lead), None)
    colors = ({"wall": "#E3D3B0" if lum(coat) < .45 else "#4A3A2E", "floor": "#6A4A32", "trim": "#3A2A1C"}
              if place == "room" else {})
    needs = [t["what"][:40] for t in st["things"] if t["id"] in (on, *names)] + \
            [p["holds"] for p in st["people"] if p["holds"] != "none"]
    return {"moment": st["moment"], "needs": needs[:8], "place": place, "mood": st["light"], "colors": colors,
            "props": props, "cutouts": cutouts, "shots": shots, "effects": effects}


def assemble(raw, cuts: list[dict], st: dict, words: list, seconds: float, narration: str) -> tuple[dict | None, list[str]]:
    """The laid-out stage with the painters' cut-outs in it, cleaned by opener3d.clean, plus the story checks."""
    if not isinstance(raw, dict):
        return None, ["stager: the stage was not a JSON object"]
    by = {c["name"]: c for c in cuts}
    placed = {c.get("name"): c for c in raw.get("cutouts") or [] if isinstance(c, dict)}
    bad = [f"stager: {n!r} isn't one of the painted cut-outs ({', '.join(by)})" for n in placed if n not in by]
    merged = []
    for name, c in by.items():
        spot = placed.get(name) or {"place": {"mark": "centre"}}
        if name not in placed:
            bad.append(f"stager: the cut-out {name} is missing from the layout")
        merged.append({**{k: v for k, v in spot.items() if k not in ("code", "w", "h", "frames", "height")},
                       **{k: v for k, v in c.items() if k != "what" and v is not None}})
    # the stager's sign effects are put in by code: the live placer left the sparks out (Carrington, 2026-11-06)
    have = {(e.get("type"), e.get("on")) for e in raw.get("effects") or [] if isinstance(e, dict)}
    signs = [{**e, "at": 0} for e in (st.get("strange") or {}).get("effects") or [] if (e["type"], e.get("on")) not in have]
    raw = {**raw, "cutouts": merged, "effects": list(raw.get("effects") or []) + signs}
    stage, found = opener3d.clean(raw, words, seconds)
    if stage and len(stage["shots"]) == len(raw.get("shots") or []):
        # a close or medium shot whose subjects can't fit side by side (a wide drawn workbench, live 2026-11-06)
        # films its first subject alone, at the size planned (turning it wide made everyone tiny, 2026-11-06);
        # wide only when that would repeat the shot before it
        tight = {i for i, sh in enumerate(stage["shots"]) if opener3d.spread_out([sh], stage["cutouts"], stage["props"])}
        if tight:
            first = lambda sh: sh["target"][0] if isinstance(sh["target"], list) else sh["target"]  # noqa: E731
            shots = [{**sh, "target": first(sh)} if i in tight else sh for i, sh in enumerate(raw["shots"])]
            shown = {x for sh in shots for x in (sh["target"] if isinstance(sh["target"], list) else [sh["target"]])}
            for i in sorted(tight):  # never narrow a person out of every shot: then this shot films them
                orig = raw["shots"][i]["target"] if isinstance(raw["shots"][i]["target"], list) else []
                lost = [x for x in orig if x not in shown and any(p["id"] == x for p in st.get("people", []))]
                if lost:
                    shots[i]["target"] = lost[0]
                    shown.add(lost[0])
            for i in sorted(tight):
                if i and shots[i - 1]["shot"] == shots[i]["shot"] and shots[i - 1]["target"] == shots[i]["target"]:
                    shots[i] = {**raw["shots"][i], "shot": "wide"}
            raw["shots"] = shots
            stage, found = opener3d.clean(raw, words, seconds)
    # a painter owns only its drawing code's faults (the same lint clean ran); everything else goes to the stager
    # (routing by wording sent placement errors to painters twice in live runs, 2026-11-06)
    code = {f"cut-out {n}: {p}" for n, c in by.items() for p in (opener3d.lint_cutout(c["code"]) if c.get("code") else ["no code"])}
    bad += [p if p in code else f"stager: {p}" for p in found]
    if stage:
        shown = {n for sh in stage["shots"] for n in (sh["target"] if isinstance(sh["target"], list) else [sh["target"]]) + [sh.get("over")]}
        bad += [f"stager: {p['id']} is in no beat: show every person in at least one beat"
                for p in st.get("people", []) if p["id"] in by and p["id"] not in shown]
        types = {p.get("part") or p["type"] for p in stage["props"]} | {
            c["held"].get("part") or c["held"]["type"] for c in stage["cutouts"] if c.get("held")}
        # only the prop the action happens on is required (a live reviewer called a town house wrong for a frontier
        # farm, the placer removed it and was rejected for it, 2026-11-06)
        on = (st.get("action") or {}).get("on")
        bad += [f"stager: the action happens on {t['id']} ({t['kind']}), which isn't in the props" for t in st["things"]
                if t["id"] == on and t["kind"] in opener3d.PROPS and t["kind"] not in types]
        bad += [f"stager: {p}" for p in drawn_opener.missing_parts(
            {"moment": " ".join([stage["moment"], *stage["needs"]]), "code": "\n".join(c["code"] for c in stage["cutouts"])},
            narration, types, [p.get("open", 0) for p in stage["props"] if p["type"] == "door"])]
    return stage, bad


def owner(problem: str, names: list[str]) -> str:
    """Which crew member a problem goes to: person:<name> (that painter, for how it is drawn) or the stager
    (everything else: what is in the opener, its signs and its shots; there is no placer AI since 2026-11-06)."""
    m = re.match(r"\s*person:(\w+)\s*:", problem) or re.match(r"cut-out (\w+):", problem)
    return f"person:{m.group(1)}" if m and m.group(1) in names else "stager"


# ---- the crew --------------------------------------------------------------------------------------------------

def crew(st: dict, short: dict, folder: Path, log: list[str], old: dict | None = None) -> tuple[list[dict], list[dict], dict]:
    """The part makers and the painters for a staging: (the painted people, every cut-out, id -> what). `old` maps a
    person's staging entry (as JSON) to its earlier painting: an unchanged person keeps it across a re-plan (each
    re-plan used to re-roll every drawing, 2026-11-06)."""
    make_parts(st, folder, log)
    people = st["people"]
    t = time.monotonic()
    key = lambda p: json.dumps(p, sort_keys=True)  # noqa: E731
    todo = [p for p in people if key(p) not in (old or {})]
    fresh = dict(zip([key(p) for p in todo], parallel([lambda p=p: paint(p, st, short, folder) for p in todo])))
    cuts = [dict((old or {}).get(key(p)) or fresh[key(p)]) for p in people] + [animal_cutout(a) for a in st["animals"]]
    what = {p["id"]: p["who"] for p in people} | {a["id"]: f"a {a['kind']}" for a in st["animals"]}
    for c in cuts:
        c["what"], c["height"] = what.get(c["name"], c["name"]), opener3d.num(c.get("height"), .1, 6, 1.75)
    log.append(f"painters x{len(todo)} {drawn_opener.minutes(t)}")
    return people, cuts, what


def plan(short: dict, words: list, seconds: float, folder: Path, repair: str | None = None) -> tuple[dict | None, str | None]:
    """Stage, make parts, paint, lay out (code), render, review and route fixes: a painter redraws its own cut-out,
    anything else sends the stager back to plan again with the problems. (the passed stage marked "kind": "3d",
    whose clip is folder/opener.mp4) or (None, why). `seconds` already includes the crossfade."""
    folder.mkdir(parents=True, exist_ok=True)
    began, log = time.monotonic(), []
    short["opener_crew"] = log
    print("  staging the opener in 3D with the opener crew...")
    t = time.monotonic()
    st, why = stage(short, words, seconds, folder, [repair] if repair else None)
    if not st:
        return None, why
    log.append(f"stager {drawn_opener.minutes(t)}")
    print(f"    stager ({drawn_opener.minutes(t)}): {staging_text(st)}")
    people, cuts, what = crew(st, short, folder, log)
    problems, score, best = [], 0.0, None
    for attempt in range(drawn_opener.FIXES + 1):
        t = time.monotonic()
        names = [c["name"] for c in cuts]
        owners = {"stager": "what the opener shows: the moment, place, people, things, the strange thing and its "
                            "signs (sparks, smoke, glow, aurora), and the shots",
                  **{f"person:{c['name']}": f"how {c['what']} is drawn: pose, clothes, hat, what they hold, how they move" for c in cuts}}
        stage_, problems = assemble(layout(st, cuts, words), cuts, st, words, seconds, short["scenes"][0]["narration"])
        reviewed = False
        if stage_ and not problems:
            err = opener3d.render(stage_, seconds, folder)
            problems = [f"stager: {err}"] if err else opener3d.blends(stage_, folder)
            if not problems:
                preview = opener3d.sheet(folder / "opener.mp4", seconds, folder / f"sheet3d{attempt + 1}.png", stage_["shots"], folder / "cutouts")
                needs = f" It must show: {', '.join(stage_['needs'])}." if stage_["needs"] else ""
                score, problems = drawn_opener.review(short, {"moment": stage_["moment"] + needs}, preview, seconds,
                                                      pairs=True, owners=owners)
                reviewed = True
                if score is None:
                    score, stage_["unreviewed"] = drawn_opener.PASS, True
        else:
            score = 0.0
        log.append(f"draft {attempt + 1}: {score:g}/10 ({drawn_opener.minutes(t)})")
        if reviewed and score < drawn_opener.PASS and not drawn_opener.spoils(problems) and score > (short.get("opener3d_best") or {}).get("score", 0):
            short["opener3d_best"] = {"score": score, "plan": {**stage_, "kind": "3d"}}  # drawn_opener.make_opener may keep it
        if score >= drawn_opener.PASS:
            log.append(f"total {drawn_opener.minutes(began)}")
            print(f"    3D opener passed ({score:g}/10, crew total {drawn_opener.minutes(began)})")
            return {**stage_, "kind": "3d"}, None
        print(f"    3D opener draft {attempt + 1} ({score:g}/10, {drawn_opener.minutes(t)}): " + "; ".join(problems)[:300])
        if reviewed and best is not None and score <= best:
            print("    3D opener: no better than the last reviewed draft, stopping here")
            break
        best = score if reviewed else best
        if attempt == drawn_opener.FIXES:
            break
        painted = {p["id"] for p in people}  # animals come from the kit: their problems go to the stager
        t = time.monotonic()
        if any(owner(p, names) == "stager" or owner(p, names)[7:] not in painted for p in problems):
            # the plan itself is wrong (the sound-off test, a spoiler, the scene): the stager plans again, seeing
            # its last plan and every problem, and the painters paint the new plan
            redone = {owner(p, names)[7:] for p in problems if owner(p, names).startswith("person:")}
            kept = {json.dumps(p, sort_keys=True): c for p, c in zip(people, cuts) if p["id"] not in redone}
            st, why = stage(short, words, seconds, folder, problems, last=st)
            if not st:
                return None, why
            log.append(f"fix: stager {drawn_opener.minutes(t)}")
            print(f"    stager again: {staging_text(st)}")
            people, cuts, what = crew(st, short, folder, log, kept)
            continue
        redo = [c for c in cuts if any(owner(p, names) == f"person:{c['name']}" for p in problems)]
        done = parallel([lambda c=c: paint(next(p for p in people if p["id"] == c["name"]), st, short, folder,
                                           [p for p in problems if owner(p, names) == f"person:{c['name']}"],
                                           {k: c[k] for k in ("w", "h", "height", "frames", "code") if k in c}) for c in redo])
        for f in done:
            f["what"], f["height"] = what.get(f["name"], f["name"]), opener3d.num(f.get("height"), .1, 6, 1.75)
            cuts = [f if c["name"] == f["name"] else c for c in cuts]
        log.append(f"fix: {', '.join(c['name'] for c in redo)} {drawn_opener.minutes(t)}")
    log.append(f"total {drawn_opener.minutes(began)}")
    return None, f"the 3D opener's last draft scored {score:g}/10: {'; '.join(problems)[:300]}"
