"""Copper cable overlay: the model's cable routes projected through a hero camera onto its render, so the brand colour
sits on the cable (the product) and the plant itself stays realistic.

Delivery:
- three tiers: the power spine (MV tray, 230 kV cable) bold with a copper glow; feeders (LV / control tray) finer;
  buried runs (duct banks, direct-buried cable, trenches) thin and dashed;
- occlusion: every sample along a route is tested against the plant's solid volumes (buildings, HRSGs, tanks,
  equipment) on its line of sight to the camera; hidden stretches fall back to a faint ghost line;
- burnished copper core, warm highlight and soft glow, drawn at 3x and filtered down for clean lines.

    python blender/cable_overlay.py IN.png OUT.png [CAMERA_KEY]      # default camera SC1 (Strategy cover)
"""
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
sys.path.insert(0, PLANT)

TIER = {"mv_tray": "spine", "hv_cable": "spine", "lv_tray": "feeder", "control_tray": "feeder",
        "duct_bank": "buried", "mvlv_cable": "buried", "cable_trench": "buried"}
# (core width px at 1830 wide, core alpha, glow width, glow alpha)
STYLE = {"spine": (4.2, 1.0, 16, .55), "feeder": (2.2, .85, 8, .3), "buried": (1.6, .7, 0, 0)}
CORE = (170, 86, 42)          # burnished copper (Southwire)
HI = (246, 190, 140)          # warm highlight along the spine
GLOW = (224, 132, 68)
GHOST = .16                   # alpha factor where the run is hidden behind the plant
SS = 3                        # supersampling


def camera(key):
    src = open(os.path.join(HERE, "pro_look.py")).read()
    m = re.search(r'k="%s".*?eye=\(([^)]*)\), target=\(([^)]*)\), lens=([\d.]+)' % key, src, re.S)
    return ([float(v) for v in m.group(1).split(",")], [float(v) for v in m.group(2).split(",")], float(m.group(3)))


def projector(eye, tgt, lens, W, H):
    eye, tgt = np.array(eye), np.array(tgt)
    fwd = (tgt - eye) / np.linalg.norm(tgt - eye)
    right = np.cross(fwd, [0, 0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    k = lens / 36.0 * max(W, H)                       # sensor fit AUTO: the 36 mm sensor spans the longer side

    def p(P):
        d = P - eye
        z = d @ fwd
        return np.stack([W / 2 + (d @ right) / z * k, H / 2 - (d @ up) / z * k], -1), z
    return p


def solids(model):
    """Axis-aligned volumes that hide cable: tall parts of buildings and equipment (not the trays themselves)."""
    from realism import _pbox
    skip_layers = ("ROUTES", "UNDERGROUND", "SITE")
    out = []
    for p in model["parts"]:
        if any(s in p["layer"] for s in skip_layers) or p["color"] in ("steel", "grating", "rail", "stair", "pipe",
                                                                         "cable", "cable_mv", "cable_tc", "cable_mc"):
            continue
        b = _pbox(p)
        area = (b[3] - b[0]) * (b[4] - b[1])
        if (b[5] - b[2] < 6 and area < 4000) or (area < 150 and b[5] - b[2] < 20):
            continue                                   # small / flat bits don't hide cable; roofs and walls do
        out.append(b)
    return np.array(out)


def occluded(eye, P, B):
    """For each sample P (n,3): is the segment eye->P blocked by any box in B (m,6)? Slab test, vectorised."""
    eye = np.array(eye)
    hid = np.zeros(len(P), bool)
    for i in range(0, len(P), 4000):
        Q = P[i:i + 4000]
        d = Q - eye                                    # (n,3)
        inv = 1.0 / np.where(np.abs(d) < 1e-9, 1e-9, d)
        t0 = (B[None, :, 0:3] - eye) * inv[:, None, :]
        t1 = (B[None, :, 3:6] - eye) * inv[:, None, :]
        tmin = np.minimum(t0, t1).max(-1)
        tmax = np.maximum(t0, t1).min(-1)
        hit = (tmax >= np.maximum(tmin, 0)) & (tmin < .985)   # blocked before reaching the cable
        hid[i:i + 4000] = hit.any(-1)
    return hid


def overlay(src, out, key="SC1"):
    model = json.load(open(os.path.join(PLANT, "sw3x1_model.json")))
    im = Image.open(src).convert("RGB")
    W, H = im.size
    eye, tgt, lens = camera(key)
    proj = projector(eye, tgt, lens, W * SS, H * SS)
    s = W / 1830 * SS
    B = solids(model)
    layers = {t: (Image.new("RGBA", (W * SS, H * SS)), Image.new("RGBA", (W * SS, H * SS))) for t in STYLE}
    hi = Image.new("RGBA", (W * SS, H * SS))
    dhi = ImageDraw.Draw(hi)
    for r in model["routes"]:
        tier = TIER.get(r["type"])
        if not tier:
            continue
        z = max(r.get("z", 0), .4)
        pts = np.array([[x, y, z] for x, y in r["points"]], float)
        # densify to ~6 ft samples so occlusion and dashes follow the run
        S = []
        for a, b in zip(pts, pts[1:]):
            n = max(1, int(np.linalg.norm(b - a) / 6))
            S += [a + (b - a) * k / n for k in range(n)]
        S.append(pts[-1])
        S = np.array(S)
        hid = occluded(eye, S + [0, 0, 1.5], B)
        xy, zc = proj(S)
        cw, ca, gw, ga = STYLE[tier]
        core, glow = layers[tier]
        dc, dg = ImageDraw.Draw(core), ImageDraw.Draw(glow)
        for k in range(len(S) - 1):
            if zc[k] <= 1 or zc[k + 1] <= 1:
                continue
            if tier == "buried" and (k // 2) % 2:      # dashes for buried runs
                continue
            f = GHOST if (hid[k] or hid[k + 1]) else 1.0
            seg = [tuple(xy[k]), tuple(xy[k + 1])]
            dc.line(seg, fill=CORE + (int(255 * ca * f),), width=max(1, int(cw * s)))
            if gw:
                dg.line(seg, fill=GLOW + (int(255 * ga * f),), width=max(1, int(gw * s)))
            if tier == "spine" and f == 1.0:
                dhi.line(seg, fill=HI + (200,), width=max(1, int(1.3 * s)))
    res = im.resize((W * SS, H * SS), Image.LANCZOS).convert("RGBA")
    for t in ("buried", "feeder", "spine"):
        core, glow = layers[t]
        if STYLE[t][2]:
            res.alpha_composite(glow.filter(ImageFilter.GaussianBlur(7 * s / SS * SS / 2)))
        res.alpha_composite(core)
    res.alpha_composite(hi)
    res.convert("RGB").resize((W, H), Image.LANCZOS).save(out)
    return out


if __name__ == "__main__":
    print(overlay(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "SC1"))
