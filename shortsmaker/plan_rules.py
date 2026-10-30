"""Cleaning and validating the planner's JSON (graphics, full-screen scenes, styles) and word timings."""

import io
import re
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from shortsmaker import channel_profiles, llm, session, style_lab
from shortsmaker.config import (
    CUSTOM_KINDS, DOC_KINDS, FONT, FULL_TYPES, ICONS, MAX_FIGURES, PLANNED_STYLES, SKINS, SPECIAL_TRANSITIONS,
    STYLE_CAPS,
)


def is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def coords(lat, lon) -> bool:
    return is_num(lat) and is_num(lon) and -85 <= lat <= 85 and -180 <= lon <= 180


CRASH_WORDS = {"down", "drop", "dropped", "dropping", "fell", "fall", "falling", "crashed", "crash", "crashing",
               "plunged", "plunge", "sank", "slashed", "lost", "shrunk", "shrank", "collapsed", "tumbled", "tanked"}


def clean_graphic(g, said: list[str]) -> dict | None:
    """One planned callout, validated (LLM output is untrusted); None drops it."""
    if not (isinstance(g, dict) and g.get("style") in PLANNED_STYLES and str(g.get("text", "")).strip()):
        return None
    text = str(g["text"]).strip()
    out = {"style": g["style"], "text": text[:90] if g["style"] == "quote" else text.upper()[:48 if g["style"] == "headline" else 28]}
    if g["style"] == "headline":
        out.update({k: str(g[k]).strip().upper()[:28] for k in ("paper", "date") if str(g.get(k) or "").strip()})
    if g["style"] == "quote":
        if not str(g.get("by") or "").strip() or len(text.split()) > 14:
            return None
        out["by"] = str(g["by"]).strip()[:40]
    if g["style"] == "compare":
        labels = [str(g.get(k) or "").strip().upper()[:14] for k in ("a_label", "b_label")]
        values = [g.get(k) for k in ("a_value", "b_value")]
        if not all(labels) or not all(is_num(v) and 0 < v < 1e12 for v in values):
            return None
        for side, label, v in zip("ab", labels, values):
            show = str(g.get(f"{side}_show") or "").strip().upper()[:14] or f"{v:,.10g}"
            out.update({f"{side}_label": label, f"{side}_value": float(v), f"{side}_show": show})
    if g["style"] == "stamp" and len(text.split()) > 2:
        return None
    if g["style"] == "question":  # answered later in the script: a question, never a claim
        if not text.endswith("?") or len(text.split()) > 6:
            return None
        out["text"] = text.upper()[:40]
    if g["style"] == "kinetic":  # the spoken words themselves, landing hard
        spoken = words_of(text)
        if not 1 <= len(text.split()) <= 4 or len(re.sub(r"\W", "", text)) > 20 or not spoken \
                or not all(w in said for w in spoken) or not (isinstance(g.get("trigger"), str) and contains(said, words_of(g["trigger"]))):
            return None
    if g["style"] == "invented" and len(text.split()) > 6:
        return None
    if g["style"] == "place" and coords(g.get("lat"), g.get("lon")):  # coordinates feed the animated map
        out.update(lat=float(g["lat"]), lon=float(g["lon"]))
        f = g.get("from")
        if isinstance(f, dict) and coords(f.get("lat"), f.get("lon")) and str(f.get("text", "")).strip():
            out["from"] = {"text": str(f["text"]).strip().upper()[:28], "lat": float(f["lat"]), "lon": float(f["lon"])}
    if g["style"] == "stat":
        v, of = g.get("value"), g.get("of")
        if not (is_num(v) and 0 < v < 1e12):
            return None
        out["value"] = v
        if isinstance(of, int) and not isinstance(of, bool) and float(v).is_integer() and v <= of <= 200:
            out["of"] = of
        elif g.get("direction") == "down" or g.get("isCrash") is True or bool(set(said) & CRASH_WORDS):
            out["direction"] = "down"
            if is_num(g.get("from_value")) and g["from_value"] > v:
                out["from_value"] = g["from_value"]
    if g["style"] == "timeline":
        ends = [str(g.get(k) or "").strip().upper()[:16] for k in ("start", "end")]
        if not all(ends):
            return None
        out["start"], out["end"] = ends
    if isinstance(g.get("trigger"), str) and contains(said, words_of(g["trigger"])):
        out["trigger"] = g["trigger"].strip()
    return out


