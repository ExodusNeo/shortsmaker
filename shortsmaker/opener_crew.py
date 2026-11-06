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
  placer       where everything stands (relations, never coordinates) and the shot sizes (drawn/STAGE3D.md).
  renderer     (code) opener3d.clean / render / sheet.
  checker      the art director (drawn_opener.review); every problem names who must fix it, and only that member
               redoes its part. Up to drawn_opener.FIXES fix rounds, stopping when a fix doesn't help.

No posted Short is an example in any of these prompts (owner: they are already posted)."""

import json
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from shortsmaker import drawn_opener, llm, opener3d

DRAWN = drawn_opener.DRAWN
PARTS = Path(os.environ.get("SHORTSMAKER_PARTS") or DRAWN / "parts")
MAX_PARALLEL = 3  # AI calls at once: more would only queue on the same account's quota
VERBS = ("knocks", "hands", "holds", "shows", "points", "talks", "shouts", "reads", "writes", "stands", "walks",
         "runs", "rides", "falls", "looks", "listens", "waves", "drinks", "eats", "sleeps", "works", "digs", "throws",
         "dances", "jumps", "climbs", "carries", "pulls", "pushes", "fights", "sits", "kneels", "cries", "laughs")
# the kit pose a painter should use for the action (a live "dancing" plan said "walks": no dance verb, 2026-11-06)
POSES = {"dances": "`dance: f * Math.PI / 2` (hops, sways, kicks, arms flung up), in every frame",
         "walks": "`walk: f * Math.PI / 2` (the placer moves the board)", "runs": "`walk: f * Math.PI / 2` with the arms swinging high",
         "jumps": "`dance: f * Math.PI / 2` with both arms up", "waves": "one arm waving `arms: [12, [150, 110, 150, 110][f]]`",
         "points": "one arm pointing `arms: [12, 95], bend: [6, 0]`", "shouts": "`face: 'open'` with an arm thrown up",
         "talks": "`face: f % 2 ? 'open' : 'flat'`", "knocks": "`k.knock` (the recipe)"}
HOLDABLE = ("letter", "paper", "cup", "bottle", "coin", "moneybag")  # kit.mjs HOLD: a hand grips them
DRAWN_THINGS = ("phone", "radio", "sack", "bottle", "cup", "moneybag", "coins", "clock", "fire", "letter", "paper")
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


def made_note() -> str:
    hats, things = made("hat"), made("thing")
    return (f"\nMade parts you can use: hats {', '.join(hats) or 'none'}; things {', '.join(things) or 'none'}."
            if hats or things else "")


def parallel(jobs: list) -> list:
    """Runs the zero-argument callables in `jobs`, MAX_PARALLEL at a time; their results in order."""
    if len(jobs) < 2:
        return [j() for j in jobs]
    with ThreadPoolExecutor(MAX_PARALLEL) as pool:
        return list(pool.map(lambda j: j(), jobs))


# ---- stager ----------------------------------------------------------------------------------------------------

def check_staging(raw, words: list) -> tuple[dict | None, list[str]]:
    """The stager's plan, checked against what the kit and the 3D set can show; and what's wrong with it."""
    if not isinstance(raw, dict):
        return None, ["the reply was not a JSON object"]
    bad: list[str] = []
    new = [n for n in raw.get("new_parts") or [] if isinstance(n, dict) and n.get("kind") in ("hat", "thing")
           and isinstance(n.get("name"), str) and NAME.match(n["name"]) and str(n.get("looks") or "").strip()][:4]
    hats, things = set(kit_hats()), set(HOLDABLE) | set(made("thing"))
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
            bad.append(f"{n} holds {holds!r}: a hand can hold {', '.join(sorted(things))}, or add it to new_parts as a thing")
        st["people"].append({"id": n, "who": str(p.get("who") or n)[:80], "hat": hat, "holds": holds,
                             "coat": p["coat"] if opener3d.COLOR.match(str(p.get("coat") or "")) else None,
                             "doing": str(p.get("doing") or "")[:100]})
    for a in (raw.get("animals") or [])[:2]:
        n = take(a, "animal")
        if n and a.get("kind") in ANIMALS:
            st["animals"].append({"id": n, "kind": a["kind"], "color": a["color"] if opener3d.COLOR.match(str(a.get("color") or "")) else None})
        elif n:
            bad.append(f"animal {n}: the kit's animals are {', '.join(ANIMALS)}")
    for t in (raw.get("things") or [])[:6]:
        n = take(t, "thing")
        kind = str((t or {}).get("kind") or "")
        if n and (kind in opener3d.PROPS or kind in DRAWN_THINGS or kind in new_things or kind in made("thing")):
            st["things"].append({"id": n, "kind": kind, "what": str(t.get("what") or kind)[:80],
                                 "height": opener3d.num(t.get("height"), .1, 3, .6)})
        elif n:
            bad.append(f"thing {n} ({kind!r}): use a set prop ({', '.join(sorted(opener3d.PROPS))}), a drawn thing "
                       f"({', '.join(DRAWN_THINGS)}), or add it to new_parts")
    if not st["people"] and not st["animals"]:
        bad.append("the staging needs at least one person or animal: the subject is a drawn cut-out")
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
    return st, bad


def stage(short: dict, words: list, seconds: float, folder: Path, avoid: list[str] | None = None) -> tuple[dict | None, str | None]:
    """The stager's plan (short["opener_staging"], reused when there is one), or (None, why)."""
    if isinstance(short.get("opener_staging"), dict) and not avoid:
        return short["opener_staging"], None
    short.pop("opener_staging", None)
    problems, raw = list(avoid or []), None
    for attempt in range(2):
        fix = ("\nYour last plan had these problems:\n- " + "\n- ".join(problems) +
               f"\nLast plan:\n{json.dumps(raw, ensure_ascii=False)}" if raw else
               ("\nThe last opener was sent back. Avoid this:\n- " + "\n- ".join(problems) if problems else ""))
        raw = llm.ask_ai(f"""{drawn_opener.opener_role(short, words, seconds)}
You are the STAGER: you decide what the opener shows. Painters will draw the people and things, a placer will put
them in a 3D set and film them. Plan ONE clear picture of the strangest moment scene 1's narration says.
- place: "room" (an interior) | "street" (a town street) | "outdoors" (open ground, hills). light: "day" | "golden" | "dusk" | "night" | "interior".
- people (1-3; at most 3): id, who (one line: the person and their era), hat (one of: {', '.join(kit_hats())}),
  coat (a "#RRGGBB" that stands out from the place), holds (one of: {', '.join(sorted(set(HOLDABLE) | set(made('thing'))))}, or "none"),
  doing (one line: their pose and action).
- animals (0-2): id, kind ({', '.join(ANIMALS)}), color.
- things (0-6): id, kind: set props ({', '.join(sorted(opener3d.PROPS))}) or drawn things ({', '.join(DRAWN_THINGS)}),
  what (one line), height (metres, drawn things only).
- action: who (an id), does ({', '.join(VERBS)}), on (an id or null). A knock needs a "house", "shopfront" or "cabin" thing.
- beats (2-4): at (0 or a spoken word), shot ({', '.join(opener3d.SHOT_SIZES)}), on (the ids it shows). The first
  beat (at 0) is medium, close or low on the main subject (one or two ids): it must read at a glance on a phone.
  Cut close to the strange detail on its word; a wide shot, if any, comes later.
- new_parts (0-3): ONLY when the story needs a hat or a held/standing thing the lists don't have (a pith helmet is
  there; a samurai helmet is not): kind ("hat" | "thing"), name (lowercase_id, used above as the hat/holds/kind),
  looks (one line: how it looks), instead (the nearest listed one, used if it can't be made).
Real facts only: the people, things, clothes and era of the story.{fix}
Reply with ONLY JSON: {{"moment": "one sentence", "place": "...", "light": "...", "people": [...], "animals": [...],
"things": [...], "action": {{...}}, "beats": [...], "new_parts": [...]}}""", fatal=False)
        st, problems = check_staging(raw, words)
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
    rest = ", ".join([a["kind"] for a in st.get("animals", [])] + [t["kind"] for t in st.get("things", [])])
    act = st.get("action") or {}
    beats = " / ".join(f"{b['shot']} on {'+'.join(b['on'])} at {b['at']}" for b in st.get("beats", []))
    return (f"{st.get('place')}, {st.get('light')} light | {who}{' | ' + rest if rest else ''} | "
            f"{act.get('who')} {act.get('does')}{' ' + act['on'] if act.get('on') else ''} | shots: {beats}")


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


