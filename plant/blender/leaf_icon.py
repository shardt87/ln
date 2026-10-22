"""Sustainability leaf for the CCS absorber bands (owner, Oct 22: "add a leaf for sustainability on the spaces in between
CCS"; redrawn twice the same day: "didn't like the shape ... one big one", then "from the distance ... looks like just a
blob, make sure that it looks like a leaf from distance as well").

Drawn for legibility at distance, as a signage icon rather than an illustration: an elongated blade with a long
drawn-out tip and a strong stem (the silhouette alone reads as a leaf), split along the midrib by a wide band-coloured
gap into two halves in two greens (the light side catching the sun), and only three thick vein cuts per side, wide
enough to survive at a few pixels. Transparent ground; writes screens/ccs_leaf.png (square)."""
import math
import os

from PIL import Image, ImageDraw

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screens")
DARK, LIGHT, GAP = (52, 84, 62, 255), (92, 133, 98, 255), (0, 0, 0, 0)


def bez(p0, p1, p2, p3, n=100):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def stroke(d, pts, w0, w1, fill):
    """A tapered round-capped stroke along pts, width w0 at the start to w1 at the end."""
    for k, (a, b) in enumerate(zip(pts, pts[1:])):
        w = w0 + (w1 - w0) * k / max(1, len(pts) - 2)
        d.line([a, b], fill=fill, width=max(1, int(w)))
        d.ellipse([b[0] - w / 2, b[1] - w / 2, b[0] + w / 2, b[1] + w / 2], fill=fill)


def main(out=os.path.join(D, "ccs_leaf.png"), S=1200, ss=3):
    s = S * ss
    P = lambda p: (p[0] * s, p[1] * s)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base, tip = (.27, .73), (.92, .08)                      # leaf axis tilted 45 deg, tip up to the right
    # the two halves of the blade, each bounded by its edge and the (curved) midrib; the long tip is drawn out
    rib = bez(base, (.45, .58), (.70, .33), tip)
    upper = bez(base, (.05, .40), (.42, .02), tip)          # upper-left edge
    lower = bez(tip, (.98, .42), (.62, .92), base)          # lower-right edge
    d.polygon([P(p) for p in upper + list(reversed(rib))], fill=DARK)
    d.polygon([P(p) for p in rib + lower], fill=LIGHT)
    # stem: thick, slightly curved, continuing the midrib line out of the base
    stroke(d, [P(p) for p in bez((.33, .67), base, (.19, .82), (.11, .91), 60)], s * .045, s * .030, DARK)
    # cuts in the ground colour (transparent): a wide midrib gap and three thick veins per side, angled to the tip
    cut = Image.new("L", (s, s), 0)
    c = ImageDraw.Draw(cut)
    stroke(c, [P(p) for p in rib[4:92]], s * .034, s * .010, 255)
    ang = math.radians(-45)                                 # leaf axis direction (to the tip)
    ax = (math.cos(ang), math.sin(ang))
    for t, ln in ((.30, .25), (.50, .21), (.68, .15)):
        x, y = rib[int(t * (len(rib) - 1))]
        for sgn in (-1, 1):                                 # -1: upper-left half, +1: lower-right half
            nrm = (ax[1] * -sgn, -ax[0] * -sgn)              # perpendicular to the axis, toward that edge
            e = (x + (nrm[0] * .75 + ax[0] * .65) * ln, y + (nrm[1] * .75 + ax[1] * .65) * ln)
            m = (x + (nrm[0] * .45 + ax[0] * .15) * ln, y + (nrm[1] * .45 + ax[1] * .15) * ln)
            stroke(c, [P(p) for p in bez((x, y), m, m, e, 40)], s * .024, s * .008, 255)
    im.putalpha(Image.composite(Image.new("L", (s, s), 0), im.getchannel("A"), cut))
    im.resize((S, S), Image.LANCZOS).save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
