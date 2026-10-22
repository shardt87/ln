"""Sustainability leaf for the CCS absorber bands (owner, Oct 22: "add a leaf for sustainability on the spaces in between
CCS"): a single leaf in the band lettering's dark sage, midrib and veins left as the band's light green, transparent
ground. Writes screens/ccs_leaf.png (1:1.2, upright, stem at the bottom)."""
import math
import os

from PIL import Image, ImageDraw

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screens")
INK, VEIN = (61, 92, 71, 255), (169, 189, 176, 255)


def main(out=os.path.join(D, "ccs_leaf.png"), W=1000, H=1200, ss=3):
    w, h = W * ss, H * ss
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # leaf outline: a pointed blade, widest a little below the middle, tip at the top, tilted 18 deg to the right
    tilt = math.radians(18)
    cx, cy, L, B = w * .5, h * .47, h * .40, w * .30
    rot = lambda x, y: (cx + x * math.cos(tilt) + y * math.sin(tilt), cy - x * math.sin(tilt) + y * math.cos(tilt))
    pts = []
    for k in range(121):
        t = -1 + 2 * k / 120                                   # -1 tip ... 1 base along the blade
        half = B * math.sin(math.pi * (t + 1) / 2) ** 1.1 * (1 - .18 * t)
        pts.append((half, t * L))
    outline = [rot(x, y) for x, y in pts] + [rot(-x, y) for x, y in reversed(pts)]
    d.polygon(outline, fill=INK)
    # stem
    d.line([rot(0, L * .98), rot(-w * .03, L * 1.32)], fill=INK, width=int(w * .035))
    # midrib and veins
    d.line([rot(0, -L * .9), rot(0, L * .98)], fill=VEIN, width=int(w * .018))
    hw = lambda t: B * math.sin(math.pi * (t + 1) / 2) ** 1.1 * (1 - .18 * t)
    for k in range(4):                                         # veins up and out from the midrib, inside the blade
        y0 = -L * .5 + k * L * .32
        for s in (-1, 1):
            ye = y0 - L * .02
            d.line([rot(0, y0 + L * .22), rot(s * hw(ye / L) * .72, ye)], fill=VEIN, width=int(w * .011))
    im.resize((W, H), Image.LANCZOS).save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