def show_number(v: float) -> str:
    """How the big-number scene prints a value: 30,000 / 1.5 MILLION / 2 BILLION / 0.3."""
    for size, word in ((1e9, "BILLION"), (1e6, "MILLION")):
        if v >= size:
            return f"{v / size:,.1f}".removesuffix(".0") + f" {word}"
    return f"{v:,.2f}".rstrip("0").rstrip(".") if not float(v).is_integer() else f"{v:,.0f}"


def number_figures(value: float, each) -> tuple[float, int]:
    """(what one ink figure stands for, how many to draw): the planner's `each` when it gives 1-60 figures,
    else the smallest round 1/2/5 x 10^k that does."""
    if not (is_num(each) and each > 0 and value / each <= MAX_FIGURES):
        each = next(m * 10 ** k for k in range(-2, 13) for m in (1, 2, 5) if value / (m * 10 ** k) <= MAX_FIGURES)
    return each, max(1, round(value / each))


def clean_full(f, said: list[str]) -> dict | None:
    """One planned full-screen motion graphic, validated (AI output is untrusted); None drops it. Timing words
    (`word`) are kept only when the narration says them; the renderer times everything else evenly."""
    if not (isinstance(f, dict) and f.get("type") in FULL_TYPES):
        return None

    def text(v, n: int, upper: bool = False) -> str:
        s = str(v or "").strip()
        if len(s) > n:  # cut at a word ("FRANCS PAID FOR THE EIFF" on the first number opener)
            s = s[:n + 1].rsplit(" ", 1)[0] if " " in s[:n + 1] else s[:n]
        s = s.strip()
        return s.upper() if upper else s

    def word(d: dict) -> dict:
        w = d.get("word")
        return {"word": w.strip()} if isinstance(w, str) and contains(said, words_of(w)) else {}

    out = {"type": f["type"]}
    if f.get("skin") in SKINS:
        out["skin"] = f["skin"]
    if f["type"] == "board":
        items = [{"label": " ".join(text(it.get("label"), 60, True).split()[:3])[:24], "find": text(it.get("find"), 120), **word(it),
                  **({"pic": it["pic"]} if type(it.get("pic")) is int else {})}
                 for it in f.get("items") or [] if isinstance(it, dict) and text(it.get("label"), 60)][:5]
        if len(items) < 3:
            return None
        links = [[a, b] for a, b in (lk for lk in f.get("links") or [] if isinstance(lk, list) and len(lk) == 2)
                 if isinstance(a, int) and isinstance(b, int) and not isinstance(a, bool) and not isinstance(b, bool)
                 and a != b and 0 <= a < len(items) and 0 <= b < len(items)]
        out.update(items=items, links=links)
    elif f["type"] == "journey":
        stops = [{"name": text(s.get("name"), 28), "lat": float(s["lat"]), "lon": float(s["lon"]), **word(s)}
                 for s in f.get("stops") or [] if isinstance(s, dict) and text(s.get("name"), 28) and coords(s.get("lat"), s.get("lon"))][:4]
        if not stops:
            return None
        out["stops"] = stops
        if text(f.get("note"), 24):
            out["note"] = text(f.get("note"), 24, True)
    elif f["type"] == "number":
        v = f.get("value")
        if not (is_num(v) and 0 < v < 1e12 and text(f.get("label"), 24)):
            return None
        each, figures = number_figures(v, f.get("each"))
        out.update(value=v, show=show_number(v), label=text(f["label"], 24, True), each=each, figures=figures,
                   icon=f.get("icon") if f.get("icon") in ICONS else "person", **word(f))
        thing = text(f.get("thing"), 24).lower()
        if re.fullmatch(r"[a-z][a-z '-]{1,23}", thing):  # what one figure is: painted as an ink silhouette
            out["thing"] = thing
        c = f.get("compare")
        if isinstance(c, dict) and all(text(c.get(k), 14) for k in ("a_label", "b_label")) and all(
                is_num(c.get(k)) and 0 <= c[k] < 1e12 for k in ("a_value", "b_value")) and max(c["a_value"], c["b_value"]) > 0:
            out["compare"] = {"a_label": text(c["a_label"], 14, True), "a_value": c["a_value"],
                              "b_label": text(c["b_label"], 14, True), "b_value": c["b_value"]}
    elif f["type"] == "custom":
        title, brief = text(f.get("title"), 38, True), text(f.get("brief"), 260)
        if not title or not brief:
            return None
        kind = f.get("kind") if f.get("kind") in CUSTOM_KINDS else "diagram"
        raw_words = f.get("words") if isinstance(f.get("words"), list) else ([f["word"]] if isinstance(f.get("word"), str) else [])
        words = [w.strip() for w in raw_words if isinstance(w, str) and contains(said, words_of(w))][:4]
        photos = [{"label": " ".join(text(p.get("label") or p.get("find"), 40, True).split()[:3])[:22],
                   "find": text(p.get("find") or p.get("label"), 120), **word(p)}
                  for p in (f.get("photos") or []) if isinstance(p, dict) and (text(p.get("label"), 40) or text(p.get("find"), 120))][:3]
        out.update(kind=kind, title=title, brief=brief, words=words, photos=photos)
    else:
        line = text(f.get("key_line"), 160)
        if f.get("kind") not in DOC_KINDS or not line or len(line.split()) > 14:
            return None
        out.update(kind=f["kind"], key_line=line, **word(f),
                   **{k: text(f.get(k), 40) for k in ("date", "paper", "find") if text(f.get(k), 40)})
        if "find" in out:
            out["find"] = text(f.get("find"), 120)
    return out


