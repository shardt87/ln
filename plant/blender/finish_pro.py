#!/usr/bin/env python3
"""Finish the --style pro renders: smooth vignette, fine grain and a
restrained caption with the credit (SK-3X1-11: "credit burned into every
image"). Writes <view>_pro_final.jpg (captioned) and <view>_pro_clean.jpg (for the
presentation board, which carries its own captions) next to each <view>_pro.png.

    python3 plant/blender/finish_pro.py plant/renders/pro
"""
import glob
import json
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
f = lambda name, size: ImageFont.truetype(os.path.join(FONTS, name), size)
SUN = "SUN 24° ALT / 258° AZ"


def tracked(d, xy, text, font, fill, track):
    """Draw text with letter-spacing (tracking in px); returns the end x."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x - track


def width_tracked(d, text, font, track):
    return sum(d.textlength(c, font=font) for c in text) + track * (len(text) - 1)


def vignette(im, strength=.24):
    W, H = im.size
    # radial falloff computed at low resolution, then scaled up smooth
    w, h = 320, int(320 * H / W)
    m = Image.new("L", (w, h))
    px = m.load()
    for j in range(h):
        for i in range(w):
            dx, dy = (i - w / 2) / (w / 2), (j - h / 2) / (h / 2)
            r = (dx * dx * .85 + dy * dy) ** .5
            px[i, j] = int(255 * (1 - strength * min(1, max(0, (r - .45) / .75)) ** 1.6))
    m = m.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    return ImageChops.multiply(im, Image.merge("RGB", (m, m, m)))


def grain(im, amount=2.4, seed=14):
    W, H = im.size
    rnd = random.Random(seed)
    small = Image.new("L", (W // 2, H // 2))
    small.putdata([128 + int(rnd.gauss(0, amount)) for _ in range(small.width * small.height)])
    g = small.resize((W, H), Image.BICUBIC)
    return ImageChops.add(im, Image.merge("RGB", (g, g, g)), scale=1, offset=-128)


def finish(png, meta):
    im = Image.open(png).convert("RGB")
    W, H = im.size
    k = W / 1920
    im = grain(vignette(im))
    im.save(png.replace("_pro.png", "_pro_clean.jpg"), quality=94, optimize=True, subsampling=0)
    # soft shade under the caption so it reads over any image content
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    band = int(118 * k)
    for j in range(band):
        sd.line([(0, H - band + j), (W, H - band + j)], fill=int(118 * (j / band) ** 1.8))
    im = Image.composite(Image.new("RGB", (W, H), (14, 18, 21)), im, shade)
    d = ImageDraw.Draw(im)
    v = meta["view"]
    ink, soft, copper = (244, 242, 236), (196, 199, 197), (214, 146, 88)
    m = int(46 * k)
    base = H - int(40 * k)
    title = f("Jura-Medium.ttf", int(19 * k))
    mono = f("IBMPlexMono-Regular.ttf", int(13 * k))
    light = f("Jura-Light.ttf", int(14 * k))
    # left: plate index + title / reference line
    x = tracked(d, (m, base - int(40 * k)), v["k"], title, copper, 3 * k)
    d.line([(x + 12 * k, base - int(29 * k)), (x + 34 * k, base - int(29 * k))], fill=copper, width=max(1, int(1.2 * k)))
    tracked(d, (x + 44 * k, base - int(40 * k)), v["name"].upper(), title, ink, 2.6 * k)
    sun = f"SUN {v['sun'][0]}° ALT / {v['sun'][1]}° AZ" if v.get("sun") else SUN
    tracked(d, (m, base - int(10 * k)), f"{v.get('sheet', 'SK-3X1')} · REV 14 · {v['lens']} MM · {sun} · "
            f"CYCLES {v['samples']} SPP", mono, soft, 1.2 * k)
    # right: credit and status
    r1 = "STEPHAN HARDT  |  POWER GENERATION SOLUTIONS"
    r2 = "CONCEPTUAL ILLUSTRATION · NOT ENGINEERED · NOT FOR CONSTRUCTION"
    tracked(d, (W - m - width_tracked(d, r1, light, 2.2 * k), base - int(38 * k)), r1, light, ink, 2.2 * k)
    tracked(d, (W - m - width_tracked(d, r2, light, 1.8 * k), base - int(10 * k)), r2, light, copper, 1.8 * k)
    # callouts: anchor dot, leader up to a numbered note (each placed clear of the ones already drawn)
    note = f("Jura-Medium.ttf", int(14 * k))
    num = f("Jura-Medium.ttf", int(15 * k))
    boxes = []
    for c in sorted(meta.get("callouts", ()), key=lambda c: c["y"]):
        ax, ay = c["x"] * W / meta.get("rw", W), c["y"] * H / meta.get("rh", H)
        col = tuple(int(c["colour"][i:i + 2], 16) for i in (1, 3, 5))
        tw = width_tracked(d, c["text"], note, 1.4 * k)
        bw, bh = tw + int(46 * k), int(30 * k)
        bx, by = ax - int(16 * k), ay - int(90 * k)
        for _ in range(40):                                         # nudge up until clear of earlier notes
            if all(bx + bw < x0 or bx > x1 or by + bh < y0 or by > y1 for (x0, y0, x1, y1) in boxes):
                break
            by -= bh + int(8 * k)
        bx = min(max(bx, m), W - m - bw)
        by = max(by, m)
        boxes.append((bx, by, bx + bw, by + bh))
        d.line([(ax, ay), (ax, by + bh)], fill=(250, 250, 248), width=max(1, int(1.6 * k)))
        r = int(4 * k)
        d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=(250, 250, 248), outline=col, width=max(1, int(2 * k)))
        d.rectangle([bx, by, bx + bw, by + bh], fill=(18, 22, 26))
        d.rectangle([bx, by, bx + int(30 * k), by + bh], fill=col)
        d.text((bx + int(15 * k), by + bh / 2), c["num"], font=num, fill=(255, 255, 255), anchor="mm")
        tracked(d, (bx + int(40 * k), by + int(8 * k)), c["text"], note, (240, 240, 236), 1.4 * k)
    out = png.replace("_pro.png", "_pro_final.jpg")
    im.save(out, quality=93, optimize=True, progressive=True, subsampling=0)
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "renders", "pro")
    for lj in sorted(glob.glob(os.path.join(root, "*_pro.labels.json"))):
        png = lj.replace(".labels.json", ".png")
        if os.path.exists(png):
            print("finished", finish(png, json.load(open(lj))))


if __name__ == "__main__":
    main()
