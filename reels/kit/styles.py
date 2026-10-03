"""16 layout families. Each returns (segments, internal_transitions)."""
import math
import random

from PIL import Image, ImageDraw

from kit.core import *  # noqa: F401,F403
from kit.core import (W, H, NAVY, BLUE, YELLOW, WHITE, GREEN, RED, ORANGE, clamp, prog, out_cubic, in_out,
                      out_back, out_bounce, text_layer, paste, text, rrect, circle, pill, on, lerp, lerp_c,
                      interp, base, make_card, paste_xy, confetti, Seg)


def ltext(img, s, size, x, cy, fill, maxw=800, alpha=1.0):
    lay = text_layer(s, size, fill, maxw, "left")
    paste(img, lay, x + lay.width / 2, cy, 1, alpha)
    return lay.height


def card_layer(w, h, fill=WHITE, r=44, outline=None, ow=0):
    lay, m = make_card(w, h, fill, r, outline, ow)
    return lay, m


# =================================================================== 1. swipe
def st_swipe(c, pal, bgk):
    items, N, T = c["items"], len(c["items"]), 4.2
    yes, no = c.get("labels", ("DOĞRU", "YANLIŞ"))

    def fn(u, g):
        img = base(pal, bgk, g, c)
        i = min(N - 1, int(u // T))
        lu = u - i * T
        truth, stmt, expl = items[i]
        side = 1 if truth else -1
        rrect(img, (60, 1330, 500, 1430), 50, RED, alpha=0.92)
        text(img, "← " + no, 38, 280, 1380, WHITE, maxw=400)
        rrect(img, (580, 1330, W - 60, 1430), 50, GREEN, alpha=0.92)
        text(img, yes + " →", 38, 800, 1380, WHITE, maxw=400)
        pop = out_back(prog(lu, 0, .5))
        sw = in_out(prog(lu, 2.2, .45))
        for k in (2, 1):  # deck behind
            if i + k < N:
                lay, _ = card_layer(860, 460)
                paste(img, lay, W / 2, 760 + 28 * k, 1 - .05 * k, .85)
        lay, m = card_layer(860, 460)
        pill(lay, f"{i + 1}/{N}", 30, m + 36, m + 34, pal["acc"], on(pal["acc"]))
        text(lay, f"“{stmt}”", 62, lay.width / 2, lay.height / 2 + 20, NAVY, maxw=740)
        if sw > 0:
            mask = lay.getchannel("A")
            tint = Image.new("RGBA", lay.size, (GREEN if truth else RED) + (255,))
            tint.putalpha(mask.point(lambda v: int(v * .55 * sw)))
            lay = Image.alpha_composite(lay, tint)
        shake = 8 * math.sin(lu * 40) * clamp(1 - lu / .9) if lu < .9 else 0
        paste(img, lay, W / 2 + side * sw * 1000 + shake, 760 + (1 - pop) * 300 + 40 * sw, scale=pop,
              alpha=clamp(pop * 1.5), rot=-side * 14 * sw)
        if 0.5 < lu < 2.2:
            rrect(img, (140, 1110, W - 140, 1130), 10, WHITE, alpha=.5)
            rrect(img, (140, 1110, 140 + (W - 280) * (1 - prog(lu, .5, 1.7)), 1130), 10, pal["acc"])
            text(img, "Sen ne dersin?", 44, W / 2, 1180, pal["ink"])
        if lu >= 2.4:
            r = lu - 2.4
            col = GREEN if truth else RED
            st = Image.new("RGBA", (640, 120), (0, 0, 0, 0))
            rrect(st, (0, 0, 640, 120), 30, col)
            text(st, yes if truth else no, 56, 320, 62, WHITE, maxw=600)
            paste(img, st, W / 2, 1130, scale=out_back(clamp(r / .35), 2.4), alpha=clamp(r / .1))
            text(img, expl, 46, W / 2, 1245, pal["ink"], maxw=900, alpha=prog(r, .35, .4))
            if truth:
                confetti(img, W / 2, 1000, r / 1.3, seed=i + 3, n=22, spread=380)
        return img

    return [Seg(N * T + .2, fn)], []


# =================================================================== 2. myth
def st_myth(c, pal, bgk):
    items, N, T = c["items"], len(c["items"]), 5.4
    CW, CH = 900, 330
    fcol = pal["acc"]

    def mcard(txt, strike):
        lay, m = card_layer(CW, CH, WHITE, 44, RED, 8)
        pill(lay, "MİT", 32, m + 36, m + 30, RED, WHITE)
        text(lay, txt, 62, lay.width / 2, lay.height / 2 + 14, NAVY, maxw=800)
        if strike > 0:
            tw = min(800, text_layer(txt, 62, NAVY, 800).width)
            x0 = lay.width / 2 - tw / 2 - 20
            ImageDraw.Draw(lay).line([(x0, lay.height / 2 + 20), (x0 + (tw + 40) * strike, lay.height / 2 + 20)],
                                     fill=RED + (255,), width=12)
        return lay

    def fcard(txt):
        lay, m = card_layer(CW, CH, fcol, 44)
        pill(lay, "GERÇEK", 32, m + 36, m + 30, GREEN, WHITE)
        text(lay, txt, 54, lay.width / 2, lay.height / 2 + 24, on(fcol), maxw=800)
        return lay

    def fn(u, g):
        img = base(pal, bgk, g, c)
        i = min(N - 1, int(u // T))
        lu = u - i * T
        myth, fact = items[i]
        text(img, f"{i + 1}/{N}", 44, W / 2, 340, pal["ink"], alpha=prog(lu, 0, .3))
        cx, cy = W / 2, 790
        if lu < 2.6:
            pop = out_back(prog(lu, 0, .5))
            shake = 14 * math.sin(lu * 70) * (1 - (lu - 2.1) / .5) if 2.1 < lu < 2.6 else 0
            paste(img, mcard(myth, out_cubic(prog(lu, 1.4, .7))), cx + shake, cy + (1 - pop) * 400, scale=pop,
                  alpha=clamp(pop * 2))
        elif lu < 3.0:
            card = mcard(myth, 1.0)
            r = (lu - 2.6) / .4
            for s in range(5):
                strip = card.crop((s * card.width // 5, 0, (s + 1) * card.width // 5, card.height))
                paste(img, strip, cx - card.width / 2 + (s + .5) * card.width / 5 + (s - 2) * 140 * r,
                      cy + 420 * r * r, alpha=1 - r, rot=(s - 2) * 25 * r)
        if lu >= 2.7:
            r = lu - 2.7
            s = out_back(clamp(r / .5), 2.2)
            paste(img, fcard(fact), cx, cy, scale=s, alpha=clamp(r / .15))
            if r < 1.2:
                confetti(img, cx, cy, r / 1.2, seed=i + 11, n=18, spread=420)
        return img

    return [Seg(N * T + .2, fn)], []


# =================================================================== 3. flip
def st_flip(c, pal, bgk):
    cards = c["cards"]
    fl, bl = c.get("labels", ("KAVRAM", "AÇIKLAMA"))
    POS = [(300, 640), (780, 640), (300, 1170), (780, 1170)]
    CW, CH = 440, 480
    back = pal["acc2"] if pal["acc2"] != WHITE else pal["acc"]
    if back == pal["acc"]:
        back = YELLOW
    T0, TD = 1.6, 2.6

    def face(i, is_back):
        lay, m = card_layer(CW, CH, back if is_back else WHITE, 44)
        if is_back:
            pill(lay, bl, 28, m + 28, m + 28, NAVY, YELLOW)
            text(lay, cards[i][1], 44, lay.width / 2, lay.height / 2 + 26, on(back), maxw=380)
        else:
            pill(lay, fl, 28, m + 28, m + 28, pal["acc"], on(pal["acc"]))
            text(lay, cards[i][0], 58, lay.width / 2, lay.height / 2 + 20, NAVY, maxw=380)
        return lay

    def fn(u, g):
        img = base(pal, bgk, g, c)
        for i, (cx, cy) in enumerate(POS[:len(cards)]):
            ap = out_back(prog(u, .2 + i * .25, .5))
            if ap <= 0:
                continue
            ft = T0 + i * TD
            k = prog(u, ft, .5)
            is_back = k >= .5
            sx = abs(math.cos(k * math.pi)) if 0 < k < 1 else 1
            lift = 1 + .08 * math.sin(k * math.pi)
            lay = face(i, is_back)
            paste_xy(img, lay, cx, cy, max(.02, sx) * ap * lift, ap * lift, clamp(ap))
            if ft - .9 < u < ft:
                rrect(img, (cx - CW / 2 - 8, cy - CH / 2 - 8, cx + CW / 2 + 8, cy + CH / 2 + 8), 50, None,
                      outline=pal["acc"] + (255,), width=8)
            if is_back and 0 < k - .5 < .4:
                confetti(img, cx, cy, (k - .5) / .4, seed=i + 5, n=10, spread=200)
        return img

    return [Seg(T0 + len(cards) * TD + 1.0, fn)], []


# =================================================================== 4. flow
def st_flow(c, pal, bgk):
    steps, N = c["steps"], len(c["steps"])
    T, h = 2.7, 220
    ys = [470 + i * 270 for i in range(N)]

    def fn(u, g):
        img = base(pal, bgk, g, c)
        act = int((u - .3) // T)
        for i, (title, cap) in enumerate(steps):
            t0 = .3 + i * T
            p = out_back(prog(u, t0, .55))
            if p <= 0:
                continue
            active = (act == i)
            fill = pal["acc"] if active else WHITE
            fg = on(fill)
            lay, m = card_layer(900, h, fill, 40)
            circle(lay, m + 90, lay.height / 2, 54, WHITE if active else pal["acc"])
            text(lay, str(i + 1), 62, m + 90, lay.height / 2 + 2, pal["acc"] if active else on(pal["acc"]))
            ltext(lay, title, 54, m + 175, lay.height / 2 - 40, fg if active else NAVY, maxw=680)
            ltext(lay, cap, 38, m + 175, lay.height / 2 + 44, fg if active else (60, 80, 120), maxw=680)
            dx = (1 - out_cubic(clamp(p))) * (-1100 if i % 2 == 0 else 1100)
            paste(img, lay, W / 2 + dx, ys[i], scale=1, alpha=clamp(p * 2))
            if i < N - 1:  # connector arrow
                a = prog(u, t0 + .7, .4)
                if a > 0:
                    d = ImageDraw.Draw(img)
                    y0 = ys[i] + h / 2 + 8
                    d.line([(W / 2, y0), (W / 2, y0 + 34 * a)], fill=pal["acc"] + (255,), width=10)
                    if a > .9:
                        d.polygon([(W / 2 - 24, y0 + 30), (W / 2 + 24, y0 + 30), (W / 2, y0 + 56)],
                                  fill=pal["acc"] + (255,))
        return img

    return [Seg(.3 + N * T + .8, fn)], []


# =================================================================== 5. cycle
def st_cycle(c, pal, bgk):
    nodes, n = c["nodes"], len(c["nodes"])
    CX, CY, R, NR = W / 2, 900, 335, 98
    T0, TS = 1.2, 1.8

    def pt(i):
        a = -math.pi / 2 + i * 2 * math.pi / n
        return CX + R * math.cos(a), CY + R * math.sin(a)

    def fn(u, g):
        img = base(pal, bgk, g, c)
        d = ImageDraw.Draw(img)
        box = (CX - R, CY - R, CX + R, CY + R)
        ring = (255, 255, 255, 140) if not pal["sat"] else (255, 255, 255, 120)
        d.ellipse(box, outline=ring, width=12)
        s = (u - T0) / TS
        cur = int(s) if s >= 0 else -1
        frac = s - cur if s >= 0 else 0
        glide = in_out(clamp((frac - .45) / .55)) if cur >= 0 else 0
        pos = min(n, cur + glide) if cur >= 0 else 0
        done = u >= T0 + n * TS
        if cur >= 0:
            a1 = -90 + (360 / n) * (n if done else pos)
            d.arc(box, -90, a1, fill=pal["acc"] + (255,), width=16)
        for i, (name, cap) in enumerate(nodes):
            x, y = pt(i)
            p = out_back(prog(u, .1 + i * .2, .5))
            if p <= 0:
                continue
            reached = cur >= i or (cur == i - 1 and glide > .9) or done
            fill = pal["acc"] if reached else WHITE
            circle(img, x, y, NR * p, fill)
            circle(img, x, y, NR * p, None, outline=NAVY, width=6)
            from kit.core import fit_size
            nsz = min(34, min(fit_size(l, NR * 1.7, 34, 18) for l in name.split("\n")))
            text(img, name, nsz, x, y, on(fill) if reached else NAVY, scale=p, maxw=NR * 1.8)
            if cur == i and frac < .55 and not done:
                circle(img, x, y, NR + 14 + 6 * math.sin(u * 10), None, outline=pal["acc"] + (255,), width=6)
        if 0 <= cur < n and not done:
            k = prog(frac, 0, .2)
            text(img, str(cur + 1), 120, CX, CY - 90, pal["acc"] if not pal["sat"] else YELLOW, alpha=k,
                 scale=.8 + .2 * k)
            text(img, nodes[cur][1], 40, CX, CY + 30, pal["ink"], maxw=400, alpha=k)
        elif not done:
            text(img, c.get("center", "DÖNGÜ"), 64, CX, CY, pal["ink"], alpha=prog(u, .8, .4), maxw=380)
        else:
            r = u - (T0 + n * TS)
            text(img, c.get("loop", "döngü\nsürer"), 60, CX, CY, pal["ink"], maxw=420,
                 scale=out_back(prog(r, 0, .5)))
        return img

    return [Seg(T0 + n * TS + 2.2, fn)], []


# =================================================================== 6. versus
def st_versus(c, pal, bgk):
    (lt, rt), rows = c["sides"], c["rows"]
    N = len(rows)
    T0, TR = 1.6, 2.6
    lc, rc = pal["acc"], (pal["acc2"] if pal["acc2"] != WHITE else ORANGE)
    if lc == rc:
        rc = ORANGE

    def fn(u, g):
        img = base(pal, bgk, g, c)
        p = out_cubic(prog(u, .1, .7))
        for (x0, x1, col, ttl, sgn) in ((50, 525, lc, lt, -1), (555, 1030, rc, rt, 1)):
            dx = (1 - p) * sgn * 700
            rrect(img, (x0 + dx, 330, x1 + dx, 1500), 46, col)
            text(img, ttl, 52, (x0 + x1) / 2 + dx, 420, on(col), maxw=430, scale=1.0)
        vp = out_back(prog(u, .9, .5))
        circle(img, W / 2, 500, 74 * vp, WHITE)
        circle(img, W / 2, 500, 74 * vp, None, outline=NAVY, width=6)
        text(img, "VS", 56, W / 2, 500, NAVY, scale=vp)
        for i, (a, b) in enumerate(rows):
            for j, (txt, x0, sgn) in enumerate(((a, 50, -1), (b, 555, 1))):
                rp = out_back(prog(u, T0 + i * TR + j * .35, .55))
                if rp <= 0:
                    continue
                lay, m = card_layer(430, 250, WHITE, 36)
                text(lay, txt, 40, lay.width / 2, lay.height / 2 + 8, NAVY, maxw=370)
                cy = 700 + i * 260
                paste(img, lay, x0 + 237 + (1 - clamp(rp)) * sgn * 500, cy, scale=1, alpha=clamp(rp * 2))
        return img

    return [Seg(T0 + N * TR + 1.0, fn)], []


# =================================================================== 7. quiz
def st_quiz(c, pal, bgk):
    q, opts, ok = c["q"], c["opts"], c["ok"]
    T_TIMER, T_REV = 2.0, 5.0

    def fn(u, g):
        img = base(pal, bgk, g, c)
        qp = out_back(prog(u, 0, .6))
        lay, m = card_layer(920, 360, WHITE, 46)
        pill(lay, "SORU", 30, m + 34, m + 30, pal["acc"], on(pal["acc"]))
        text(lay, q, 54, lay.width / 2, lay.height / 2 + 30, NAVY, maxw=800)
        paste(img, lay, W / 2, 540 + (1 - qp) * -300, scale=qp, alpha=clamp(qp * 2))
        rev = u >= T_REV
        r = u - T_REV
        for i, o in enumerate(opts):
            ap = out_back(prog(u, .8 + i * .22, .5))
            if ap <= 0:
                continue
            good = (i == ok)
            fill = WHITE
            if rev:
                fill = GREEN if good else (255, 255, 255)
            lay2, m2 = card_layer(900, 118, fill, 59)
            bc = pal["acc"] if not (rev and good) else WHITE
            circle(lay2, m2 + 62, lay2.height / 2, 38, bc)
            text(lay2, "ABCD"[i], 44, m2 + 62, lay2.height / 2, on(bc) if not (rev and good) else GREEN)
            ltext(lay2, o, 40, m2 + 125, lay2.height / 2, WHITE if (rev and good) else NAVY, maxw=700)
            y = 900 + i * 140
            shake = 10 * math.sin(r * 50) * clamp(1 - r / .5) if (rev and not good and 0 < r < .5) else 0
            al = clamp(ap * 2) * (0.45 if (rev and not good and r > .4) else 1.0)
            paste(img, lay2, W / 2 + (1 - clamp(ap)) * 900 + shake, y, scale=1, alpha=al)
        if T_TIMER < u < T_REV:
            k = prog(u, T_TIMER, T_REV - T_TIMER)
            cx, cy = 900, 380
            d = ImageDraw.Draw(img)
            circle(img, cx, cy, 58, WHITE)
            d.arc((cx - 58, cy - 58, cx + 58, cy + 58), -90, -90 + 360 * (1 - k), fill=pal["acc"] + (255,), width=12)
            n = 3 - int(min(2.99, k * 3))
            text(img, str(n), 64, cx, cy, NAVY)
        if rev:
            confetti(img, W / 2, 900 + ok * 140, r / 1.4, seed=7, n=30, spread=450)
            text(img, c["expl"], 44, W / 2, 1520, pal["ink"], maxw=940, alpha=prog(r, .4, .4))
        return img

    return [Seg(T_REV + 3.6, fn)], []


# =================================================================== 8. stats
def st_stats(c, pal, bgk):
    items, N, T = c["items"], len(c["items"]), 3.1
    ys = [520, 900, 1280][:N] if N == 3 else [560, 1000][:N]

    def num_text(it, k):
        if "static" in it:
            return it["static"]
        v = it["val"] * k
        s = f"{v:,.{it.get('dec', 0)}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{it.get('pre', '')}{s}{it.get('suf', '')}"

    def fn(u, g):
        img = base(pal, bgk, g, c)
        for i, it in enumerate(items):
            t0 = .3 + i * T
            p = out_back(prog(u, t0, .55))
            if p <= 0:
                continue
            lay, m = card_layer(940, 330, WHITE, 46)
            k = out_cubic(prog(u, t0 + .35, 1.6))
            num = num_text(it, k)
            text(lay, num, fit_num(num), m + 250, lay.height / 2 - 6, pal["acc"] if not pal["sat"] else (40, 110, 220),
                 maxw=480)
            ltext(lay, it["label"], 40, m + 510, lay.height / 2, NAVY, maxw=380)
            bar = prog(u, t0 + .35, 1.6)
            rrect(lay, (m + 40, lay.height - m - 40, m + 40 + 860 * bar, lay.height - m - 26), 7, pal["acc"])
            paste(img, lay, W / 2, ys[i] + (1 - clamp(p)) * 500, scale=1, alpha=clamp(p * 2))
        return img

    def fit_num(s):
        size = 150
        from kit.core import font
        while size > 60 and font(size).getlength(s) > 470:
            size -= 6
        return size

    return [Seg(.3 + N * T + 1.2, fn)], []


# =================================================================== 9. sorter
def st_sorter(c, pal, bgk):
    bins, items = c["bins"], c["items"]
    n, N, T = len(bins), len(items), 2.4
    bcols = [(31, 99, 216), ORANGE, (46, 170, 100)][:n]
    bw = (W - 120 - (n - 1) * 24) / n
    bx = [60 + bw / 2 + i * (bw + 24) for i in range(n)]
    BY0, BY1 = 1060, 1440
    from kit.core import fit_size
    bsize = min(40, min(fit_size(max(nm.split("\n"), key=len), bw - 30, 40, 26) for nm in bins))

    def fn(u, g):
        img = base(pal, bgk, g, c)
        counts = [0] * n
        for k, (_, b) in enumerate(items):
            if u >= .4 + k * T + 1.9:
                counts[b] += 1
        pulse = [0.0] * n
        for k, (_, b) in enumerate(items):
            lt = u - (.4 + k * T + 1.9)
            if 0 <= lt < .4:
                pulse[b] = 1 - lt / .4
        for i, nm in enumerate(bins):
            sc = 1 + .06 * pulse[i]
            lay = Image.new("RGBA", (int(bw) + 20, BY1 - BY0 + 20), (0, 0, 0, 0))
            rrect(lay, (10, 10, 10 + bw, 10 + BY1 - BY0), 36, bcols[i])
            rrect(lay, (10, 10, 10 + bw, 10 + 36), 18, (255, 255, 255), alpha=.25)
            text(lay, nm, bsize, lay.width / 2, 90, WHITE, maxw=bw - 30)
            text(lay, str(counts[i]), 120, lay.width / 2, 250, WHITE)
            paste(img, lay, bx[i], (BY0 + BY1) / 2, scale=sc)
        k = min(N - 1, int((u - .4) // T)) if u >= .4 else -1
        if k >= 0:
            txt, b = items[k]
            lu = u - (.4 + k * T)
            lay, m = card_layer(560, 120, WHITE, 60)
            text(lay, txt, 44, lay.width / 2, lay.height / 2 + 4, NAVY, maxw=500)
            if lu < .5:
                y = 300 + out_bounce(lu / .5) * 330 - 330
                y = -120 + out_bounce(lu / .5) * 770
                paste(img, lay, W / 2, y)
            elif lu < 1.4:
                paste(img, lay, W / 2, 650)
                text(img, "Hangi kutu?", 46, W / 2, 470, pal["ink"], alpha=.9 + .1 * math.sin(lu * 10))
                rrect(img, (240, 780, W - 240, 796), 8, WHITE, alpha=.5)
                rrect(img, (240, 780, 240 + (W - 480) * (1 - prog(lu, .5, .9)), 796), 8, pal["acc"])
            elif lu < 1.9:
                f = in_out((lu - 1.4) / .5)
                x = W / 2 + (bx[b] - W / 2) * f
                y = 650 + (BY0 + 120 - 650) * f - 140 * math.sin(f * math.pi)
                paste(img, lay, x, y, scale=1 - .5 * f, alpha=1 - .3 * f)
        return img

    return [Seg(.4 + N * T + .8, fn)], []


# =================================================================== 10. reveal
def st_reveal(c, pal, bgk):
    facts = c["facts"]
    from kit.core import BGS
    segs = []
    for i, f in enumerate(facts):
        def mk(i=i, f=f):
            def fn(u, g):
                p2 = dict(pal)
                kind = BGS[(BGS.index(bgk) + i * 3) % len(BGS)]
                img = base(p2, kind, g, c)
                p = out_back(prog(u, 0, .5))
                circle(img, W / 2, 520, 130 * p, pal["acc"])
                text(img, str(i + 1), 150, W / 2, 520, on(pal["acc"]), scale=p)
                text(img, "BİLİYOR MUYDUN?", 44, W / 2, 700, pal["ink"], alpha=prog(u, .3, .3))
                lay, m = card_layer(940, 560, WHITE, 46)
                text(lay, f, 64, lay.width / 2, lay.height / 2 + 10, NAVY, maxw=820)
                tp = out_back(prog(u, .35, .55))
                paste(img, lay, W / 2, 1100, scale=tp, alpha=clamp(tp * 2))
                return img

            return Seg(4.1, fn)
        segs.append(mk())
    trs = [c.get("rt", ["iris", "blinds", "wipe_u"])[i % 3] for i in range(len(facts) - 1)]
    return segs, trs


# =================================================================== 11. riddle
def st_riddle(c, pal, bgk):
    clues, ans = c["clues"], c["answer"]
    n = len(ans)
    bsz = int(min(104, (W - 120 - (n - 1) * 10) / n))
    rnd = random.Random(sum(map(ord, ans)))
    order = list(range(n))
    rnd.shuffle(order)
    T0, TC = 1.0, 2.5
    T_END = T0 + len(clues) * TC

    def revealed(i, u):
        if u >= T_END + .4 + order.index(i) * .12:
            return True
        k = int(n * .3) if u >= T0 + TC else 0
        k = int(n * .6) if u >= T0 + 2 * TC else k
        return order.index(i) < k

    def fn(u, g):
        img = base(pal, bgk, g, c)
        p = out_back(prog(u, 0, .5))
        text(img, "BEN KİMİM?", 110, W / 2, 400, pal["ink"], scale=p)
        for i, cl in enumerate(clues):
            ap = out_back(prog(u, T0 + i * TC, .5))
            if ap <= 0:
                continue
            lay, m = card_layer(920, 170, WHITE, 40)
            circle(lay, m + 70, lay.height / 2, 38, pal["acc"])
            text(lay, str(i + 1), 44, m + 70, lay.height / 2, on(pal["acc"]))
            ltext(lay, cl, 40, m + 135, lay.height / 2, NAVY, maxw=720)
            paste(img, lay, W / 2 + (1 - clamp(ap)) * (-1000 if i % 2 == 0 else 1000), 660 + i * 205,
                  alpha=clamp(ap * 2))
        x0 = W / 2 - (n * bsz + (n - 1) * 10) / 2 + bsz / 2
        done = u >= T_END + .4 + n * .12
        for i, chh in enumerate(ans):
            x = x0 + i * (bsz + 10)
            show = revealed(i, u)
            fill = WHITE
            lay, m = card_layer(bsz, bsz, fill, 18)
            if show:
                lt = u - (T_END + .4 + order.index(i) * .12)
                bounce = 1 + .25 * math.sin(clamp(lt / .3) * math.pi) if lt > -1 and lt < .3 else 1
                text(lay, chh, int(bsz * .7), lay.width / 2, lay.height / 2 + 2, pal["acc"] if pal["acc"] != YELLOW else BLUE)
                paste(img, lay, x, 1330, scale=bounce)
            else:
                rrect(lay, (m, m, m + bsz, m + bsz), 18, (255, 255, 255), alpha=.55)
                paste(img, lay, x, 1330)
        if done:
            confetti(img, W / 2, 1330, (u - (T_END + .4 + n * .12)) / 1.4, seed=2, n=36, spread=520)
        return img

    return [Seg(T_END + .4 + n * .12 + 1.6, fn)], []


# =================================================================== 12. bars
def st_bars(c, pal, bgk):
    bars, hi = c["bars"], c.get("hi", 0)
    n = len(bars)
    vmax = max(v for _, v in bars)
    X0, X1, BASE, HMAX = 100, 980, 1260, 640
    slot = (X1 - X0) / n
    bw = slot * .62
    T0, TB = 1.2, .85

    def fn(u, g):
        img = base(pal, bgk, g, c)
        text(img, c["title"], 52, W / 2, 360, pal["ink"], maxw=940, scale=out_back(prog(u, 0, .5)))
        d = ImageDraw.Draw(img)
        d.line([(X0 - 20, BASE), (X1 + 20, BASE)], fill=pal["ink"] + (255,), width=8)
        done = u >= T0 + n * TB
        for i, (lab, v) in enumerate(bars):
            t0 = T0 + i * TB
            k = out_cubic(prog(u, t0, .9))
            if k <= 0:
                text(img, lab, 32, X0 + slot * (i + .5), BASE + 62, pal["ink"], maxw=slot, alpha=prog(u, .6, .5))
                continue
            h = HMAX * v / vmax * k
            x = X0 + slot * (i + .5)
            col = (ORANGE if i == hi else pal["acc"]) if not pal["sat"] else (YELLOW if i == hi else WHITE)
            rrect(img, (x - bw / 2, BASE - h, x + bw / 2, BASE), 22, col)
            vv = c.get("fmt", "{:.0f}").format(v * k)
            text(img, vv, 46, x, BASE - h - 36, pal["ink"])
            text(img, lab, 32, x, BASE + 62, pal["ink"], maxw=slot)
            if i == hi and k >= 1:
                pulse = 1 + .08 * math.sin(u * 8)
                ImageDraw.Draw(img).polygon(
                    [(x + 38 * math.cos(math.pi / 2 + a * math.pi / 5) * (1 if a % 2 == 0 else .45) * pulse,
                      BASE - h - 110 - 38 * math.sin(math.pi / 2 + a * math.pi / 5) * (1 if a % 2 == 0 else .45) * pulse)
                     for a in range(10)], fill=YELLOW + (255,))
        if c.get("note"):
            text(img, c["note"], 34, W / 2, 1400, pal["ink"], alpha=.8)
        if done:
            r = u - (T0 + n * TB)
            lay, m = card_layer(940, 130, WHITE, 40)
            text(lay, c["punch"], 46, lay.width / 2, lay.height / 2 + 4, NAVY, maxw=860)
            paste(img, lay, W / 2, 1490, scale=out_back(prog(r, 0, .5)), alpha=clamp(r * 4))
        return img

    return [Seg(T0 + n * TB + 3.0, fn)], []


# =================================================================== 13. lab
def st_lab(c, pal, bgk):
    steps, N, kind = c["steps"], len(c["steps"]), c["kind"]
    T0, TS = .8, 2.8
    dy = 140 if kind == "balloon" else 0
    BX0, BX1, BY0, BY1 = 360, 720, 430 + dy, 900 + dy
    sh, sy0 = (150, 1190) if kind == "balloon" else (170, 1070)
    chh = 130 if kind == "balloon" else 150
    rnd = random.Random(5)
    seeds = [(rnd.random(), rnd.random(), rnd.uniform(.6, 1.4)) for _ in range(14)]

    def fn(u, g):
        img = base(pal, bgk, g, c)
        text(img, c["title"], 50, W / 2, 330, pal["ink"], maxw=940, alpha=prog(u, 0, .4))
        pos = clamp((u - T0) / TS, 0, N - .001)
        s = clamp((u - T0) / (N * TS))
        d = ImageDraw.Draw(img)
        if kind == "plant":
            bend = interp(c["bend"], pos)
            # sun
            sx, sy = 880, 520
            circle(img, sx, sy, 70, YELLOW)
            for a in range(12):
                aa = a * math.pi / 6 + u
                d.line([(sx + 90 * math.cos(aa), sy + 90 * math.sin(aa)), (sx + 118 * math.cos(aa), sy + 118 * math.sin(aa))],
                       fill=YELLOW + (255,), width=10)
            px, py = 480, 900
            pts = [(px + 200 * bend * (q / 20) ** 2, py - 380 * (q / 20)) for q in range(21)]
            d.line(pts, fill=(60, 170, 70, 255), width=18, joint="curve")
            tx, ty = pts[-1]
            d.ellipse((tx - 20, ty - 70, tx + 100, ty - 10), fill=(60, 170, 70, 255))
            d.ellipse((tx - 110, ty - 40, tx + 10, ty + 20), fill=(60, 170, 70, 255))
            d.polygon([(px - 130, py), (px + 130, py), (px + 95, py + 110), (px - 95, py + 110)], fill=(196, 120, 70, 255))
        else:
            liq = interp(c["colors"], pos) if "colors" in c else (120, 190, 255)
            lvl = 0.72
            ly = BY1 - (BY1 - BY0) * lvl
            d.rounded_rectangle((BX0, BY0, BX1, BY1), 40, fill=(255, 255, 255, 90), outline=NAVY + (150,), width=10)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle((BX0 + 12, ly, BX1 - 12, BY1 - 12), 30, fill=liq + (235,))
            for xx in range(BX0 + 12, BX1 - 12, 8):
                ld.line([(xx, ly + 6 * math.sin(xx / 30 + u * 3)), (xx + 8, ly + 6 * math.sin((xx + 8) / 30 + u * 3))],
                        fill=(255, 255, 255, 120), width=5)
            img.alpha_composite(lay)
            if kind == "bubbles":
                for q in range(6):  # sprig
                    d.line([(540, BY1 - 20), (500 + q * 16, BY1 - 150 - q * 12)], fill=(40, 150, 70, 255), width=8)
                rate = interp(c["rates"], pos)
                for j, (a, b, sp) in enumerate(seeds):
                    if j / 14 > rate:
                        continue
                    ph = (u * .5 * sp + b) % 1
                    x = 500 + a * 80 + 8 * math.sin(u * 4 + j)
                    y = BY1 - 140 - ph * (BY1 - 140 - ly)
                    r = 8 + a * 8
                    d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, 240), width=4)
            if kind == "balloon":
                d.rectangle((510, 330 + dy, 570, BY0), fill=(255, 255, 255, 220), outline=NAVY + (150,), width=4)
                bs = interp(c["balloon"], pos)
                rw, rh = 36 + 100 * bs, 40 + 120 * bs
                d.ellipse((540 - rw, 330 + dy - rh * 1.8, 540 + rw, 330 + dy - rh * .2), fill=pal["acc2"] + (255,) if pal["acc2"] != WHITE else ORANGE + (255,))
                for j, (a, b, sp) in enumerate(seeds[:10]):
                    ph = (u * .6 * sp + b) % 1
                    x = BX0 + 40 + a * (BX1 - BX0 - 80)
                    y = BY1 - 30 - ph * (BY1 - 30 - ly)
                    d.ellipse((x - 9, y - 9, x + 9, y + 9), outline=(255, 255, 255, 240), width=4)
        for i, (lab, txt) in enumerate(steps):
            ap = out_back(prog(u, T0 + i * TS - .3, .5))
            if ap <= 0:
                continue
            lay2, m = card_layer(940, chh, WHITE, 36)
            circle(lay2, m + 64, lay2.height / 2, 38, pal["acc"])
            text(lay2, str(i + 1), 44, m + 64, lay2.height / 2, on(pal["acc"]))
            ltext(lay2, lab, 38, m + 125, lay2.height / 2 - 30, pal["acc"] if not pal["sat"] else (40, 110, 220), maxw=740)
            ltext(lay2, txt, 36, m + 125, lay2.height / 2 + 26, NAVY, maxw=740)
            paste(img, lay2, W / 2, sy0 + i * sh + (1 - clamp(ap)) * 400, alpha=clamp(ap * 2))
        return img

    return [Seg(T0 + N * TS + 1.2, fn)], []


# =================================================================== 14. rank
def st_rank(c, pal, bgk):
    items, N, T = c["items"], len(c["items"]), 3.7

    def fn(u, g):
        img = base(pal, bgk, g, c)
        i = min(N - 1, int(u // T))
        lu = u - i * T
        num = N - i
        title, sub = items[i]
        p = out_cubic(prog(lu, 0, .45))
        shake = 12 * math.sin(lu * 60) * clamp(1 - lu / .5) if lu < .5 else 0
        col = pal["acc"] if not pal["sat"] else YELLOW
        text(img, str(num), 360, W / 2 + shake, 560, col, scale=1 + (1 - p) * 2.2, alpha=clamp(p * 2))
        text(img, "NUMARA", 40, W / 2, 330, pal["ink"], alpha=.8)
        cp = out_back(prog(lu, .6, .5))
        lay, m = card_layer(940, 430, WHITE, 46)
        text(lay, title, 62, lay.width / 2, lay.height / 2 - 70, NAVY, maxw=840)
        text(lay, sub, 42, lay.width / 2, lay.height / 2 + 80, (60, 80, 120), maxw=840)
        dy = (1 - clamp(cp)) * (500 if i % 2 == 0 else -400)
        paste(img, lay, W / 2, 1130 + dy, alpha=clamp(cp * 2))
        if num == 1 and lu > .6:
            confetti(img, W / 2, 560, (lu - .6) / 1.8, seed=4, n=36, spread=520)
        return img

    return [Seg(N * T + .2, fn)], []


# =================================================================== 15. diagram
def st_diagram(c, pal, bgk):
    center, parts = c["center"], c["parts"]
    CX, CY = W / 2, 900
    POS = [(250, 640), (830, 640), (250, 1160), (830, 1160)]
    T0, TP = 1.0, 2.4

    def fn(u, g):
        img = base(pal, bgk, g, c)
        d = ImageDraw.Draw(img)
        for i, (name, desc) in enumerate(parts):
            t0 = T0 + i * TP
            lp = prog(u, t0, .5)
            x, y = POS[i]
            if lp > 0:
                d.line([(CX, CY), (CX + (x - CX) * lp * .8, CY + (y - CY) * lp * .8)], fill=pal["acc"] + (255,), width=8)
            cpp = out_back(prog(u, t0 + .3, .5))
            if cpp <= 0:
                continue
            lay, m = card_layer(400, 230, WHITE, 40)
            text(lay, name, 46, lay.width / 2, lay.height / 2 - 46, pal["acc"] if not pal["sat"] else (40, 110, 220), maxw=350)
            text(lay, desc, 32, lay.width / 2, lay.height / 2 + 36, NAVY, maxw=350)
            glow = 1 + .04 * math.sin((u - t0) * 8) if 0 < u - t0 < 2.0 else 1
            paste(img, lay, x, y, scale=cpp * glow, alpha=clamp(cpp * 2))
        cp = out_back(prog(u, 0, .6))
        circle(img, CX, CY, 125 * cp, pal["acc"])
        circle(img, CX, CY, 125 * cp, None, outline=WHITE, width=8)
        from kit.core import fit_size
        csz = min(46, min(fit_size(l, 220, 46, 24) for l in center.split("\n")))
        text(img, center, csz, CX, CY, on(pal["acc"]), maxw=230, scale=cp)
        return img

    return [Seg(T0 + len(parts) * TP + 1.6, fn)], []


# =================================================================== 16. chat
def st_chat(c, pal, bgk):
    msgs = c["msgs"]
    names = c.get("names", ("Öğrenci", "Rehber"))
    TW = 760
    T_TYPE, T_HOLD = .8, 1.8
    heights = []
    for side, txt in msgs:
        lay = text_layer(txt, 44, NAVY, TW - 70, "left")
        heights.append(lay.height + 64)
    starts = []
    t = .6
    for (side, txt) in msgs:
        starts.append(t)
        t += T_TYPE + T_HOLD + .0006 * len(txt) * 100
    total = t + 1.0
    Y0 = 380

    def fn(u, g):
        img = base(pal, bgk, g, c)
        # content layout (static) then camera offset
        ys, y = [], Y0
        for h in heights:
            ys.append(y)
            y += h + 40
        shown = [i for i, s0 in enumerate(starts) if u >= s0]
        cam = 0
        if shown:
            last = shown[-1]
            bottom = ys[last] + heights[last] + 60 + 0
            cam = max(0, bottom - 1430)
            # smooth camera
            tprev = starts[last] + T_TYPE
            cam_prev = 0
            if last > 0:
                cam_prev = max(0, ys[last - 1] + heights[last - 1] + 60 - 1430)
            cam = lerp(cam_prev, cam, in_out(prog(u, tprev, .5)))
        for i, (side, txt) in enumerate(msgs):
            s0 = starts[i]
            if u < s0:
                continue
            left = (side == "L")
            yy = ys[i] - cam
            av_x = 105 if left else W - 105
            avc = pal["acc2"] if left and pal["acc2"] != WHITE else (BLUE if left else pal["acc"])
            if left and avc == pal["acc"]:
                avc = ORANGE
            typing = u < s0 + T_TYPE
            if typing:
                bx = 190 if left else W - 190 - 200
                rrect(img, (bx, yy, bx + 200, yy + 90), 45, WHITE if left else pal["acc"])
                for q in range(3):
                    r = 9 + 5 * max(0, math.sin(u * 9 - q))
                    circle(img, bx + 55 + q * 45, yy + 45, r, (130, 150, 190) if left else on(pal["acc"]))
            else:
                bp = out_back(prog(u, s0 + T_TYPE, .35))
                lay = text_layer(txt, 44, NAVY if left else on(pal["acc"]), TW - 70, "left")
                bw, bh = lay.width + 70, lay.height + 64
                bub = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
                rrect(bub, (10, 10, 10 + bw, 10 + bh), 44, WHITE if left else pal["acc"])
                bub.alpha_composite(lay, (10 + 35, 10 + 32))
                cx = 190 + bw / 2 if left else W - 190 - bw / 2
                paste(img, bub, cx, yy + bh / 2, scale=bp, alpha=clamp(bp * 2))
            circle(img, av_x, yy + 48, 46, avc)
            text(img, names[0][0] if left else "BR", 34 if left else 30, av_x, yy + 48, WHITE)
        return img

    return [Seg(total, fn)], []


STYLES = dict(swipe=st_swipe, myth=st_myth, flip=st_flip, flow=st_flow, cycle=st_cycle, versus=st_versus,
              quiz=st_quiz, stats=st_stats, sorter=st_sorter, reveal=st_reveal, riddle=st_riddle,
              bars=st_bars, lab=st_lab, rank=st_rank, diagram=st_diagram, chat=st_chat)
