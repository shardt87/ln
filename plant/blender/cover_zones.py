"""Section cover 'Plant Zones' on the clean E68 render (CCS absorbers over the legend-printed cable on the CCS rack).

    python blender/cover_zones.py [renders/epic/E68_pro_clean.jpg] [out.jpg]
Writes renders/cover/SK-3X1_plant_zones_cover.jpg (and .pdf, letter portrait)."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, "fonts")
COPPER = (210, 135, 74)
INK = (31, 36, 40)


def f(name, px):
    return ImageFont.truetype(os.path.join(FONTS, name), px)


def tracked(d, xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PLANT, "renders", "epic", "E68_pro_clean.jpg")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PLANT, "renders", "cover", "SK-3X1_plant_zones_cover.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = Image.open(src).convert("RGB")
    W0, H0 = img.size
    # letter portrait (8.5 x 11): crop the sides a little, which also trims the tower edge at top left
    W = int(H0 * 8.5 / 11)
    x0 = min(W0 - W, int((W0 - W) * .7))
    img = img.crop((x0, 0, x0 + W, H0))
    W, H = img.size
    k = W / 1545
    # soft light veil over the sky on the left, so the type sits on a calm field
    veil = Image.new("L", (W, H), 0)
    px = veil.load()
    for yy in range(0, int(H * .8)):
        fy = 1.0 if yy < H * .55 else max(0.0, 1 - (yy - H * .55) / (H * .25))   # smooth fade below the type
        fy = fy * fy * (3 - 2 * fy)
        for xx in range(0, int(W * .62)):
            fx = (1 - xx / (W * .62)) ** 1.6
            px[xx, yy] = int(150 * fx * fy)
    img = Image.composite(Image.new("RGB", (W, H), (236, 238, 237)), img, veil)
    d = ImageDraw.Draw(img)
    m = int(96 * k)
    tracked(d, (m, int(110 * k)), "SK-3X1  ·  REV 14  ·  3x1 COMBINED CYCLE", f("IBMPlexMono-Regular.ttf", int(22 * k)), INK,
            3 * k)
    d.line([(m, int(160 * k)), (m + int(84 * k), int(160 * k))], fill=COPPER, width=max(2, int(4 * k)))
    tracked(d, (m - int(6 * k), int(200 * k)), "PLANT", f("Jura-Light.ttf", int(150 * k)), INK, 14 * k)
    tracked(d, (m - int(6 * k), int(350 * k)), "ZONES", f("Jura-Light.ttf", int(150 * k)), INK, 14 * k)
    d.text((m, int(540 * k)), "From the grid to the absorber stack,", font=f("InstrumentSerif-Italic.ttf", int(40 * k)),
           fill=INK)
    d.text((m, int(590 * k)), "and the cable that connects it all.", font=f("InstrumentSerif-Italic.ttf", int(40 * k)),
           fill=INK)
    # zone index (plant zones; the data-centre option is left out)
    areas = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))["areas"]
    zones = [(a, n) for a, n in areas.items() if a != "L"]
    y = int(700 * k)
    mono = f("IBMPlexMono-Regular.ttf", int(21 * k))
    name = f("Jura-Medium.ttf", int(23 * k))
    for a, n in zones:
        d.text((m, y + int(2 * k)), a, font=mono, fill=COPPER)
        tracked(d, (m + int(40 * k), y), n.upper(), name, INK, 1.6 * k)
        y += int(40 * k)
    # foot: credit and disclaimer, on a thin dark band
    band = int(64 * k)
    d.rectangle([(0, H - band), (W, H)], fill=(24, 28, 31))
    tracked(d, (m, H - band + int(22 * k)), "STEPHAN HARDT  |  POWER GENERATION SOLUTIONS", f("Jura-Medium.ttf",
            int(18 * k)), (225, 228, 230), 2.5 * k)
    note = "CONCEPTUAL ILLUSTRATION · NOT ENGINEERED · NOT FOR CONSTRUCTION"
    nf = f("Jura-Medium.ttf", int(16 * k))
    wn = sum(d.textlength(c, font=nf) for c in note) + 2 * k * (len(note) - 1)
    tracked(d, (W - m - wn, H - band + int(24 * k)), note, nf, COPPER, 2 * k)
    img.save(out, quality=94)
    img.save(os.path.splitext(out)[0] + ".pdf", resolution=W / 8.5)
    print("wrote", out)


if __name__ == "__main__":
    main()
