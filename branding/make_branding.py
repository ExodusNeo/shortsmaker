"""Channel profile picture + banner for Archive Oddities, drawn like printed matter (no AI imagery).
Run with local_ai/.venv (has numpy):  local_ai\\.venv\\Scripts\\python.exe branding\\make_branding.py
Photos in branding/src are public-domain Wikimedia Commons files (see SOURCES)."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).parent
FONTS = HERE.parent / "remotion" / "public" / "fonts"
PAPER, INK, RED = (233, 223, 200), (27, 23, 18), (168, 38, 30)
rng = np.random.default_rng(7)

SOURCES = {  # file -> (Commons file, caption, crop box or None); unidentified sitters: not tied to any one Short
    "woman.jpg": ("Portrait, unidentified woman LCCN2016824726.jpg", "FILE No. 0047", (250, 230, 710, 830)),  # head and shoulders
    "pilot.jpg": ("Marian Wesołowski (pilot).png", "FILE No. 0112", None),
    "soldier.jpg": ("Unidentified young soldier in Confederate infantry uniform.jpg", "FILE No. 0390", None),
    "profile.jpg": ("Unidentified woman (39456u).jpg", "FILE No. 0521", (180, 150, 760, 910)),
}


def garamond(size: int, weight: str = "Bold") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONTS / "EBGaramond.ttf"), size)
    f.set_variation_by_name(weight)
    return f


def typewriter(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / "SpecialElite-Regular.ttf"), size)


def paper(w: int, h: int) -> Image.Image:
    """Cream stock: faint uneven tone, fine grain and a few fibres."""
    tone = Image.fromarray((rng.random((h // 160 + 2, w // 160 + 2)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    tone = (np.asarray(tone, np.float32) / 255 - 0.5) * 3
    grain = rng.normal(0, 4.5, (h, w))
    base = np.array(PAPER, np.float32)[None, None, :] + (tone + grain)[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(w * h // 9000):  # short fibres, a shade darker
        x, y = rng.integers(0, w), rng.integers(0, h)
        a, ln = rng.uniform(0, np.pi), rng.uniform(4, 14)
        c = tuple(int(v - rng.uniform(10, 22)) for v in PAPER)
        d.line([(x, y), (x + ln * np.cos(a), y + ln * np.sin(a))], fill=c, width=1)
    return img


def ink(base: Image.Image, mask: Image.Image, color: tuple, wear: float = 0.12, blur: float = 0.7) -> None:
    """Print `mask` onto `base` with uneven ink: speckled dropouts and soft edges, like letterpress."""
    m = np.asarray(mask.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255
    speck = Image.fromarray((rng.random((mask.height // 3 + 1, mask.width // 3 + 1)) * 255).astype(np.uint8))
    speck = np.asarray(speck.resize(mask.size, Image.BILINEAR), np.float32) / 255
    m *= np.clip((speck - wear) / 0.25, 0.35, 1.0) if wear else 1.0
    m *= rng.uniform(0.88, 1.0, m.shape)  # ink density varies pixel to pixel
    arr = np.asarray(base, np.float32)
    col = np.array(color, np.float32)[None, None, :]
    # ink multiplies into the paper instead of sitting on top of it
    arr = arr * (1 - m[..., None]) + (arr * col / 255) * m[..., None] * 0.25 + col * m[..., None] * 0.75
    base.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))


def tracked(text: str, font, spacing: int) -> int:
    return int(sum(font.getlength(c) for c in text) + spacing * (len(text) - 1))


def text_mask(size, xy, text, font, anchor="mm", spacing=0) -> Image.Image:
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    if spacing:  # tracked capitals: draw letter by letter
        total = sum(font.getlength(c) for c in text) + spacing * (len(text) - 1)
        x = xy[0] - total / 2 if anchor[0] == "m" else xy[0]
        for c in text:
            d.text((x, xy[1]), c, font=font, fill=255, anchor="l" + anchor[1])
            x += font.getlength(c) + spacing
    else:
        d.text(xy, text, font=font, fill=255, anchor=anchor)
    return m


def halftone(photo: Image.Image, w: int, h: int, cell: int = 5) -> Image.Image:
    """Crop to w x h and screen it into round dots (a newspaper halftone), dark ink on paper."""
    g = ImageOps.autocontrast(photo.convert("L"), cutoff=1)
    s = max(w / g.width, h / g.height)
    g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
    g = g.crop(((g.width - w) // 2, max(0, (g.height - h) // 4), (g.width - w) // 2 + w, max(0, (g.height - h) // 4) + h))
    g = Image.fromarray(np.clip((np.asarray(g, np.float32) - 128) * 1.15 + 128, 0, 255).astype(np.uint8))
    up = 4  # draw dots large, then shrink: smooth edges
    m = Image.new("L", (w * up, h * up), 0)
    d = ImageDraw.Draw(m)
    a = np.asarray(g, np.float32) / 255
    for y in range(0, h, cell):
        off = cell / 2 if (y // cell) % 2 else 0  # staggered rows, like a 45 degree screen
        for x in np.arange(-off, w, cell):
            xi, yi = int(min(w - 1, max(0, x + cell / 2))), min(h - 1, y + cell // 2)
            r = (1 - a[yi, xi]) ** 0.8 * cell * 0.72
            if r > 0.3:
                cx, cy = (x + cell / 2) * up, (y + cell / 2) * up
                d.ellipse([cx - r * up, cy - r * up, cx + r * up, cy + r * up], fill=255)
    return m.resize((w, h), Image.LANCZOS)


def stamp_ring(size: int, cx: int, cy: int, r_out: int, r_in: int, text: str, font) -> Image.Image:
    """Rubber-stamp ring with text around it, as a mask."""
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], fill=255)
    d.ellipse([cx - r_out + 10, cy - r_out + 10, cx + r_out - 10, cy + r_out - 10], fill=0)
    d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=255)
    d.ellipse([cx - r_in + 6, cy - r_in + 6, cx + r_in - 6, cy + r_in - 6], fill=0)
    r_text = (r_out - 10 + r_in) / 2
    step = 360 / len(text)
    for k, c in enumerate(text):  # one glyph per angle, rotated to face outward
        g = Image.new("L", (90, 90), 0)
        ImageDraw.Draw(g).text((45, 45), c, font=font, fill=255, anchor="mm")
        ang = -90 + k * step
        g = g.rotate(-(ang + 90), resample=Image.BICUBIC)
        x = cx + r_text * np.cos(np.radians(ang)) - 45
        y = cy + r_text * np.sin(np.radians(ang)) - 45
        m.paste(255, (int(x), int(y)), g)
    return m


def avatar(path: Path) -> None:
    S = 800
    img = paper(S, S)
    ink(img, stamp_ring(S, S // 2, S // 2, 330, 248, "ARCHIVE ODDITIES • TRUE STORIES • ", typewriter(44)), RED, wear=0.14)
    ink(img, text_mask((S, S), (S // 2, S // 2 + 6), "AO", garamond(290, "ExtraBold")), INK, wear=0.03)
    img.save(path, quality=95)


def banner(path: Path) -> None:
    W, H = 2560, 1440
    img = paper(W, H)
    cy = H // 2  # everything that matters sits in the middle 1546 x 423 (all devices show it)
    ink(img, text_mask((W, H), (W // 2, cy - 128), "CASE FILES FROM HISTORY", typewriter(40), spacing=6), INK, wear=0.15)
    size = 158  # shrink until the title fits the phone-safe width with room to spare
    while tracked("ARCHIVE ODDITIES", garamond(size), 10) > 1340:
        size -= 2
    ink(img, text_mask((W, H), (W // 2, cy - 18), "ARCHIVE ODDITIES", garamond(size, "Bold"), spacing=10), INK, wear=0.02)
    half = tracked("ARCHIVE ODDITIES", garamond(size), 10) // 2
    rules = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(rules)
    for y, t in ((cy + 72, 4), (cy + 82, 1)):  # thick-thin rule, like a newspaper masthead
        d.rectangle([W // 2 - half, y, W // 2 + half, y + t], fill=255)
    ink(img, rules, INK, wear=0.05, blur=0.4)
    ink(img, text_mask((W, H), (W // 2, cy + 132), "True stories from history that sound made up.", garamond(52, "Medium")), INK, wear=0.05)
    # photos on the outer edges: seen on desktop and TV, cropped away on phones
    pw, ph, gap = 190, 250, 34
    left = [("woman.jpg", 70), ("pilot.jpg", 70 + pw + gap)]
    right = [("soldier.jpg", W - 70 - 2 * pw - gap), ("profile.jpg", W - 70 - pw)]
    top = cy - ph // 2 - 24
    for name, x in left + right:
        frame = Image.new("L", (W, H), 0)
        ImageDraw.Draw(frame).rectangle([x - 3, top - 3, x + pw + 2, top + ph + 2], outline=255, width=2)
        ink(img, frame, INK, wear=0.0, blur=0.3)
        dots = Image.new("L", (W, H), 0)
        photo = Image.open(HERE / "src" / name)
        if SOURCES[name][2]:
            photo = photo.crop(SOURCES[name][2])
        dots.paste(halftone(photo, pw, ph), (x, top))
        ink(img, dots, INK, wear=0.0, blur=0.35)
        ink(img, text_mask((W, H), (x + pw // 2, top + ph + 30), SOURCES[name][1], typewriter(22)), INK, wear=0.15)
    img.save(path, quality=95)


if __name__ == "__main__":
    avatar(HERE / "profile_picture.jpg")
    banner(HERE / "banner.jpg")
    print("saved profile_picture.jpg and banner.jpg in", HERE)
