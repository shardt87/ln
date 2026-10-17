"""Rooftop equipment on the plant's buildings (LOD 3, user review): packaged rooftop HVAC units on curbs, exhaust
fans, plumbing vents and a roof hatch with its guard rail, on every occupied building, e-house and module.

Count scales with roof area; every unit is placed on the building's own roof slab and tested against the geometry
already in the model (parapets, fans, stacks, cable entries), so nothing floats or clashes. The turbine hall's pitched
roof keeps its own powered roof fans and lightning protection (hall.py). Typical, not engineered.
"""
import re

import realism

KEEP = re.compile(r"building|house|e-house|room|module|PCM|warehouse|workshop|gallery|switchgear|treatment|NOC|"
                  r"^R[1-4][A-C]?:|^RH:|MCC|control|compression", re.I)
SKIP = re.compile(r"interior|canopy|skid|unloading|duct|damper|catalyst|aeroderivative|laydown|gas yard|pickup|"
                  r"cable pull|scaffold|underground|ground over|engine hall|electrolyzer|gatehouse|fire pump|"
                  r"rooftop|trailer|container|enclosure|filter|M&R 7", re.I)
ROOFC = ("roof", "building", "ehouse", "ccs", "swgr", "panel", "concrete", "rollup")


class Roofs(realism.Realism):
    def roof_of(self, it, boxes):
        fp = it["fp"]
        A = (fp[1] - fp[0]) * (fp[3] - fp[2])
        best = None
        for p in boxes:
            (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
            a = (x1 - x0) * (y1 - y0)
            if p["color"] in ROOFC and (a >= .45 * A or (p["color"] == "roof" and a >= 1000)) and it["z"][1] - 1.6 <= z1 <= it["z"][1] + .4 and z1 >= 9:
                if best is None or z1 > best[5] + .01 or (abs(z1 - best[5]) <= .01 and a > best[0]):
                    best = (a, x0, x1, y0, y1, z1)                  # the highest roof surface (the deck, not the body)
        return best

    def rtu(self, x, y, big, along_x):
        w, d, h = (9.5, 5.5, 4.2) if big else (6.5, 4.0, 3.2)
        if not along_x:
            w, d = d, w
        z = self.z
        if not self.free(x - w / 2 - .6, x + w / 2 + .6, y - d / 2 - .6, y + d / 2 + .6, z + .05, z + h + 2, 1.2):
            return False
        self.box(x - w / 2 - .4, x + w / 2 + .4, y - d / 2 - .4, y + d / 2 + .4, z, z + 1.0, "steel")      # roof curb
        self.box(x - w / 2, x + w / 2, y - d / 2, y + d / 2, z + 1.0, z + 1.0 + h, "equip")                # cabinet
        # condenser coil end and the fan(s) on top
        if along_x:
            self.box(x + w / 2 - 2.2, x + w / 2 + .05, y - d / 2 + .3, y + d / 2 - .3, z + 1.4, z + .8 + h, "bundle")
            fans = [(x + w / 2 - 1.6, y)] if not big else [(x + w / 2 - 1.6, y - 1.3), (x + w / 2 - 1.6, y + 1.3)]
        else:
            self.box(x - w / 2 + .3, x + w / 2 - .3, y + d / 2 - 2.2, y + d / 2 + .05, z + 1.4, z + .8 + h, "bundle")
            fans = [(x, y + d / 2 - 1.6)] if not big else [(x - 1.3, y + d / 2 - 1.6), (x + 1.3, y + d / 2 - 1.6)]
        for fx, fy in fans:
            self.rod((fx, fy, z + 1.0 + h), (fx, fy, z + 1.35 + h), 1.15, "fan", seg=16)
            self.rod((fx, fy, z + 1.35 + h), (fx, fy, z + 1.5 + h), .35, "fanhub", seg=10)
        # service access panels on the long side
        for k in (-1, 1):
            if along_x:
                self.box(x + k * w / 5 - .9, x + k * w / 5 + .9, y - d / 2 - .05, y - d / 2 + .02, z + 1.4, z + .6 + h, "cabinet")
            else:
                self.box(x - w / 2 - .05, x - w / 2 + .02, y + k * d / 5 - .9, y + k * d / 5 + .9, z + 1.4, z + .6 + h, "cabinet")
        self.count("rooftop HVAC units")
        return True

    def exhaust_fan(self, x, y):
        z = self.z
        if not self.free(x - 1.6, x + 1.6, y - 1.6, y + 1.6, z + .05, z + 3.5, .8):
            return False
        self.box(x - 1.3, x + 1.3, y - 1.3, y + 1.3, z, z + .9, "steel")                                  # curb
        self.rod((x, y, z + .9), (x, y, z + 2.1), .95, "fan", seg=16)                                     # fan body
        self.rod((x, y, z + 2.1), (x, y, z + 2.7), 1.55, "fan", r2=.35, seg=16)                           # mushroom hood
        self.count("exhaust fans")
        return True

    def vent(self, x, y):
        z = self.z
        if not self.free(x - .4, x + .4, y - .4, y + .4, z + .05, z + 2.4, .4):
            return False
        self.rod((x, y, z), (x, y, z + 1.9), .22, "pipe", seg=8)
        self.rod((x, y, z + 1.9), (x, y, z + 2.1), .3, "pipe", seg=8)
        self.count("roof vents")
        return True

    def hatch(self, x, y):
        z = self.z
        if not self.free(x - 3, x + 3, y - 3, y + 3, z + .05, z + 4, .6):
            return False
        self.box(x - 1.6, x + 1.6, y - 1.9, y + 1.9, z, z + 1.1, "steel")                                 # curb
        self.box(x - 1.75, x + 1.75, y - 2.05, y + 2.05, z + 1.1, z + 1.3, "door")                        # lid
        for (px, py) in ((x - 2.6, y - 2.9), (x + 2.6, y - 2.9), (x - 2.6, y + 2.9), (x + 2.6, y + 2.9)):
            self.rod((px, py, z), (px, py, z + 3.5), .08, "rail", seg=6)                                  # guard posts
        for zz in (1.8, 3.5):
            self.rod((x - 2.6, y - 2.9, z + zz), (x + 2.6, y - 2.9, z + zz), .06, "rail", seg=6)
            self.rod((x - 2.6, y + 2.9, z + zz), (x + 2.6, y + 2.9, z + zz), .06, "rail", seg=6)
            self.rod((x - 2.6, y - 2.9, z + zz), (x - 2.6, y + 2.9, z + zz), .06, "rail", seg=6)
        self.count("roof hatches")
        return True

    def building(self, it, roof):
        _, x0, x1, y0, y1, z = roof
        self.z = z
        A = (x1 - x0) * (y1 - y0)
        along_x = (x1 - x0) >= (y1 - y0)
        m = 4.0
        X0, X1, Y0, Y1 = x0 + m, x1 - m, y0 + m, y1 - m
        if X1 - X0 < 6 or Y1 - Y0 < 5:
            return
        self.new(it["layer"], f"{it['name'].split(':')[0].split('(')[0].strip()}: rooftop HVAC, exhaust fans, vents",
                 (round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1)), (round(z, 1), round(z + 6.5, 1)),
                 info="Packaged rooftop units on curbs, exhaust fans, plumbing vents and the roof hatch (typical).")
        L, D = (X1 - X0, Y1 - Y0) if along_x else (Y1 - Y0, X1 - X0)
        at = (lambda u, v: (X0 + u, Y0 + v)) if along_x else (lambda u, v: (X0 + v, Y0 + u))
        big = A >= 1800 and D >= 12
        n_rtu = max(1, min(6, round(A / 2600)))
        placed = 0
        for k in range(n_rtu * 3):
            if placed >= n_rtu:
                break
            u = L * ((k % n_rtu) + .5) / n_rtu
            v = D * (.5 if D < 30 else (.33 if (k // n_rtu) % 2 == 0 else .66))
            v += (k // n_rtu) * 2.5 * (1 if k % 2 else -1)
            x, y = at(u, min(max(v, 3.5), D - 3.5))
            placed += self.rtu(x, y, big, along_x)
        n_fan = max(1, min(8, round(A / 1700)))
        for k in range(n_fan):
            u = L * (k + .25) / n_fan
            v = D * (.18 if k % 2 == 0 else .82)
            x, y = at(u, min(max(v, 2), D - 2))
            if not self.exhaust_fan(x, y):
                self.exhaust_fan(*at(min(u + 4, L - 2), min(max(v, 2), D - 2)))
        for k in range(max(2, min(6, round(A / 1500)))):
            u = L * (k + .7) / max(2, min(6, round(A / 1500)))
            self.vent(*at(min(u, L - 1), D * (.08 if k % 2 else .92)))
        if A >= 1200:
            for u in (L - 4.5, 4.5, L / 2):
                if self.hatch(*at(u, D * .5 if D < 14 else D * .25)):
                    break



def build(item, items, parts, routes):
    R = Roofs(item, items, parts, routes)
    boxes = {}
    for p in parts:
        if p["kind"] == "box":
            boxes.setdefault(p["item"], []).append(p)
    todo = []
    for it in list(items):
        fp = it.get("fp")
        if not fp or len(fp) != 4 or not KEEP.search(it["name"]) or SKIP.search(it["name"]):
            continue
        if (fp[1] - fp[0]) * (fp[3] - fp[2]) < 450 or it["z"][1] < 9:
            continue
        roof = R.roof_of(it, boxes.get(it["id"], ()))
        if roof:
            todo.append((it, roof))
    for it, roof in todo:
        R.building(it, roof)
    return dict(R.counts, buildings=len(todo))
