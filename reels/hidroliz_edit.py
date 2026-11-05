"""Hidroliz reels – viral re-cut: new hook + original narration + brand closing."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from PIL import Image  # noqa: E402

from kit.core import (W, H, hook, cta_block, text, prog, out_back, render, vgradient, NAVY,  # noqa: E402
                      YELLOW)

SRC = sys.argv[1]
OUT = Path(sys.argv[2])
WORK = Path(sys.argv[3])
WORK.mkdir(parents=True, exist_ok=True)

PAL = dict(bg=((226, 224, 214), (238, 236, 228)), ink=(36, 36, 36), acc=(206, 56, 32), acc2=YELLOW, sat=False)
HOOK_S, CTA_S = 2.6, 4.6
CUT_IN, CUT_OUT, AUDIO_END = 9.3, 36.55, 38.4


def bg():
    return vgradient(*PAL["bg"]).copy()


def hook_scene(t):
    img = bg()
    hook(img, PAL, "DEHİDRASYON mu\nHİDROLİZ mi?", "Çoğu öğrenci karıştırıyor!", t, "stretch")
    return img


def cta_scene(t):
    img = bg()
    hook(img, PAL, "Hidroliz: su ALIR\nDehidrasyon: su ÇIKAR", None, t, "pop", yoff=-330)
    text(img, "Daha fazla biyoloji için:", 50, W / 2, 940, PAL["ink"], alpha=prog(t, 1.0, .4))
    cta_block(img, PAL, t, 1.2, "rise", top=1010)
    return img


def sh(*a):
    subprocess.run(a, check=True)


render(hook_scene, HOOK_S, str(WORK / "hook.mp4"), crf=18, preset="veryfast")
render(cta_scene, CTA_S, str(WORK / "cta.mp4"), crf=18, preset="veryfast")

# synthetic pop sounds for the hook (the original has no sound there)
sh("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
   "aevalsrc='0.45*sin(2*PI*520*t)*exp(-22*t)+0.4*sin(2*PI*880*(t-0.55))*exp(-22*(t-0.55))*gte(t,0.55)"
   "+0.4*sin(2*PI*1180*(t-1.1))*exp(-22*(t-1.1))*gte(t,1.1)':d=%s:s=44100" % HOOK_S,
   "-ac", "2", str(WORK / "hook_a.wav"))
# original narration from the first spoken word on
sh("ffmpeg", "-y", "-v", "error", "-ss", str(CUT_IN), "-to", str(CUT_OUT), "-i", SRC, "-vf", "fps=30",
   "-af", "afade=t=in:st=0:d=0.15,aresample=44100", "-ac", "2", "-c:v", "libx264", "-preset", "veryfast",
   "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", str(WORK / "mid.mp4"))
# tail of the narration under the brand card, padded with silence
sh("ffmpeg", "-y", "-v", "error", "-ss", str(CUT_OUT), "-t", str(AUDIO_END - CUT_OUT), "-i", SRC, "-vn",
   "-af", f"afade=t=out:st={AUDIO_END - CUT_OUT - 0.5}:d=0.5,aresample=44100,apad=whole_dur={CTA_S}", "-ac", "2",
   str(WORK / "cta_a.wav"))

sh("ffmpeg", "-y", "-v", "error",
   "-i", str(WORK / "hook.mp4"), "-i", str(WORK / "hook_a.wav"),
   "-i", str(WORK / "mid.mp4"),
   "-i", str(WORK / "cta.mp4"), "-i", str(WORK / "cta_a.wav"),
   "-filter_complex",
   "[0:v]setsar=1[v0];[2:v]setsar=1[v1];[3:v]setsar=1[v2];"
   "[1:a]aresample=44100[a0];[2:a]aresample=44100[a1];[4:a]aresample=44100[a2];"
   "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
   "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(OUT))
print("ok", OUT)
