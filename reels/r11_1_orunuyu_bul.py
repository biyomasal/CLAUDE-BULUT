"""11.1.1 Reel 1 – ÖRÜNTÜYÜ BUL (örüntü/genelleme formatı, açık mavi zemin)."""
import math

from PIL import Image, ImageDraw

import engine
from engine import *

engine.LABELS = ("11. SINIF BİYOLOJİ", "BİY.11.1.1")

LIGHT = (214, 232, 255)
ROWS = [
    ("Işık", "Fide ışığa doğru\neğilir"),
    ("Dokunma", "Küsmeotu\nyaprağını kapatır"),
    ("Sıcak yüzey", "İnsan elini\ngeri çeker"),
]
T_HOOK, SEG = 2.8, 2.8
T_Q = T_HOOK + SEG * 3          # "ortak kural?" question
T_REV = T_Q + 3.2               # reveal
T_END = T_REV + 3.6
TOTAL = T_END + 4.4
Y0, DY = 520, 300


def scene(t):
    img = vgradient(LIGHT, (240, 247, 255))
    for k in range(5):
        circle(img, (k * 300 + 60 * math.sin(t * .5 + k)) % W, 300 + k * 330, 150, BLUE, 0.07)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 820, 18), fill=BLUE + (255,))
    header(img)
    if t < T_END:
        footer(img, NAVY)

    if t < T_HOOK:
        text(img, "ÖRÜNTÜYÜ BUL!", 118, W / 2, 640, NAVY, maxw=1000, scale=out_back(prog(t, 0.1, .5)))
        text(img, "3 canlı, 3 olay.", 70, W / 2, 860, BLUE, scale=out_back(prog(t, .7, .5)))
        text(img, "Ortak kural ne?", 90, W / 2, 1010, NAVY, scale=out_back(prog(t, 1.2, .5)))
        return img

    for i, (stim, resp) in enumerate(ROWS):
        t0 = T_HOOK + i * SEG
        p = out_back(prog(t, t0, 0.55))
        if p <= 0:
            continue
        y = Y0 + i * DY
        slide = (1 - p) * (-W if i % 2 == 0 else W)
        row = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
        rrect(row, (60, 10, W - 60, 250), 40, WHITE)
        rrect(row, (60, 10, 84, 250), 12, BLUE)
        pill(row, "UYARAN", 28, 110, 34, BLUE, WHITE)
        text(row, stim, 62, 300, 160, NAVY, maxw=360)
        # arrow (draws itself)
        a = prog(t, t0 + 0.5, 0.4)
        dr = ImageDraw.Draw(row)
        x1 = 470 + 70 * a
        dr.line([(470, 130), (x1, 130)], fill=YELLOW + (255,), width=16)
        if a > 0.9:
            dr.polygon([(540, 100), (590, 130), (540, 160)], fill=YELLOW + (255,))
        pill(row, "TEPKİ", 28, 610, 34, NAVY, YELLOW)
        text(row, resp, 46, 790, 168, NAVY, maxw=380, alpha=prog(t, t0 + 0.7, 0.4))
        paste(img, row, W / 2 + slide, y + 130 - 10, 1, clamp(p))

    if t >= T_Q:
        u = t - T_Q
        if t < T_REV:
            rrect(img, (60, 1430, W - 60, 1560), 40, NAVY, alpha=prog(u, 0, .3))
            text(img, "ORTAK KURAL?", 80, W / 2, 1495, YELLOW, scale=1 + 0.04 * math.sin(u * 8),
                 alpha=prog(u, 0, .3))
        else:
            r = t - T_REV
            rrect(img, (60, 1400, W - 60, 1580), 40, YELLOW, alpha=prog(r, 0, .25))
            text(img, "UYARAN  →  TEPKİ", 74, W / 2, 1450, NAVY, scale=out_back(prog(r, 0, .5)),
                 alpha=prog(r, 0, .25))
            text(img, "Her canlı uyarana tepki verir!", 46, W / 2, 1530, NAVY, alpha=prog(r, .5, .4))

    if t >= T_END:
        # clear the screen for the closing block
        u = t - T_END
        img = vgradient(LIGHT, (240, 247, 255))
        header(img)
        text(img, "Uyaran → Tepki", 100, W / 2, 560, NAVY, maxw=1000, scale=out_back(prog(u, 0, .5)))
        text(img, "Genellemeyi sen yaptın!", 62, W / 2, 740, BLUE, alpha=prog(u, .4, .4))
        text(img, "Daha fazla biyoloji için:", 52, W / 2, 1100, NAVY, alpha=prog(u, .9, .4))
        cta(img, 1200, alpha=prog(u, 1.1, .4), scale=1 + 0.02 * math.sin(u * 6), light=True)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "11.1.1_Reels_1_OruntuyuBul.mp4"
    render(scene, TOTAL, out)