def make_parts(st: dict, folder: Path, log: list[str]) -> None:
    """The kit scout and part makers: draws each new part the staging needs (in parallel); a part that fails is
    swapped for its substitute in the staging. In place."""
    todo = [n for n in st["new_parts"] if n["name"] not in made(n["kind"]) and not (n["kind"] == "hat" and n["name"] in kit_hats())]
    results = parallel([lambda n=n: make_part(n, folder) for n in todo])
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
                p["holds"] = sub if sub in HOLDABLE or sub in made("thing") else "none"
        st["things"] = [t if t["kind"] != n["name"] else {**t, "kind": sub} for t in st["things"]
                        if t["kind"] != n["name"] or sub in DRAWN_THINGS or sub in made("thing")]


# ---- painters --------------------------------------------------------------------------------------------------

def default_cutout(p: dict, st: dict) -> dict:
    """A person's cut-out with no AI: the kit's person (or its knock) in the staging's hat, coat and held thing."""
    hold = f"[null, '{p['holds']}']" if p["holds"] != "none" else "[null, null]"
    coat = f"'{p['coat']}'" if p.get("coat") else "k.C.navy"
    if st["action"]["does"] == "knocks" and st["action"]["who"] == p["id"]:
        hold = f"['{p['holds']}', null]" if p["holds"] != "none" else "[null, null]"
        return {"name": p["id"], "w": 1200, "h": 1100, "height": 2.3, "frames": 4, "fps": 8,
                "code": f"export default function draw(k, f) {{ k.knock(600, 1080, 3.4, {{phase: f / 4, person: {{hat: '{p['hat']}', "
                        f"coat: {coat}, skin: k.SKIN[1], face: f % 2 ? 'open' : 'flat', hold: {hold}}}}}); }}"}
    return {"name": p["id"], "w": 700, "h": 1100, "height": 1.75, "frames": 2, "fps": 6,
            "code": f"export default function draw(k, f) {{ k.person(350, 1080, 4, {{hat: '{p['hat']}', coat: {coat}, "
                    f"skin: k.SKIN[1], face: f % 2 ? 'open' : 'flat', hold: {hold}, arms: [35, f % 2 ? 48 : 38], bend: [-75, 30]}}); }}"}


