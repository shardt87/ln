"""Station electrical at LOD 3 (detail cycle 2): e-houses, auxiliary transformers, emergency
diesels and the duct-bank network.

- Auxiliary and station transformers (UAT, T4, LCT, T-R2x, T-R3, T-R4): 13.8 kV bushings in an air
  terminal chamber, an LV cable-termination box, a control / marshalling cabinet, nameplate and
  hazard sign, ground leads.
- E-houses (R2A-C, R3, R4): steel skid with lifting lugs, landings and stairs at both doors,
  bottom cable-entry transit frames with the cables rising from the duct bank, emergency light
  and fire-extinguisher cabinet at each door, rooftop HVAC condensers, ground leads.
- Emergency diesel generators: a weatherproof enclosure each with radiator, exhaust silencer and
  stack, a sub-base day tank, fuel fill box, and its own output breaker cabinet.
- Duct-bank manholes at every bend and about every 300 ft of run, and handholes at the feeder
  ends, with cast covers flush with grade.
All typical, not engineered; drawn footprints and heights kept.
"""
import math

import fuel
from fuel import box, rod, find, on
import yard


def dress(flag):
    fuel.D = flag


def transformers():
    names = ("UAT-", "T4-", "LCT-", "T-R2", "T-R3", "T-R4")
    for it in fuel.G["items"]:
        if not it["name"].startswith(names) or it["layer"] != "BASE_ELECTRICAL":
            continue
        x0, x1, y0, y1 = it["fp"]
        h = it["z"][1]
        W, D = x1 - x0, y1 - y0
        tx0, tx1 = x0 + W * .2, x1 - W * .2
        ty0, ty1 = y0 + D * .08, y1 - D * .08
        th = h * .72
        cx = (tx0 + tx1) / 2
        on(it)
        dress(True)
        box(tx0 + .5, tx1 - .5, ty1 - .1, ty1 + 1.6, th - 3.2, th - .3, "xfmr")            # MV air terminal chamber
        for k in (-1, 0, 1):
            rod((cx + k * (tx1 - tx0) * .22, ty1 + .8, th - .3), (cx + k * (tx1 - tx0) * .22, ty1 + .8, th + 1.6),
                .3, "insulator", seg=8)
        box(tx0 + .6, tx1 - .6, ty0 - 1.5, ty0 + .1, 1.6, th - 1.2, "xfmr")                # LV cable box
        rod((cx, ty0 - .8, 1.6), (cx, ty0 - .8, .2), .55, "steel", seg=8)                 # cable conduit down
        box(tx1 + .2, tx1 + 1.2, ty0 + .5, ty0 + 2.5, 1.5, 5.5, "cabinet")               # marshalling cabinet
        box(tx0 - .12, tx0 - .02, (ty0 + ty1) / 2 - .8, (ty0 + ty1) / 2 + .8, th - 3, th - 2, "sign")   # nameplate
        box(cx - .9, cx + .9, ty0 - 1.62, ty0 - 1.52, th - 2.6, th - 1.6, "amber")         # hazard sign
        for (gx_, gy_) in ((tx0, ty0), (tx1, ty1)):
            rod((gx_, gy_, 1), (gx_, gy_, .1), .09, "copper", seg=4)
        dress(False)