def clean_transition(v) -> str:
    """A planned scene change: a library transition name or "invented"; anything else is a fade (the old default)."""
    names = {e["name"] for e in style_lab.style_library("transition")} | {"invented"}
    return v if isinstance(v, str) and v in names else "fade"


def clean_look(v, ch: dict) -> dict | None:
    """The Short's photo look: {"name": <library look>} (not one of the channel's last 2), or an invention
    {"name": "invented", "title", "brief", "fallback": <library look>}; None = no look."""
    if not isinstance(v, dict):
        return None
    if isinstance(v.get("invent"), dict):
        inv = clean_invention(v["invent"], "look")
        return {"name": "invented", **inv} if inv else None
    looks = {e["name"] for e in style_lab.style_library("look")}
    name = v.get("name")
    return {"name": name} if name in looks and name not in ch.get("recent_looks", [])[-2:] else None


def clean_invention(v, kind: str) -> dict | None:
    """A planned invention {"title", "brief", "fallback": <library name of that kind>}, validated; None drops it."""
    if not isinstance(v, dict):
        return None
    title, brief = str(v.get("title") or "").strip(), str(v.get("brief") or "").strip()
    names = {e["name"] for e in style_lab.style_library(kind)}
    return {"title": title[:40], "brief": brief[:400], "fallback": v["fallback"]} \
        if title and brief and v.get("fallback") in names else None


def settle_style(s: dict, ch: dict) -> None:
    """Validates the Short's style plan (look, invented transition/overlay); an "invented" transition or overlay
    without its validated spec falls back to a fade / no graphic."""
    s["look"] = clean_look(s.get("look"), ch)
    s["invented_transition"] = clean_invention(s.get("invented_transition"), "transition")
    s["invented_overlay"] = clean_invention(s.get("invented_overlay"), "overlay")
    for sc in s["scenes"]:
        if sc.get("transition") == "invented" and not s["invented_transition"]:
            sc["transition"] = "fade"
        if (sc.get("graphic") or {}).get("style") == "invented" and not s["invented_overlay"]:
            sc["graphic"] = None


