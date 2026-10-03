"""Small frame-by-frame animation engine (Pillow + ffmpeg) for 9:16 reels."""
import math
import subprocess
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

NAVY = (11, 37, 89)
BLUE = (31, 99, 216)
YELLOW = (255, 217, 61)
WHITE = (255, 255, 255)
GREEN = (46, 204, 113)
RED = (235, 77, 75)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, t0, d):
    return clamp((t - t0) / d)


def out_cubic(x):
    return 1 - (1 - x) ** 3


def in_out(x):
    return x * x * (3 - 2 * x)


def out_back(x, s=1.9):
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


@lru_cache(maxsize=None)
def font(size):
    return ImageFont.truetype(FONT, size)


def wrap(text, size, maxw):
    f = font(size)
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            test = (cur + " " + word).strip()
            if f.getlength(test) <= maxw or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


@lru_cache(maxsize=512)
def text_layer(text, size, fill, maxw=900, align="center", gap=1.12):
    lines = wrap(text, size, maxw)
    f = font(size)
    lh = int(size * gap)
    w = int(max(f.getlength(l) for l in lines)) + 8
    h = lh * len(lines) + 8
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        lw = f.getlength(l)
        x = {"center": (w - lw) / 2, "left": 4, "right": w - lw - 4}[align]
        d.text((x, i * lh + 2), l, font=f, fill=fill)
    return img


def paste(base, layer, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.003 or scale <= 0.003:
        return
    if scale != 1.0:
        layer = layer.resize(
            (max(1, int(layer.width * scale)), max(1, int(layer.height * scale))),
            Image.BILINEAR,
        )
    if rot:
        layer = layer.rotate(rot, expand=True, resample=Image.BILINEAR)
    if alpha < 1.0:
        layer = layer.copy()
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer.putalpha(a)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def text(base, s, size, cx, cy, fill=WHITE, maxw=900, scale=1.0, alpha=1.0, rot=0.0,
         align="center"):
    paste(base, text_layer(s, size, fill, maxw, align), cx, cy, scale, alpha, rot)


def shape_layer(draw_fn, w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(img))
    return img


def rrect(base, box, r, fill, alpha=1.0, outline=None, width=0):
    x0, y0, x1, y1 = [int(v) for v in box]
    layer = Image.new("RGBA", (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(
        (0, 0, x1 - x0 - 1, y1 - y0 - 1), r, fill=fill + (int(255 * alpha),) if fill else None,
        outline=outline, width=width)
    base.alpha_composite(layer, (x0, y0))


def circle(base, cx, cy, r, fill, alpha=1.0, outline=None, width=0):
    r = max(1, int(r))
    layer = Image.new("RGBA", (2 * r + 2, 2 * r + 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        (1, 1, 2 * r, 2 * r), fill=fill + (int(255 * alpha),) if fill else None,
        outline=outline, width=width)
    base.alpha_composite(layer, (int(cx - r - 1), int(cy - r - 1)))


def pill(base, s, size, x, y, bg, fg):
    """Left-aligned label pill whose top-left corner is (x, y). Returns right edge."""
    lay = text_layer(s, size, fg, 2000)
    w, h = lay.width + 50, lay.height + 22
    rrect(base, (x, y, x + w, y + h), h // 2, bg)
    base.alpha_composite(lay, (int(x + 25), int(y + 11)))
    return x + w


LABELS = ("10. SINIF BİYOLOJİ", "BİY.10.1.1")


def header(base, a=1.0, dark_text=False):
    x = pill(base, LABELS[0], 38, 70, 150, BLUE, WHITE)
    pill(base, LABELS[1], 38, x + 18, 150, YELLOW, NAVY)


def footer(base, color=WHITE):
    text(base, "@biyolojininrehberi", 38, W / 2, 1620, color, alpha=0.9)


def cta(base, top, alpha=1.0, scale=1.0, light=False):
    """Closing brand block: channel name + Instagram / YouTube / website."""
    h = 250
    layer = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    bgc, fg, accent = (NAVY, WHITE, YELLOW) if light else (YELLOW, NAVY, BLUE)
    rrect(layer, (60, 0, W - 60, h), 44, bgc)
    text(layer, "BİYOLOJİ REHBERİ", 66, W / 2, 58, accent if light else NAVY)
    text(layer, "Instagram  @biyolojininrehberi", 40, W / 2, 128, fg, maxw=940)
    text(layer, "YouTube  @BiyoRehber   •   biyolojirehberi.com", 38, W / 2, 188, fg, maxw=940)
    paste(base, layer, W / 2, top + h / 2, scale, alpha)


def vgradient(c0, c1):
    img = Image.new("RGB", (1, H))
    px = img.load()
    for y in range(H):
        k = y / (H - 1)
        px[0, y] = tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3))
    return img.resize((W, H)).convert("RGBA")


def render(scene, seconds, out):
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i",
         f"anullsrc=r=44100:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)
    n = int(seconds * FPS)
    for i in range(n):
        frame = scene(i / FPS)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()


def spin(cx, cy, r0, r1, n, ang):
    pts = []
    for i in range(n):
        a = ang + i * 2 * math.pi / n
        pts.append(((cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                    (cx + r1 * math.cos(a), cy + r1 * math.sin(a))))
    return pts
