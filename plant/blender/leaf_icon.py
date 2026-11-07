"""Sustainability mark for the CCS absorber bands: the Southwire "Growing Green" sprig (owner, Oct 22: "add a leaf for
sustainability on the spaces in between CCS"; then "use this as reference ... all same colour"; then "use the same
model, you can use it since it's Southwire").

Taken from the owner-supplied mark (blender/ref/southwire_growing_green.jpg): the sprig is lifted off the white
ground, the "Growing Green" wordmark left out, and every leaf (grey and green in the original) recoloured one green;
the white vein cuts stay cut, so the band shows through. Upscaled with a smoothed edge; writes screens/ccs_leaf.png
(square, transparent)."""
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(HERE, "blender", "ref", "southwire_growing_green.jpg")
INK = (61, 100, 72)                                          # one green, a shade greener than the CCS lettering


def main(out=os.path.join(HERE, "screens", "ccs_leaf.png"), S=1200, up=6):
    im = Image.open(REF).convert("RGB")
    a = np.asarray(im).astype(float)
    ink = (a.min(axis=2) < 228).astype(float)                # any leaf, pale grey or green, is solid (white ground ~250)
    h, w = ink.shape
    ink[300:, :240] = 0                                      # the "Growing Green" wordmark, left of the stem foot
    m = Image.fromarray((ink * 255).astype(np.uint8), "L").filter(ImageFilter.MedianFilter(3))   # JPEG specks off
    m = m.resize((w * up, h * up), Image.BICUBIC).filter(ImageFilter.GaussianBlur(up * 1.3))
    m = m.point(lambda v: 0 if v < 112 else 255 if v > 144 else int((v - 112) * 255 / 32))   # crisp, anti-aliased edge
    bb = m.getbbox()
    m = m.crop(bb)
    side = int(max(m.size) * 1.04)
    sq = Image.new("L", (side, side), 0)
    sq.paste(m, ((side - m.width) // 2, (side - m.height) // 2))
    rgba = Image.new("RGBA", (side, side), INK + (0,))
    rgba.putalpha(sq)
    rgba.resize((S, S), Image.LANCZOS).save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
