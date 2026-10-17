"""Copper cable overlay: the model's cable routes (tray, duct bank, buried cable, HV cable, trenches) projected through
a hero camera onto its render and drawn as a soft copper glow. The brand colour goes on the cable, the product, while
the plant itself stays realistic.

    python blender/cable_overlay.py IN.png OUT.png [CAMERA_KEY]      # default camera SC1 (Strategy cover)
"""
import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CABLE = {"mv_tray": 1.0, "lv_tray": .8, "control_tray": .7, "hv_cable": 1.0, "duct_bank": .75, "mvlv_cable": .6,
         "cable_trench": .7}
COPPER = (214, 120, 60)          # halo
LINE = (196, 96, 40)             # Southwire copper


def camera(key):
    import re
    src = open(os.path.join(HERE, "pro_look.py")).read()
    m = re.search(r'k="%s".*?eye=\(([^)]*)\), target=\(([^)]*)\), lens=([\d.]+)' % key, src, re.S)
    eye = [float(v) for v in m.group(1).split(",")]
    tgt = [float(v) for v in m.group(2).split(",")]
    return eye, tgt, float(m.group(3))


def projector(eye, tgt, lens, W, H):
    sub = lambda a, b: [a[i] - b[i] for i in range(3)]
    dot = lambda a, b: sum(a[i] * b[i] for i in range(3))
    cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    norm = lambda a: [v / math.sqrt(dot(a, a)) for v in a]
    fwd = norm(sub(tgt, eye))
    right = norm(cross(fwd, [0, 0, 1]))
    up = cross(right, fwd)
    k = lens / 36.0 * max(W, H)                       # sensor fit AUTO: the 36 mm sensor spans the longer side

    def p(pt):
        d = sub(pt, eye)
        z = dot(d, fwd)
        if z <= 1:
            return None
        return (W / 2 + dot(d, right) / z * k, H / 2 - dot(d, up) / z * k)
    return p


def overlay(src, out, key="SC1"):
    model = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))
    im = Image.open(src).convert("RGB")
    W, H = im.size
    proj = projector(*camera(key), W, H)
    s = W / 1830
    line = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl, dh = ImageDraw.Draw(line), ImageDraw.Draw(halo)
    for r in model["routes"]:
        wgt = CABLE.get(r["type"])
        if not wgt:
            continue
        buried = r.get("z", 0) < 0
        z = max(r.get("z", 0), .3)                    # buried runs drawn on the ground they run under
        pts = [proj((x, y, z)) for x, y in r["points"]]
        a_line = int(255 * (.62 if buried else .95))
        for a, b in zip(pts, pts[1:]):
            if a and b:
                dh.line([a, b], fill=COPPER + (int(150 * wgt),), width=max(3, int(11 * s * wgt)))
                dl.line([a, b], fill=LINE + (a_line,), width=max(2, int(3.6 * s * wgt)))
    halo = halo.filter(ImageFilter.GaussianBlur(6 * s))
    res = im.convert("RGBA")
    res.alpha_composite(halo)
    res.alpha_composite(line.filter(ImageFilter.GaussianBlur(.6 * s)))
    res = res.convert("RGB")
    res.save(out)
    return out


if __name__ == "__main__":
    print(overlay(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "SC1"))
