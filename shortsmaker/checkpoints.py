"""Atomic progress records for unfinished Shorts; no executable serialized state."""
import base64
import io
import json
from pathlib import Path

from PIL import Image

from shortsmaker import media_tools, session
from shortsmaker.config import OUTPUT


def pack(value):
    if isinstance(value, Image.Image):
        stream = io.BytesIO()
        value.save(stream, format="PNG")
        return {"_image_png": base64.b64encode(stream.getvalue()).decode("ascii")}
    if isinstance(value, bytes):
        return {"_bytes": base64.b64encode(value).decode("ascii")}
    if isinstance(value, Path):
        return {"_path": str(value)}
    if isinstance(value, (list, tuple, set)):
        return [pack(item) for item in value]
    if isinstance(value, dict):
        return {str(key): pack(item) for key, item in value.items()}
    return value


def unpack(value):
    if isinstance(value, list):
        return [unpack(item) for item in value]
    if isinstance(value, dict):
        if set(value) == {"_image_png"}:
            with Image.open(io.BytesIO(base64.b64decode(value["_image_png"], validate=True))) as picture:
                if picture.format != "PNG":
                    raise ValueError("Checkpoint image must be PNG")
                picture.load()
                return picture.copy()
        if set(value) == {"_bytes"}:
            return base64.b64decode(value["_bytes"])
        if set(value) == {"_path"}:
            return Path(value["_path"])
        return {key: unpack(item) for key, item in value.items()}
    return value


def read(path: Path):
    return unpack(json.loads(path.read_text(encoding="utf-8")))


def begin(folder: Path, short: dict, mode: str) -> None:
    work = folder / "work"
    work.mkdir(parents=True, exist_ok=True)
    path = work / "progress.json"
    if path.exists() and read(path).get("stage") != "complete":
        raise RuntimeError(f"Unfinished work already exists: {folder}. Use resume instead.")
    media_tools.write_json(path, pack({"stage": "scripted", "short": short, "mode": mode,
                                     "brain": session.BRAIN, "partner": session.PARTNER,
                                     "short_form": session.SHORT_FORM, "veo": session.VEO_HANDOFF}))


def update(work: Path, stage: str, short: dict | None = None, error: str | None = None) -> None:
    path = work / "progress.json"
    if not path.exists():
        return  # legacy renders and manual fixes do not create resumable batch entries
    job = read(path)
    if job["stage"] == "complete":
        return
    job.update(stage=stage, brain=session.BRAIN, partner=session.PARTNER)
    if short is not None:
        job["short"] = short
    job["error"] = error
    media_tools.write_json(path, pack(job))


def pending() -> list[Path]:
    folders = []
    for path in sorted(OUTPUT.glob("*/*/work/progress.json")):
        try:
            if read(path)["stage"] != "complete":
                folders.append(path.parent.parent)
        except (ValueError, OSError, KeyError):
            print(f"Could not read progress record; files preserved: {path}")
    return folders


def pending_topics(channel: str) -> list[str]:
    """Topics of this channel's unfinished Shorts: not in done_topics yet, but already being made."""
    topics = []
    for folder in pending():
        if folder.parent.name != channel:
            continue
        try:
            topic = read(folder / "work" / "progress.json")["short"].get("topic")
        except (ValueError, OSError, KeyError, AttributeError):
            continue
        if isinstance(topic, str) and topic.strip():
            topics.append(topic)
    return topics


def save_context(work: Path, context: dict) -> None:
    media_tools.write_json(work / "render-context.json", pack(context))


def context(work: Path) -> dict:
    data = read(work / "render-context.json")
    data["clips"] = {int(key): value for key, value in data["clips"].items()}
    data["emphasis"], data["flashes"] = set(data["emphasis"]), set(data["flashes"])
    return data
