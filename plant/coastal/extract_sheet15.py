#!/usr/bin/env python3
"""Reference geometry for the coastal variant from sheet SK-3X1-15 (needs PyMuPDF and the PDF).

Both panels draw the 2,420 x 1,920 ft compound to scale, so the compound frame gives
the transform to model feet (X east, Y north, origin at the SW compound corner).
Every numbered key item is matched to the filled shape its label sits on (or nearest to).
Writes plant/reference/sk3x1_rev14_sheet15.json, which build_coastal.py and
verify_coastal.py read, so neither needs the PDF.

    python3 plant/coastal/extract_sheet15.py SK-3X1_Drawing_Set_Rev14.pdf
"""
import json
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "reference", "sk3x1_rev14_sheet15.json")

# panel windows in PDF points (A: onshore terminal, B: FSRU) and the compound frame inside each
PANELS = {"A": dict(win=(24, 102, 810, 392), frame=(32.4, 118.7, 350.4, 371.0)),
          "B": dict(win=(24, 427, 810, 716), frame=(32.4, 443.4, 350.4, 695.7))}
KEYS = {"A": range(1, 12), "B": range(12, 17)}


def main(pdf):
    page = fitz.open(pdf)[14]
    drawings = page.get_drawings()
    words = page.get_text("words")
    out = dict(source=os.path.basename(pdf), sheet="SK-3X1-15", panels={})
    for name, P in PANELS.items():
        wx0, wy0, wx1, wy1 = P["win"]
        fx0, fy0, fx1, fy1 = P["frame"]
        s = 2420 / (fx1 - fx0)
        X = lambda px: round((px - fx0) * s, 1)
        Y = lambda py: round((fy1 - py) * s, 1)
        inside = lambda r: r.x0 >= wx0 and r.x1 <= wx1 and r.y0 >= wy0 and r.y1 <= wy1
        shapes, lines = [], []
        shore, boundary = None, None
        for g in drawings:
            r = g["rect"]
            if not inside(r):
                continue
            ops = "".join(i[0] for i in g["items"])
            if r.width == 0 and r.height > 250:
                shore = X(r.x0)
                continue
            if g.get("dashes") and g["dashes"] not in ("[] 0",) and g.get("fill") is None:
                pts = []
                for it in g["items"]:
                    if it[0] == "l":
                        for p in it[1:3]:
                            q = (X(p.x), Y(p.y))
                            if not pts or pts[-1] != q:
                                pts.append(q)
                lines.append(dict(pts=pts, bbox=[X(r.x0), X(r.x1), Y(r.y1), Y(r.y0)], ops=ops))
                continue
            if g.get("fill") is None or (r.width > 200 and r.height > 200):
                continue
            if g.get("dashes") and g["dashes"] != "[] 0":             # dashed, filled: terminal boundary
                boundary = [X(r.x0), X(r.x1), Y(r.y1), Y(r.y0)]
                continue
            teal_label = abs(r.width - 8.9) < .2 and g["fill"][2] < .6
            if teal_label or (r.width > 50 and r.height < 5):          # key labels, scale-bar cells
                continue
            shapes.append(dict(r=r, circle=ops.startswith("c"), poly=ops.startswith("l")))
        # key labels: the small numbers inside the teal circles
        keys = {}
        for (x0, y0, x1, y1, w, *_) in words:
            if not w.isdigit() or int(w) not in KEYS[name]:
                continue
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if not (wx0 < cx < wx1 and wy0 < cy < wy1) or cx < fx1:
                continue

            def dist(sh):
                r = sh["r"]
                dx = max(r.x0 - cx, 0, cx - r.x1)
                dy = max(r.y0 - cy, 0, cy - r.y1)
                return (round((dx * dx + dy * dy) ** .5, 1), r.width * r.height)
            cands = [sh for sh in shapes if not (sh["circle"] and 11 < sh["r"].width < 14)]   # not cargo domes
            best = min(cands, key=dist, default=None)
            if best is None or dist(best)[0] > 14:
                continue
            r = best["r"]
            keys[w] = dict(fp=[X(r.x0), X(r.x1), Y(r.y1), Y(r.y0)],
                           shape="circle" if best["circle"] else ("hull" if best["poly"] else "rect"))
        # circles that sit inside the two hulls (cargo tanks) and the terminal boundary
        domes = []
        for sh in shapes:
            r = sh["r"]
            if sh["circle"] and 11 < r.width < 14:
                domes.append([round((X(r.x0) + X(r.x1)) / 2, 1), round((Y(r.y0) + Y(r.y1)) / 2, 1),
                              round((r.width) * s, 1)])
        vessels = [[X(sh["r"].x0), X(sh["r"].x1), Y(sh["r"].y1), Y(sh["r"].y0)] for sh in shapes if sh["poly"]]
        out["panels"][name] = dict(vessels=vessels, ft_per_pt=round(s, 4), shoreline_x=shore, boundary=boundary, keys=keys,
                                   cargo_domes=sorted(domes, key=lambda d: (d[0], d[1])), dashed=lines)
    json.dump(out, open(OUT, "w"), indent=1)
    for n, p in out["panels"].items():
        print(f"panel {n}: shoreline x = {p['shoreline_x']} ft, {len(p['keys'])} keys, "
              f"{len(p['cargo_domes'])} cargo domes, {len(p['dashed'])} dashed runs")
    print("wrote", OUT)


if __name__ == "__main__":
    main(sys.argv[1])
