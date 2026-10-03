"""11.1.1 Reel 2 – İNSAN mı BİTKİ mi? Kim daha hızlı? (yarış formatı, lacivert zemin)."""
import math

from PIL import Image, ImageDraw

import engine
from engine import *

engine.LABELS = ("11. SINIF BİYOLOJİ", "BİY.11.1.1")

T_HOOK, T_SETUP = 2.8, 2.0
T_GO = T_HOOK + T_SETUP          # uyaran!
T_HUMAN = 0.35
T_PLANT = 8.0
T_SUM = T_GO + T_PLANT + 0.8
T_END = T_SUM + 3.4
TOTAL = T_END + 4.4
LANE_X0, LANE_X1 = 110, W - 110


def human(img, cx, cy, react):
    d = ImageDraw.Draw(img)
    circle(img, cx, cy - 62, 28, WHITE)
    rrect(img, (cx - 24, cy - 28, cx + 24, cy + 52), 18, WHITE)
    # arm pulls back when reacting
    sh = (cx + 20, cy - 14)
    hand = (cx + 70 - 55 * react, cy + 24 - 50 * react)
    d.line([sh, hand], fill=WHITE + (255,), width=14)
    circle(img, hand[0], hand[1], 11, WHITE)
    # hot surface
    rrect(img, (cx + 82, cy + 18, cx + 140, cy + 34), 6, RED)


def plant(img, cx, cy, bend):
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(0, 21):
        k = i / 20
        pts.append((cx + 70 * bend * k * k, cy - 120 * k))
    d.line(pts, fill=GREEN + (255,), width=12, joint="curve")
    tipx, tipy = pts[-1]
    d.ellipse((tipx - 6, tipy - 34, tipx + 40, tipy - 4), fill=GREEN + (255,))
    d.ellipse((tipx - 44, tipy - 20, tipx + 2, tipy + 8), fill=GREEN + (255,))
    rrect(img, (cx - 40, cy, cx + 40, cy + 26), 8, (150, 100, 60))
    # light source
    circle(img, cx + 150, cy - 140, 24, YELLOW)


def lane(img, y, label, sub, frac, col, icon_fn, done, t):
    rrect(img, (LANE_X0 - 30, y - 150, LANE_X1 + 30, y + 150), 40, WHITE, alpha=0.07)
    text(img, label, 60, LANE_X0 + 20 + text_layer(label, 60, WHITE, 500, "left").width / 2, y - 105,
         WHITE, maxw=500, align="left")
    text(img, sub, 36, LANE_X0 + 20 + text_layer(sub, 36, YELLOW, 600, "left").width / 2, y - 55,
         YELLOW, maxw=600, align="left")
    icon_fn(y)
    bx0, bx1 = LANE_X0 + 260, LANE_X1 - 10
    rrect(img, (bx0, y + 15, bx1, y + 75), 30, WHITE, alpha=0.15)
    if frac > 0.01:
        rrect(img, (bx0, y + 15, bx0 + (bx1 - bx0) * frac, y + 75), 30, col)
    if done:
        text(img, "TEPKİ VERDİ!", 38, bx0 + (bx1 - bx0) / 2, y + 45, NAVY if col == YELLOW else WHITE,
             scale=1 + 0.05 * math.sin(t * 10))


def scene(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    for k in range(6):
        circle(img, (k * 260 + t * 30) % (W + 300) - 100, 280 + k * 280, 140, BLUE, 0.14)
    header(img)
    if t < T_END:
        footer(img)

    if t < T_HOOK:
        text(img, "İNSAN mı", 150, W / 2, 620, WHITE, scale=out_back(prog(t, .1, .5)))
        text(img, "BİTKİ mi?", 150, W / 2, 800, YELLOW, scale=out_back(prog(t, .5, .5)))
        text(img, "Uyarana kim\ndaha hızlı tepki verir?", 62, W / 2, 1100, WHITE, maxw=950,
             alpha=prog(t, 1.3, .5))
        return img

    if t >= T_END:
        u = t - T_END
        text(img, "Hızlar farklı,", 90, W / 2, 520, WHITE, scale=out_back(prog(u, 0, .5)))
        text(img, "kural aynı:", 90, W / 2, 650, WHITE, scale=out_back(prog(u, .3, .5)))
        text(img, "UYARAN → TEPKİ", 100, W / 2, 820, YELLOW, maxw=1000, scale=out_back(prog(u, .7, .5)))
        text(img, "Daha fazla biyoloji için:", 52, W / 2, 1100, WHITE, alpha=prog(u, 1.2, .4))
        cta(img, 1200, alpha=prog(u, 1.4, .4), scale=1 + 0.02 * math.sin(u * 6))
        return img

    g = t - T_GO
    appear = out_back(prog(t, T_HOOK, .6))
    hf = clamp(g / T_HUMAN) if g > 0 else 0
    pf = clamp(g / T_PLANT) if g > 0 else 0
    pf = in_out(pf) * 0.0 + pf  # linear, slow
    h_done, p_done = hf >= 1, pf >= 1

    # lanes slide in
    yoff = (1 - appear) * 300
    img2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lane(img2, 640 + 0, "İNSAN", "sinir sistemi ile", hf, GREEN,
         lambda y: human(img2, LANE_X0 + 105, y + 78, 1 if g > 0.05 else 0), h_done, t)
    lane(img2, 1090, "BİTKİ", "hormonlarla", pf, YELLOW,
         lambda y: plant(img2, LANE_X0 + 105, y + 108, pf), p_done, t)
    paste(img, img2, W / 2, H / 2 + yoff, 1, clamp(appear))

    if g > 0:
        # UYARAN flash + label
        if g < 0.5:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(120 * (1 - g / 0.5))))
            img.alpha_composite(fl)
        text(img, "UYARAN!", 70, W / 2, 330, RED if g < 1.0 else WHITE, scale=1 + .15 * max(0, 1 - g * 3))
    if g > 0.5 and not p_done:
        hours = min(3, int(g / T_PLANT * 3) + 1)
        text(img, f"{hours}. saat…", 56, W / 2, 1330, YELLOW,
             scale=1 + 0.03 * math.sin(g * 6))
    if h_done and g < 2.0:
        text(img, "saniyenin kesri!", 46, W / 2, 870, WHITE, alpha=prog(g, .35, .3))
    if t >= T_SUM:
        u = t - T_SUM
        rrect(img, (60, 1400, W - 60, 1580), 40, YELLOW, alpha=prog(u, 0, .3))
        text(img, "İkisi de tepki verdi!", 66, W / 2, 1490, NAVY, maxw=900,
             scale=out_back(prog(u, 0, .5)), alpha=prog(u, 0, .3))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "11.1.1_Reels_2_KimDahaHizli.mp4"
    render(scene, TOTAL, out)
