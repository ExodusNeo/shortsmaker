"""The opener model library and the link to the owner's live Blender (2026-10-27). Models are searched and
downloaded through the Blender MCP add-on (it holds the Poly Pizza key) over its local socket, in a temporary scene
so the owner's open scene is never touched, and saved as <source>_<id>.blend + .json in config.LIBRARY, so later
runs reuse them without Blender. Only CC0 and CC-BY models are used; CC-BY ones are credited in upload.txt.
Poly Pizza only: Poly Haven's photo-real scans would clash with the low-poly opener look."""

import json
import re
import socket
from pathlib import Path

from shortsmaker import config



class LinkError(RuntimeError):
    """The add-on isn't reachable or answered with an error."""


def call(cmd: str, params: dict | None = None, timeout: float = 120) -> dict:
    """One add-on command; its result. A transport problem or an error reply raises LinkError."""
    try:
        with socket.create_connection(("127.0.0.1", config.MCP_PORT), timeout=timeout) as s:
            s.sendall(json.dumps({"type": cmd, "params": params or {}}).encode("utf-8"))
            buf = b""
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    raise LinkError(f"Blender closed the connection during {cmd}")
                buf += chunk
                try:
                    reply = json.loads(buf.decode("utf-8"))
                    break
                except ValueError:  # a reply split over several packets
                    continue
    except OSError as e:
        raise LinkError(f"Blender MCP isn't reachable ({e})") from e
    if not isinstance(reply, dict) or reply.get("status") != "success":
        raise LinkError(str(reply.get("message") if isinstance(reply, dict) else reply))
    result = reply.get("result")
    if isinstance(result, dict) and result.get("error"):
        raise LinkError(str(result["error"]))
    return result if isinstance(result, dict) else {"result": result}


def ping(timeout: float = 2.0) -> bool:
    try:
        call("ping", timeout=timeout)
        return True
    except LinkError:
        return False


def allowed_licence(licence: str) -> bool:
    """CC0, or plain CC-BY (no NC, ND or SA): free to use in a monetised Short with a credit at most."""
    up = str(licence or "").upper()
    return "CC0" in up or (re.search(r"\bCC[- ]BY\b", up) is not None and not re.search(r"\b(NC|ND|SA)\b", up))


def search(find: str) -> list[dict]:
    """Poly Pizza models for `find` that we may use."""
    data = call("search_polypizza_models", {"query": find, "limit": 20})
    return [{"source": "polypizza", "id": str(m.get("ID")), "title": str(m.get("Title") or ""),
             "author": str(m.get("Creator") or ""), "licence": str(m.get("Licence") or ""), "tags": list(m.get("Tags") or [])}
            for m in data.get("results") or [] if isinstance(m, dict) and m.get("ID") and allowed_licence(m.get("Licence"))]


def words(text: str) -> set[str]:
    """Lower-case words with a plural 's' dropped, so "Roosters" finds "Rooster"."""
    return {w[:-1] if len(w) > 3 and w.endswith("s") else w for w in re.findall(r"[a-z0-9]+", str(text).lower())}


def in_library(find: str) -> Path | None:
    """A saved model whose title and tags hold every word of `find` (the closest title wins), else None."""
    want, best = words(find), None
    if not want or not config.LIBRARY.exists():
        return None
    for meta_path in sorted(config.LIBRARY.glob("*.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        have = words(meta.get("title", "")) | {w for t in meta.get("tags", []) for w in words(t)}
        blend = meta_path.with_suffix(".blend")
        if want <= have and blend.exists():
            extra = len(words(meta.get("title", "")) - want)  # "Tree Stump" beats "Tree Stump with Moss"
            if best is None or extra < best[0]:
                best = (extra, blend)
    return best[1] if best else None


def attribution(hit: dict) -> str:
    return (f'"{hit["title"]}" by {hit["author"]}, https://poly.pizza/m/{hit["id"]}. Licence: {hit["licence"]}')


def credit(blend: Path) -> str | None:
    """The upload.txt credit a saved model needs: its attribution when CC-BY, None for CC0."""
    meta = json.loads(blend.with_suffix(".json").read_text(encoding="utf-8"))
    return None if "CC0" in meta.get("licence", "").upper() else meta.get("attribution")


# Fetched in the owner's own scene, never a scene of ours (owner, 2026-10-28: a new scene meant starting the MCP
# again): the objects that were there before are noted, the download's new ones saved and removed, nothing else
# touched. The add-on's commands also only exist while a scene with its switches on is current.
SETUP = """import bpy, tempfile
tempfile.tempdir = r'{tmp}'
bpy.app.driver_namespace['sm_before'] = set(bpy.data.objects.keys())
print('ready')
"""

FINISH = """import bpy
before = bpy.app.driver_namespace.pop('sm_before', None)
objs = [o for o in bpy.data.objects if before is not None and o.name not in before]  # unknown before: touch nothing
{save}
for o in objs:
    bpy.data.objects.remove(o, do_unlink=True)
print('saved', len(objs))
"""

SAVE = "SAVE_PATH = r'{path}'\nbpy.data.libraries.write(SAVE_PATH, set(objs), fake_user=True)"


def fetch_model(hit: dict, find: str, size_m: float) -> tuple[Path | None, str | None]:
    """Download `hit` through the owner's Blender into the library: (the .blend, None), or (None, why not)."""
    try:
        status = call("get_polypizza_status")
        if not status.get("enabled"):
            return None, f"Poly Pizza is switched off in Blender ({status.get('message', '')})"
        config.BLENDER_TMP.mkdir(parents=True, exist_ok=True)
        config.LIBRARY.mkdir(parents=True, exist_ok=True)
        call("execute_code", {"code": SETUP.format(tmp=config.BLENDER_TMP)})
    except LinkError as e:
        return None, str(e)
    blend = config.LIBRARY / f"{hit['source']}_{hit['id']}.blend"
    try:
        call("download_polypizza_model", {"model_id": hit["id"], "normalize_size": True, "target_size": size_m}, timeout=300)
    except LinkError as e:
        try:
            call("execute_code", {"code": FINISH.format(save="")})  # remove the temporary scene, save nothing
        except LinkError:
            pass
        return None, str(e)
    try:
        call("execute_code", {"code": FINISH.format(save=SAVE.format(path=blend))})
    except LinkError as e:
        return None, str(e)
    if not blend.exists():
        return None, f"Blender saved nothing for {hit['title']}"
    meta = {"source": hit["source"], "id": hit["id"], "title": hit["title"], "author": hit["author"],
            "licence": hit["licence"], "attribution": attribution(hit), "size_m": size_m,
            "tags": sorted(words(find) | {w for t in hit.get("tags", []) for w in words(t)})}
    blend.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return blend, None
