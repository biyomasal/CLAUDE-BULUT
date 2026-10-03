"""9.1.2 Reel 1 – BİLİM Mİ, DEĞİL Mİ? (kaydırmalı kart formatı, lacivert zemin)."""
import math

from PIL import Image, ImageDraw

import engine
from engine import *

engine.LABELS = ("9. SINIF BİYOLOJİ", "BİY.9.1.2")

CARDS = [
    ("Gözlem ve deneye dayanır.", True, "Bilim kanıta dayanır."),
    ("Tek bir kişinin sözü yeterlidir.", False, "Kanıt ve doğrulama gerekir."),
    ("Yeni kanıt gelirse değişebilir.", True, "Bilimsel bilgi güncellenebilir."),
    ("Kesindir, asla değişmez.", False, "Bilimsel bilgi geçicidir, gelişir."),
]
T_HOOK, T_C = 2.8, 4.2
T_END = T_HOOK + T_C * len(CARDS)
TOTAL = T_END + 4.4


def scene(t):
    img = vgradient((8, 28, 72), (16, 52, 120))
    for k in range(5):
        circle(img, (k * 290 + t * 25) % (W + 300) - 100, 300 + k * 330, 150, BLUE, 0.13)
    header(img)

    if t < T_HOOK:
        text(img, "BİLİM Mİ,", 150, W / 2, 640, WHITE, scale=out_back(prog(t, .1, .5)))
        text(img, "DEĞİL Mİ?", 150, W / 2, 830, YELLOW, scale=out_back(prog(t, .5, .5)))
        text(img, "Kartı kaydır, kararını ver!", 56, W / 2, 1120, WHITE, alpha=prog(t, 1.4, .5))
        return img

    if t >= T_END:
        u = t - T_END
        text(img, "Bilim bir kanıt\nve sorgulama işidir.", 74, W / 2, 560, WHITE, maxw=1000,
             scale=out_back(prog(u, 0, .5)))
        text(img, "Daha fazla biyoloji için:", 52, W / 2, 900, YELLOW, alpha=prog(u, .8, .4))
        cta(img, 1000, alpha=prog(u, 1.0, .4), scale=1 + 0.02 * math.sin(u * 6))
        return img

    i = int((t - T_HOOK) // T_C)
    u = (t - T_HOOK) - i * T_C
    stmt, sci, expl = CARDS[i]
    side = 1 if sci else -1

    # side hints
    rrect(img, (60, 1330, 500, 1430), 50, RED, alpha=0.9)
    text(img, "← BİLİM DEĞİL", 38, 280, 1380, WHITE)
    rrect(img, (580, 1330, W - 60, 1430), 50, GREEN, alpha=0.9)
    text(img, "BİLİM →", 38, 800, 1380, WHITE)

    pop = out_back(prog(u, 0.0, 0.5))
    sw = in_out(prog(u, 2.2, 0.45))
    card = Image.new("RGBA", (860, 480), (0, 0, 0, 0))
    rrect(card, (0, 0, 860, 480), 50, WHITE)
    pill(card, f"İDDİA {i + 1}/{len(CARDS)}", 30, 36, 34, BLUE, WHITE)
    text(card, f"“{stmt}”", 66, 430, 270, NAVY, maxw=740)
    shake = 8 * math.sin(u * 40) * (1 - prog(u, 0.6, .3)) * prog(u, 0.5, .01) if u < 0.9 else 0
    x = W / 2 + side * sw * 1000 + shake
    y = 760 + (1 - pop) * 300 + 40 * sw
    rot = -side * 14 * sw
    # tint the card as it flies
    if sw > 0:
        tint = Image.new("RGBA", card.size, (GREEN if sci else RED) + (int(140 * sw),))
        mask = card.getchannel("A")
        card = Image.composite(tint, card, mask).convert("RGBA")
        card.putalpha(mask)
    paste(img, card, x, y, scale=pop, alpha=clamp(pop * 1.5), rot=rot)

    # thinking bar
    if 0.5 < u < 2.2:
        rrect(img, (140, 1110, W - 140, 1130), 10, WHITE, alpha=0.2)
        rrect(img, (140, 1110, 140 + (W - 280) * (1 - prog(u, 0.5, 1.7)), 1130), 10, YELLOW)
        text(img, "Sen ne dersin?", 44, W / 2, 1180, WHITE, alpha=0.9)
    if u >= 2.4:
        r = u - 2.4
        col = GREEN if sci else RED
        stamp = Image.new("RGBA", (560, 120), (0, 0, 0, 0))
        rrect(stamp, (0, 0, 560, 120), 30, col)
        text(stamp, "BİLİM" if sci else "BİLİM DEĞİL", 58, 280, 62, WHITE)
        paste(img, stamp, W / 2, 1130, scale=out_back(clamp(r / 0.35), 2.4), alpha=clamp(r / 0.1))
        text(img, expl, 48, W / 2, 1240, WHITE, maxw=900, alpha=prog(r, .35, .4))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "9.1.2_Reels_1_BilimMi.mp4"
    render(scene, TOTAL, out)
