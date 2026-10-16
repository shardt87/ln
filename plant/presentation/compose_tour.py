"""Composite the tour captions onto the recorded frames and encode the clips (H.264 MP4, PowerPoint-ready).

    python3 compose_tour.py FRAMES_DIR OUT_DIR
FRAMES_DIR holds stop_NN/ folders from record_tour.js. Writes OUT_DIR/SK-3X1_tour_NN.mp4 per stop and
OUT_DIR/SK-3X1_tour_full.mp4. Captions follow the deck style (Barlow Condensed, charcoal card, copper rule):
hidden in flight, faded in after arrival."""
import json
import os
import subprocess
import sys
import textwrap

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts") if os.path.isdir(os.path.join(HERE, "fonts")) else os.path.join(os.path.dirname(HERE), "blender", "deck")
TOUR = json.load(open(os.path.join(HERE, "tour.json")))["stops"]
W, H = 1920, 1080
COPPER, LIGHT, GREY, CAB = (200, 105, 43), (243, 241, 236), (169, 179, 184), (240, 164, 107)


def font(n, s):
    return ImageFont.truetype(os.path.join(FD, n), s)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


def caption(i):
    s = TOUR[i]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    fs, ft, fl, fb = font("BarlowCondensed-Bold.ttf", 21), font("BarlowCondensed-ExtraBold.ttf", 54), \
        font("BarlowCondensed-Bold.ttf", 17), font("Barlow-Regular.ttf", 23)
    x0, pad, cw = 56, 30, 900
    lw = max(d.textlength(" ".join(k), font=fl) for k in ("EQUIPMENT", "SYSTEM", "CABLE")) + 24
    tlines = wrap(d, s["title"].upper(), ft, cw - 2 * pad)
    rows = [(k, wrap(d, s[v], fb, cw - 2 * pad - lw), c) for k, v, c in
            (("EQUIPMENT", "eq", LIGHT), ("SYSTEM", "sys", LIGHT), ("CABLE", "cab", CAB))]
    h = pad + 28 + len(tlines) * 54 + 24 + sum(len(r[1]) * 30 + 8 for r in rows) + pad - 6
    y0 = H - 56 - h
    d.rectangle([x0, y0, x0 + cw, H - 56], fill=(22, 26, 29, 228))
    d.rectangle([x0, y0, x0 + cw, y0 + 5], fill=COPPER + (255,))
    y = y0 + pad
    d.text((x0 + pad, y), " ".join(s["sec"].upper()), font=fs, fill=(224, 138, 74, 255))
    y += 34
    for t in tlines:
        d.text((x0 + pad, y), t, font=ft, fill=LIGHT + (255,))
        y += 54
    y += 24
    for k, lines, c in rows:
        d.text((x0 + pad, y + 4), " ".join(k), font=fl, fill=GREY + (255,))
        for j, t in enumerate(lines):
            d.text((x0 + pad + lw, y + j * 30), t, font=fb, fill=c + (255,))
        y += len(lines) * 30 + 8
    return ov


def chrome(i, n):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, W, 5], fill=(20, 24, 27, 90))
    d.rectangle([0, 0, int(W * (i + 1) / n), 5], fill=COPPER + (255,))
    f = font("BarlowCondensed-Bold.ttf", 17)
    for k, t in enumerate(("CONCEPTUAL ILLUSTRATION", "NOT ENGINEERED · NOT FOR CONSTRUCTION")):
        tw = d.textlength(" ".join(t), font=f)
        d.text((W - 40 - tw + 1, H - 70 + k * 22 + 1), " ".join(t), font=f, fill=(0, 0, 0, 120))
        d.text((W - 40 - tw, H - 70 + k * 22), " ".join(t), font=f, fill=(232, 150, 90, 255))
    return ov


def encode(frames_dir, out, i, n):
    meta = json.load(open(os.path.join(frames_dir, "meta.json")))
    fps, fly, nf = meta["fps"], meta["fly_ms"], meta["frames"]
    cap, chr_ = caption(i), chrome(i, n)
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(nf):
        t = f * 1000 / fps
        im = Image.open(os.path.join(frames_dir, "f_%04d.jpg" % f)).convert("RGBA")
        im.alpha_composite(chr_)
        a = min(1.0, max(0.0, (t - fly - 150) / 600))       # caption fades in after arrival
        if a > 0:
            c = cap if a >= 1 else cap.copy()
            if a < 1:
                c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
            im.alpha_composite(c)
        pr.stdin.write(im.convert("RGB").tobytes())
    pr.stdin.close()
    pr.wait()


def main(src, out):
    os.makedirs(out, exist_ok=True)
    n = len(TOUR)
    done = []
    for i in range(n):
        fd = os.path.join(src, "stop_%02d" % i)
        if not os.path.exists(os.path.join(fd, "meta.json")):
            continue
        o = os.path.join(out, "SK-3X1_tour_%02d.mp4" % (i + 1))
        if not os.path.exists(o):                    # clips already encoded are kept (incremental runs)
            encode(fd, o, i, n)
        done.append(o)
    if len(done) == n:
        lst = os.path.join(out, "concat.txt")
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in done))
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", "-movflags", "+faststart", os.path.join(out, "SK-3X1_tour_full.mp4")], check=True)
        os.remove(lst)
        print("wrote", os.path.join(out, "SK-3X1_tour_full.mp4"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
