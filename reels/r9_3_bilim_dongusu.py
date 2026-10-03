"""9.1.2 Reel 3 – BİLİM BİR DÖNGÜ (dairesel akış formatı, koyu mavi radyal zemin)."""
import math

from PIL import Image, ImageDraw

import engine
from engine import *

engine.LABELS = ("9. SINIF BİYOLOJİ", "BİY.9.1.2")

STEPS = [
    ("Gözlem", "Bir şey dikkatini çeker."),
    ("Soru", "“Neden böyle oluyor?”"),
    ("Hipotez", "Olası bir açıklama kurulur."),
    ("Deney", "Açıklama test edilir."),
    ("Sonuç", "Kanıtlar değerlendirilir."),
]
CX, CY, R, NR = W / 2, 930, 330, 92
T_HOOK, T_NODES, T_STEP = 2.8, 1.4, 1.7
T_ORBIT = T_HOOK + T_NODES
T_LOOP = T_ORBIT + T_STEP * 5          # "sonuç yeni soru doğurur"
T_END = T_LOOP + 3.4
TOTAL = T_END + 4.4


def ang(i):
    return -math.pi / 2 + i * 2 * math.pi / 5


def pt(i):
    a = ang(i)
    return CX + R * math.cos(a), CY + R * math.sin(a)


def bg():
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    for r, a in ((900, .10), (650, .12), (400, .14)):
        circle(img, W / 2, 930, r, BLUE, a)
    return img


def scene(t):
    img = bg()
    header(img)

    if t < T_HOOK:
        text(img, "BİLİM", 170, W / 2, 620, WHITE, scale=out_back(prog(t, .1, .5)))
        text(img, "HİÇ BİTMEYEN", 110, W / 2, 810, YELLOW, maxw=1000, scale=out_back(prog(t, .5, .5)))
        text(img, "BİR DÖNGÜDÜR!", 110, W / 2, 940, YELLOW, maxw=1000, scale=out_back(prog(t, .8, .5)))
        text(img, "Nasıl mı? İzle.", 56, W / 2, 1200, WHITE, alpha=prog(t, 1.6, .5))
        return img

    if t >= T_END:
        u = t - T_END
        text(img, "Sonuç yeni bir\nsoruya yol açar.", 80, W / 2, 540, WHITE, maxw=1000,
             scale=out_back(prog(u, 0, .5)))
        text(img, "Bilim hiç bitmez!", 80, W / 2, 800, YELLOW, maxw=1000, scale=out_back(prog(u, .5, .5)))
        text(img, "Daha fazla biyoloji için:", 52, W / 2, 1000, WHITE, alpha=prog(u, 1.0, .4))
        cta(img, 1100, alpha=prog(u, 1.2, .4), scale=1 + 0.02 * math.sin(u * 6))
        return img

    d = ImageDraw.Draw(img)
    # faint ring + progress arc
    box = (CX - R, CY - R, CX + R, CY + R)
    d.ellipse(box, outline=(255, 255, 255, 40), width=10)

    s = (t - T_ORBIT) / T_STEP            # continuous step position (0..5)
    cur = int(s) if s >= 0 else -1
    frac = s - cur if s >= 0 else 0
    # ball position: waits at node (0.45 of step) then glides to next
    glide = in_out(clamp((frac - 0.45) / 0.55)) if cur >= 0 else 0
    pos = min(5, cur + glide) if cur >= 0 else 0
    if cur >= 0:
        a0 = -90
        a1 = -90 + 72 * min(5, pos)
        if a1 > a0:
            d.arc(box, a0, a1, fill=YELLOW + (255,), width=14)

    for i, (name, cap) in enumerate(STEPS):
        x, y = pt(i)
        p = out_back(prog(t, T_HOOK + i * 0.22, 0.5))
        if p <= 0:
            continue
        reached = cur >= i or (cur == i - 1 and glide > 0.9) or t >= T_LOOP
        active = cur == i and frac < 0.55 or (cur == 4 and i == 4 and t < T_LOOP)
        circle(img, x, y, NR * p, YELLOW if reached else WHITE)
        circle(img, x, y, NR * p, None, outline=NAVY, width=6)
        text(img, name, 38, x, y, NAVY, scale=p, maxw=170)
        if active:
            circle(img, x, y, NR + 14 + 6 * math.sin(t * 10), None, outline=YELLOW + (255,), width=6)

    # centre caption
    if 0 <= cur < 5 and t < T_LOOP:
        name, cap = STEPS[cur]
        k = prog(frac, 0.0, 0.2)
        text(img, f"{cur + 1}", 120, CX, CY - 90, YELLOW, alpha=k, scale=0.8 + 0.2 * k)
        text(img, cap, 40, CX, CY + 20, WHITE, maxw=380, alpha=k)
    elif t < T_ORBIT:
        text(img, "BİLİM\nDÖNGÜSÜ", 60, CX, CY, WHITE, alpha=prog(t, T_HOOK + 0.8, .4))
    else:
        u = t - T_LOOP
        text(img, "SONUÇ\nyeni bir\nSORU doğurur", 54, CX, CY + 70, YELLOW, maxw=400,
             scale=out_back(prog(u, 0, .5)))
        # arrow from Sonuç back to Soru
        if u > 0.4:
            x4, y4 = pt(4)
            x1, y1 = pt(1)
            k = prog(u, 0.4, 0.8)
            for q in range(0, 100, 4):
                f = q / 100
                if f <= k:
                    px = x4 + NR + (x1 - x4 - 2 * NR) * f
                    py = y4 + (y1 - y4) * f
                    circle(img, px, py, 6, YELLOW)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "9.1.2_Reels_3_BilimDongusu.mp4"
    render(scene, TOTAL, out)
