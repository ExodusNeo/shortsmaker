"""Owner media imports, source settings and provenance. No credentials are bundled."""

import hashlib
import json
import os
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path

from shortsmaker import media_tools
from shortsmaker.config import ROOT


LIBRARY = ROOT / "media_library"
SETTINGS = ROOT / "media_sources.json"
STATUS = ROOT / "cache" / "source_status.json"
_status_lock = threading.Lock()
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".mkv", ".m4v"}


def settings() -> dict:
    try:
        data = json.loads(SETTINGS.read_text(encoding="utf-8-sig"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def source_enabled(name: str) -> bool:
    return settings().get("sources", {}).get(name, True) is not False


def optional_key(name: str) -> str:
    key = os.environ.get(f"SHORTSMAKER_{name.upper()}_KEY", "").strip()
    path = ROOT / f"{name.lower()}_key.txt"
    if not key and path.exists():
        key = path.read_text(encoding="utf-8-sig").strip()
    return key


def source_status(name: str, message: str) -> None:
    """One record per source, no URLs/exception messages that could contain credentials."""
    with _status_lock:
        try:
            data = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
            data[name] = {"status": message, "checked": time.strftime("%Y-%m-%d %H:%M:%S")}
            STATUS.parent.mkdir(parents=True, exist_ok=True)
            media_tools.write_json(STATUS, data)
        except (OSError, ValueError):
            pass


def import_media(path: Path, title: str, tags: str, source: str, credit: str) -> Path:
    """Copy into the library; never move/modify the owner's original. Sidecars also work for dropped files."""
    path = path.expanduser().resolve(strict=True)
    if path.suffix.lower() not in IMAGE_EXTS | VIDEO_EXTS:
        raise ValueError("Choose a picture or a video file.")
    folder = LIBRARY / ("videos" if path.suffix.lower() in VIDEO_EXTS else "images")
    folder.mkdir(parents=True, exist_ok=True)
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()[:12]
    slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")[:60] or "asset"
    out = folder / f"{slug}-{digest}{path.suffix.lower()}"
    if path != out:
        shutil.copy2(path, out)
    media_tools.write_json(out.with_suffix(out.suffix + ".json"),
                           {"title": title or path.stem, "tags": tags, "source_url": source,
                            "credit": credit or "Owner supplied; rights not specified", "crop": "preserve"})
    return out


def local_assets(query: str, video: bool = False, limit: int = 6) -> list[dict]:
    if not LIBRARY.exists():
        return []
    words = media_search_words(query) - {"photo", "video", "image", "footage", "commercial", "advertisement"}
    found = []
    for path in sorted(LIBRARY.rglob("*")):
        if path.suffix.lower() not in (VIDEO_EXTS if video else IMAGE_EXTS):
            continue
        try:
            meta = json.loads(path.with_suffix(path.suffix + ".json").read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            meta = {}
        text = " ".join((path.stem, str(meta.get("title", "")), str(meta.get("tags", ""))))
        overlap = words & media_search_words(text)
        if not overlap:
            continue
        credit = meta.get("credit") or "Owner supplied; rights not specified"
        if meta.get("source_url"):
            credit += f"; {meta['source_url']}"
        row = {"title": meta.get("title") or path.stem, "credit": credit, "site": "Local library",
               "source_page": meta.get("source_url"), "local_path": str(path), "crop": meta.get("crop", "preserve")}
        if video:
            try:
                dur = media_tools.duration(path)
            except (OSError, ValueError, subprocess.SubprocessError):
                continue
            row.update(src=str(path), dur=dur)
        else:
            row.update(url=path.as_uri(), small=path.as_uri(), source="Local library")
        found.append((len(overlap), row))
    return [row for _, row in sorted(found, key=lambda it: -it[0])[:limit]]


def media_search_words(text: str) -> set[str]:
    text = re.sub(r"(?<=\w)['’](?=\w)", "", text.lower())
    return set(re.findall(r"[a-z0-9]+", text))