def animal_cutout(a: dict) -> dict:
    w, h, height, call = ANIMALS[a["kind"]]
    o = "{" + (f"color: '{a['color']}', " if a.get("color") else "") + "walk: f * 1.6}"
    return {"name": a["id"], "w": w, "h": h, "height": height, "frames": 4, "fps": 6,
            "code": f"export default function draw(k, f) {{ const o = {o}; {call}; }}"}


def paint(who: dict, st: dict, short: dict, folder: Path, problems: list[str] | None = None, old: dict | None = None) -> dict:
    """One painter: a person's or drawn thing's cut-out ({name, w, h, height, frames, fps, code}). Falls back to the
    plain kit version (default_cutout) when the AI's code is unusable twice."""
    thing = "kind" in who
    brief = (f"the {who['what']} ({who['kind']}), standing about {who['height']} m tall" if thing else
             f"{who['who']}: hat {who['hat']}, coat {who.get('coat') or 'your choice'}, holding {who['holds']}; {who['doing']}")
    act = st["action"]
    role = (f"THE KNOCKER: use k.knock (the recipe), the door closed, {who.get('holds', 'nothing')} in the other hand."
            if not thing and act["does"] == "knocks" and act["who"] == who["id"] else
            f"In the moment: {act['who']} {act['does']}{' ' + act['on'] if act.get('on') else ''}."
            + (f" Draw that with {POSES[act['does']]}." if act["who"] == who["id"] and act["does"] in POSES else ""))
    keep = (f" Keep everything the staging asks: {'the ' + who['hat'] + ' hat, ' if who.get('hat') not in (None, 'none') else ''}"
            f"{'holding the ' + who['holds'] + ', ' if who.get('holds') not in (None, 'none') else ''}the same clothes and colours."
            if not thing else "")
    fix = (f"\nYour last cut-out had these problems:\n- " + "\n- ".join(problems or []) +
           f"\nFix only those.{keep} (a live fix dropped the thing the person was holding, 2026-11-06)"
           f"\nLast one:\n{json.dumps(old, ensure_ascii=False)}") if old else ""
    for attempt in range(2):
        data = llm.ask_ai(f"""You are a PAINTER for the 3D opener of a YouTube Short: "{short['title']}".
Paint the cut-out "{who['id']}": {brief}. {role}
The set: {st['place']}, {st['light']} light. Story era: {short.get('topic') or short['title']}.
{(DRAWN / 'CUTOUT.md').read_text(encoding='utf-8')}
--- The drawing kit (only these sections apply to a cut-out) ---
{kit_text('People', 'Animals', 'Rooms and furniture', 'Props', 'Made parts', 'Drawing your own thing')}{made_note()}{fix}
Reply with ONLY JSON: {{"w": ..., "h": ..., "height": ..., "frames": ..., "fps": ..., "code": "export default function draw(k, f) {{ ... }}"}}""",
                          fatal=False)
        cut = {"name": who["id"], **{k: data.get(k) for k in ("w", "h", "height", "frames", "fps")},
               "code": drawn_opener.clean_code(data.get("code"))} if isinstance(data, dict) else None
        bad = opener3d.lint_cutout(cut["code"]) if cut and cut["code"] else ["no code"]
        if not bad:
            return cut
        fix = "\nYour last cut-out broke these rules:\n- " + "\n- ".join(bad)
    print(f"    painter {who['id']}: no usable code, drawing the plain kit version")
    return default_cutout(who, st) if not thing else {
        "name": who["id"], "w": 600, "h": 600, "height": who["height"], "frames": 1,
        "code": f"export default function draw(k, f) {{ {'k.thing(' + repr(who['kind']) + ', 300, 580, 3)' if who['kind'] in made('thing') else 'k.' + who['kind'] + '(300, 580, 2)'}; }}"}


