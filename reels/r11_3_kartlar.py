"""11.1.1 Reel 3 – DOKUNUNCA KAPANAN BİTKİ (kart çevirme formatı, parlak mavi zemin)."""
import math

from PIL import Image, ImageDraw

import engine
from engine import *

engine.LABELS = ("11. SINIF BİYOLOJİ", "BİY.11.1.1")

CARDS = [
    ("Parlak ışık", "İnsanda göz bebeği\nküçülür"),
    ("Dokunma", "Küsmeotu\nyapraklarını kapatır"),
    ("Tehlike", "Salyangoz\nkabuğuna çekilir"),
    ("Işık", "Fide ışığa doğru\neğilir"),
]
POS = [(300, 620), (780, 620), (300, 1140), (780, 1140)]
CW, CH = 440, 480
T_HOOK = 3.0
T_FLIP0, T_FLIPD = 4.4, 2.7
T_SUM = T_FLIP0 + T_FLIPD * 4 + 0.4
T_END = T_SUM + 3.4
TOTAL = T_END + 4.4


def card_face(i, back):
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    if not back:
        rrect(lay, (0, 0, CW, CH), 44, WHITE)
        pill(lay, "UYARAN", 30, 30, 30, BLUE, WHITE)
        lay.alpha_composite(text_layer(CARDS[i][0], 64, NAVY, 380), (int((CW - text_layer(CARDS[i][0], 64, NAVY, 380).width) / 2), 190))
        lay.alpha_composite(text_layer("?", 130, BLUE, 200), (int((CW - text_layer("?", 130, BLUE, 200).width) / 2), 300))
    else:
        rrect(lay, (0, 0, CW, CH), 44, YELLOW)
        pill(lay, "TEPKİ", 30, 30, 30, NAVY, YELLOW)
        tl = text_layer(CARDS[i][1], 50, NAVY, 380)
        lay.alpha_composite(tl, (int((CW - tl.width) / 2), int(CH / 2 - tl.height / 2 + 30)))
    return lay


def scene(t):
    img = Image.new("RGBA", (W, H), BLUE + (255,))
    for k in range(6):
        circle(img, (k * 280 - t * 35) % (W + 300) - 100, 260 + k * 290, 170, (255, 255, 255), 0.07)
    header(img)
    if t < T_END:
        footer(img)

    if t < T_HOOK:
        words = ["DOKUNUNCA", "KAPANAN", "BİR BİTKİ", "VAR!"]
        for j, w in enumerate(words):
            p = out_back(prog(t, .1 + j * .35, .45))
            text(img, w, 140, W / 2, 560 + j * 200, YELLOW if j == 3 else WHITE, maxw=1000, scale=p,
                 alpha=clamp(p * 2))
        text(img, "Peki başkaları ne yapar?", 54, W / 2, 1450, WHITE, alpha=prog(t, 2.0, .5))
        return img

    if t >= T_END:
        u = t - T_END
        img2 = Image.new("RGBA", (W, H), BLUE + (255,))
        header(img2)
        text(img2, "Hepsinde aynı örüntü:", 70, W / 2, 520, WHITE, maxw=1000, scale=out_back(prog(u, 0, .5)))
        text(img2, "UYARAN → TEPKİ", 110, W / 2, 700, YELLOW, maxw=1000, scale=out_back(prog(u, .4, .5)))
        text(img2, "Daha fazla biyoloji için:", 52, W / 2, 1100, WHITE, alpha=prog(u, 1.1, .4))
        cta(img2, 1200, alpha=prog(u, 1.3, .4), scale=1 + 0.02 * math.sin(u * 6))
        return img2

    dim = prog(t, T_SUM, 0.4)
    for i, (cx, cy) in enumerate(POS):
        appear = out_back(prog(t, T_HOOK + 0.1 + i * 0.25, 0.5))
        if appear <= 0:
            continue
        ft = T_FLIP0 + i * T_FLIPD
        k = prog(t, ft, 0.5)
        # flip: scale x 1 -> 0 -> 1, face switches at middle
        back = k >= 0.5
        sx = abs(math.cos(k * math.pi)) if 0 < k < 1 else 1
        face = card_face(i, back)
        lift = 1 + 0.08 * math.sin(k * math.pi)
        if sx < 0.995:
            face = face.resize((max(1, int(CW * sx)), CH), Image.BILINEAR)
        paste(img, face, cx, cy, appear * lift, (1 - dim) * clamp(appear))
        # highlight ring on the active card
        if ft - 0.9 < t < ft:
            rrect(img, (cx - CW / 2 - 8, cy - CH / 2 - 8, cx + CW / 2 + 8, cy + CH / 2 + 8), 50, None,
                  outline=YELLOW + (255,), width=8)

    if t >= T_SUM:
        u = t - T_SUM
        text(img, "UYARAN → TEPKİ", 100, W / 2, 900, YELLOW, maxw=1000, scale=out_back(prog(u, 0, .5)))
        text(img, "Canlılar uyaranları algılar\nve tepki verir.", 54, W / 2, 1060, WHITE, maxw=950,
             alpha=prog(u, .5, .4))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "11.1.1_Reels_3_Kartlar.mp4"
    render(scene, TOTAL, out)
