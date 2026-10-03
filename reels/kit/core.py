"""Shared building blocks for the one-reel-per-kazanım series.

Palettes (light/bright – no dark backgrounds), animated backgrounds, kinetic hook
text, 11 scene transitions and the closing brand block.
"""
import math
import random
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw  # noqa: E402

from engine import (W, H, FPS, NAVY, BLUE, YELLOW, WHITE, GREEN, RED, clamp, prog, out_cubic,  # noqa: E402,F401
                    in_out, out_back, font, text_layer, paste, text, rrect, circle, pill,
                    vgradient, render)

ORANGE = (245, 140, 40)


def out_bounce(x):
    x = clamp(x)
    if x < 1 / 2.75:
        return 7.5625 * x * x
    if x < 2 / 2.75:
        x -= 1.5 / 2.75
        return 7.5625 * x * x + 0.75
    if x < 2.5 / 2.75:
        x -= 2.25 / 2.75
        return 7.5625 * x * x + 0.9375
    x -= 2.625 / 2.75
    return 7.5625 * x * x + 0.984375


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def on(c):
    """Readable text colour for a filled background colour."""
    return NAVY if lum(c) > 150 else WHITE


def lerp(a, b, k):
    return a + (b - a) * k


def lerp_c(a, b, k):
    return tuple(int(lerp(a[i], b[i], k)) for i in range(3))


def interp(seq, pos):
    """Piecewise-linear lookup in a list at a float index."""
    pos = clamp(pos, 0, len(seq) - 1)
    i = int(pos)
    j = min(len(seq) - 1, i + 1)
    k = pos - i
    if isinstance(seq[i], (tuple, list)):
        return lerp_c(seq[i], seq[j], k)
    return lerp(seq[i], seq[j], k)


# ----------------------------------------------------------------- palettes
PALS = {
    "sky":   dict(bg=((218, 236, 255), (250, 253, 255)), ink=NAVY, acc=BLUE, acc2=YELLOW, sat=False),
    "sun":   dict(bg=((255, 238, 186), (255, 251, 232)), ink=NAVY, acc=(232, 112, 20), acc2=BLUE, sat=False),
    "mint":  dict(bg=((200, 244, 226), (240, 255, 248)), ink=NAVY, acc=(14, 150, 110), acc2=YELLOW, sat=False),
    "peach": dict(bg=((255, 222, 206), (255, 244, 236)), ink=NAVY, acc=(226, 86, 48), acc2=BLUE, sat=False),
    "lav":   dict(bg=((228, 220, 255), (247, 244, 255)), ink=NAVY, acc=(112, 78, 224), acc2=YELLOW, sat=False),
    "rose":  dict(bg=((255, 216, 232), (255, 243, 248)), ink=NAVY, acc=(216, 44, 104), acc2=BLUE, sat=False),
    "lime":  dict(bg=((226, 247, 186), (246, 253, 226)), ink=NAVY, acc=(86, 150, 8), acc2=ORANGE, sat=False),
    "aqua":  dict(bg=((196, 241, 246), (234, 252, 253)), ink=NAVY, acc=(8, 140, 162), acc2=YELLOW, sat=False),
    "ocean": dict(bg=((38, 120, 235), (104, 182, 255)), ink=WHITE, acc=YELLOW, acc2=WHITE, sat=True),
    "coral": dict(bg=((255, 100, 86), (255, 156, 112)), ink=WHITE, acc=YELLOW, acc2=WHITE, sat=True),
    "sunny": dict(bg=((255, 212, 56), (255, 235, 128)), ink=NAVY, acc=BLUE, acc2=WHITE, sat=False),
    "grape": dict(bg=((146, 100, 248), (192, 154, 255)), ink=WHITE, acc=YELLOW, acc2=WHITE, sat=True),
    "leaf":  dict(bg=((44, 186, 116), (118, 228, 164)), ink=WHITE, acc=YELLOW, acc2=WHITE, sat=True),
}

BGS = ["circles", "dots", "stripes", "bubbles", "waves", "blobs", "rays", "grid"]
HFX = ["pop", "slide", "drop", "type", "zoom", "spin", "stretch"]
TRS = ["wipe_r", "iris", "blinds", "push_u", "diag", "zoom", "circles", "wipe_u", "flash", "push_l", "wipe_l"]
CFX = ["rise", "pop", "flip", "slide"]


@lru_cache(maxsize=32)
def _grad(c0, c1):
    return vgradient(c0, c1)


