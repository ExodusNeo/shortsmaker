"""Cleaning found photos: stereograph cards, scanner borders, vertical crops."""

import io
import statistics
from pathlib import Path

from PIL import Image, ImageOps

from shortsmaker.config import H, SRC, W


def is_stereo(img: Image.Image) -> bool:
    """A stereograph card: two near-identical photos side by side. Compares the halves' photo areas
    (right one shifted up to 10%, since mounts are off-centre) after removing each row's average, so
    any landscape's shared sky-over-ground doesn't count. Tested 2026-10-15: a real card scored 0.52,
    wide photos, a card grid and drone footage 0.1 or less."""
    if not 1.6 <= img.width / img.height <= 2.4:
        return False
    half, n = img.width // 2, 48

    def detail(x0: int) -> list[float]:
        b = img.crop((x0 + int(half * 0.04), int(img.height * 0.06), x0 + int(half * 0.97),
                      int(img.height * 0.84))).convert("L").resize((n, n)).tobytes()
        return [v - sum(b[y * n:(y + 1) * n]) / n for y in range(n) for v in b[y * n:(y + 1) * n]]

    left, best = detail(0), -1.0
    for d in range(-half // 10, half // 10 + 1, max(1, half // 100)):
        try:
            best = max(best, statistics.correlation(left, detail(half + d)))
        except statistics.StatisticsError:  # a blank half
            pass
    return best > 0.4


def trim_borders(img: Image.Image) -> Image.Image:
    """Cut plain strips (white mounts, black plate edges) off the sides, at most 15% per side.
    shortcut: a plain sky or wall touching the edge can lose up to 15% too; harmless once cover-cropped."""
    g = img.convert("L")
    g.thumbnail((400, 400))
    box = [0, 0, g.width, g.height]  # left, top, right, bottom in thumbnail pixels

    def plain(b: tuple) -> bool:  # 90% one flat tone: lets a line through dust, lettering or a crossing strip
        px = sorted(g.crop(b).tobytes())
        mid = px[len(px) // 2]
        return sum(abs(v - mid) <= 16 for v in px) >= 0.9 * len(px)

    def border(line) -> bool:  # plain, or one of up to 3 soft edge lines just before more plain border
        return any(plain(line(k)) for k in range(4))

    changed = True
    while changed:  # borders nest (black frame, then a white strip): repeat until nothing more is plain
        changed = False
        l, t, r, b = box
        if l < g.width * 0.15 and border(lambda k: (l + k, t, l + k + 1, b)):
            box[0], changed = l + 1, True
        if r > g.width * 0.85 and border(lambda k: (r - k - 1, t, r - k, b)):
            box[2], changed = r - 1, True
        if t < g.height * 0.15 and border(lambda k: (l, t + k, r, t + k + 1)):
            box[1], changed = t + 1, True
        if b > g.height * 0.85 and border(lambda k: (l, b - k - 1, r, b - k)):
            box[3], changed = b - 1, True
    sx, sy = img.width / g.width, img.height / g.height
    return img.crop((round(box[0] * sx), round(box[1] * sy), round(box[2] * sx), round(box[3] * sy)))


def clean_photo(data: bytes) -> bytes:
    """Archive scans look broken on screen with their extras: a stereograph card keeps only its left
    photo, and plain borders are cut off. Returns the original bytes when there's nothing to fix."""
    img = Image.open(io.BytesIO(data)).convert("RGB")
    size = img.size
    if is_stereo(img):
        img = img.crop((0, 0, img.width // 2, img.height))
        # shortcut: fixed box for the standard card layout (mount around, caption below the photo);
        # upgrade to detecting the photo's edge if odd cards slip through
        img = img.crop((int(img.width * 0.22), int(img.height * 0.12), int(img.width * 0.97), int(img.height * 0.84)))
    img = trim_borders(img)
    if img.size == size:
        return data
    out = io.BytesIO()
    img.save(out, "JPEG", quality=95)
    return out.getvalue()


def to_vertical(path: Path) -> None:
    """Fill the 9:16 frame with the picture (centre crop) for the slow zoom/pan. This was the 2.5D parallax
    clip's full-screen framing; parallax itself was dropped (2026-10-16) because its depth warp bent paintings."""
    img = Image.open(path).convert("RGB")
    ImageOps.fit(img, (int(W * SRC), int(H * SRC)), Image.LANCZOS).save(path, quality=95)