def limit_style(scenes: list[dict]) -> None:
    """Guardrails for the style library (STYLE_CAPS): the hook keeps only its title (no question/kinetic/invented
    overlay), at most 1 question beat, 2 kinetic titles, 2 invented overlays and 3 special transitions per Short;
    later ones are dropped (graphics) or become fades (transitions)."""
    used = {"question": 0, "kinetic": 0, "invented": 0, "special": 0}
    for i, sc in enumerate(scenes):
        style = (sc.get("graphic") or {}).get("style")
        if style in ("question", "kinetic", "invented"):
            used[style] += 1
            if i == 0 or used[style] > STYLE_CAPS[style]:
                sc["graphic"] = None
        if i and sc.get("transition") in SPECIAL_TRANSITIONS:
            used["special"] += 1
            if used["special"] > STYLE_CAPS["special"]:
                sc["transition"] = "fade"


def limit_full(scenes: list[dict], most: int) -> None:
    """Never scene 1 (real footage keeps the hook), never two in a row, never a scene too short to play it
    (FULL_MIN_WORDS), at most `most`; a kept one replaces that scene's overlay graphic and person card (one
    thing on screen at a time)."""
    kept, last, has_doc = 0, -2, False
    min_words = 6 if most > 2 else channel_profiles.FULL_MIN_WORDS
    for i, sc in enumerate(scenes):
        if not sc.get("full"):
            sc["full"] = None
        elif (i == 0 or i == last + 1 or kept >= most or len(sc["narration"].split()) < min_words
              or (most > 2 and sc["full"].get("type") == "document" and has_doc)):
            sc["full"] = None
        else:
            kept, last = kept + 1, i
            has_doc = has_doc or sc["full"].get("type") == "document"
            sc["graphic"] = sc["person"] = None
            sc["animate"] = False  # no AI clip for a scene nobody will see as a picture


MONEY_SCALE = {"hundred": 1e2, "thousand": 1e3, "million": 1e6, "billion": 1e9, "trillion": 1e12,
               "k": 1e3, "m": 1e6, "b": 1e9}
MONEY_RE = re.compile(
    r"\$(?P<num>\d[\d,]*(?:\.\d+)?)(?:[\s-]*(?P<scale>hundred|thousand|million|billion|trillion|[kmb])\b)?",
    re.I,
)
YEAR_RE = re.compile(r"\b(1[7-9]\d\d|20\d\d)\b")
STOP_LABELS = {
    "THE", "AND", "BUT", "FOR", "WITH", "FROM", "INTO", "OVER", "ONLY", "JUST", "EVEN", "STILL", "SENT", "PAID",
    "TOOK", "MADE", "LOST", "COST", "WERE", "WAS", "HAD", "HAS", "THAT", "THIS", "THEY", "THEM", "THEIR", "EACH",
    "MORE", "THAN", "NEARLY", "ABOUT", "AROUND", "ALMOST", "EVERY", "YEARLY",
}


def parse_scene_money(narration: str) -> tuple[float, str, str, str] | None:
    """Extract (numeric_value, compact_display, short_label, trigger_phrase) from a scene's dollar figure."""
    m = MONEY_RE.search(narration)
    if not m:
        return None
    base = float(m.group("num").replace(",", ""))
    scale = (m.group("scale") or "").lower()
    val = base * MONEY_SCALE.get(scale, 1.0)
    if not (0 < val < 1e12):
        return None
    suf = {"thousand": "K", "k": "K", "million": "M", "m": "M", "billion": "B", "b": "B", "trillion": "T"}.get(scale, "")
    if suf:
        show = f"${m.group('num')}{suf}"
    elif val >= 1e6 and val % 1e5 == 0:
        show = f"${val / 1e6:g}M"
    else:
        show = f"${int(val):,}" if val.is_integer() else f"${val:,.2f}"
    trigger = m.group(0).strip()
    yr = YEAR_RE.search(narration)
    if yr:
        label = yr.group(1)
    elif re.search(r"\byear\s+one\b", narration, re.I):
        label = "YEAR 1"
    else:
        after = [w.upper() for w in re.findall(r"[A-Za-z]+", narration[m.end():]) if len(w) > 2 and w.upper() not in STOP_LABELS]
        before = [w.upper() for w in re.findall(r"[A-Za-z]+", narration[:m.start()]) if len(w) > 2 and w.upper() not in STOP_LABELS]
        picks = (after[:2] or before[-2:] or ["TOTAL"])
        label = " ".join(picks)[:14]
    return (int(val) if val.is_integer() else val, show[:12], label, trigger)


