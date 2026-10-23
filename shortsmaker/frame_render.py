"""The Python renderer: camera moves, graphic overlays, person cards, clip reading, thumbnail."""

import io
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from shortsmaker import footage, image_sources, plan_rules, session
from shortsmaker.config import FONT, FPS, H, W, XFADE


def fills_frame(path: Path) -> bool:
    """True only when a video is already vertical (9:16-ish, 720p+); horizontal videos use FILM_VF
    (zoomed out over a blurred background) so subjects on the left/right are never cut off."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    try:
        w, h = (int(v) for v in out.strip().split(",")[:2])
    except ValueError:
        return False
    return h >= 720 and w < h


def shot(img: Image.Image, move: str, p: float) -> Image.Image:
    """One frame of slow Ken Burns motion; affine sampling is sub-pixel so it never shakes."""
    zmax = 1.12
    z = {"in": 1 + (zmax - 1) * p, "out": zmax - (zmax - 1) * p}.get(move, zmax)
    vw, vh = img.width / z, img.height / z
    cx, cy = img.width / 2, img.height / 2
    dx, dy = (img.width - vw) / 2, (img.height - vh) / 2
    cx += {"right": dx * (2 * p - 1), "left": dx * (1 - 2 * p)}.get(move, 0)
    cy += {"down": dy * (2 * p - 1), "up": dy * (1 - 2 * p)}.get(move, 0)
    s = vw / W
    return img.transform((W, H), Image.AFFINE, (s, 0, cx - vw / 2, 0, s, cy - vh / 2), Image.BICUBIC)


def fit_font(text: str, size: int, max_w: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(FONT, size)
    while font.getlength(text) > max_w and size > 30:
        size -= 6
        font = ImageFont.truetype(FONT, size)
    return font


def graphic_overlay(style: str, text: str) -> Image.Image:
    """Pre-render a callout as a small transparent image (animated per frame later)."""
    if style == "hook":  # title over the opening, up to two lines; also makes frame 0 thumbnail-ready
        words = text.upper().split()
        lines = [" ".join(words)]
        if len(words) > 1 and len(lines[0]) > 12:  # two lines, split where they're most even in length
            k = min(range(1, len(words)), key=lambda k: max(len(" ".join(words[:k])), len(" ".join(words[k:]))))
            lines = [" ".join(words[:k]), " ".join(words[k:])]
        font = fit_font(max(lines, key=len), 120, W - 140)
        img = Image.new("RGBA", (W, 150 * len(lines) + 40))
        d = ImageDraw.Draw(img)
        for k, line in enumerate(lines):
            d.text(((W - font.getlength(line)) / 2, 20 + k * 150), line, font=font, fill=session.YELLOW,
                   stroke_width=10, stroke_fill="black")
        return img
    if style == "cta":  # red subscribe button with a small line under it
        big, small = ImageFont.truetype(FONT, 80), ImageFont.truetype(FONT, 50)
        bw = int(big.getlength("SUBSCRIBE")) + 120
        img = Image.new("RGBA", (max(bw, int(small.getlength(text))) + 20, 200))
        d = ImageDraw.Draw(img)
        x = (img.width - bw) // 2
        d.rounded_rectangle((x, 0, x + bw, 120), radius=60, fill=(204, 0, 0, 255), outline="black", width=5)
        d.text((x + 60, 12), "SUBSCRIBE", font=big, fill="white")
        d.text(((img.width - small.getlength(text)) / 2, 130), text, font=small, fill="white",
               stroke_width=5, stroke_fill="black")
        return img
    if style == "date":  # big white year with a yellow underline
        font = fit_font(text, 170, W - 200)
        tw = int(font.getlength(text))
        img = Image.new("RGBA", (tw + 100, 290))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, tw + 100, 290), radius=36, fill=(0, 0, 0, 160))  # readable on any image
        d.text((50, 20), text, font=font, fill="white", stroke_width=8, stroke_fill="black")
        d.rounded_rectangle((50 + tw * 0.15, 242, 50 + tw * 0.85, 258), radius=8, fill=session.YELLOW)
        return img
    if style == "place":  # dark pill with a yellow map pin
        font = fit_font(text, 64, W - 300)
        tw = int(font.getlength(text))
        img = Image.new("RGBA", (tw + 150, 110))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, tw + 150, 110), radius=55, fill=(0, 0, 0, 185))
        d.ellipse((34, 22, 76, 64), fill=session.YELLOW)
        d.polygon([(38, 52), (72, 52), (55, 92)], fill=session.YELLOW)
        d.ellipse((47, 35, 63, 51), fill=(0, 0, 0, 185))
        d.text((100, 18), text, font=font, fill="white")
        return img
    font = fit_font(text, 84, W - 220)  # fact: black text on a yellow box
    tw = int(font.getlength(text))
    img = Image.new("RGBA", (tw + 80, 130))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, tw + 80, 130), radius=22, fill=session.YELLOW, outline="black", width=5)
    d.text((40, 16), text, font=font, fill="black")
    return img


def graphic_low(choice: dict, raw: Path, film: Path | None) -> bool:
    """True when the picture's subject would land under the top callouts (y ~180-680 of the frame):
    the callout then sits just above the captions instead, so it doesn't cover a face. Maps the photo
    editor's subject row through how the picture is framed: cover crop for photos, parallax, AI clips
    and widescreen film, or the whole film centred (FILM_VF)."""
    y = choice.get("subject_y")
    if y is None or not raw.exists():
        return False
    with Image.open(raw) as im:
        aspect = im.width / im.height
    if film and not fills_frame(film):
        fy = (H - footage.FILM_BAND) / 2 + y * footage.FILM_BAND  # FILM_VF: always a FILM_BAND-tall band, centred
    else:  # a wide picture keeps its full height; a tall one loses some top and bottom
        shown = min(1.0, aspect / (W / H))
        fy = ((y - 0.5) / shown + 0.5) * H
    return 180 <= fy <= 680


LOW_BOTTOM = 1110  # a lowered callout ends here, just above the captions (~1175-1300)


def draw_graphic(frame: Image.Image, style: str, ov: Image.Image, t: float, start: float, end: float,
                 low: bool = False) -> None:
    """Animate the callout in, hold it, fade it out before the scene ends."""
    if style == "hook":  # fully visible on the first frame, fades out by 1.8s
        k, dx, dy, scale = min(1.0, max(0.0, (1.8 - t) / 0.3)), 0, 0, 1.0
    else:
        t_in, t_out = start, end - 0.25  # start = when the callout appears
        if not t_in <= t <= t_out:
            return
        e = min(1.0, (t - t_in) / 0.35)
        e = 1 - (1 - e) ** 3  # ease-out
        k = e * min(1.0, (t_out - t) / 0.3)
        dx = -60 * (1 - e) if style == "place" else 0
        dy = -40 * (1 - e) if style == "date" else 40 * (1 - e) if style == "cta" else 0
        scale = 0.7 + 0.3 * e if style == "fact" else 1.0
    if k <= 0:
        return
    img = ov if scale == 1.0 else ov.resize((max(1, int(ov.width * scale)), max(1, int(ov.height * scale))))
    if k < 1:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * k)))
    # clear of YouTube's top icons and the captions; the subscribe button sits just under the captions
    top = LOW_BOTTOM - ov.height if low else {"hook": 220, "cta": 1330}.get(style, 300)
    frame.paste(img, (int((W - img.width) / 2 + dx), int(top + (ov.height - img.height) / 2 + dy)), img)


def person_card(data: bytes, name: str) -> Image.Image:
    """Tilted photo card with a white border, drop shadow and a yellow name banner."""
    photo = Image.open(io.BytesIO(data)).convert("RGB")
    pw, ph = 520, 624  # 5:6 portrait crop, biased to the top where faces usually are
    scale = max(pw / photo.width, ph / photo.height)
    photo = photo.resize((int(photo.width * scale) + 1, int(photo.height * scale) + 1), Image.LANCZOS)
    left, top = (photo.width - pw) // 2, int((photo.height - ph) * 0.2)
    photo = photo.crop((left, top, left + pw, top + ph))
    b, pad, banner = 12, 40, 96
    card = Image.new("RGBA", (pw + 2 * b + 2 * pad, ph + 2 * b + banner // 2 + 2 * pad))
    shadow = Image.new("RGBA", card.size)
    ImageDraw.Draw(shadow).rounded_rectangle((pad + 10, pad + 16, pad + pw + 2 * b + 10, pad + ph + 2 * b + 16),
                                             radius=30, fill=(0, 0, 0, 170))
    card.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((pad, pad, pad + pw + 2 * b, pad + ph + 2 * b), radius=30, fill="white")
    mask = Image.new("L", (pw, ph))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=22, fill=255)
    card.paste(photo, (pad + b, pad + b), mask)
    font = fit_font(name.upper(), 64, pw - 40)
    tw = font.getlength(name.upper())
    bx0, by0 = pad + b + (pw - tw) / 2 - 28, pad + ph + 2 * b - banner // 2
    d.rounded_rectangle((bx0, by0, bx0 + tw + 56, by0 + banner), radius=18, fill=session.YELLOW, outline="black", width=5)
    d.text((bx0 + 28, by0 + 12), name.upper(), font=font, fill="black")
    return card.rotate(-3, resample=Image.BICUBIC, expand=True)


def draw_card(frame: Image.Image, card: Image.Image, t: float, on: float, off: float) -> Image.Image:
    """Pop the card in with a slight overshoot over a dimmed background, then shrink it away."""
    if not on <= t <= off:
        return frame
    a = min(1.0, (t - on) / 0.3)
    c1 = 1.70158  # easeOutBack: overshoots ~6% then settles
    scale = 0.6 + 0.4 * (1 + (c1 + 1) * (a - 1) ** 3 + c1 * (a - 1) ** 2)
    alpha = min(1.0, a * 2)
    drop_y = 0
    if t > off - 0.32:  # exit: smooth sink and fade
        e = (off - t) / 0.32
        scale, alpha = scale * (0.75 + 0.25 * e), alpha * (e ** 1.5)
        drop_y = int(45 * (1 - e))
    frame = frame.point(lambda v: int(v * (1 - 0.35 * alpha)))  # dim the background
    img = card.resize((max(1, int(card.width * scale)), max(1, int(card.height * scale))), Image.BILINEAR)
    if alpha < 1:
        img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    frame.paste(img, ((W - img.width) // 2, 680 - img.height // 2 + drop_y), img)  # between top graphics and captions
    return frame


class ClipReader:
    """Streams a clip's frames in order. Decoding a whole 1080x1920 clip up front would hold GBs of
    RAM; the renderer only ever moves forward through a scene, so one pass is enough."""

    def __init__(self, path: Path):
        meta = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                               "-show_entries", "stream=width,height,nb_read_packets", "-of", "csv=p=0", str(path)],
                              capture_output=True, text=True).stdout.strip().split(",")
        self.w, self.h, self.n = (int(v) for v in meta[:3])
        self.proc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(path), "-f", "rawvideo",
                                      "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.pos, self.buf = -1, None

    def at(self, p: float) -> Image.Image | None:
        """Frame at fraction p (0..1) of the clip; p never goes backwards within a scene."""
        want, size = round(p * (self.n - 1)), self.w * self.h * 3
        while self.pos < want:
            chunk = self.proc.stdout.read(size)
            if len(chunk) < size:
                break
            self.buf, self.pos = chunk, self.pos + 1
        if self.buf is None:
            return None
        img = Image.frombytes("RGB", (self.w, self.h), self.buf)
        return img if img.size == (W, H) else img.resize((W, H), Image.BICUBIC)

    def close(self) -> None:
        self.proc.kill()


def frame_maker(images, scenes, hook_text, cta_line, bounds, cues, clips: dict[int, Path]):
    """Returns frame(i, t): scene i at time t with camera move and graphics applied.
    cues[i] holds the timed extras for scene i, e.g. "card" (+ "on"/"off"). Scenes in `clips` play
    their clip (AI motion or 2.5D parallax, made on the GPU) stretched over the whole scene,
    instead of the CPU Ken Burns move. Readers are opened lazily: at most two stream at a time."""
    overlays = [graphic_overlay(*plan_rules.fallback_graphic(sc["graphic"])) if sc["graphic"] else None for sc in scenes]
    hook = graphic_overlay("hook", hook_text) if hook_text else None
    cta = graphic_overlay("cta", cta_line)
    tags = [image_sources.credit_tag_image(sc["credit_tag"]) if sc.get("credit_tag") else None for sc in scenes]
    readers: dict[int, ClipReader] = {}

    def frame(i: int, t: float) -> Image.Image:
        start, end, cue = bounds[i], bounds[i + 1], cues[i]
        p = min(max((t - start + XFADE / 2) / (end - start + XFADE), 0), 1)
        img = None
        if i in clips:
            if i not in readers:
                for done in [k for k in readers if k < i - 1]:  # scenes behind us: free them
                    readers.pop(done).close()
                readers[i] = ClipReader(clips[i])
            img = readers[i].at(p)
        if img is None:
            img = shot(images[i], scenes[i]["move"], p)
        if overlays[i]:
            draw_graphic(img, scenes[i]["graphic"]["style"], overlays[i], t, cue["graphic"], end,
                         scenes[i]["graphic"].get("low", False))
        if i == 0 and hook:
            draw_graphic(img, "hook", hook, t, start, end)
        if cue.get("cta") is not None:
            draw_graphic(img, "cta", cta, t, cue["cta"], end)
        if cue.get("card"):
            img = draw_card(img, cue["card"], t, cue["on"], cue["off"])
        if tags[i] and t - start < image_sources.CREDIT_SECONDS and (cue.get("cta") is None or t < cue["cta"]):  # never under the subscribe line
            img.paste(tags[i], (36, image_sources.CREDIT_Y), tags[i])
        return img
    frame.close = lambda: [r.close() for r in readers.values()]  # type: ignore[attr-defined]
    return frame


def flash_alpha(t: float, cut: float) -> float:
    """White camera-flash curve: snaps up over the 2 frames before the cut, then decays (~0.4s)."""
    if cut - 0.07 <= t < cut:
        return 0.9 * (t - (cut - 0.07)) / 0.07
    return 0.9 * math.exp(-(t - cut) / 0.11) if cut <= t < cut + 0.5 else 0.0


def write_frames(frame, n: int, bounds: list[float], total: float, out, flashes: set[float],
                 cuts: set[float] = frozenset()) -> None:
    """Stream every frame to ffmpeg. Cuts in `flashes` are hard cuts under a white flash, those in `cuts` plain
    hard cuts; the others crossfade for XFADE seconds."""
    hard = flashes | cuts
    white = Image.new("RGB", (W, H), "white")
    for f in range(int(total * FPS)):
        t = f / FPS
        i = min(sum(1 for b in bounds[1:-1] if b <= t), n - 1)
        img = None
        if i + 1 < n and t >= bounds[i + 1] - XFADE / 2 and bounds[i + 1] not in hard:
            a, b, cut = i, i + 1, bounds[i + 1]
        elif i > 0 and t < bounds[i] + XFADE / 2 and bounds[i] not in hard:
            a, b, cut = i - 1, i, bounds[i]
        else:
            img = frame(i, t)
        if img is None:
            img = Image.blend(frame(a, t), frame(b, t), (t - (cut - XFADE / 2)) / XFADE)
        glare = max((flash_alpha(t, c) for c in flashes), default=0.0)
        out.write((Image.blend(img, white, glare) if glare else img).tobytes())


def thumbnail(image: Path, text: str, path: Path) -> None:
    img = Image.open(image).convert("RGB").resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    words, lines = text.upper().split(), []
    for w in words:  # two words per line
        if lines and len(lines[-1].split()) < 2:
            lines[-1] += " " + w
        else:
            lines.append(w)
    font = fit_font(max(lines, key=len), 190, W - 100)  # shrink long lines so nothing runs off the edge
    y = H * 0.30
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text(((W - tw) / 2, y), line, font=font, fill=(255, 221, 0),
                  stroke_width=12, stroke_fill=(0, 0, 0))
        y += font.size * 1.16
    img.save(path, quality=92)
