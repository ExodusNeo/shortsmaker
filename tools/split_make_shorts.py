"""One-off: split make_shorts.py into the shortsmaker package without changing any function.

Usage (from D:\\ShortsMaker, with the project venv):
    python tools/split_make_shorts.py split      write shortsmaker/*.py + the new make_shorts.py, then prove them
                                                 (refuses if shortsmaker/ exists; --force regenerates it from baseline)
    python tools/split_make_shorts.py tests      point the tests' `m.name` at the owning module
    python tools/split_make_shorts.py selftest   check the rewriter on a toy file

Every top-level statement moves unchanged except: a load of a name owned by another module becomes `module.name`
(names owned by `config` are imported by name instead), `global X` for a `session` name is dropped and `X = ...`
becomes `session.X = ...`, and config's ROOT climbs one more folder. Plan: docs/superpowers/plans/2026-10-21-split-make-shorts.md
"""
import ast
import builtins
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "shortsmaker"
BASELINE = "54a1d70"  # the commit with the original single-file make_shorts.py
TEST_FILES = ["test_full_scenes.py", "test_pictures_first.py", "test_style.py", "render_style.py"]

# Start line of each top-level statement in the original -> module (plan, Task 2).
RANGES = [(35, 150, "config"), (151, 291, "llm"), (292, 490, "channel_profiles"), (491, 518, "style_lab"),
          (519, 759, "writing"), (760, 808, "picture_pool"), (809, 1142, "writing"), (1143, 1506, "plan_rules"),
          (1507, 1577, "seo"), (1578, 1695, "image_sources"), (1696, 1715, "footage"), (1716, 1782, "image_sources"),
          (1783, 1833, "footage"), (1834, 1873, "image_sources"), (1874, 1942, "footage"),
          (1943, 1975, "image_sources"), (1976, 2068, "footage"), (2069, 2284, "picture_pool"),
          (2285, 2454, "picker"), (2455, 2462, "remotion_render"), (2463, 2487, "style_lab"), (2488, 2577, "picker"),
          (2578, 2656, "photo_prep"), (2657, 2931, "audio_mix"), (2932, 3215, "frame_render"), (3216, 3341, "review"),
          (3342, 3432, "audio_mix"), (3433, 3732, "motion"), (3733, 3986, "style_lab"), (3987, 4174, "remotion_render"),
          (4175, 4343, "editplan"), (4344, 4701, "gpu"), (4702, 5016, "short_render"), (5017, 5106, "logbook"),
          (5107, 5292, "cli")]
OVERRIDES = {"fetch": "media_tools", "write_json": "media_tools", "duration": "media_tools",
             "video_encoder": "media_tools", "ffmpeg": "media_tools", "clock": "media_tools",
             "TOPIC_BACKUPS": "picture_pool",
             "fills_frame": "frame_render", "MUSIC_LUFS": "audio_mix", "music_gain": "audio_mix",
             "_last_ov": "image_sources", "_ov_lock": "image_sources",
             "film_ffmpeg": "image_sources"}  # shares wm_get's private Wikimedia rate-limit clock (_last_wm)
CONTINUED = {151}  # BRAIN's trailing comment runs on over the next lines
LINE_OVERRIDES = {393: "config"}  # the PIL warning filter must run on import, like the other config side effects
SESSION = {"CHANNEL", "RESEARCH", "LOG", "YELLOW", "EMPHASIS", "BRAIN", "NO_QUOTA", "LAST_AI", "SHORT_FORM",
           "VEO_HANDOFF"}