# ---- placer ----------------------------------------------------------------------------------------------------

def place(st: dict, cuts: list[dict], short: dict, words: list, seconds: float, folder: Path,
          problems: list[str] | None = None, old=None):
    """The placer's stage JSON (props, where each cut-out stands, shots, effects)."""
    coats = {p["id"]: p["coat"] for p in st["people"] if p.get("coat")}
    listing = "\n".join(f"- {c['name']}: {c['what']}, a board {c['height']:g} m tall"
                        + (f", coat {coats[c['name']]} (pick set colours that stand out from it)" if c["name"] in coats else "")
                        for c in cuts)
    fix = (f"\nYour last stage had these problems:\n- " + "\n- ".join(problems or []) +
           f"\nLast stage:\n{json.dumps(old, ensure_ascii=False)}\nFix every one of them.") if old else (
        ("\nAvoid this:\n- " + "\n- ".join(problems)) if problems else "")
    return llm.ask_ai(f"""{drawn_opener.opener_role(short, words, seconds)}
You are the PLACER. The painted cut-outs (place and time each one; you cannot change their drawings):
{listing}
{(DRAWN / 'STAGE3D.md').read_text(encoding='utf-8')}{fix}
Reply with ONLY the stage JSON.""", fatal=False)


def assemble(raw, cuts: list[dict], st: dict, words: list, seconds: float, narration: str) -> tuple[dict | None, list[str]]:
    """The placer's stage with the painters' cut-outs in it, cleaned by opener3d.clean, plus the story checks."""
    if not isinstance(raw, dict):
        return None, ["placement: the reply was not a JSON object"]
    by = {c["name"]: c for c in cuts}
    placed = {c.get("name"): c for c in raw.get("cutouts") or [] if isinstance(c, dict)}
    bad = [f"placement: {n!r} isn't one of the painted cut-outs ({', '.join(by)})" for n in placed if n not in by]
    merged = []
    for name, c in by.items():
        spot = placed.get(name) or {"place": {"mark": "centre"}}
        if name not in placed:
            bad.append(f"placement: the cut-out {name} is missing: give it a place")
        merged.append({**{k: v for k, v in spot.items() if k not in ("code", "w", "h", "frames", "height")},
                       **{k: v for k, v in c.items() if k != "what" and v is not None}})
    stage, found = opener3d.clean({**raw, "cutouts": merged}, words, seconds)
    # a painter owns only its drawing code's faults (the same lint clean ran); everything else is where the placer
    # put things (routing by wording sent placement errors to painters twice in live runs, 2026-11-06)
    code = {f"cut-out {n}: {p}" for n, c in by.items() for p in (opener3d.lint_cutout(c["code"]) if c.get("code") else ["no code"])}
    bad += [p if p in code else f"placement: {p}" for p in found]
    if stage:
        shown = {n for sh in stage["shots"] for n in (sh["target"] if isinstance(sh["target"], list) else [sh["target"]]) + [sh.get("over")]}
        bad += [f"camera: {p['id']} is in no shot: aim at least one shot at them (a list frames several)"
                for p in st.get("people", []) if p["id"] in by and p["id"] not in shown]
        types = {p["type"] for p in stage["props"]}
        # only the prop the action happens on is required: the placer may drop the rest (a live reviewer called a
        # town house wrong for a frontier farm, the placer removed it and was rejected for it, 2026-11-06)
        on = (st.get("action") or {}).get("on")
        bad += [f"placement: the action happens on {t['id']} ({t['kind']}), which isn't in the props" for t in st["things"]
                if t["id"] == on and t["kind"] in opener3d.PROPS and t["kind"] not in types]
        bad += [f"placement: {p}" for p in drawn_opener.missing_parts(
            {"moment": " ".join([stage["moment"], *stage["needs"]]), "code": "\n".join(c["code"] for c in stage["cutouts"])},
            narration, types, [p.get("open", 0) for p in stage["props"] if p["type"] == "door"])]
    return stage, bad