def bg(pal, kind, g):
    img = _grad(*pal["bg"]).copy()
    tint = WHITE if pal["sat"] else pal["acc"]
    a = 38 if pal["sat"] else 30
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = tint + (a,)
    if kind == "circles":
        for k in range(6):
            x = (k * 270 + g * 40 * (1 if k % 2 else -1)) % (W + 400) - 200
            r = 140 + 24 * math.sin(g + k)
            y = 250 + k * 290
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    elif kind == "dots":
        for ix in range(13):
            for iy in range(23):
                r = 5 + 5 * math.sin(g * 2 + ix * .6 + iy * .5)
                x, y = ix * 90 + 20, iy * 90 + 10
                d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    elif kind == "stripes":
        off = (g * 60) % 280
        for k in range(-4, 9):
            x0 = k * 280 + off
            d.polygon([(x0, 0), (x0 + 120, 0), (x0 + 120 - 700, H), (x0 - 700, H)], fill=col)
    elif kind == "bubbles":
        for k in range(11):
            x = (k * 137 + 60) % W + 24 * math.sin(g + k)
            y = H + 100 - ((g * 70 + k * 210) % (H + 220))
            r = 24 + (k % 4) * 20
            d.ellipse((x - r, y - r, x + r, y + r), outline=tint + (a + 30,), width=6)
    elif kind == "waves":
        for j, (yb, amp, sp) in enumerate(((1560, 40, 1.4), (1650, 34, -1.1))):
            pts = [(0, H)]
            for x in range(0, W + 31, 30):
                pts.append((x, yb + amp * math.sin(x / 150 + g * sp + j)))
            pts.append((W, H))
            d.polygon(pts, fill=tint + (a + 10,))
        for k in range(4):
            r = 120 + k * 50
            d.ellipse((W - 150 - r, 260 - r, W - 150 + r, 260 + r), outline=col, width=6)
    elif kind == "blobs":
        for k in range(4):
            ang = g * .35 + k * math.pi / 2
            x, y = W / 2 + 330 * math.cos(ang), 900 + 520 * math.sin(ang * 1.0)
            r = 260 + 30 * math.sin(g + k)
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    elif kind == "rays":
        cx, cy = W / 2, 260
        for k in range(16):
            a0 = g * .15 + k * math.pi / 8
            a1 = a0 + math.pi / 16
            d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)),
                       (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))], fill=col)
    elif kind == "grid":
        off = (g * 30) % 140
        for ix in range(-1, 9):
            for iy in range(-1, 15):
                x, y = ix * 140 + off, iy * 140 + off
                d.line([(x - 14, y), (x + 14, y)], fill=tint + (a + 20,), width=6)
                d.line([(x, y - 14), (x, y + 14)], fill=tint + (a + 20,), width=6)
    img.alpha_composite(lay)
    return img


def header2(img, pal, grade, code):
    b1 = (WHITE, NAVY) if pal["sat"] else (BLUE, WHITE)
    x = pill(img, f"{grade}. SINIF BİYOLOJİ", 38, 70, 150, *b1)
    pill(img, code, 38, x + 18, 150, NAVY, YELLOW)


def base(pal, kind, g, c):
    img = bg(pal, kind, g)
    header2(img, pal, c["grade"], "BİY." + c["id"])
    return img


# ----------------------------------------------------------------- helpers
def paste_xy(base_img, layer, cx, cy, sx=1.0, sy=1.0, alpha=1.0):
    if alpha <= 0.003 or sx <= 0.003 or sy <= 0.003:
        return
    if sx != 1.0 or sy != 1.0:
        layer = layer.resize((max(1, int(layer.width * sx)), max(1, int(layer.height * sy))), Image.BILINEAR)
    if alpha < 1.0:
        layer = layer.copy()
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    base_img.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def make_card(w, h, fill=WHITE, r=44, outline=None, owidth=0):
    m = 18
    lay = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    rrect(lay, (m, m + 10, m + w, m + h + 10), r, (0, 0, 0), alpha=0.12)
    rrect(lay, (m, m, m + w, m + h), r, fill, outline=outline, width=owidth)
    return lay, m