def fill_money_graphics(scenes: list[dict]) -> None:
    """Ensure money beats in economics/finance Shorts don't go bare when the LLM omits a graphic or fact_check
    drops one: pair adjacent/nearby dollar scenes into a side-by-side `compare` bar chart, else a `stat` counter."""
    parsed = [parse_scene_money(sc.get("narration", "")) for sc in scenes]
    for i, sc in enumerate(scenes):
        if i == 0 or sc.get("graphic") or sc.get("full") or sc.get("person") or not parsed[i]:
            continue
        val, show, label, trigger = parsed[i]
        prev = next((j for j in range(i - 1, max(0, i - 4) - 1, -1) if parsed[j] and parsed[j][0] != val), None)
        if prev is not None:
            p_val, p_show, p_label, _ = parsed[prev]
            if p_label == label:
                p_label, label = "BEFORE", "AFTER"
            sc["graphic"] = {
                "style": "compare",
                "text": "THE NUMBERS",
                "a_label": p_label,
                "a_value": p_val,
                "a_show": p_show,
                "b_label": label,
                "b_value": val,
                "b_show": show,
                "trigger": trigger,
            }
        else:
            said_words = set(words_of(sc.get("narration", "")))
            sc["graphic"] = {
                "style": "stat",
                "value": val,
                "text": label if label != "TOTAL" else "DOLLARS",
                "trigger": trigger,
                **({"direction": "down"} if said_words & CRASH_WORDS else {}),
            }


SCENE_CONTEXT_WORDS = {
    "store", "stores", "interior", "exterior", "building", "crowd", "crowds", "floor", "aisle", "counter",
    "register", "turnstile", "street", "newspaper", "headline", "document", "contract", "letter", "map",
    "factory", "team", "game", "court", "arena", "stadium", "office", "exchange", "bank", "shop",
}


def is_person_portrait(cand: dict, person_name: str, catalog: list[dict] | None = None, cand_num: int | None = None) -> bool:
    """True when `cand` is a solo portrait/headshot of `person_name` (so a scene that pops up a PersonCard for
    `person_name` doesn't also use their portrait as the full-screen background behind the card)."""
    if not cand or cand.get("film") or not person_name:
        return False
    p_words = set(words_of(person_name))
    if not p_words:
        return False
    title_raw = re.sub(r"\.(jpe?g|png|tiff?|gif|svg|webm|ogv)$", "", cand.get("title", "").removeprefix("File:"), flags=re.I)
    title_words = set(words_of(title_raw))
    rem_words = set(words_of(re.sub(r"\blccn\w+|\b\d+\b", "", title_raw, flags=re.I))) - {
        "cropped", "bw", "retouched", "photo", "portrait", "headshot", "sir", "mr", "mrs", "dr", "jr", "sr",
    }
    what = next((str(e.get("what") or "") for e in (catalog or []) if isinstance(e, dict) and e.get("n") == cand_num), "")
    what_words = set(words_of(what))
    if not (p_words & (title_words | what_words)):
        return False
    if rem_words and rem_words <= p_words and not (what_words & SCENE_CONTEXT_WORDS):
        return True
    if ("portrait" in (title_words | what_words) or "headshot" in (title_words | what_words)) and not ((title_words | what_words) & SCENE_CONTEXT_WORDS):
        return True
    return False


def is_loop_short(scenes: list[dict]) -> bool:
    """True when the Short's final scene is an open grammatical loop bridge into scene 1 (either configured via
    channel rules or ending without sentence-closing punctuation)."""
    if not scenes:
        return False
    last = str(scenes[-1].get("narration") or "").strip()
    if not last:
        return False
    if not re.search(r"[.!?][\"')\]]*$", last):
        return True
    return "infinite loop" in (session.RULES.get("Story rules") or "").lower()