def ehouses():
    for tag in ("R2A", "R2B", "R2C", "R3", "R4"):
        it = next((i for i in fuel.G["items"] if i["tag"] == tag), None)
        if it is None:
            continue
        x0, x1, y0, y1 = it["fp"]
        h = it["z"][1]
        on(it)
        dress(True)
        along_x = (x1 - x0) >= (y1 - y0)
        # skid lifting lugs at the corners
        for (x, y) in ((x0 + 1, y0), (x1 - 1, y0), (x0 + 1, y1), (x1 - 1, y1)):
            box(x - .3, x + .3, y - .25, y + .25, 2.5, 3.6, "steel")
        # doors on the long faces near each end: landing, stair, emergency light, extinguisher cabinet
        faces = ((y0, -1), (y1, 1)) if along_x else ((x0, -1), (x1, 1))
        for (f, s) in faces[:1]:
            for u in ((x0 + 5, x1 - 8) if along_x else (y0 + 5, y1 - 8)):
                if along_x:
                    box(u - 1, u + 3, f + s * 4, f, 2.2, 2.5, "grating")                   # landing
                    for st in range(4):
                        z = 2.2 - .5 * (st + 1)
                        box(u - 1, u + 3, f + s * (4 + st * .9), f + s * (4.9 + st * .9), z - .1, z, "grating")
                    rod((u - 1, f + s * 4, 2.5), (u - 1, f + s * 4, 5.9), .06, "rail", seg=4)
                    rod((u + 3, f + s * 4, 2.5), (u + 3, f + s * 4, 5.9), .06, "rail", seg=4)
                    box(u + .2, u + 1.8, f + s * .12, f + s * .3, 8.2, 8.7, "lamp")           # emergency light
                    box(u + 3.4, u + 4.6, f + s * .02, f + s * .4, 3.5, 5.6, "red")          # extinguisher cabinet
                else:
                    box(f + s * 4, f, u - 1, u + 3, 2.2, 2.5, "grating")
                    for st in range(4):
                        z = 2.2 - .5 * (st + 1)
                        box(f + s * (4 + st * .9), f + s * (4.9 + st * .9), u - 1, u + 3, z - .1, z, "grating")
                    box(f + s * .12, f + s * .3, u + .2, u + 1.8, 8.2, 8.7, "lamp")
                    box(f + s * .02, f + s * .4, u + 3.4, u + 4.6, 3.5, 5.6, "red")
        # bottom cable entry: transit frames under the floor and cables rising from the duct bank
        n = max(2, int(((x1 - x0) if along_x else (y1 - y0)) // 15))
        for m in range(n):
            u = (x0 if along_x else y0) + ((x1 - x0) if along_x else (y1 - y0)) * (m + .5) / n
            if along_x:
                box(u - 1.5, u + 1.5, y1 - 2, y1 - .5, 0, 2.5, "steel")
                for c in range(4):
                    rod((u - 1.1 + c * .7, y1 - 1.25, 0), (u - 1.1 + c * .7, y1 - 1.25, 2.4), .14, "cable_tc", seg=6)
            else:
                box(x1 - 2, x1 - .5, u - 1.5, u + 1.5, 0, 2.5, "steel")
                for c in range(4):
                    rod((x1 - 1.25, u - 1.1 + c * .7, 0), (x1 - 1.25, u - 1.1 + c * .7, 2.4), .14, "cable_tc", seg=6)
        # rooftop HVAC condensers
        for m in range(2 if (x1 - x0) * (y1 - y0) < 2500 else 4):
            u = (x0 if along_x else y0) + ((x1 - x0) if along_x else (y1 - y0)) * (m + .5) / (2 if (x1 - x0) * (y1 - y0) < 2500 else 4)
            cxr, cyr = (u, (y0 + y1) / 2) if along_x else ((x0 + x1) / 2, u)
            box(cxr - 2.5, cxr + 2.5, cyr - 2, cyr + 2, h + .1, h + 3, "machine")
            rod((cxr, cyr, h + 3), (cxr, cyr, h + 3.3), 1.5, "fan", seg=14)
        rod((x0 + .5, y0 + .5, 2.5), (x0 + .5, y0 + .5, .1), .09, "copper", seg=4)          # ground lead
        dress(False)


def diesels():
    for k in (1, 2):
        it = find(f"EDG-{k}:")
        x0, x1, y0, y1 = it["fp"]
        it["info"] = (it.get("info") or "") + " Weatherproof enclosure with radiator, silencer and stack, " \
                                               "sub-base day tank, fuel fill box and output breaker (typical)."
        yard.genset_enclosure(it, 13, "ehouse", stack_top=22, fans=3)
        on(it)
        dress(True)
        box(x0 + 2, x1 - 2, y0 + .5, y1 - .5, 0, .5, "steel")                              # sub-base day tank
        box(x1 - 4, x1 - 2, y0 - .4, y0, 2, 4, "red")                                        # fuel fill box
        box(x0 + 1, x0 + 4, y0 - .45, y0, 1, 7, "cabinet")                                  # output breaker
        dress(False)


def manholes():
    fuel.new_item("ROUTES_BASE", "Duct-bank manholes and handholes", (0, 2420, 0, 1920), (0, .6),
                  basis="typical", register=False, sheet="typical (station electrical)",
                  info="Precast manholes at duct-bank bends and about every 300 ft of run; handholes at feeder ends.")
    seen = set()
    for r in fuel.G["routes"]:
        if r["type"] not in ("duct_bank", "mvlv_cable") or r["z"] >= 0:
            continue
        pts = r["points"]
        cand = []
        for k in range(1, len(pts) - 1):
            cand.append((pts[k], 3.5))                                                      # bends: manholes
        for a, b in zip(pts, pts[1:]):
            L = abs(b[0] - a[0]) + abs(b[1] - a[1])
            n = int(L // 300)
            for m in range(1, n + 1):
                t = m / (n + 1)
                cand.append(((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), 3.5))
        if r.get("sheet") == "typical (wiring applications)":
            cand.append((pts[0], 1.6))                                                      # handhole at the feeder end
        for (p, hw) in cand:
            key = (round(p[0] / 8), round(p[1] / 8))
            if key in seen:
                continue
            seen.add(key)
            x, y = p
            if not _clear(x, y, hw):
                continue
            box(x - hw, x + hw, y - hw, y + hw, 0, .42, "concrete", layer=r["layer"])
            if hw > 2:
                rod((x, y, .42), (x, y, .5), 1.4, "fanhub", seg=16, layer=r["layer"])     # cast cover
            else:
                box(x - 1.2, x + 1.2, y - 1.2, y + 1.2, .42, .48, "fanhub", layer=r["layer"])


def _clear(x, y, hw):
    """No equipment, building or pad above grade over the spot (roads and gravel are fine)."""
    for it in fuel.G["items"]:
        f = it["fp"]
        if it["layer"] == "SITE" or it["z"][1] < .7:
            continue
        if f[0] - .5 < x + hw and f[1] + .5 > x - hw and f[2] - .5 < y + hw and f[3] + .5 > y - hw:
            if f[1] - f[0] > 1500 or f[3] - f[2] > 1500:              # site-wide dressing items
                continue
            return False
    return True


def build():
    transformers()
    ehouses()
    diesels()


def build_late():
    manholes()
