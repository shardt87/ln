"""Sustainability mark for the CCS absorber bands (owner, Oct 22: "add a leaf for sustainability on the spaces in between
CCS"; then, with the Southwire "Growing Green" mark as the reference: "use this as reference ... all same colour, not
just one leaf green").

A sprig in the manner of that mark, drawn here (not traced) and in one colour: a gently curving stem, a leaf at the
top and three pairs of leaves growing larger toward the base, each pointed leaf bowed upward with a curved vein cut
through it to the band colour. The stem and the stacked leaves keep it legible at distance. Transparent ground;
writes screens/ccs_leaf.png (square)."""
import math
import os

from PIL import Image, ImageDraw

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screens")
INK = (61, 100, 72, 255)                                     # one green, a shade greener than the CCS lettering


def bez(p0, p1, p2, p3, n=80):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def stroke(d, pts, w0, w1, fill):
    for k, (a, b) in enumerate(zip(pts, pts[1:])):
        w = w0 + (w1 - w0) * k / max(1, len(pts) - 2)
        d.line([a, b], fill=fill, width=max(1, int(w)))
        d.ellipse([b[0] - w / 2, b[1] - w / 2, b[0] + w / 2, b[1] + w / 2], fill=fill)


def leaf(base, ang, L, W, bow):
    """Outline and vein of one leaf in image units: base, direction ang (deg, image axes, y down), length, half width,
    bow (+1 / -1 bends the tip toward local +y / -y, 0 straight)."""
    A = math.radians(ang)
    T = lambda x, y: (base[0] + x * math.cos(A) - y * math.sin(A), base[1] + x * math.sin(A) + y * math.cos(A))
    b = bow * W * 1.25                                       # tip lift: the leaves curl up as in the reference
    tip = (L, b)
    edge1 = bez((0, 0), (L * .10, W * 1.30), (L * .72, W * 1.25 + b * .6), tip)
    edge2 = bez(tip, (L * .80, -W * .55 + b * .9), (L * .30, -W * 1.05 + b * .2), (0, 0))
    vein = bez((L * .16, W * .10), (L * .40, W * .28 + b * .1), (L * .66, W * .25 + b * .45), (L * .88, b * .85), 40)
    return [T(*p) for p in edge1 + edge2], [T(*p) for p in vein]


def main(out=os.path.join(D, "ccs_leaf.png"), S=1200, ss=3):
    s = S * ss
    P = lambda p: (p[0] * s, p[1] * s)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cut = Image.new("L", (s, s), 0)
    c = ImageDraw.Draw(cut)
    # stem: from the foot, curving gently, up to the top leaf
    stem = bez((.47, .97), (.53, .78), (.47, .48), (.505, .22), 120)
    stroke(d, [P(p) for p in stem], s * .040, s * .014, INK)
    at = lambda t: stem[int(t * (len(stem) - 1))]
    # (stem position, direction deg, length, half width, bow): top leaf, then left / right pairs, larger toward the foot
    leaves = [(1.00, -96, .19, .060, 1),
              (.80, -158, .22, .078, 1), (.74, -24, .23, .080, -1),
              (.56, -170, .27, .095, 1), (.50, -12, .28, .098, -1),
              (.31, -178, .31, .110, 1), (.24, -4, .36, .125, -1)]
    for t, ang, L, W, bow in leaves:
        outline, vein = leaf(at(t), ang, L, W, bow)
        d.polygon([P(p) for p in outline], fill=INK)
        stroke(c, [P(p) for p in vein], s * .016, s * .005, 255)
    im.putalpha(Image.composite(Image.new("L", (s, s), 0), im.getchannel("A"), cut))
    bb = im.getbbox()                                        # centre the sprig on the square
    sq = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    cw, ch = bb[2] - bb[0], bb[3] - bb[1]
    sc = min(1.0, s * .96 / max(cw, ch))
    spr = im.crop(bb).resize((int(cw * sc), int(ch * sc)), Image.LANCZOS)
    sq.alpha_composite(spr, ((s - spr.width) // 2, (s - spr.height) // 2))
    sq.resize((S, S), Image.LANCZOS).save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
