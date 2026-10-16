"""Deck slide: three ways to house the turbine island (common hall / GTs outdoors with an ST building / all outdoors),
with simple elevation sketches and the key differences, including what each asks of cable.

    python3 plant/blender/slide_turbine_island.py      # -> plant/renders/deck/SK-3X1_turbine_island_layouts.png
Typical practice, not engineered; SK-3X1 follows the drawing set (common hall).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DECK = os.path.join(HERE, "deck")
S = 2                                                   # px per design px (output 4000 x 2250)
W, H = 2000 * S, 1125 * S
NAVY, GREY, COPPER, BG, RULE = (31, 45, 61), (98, 104, 110), (166, 84, 40), (247, 247, 245), (214, 214, 210)
STEEL, PANEL, MACH, GROUND, SKY = (120, 132, 142), (226, 230, 233), (92, 110, 128), (182, 172, 150), (236, 241, 245)


def f(name, px):
    return ImageFont.truetype(os.path.join(DECK, name), int(px * S))


def P(x, y):
    return (int(x * S), int(y * S))


def R(x0, y0, x1, y1):
    return [P(x0, y0), P(x1, y1)]


def gt(d, x, g, w=66):
    """Gas turbine + generator on a pedestal, seen from the side (x = left end, g = grade y)."""
    d.rectangle(R(x, g - 14, x + w + 30, g), fill=(200, 200, 196))                       # pedestal
    d.polygon([P(x + 30, g - 26), P(x + 30 + w * .35, g - 38), P(x + 30 + w, g - 40), P(x + 30 + w, g - 18),
               P(x + 30 + w * .35, g - 20)], fill=MACH)                                    # compressor / turbine
    d.rounded_rectangle(R(x + 2, g - 38, x + 28, g - 16), radius=int(6 * S), fill=(110, 126, 142))   # generator


def st(d, x, g):
    """Steam turbine-generator (bigger, rounded LP casing)."""
    d.rectangle(R(x, g - 14, x + 112, g), fill=(200, 200, 196))
    d.rounded_rectangle(R(x + 2, g - 36, x + 28, g - 16), radius=int(6 * S), fill=(110, 126, 142))
    d.rectangle(R(x + 34, g - 34, x + 110, g - 16), fill=MACH)
    d.pieslice(R(x + 44, g - 60, x + 100, g - 8), 180, 360, fill=MACH)                     # LP upper casing


def crane(d, x0, x1, y):
    d.rectangle(R(x0, y, x1, y + 6), fill=COPPER)
    d.rectangle(R((x0 + x1) / 2 - 8, y + 6, (x0 + x1) / 2 + 8, y + 12), fill=COPPER)
    d.line([P((x0 + x1) / 2, y + 12), P((x0 + x1) / 2, y + 40)], fill=COPPER, width=int(2 * S))


def mobile_crane(d, x, g):
    """Rented crawler crane parked in front of the units (on the ground strip), boom over a GT enclosure."""
    b = g + 22
    d.rectangle(R(x, b - 10, x + 46, b), fill=COPPER)                                     # crawler body
    d.rectangle(R(x - 4, b, x + 50, b + 5), fill=(90, 60, 40))                            # tracks
    d.line([P(x + 12, b - 10), P(x + 66, g - 120)], fill=COPPER, width=int(4 * S))       # boom
    d.line([P(x + 66, g - 120), P(x + 66, g - 72)], fill=COPPER, width=int(2 * S))       # hook line


def enclosure(d, x0, x1, g, h):
    d.rectangle(R(x0, g - h, x1, g), fill=PANEL, outline=STEEL, width=int(2 * S))
    d.rectangle(R(x0 + 10, g - h - 6, x0 + 24, g - h), fill=STEEL)                          # roof vent fan


def sketch(d, kind, X, Y, Wd=560, Hd=300):
    d.rectangle(R(X, Y, X + Wd, Y + Hd), fill=SKY)
    g = Y + Hd - 34
    d.rectangle(R(X, g, X + Wd, Y + Hd), fill=GROUND)
    xs = [X + 22 + 108 * k for k in range(3)]
    xst = X + 22 + 108 * 3 + 6
    if kind == 0:                                                                           # common hall
        d.rectangle(R(X + 12, Y + 70, X + Wd - 12, g), fill=(232, 236, 239), outline=STEEL, width=int(3 * S))
        d.polygon([P(X + 6, Y + 70), P(X + Wd / 2, Y + 44), P(X + Wd - 6, Y + 70)], fill=STEEL)
        crane(d, X + 20, X + Wd - 20, Y + 84)
        for x in xs:
            gt(d, x, g)
        st(d, xst, g)
    elif kind == 1:                                                                         # GT enclosures + ST building
        for x in xs:
            enclosure(d, x - 4, x + 100, g, 60)
            gt(d, x, g)
        d.rectangle(R(xst - 10, Y + 92, X + Wd - 8, g), fill=(232, 236, 239), outline=STEEL, width=int(3 * S))
        d.polygon([P(xst - 16, Y + 92), P((xst + X + Wd) / 2, Y + 74), P(X + Wd - 2, Y + 92)], fill=STEEL)
        crane(d, xst - 2, X + Wd - 16, Y + 104)
        st(d, xst, g)
        mobile_crane(d, X + 210, g)
    else:                                                                                   # everything outdoors
        for x in xs:
            enclosure(d, x - 4, x + 100, g, 60)
            gt(d, x, g)
        enclosure(d, xst - 6, xst + 118, g, 72)
        st(d, xst, g)
        mobile_crane(d, X + 210, g)


COLS = [
    ("1  COMMON TURBINE HALL", "SK-3X1 (this campus)",
     [("Where", "Cold climates; noise-sensitive or urban sites; Europe, Japan, northern US and Canada"),
      ("Why", "One bridge crane serves every unit; outages in any weather; noise contained; shared laydown"),
      ("Trade-off", "Largest building, highest cost, longer build; gas indoors needs ventilation, detection, fire separation"),
      ("Cable", "Mostly indoor tray: TC-ER and MV-105 in a protected, climate-controlled space")]),
    ("2  GTs OUTDOORS, ST IN A BUILDING", "Common in warm US regions",
     [("Where", "Texas, the Southeast and Southwest; the Middle East"),
      ("Why", "Lower cost, faster build; OEM GT packages bring their own enclosure, ventilation and CO2 fire suppression; "
              "the ST keeps a crane and cover for its valves, lube oil and hydraulics"),
      ("Trade-off", "Rented crawler crane at every GT outage; crews work in the weather"),
      ("Cable", "Outdoor-rated: sunlight-resistant, wet-rated jackets; more conduit; heat tracing for cold snaps")]),
    ("3  EVERYTHING OUTDOORS", "Lowest capital cost",
     [("Where", "Hot, dry sites; tight budgets; simple-cycle peakers"),
      ("Why", "No buildings for the turbines at all; fastest to build"),
      ("Trade-off", "All maintenance with mobile cranes; harshest exposure for machines and people"),
      ("Cable", "As 2, plus heat and UV; cold-impact ratings (to -40 C) where winters are hard")]),
]


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width * S:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build(out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text(P(73, 40), "THE TURBINE ISLAND: THREE WAYS TO HOUSE IT", font=f("BarlowCondensed-ExtraBold.ttf", 52), fill=NAVY)
    d.text(P(75, 106), "Same machines, same power. The difference is the building: who lifts the heavy parts, and what "
                       "the weather can reach.", font=f("Barlow-Regular.ttf", 23), fill=GREY)
    d.line([P(73, 150), P(1927, 150)], fill=RULE, width=int(2 * S))
    X0, CW, GAP = 73, 600, 27
    for k, (title, sub, rows) in enumerate(COLS):
        X = X0 + k * (CW + GAP)
        sketch(d, k, X + 20, 172, CW - 40, 300)
        d.text(P(X + 20, 492), title, font=f("BarlowCondensed-ExtraBold.ttf", 33), fill=NAVY if k else COPPER)
        d.text(P(X + 20, 532), sub, font=f("BarlowCondensed-Bold.ttf", 22), fill=GREY)
        y = 572
        for lab, txt in rows:
            d.text(P(X + 20, y), lab.upper(), font=f("BarlowCondensed-Bold.ttf", 19), fill=COPPER if lab == "Cable" else NAVY)
            lines = wrap(d, txt, f("Barlow-Regular.ttf", 19.5), CW - 150)
            for i, ln in enumerate(lines):
                d.text(P(X + 125, y + i * 26), ln, font=f("Barlow-Regular.ttf", 19.5), fill=(45, 52, 60))
            y += max(1, len(lines)) * 26 + 16
        if k < 2:
            d.line([P(X + CW + GAP / 2, 180), P(X + CW + GAP / 2, 960)], fill=RULE, width=int(2 * S))
    # key difference banner
    d.rectangle(R(73, 975, 1927, 1062), fill=NAVY)
    d.text(P(100, 988), "KEY DIFFERENCE", font=f("BarlowCondensed-ExtraBold.ttf", 25), fill=(232, 170, 120))
    d.text(P(100, 1020), "A hall buys an in-house crane, all-weather outages and quiet; enclosures buy lower cost and "
                         "speed. For cable: indoor tray in a hall, outdoor-rated cable and more conduit without one.",
           font=f("Barlow-Regular.ttf", 21), fill="white")
    d.text(P(73, 1080), "Typical practice; site, owner and OEM choices vary. Sketches not to scale.",
           font=f("Barlow-Regular.ttf", 16), fill=GREY)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)
    img.resize((W // 2, H // 2), Image.LANCZOS).save(out.replace(".png", "_preview.jpg"), quality=90)
    return out


if __name__ == "__main__":
    print(build(os.path.join(PLANT, "renders", "deck", "SK-3X1_turbine_island_layouts.png")))