def mark_details(short: dict, choices: list[dict], work: Path) -> None:
    """Let Claude circle (or point an arrow at) a detail in up to 2 chosen pictures. It sees each
    picture under a lettered 10x10 grid and names the cell, which places the mark accurately. Only
    scenes with a picture and no other callout or person card qualify. Failure just means no marks."""
    folder = work / "marks"
    folder.mkdir(exist_ok=True)
    eligible = {}
    for i, (sc, c) in enumerate(zip(short["scenes"], choices)):
        if i and c["bg"] and not c.get("film") and not sc["graphic"] and not sc["person"] and not sc.get("full"):
            try:
                img = Image.open(io.BytesIO(c["bg"][0])).convert("RGB")
            except Exception:
                continue
            img.thumbnail((1000, 1000))
            d, font = ImageDraw.Draw(img), ImageFont.truetype(FONT, 26)
            for k in range(1, 10):
                x, y = img.width * k / 10, img.height * k / 10
                d.line((x, 0, x, img.height), fill=session.YELLOW, width=2)
                d.line((0, y, img.width, y), fill=session.YELLOW, width=2)
            for k in range(10):
                d.text((img.width * (k + 0.5) / 10 - 8, 4), "ABCDEFGHIJ"[k], font=font, fill=session.YELLOW, stroke_width=3, stroke_fill="black")
                d.text((6, img.height * (k + 0.5) / 10 - 14), str(k + 1), font=font, fill=session.YELLOW, stroke_width=3, stroke_fill="black")
            img.save(folder / f"scene{i + 1}.jpg", quality=90)
            eligible[i + 1] = sc
    if not eligible:
        return
    lines = "\n".join(f"scene {n}: {folder / f'scene{n}.jpg'} | narration: {sc['narration']}" for n, sc in eligible.items())
    data = llm.ask_ai(f"""You are the motion-graphics editor of a YouTube Short: "{short['title']}". Open and look at
these pictures; each has a 10x10 grid, columns A-J left to right, rows 1-10 top to bottom.
{lines}
For at most 2 scenes, choose ONE specific detail that the narration is about and a viewer could
miss (a face in a crowd, a sign, a crack, a small object), clearly visible in the picture. Give the
grid cell of its centre, shape "circle" (an object or face) or "arrow" (a spot in a wide view), and
a label of 1-3 words. If no picture has such a detail, reply with an empty list.
Reply with ONLY JSON: {{"marks": [{{"scene": 3, "cell": "D4", "shape": "circle", "label": "THE CRACK"}}]}}""",
                      fatal=False, read_dir=folder)
    for m in ((data or {}).get("marks") or [])[:2]:
        if not isinstance(m, dict):
            continue
        cell = re.fullmatch(r"([A-J])(10|[1-9])", str(m.get("cell", "")).strip().upper())
        sc = eligible.get(m.get("scene")) if cell else None
        label = str(m.get("label") or "").strip().upper()
        if sc and not sc["graphic"] and 0 < len(label.split()) <= 3:
            sc["graphic"] = {"style": "mark", "text": label[:24], "shape": "arrow" if m.get("shape") == "arrow" else "circle",
                             "x": ("ABCDEFGHIJ".index(cell[1]) + 0.5) / 10, "y": (int(cell[2]) - 0.5) / 10}


def fallback_graphic(g: dict) -> tuple[str, str]:
    """(style, text) for the built-in renderer, which draws only dates, places and fact boxes."""
    if g["style"] == "stat":
        num = f"{g['value']:,.0f}" if float(g["value"]).is_integer() else f"{g['value']:,.1f}"
        return "fact", f"{num}{' OF ' + str(g['of']) if 'of' in g else ''} {g['text']}"
    if g["style"] == "compare":
        return "fact", f"{g['a_label']} {g['a_show']} VS {g['b_label']} {g['b_show']}"
    if g["style"] == "quote":
        return "fact", f"\"{g['text']}\" - {g['by']}"
    return (g["style"] if g["style"] in ("date", "place", "fact") else "fact"), g["text"]