def confetti(img, cx, cy, k, seed=1, n=34, spread=520):
    """Burst of coloured squares; k in 0..1 (animation progress)."""
    if k <= 0 or k >= 1:
        return
    rnd = random.Random(seed)
    d = ImageDraw.Draw(img)
    cols = [YELLOW, BLUE, GREEN, RED, ORANGE, (180, 90, 240)]
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        sp = rnd.uniform(.35, 1.0) * spread
        kx = out_cubic(k)
        x = cx + math.cos(a) * sp * kx
        y = cy + math.sin(a) * sp * kx + 520 * k * k * rnd.uniform(.6, 1.2)
        s = rnd.uniform(10, 20)
        rot = rnd.uniform(0, 6.28) + k * rnd.uniform(-9, 9)
        pts = [(x + s * math.cos(rot + q * math.pi / 2), y + s * math.sin(rot + q * math.pi / 2)) for q in range(4)]
        d.polygon(pts, fill=cols[i % len(cols)] + (int(255 * (1 - k ** 3)),))


# ----------------------------------------------------------------- hook
def fit_size(s, maxw=960, start=132, minimum=54):
    size = start
    while size > minimum and font(size).getlength(s) > maxw:
        size -= 4
    return size


def hook(img, pal, s, sub, u, fx, yoff=0):
    lines = s.split("\n")
    n = len(lines)
    y0 = 760 - (n - 1) * 100
    for i, l in enumerate(lines):
        size = fit_size(l)
        col = pal["acc"] if (i == n - 1 and n > 1) else pal["ink"]
        cy = y0 + i * 200 + yoff
        p = prog(u, 0.15 + i * 0.38, 0.6)
        if p <= 0:
            continue
        if fx == "pop":
            text(img, l, size, W / 2, cy, col, maxw=1000, scale=out_back(p), alpha=clamp(p * 2))
        elif fx == "slide":
            dx = (1 - out_cubic(p)) * (-1200 if i % 2 == 0 else 1200)
            text(img, l, size, W / 2 + dx, cy, col, maxw=1000)
        elif fx == "drop":
            text(img, l, size, W / 2, cy - (1 - out_bounce(p)) * 800, col, maxw=1000)
        elif fx == "type":
            tp = prog(u, 0.15 + i * 0.7, 0.8)
            k = int(len(l) * tp)
            wfull = font(size).getlength(l)
            if k > 0:
                lay = text_layer(l[:k], size, col, 2000, "left")
                img.alpha_composite(lay, (int(W / 2 - wfull / 2), int(cy - lay.height / 2)))
            if tp < 1 and int(u * 6) % 2 == 0:
                lay = text_layer("|", size, col, 200, "left")
                wk = font(size).getlength(l[:k])
                img.alpha_composite(lay, (int(W / 2 - wfull / 2 + wk), int(cy - lay.height / 2)))
        elif fx == "zoom":
            text(img, l, size, W / 2, cy, col, maxw=1000, scale=1 + (1 - out_cubic(p)) * 2.4, alpha=clamp(p * 2))
        elif fx == "spin":
            text(img, l, size, W / 2, cy, col, maxw=1000, scale=out_back(p), rot=(1 - out_cubic(p)) * -35)
        else:  # stretch
            lay = text_layer(l, size, col, 1000)
            paste_xy(img, lay, W / 2, cy, 1.0, max(.01, out_back(p, 2.6)), clamp(p * 3))
    if sub:
        text(img, sub, 54, W / 2, 1180, pal["ink"], maxw=950, alpha=prog(u, 1.5, .5))


# ----------------------------------------------------------------- brand block
def cta_layer(pal):
    h = 340
    lay = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    card = WHITE if pal["sat"] else NAVY
    fg = NAVY if pal["sat"] else WHITE
    ttl = BLUE if pal["sat"] else YELLOW
    rrect(lay, (60, 0, W - 60, h), 44, card)
    text(lay, "BİYOLOJİ REHBERİ", 64, W / 2, 60, ttl)
    for i, (lab, val) in enumerate([("WEB", "biyolojirehberi.com"), ("YOUTUBE", "@BiyoRehber"),
                                    ("INSTAGRAM", "@biyolojininrehberi")]):
        y = 148 + i * 66
        pill(lay, lab, 28, 110, y - 28, BLUE, WHITE)
        vl = text_layer(val, 44, fg, 600, "left")
        lay.alpha_composite(vl, (400, int(y - vl.height / 2)))
    return lay


def cta_block(img, pal, u, t0, fx, top=1050):
    p = prog(u, t0, 0.6)
    if p <= 0:
        return
    lay = cta_layer(pal)
    cy = top + lay.height / 2
    if p >= 1:  # gentle breathing once settled
        k = 1 + 0.012 * math.sin((u - t0) * 5)
        paste_xy(img, lay, W / 2, cy, k, k)
    elif fx == "rise":
        paste_xy(img, lay, W / 2, cy + (1 - out_back(p)) * 600, 1, 1, clamp(p * 3))
    elif fx == "pop":
        s = out_back(p)
        paste_xy(img, lay, W / 2, cy, s, s, clamp(p * 3))
    elif fx == "flip":
        paste_xy(img, lay, W / 2, cy, 1, max(.01, out_back(p, 2.4)), clamp(p * 3))
    else:
        paste_xy(img, lay, W / 2 + (1 - out_cubic(p)) * -1200, cy)