DOCS = {
    "config": "Paths, fixed settings, palettes and the style/skin tables every module shares. Importing it puts the\n"
              "bundled ffmpeg on PATH and checks the palettes' caption contrast.",
    "session": "Settings that change during a run (who plans, quota-out agents, the channel's files, run.bat modes,\n"
               "this Short's accent colours). Always read and set them as `session.NAME`.",
    "llm": "Headless Claude Code / Gemini (agy) calls that return JSON, with automatic fallback when one fails or\n"
           "runs out of quota.",
    "channel_profiles": "Channel profiles (channels/<name>.json), the run.bat menus, and YouTube/trend research.",
    "writing": "Topics -> Wikipedia research -> writer -> editor -> director -> fact check.",
    "plan_rules": "Cleaning and validating the planner's JSON (graphics, full-screen scenes, styles) and word timings.",
    "seo": "Titles, descriptions and tags from YouTube autocomplete; the .srt captions file.",
    "image_sources": "Pictures from Wikimedia Commons, Openverse, NASA and the Internet Archive, with licences and\n"
                     "on-screen credits.",
    "footage": "Real film clips (Commons, Internet Archive, NASA, Pixabay) and their ffmpeg crops.",
    "picture_pool": "The pictures gathered for a topic before writing, their catalog, cache and contact sheets.",
    "picker": "Choosing each scene's picture, pictures for full-screen scenes, and rescue graphics.",
    "photo_prep": "Cleaning found photos: stereograph cards, scanner borders, vertical crops.",
    "audio_mix": "Voice, captions, sound effects, story sounds and music levels.",
    "frame_render": "The Python renderer: camera moves, graphic overlays, person cards, clip reading, thumbnail.",
    "review": "Automatic checks on a finished Short, the AI visual review and its fixes, the storyboard.",
    "motion": "Full-screen motion-graphic scenes and the AI-coded Custom scenes (with their look-and-fix check).",
    "style_lab": "The style library: invented looks, overlays and scene changes, candidates and the library menu.",
    "remotion_render": "Rendering a Short with Remotion (with the Python renderer as fallback), redraws, paper and ink.",
    "editplan": "edit_plan.txt (the timestamped edit list) and per-scene cue timing.",
    "gpu": "Local AI on the owner's GPU and helpers: ComfyUI/MOSS, VoiceStudio, Gemini images, LTX clips, Veo hand-off.",
    "short_render": "A Short's saved work state and `render()`, which turns a written Short into the finished video.",
    "logbook": "The owner's logbook and the Obsidian vault pages.",
    "cli": "Command-line entry: making a batch (`main`), fix.bat's one-scene re-render, `library`, `notes`.",
    "media_tools": "Small shared helpers: downloads, ffmpeg, video encoder choice, durations, JSON files, clock.",
}
FIXED_ROOT = ("ROOT = Path(__file__).parent", "ROOT = Path(__file__).parent.parent")
SCOPE_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)
COMPS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
BUILTINS = set(dir(builtins)) | {"__file__", "__name__"}


# ---- scopes -------------------------------------------------------------------------------------------------------

def stored_names(nodes) -> tuple[set[str], set[str]]:
    """(local names, names declared global) bound directly in a function body (not in nested scopes)."""
    local, glob, todo = set(), set(), list(nodes)
    while todo:
        n = todo.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            local.add(n.name)
            todo += n.decorator_list
            continue
        if isinstance(n, ast.Lambda):
            continue
        if isinstance(n, COMPS):  # a walrus inside a comprehension binds in the enclosing function
            local |= {w.target.id for w in ast.walk(n) if isinstance(w, ast.NamedExpr)}
            continue
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            local.add(n.id)
        elif isinstance(n, ast.Global):
            glob |= set(n.names)
        elif isinstance(n, ast.Nonlocal):
            local |= set(n.names)
        elif isinstance(n, ast.alias):
            local.add((n.asname or n.name).split(".")[0])
        elif isinstance(n, ast.ExceptHandler) and n.name:
            local.add(n.name)
        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name:
            local.add(n.name)
        elif isinstance(n, ast.MatchMapping) and n.rest:
            local.add(n.rest)
        todo += list(ast.iter_child_nodes(n))
    return local - glob, glob


def arg_names(a: ast.arguments) -> set[str]:
    names = {x.arg for x in a.posonlyargs + a.args + a.kwonlyargs}
    return names | {x.arg for x in (a.vararg, a.kwarg) if x}


