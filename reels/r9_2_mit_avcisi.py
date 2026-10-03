"""9.1.2 Reel 2 – BİLİM MİTLERİ (mit avcısı formatı, krem zemin)."""
import math

from PIL import Image, ImageDraw

import engine
from engine import *

engine.LABELS = ("9. SINIF BİYOLOJİ", "BİY.9.1.2")

CREAM = (255, 246, 226)
MYTHS = [
    ("Teori sadece bir tahmindir.",
     "Teori, çok sayıda kanıtla desteklenen güçlü bir açıklamadır."),
    ("Bilimsel bilgi asla değişmez.",
     "Yeni kanıtlar gelince bilimsel bilgi güncellenir."),
    ("Bilim insanları hayal gücü kullanmaz.",
     "Yaratıcılık ve hayal gücü bilimin bir parçasıdır."),
]
T_HOOK, T_M = 2.8, 5.4
T_END = T_HOOK + T_M * len(MYTHS)
TOTAL = T_END + 4.4
CARD_W, CARD_H = 900, 330


def myth_card(txt, strike):
    c = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    rrect(c, (0, 0, CARD_W, CARD_H), 44, WHITE)
    rrect(c, (0, 0, CARD_W, CARD_H), 44, None, outline=RED + (255,), width=8)
    pill(c, "MİT", 32, 36, 30, RED, WHITE)
    text(c, txt, 62, CARD_W / 2, 190, NAVY, maxw=800)
    if strike > 0:
        tw = min(800, text_layer(txt, 62, NAVY, 800).width)
        d = ImageDraw.Draw(c)
        x0 = CARD_W / 2 - tw / 2 - 20
        d.line([(x0, 195), (x0 + (tw + 40) * strike, 195)], fill=RED + (255,), width=12)
    return c


def fact_card(txt):
    c = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    rrect(c, (0, 0, CARD_W, CARD_H), 44, NAVY)
    pill(c, "GERÇEK", 32, 36, 30, GREEN, WHITE)
    text(c, txt, 54, CARD_W / 2, 200, WHITE, maxw=800)
    return c


def scene(t):
    img = vgradient((255, 238, 200), CREAM)
    for k in range(5):
        circle(img, (k * 300 - t * 28) % (W + 300) - 100, 280 + k * 330, 150, YELLOW, 0.13)
    header(img)

    if t < T_HOOK:
        text(img, "BİLİM HAKKINDA", 90, W / 2, 600, NAVY, maxw=1000, scale=out_back(prog(t, .1, .5)))
        text(img, "3 BÜYÜK MİT!", 120, W / 2, 790, RED, maxw=1000, scale=out_back(prog(t, .5, .5)))
        text(img, "Hangilerine inanıyordun?", 56, W / 2, 1100, BLUE, alpha=prog(t, 1.4, .5))
        return img

    if t >= T_END:
        u = t - T_END
        text(img, "Mitleri bırak,", 90, W / 2, 520, NAVY, scale=out_back(prog(u, 0, .5)))
        text(img, "kanıta bak!", 120, W / 2, 680, BLUE, scale=out_back(prog(u, .4, .5)))
        text(img, "Daha fazla biyoloji için:", 52, W / 2, 960, NAVY, alpha=prog(u, .9, .4))
        cta(img, 1060, alpha=prog(u, 1.1, .4), scale=1 + 0.02 * math.sin(u * 6), light=True)
        return img

    i = int((t - T_HOOK) // T_M)
    u = (t - T_HOOK) - i * T_M
    myth, fact = MYTHS[i]
    text(img, f"MİT {i + 1}/{len(MYTHS)}", 40, W / 2, 330, BLUE, alpha=prog(u, 0, .3))

    cx, cy = W / 2, 780
    if u < 3.0:
        pop = out_back(prog(u, 0.0, 0.5))
        strike = out_cubic(prog(u, 1.4, 0.7))
        shake = 0
        if 2.1 < u < 2.6:
            shake = 14 * math.sin(u * 70) * (1 - (u - 2.1) / 0.5)
        if u < 2.6:
            paste(img, myth_card(myth, strike), cx + shake, cy + (1 - pop) * 400, scale=pop, alpha=clamp(pop * 2))
        else:
            # shatter into strips that fall away
            card = myth_card(myth, 1.0)
            r = (u - 2.6) / 0.4
            for s in range(5):
                strip = card.crop((s * CARD_W // 5, 0, (s + 1) * CARD_W // 5, CARD_H))
                dx = (s - 2) * 140 * r
                dy = 420 * r * r
                paste(img, strip, cx - CARD_W / 2 + (s + .5) * CARD_W / 5 + dx, cy + dy,
                      alpha=1 - r, rot=(s - 2) * 25 * r)
    if u >= 2.7:
        r = u - 2.7
        pop = out_back(clamp(r / 0.5), 2.2)
        paste(img, fact_card(fact), cx, cy, scale=pop, alpha=clamp(r / 0.15))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "9.1.2_Reels_2_MitAvcisi.mp4"
    render(scene, TOTAL, out)
