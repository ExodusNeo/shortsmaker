"""Tests for the model library and the Blender MCP add-on link (blender_link.py, 2026-10-27). The add-on is faked by
a tiny socket server speaking its JSON protocol. No AI usage, no Blender. Run: .venv\\Scripts\\python.exe
tests\\test_blender_link.py"""
import json
import re
import socketserver
import sys
import tempfile
import threading
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shortsmaker import blender_link, config  # noqa: E402

HITS = [{"ID": "a1", "Title": "Tree Stump", "Creator": "Quaternius", "Licence": "CC0 1.0", "Tags": ["stump"]},
        {"ID": "b2", "Title": "Rooster", "Creator": "Poly by Google", "Licence": "CC-BY 3.0", "Tags": ["bird"]},
        {"ID": "c3", "Title": "Stump NC", "Creator": "someone", "Licence": "CC-BY-NC 4.0", "Tags": []}]


class Fake:
    """Answers the add-on's commands; `replies` maps a command to a function(params) -> reply dict."""
    def __init__(self):
        self.calls, self.replies = [], {}
        fake = self

        class Handler(socketserver.BaseRequestHandler):
            def handle(self):
                buf = b""
                while True:
                    chunk = self.request.recv(65536)
                    if not chunk:
                        return
                    buf += chunk
                    try:
                        cmd = json.loads(buf.decode("utf-8"))
                        break
                    except ValueError:
                        continue
                fake.calls.append(cmd)
                fn = fake.replies.get(cmd["type"])
                reply = fn(cmd.get("params", {})) if fn else {"status": "error", "message": f"Unknown command type: {cmd['type']}"}
                self.request.sendall(json.dumps(reply).encode("utf-8"))

        self.server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.port = self.server.server_address[1]

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


def ok(result):
    return {"status": "success", "result": result}


def with_fake(test):
    def run():
        fake, old_port, old_lib = Fake(), config.MCP_PORT, config.LIBRARY
        with tempfile.TemporaryDirectory() as d:
            config.MCP_PORT, config.LIBRARY = fake.port, Path(d) / "library"
            try:
                test(fake)
            finally:
                fake.stop()
                config.MCP_PORT, config.LIBRARY = old_port, old_lib
    run.__name__ = test.__name__
    return run


@with_fake
def test_ping_on_off(fake):
    fake.replies["ping"] = lambda p: ok({"pong": True})
    assert blender_link.ping()
    fake.stop()
    assert not blender_link.ping(timeout=0.5)


@with_fake
def test_search_filters_licences(fake):
    fake.replies["search_polypizza_models"] = lambda p: ok({"total": 3, "results": HITS})
    hits = blender_link.search("stump")
    assert [h["id"] for h in hits] == ["a1", "b2"], hits
    assert hits[0] == {"source": "polypizza", "id": "a1", "title": "Tree Stump", "author": "Quaternius",
                       "licence": "CC0 1.0", "tags": ["stump"]}


def _fetch_replies(fake, saved_marker="saved"):
    fake.replies["get_polypizza_status"] = lambda p: ok({"enabled": True, "message": "ready"})
    fake.replies["download_polypizza_model"] = lambda p: ok({"success": True, "imported_objects": ["Rooster_mesh"]})

    def execute(p):
        m = re.search(r"SAVE_PATH = r'(.+?)'", p["code"])
        if m:
            Path(m.group(1)).write_bytes(b"BLENDER-fake")
        return ok({"executed": True, "result": saved_marker})
    fake.replies["execute_code"] = execute


@with_fake
def test_fetch_saves_pair(fake):
    _fetch_replies(fake)
    hit = {"source": "polypizza", "id": "b2", "title": "Rooster", "author": "Poly by Google", "licence": "CC-BY 3.0",
           "tags": ["bird"]}
    blend, why = blender_link.fetch_model(hit, "rooster", 0.55)
    assert why is None and blend == config.LIBRARY / "polypizza_b2.blend" and blend.exists(), (blend, why)
    meta = json.loads(blend.with_suffix(".json").read_text(encoding="utf-8"))
    assert meta["title"] == "Rooster" and meta["author"] == "Poly by Google" and meta["licence"] == "CC-BY 3.0"
    assert meta["size_m"] == 0.55 and "rooster" in meta["tags"] and "poly.pizza/m/b2" in meta["attribution"]
    assert blender_link.credit(blend) == meta["attribution"]
    codes = [c["params"]["code"] for c in fake.calls if c["type"] == "execute_code"]
    assert any("sm_before" in c for c in codes), "fetched in the owner's scene: only the download's new objects"
    assert not any("scenes.new" in c or "window.scene =" in c for c in codes), "never a scene of ours (owner)"
    assert any("tempdir" in c and str(config.BLENDER_TMP) in c for c in codes), "downloads go through D:"
    cc0 = dict(hit, id="a1", licence="CC0 1.0", title="Tree Stump")
    blend0, _ = blender_link.fetch_model(cc0, "tree stump", 1.2)
    assert blender_link.credit(blend0) is None


@with_fake
def test_switched_off_reason(fake):
    fake.replies["get_polypizza_status"] = lambda p: ok({"enabled": False, "message": "Poly Pizza is disabled"})
    blend, why = blender_link.fetch_model({"source": "polypizza", "id": "b2", "title": "Rooster", "author": "x",
                                           "licence": "CC0 1.0", "tags": []}, "rooster", 0.5)
    assert blend is None and "switched off in Blender" in why, why
    assert not any(c["type"] == "download_polypizza_model" for c in fake.calls)


@with_fake
def test_download_error_cleans_up(fake):
    _fetch_replies(fake)
    fake.replies["download_polypizza_model"] = lambda p: ok({"error": "No Poly Pizza model found with ID 'zz'"})
    blend, why = blender_link.fetch_model({"source": "polypizza", "id": "zz", "title": "x", "author": "x",
                                           "licence": "CC0 1.0", "tags": []}, "thing", 1.0)
    assert blend is None and "No Poly Pizza model" in why
    last = [c["params"]["code"] for c in fake.calls if c["type"] == "execute_code"][-1]
    assert "sm_before" in last and "SAVE_PATH" not in last, "the download's objects are removed without saving"


@with_fake
def test_in_library(fake):
    _fetch_replies(fake)
    blender_link.fetch_model({"source": "polypizza", "id": "b2", "title": "Rooster", "author": "Poly by Google",
                              "licence": "CC-BY 3.0", "tags": ["bird"]}, "rooster", 0.55)
    assert blender_link.in_library("rooster") == config.LIBRARY / "polypizza_b2.blend"
    assert blender_link.in_library("Roosters") == config.LIBRARY / "polypizza_b2.blend"  # a plural still finds it
    assert blender_link.in_library("baboon") is None


if __name__ == "__main__":
    names = [n for n in sorted(globals()) if n.startswith("test_") and (len(sys.argv) < 2 or n in sys.argv[1:])]
    failed = 0
    for n in names:
        try:
            globals()[n]()
            print(f"PASS {n}")
        except Exception:
            failed += 1
            print(f"FAIL {n}")
            traceback.print_exc()
    print(f"{len(names) - failed}/{len(names)} passed")
    sys.exit(1 if failed else 0)
