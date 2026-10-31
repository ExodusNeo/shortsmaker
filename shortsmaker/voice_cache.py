"""Reuse completed narration only when text, voice settings and source files still match."""
import hashlib
import json
import shutil
from pathlib import Path

from shortsmaker import gpu, media_tools, plan_rules


def signature(short: dict, ch: dict) -> str:
    ref = gpu.COSY_REF
    data = {"lines": [sc["narration"] for sc in short["scenes"]], "voice": ch.get("voice"),
            "local_voice": ch.get("local_voice"), "loop": plan_rules.is_loop_short(short["scenes"]),
            "cosy_speed": gpu.COSY_SPEED, "instruct": gpu.COSY_INSTRUCT, "qwen": gpu.QWEN_SPEAKER,
            "ref": str(ref), "ref_hash": hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else None,
            "version": 1}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def load(short: dict, ch: dict, work: Path):
    try:
        data = json.loads((work / "voice-cache.json").read_text())
        if data["signature"] != signature(short, ch) or len(data["items"]) != len(short["scenes"]):
            return None
        result = []
        for item in data["items"]:
            path = work / "voice-cache" / item["file"]
            if path.parent.resolve() != (work / "voice-cache").resolve() or not path.is_file() or not item["words"]:
                return None
            if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                return None
            result.append((path, [tuple(word) for word in item["words"]]))
        return result
    except (OSError, ValueError, KeyError, TypeError):
        return None


def save(short: dict, ch: dict, work: Path, voices: list) -> None:
    if not voices or not all(item and item[1] and Path(item[0]).is_file() for item in voices):
        return
    folder = work / "voice-cache"
    folder.mkdir(exist_ok=True)
    items = []
    for index, (path, words) in enumerate(voices):
        dest = folder / f"scene{index}{Path(path).suffix}"
        if Path(path).resolve() != dest.resolve():
            temp = dest.with_suffix(dest.suffix + ".tmp")
            shutil.copyfile(path, temp)
            temp.replace(dest)
        items.append({"file": dest.name, "words": words, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()})
    media_tools.write_json(work / "voice-cache.json", {"signature": signature(short, ch), "items": items})
