"""Electricity effect for the copper cable X-ray (Strategy cover): energised white-gold cores, a two-stage copper
bloom and current pulses (small flares along the cables, weighted toward the power block where the energy starts).

    python blender/electrify.py IN.jpg OUT.jpg [SEED]
IN is the copper X-ray capture (all cable classes in copper, no glow).
"""
import random
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter


def screen(a, b, k=1.0):
    if k != 1.0:
        b = ImageChops.multiply(b, Image.new("RGB", b.size, tuple([int(255 * k)] * 3)))
    return ImageChops.screen(a, b)


def electrify(src, out, seed=7):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(float)
    m = np.clip((a[..., 0] - a[..., 2] - 40) / 60, 0, 1)            # copper cable pixels
    s = W / 1830

    def layer(r, g, b, mask):
        x = np.zeros_like(a)
        x[..., 0], x[..., 1], x[..., 2] = mask * r, mask * g, mask * b
        return Image.fromarray(np.clip(x, 0, 255).astype("uint8"))

    cop = layer(255, 140, 60, m)
    # 1. energised core: the line centres heat to white-gold
    core = layer(255, 226, 170, (m > .55) * m).filter(ImageFilter.GaussianBlur(.6 * s))
    res = screen(im, core, .85)
    # 2. two-stage bloom: tight bright glow + wide soft halo
    res = screen(res, cop.filter(ImageFilter.GaussianBlur(3.5 * s)), .8)
    res = screen(res, cop.filter(ImageFilter.GaussianBlur(16 * s)), .55)
    res = screen(res, cop.filter(ImageFilter.GaussianBlur(45 * s)), .22)
    # 3. current pulses along the cables, weighted toward the power block (image centre-low)
    ys, xs = np.nonzero(m > .8)
    rnd = random.Random(seed)
    pulse = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(pulse)
    cx, cy = W * .58, H * .62
    idx = list(range(len(xs)))
    rnd.shuffle(idx)
    n = 0
    for i in idx:
        x, y = xs[i], ys[i]
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / W
        if rnd.random() > max(.08, 1 - dist * 1.6):
            continue
        r = rnd.uniform(1.4, 3.2) * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 236, 200))
        if rnd.random() < .35:                                          # a few brighter flares with a glint
            L = r * 4.5
            d.line([(x - L, y), (x + L, y)], fill=(255, 210, 150), width=max(1, int(.8 * s)))
            d.line([(x, y - L * .6), (x, y + L * .6)], fill=(255, 210, 150), width=max(1, int(.8 * s)))
        n += 1
        if n >= int(70 * (W * H) / (1830 * 1620)):
            break
    res = screen(res, pulse.filter(ImageFilter.GaussianBlur(.7 * s)), 1.0)
    res = screen(res, pulse.filter(ImageFilter.GaussianBlur(7 * s)), .7)
    res.save(out, quality=94)
    return out


if __name__ == "__main__":
    print(electrify(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 7))