def words_of(text: str) -> list[str]:
    """Lowercase, accent-free word tokens, for matching names against spoken words."""
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", plain.lower())


def contains(words: list[str], phrase: list[str]) -> bool:
    return bool(phrase) and any(words[k:k + len(phrase)] == phrase for k in range(len(words)))


def spoken_span(words: list[tuple[float, float, str]], phrase: str) -> tuple[float, float] | None:
    """(start, end) of the first time `phrase` is spoken, from TTS word timings."""
    target, flat = words_of(phrase), []
    for start, end, text in words:  # a TTS "word" can hold punctuation or several tokens
        flat += [(start, end, tok) for tok in words_of(text)]
    toks = [tok for _, _, tok in flat]
    for k in range(len(toks)):
        if target and toks[k:k + len(target)] == target:
            return flat[k][0], flat[k + len(target) - 1][1]
    return None


def spoken_at(words: list[tuple[float, float, str]], phrase: str) -> float | None:
    """Start time of the first time `phrase` is spoken, from TTS word timings."""
    span = spoken_span(words, phrase)
    return span[0] if span else None


# Seconds a full-screen motion graphic's last beat needs before the cut: the AI-coded scene adds its own delay
# (Mike's "NO SYRINGE" stamp: beat + 0.35 s, ~0.5 s to land), then it should stay a moment (it showed 0.3 s, 2026-10-21).
FULL_SETTLE = 1.6


def full_cues(full: dict, words: list[tuple[float, float, str]], start: float, end: float) -> dict:
    """When each element of a full-screen motion graphic appears (absolute seconds): on its spoken `word`, else
    on an even slot inside the scene; board prints and map stops always appear in order, 0.4 s apart at least.
    The last beat comes FULL_SETTLE before the cut so it can finish and be seen; a late beat pulls the earlier ones
    forward with it (squeezed, order kept) instead of all piling up at the end."""
    lo = start + (0.4 if start else 0.0)  # scene 1 has no transition to wait out: its opener moves on frame 0
    hi = max(lo + 0.3, end - FULL_SETTLE)
    said = lambda w: (start + spoken_at(words, w)) if isinstance(w, str) and spoken_at(words, w) is not None else None  # noqa: E731

    def squeeze(ts: list[float]) -> list[float]:
        k = min(1.0, (hi - lo) / max(1e-6, ts[-1] - lo)) if ts else 1.0
        return [round(lo + (t - lo) * k, 3) for t in ts]

    if full["type"] in ("board", "journey"):
        parts = full["items" if full["type"] == "board" else "stops"]
        times, last = [], lo - 0.4
        for k, p in enumerate(parts):
            t = said(p.get("word"))
            t = lo + (hi - lo) * k / max(1, len(parts) - 1) * 0.85 if t is None else t
            last = max(t, last + 0.4)
            times.append(last)
        times = squeeze(times)
        cue = {"times": times}
        if full["type"] == "journey":
            cue["noteAt"] = round(min(hi, times[-1] + 0.4), 3)
        return cue
    if full["type"] == "custom":
        tokens = list(full.get("words") or []) or [p.get("word") for p in full.get("photos") or [] if isinstance(p, dict) and p.get("word")]
        n = max(3, len(tokens))
        cues, last = [], lo - 0.35
        for k in range(n):
            t = said(tokens[k]) if k < len(tokens) else None
            t = lo + (hi - lo) * k / max(1, n - 1) * 0.85 if t is None else t
            last = max(t, last + 0.35)
            cues.append(last)
        return {"cues": squeeze(cues)}
    if full["type"] == "number":
        t = said(full.get("word"))
        return {"at": round(min(hi, t if t is not None else lo), 3)}
    span = spoken_span(words, full["key_line"])
    if span:
        return {"at": round(start + span[0], 3), "lineEnd": round(start + span[1], 3)}
    t = said(full.get("word"))
    at = min(hi, t if t is not None else lo + 0.2)
    return {"at": round(at, 3), "lineEnd": round(at + 1.2, 3)}
