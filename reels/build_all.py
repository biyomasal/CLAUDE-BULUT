"""Render one reel per kazanım.

    python3 build_all.py list
    python3 build_all.py stills 9.1.1 10.1.2 ...        # contact sheets in $STILLS
    python3 build_all.py render [ids...] [--jobs 4]      # mp4s into tum_kazanimlar/
"""
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kit.core import (BGS, HFX, TRS, CFX, PALS, assemble, hook_seg, cta_seg, render, W, H)  # noqa: E402
from kit.content import R  # noqa: E402
from kit.styles import STYLES  # noqa: E402

ORDER = ["sky", "sun", "mint", "peach", "lav", "rose", "lime", "aqua", "ocean", "coral", "sunny", "grape", "leaf"]
OUT = HERE / "tum_kazanimlar"


def make(idx):
    c = R[idx]
    pal = PALS[ORDER[(idx * 5 + 2) % len(ORDER)]]
    bgk = BGS[(idx * 3) % len(BGS)]
    fx_h = HFX[(idx * 3 + 1) % len(HFX)]
    fx_c = CFX[(idx * 3) % len(CFX)]
    fx_close = HFX[(idx * 2 + 3) % len(HFX)]
    tr1 = TRS[(idx * 2) % len(TRS)]
    tr2 = TRS[(idx * 5 + 3) % len(TRS)]
    if tr2 == tr1:
        tr2 = TRS[(idx * 5 + 4) % len(TRS)]
    body, inner = STYLES[c["style"]](c, pal, bgk)
    segs = [hook_seg(c, pal, bgk, fx_h)] + body + [cta_seg(c, pal, bgk, fx_close, fx_c)]
    trs = [tr1] + inner + [tr2]
    scene, total = assemble(segs, trs)
    return scene, total, dict(pal=ORDER[(idx * 5 + 2) % len(ORDER)], bg=bgk, hook=fx_h, cta=fx_c, tr=(tr1, tr2))


def out_path(c):
    return OUT / f"{c['id']}_Reels.mp4"


def render_one(idx):
    OUT.mkdir(exist_ok=True)
    scene, total, info = make(idx)
    p = out_path(R[idx])
    render(scene, total, str(p), crf=22, preset="veryfast")
    return R[idx]["id"], round(total, 1), info


def find(ids):
    pos = {c["id"]: i for i, c in enumerate(R)}
    return [pos[i] for i in ids] if ids else list(range(len(R)))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    jobs = 4
    if "--jobs" in sys.argv:
        jobs = int(sys.argv[sys.argv.index("--jobs") + 1])
        args = [a for a in args if a != str(jobs)]
    if cmd == "list":
        for i, c in enumerate(R):
            print(i, c["id"], c["style"], ORDER[(i * 5 + 2) % len(ORDER)])
    elif cmd == "stills":
        from PIL import Image
        outd = Path(os.environ.get("STILLS", "/tmp/stills"))
        outd.mkdir(parents=True, exist_ok=True)
        for idx in find(args):
            scene, total, info = make(idx)
            n = 8
            ts = [total * (k + .5) / n for k in range(n)]
            fr = [scene(t).convert("RGB").resize((240, 427)) for t in ts]
            sh = Image.new("RGB", (240 * n, 427))
            for k, f in enumerate(fr):
                sh.paste(f, (240 * k, 0))
            sh.save(outd / f"{R[idx]['id']}.jpg", quality=80)
            print(R[idx]["id"], round(total, 1), info)
    elif cmd == "render":
        idxs = find(args)
        with ProcessPoolExecutor(max_workers=jobs) as ex:
            for r in ex.map(render_one, idxs):
                print("done", *r, flush=True)
