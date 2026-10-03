"""10.1.1 Reel 2 – ENERJİ YOLCULUĞU (akış/yolculuk formatı, açık zemin)."""
import math

from PIL import Image, ImageDraw

from engine import *

CREAM = (255, 246, 214)
GREENL = (60, 170, 90)
BROWN = (196, 132, 60)

NODES = [  # (x, y, title, caption)
    (230, 470, "GÜNEŞ", "Işık enerjisi kaynağı"),
    (230, 730, "BUĞDAY", "Fotosentezle besin üretir"),
    (230, 990, "EKMEK", "Besinde kimyasal enerji depolu"),
    (230, 1250, "HÜCRELERİN", "Solunumla ATP üretir"),
]
T_HOOK, SEG = 3.0, 3.1
T_END = T_HOOK + SEG * 4 + 0.6
TOTAL = T_END + 4.2


def icon(base, k, cx, cy, t, s):
    r = int(105 * s)
    circle(base, cx, cy, r, WHITE)
    circle(base, cx, cy, r, None, outline=NAVY, width=6)
    d = ImageDraw.Draw(base)
    if k == 0:  # sun
        for a, b in spin(cx, cy, 58 * s, 84 * s, 12, t * 0.8):
            d.line([a, b], fill=YELLOW + (255,), width=int(11 * s))
        circle(base, cx, cy, 44 * s, YELLOW)
    elif k == 1:  # wheat
        d.line([(cx, cy + 70 * s), (cx, cy - 55 * s)], fill=GREENL + (255,), width=int(7 * s))
        for j in range(4):
            y = cy - 50 * s + j * 22 * s
            for sx in (-1, 1):
                ex, ey = cx + sx * 24 * s, y - 14 * s
                d.ellipse((ex - 12 * s, ey - 22 * s, ex + 12 * s, ey + 22 * s), fill=(214, 168, 60, 255))
        d.ellipse((cx - 12 * s, cy - 84 * s, cx + 12 * s, cy - 36 * s), fill=(214, 168, 60, 255))
    elif k == 2:  # bread
        rrect(base, (cx - 70 * s, cy - 30 * s, cx + 70 * s, cy + 52 * s), int(26 * s), BROWN)
        for sx in (-38, 0, 38):
            circle(base, cx + sx * s, cy - 28 * s, 34 * s, BROWN)
        for sx in (-30, 0, 30):
            d.line([(cx + sx * s - 6, cy - 22 * s), (cx + sx * s + 6, cy + 12 * s)],
                   fill=(241, 207, 150, 255), width=int(8 * s))
    else:  # cell + bolt
        circle(base, cx, cy, 78 * s, (176, 206, 255))
        circle(base, cx - 22 * s, cy + 14 * s, 26 * s, BLUE)
        bolt = [(cx + 30 * s, cy - 70 * s), (cx - 4 * s, cy - 6 * s), (cx + 18 * s, cy - 6 * s),
                (cx - 20 * s, cy + 66 * s), (cx + 2 * s, cy + 8 * s), (cx - 18 * s, cy + 8 * s)]
        d.polygon(bolt, fill=YELLOW + (255,), outline=NAVY + (255,))


def pos(t):
    """Energy-ball position along the path."""
    t0 = T_HOOK
    if t < t0:
        return None
    seg = (t - t0) / SEG
    i = int(seg)
    if i >= 3:
        return NODES[3][:2]
    f = in_out(clamp((seg - i) * 1.35 - 0.0))
    a, b = NODES[i], NODES[i + 1]
    return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f


def scene(t):
    img = vgradient((255, 235, 150), CREAM)
    for k in range(5):
        circle(img, (k * 330 + 90 * math.sin(t * .6 + k)) % W, 260 + k * 330, 170, (255, 217, 61), 0.14)
    header(img, dark_text=True)
    if t < T_END:
        footer(img, NAVY)

    if t < T_HOOK:
        words = ["YEDİĞİN", "EKMEĞİN", "ENERJİSİ", "NEREDEN", "GELİYOR?"]
        for j, w in enumerate(words):
            p = out_back(prog(t, 0.15 + j * 0.28, 0.45))
            text(img, w, 130, W / 2, 520 + j * 170, YELLOW if j == 4 else NAVY, maxw=1000, scale=p,
                 alpha=clamp(p * 2))
        if t > 2.1:
            text(img, "Yolculuğu izle", 54, W / 2, 1420, BLUE, alpha=prog(t, 2.1, 0.5))
        return img

    # path
    d = ImageDraw.Draw(img)
    bp = pos(t)
    for i in range(3):
        a, b = NODES[i], NODES[i + 1]
        for q in range(0, 100, 2):
            x = a[0] + (b[0] - a[0]) * q / 100
            y = a[1] + (b[1] - a[1]) * q / 100
            if bp and (t - T_HOOK) / SEG > i + q / 100 / 1.35 - 0.05:
                circle(img, x, y, 7, BLUE, 0.85)
            else:
                circle(img, x, y, 4, NAVY, 0.15)

    for k, (x, y, title, cap) in enumerate(NODES):
        arrive = T_HOOK + k * SEG if k else T_HOOK - 0.4
        arrive += 0.0 if k == 0 else SEG * 0.74
        p = out_back(prog(t, arrive, 0.5))
        if p <= 0:
            continue
        pulse = 1 + 0.05 * math.sin((t - arrive) * 6) * clamp(1 - (t - arrive) / 2.5)
        icon(img, k, x, y, t, p * pulse)
        tl = text_layer(title, 72, NAVY, 640, "left")
        cl = text_layer(cap, 42, BLUE, 700, "left")
        paste(img, tl, 370 + tl.width / 2, y - 38, p, clamp(p))
        paste(img, cl, 370 + cl.width / 2, y + 46, 1, prog(t, arrive + 0.25, 0.4))

    # energy ball with glow
    if bp and t < T_END:
        for g, a in ((70, .12), (46, .22), (28, .5)):
            circle(img, bp[0], bp[1], g + 4 * math.sin(t * 12), YELLOW, a)
        circle(img, bp[0], bp[1], 14, WHITE)

    if t >= T_END:
        u = t - T_END
        rrect(img, (60, 1400, W - 60, 1540), 40, NAVY, alpha=0.96 * prog(u, 0, .3))
        text(img, "Çoğu canlının enerjisi\nGÜNEŞ’ten gelir!", 56, W / 2, 1470, WHITE, maxw=900,
             scale=out_back(prog(u, 0, .5)), alpha=prog(u, 0, .3))
        if u > 1.4:
            k = 1 + 0.04 * math.sin(u * 7)
            rrect(img, (W / 2 - 360 * k, 1580, W / 2 + 360 * k, 1580 + 100), 50, BLUE,
                  alpha=prog(u, 1.4, .4))
            text(img, "TÜM CEVAPLAR KANALDA", 46, W / 2, 1630, WHITE, alpha=prog(u, 1.4, .4), scale=k)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "10.1.1_Reels_2_EnerjiYolculugu.mp4"
    render(scene, TOTAL, out)