def owner(problem: str, names: list[str]) -> str:
    """Which crew member a problem goes to: person:<name> (that painter) or placement (the placer)."""
    m = re.match(r"\s*(person:\w+|placement|camera)\s*:", problem)
    if m:
        tag = m.group(1)
        return tag if tag in ("placement", "camera") or tag[7:] in names else "placement"
    m = re.match(r"cut-out (\w+):", problem)
    if m and m.group(1) in names:
        return f"person:{m.group(1)}"
    # opener3d.blends: the placer picks the wall colour, and that always fixes it (a live run sent pale paper back to
    # its painter, who can't make paper dark, 2026-11-06); everything else unnamed is the placer's too
    return "placement"


# ---- the crew --------------------------------------------------------------------------------------------------

def plan(short: dict, words: list, seconds: float, folder: Path, repair: str | None = None) -> tuple[dict | None, str | None]:
    """Stage, make parts, paint, place, render, review and route fixes. (the passed stage marked "kind": "3d",
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
    make_parts(st, folder, log)
    people = st["people"] + [x for x in st["things"] if x["kind"] not in opener3d.PROPS]
    t = time.monotonic()
    cuts = parallel([lambda p=p: paint(p, st, short, folder) for p in people]) + [animal_cutout(a) for a in st["animals"]]
    what = {p["id"]: (p.get("what") or p.get("who")) for p in people} | {a["id"]: f"a {a['kind']}" for a in st["animals"]}
    for c in cuts:
        c["what"] = what.get(c["name"], c["name"])
        c["height"] = opener3d.num(c.get("height"), .1, 6, 1.75)
    log.append(f"painters x{len(people)} {drawn_opener.minutes(t)}")
    names = [c["name"] for c in cuts]
    owners = {"placement": "where things stand, the props, set colours and effects",
              "camera": "the shots: their sizes, angles, targets and timing",
              **{f"person:{c['name']}": f"how {c['what']} is drawn: pose, clothes, hat, what they hold, how they move" for c in cuts}}
    raw, problems, score, best = None, [], 0.0, None
    for attempt in range(drawn_opener.FIXES + 1):
        t = time.monotonic()
        if raw is None:
            raw = place(st, cuts, short, words, seconds, folder, [repair] if repair else None)
            log.append(f"placer {drawn_opener.minutes(t)}")
        stage_, problems = assemble(raw, cuts, st, words, seconds, short["scenes"][0]["narration"])
        reviewed = False
        if stage_ and not problems:
            err = opener3d.render(stage_, seconds, folder)
            problems = [f"placement: {err}"] if err else opener3d.blends(stage_, folder)
            if not problems:
                preview = opener3d.sheet(folder / "opener.mp4", seconds, folder / f"sheet3d{attempt + 1}.png", stage_["shots"])
                needs = f" It must show: {', '.join(stage_['needs'])}." if stage_["needs"] else ""
                score, problems = drawn_opener.review(short, {"moment": stage_["moment"] + needs}, preview, seconds,
                                                      pairs=True, owners=owners)
                reviewed = True
                if score is None:
                    score, stage_["unreviewed"] = drawn_opener.PASS, True
        else:
            score = 0.0
        log.append(f"draft {attempt + 1}: {score:g}/10 ({drawn_opener.minutes(t)})")
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
        spoiler = next((p for p in problems if p.startswith("Opening reveals the answer")), None)
        if spoiler:  # the plan itself shows the answer: the stager plans again and the crew starts over
            st, why = stage(short, words, seconds, folder, [spoiler])
            if not st:
                return None, why
            make_parts(st, folder, log)
            people = st["people"] + [x for x in st["things"] if x["kind"] not in opener3d.PROPS]
            cuts = parallel([lambda p=p: paint(p, st, short, folder) for p in people]) + [animal_cutout(a) for a in st["animals"]]
            what = {p["id"]: (p.get("what") or p.get("who")) for p in people} | {a["id"]: f"a {a['kind']}" for a in st["animals"]}
            for c in cuts:
                c["what"], c["height"] = what.get(c["name"], c["name"]), opener3d.num(c.get("height"), .1, 6, 1.75)
            names, raw, problems, best = [c["name"] for c in cuts], None, [], None
            continue
        # each problem goes to its owner; the faulted painters and the placer fix theirs at the same time
        painted = {p["id"] for p in people}  # animals come from the kit: their problems go to the placer
        redo = [c for c in cuts if c["name"] in painted and any(owner(p, names) == f"person:{c['name']}" for p in problems)]
        mine = [p for p in problems if owner(p, names) in ("placement", "camera") or owner(p, names)[7:] not in painted]
        mine = mine or ([] if redo else problems)
        t = time.monotonic()
        jobs = [lambda c=c: paint(next(p for p in people if p["id"] == c["name"]), st, short, folder,
                                  [p for p in problems if owner(p, names) == f"person:{c['name']}"],
                                  {k: c[k] for k in ("w", "h", "height", "frames", "code") if k in c}) for c in redo]
        if mine:  # the placer sees the painted cut-outs as they were: it only moves, frames and times them
            jobs.append(lambda old=raw, mine=mine: place(st, cuts, short, words, seconds, folder, mine, old))
        done = parallel(jobs)
        if mine:
            raw = done.pop()
        for f in done:
            f["what"], f["height"] = what.get(f["name"], f["name"]), opener3d.num(f.get("height"), .1, 6, 1.75)
            cuts = [f if c["name"] == f["name"] else c for c in cuts]
        log.append(f"fix: {', '.join([c['name'] for c in redo] + (['placer'] if mine else []))} {drawn_opener.minutes(t)}")
    log.append(f"total {drawn_opener.minutes(began)}")
    return None, f"the 3D opener's last draft scored {score:g}/10: {'; '.join(problems)[:300]}"
