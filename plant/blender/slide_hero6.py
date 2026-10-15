"""'Hero shots' slide (16:9, PNG + PDF): six renders of the SK-3X1 model in the deck style of slide_modular.py.
The campus aerial is the large tile; two tiles beside it and three across the bottom show the cable with the
HRSGs and stacks behind.

    python blender/slide_hero6.py RENDER_DIR [OUT_STEM]
RENDER_DIR holds the finished E123, E124, E71, E70, E121 and E99 renders (<k>_pro_clean.jpg, from finish_pro.py)."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DJ = "/usr/share/fonts/truetype/dejavu/"
S = 2                                       # px per design px (output 4000 x 2250)
W, H = 2000 * S, 1125 * S
NAVY, GREY, COPPER, BG, RULE = (31, 45, 61), (98, 104, 110), (166, 84, 40), (247, 247, 245), (214, 214, 210)
# (camera, caption, focus x, focus y): focus is the crop centre as a fraction of the render
TILES = [
    ("E123", "The SK-3X1 campus: 3x1 combined cycle, carbon capture, modular yard, BTM campus", .5, .5),
    ("E71", "ARMOR-X and MV-105 in the R1 tray, HRSG 1 and its stack ahead", .5, .62),
    ("E124", "Main pipe and cable rack beside the HRSG stacks", .5, .55),
    ("E70", "Cable legends in the hall tray, HRSG 2 beyond", .5, .6),
    ("E121", "MC risers up the turbine-hall roof, the stacks behind", .5, .45),
    ("E99", "HRSG 1: stair tower and access platforms, cable on the east wall", .5, .5),
]


def f(name, px):
    return ImageFont.truetype(DJ + name, int(px * S))


def tile(img, src, box, fx, fy, caption):
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    ph = Image.open(src).convert("RGB")
    sw, sh = ph.size
    sc = max(tw / sw, th / sh)
    ph = ph.resize((round(sw * sc), round(sh * sc)), Image.LANCZOS)
    ox = min(max(0, round(ph.size[0] * fx - tw / 2)), ph.size[0] - tw)
    oy = min(max(0, round(ph.size[1] * fy - th / 2)), ph.size[1] - th)
    img.paste(ph.crop((ox, oy, ox + tw, oy + th)), (x0, y0))
    # caption on a soft dark gradient along the bottom edge
    gh = 70 * S
    grad = Image.new("L", (tw, gh))
    for y in range(gh):
        ImageDraw.Draw(grad).line([(0, y), (tw, y)], fill=int(170 * (y / gh) ** 1.6))
    img.paste((14, 20, 28), (x0, y1 - gh), grad)
    d = ImageDraw.Draw(img)
    d.text((x0 + 16 * S, y1 - 30 * S), caption, font=f("DejaVuSans.ttf", 14.5), fill="white")


def main(rdir, stem):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((73 * S, 34 * S), "SK-3X1 IN 3D", font=f("DejaVuSans-Bold.ttf", 40), fill=NAVY)
    d.text((74 * S, 92 * S), "The power block from above, and the cable that connects it, with the HRSGs and stacks in view.",
           font=f("DejaVuSans.ttf", 20), fill=GREY)
    gx0, gy0, gx1, gy1, g = 37 * S, 140 * S, 1963 * S, 1015 * S, 10 * S
    cw = (gx1 - gx0 - 2 * g) / 3
    rh = (gy1 - gy0 - g) / 2
    big_h = round(rh * 1.18)                                       # campus tile a little taller than the rest
    small_h = (gy1 - gy0 - g) - big_h
    sh_ = (big_h - g) / 2
    c = [round(gx0 + i * (cw + g)) for i in range(3)]
    boxes = [
        (c[0], gy0, round(c[1] + cw), gy0 + big_h),                                 # campus: two columns
        (c[2], gy0, gx1, round(gy0 + sh_)),
        (c[2], round(gy0 + sh_ + g), gx1, gy0 + big_h),
        (c[0], gy0 + big_h + g, round(c[0] + cw), gy1),
        (c[1], gy0 + big_h + g, round(c[1] + cw), gy1),
        (c[2], gy0 + big_h + g, gx1, gy1),
    ]
    assert small_h > 0
    for (k, cap, fx, fy), box in zip(TILES, boxes):
        tile(img, os.path.join(rdir, f"{k}_pro_clean.jpg"), box, fx, fy, cap)
    d.line([(73 * S, 1038 * S), (1927 * S, 1038 * S)], fill=RULE, width=S)
    d.text((73 * S, 1052 * S), "Rendered from the SK-3X1 3D model (Rev 14). Conceptual illustration: not engineered.",
           font=f("DejaVuSans.ttf", 17), fill=GREY)
    d.text((73 * S, 1084 * S), "© 2026 Southwire Company, LLC. All rights reserved.", font=f("DejaVuSans.ttf", 15),
           fill=GREY)
    img.save(stem + ".png")
    img.save(stem + ".pdf", resolution=200 * S / 2)
    print("wrote", stem + ".png", stem + ".pdf")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(PLANT, "renders", "deck", "SK-3X1_hero_shots"))