def global_names(tree_nodes) -> list[ast.Name]:
    """Every Name node in `tree_nodes` (top-level statements) that refers to a module-level name."""
    out: list[ast.Name] = []

    def visit(n, scopes):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for x in n.decorator_list + n.args.defaults + [d for d in n.args.kw_defaults if d]:
                visit(x, scopes)
            for x in [a.annotation for a in n.args.posonlyargs + n.args.args + n.args.kwonlyargs
                      + [a for a in (n.args.vararg, n.args.kwarg) if a]] + [n.returns]:
                if x is not None:
                    visit(x, scopes)
            local, _ = stored_names(n.body)
            inner = [s for s in scopes if s[0] != "class"] + [("fn", local | arg_names(n.args))]
            for s in n.body:
                visit(s, inner)
            return
        if isinstance(n, ast.Lambda):
            for x in n.args.defaults + [d for d in n.args.kw_defaults if d]:
                visit(x, scopes)
            visit(n.body, [s for s in scopes if s[0] != "class"] + [("fn", arg_names(n.args))])
            return
        if isinstance(n, ast.ClassDef):
            for x in n.decorator_list + n.bases + [k.value for k in n.keywords]:
                visit(x, scopes)
            local, _ = stored_names(n.body)
            for s in n.body:
                visit(s, scopes + [("class", local)])
            return
        if isinstance(n, COMPS):
            gens = n.generators
            visit(gens[0].iter, scopes)
            local = {t.id for g in gens for t in ast.walk(g.target) if isinstance(t, ast.Name)}
            inner = scopes + [("fn", local)]
            for i, g in enumerate(gens):
                visit(g.target, inner)
                if i:
                    visit(g.iter, inner)
                for c in g.ifs:
                    visit(c, inner)
            for x in ([n.key, n.value] if isinstance(n, ast.DictComp) else [n.elt]):
                visit(x, inner)
            return
        if isinstance(n, ast.Name):
            if not any(n.id in names for _, names in scopes):
                out.append(n)
            return
        for c in ast.iter_child_nodes(n):
            visit(c, scopes)

    for s in tree_nodes:
        visit(s, [])
    return out


