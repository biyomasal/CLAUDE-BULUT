"""10.1.1 Reel 1 – DOĞRU MU YANLIŞ MI? (quiz formatı, lacivert zemin)."""
import math
import random

from PIL import Image, ImageDraw

from engine import *

QS = [
    ("Uyurken enerji harcamayız.", False,
     "Uyurken de kalp, solunum ve beyin çalışır. Enerji gerekir!"),
    ("Bitkiler sadece fotosentez yapar, solunum yapmaz.", False,
     "Bitkiler de canlıdır: hücresel solunumla enerji elde eder."),
    ("Beyin, vücut ağırlığının yaklaşık %2’si olduğu hâlde enerjinin yaklaşık %20’sini kullanır.", True,
     "Beyin çok enerji isteyen bir organdır."),
]
T_HOOK, T_Q, T_END = 2.6, 5.6, 2.6 + 5.6 * 3
TOTAL = T_END + 4.4


def bg(t):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    for k in range(6):  # drifting soft circles
        x = (k * 260 + t * 40 * (1 if k % 2 else -1)) % (W + 400) - 200
        y = 300 + k * 270
        circle(img, x, y, 150 + 20 * math.sin(t + k), BLUE, 0.16)
    d = ImageDraw.Draw(img)
    d.polygon([(W - 330, 0), (W - 230, 0), (W - 60, 260), (W - 160, 260)], fill=BLUE + (255,))
    d.polygon([(W - 215, 0), (W - 170, 0), (W, 260 * 0 + 232), (W, 280)], fill=YELLOW + (255,))
    return img


def check(img, cx, cy, s, col):
    d = ImageDraw.Draw(img)
    d.line([(cx - s, cy), (cx - s * .3, cy + s * .7), (cx + s, cy - s * .7)], fill=col, width=int(s * .35), joint="curve")


def cross(img, cx, cy, s, col):
    d = ImageDraw.Draw(img)
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=col, width=int(s * .35))
    d.line([(cx - s, cy + s), (cx + s, cy - s)], fill=col, width=int(s * .35))


def ring(base, cx, cy, r, frac, col):
    d = ImageDraw.Draw(base)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 50), width=16)
    if frac > 0:
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * frac, fill=col + (255,), width=16)


def scene(t):
    img = bg(t)
    header(img)
    if t < T_END:
        footer(img)

    if t < T_HOOK:
        p = out_back(prog(t, 0.0, 0.6))
        text(img, "3 İDDİA", 130, W / 2, 560, YELLOW, scale=p)
        text(img, "DOĞRU MU", 160, W / 2, 800, WHITE, maxw=1000, scale=out_back(prog(t, 0.35, 0.6)))
        text(img, "YANLIŞ MI?", 160, W / 2, 980, WHITE, maxw=1000, scale=out_back(prog(t, 0.6, 0.6)))
        text(img, "Kaçını bilirsin?", 64, W / 2, 1250, WHITE,
             alpha=prog(t, 1.1, 0.5))
        return img

    if t >= T_END:
        u = t - T_END
        text(img, "3/3 yaptıysan", 80, W / 2, 620, WHITE, alpha=prog(u, 0, .4), scale=out_back(prog(u, 0, .5)))
        text(img, "ENERJİ\nUSTASISIN!", 150, W / 2, 880, YELLOW, scale=out_back(prog(u, .4, .6)))
        text(img, "Daha fazla biyoloji için:", 52, W / 2, 1150, WHITE, alpha=prog(u, 1.0, .5))
        cta(img, 1250, alpha=prog(u, 1.2, .4), scale=1 + 0.02 * math.sin(u * 6))
        return img

    i = int((t - T_HOOK) // T_Q)
    u = (t - T_HOOK) - i * T_Q
    stmt, ans, expl = QS[i]

    # reveal at u>=3.6
    revealed = u >= 3.6
    r = u - 3.6
    shake = 0
    if revealed and r < 0.4:
        random.seed(int(t * FPS))
        shake = (1 - r / 0.4) * 16

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # statement card
    card_in = out_back(prog(u, 0.0, 0.55))
    cy = 700 + (1 - card_in) * 500
    col = (GREEN if ans else RED) if revealed else WHITE
    card_col = (255, 255, 255)
    rrect(layer, (80, cy - 270, W - 80, cy + 270), 50, card_col)
    if revealed:
        a = clamp(r / 0.25)
        rrect(layer, (80, cy - 270, W - 80, cy + 270), 50, col, alpha=0.18 * a)
        rrect(layer, (80, cy - 270, 104, cy + 270), 12, col, alpha=a)
    else:
        rrect(layer, (80, cy - 270, 104, cy + 270), 12, BLUE)
    pill(layer, f"İDDİA {i + 1}/3", 34, 120, cy - 320, BLUE, WHITE)
    size = 78 if len(stmt) < 40 else (66 if len(stmt) < 60 else 56)
    text(layer, f"“{stmt}”", size, W / 2 + 10, cy, NAVY, maxw=800)

    # timer / stamp
    if not revealed:
        if u > 0.5:
            tl = clamp((u - 0.5) / 3.1)
            ring(layer, W / 2, 1220, 120, 1 - tl, YELLOW)
            n = 3 - int(min(2.99, (u - 0.5)))
            frac = ((u - 0.5) % 1)
            text(layer, str(n), 130, W / 2, 1220, WHITE, scale=1.25 - 0.25 * out_cubic(clamp(frac * 3)))
    else:
        s = out_back(clamp(r / 0.35), 2.6)
        stamp = Image.new("RGBA", (520, 200), (0, 0, 0, 0))
        rrect(stamp, (0, 0, 520, 200), 36, col)
        (check if ans else cross)(stamp, 110, 100, 42, WHITE)
        stamp.alpha_composite(text_layer("DOĞRU" if ans else "YANLIŞ", 76, WHITE, 500), (190 if ans else 180, 54))
        paste(layer, stamp, W / 2, 1160, scale=s * (1 + 1.2 * (1 - clamp(r / 0.35))), alpha=clamp(r / 0.1),
              rot=(-4 if ans else 4) * (1 - clamp(r / 0.5)))
        text(layer, expl, 52, W / 2, 1400, WHITE, maxw=900, alpha=prog(r, 0.5, 0.4))

    # slide-out of the card at the very end of each question
    out = prog(u, T_Q - 0.35, 0.35)
    layer = layer.transform(layer.size, Image.AFFINE, (1, 0, -out * W * 0.8 + shake * (1 if int(t * 60) % 2 else -1), 0, 1, 0))
    img.alpha_composite(layer)

    if revealed and r < 0.12:  # white flash
        flash = Image.new("RGBA", (W, H), (255, 255, 255, int(110 * (1 - r / 0.12))))
        img.alpha_composite(flash)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "10.1.1_Reels_1_DogruYanlis.mp4"
    render(scene, TOTAL, out)
