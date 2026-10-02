#!/usr/bin/env python3
"""Presentation board for the SK-3X1 pro renders ("Measured Light").

One sheet, 4800 x 3200 px (plus a PDF at 300 dpi, 16 x 10.67 in):
- P1 as the dominant plate, P2 / P3 stacked beside it, P4-P6 in a row;
- a hairline key plan drawn from the verified model, with the view cone of every plate;
- a sun-angle diagram, scale bar and north point;
- sparse type: Instrument Serif (names), Jura (labels), IBM Plex Mono (numbers).

    python3 plant/blender/board.py plant/renders/pro              # inland plant, P1-P6
    python3 plant/blender/board.py plant/renders/coastal coastal  # sheet 15 coastal variant
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
FONTS = os.path.join(HERE, "fonts")

S = 2                                  # supersampling factor
W, H = 4800 * S, 3200 * S
PAPER = (239, 237, 231)
INK = (29, 36, 41)
GRAPHITE = (92, 101, 107)
HAIR = (170, 172, 168)
COPPER = (176, 104, 50)
f = lambda name, size: ImageFont.truetype(os.path.join(FONTS, name), int(size * S))

# The hero lists live in pro_look.py, which imports bpy; read just those assignments.
_src = open(os.path.join(HERE, "pro_look.py")).read()
_env = {"dict": dict}
for _name in ("HEROES", "COASTAL_A", "COASTAL_B"):
    _i = _src.index(f"{_name} = [")
    exec(_src[_i:_src.index("\n]\n", _i) + 3], _env)
HERO = {h["k"]: h for n in ("HEROES", "COASTAL_A", "COASTAL_B") for h in _env[n]}

# one board per scene: plates (dominant, two stacked, a row of three), key plan window and apparatus
BOARDS = {
    "inland": dict(main="P1", right=("P2", "P3"), row=("P4", "P5", "P6"), cones=("P1", "P2", "P3", "P4", "P5", "P6"),
                   window=(-420, 2540, -520, 2140), overlay=None, sun=(24, 258), out="SK-3X1_presentation_board",
                   subtitle="SK-3X1  ·  REVISION 14  ·  PRESENTATION PLATES", sheet="SHEET 01 / 01",
                   names={"P2": "Transformer bays from the access road"}),
    "coastal": dict(main="C1", right=("C2", "C3"), row=("C5", "F1", "F3"), cones=("C1", "C2", "C3", "C5"),
                    window=(-600, 3100, -300, 5500), overlay="sk3x1_coastal_A.json", sun=(28, 140), bar=500,
                    out="SK-3X1-15_coastal_board",
                    subtitle="SK-3X1-15  ·  REVISION 14  ·  LNG MARINE TERMINAL, COASTAL VARIANT", sheet="SHEET 15 / 16",
                    names={"C2": "LNG carrier at the berth", "F1": "Variant B: FSRU and carrier, ship to ship",
                           "F3": "Variant B: FSRU 6.4 km offshore"}),
}


def tracked(d, x, y, text, font, fill, track):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track * S
    return x


def tw(d, text, font, track):
    return sum(d.textlength(c, font=font) for c in text) + track * S * (len(text) - 1)


def place(board, path, box):
    x0, y0, x1, y1 = [int(v * S) for v in box]
    im = Image.open(path).convert("RGB")
    im = im.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    board.paste(im, (x0, y0))


def caption(d, x, y, key, title, width):
    mono, lab = f("IBMPlexMono-Regular.ttf", 21), f("Jura-Light.ttf", 23)
    xe = tracked(d, x * S, y * S, key, mono, COPPER, 1.5)
    d.line([(xe + 14 * S, (y + 13) * S), (xe + 38 * S, (y + 13) * S)], fill=COPPER, width=S)
    tracked(d, xe + 52 * S, y * S - 1 * S, title.upper(), lab, INK, 3.2)


def key_plan(d, box, B):
    model = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))
    coastal = None
    if B["overlay"]:
        ov = json.load(open(os.path.join(PLANT, "coastal", B["overlay"])))
        model["items"] += ov["items"]
        coastal = ov["coastal"]
    x0, y0, x1, y1 = box
    # world window: compound plus room for camera positions
    wx0, wx1, wy0, wy1 = B["window"]
    sc = min((x1 - x0) / (wx1 - wx0), (y1 - y0) / (wy1 - wy0))
    ox = x0 + ((x1 - x0) - (wx1 - wx0) * sc) / 2
    oy = y0 + ((y1 - y0) - (wy1 - wy0) * sc) / 2
    P = lambda x, y: ((ox + (x - wx0) * sc) * S, (oy + (wy1 - y) * sc) * S)
    # sea, as a quiet tint north of the shoreline
    if coastal:
        sh = coastal["shoreline_y"]
        d.rectangle([P(wx0, wy1), P(wx1, sh)], fill=(226, 231, 232))
        d.line([P(wx0, sh), P(wx1, sh)], fill=HAIR, width=S)
    # compound
    d.rectangle([P(0, 1920), P(2420, 0)], outline=GRAPHITE, width=S)
    # footprints of register items, base plant solid hairline, optional systems fainter
    for it in model["items"]:
        sheet15 = it.get("tag") == "LNGC" or it["name"].startswith("Terminal plot")
        if (not it["register"] and not sheet15) or it["layer"] in ("SITE", "R1_INTERIOR", "R4_INTERIOR"):
            continue
        fx0, fx1, fy0, fy1 = it["fp"]
        if (fx1 - fx0) * (fy1 - fy0) < 120 and not it.get("key"):
            continue
        opt = it["layer"].startswith(("OPT_", "HV_", "SWYD_FUTURE"))
        if coastal and it["layer"].startswith("OPT_LNG"):   # trucked satellite, replaced by the terminal
            continue
        if it.get("key") or sheet15:                          # sheet 15 item: base-plant weight
            opt = False
        col = (192, 193, 188) if opt else (120, 128, 132)
        if it["shape"] == "hull" and coastal:                # placed north of the plant: bow west
            d.polygon([P(fx1, fy0), P(fx1, fy1), P(fx0 + 60, fy1), P(fx0, (fy0 + fy1) / 2), P(fx0 + 60, fy0)],
                      outline=col, width=S)
        elif it["shape"] == "hull":
            d.polygon([P(fx0, fy0), P(fx1, fy0), P(fx1, fy1 - 60), P((fx0 + fx1) / 2, fy1), P(fx0, fy1 - 60)],
                      outline=col, width=S)
        elif it["shape"] == "circle":
            d.ellipse([P(fx0, fy1), P(fx1, fy0)], outline=col, width=S)
        else:
            d.rectangle([P(fx0, fy1), P(fx1, fy0)], outline=col, width=S)
    # view cones
    lab = f("IBMPlexMono-Regular.ttf", 17)
    t = coastal.get("transform") if coastal else None
    for k, h in HERO.items():
        if k not in B["cones"]:
            continue
        ex, ey, _ = h["eye"]
        tx, ty, _ = h["target"]
        if t and k[0] in "CF" and not h.get("site"):                                # sheet-15 cameras, rotated onto the site
            ex, ey, tx, ty = t["c"] - ey, ex - t["d"], t["c"] - ty, tx - t["d"]
        # far viewpoints are pulled onto the plan window edge, keeping their bearing
        ex = min(max(ex, wx0 + 60), wx1 - 60)
        ey = min(max(ey, wy0 + 60), wy1 - 60)
        ang = math.atan2(ty - ey, tx - ex)
        half = math.atan(18 / h["lens"])            # 36 mm sensor: half horizontal FOV
        L = 330
        a = P(ex, ey)
        b = P(ex + L * math.cos(ang - half), ey + L * math.sin(ang - half))
        c = P(ex + L * math.cos(ang + half), ey + L * math.sin(ang + half))
        d.polygon([a, b, c], fill=(236, 214, 193), outline=COPPER)
        r = 7 * S
        d.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r], fill=COPPER)
        lx, ly = a[0] - 30 * S * math.cos(ang), a[1] + 30 * S * math.sin(ang)
        d.text((lx - d.textlength(k, font=lab) / 2, ly - 11 * S), k, font=lab, fill=COPPER)
    # scale bar: two segments
    bx, by = P(0, 0)[0], (oy + (wy1 - wy0) * sc + 30) * S
    step = B.get("bar", 250)
    seg = step * sc * S
    for i in range(2):
        d.rectangle([bx + i * seg, by - 8 * S, bx + (i + 1) * seg, by], outline=INK, width=S,
                    fill=INK if i == 0 else None)
    small = f("IBMPlexMono-Regular.ttf", 16)
    for i, t in enumerate(("0", f"{step:,}", f"{2 * step:,} FT")):
        d.text((bx + i * seg - (0 if i == 0 else d.textlength(t, font=small) / 2), by + 8 * S), t, font=small,
               fill=GRAPHITE)
    return sc


def north_and_sun(d, x, y, sun):
    elev, azim = sun
    # north point
    cx, cy = x * S, y * S
    d.line([(cx, cy + 46 * S), (cx, cy - 36 * S)], fill=INK, width=S)
    d.polygon([(cx, cy - 46 * S), (cx - 9 * S, cy - 22 * S), (cx, cy - 28 * S)], fill=INK)
    d.polygon([(cx, cy - 46 * S), (cx + 9 * S, cy - 22 * S), (cx, cy - 28 * S)], outline=INK)
    n = f("Jura-Medium.ttf", 22)
    d.text((cx - d.textlength("N", font=n) / 2, cy + 52 * S), "N", font=n, fill=INK)
    # sun angle: elevation arc
    sx, sy, R = cx + 120 * S, cy + 40 * S, 70 * S
    d.line([(sx, sy), (sx + R + 14 * S, sy)], fill=GRAPHITE, width=S)
    d.arc([sx - R, sy - R, sx + R, sy + R], 180 + 0, 360, fill=HAIR, width=S)
    e = math.radians(elev)
    ex, ey = sx + R * math.cos(e), sy - R * math.sin(e)
    d.line([(sx, sy), (ex, ey)], fill=COPPER, width=S)
    d.ellipse([ex - 7 * S, ey - 7 * S, ex + 7 * S, ey + 7 * S], outline=COPPER, width=S)
    d.arc([sx - 34 * S, sy - 34 * S, sx + 34 * S, sy + 34 * S], 360 - elev, 360, fill=COPPER, width=S)
    m = f("IBMPlexMono-Regular.ttf", 16)
    d.text((sx + R + 22 * S, sy - 44 * S), f"{elev}°", font=m, fill=COPPER)
    d.text((sx + R + 22 * S, sy - 20 * S), f"AZ {azim}°", font=m, fill=GRAPHITE)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PLANT, "renders", "pro")
    B = BOARDS[sys.argv[2] if len(sys.argv) > 2 else "inland"]
    name = lambda k: B["names"].get(k, HERO[k]["n"]).replace(" (optional)", "")
    img = lambda k: os.path.join(root, f"{k}_pro_clean.jpg")
    board = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(board)
    L, R, T = 150, 4650, 150
    # header
    tracked(d, L * S, (T - 14) * S, "3×1 Combined Cycle", f("InstrumentSerif-Regular.ttf", 132), INK, 0.5)
    tracked(d, L * S, (T + 150) * S, B["subtitle"], f("Jura-Light.ttf", 27), GRAPHITE, 7)
    mono = f("IBMPlexMono-Regular.ttf", 20)
    for i, t in enumerate((B["sheet"], "SEPT 2026", "BLENDER CYCLES · AgX")):
        d.text(((R) * S - d.textlength(t, font=mono), (T + 30 + i * 36) * S), t, font=mono, fill=GRAPHITE)
    d.line([(L * S, 372 * S), (R * S, 372 * S)], fill=INK, width=S)
    # plates
    gx, g2 = 3150, 3230
    k = B["main"]
    place(board, img(k), (L, 420, gx, 420 + 1687))
    caption(d, L, 2130, k, name(k), 3000)
    for (k, y0, yc) in zip(B["right"], (420, 1308), (1238, 2130)):
        place(board, img(k), (g2, y0, R, y0 + 799))
        caption(d, g2, yc, k, name(k), 1420)
    for i, k in enumerate(B["row"]):
        x = L + i * (960 + 60)
        place(board, img(k), (x, 2230, x + 960, 2230 + 540))
        caption(d, x, 2790, k, name(k), 960)
    # key plan + apparatus
    tracked(d, g2 * S, 2222 * S, "KEY PLAN", f("Jura-Medium.ttf", 21), INK, 5)
    tracked(d, (g2 + 175) * S, 2222 * S, "VIEW CONES · HAIRLINE FOOTPRINTS FROM THE VERIFIED MODEL",
            f("Jura-Light.ttf", 17), GRAPHITE, 2.4)
    key_plan(d, (g2, 2262, R - 300, 2930), B)
    north_and_sun(d, R - 190, 2400, B["sun"])
    legend = f("Jura-Light.ttf", 17)
    keys = ((((120, 128, 132), "BASE PLANT"), ((192, 193, 188), "OPTIONAL SYSTEMS"), (COPPER, "PLATE VIEWPOINT"))
            if not B["overlay"] else
            (((120, 128, 132), "PLANT + TERMINAL"), ((192, 193, 188), "OPTIONAL SYSTEMS"), ((226, 231, 232), "SEA"),
             (COPPER, "PLATE VIEWPOINT")))
    for i, (sw, t) in enumerate(keys):
        y = (2640 + i * 40) * S
        d.rectangle([(R - 250) * S, y + 4 * S, (R - 226) * S, y + 20 * S], outline=sw, width=S * 2,
                    fill=sw if t == "SEA" else None)
        tracked(d, (R - 212) * S, y, t, legend, GRAPHITE, 2.2)
    # footer
    d.line([(L * S, 3040 * S), (R * S, 3040 * S)], fill=HAIR, width=S)
    foot = f("Jura-Light.ttf", 20)
    tracked(d, L * S, 3062 * S, "CONCEPTUAL ILLUSTRATION  ·  NOT ENGINEERED  ·  NOT FOR CONSTRUCTION", foot, COPPER, 3.4)
    t = "STEPHAN HARDT  |  POWER GENERATION SOLUTIONS"
    tracked(d, R * S - tw(d, t, foot, 3.4), 3062 * S, t, foot, INK, 3.4)
    out = board.resize((W // S, H // S), Image.LANCZOS)
    png = os.path.join(root, B["out"] + ".png")
    out.save(png, optimize=True)
    out.save(os.path.join(root, B["out"] + ".pdf"), resolution=300)
    out.save(os.path.join(root, B["out"] + ".jpg"), quality=92, optimize=True, subsampling=0)
    print("wrote", png, ".pdf and .jpg")


if __name__ == "__main__":
    main()