# ----------------------------------------------------------------- transitions
def _mask(draw_fn):
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m))
    return m


def trans(A, B, p, kind):
    p = in_out(clamp(p))
    if kind == "wipe_r":
        return Image.composite(B, A, _mask(lambda d: d.rectangle((0, 0, int(W * p), H), fill=255)))
    if kind == "wipe_l":
        return Image.composite(B, A, _mask(lambda d: d.rectangle((int(W * (1 - p)), 0, W, H), fill=255)))
    if kind == "wipe_u":
        return Image.composite(B, A, _mask(lambda d: d.rectangle((0, int(H * (1 - p)), W, H), fill=255)))
    if kind == "diag":
        s = p * (W + H * .5)
        return Image.composite(B, A, _mask(lambda d: d.polygon([(0, 0), (s, 0), (s - .5 * H, H), (0, H)], fill=255)))
    if kind == "iris":
        r = p * 1250
        return Image.composite(B, A, _mask(lambda d: d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=255)))
    if kind == "blinds":
        def f(d):
            for k in range(10):
                y0 = k * H / 10
                d.rectangle((0, y0, W, y0 + H / 10 * p + 1), fill=255)
        return Image.composite(B, A, _mask(f))
    if kind == "circles":
        def f(d):
            r = p * 190
            for i in range(5):
                for j in range(8):
                    cx, cy = W / 5 * (i + .5), H / 8 * (j + .5)
                    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        return Image.composite(B, A, _mask(f))
    if kind == "push_l":
        c = Image.new("RGBA", (W, H))
        c.paste(A, (-int(p * W), 0))
        c.paste(B, (W - int(p * W), 0))
        return c
    if kind == "push_u":
        c = Image.new("RGBA", (W, H))
        c.paste(A, (0, -int(p * H)))
        c.paste(B, (0, H - int(p * H)))
        return c
    if kind == "zoom":
        s = 1 + .35 * p
        a = A.resize((int(W * s), int(H * s)), Image.BILINEAR)
        a = a.crop(((a.width - W) // 2, (a.height - H) // 2, (a.width - W) // 2 + W, (a.height - H) // 2 + H))
        s2 = .8 + .2 * p
        b = B.resize((int(W * s2), int(H * s2)), Image.BILINEAR)
        bb = Image.new("RGBA", (W, H))
        bb.paste(b, ((W - b.width) // 2, (H - b.height) // 2))
        return Image.blend(a, bb, p)
    if kind == "flash":
        white = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        return Image.blend(A, white, p * 2) if p < .5 else Image.blend(white, B, (p - .5) * 2)
    return Image.blend(A, B, p)


class Seg:
    def __init__(self, dur, fn):
        self.dur, self.fn = dur, fn


def assemble(segs, trs, tdur=0.6):
    n = len(segs)
    starts = [0.0]
    for i in range(1, n):
        starts.append(starts[-1] + segs[i - 1].dur - tdur)
    total = starts[-1] + segs[-1].dur

    def scene(g):
        i = max(k for k in range(n) if starts[k] <= g + 1e-9)
        if i > 0 and g < starts[i] + tdur:
            a = segs[i - 1].fn(min(segs[i - 1].dur, g - starts[i - 1]), g)
            b = segs[i].fn(g - starts[i], g)
            return trans(a, b, (g - starts[i]) / tdur, trs[i - 1])
        return segs[i].fn(min(segs[i].dur, g - starts[i]), g)

    return scene, total


def cta_seg(c, pal, bgk, fx_h, fx_c):
    close = c["close"]

    def fn(u, g):
        img = base(pal, bgk, g, c)
        hook(img, pal, close, None, u, fx_h, yoff=-330)
        text(img, "Daha fazla biyoloji için:", 50, W / 2, 940, pal["ink"], alpha=prog(u, 1.0, .4))
        cta_block(img, pal, u, 1.2, fx_c, top=1010)
        return img

    return Seg(4.8, fn)


def hook_seg(c, pal, bgk, fx):
    def fn(u, g):
        img = base(pal, bgk, g, c)
        hook(img, pal, c["hook"], c.get("sub"), u, fx)
        return img

    return Seg(2.9, fn)
