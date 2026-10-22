"""Sustainability leaf for the CCS absorber bands (owner, Oct 22: "add a leaf for sustainability on the spaces in between
CCS"; redrawn the same day: "I didn't like the shape of this leaf ... one big one in between those CCS"). A single
smooth leaf drawn from cubic Bezier curves, tip up and to the right, a curved midrib with sweeping veins and a curled
stem, in the lettering's dark sage; the veins are cut out in the band's light green. Transparent ground; writes
screens/ccs_leaf.png (square)."""
import os

from PIL import Image, ImageDraw

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screens")
INK, VEIN = (61, 92, 71, 255), (169, 189, 176, 255)


def bez(p0, p1, p2, p3, n=80):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def stroke(d, pts, w0, w1, fill):
    """A tapered stroke along pts, width w0 at the start to w1 at the end."""
    for k, (a, b) in enumerate(zip(pts, pts[1:])):
        w = w0 + (w1 - w0) * k / max(1, len(pts) - 2)
        d.line([a, b], fill=fill, width=max(1, int(w)))
        d.ellipse([b[0] - w / 2, b[1] - w / 2, b[0] + w / 2, b[1] + w / 2], fill=fill)


def main(out=os.path.join(D, "ccs_leaf.png"), S=1200, ss=3):
    s = S * ss
    P = lambda x, y: (x * s, y * s)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base, tip = (.30, .74), (.86, .12)
    # blade: upper-left edge bulging out, lower-right edge fuller, both meeting in a fine point at the tip
    upper = bez(base, (.08, .46), (.40, .10), tip)
    lower = bez(tip, (.86, .50), (.62, .80), base)
    d.polygon([P(*p) for p in upper + lower], fill=INK)
    # curled stem out of the base
    stroke(d, [P(*p) for p in bez((.34, .69), (.24, .82), (.16, .88), (.10, .90), 40)], s * .028, s * .014, INK)
    # midrib: a gentle curve from the base toward the tip, tapering
    rib = bez(base, (.46, .56), (.66, .34), (.80, .18), 80)
    stroke(d, [P(*p) for p in rib], s * .020, s * .006, VEIN)
    # veins: sweeping from the midrib toward the tip side of each edge, shorter toward the tip
    for t, ln in ((.18, .20), (.36, .19), (.54, .16), (.72, .11)):
        i = int(t * (len(rib) - 1))
        x, y = rib[i]
        stroke(d, [P(*p) for p in bez((x, y), (x - .04 * ln / .2, y - .05 * ln / .2), (x - .10 * ln / .2, y - .12 * ln / .2),
                                    (x - .11 * ln / .2, y - .19 * ln / .2), 30)], s * .011, s * .003, VEIN)   # to the upper edge
        stroke(d, [P(*p) for p in bez((x, y), (x + .06 * ln / .2, y), (x + .13 * ln / .2, y - .03 * ln / .2),
                                    (x + .18 * ln / .2, y - .08 * ln / .2), 30)], s * .011, s * .003, VEIN)   # to the lower edge
    # trim anything outside the blade (vein tips) by re-masking with the blade shape plus the stem
    mask = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([P(*p) for p in upper + lower], fill=255)
    stroke(md, [P(*p) for p in bez((.34, .69), (.24, .82), (.16, .88), (.10, .90), 40)], s * .028, s * .014, 255)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (s, s), 0), mask))
    im.resize((S, S), Image.LANCZOS).save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