def defined_names(node) -> set[str]:
    """Top-level names a statement defines (def/class/assignment targets)."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
    names, todo = set(), list(targets)
    while todo:  # plain names and unpacking only: `X.attr = ...` / `X[k] = ...` define nothing
        t = todo.pop()
        if isinstance(t, ast.Name):
            names.add(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            todo += t.elts
        elif isinstance(t, ast.Starred):
            todo.append(t.value)
    return names


def is_main_guard(node) -> bool:
    return isinstance(node, ast.If) and "__main__" in ast.unparse(node.test)


# ---- splitting ----------------------------------------------------------------------------------------------------

def module_for(node, ranges, overrides, session, line_overrides) -> str:
    names = defined_names(node)
    if node.lineno in line_overrides:
        return line_overrides[node.lineno]
    if names & session:
        return "session"
    for name in names:
        if name in overrides:
            return overrides[name]
    for a, b, mod in ranges:
        if a <= node.lineno <= b:
            return mod
    raise SystemExit(f"line {node.lineno}: no module for {ast.unparse(node)[:60]!r}")


def chunks_of(src: str, tree: ast.Module, continued=frozenset()) -> list[tuple[ast.stmt, int, int]]:
    """(statement, first line, last line) with the comments above it. For a statement ending on a line in
    `continued`, the comment lines right under it finish its trailing comment and stay with it."""
    lines = src.splitlines()
    body = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))
            and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and n is tree.body[0])]
    out, prev_end = [], max((n.end_lineno for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))), default=0)
    for node in body:
        out.append([node, prev_end + 1, node.end_lineno])
        prev_end = node.end_lineno
    for i in range(len(out) - 1):
        node, a, end = out[i]
        if end in continued:
            nxt = end + 1
            while nxt < out[i + 1][0].lineno and lines[nxt - 1].lstrip().startswith("#"):
                nxt += 1
            out[i][2], out[i + 1][1] = nxt - 1, nxt
    return [tuple(c) for c in out]


def import_lines(tree: ast.Module) -> list[tuple[str, set[str], ast.stmt]]:
    """(source line, names it binds, node) for each top-level import, in order."""
    res = []
    for n in tree.body:
        if isinstance(n, ast.Import):
            for a in n.names:
                res.append((f"import {a.name}" + (f" as {a.asname}" if a.asname else ""),
                            {(a.asname or a.name).split(".")[0]}, n))
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                res.append((f"from {n.module} import {a.name}" + (f" as {a.asname}" if a.asname else ""),
                            {a.asname or a.name}, n))
    return res


def wrap_import(prefix: str, names: list[str]) -> str:
    line = prefix + ", ".join(names)
    if len(line) <= 120:
        return line
    out, cur = [prefix + "("], "    "
    for nm in names:
        piece = nm + ", "
        if len(cur) + len(piece) > 118:
            out.append(cur.rstrip())
            cur = "    "
        cur += piece
    out.append(cur.rstrip().rstrip(",") + ",")
    return "\n".join(out) + "\n)"


def split_source(src: str, ranges, overrides: dict, session: set, line_overrides: dict | None = None,
                 fix_root: bool = False, continued=frozenset()) -> dict[str, str]:
    """{module: source} for the package (see the module docstring for the rules)."""
    line_overrides = line_overrides or {}
    tree = ast.parse(src)
    chunks = [c for c in chunks_of(src, tree, continued) if not is_main_guard(c[0])]
    owner: dict[str, str] = {}
    mod_of: dict[int, str] = {}
    for node, _, _ in chunks:
        mod = mod_of[id(node)] = module_for(node, ranges, overrides, session, line_overrides)
        for name in defined_names(node):
            if name in owner and owner[name] != mod:
                raise SystemExit(f"{name} defined in both {owner[name]} and {mod}")
            owner[name] = mod
    imports = import_lines(tree)
    imported = set().union(*(b for _, b, _ in imports)) if imports else set()

    lines = [ln.encode("utf-8") for ln in src.splitlines(keepends=True)]
    edits: dict[int, list[tuple[int, int, bytes]]] = {}
    drop: set[int] = set()
    needs: dict[str, dict[str, set]] = {}
    for node, _, _ in chunks:
        cur = mod_of[id(node)]
        need = needs.setdefault(cur, {"mods": set(), "config": set(), "imports": set()})
        for name in global_names([node]):
            if name.id in imported:
                need["imports"].add(name.id)
            mod = owner.get(name.id)
            if mod is None or mod == cur:
                continue
            if not isinstance(name.ctx, ast.Load) and mod != "session":
                raise SystemExit(f"line {name.lineno}: {cur} assigns {mod}'s global {name.id}")
            if mod == "config" and isinstance(name.ctx, ast.Load):
                need["config"].add(name.id)
                continue
            need["mods"].add(mod)
            edits.setdefault(name.lineno, []).append(
                (name.col_offset, name.end_col_offset, f"{mod}.{name.id}".encode()))
        for g in (n for n in ast.walk(node) if isinstance(n, ast.Global)):
            keep = [x for x in g.names if owner.get(x) == cur]
            if keep == g.names:
                continue
            if g.lineno != g.end_lineno:
                raise SystemExit(f"line {g.lineno}: multi-line global")
            if keep:
                edits.setdefault(g.lineno, []).append((g.col_offset, g.end_col_offset, f"global {', '.join(keep)}".encode()))
            else:
                drop.add(g.lineno)
    for ln, eds in edits.items():
        b = lines[ln - 1]
        for a, e, rep in sorted(eds, reverse=True):
            b = b[:a] + rep + b[e:]
        lines[ln - 1] = b
    text = [None if i + 1 in drop else b.decode("utf-8") for i, b in enumerate(lines)]

    bodies: dict[str, list[str]] = {}
    prev_kind: dict[str, str] = {}
    for node, a, e in chunks:
        cur = mod_of[id(node)]
        piece = [t for t in text[a - 1:e] if t is not None]
        blanks = 0
        while piece and not piece[0].strip():
            piece.pop(0)
            blanks += 1
        kind = "def" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else "stmt"
        if cur not in bodies:
            blanks = 2
        elif kind == "def" or prev_kind[cur] == "def":
            blanks = max(blanks, 2)
        prev_kind[cur] = kind
        chunk = "".join(piece)
        if fix_root and chunk.startswith(FIXED_ROOT[0]):
            chunk = chunk.replace(FIXED_ROOT[0], FIXED_ROOT[1], 1)
        bodies.setdefault(cur, []).append("\n" * blanks + chunk)

    out = {}
    for mod, parts in bodies.items():
        need = needs[mod]
        head = [f'"""{DOCS.get(mod, mod)}"""']
        std, third = [], []
        for line, binds, n in imports:
            if not binds & need["imports"]:
                continue
            if line.startswith("import urllib."):  # `urllib` is bound by any of them: keep the ones this module uses
                if not re.search(rf"\b{re.escape(line[7:])}\b", "".join(parts)):
                    continue
            (third if line.split()[1].split(".")[0] in ("edge_tts", "PIL") else std).append((line, n))
        std_lines = merge_from([x for x in std])
        third_lines = merge_from([x for x in third])
        head += [("\n".join(std_lines))] if std_lines else []
        head += [("\n".join(third_lines))] if third_lines else []
        pkg = []
        if need["mods"]:
            pkg.append(wrap_import("from shortsmaker import ", sorted(need["mods"])))
        if need["config"]:
            pkg.append(wrap_import("from shortsmaker.config import ", sorted(need["config"])))
        head += ["\n".join(pkg)] if pkg else []
        out[mod] = "\n\n".join(head).rstrip() + "\n" + "".join(parts).rstrip() + "\n"
    return out


def merge_from(items) -> list[str]:
    """Import lines in original order, with `from x import a` lines of one statement joined back together."""
    res, seen = [], {}
    for line, node in items:
        if isinstance(node, ast.ImportFrom):
            if id(node) in seen:
                seen[id(node)].append(line.split(" import ", 1)[1])
                continue
            seen[id(node)] = [line.split(" import ", 1)[1]]
            res.append(("from", node))
        else:
            res.append((line, None))
    return [wrap_import(f"from {n.module} import ", seen[id(n)]) if kind == "from" else kind for kind, n in res]


# ---- proofs -------------------------------------------------------------------------------------------------------

class Unqualify(ast.NodeTransformer):
    """`module.name` -> `name` for package modules, and no `global` statements (applied to both sides)."""

    def __init__(self, mods):
        self.mods = mods

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name) and node.value.id in self.mods:
            return ast.copy_location(ast.Name(node.attr, node.ctx), node)
        return node

    def visit_Global(self, node):
        return None


def identifiers(tree) -> set[str]:
    ids = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            ids.add(n.id)
        elif isinstance(n, ast.arg):
            ids.add(n.arg)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            ids.add(n.name)
        elif isinstance(n, ast.alias):
            ids.add((n.asname or n.name).split(".")[0])
    return ids


def prove(src: str, mods: dict[str, str], ranges, overrides, session, line_overrides, test_sources=()) -> list[str]:
    """Problems found (empty = proven): names, clashes, undefined names, AST identity, import-time references."""
    problems = []
    tree = ast.parse(src)
    chunks = [c for c in chunks_of(src, tree) if not is_main_guard(c[0])]
    new = {m: ast.parse(s) for m, s in mods.items()}
    names = set(mods)

    original_names = set().union(*(defined_names(c[0]) for c in chunks))
    where: dict[str, list[str]] = {}
    for m, t in new.items():
        for n in t.body:
            for name in defined_names(n):
                where.setdefault(name, []).append(m)
    for name in original_names:
        if len(where.get(name, [])) != 1:
            problems.append(f"names: {name} is defined in {where.get(name, [])}")
    problems += [f"names: new name {n}" for n in set(where) - original_names]

    ids = identifiers(tree).union(*(identifiers(ast.parse(s)) for s in test_sources))
    problems += [f"clash: module name {m!r} is also an identifier" for m in sorted(names & ids)]

    for m, t in new.items():
        known = set(BUILTINS)
        for n in t.body:
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                known |= {(a.asname or a.name).split(".")[0] for a in n.names}
        known |= {x.id for n in t.body if not isinstance(n, SCOPE_NODES)
                  for x in ast.walk(n) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store)}
        known |= {n.name for n in t.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        for x in global_names(t.body):
            if x.id not in known:
                problems.append(f"undefined: {m}.py line {x.lineno}: {x.id}")
        for x in ast.walk(t):
            if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id in names:
                if x.attr not in {d for n in new[x.value.id].body for d in defined_names(n)}:
                    problems.append(f"undefined: {m}.py line {x.lineno}: {x.value.id}.{x.attr}")
        for n in t.body:  # code that runs on import may only lean on config (imported by name)
            parts = [n] if not isinstance(n, SCOPE_NODES) else (
                n.decorator_list + getattr(getattr(n, "args", None), "defaults", []) + (n.bases if isinstance(n, ast.ClassDef) else []))
            for p in parts:
                for x in ast.walk(p):
                    if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id in names:
                        problems.append(f"import-time: {m}.py line {x.lineno}: {x.value.id}.{x.attr}")

    norm = Unqualify(names)
    per_mod: dict[str, list] = {}
    for node, _, _ in chunks:
        per_mod.setdefault(module_for(node, ranges, overrides, session, line_overrides), []).append(node)
    for m, olds in per_mod.items():
        body = [n for n in new[m].body if not isinstance(n, (ast.Import, ast.ImportFrom))][1:]  # minus docstring
        if len(body) != len(olds):
            problems.append(f"identity: {m} has {len(body)} statements, expected {len(olds)}")
            continue
        for old, nw in zip(olds, body):
            if ast.unparse(old).startswith(FIXED_ROOT[0]):
                continue
            a = ast.dump(norm.visit(ast.parse(ast.unparse(old)).body[0]), include_attributes=False)
            b = ast.dump(norm.visit(ast.parse(ast.unparse(nw)).body[0]), include_attributes=False)
            if a != b:
                problems.append(f"identity: {m}: {sorted(defined_names(old)) or ast.unparse(old)[:50]} changed")
    return problems


# ---- commands -----------------------------------------------------------------------------------------------------

def original(path: str = "make_shorts.py") -> str:
    return subprocess.run(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def split() -> None:
    if PKG.exists() and "--force" not in sys.argv:  # the package is edited by hand after the split
        raise SystemExit(f"{PKG} already exists: re-splitting would overwrite every edit made since. "
                         "Pass --force only to regenerate it from the baseline on purpose.")
    src = original()
    mods = split_source(src, RANGES, OVERRIDES, SESSION, LINE_OVERRIDES, fix_root=True, continued=CONTINUED)
    tests = [original(f"tests/{f}") for f in TEST_FILES]  # as they were: the rewritten ones use the module names
    problems = prove(src, mods, RANGES, OVERRIDES, SESSION, LINE_OVERRIDES, tests)
    if problems:
        print("\n".join(problems))
        raise SystemExit(f"{len(problems)} problem(s); nothing written")
    PKG.mkdir(exist_ok=True)
    lf = {"encoding": "utf-8", "newline": "\n"}  # LF like the rest of the project (Windows would write CRLF)
    (PKG / "__init__.py").write_text('"""ShortsMaker: make ready-to-upload YouTube Shorts. Entry point: make_shorts.py."""\n',
                                     **lf)
    for m, s in mods.items():
        (PKG / f"{m}.py").write_text(s, **lf)
    doc = ast.get_docstring(ast.parse(src))
    (ROOT / "make_shorts.py").write_text(
        f'"""{doc}\n\nThe code lives in the shortsmaker/ package; this file is what run.bat, fix.bat and library.bat run.\n"""\n'
        "from shortsmaker.cli import main\n\nif __name__ == \"__main__\":\n    main()\n", **lf)
    for m in sorted(mods, key=lambda k: -len(mods[k].splitlines())):
        print(f"  {m + '.py':<22}{len(mods[m].splitlines()):>5} lines")
    print(f"proofs OK: {len(mods)} modules written")


def owners() -> dict[str, str]:
    owner = {}
    for f in PKG.glob("*.py"):
        for n in ast.parse(f.read_text(encoding="utf-8")).body:
            for name in defined_names(n):
                owner[name] = f.stem
    return owner


def rewrite_tests() -> None:
    """`m.name` -> `owner.name`; `m.subprocess` and other stdlib modules reached through m -> a plain import
    (patching `subprocess.run` patches the same module object). Writes nothing if any file has a problem."""
    owner, bad, out = owners(), [], {}
    stdlib = {b for _, binds, _ in import_lines(ast.parse(original())) for b in binds}
    for f in TEST_FILES:
        path = ROOT / "tests" / f
        s = path.read_text(encoding="utf-8")
        used, plain = set(), set()

        def sub(mt):
            name = mt.group(1)
            if name in owner:
                used.add(owner[name])
                return f"{owner[name]}.{name}"
            if name in stdlib:
                plain.add(name)
                return name
            bad.append(f"{f}: m.{name}")
            return mt.group(0)
        s = re.sub(r"(?<![\w.])m\.([A-Za-z_]\w*)", sub, s)
        s = s.replace("import make_shorts as m  # noqa: E402",
                      f"from shortsmaker import {', '.join(sorted(used))}  # noqa: E402", 1)
        extra = "".join(f"import {x}\n" for x in sorted(plain) if not re.search(rf"^import {x}$", s, re.M))
        s = s.replace("\nsys.path.insert(", f"\n{extra}sys.path.insert(", 1) if extra else s
        tree = ast.parse(s)
        local = {x.id for x in ast.walk(tree) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store)}
        local |= {x.arg for x in ast.walk(tree) if isinstance(x, ast.arg)}
        if used & local:
            bad.append(f"{f}: module names used as variables: {sorted(used & local)}")
        out[path] = s
        print(f"  {f}: {len(used)} modules{', plain imports: ' + ', '.join(sorted(plain)) if plain else ''}")
    if bad:
        raise SystemExit("\n".join(bad))
    for path, s in out.items():
        path.write_text(s, encoding="utf-8", newline="\n")


TOY = '''import json
from pathlib import Path

ROOT = Path(".")
LIMIT = 3
BRAIN = "claude"


def helper(x):
    return x + LIMIT


def ask():
    global BRAIN
    BRAIN = "gemini"
    return json.dumps(helper(1))


def user(helper=None):
    return ask(), helper


def shadow():
    ask = 1
    return [helper for helper in range(ask)]
'''


def selftest() -> None:
    mods = split_source(TOY, [(4, 10, "config"), (11, 17, "llm"), (18, 99, "writing")], {}, {"BRAIN"})
    assert set(mods) == {"config", "session", "llm", "writing"}, set(mods)
    assert 'BRAIN = "claude"' in mods["session"]
    assert "def helper(x):\n    return x + LIMIT" in mods["config"], mods["config"]
    llm = mods["llm"]
    assert "global" not in llm, llm
    assert 'session.BRAIN = "gemini"' in llm, llm
    assert "json.dumps(helper(1))" in llm and "from shortsmaker.config import helper" in llm, llm
    assert "from shortsmaker import session" in llm, llm
    assert "import json" in llm and "import json" not in mods["writing"], llm
    w = mods["writing"]
    assert "return llm.ask(), helper" in w, w  # the parameter `helper` shadows config.helper and stays bare
    assert "    ask = 1\n    return [helper for helper in range(ask)]" in w, w  # locals and comprehension vars too
    problems = prove(TOY, mods, [(4, 10, "config"), (11, 17, "llm"), (18, 99, "writing")], {}, {"BRAIN"}, {})
    assert problems == [], problems
    broken = dict(mods, writing=mods["writing"].replace("llm.ask()", "llm.asked()"))
    assert any("undefined" in p for p in prove(TOY, broken, [(4, 10, "config"), (11, 17, "llm"), (18, 99, "writing")],
                                                {}, {"BRAIN"}, {})), "a broken reference must be caught"
    global PKG
    saved, PKG = PKG, Path(__file__)  # an existing path: the package is already there
    try:
        split()
        raise AssertionError("split must refuse to overwrite an existing shortsmaker/")
    except SystemExit as e:
        assert "already exists" in str(e), e
    finally:
        PKG = saved
    print("selftest OK")


if __name__ == "__main__":
    {"split": split, "tests": rewrite_tests, "selftest": selftest}[sys.argv[1]]()
