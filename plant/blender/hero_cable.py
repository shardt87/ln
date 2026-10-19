"""Hero cable: the photoreal render with every visible cable energised in copper, the plant itself untouched.

The cable pixels come from a second render of the same camera with the cables in pure red (SK_CABLE_MASK=1), so the
effect follows the real cable geometry and hides wherever the plant does. On those pixels: a burnished-copper tint that
keeps the render's light and shade, a white-gold core, a tight and a wide copper bloom, and a few current pulses.

    SK_CABLE_MASK=1 python blender/SW-3X1_Rev14_blender_build.py --views HX1 ... --out MASKDIR
    python blender/SW-3X1_Rev14_blender_build.py --views HX1 ... --out PHOTODIR
    python blender/hero_cable.py PHOTO.png MASK.png OUT.jpg [SEED]
"""
import random
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

COPPER = np.array([214, 118, 58], float)      # burnished copper, lit
CORE = (255, 222, 168)                        # energised core, white-gold
GLOW = (255, 140, 62)


def screen(a, b, k=1.0):
    if k != 1.0:
        b = ImageChops.multiply(b, Image.new("RGB", b.size, tuple([int(255 * k)] * 3)))
    return ImageChops.screen(a, b)


def cable_mask(mask_png, size):
    a = np.asarray(Image.open(mask_png).convert("RGB").resize(size, Image.LANCZOS)).astype(float)
    m = np.clip((a[..., 0] - np.maximum(a[..., 1], a[..., 2]) - 60) / 90, 0, 1)
    return m


def hero(photo_png, mask_png, out, seed=5):
    im = Image.open(photo_png).convert("RGB")
    W, H = im.size
    s = W / 1920
    a = np.asarray(im).astype(float)
    m = cable_mask(mask_png, (W, H))
    # 1. copper tint that keeps the render's shading (luminance drives the copper's brightness)
    lum = (a @ [.299, .587, .114]) / 255
    cu = COPPER[None, None, :] * (.45 + 1.1 * lum[..., None])
    a = a * (1 - .9 * m[..., None]) + cu * (.9 * m[..., None])
    res = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))

    def layer(col, mask):
        x = np.zeros((H, W, 3))
        for i in range(3):
            x[..., i] = mask * col[i]
        return Image.fromarray(np.clip(x, 0, 255).astype("uint8"))

    # 2. energised core along the middle of each cable run
    mi = Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.MinFilter(3))
    core = layer(CORE, np.asarray(mi).astype(float) / 255).filter(ImageFilter.GaussianBlur(.5 * s))
    res = screen(res, core, .55)
    # 3. bloom: tight glow, wide soft halo (lighter than on the dark X-ray: the photo is already bright)
    g = layer(GLOW, m)
    res = screen(res, g.filter(ImageFilter.GaussianBlur(3 * s)), .5)
    res = screen(res, g.filter(ImageFilter.GaussianBlur(12 * s)), .32)
    res = screen(res, g.filter(ImageFilter.GaussianBlur(36 * s)), .14)
    # 4. a few current pulses travelling the runs
    ys, xs = np.nonzero(m > .85)
    rnd = random.Random(seed)
    pulse = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(pulse)
    for i in rnd.sample(range(len(xs)), min(len(xs), int(40 * W * H / (1920 * 1440)))):
        x, y = xs[i], ys[i]
        r = rnd.uniform(1.2, 2.6) * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 238, 205))
    res = screen(res, pulse.filter(ImageFilter.GaussianBlur(.6 * s)), 1.0)
    res = screen(res, pulse.filter(ImageFilter.GaussianBlur(6 * s)), .6)
    res.save(out, quality=94)
    return out


if __name__ == "__main__":
    print(hero(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 5))
