"""Slide 19 replacement: the SK-3X1 campus as '16 zones' in the Anixter/Wesco deck style.

Takes the clean P19 render and its labels.json (marker anchors projected by Blender), darkens and desaturates the land
outside the compound, draws numbered orange markers on short leaders, and lays out the slide (1920 x 1080): kicker,
title, legend of the 16 zones, footer. Writes the full slide and the bare image for reuse.

  python3 blender/deck_zones.py <render dir> <out dir>
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "deck")
ORANGE = (224, 122, 46)
INK_BG = (13, 15, 18)
PANEL = (16, 19, 23)


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def main(src, out):
    os.makedirs(out, exist_ok=True)
    im = Image.open(os.path.join(src, "P19_pro_clean.jpg")).convert("RGB")
    meta = json.load(open(os.path.join(src, "P19_pro.labels.json")))
    W, H = im.size
    sx, sy = W / meta["rw"], H / meta["rh"]
    calls = meta["callouts"]
    corners = [(c["x"] * sx, c["y"] * sy) for c in calls if c["num"] == "C"]
    zones = [c for c in calls if c["num"] != "C"]
    # outside the compound: dark, desaturated, so the plant sits on the slide like a model on a table
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(corners, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2.5))
    a = np.asarray(im).astype(np.float32)
    g = a.mean(2, keepdims=True)
    dark = (g * .05 + np.array(INK_BG, np.float32) * .95)
    m = np.asarray(mask).astype(np.float32)[..., None] / 255
    a = a * .9 * m + dark * (1 - m)
    plate = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    # markers: leader up from the anchor, numbered orange disc
    d = ImageDraw.Draw(plate)
    num = font("BarlowCondensed-Bold.ttf", int(30 * W / 2400))
    R = int(25 * W / 2400)
    lift = {"07": 70, "08": 120, "05": 60, "06": 110, "16": 60, "11": 90, "14": 70}
    placed = []
    for c in sorted(zones, key=lambda c: c["y"]):
        ax, ay = c["x"] * sx, c["y"] * sy
        ly = lift.get(c["num"], 70) * W / 2400
        bx, by = ax, ay - ly
        for _ in range(12):                                   # keep discs apart
            if all((bx - px) ** 2 + (by - py) ** 2 > (2.3 * R) ** 2 for (px, py) in placed):
                break
            by -= 1.6 * R
        placed.append((bx, by))
        d.line([(ax, ay), (bx, by)], fill=(245, 245, 242), width=max(2, int(2.2 * W / 2400)))
        d.ellipse([ax - 5, ay - 5, ax + 5, ay + 5], fill=(245, 245, 242))
        d.ellipse([bx - R - 3, by - R - 3, bx + R + 3, by + R + 3], fill=(245, 245, 242))
        d.ellipse([bx - R, by - R, bx + R, by + R], fill=ORANGE)
        d.text((bx, by + 1), str(int(c["num"])), font=num, fill=(255, 255, 255), anchor="mm")
    xs, ys = [p[0] for p in corners] + [p[0] for p in placed], [p[1] for p in corners] + [p[1] for p in placed]
    mx, my = .03 * W, .05 * H
    box = (max(0, min(xs) - mx), max(0, min(ys) - my - R), min(W, max(xs) + mx), min(H, max(ys) + my))
    plate = plate.crop(tuple(int(v) for v in box))
    W, H = plate.size
    plate.save(os.path.join(out, "P19_zones_plate.jpg"), quality=94, subsampling=0)

    # slide 1920 x 1080 in the deck layout
    S = Image.new("RGB", (1920, 1080), INK_BG)
    sd = ImageDraw.Draw(S)
    sd.text((128, 70), "THE PLANT IS THE MODEL", font=font("BarlowCondensed-Bold.ttf", 30), fill=ORANGE)
    sd.text((128, 104), "16 ZONES, ONE PLANT-WIDE CABLE SCOPE", font=font("BarlowCondensed-ExtraBold.ttf", 60),
            fill=(245, 245, 242))
    pw = 1270
    ph = int(pw * H / W)
    if ph > 740:
        ph = 740
        pw = int(ph * W / H)
    y0 = 200 + (760 - ph) // 2
    S.paste(plate.resize((pw, ph), Image.LANCZOS), (40, y0))
    names = sorted(((int(c["num"]), c["text"]) for c in zones))
    ly0 = 215
    f1, f2 = font("BarlowCondensed-Bold.ttf", 30), font("Barlow-Regular.ttf", 25)
    for k, (n, t) in enumerate(names):
        y = ly0 + k * 37.5
        sd.text((1340, y), f"{n:02d}", font=f1, fill=ORANGE)
        sd.text((1384, y + 3), t, font=f2, fill=(232, 232, 228))
    sd.text((128, 985), "PLANT · EQUIPMENT · CABLE · DELIVERY", font=font("BarlowCondensed-Bold.ttf", 30), fill=ORANGE)
    sd.text((128, 1030), "SK-3X1 3x1 combined cycle campus · rendered from the plant model · conceptual, not engineered",
            font=font("Barlow-Regular.ttf", 21), fill=(150, 150, 146))
    S.save(os.path.join(out, "slide19_zones.png"))
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
