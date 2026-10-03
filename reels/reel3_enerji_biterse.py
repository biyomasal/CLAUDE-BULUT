"""10.1.1 Reel 3 – ENERJİ BİTERSE? (pil/geri sayım formatı, siyah-neon zemin)."""
import math
import random

from PIL import Image, ImageDraw

from engine import *

BLACK = (6, 8, 16)
NEON = (255, 224, 70)
CYAN = (70, 220, 255)

ROWS = [  # (label, battery % at which it switches off)
    ("Kasların kasılması", 75),
    ("Madde taşıma", 50),
    ("Sinir hücrelerinde sinyal", 25),
    ("Büyüme ve onarım", 8),
]
T_HOOK, T_DRAIN = 3.0, 8.6
T_OFF = T_HOOK + T_DRAIN
T_BLACK = T_OFF + 0.9
T_END = T_BLACK + 1.0
TOTAL = T_END + 4.6


def bg(t, grid=True):
    img = Image.new("RGBA", (W, H), BLACK + (255,))
    if grid:
        d = ImageDraw.Draw(img)
        off = (t * 60) % 90
        for x in range(0, W + 90, 90):
            d.line([(x, 0), (x, H)], fill=(255, 255, 255, 12), width=2)
        for y in range(-90, H + 90, 90):
            d.line([(0, y + off), (W, y + off)], fill=(255, 255, 255, 12), width=2)
    return img


def glitch_text(img, s, size, cx, cy, t, amount, maxw=980):
    random.seed(int(t * 20))
    for col, dx in ((CYAN, -1), ((255, 60, 90), 1)):
        text(img, s, size, cx + dx * amount * random.uniform(.5, 1.5), cy + random.uniform(-1, 1) * amount * .4,
             col, maxw=maxw, alpha=0.7)
    text(img, s, size, cx, cy, WHITE, maxw=maxw)


def battery(img, cx, cy, pct, t):
    w, h = 560, 280
    col = GREEN if pct > 50 else (YELLOW if pct > 20 else RED)
    x0, y0 = cx - w // 2, cy - h // 2
    rrect(img, (x0 + w + 6, cy - 55, x0 + w + 42, cy + 55), 12, WHITE, alpha=0.9)
    rrect(img, (x0, y0, x0 + w, y0 + h), 44, None, outline=WHITE + (255,), width=10)
    inner = (w - 36) * pct / 100
    if inner > 4:
        rrect(img, (x0 + 18, y0 + 18, x0 + 18 + inner, y0 + h - 18), 28, col)
    if pct < 20 and int(t * 4) % 2 == 0:
        rrect(img, (x0, y0, x0 + w, y0 + h), 44, None, outline=RED + (255,), width=10)
    return col


def toggle(img, x, y, on, k):
    """k: 0..1 flip progress."""
    w, h = 150, 70
    col = GREEN if on else RED
    rrect(img, (x, y, x + w, y + h), h // 2, col, alpha=0.9)
    kx = x + 8 + (w - 70) * (1 if on else 1 - k)
    circle(img, kx + 27, y + h / 2, 27, WHITE)


def scene(t):
    # ---------- hook ----------
    if t < T_HOOK:
        img = bg(t)
        header(img)
        a = out_back(prog(t, 0.1, 0.5))
        text(img, "HÜCRELERİNİN", 112, W / 2, 620, WHITE, maxw=1000, scale=a)
        glitch_text(img, "ENERJİSİ", 170, W / 2, 800, t, 10 * (1 - prog(t, 1.2, 0.3)) + 3)
        text(img, "KESİLİRSE?", 150, W / 2, 1000, NEON, maxw=1000, scale=out_back(prog(t, 0.9, 0.5)))
        text(img, "Pil gibi tükenirse ne olur?", 56, W / 2, 1300, WHITE, alpha=prog(t, 1.8, .5))
        return img

    # ---------- draining battery ----------
    if t < T_OFF:
        u = t - T_HOOK
        pct = max(0, 100 - 100 * clamp((u - 0.4) / (T_DRAIN - 0.4)))
        img = bg(t)
        header(img)
        text(img, "HÜCREDE ATP BİTİYOR…", 56, W / 2, 400, NEON, alpha=clamp(u / 0.4))
        col = battery(img, W // 2, 760, pct, t)
        text(img, f"%{int(round(pct))}", 170, W / 2, 1010, col)
        y0 = 1190
        for i, (label, thr) in enumerate(ROWS):
            y = y0 + i * 100
            on = pct > thr
            # time at which pct reached thr
            flip_t = 0.4 + (T_DRAIN - 0.4) * (1 - thr / 100)
            k = prog(u, flip_t, 0.25)
            rrect(img, (70, y - 40, W - 70, y + 40), 22, WHITE, alpha=0.07)
            text(img, label, 48, 110 + text_layer(label, 48, WHITE, 700, "left").width / 2, y, WHITE,
                 maxw=700, align="left", alpha=0.95 if on else 0.4)
            toggle(img, W - 70 - 170, y - 35, on, k)
            if not on and u - flip_t < 0.3:
                flash = Image.new("RGBA", (W, H), (255, 60, 60, int(40 * (1 - (u - flip_t) / 0.3))))
                img.alpha_composite(flash)
        if pct < 8:
            random.seed(int(t * 30))
            for _ in range(6):
                y = random.randint(300, 1100)
                strip = img.crop((0, y, W, y + 14)).transform((W, 14), Image.AFFINE,
                                                              (1, 0, random.randint(-40, 40), 0, 1, 0))
                img.alpha_composite(strip, (0, y))
        return img

    # ---------- power off (CRT collapse) ----------
    if t < T_BLACK:
        u = (t - T_OFF) / 0.9
        img = bg(t, grid=False)
        k = 1 - in_out(clamp(u * 1.6))
        bar_h = max(6, int(H * k))
        layer = Image.new("RGBA", (W, bar_h), (255, 255, 255, 255))
        img.alpha_composite(layer, (0, (H - bar_h) // 2))
        if u > 0.6:
            img = bg(t, grid=False)
            circle(img, W / 2, H / 2, 14 * (1 - clamp((u - .6) / .4)) + 2, WHITE)
        return img

    if t < T_END:
        return bg(t, grid=False)

    # ---------- ending ----------
    u = t - T_END
    img = bg(t)
    header(img)
    text(img, "ENERJİ YOKSA", 100, W / 2, 380, WHITE, maxw=1000, scale=out_back(prog(u, 0.1, .5)))
    text(img, "YAŞAM DA YOK!", 120, W / 2, 520, NEON, maxw=1000, scale=out_back(prog(u, 0.4, .5)))
    # bolt
    s = out_back(prog(u, 0.9, .6)) * (1 + 0.04 * math.sin(u * 6))
    bolt = [(560, 780), (410, 1030), (520, 1030), (470, 1290), (700, 960), (580, 960), (650, 780)]
    cx, cy = W / 2, 880
    pts = [(cx + (x - 540) * s, cy + (y - 1030) * s) for x, y in bolt]
    for g, a in ((22, .08), (12, .15)):
        circle(img, cx, cy, 190 * s + g * 4, NEON, a)
    ImageDraw.Draw(img).polygon(pts, fill=NEON + (255,))
    text(img, "ATP = hücrenin enerji parası", 50, W / 2, 1185, WHITE, alpha=prog(u, 1.5, .4))
    cta(img, 1255, alpha=prog(u, 2.4, .4), scale=1 + 0.02 * math.sin(u * 6))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "10.1.1_Reels_3_EnerjiBiterse.mp4"
    render(scene, TOTAL, out)
