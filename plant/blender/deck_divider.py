"""Section-divider slide in the style of the 'Southwire x Anixter/Wesco - Power Generation Solutions' deck
(16:9, 1440 x 810 pt): charcoal field, copper edge bar, logo, big section number, two-tone condensed title,
copper tag box, item list on hairline rules, render photo on the right behind a dark diagonal, watermark, footer.
Geometry and colours measured from the deck (section 01 divider).

    python blender/deck_divider.py            # writes renders/deck/SK-3X1_divider_ccs.png / .pdf
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DECK = os.path.join(HERE, "deck")
S = 2.0                                     # px per pt: 2880 x 1620 output
BG, BAR, ORANGE, WHITE, TAGTXT, GREY, RULE, FOOTGREY, FOOTBOX = (
    (14, 16, 18), (180, 88, 31), (227, 154, 95), (245, 243, 239), (255, 253, 250), (201, 205, 210), (58, 63, 69),
    (138, 143, 149), (20, 22, 25))

SLIDES = {
    "ccs": dict(photo=os.environ.get("DECK_PHOTO", os.path.join(PLANT, "renders", "epic", "E69_pro.png")), number="14",
                title=("CARBON", "CAPTURE"), tag="PRODUCT APPLICATION · CCS",
                items=["230 KV XLPE TO THE CCS TRANSFORMERS",
                       "MV-105 TO 16 MW FANS AND CO2 COMPRESSORS",
                       "ARMOR-X MC-HL AND TYPE TC-ER ON THE RACKS",
                       "INSTRUMENTATION AND GROUNDING"],
                out="SK-3X1_divider_ccs"),
    "gas": dict(photo=os.path.join(PLANT, "renders", "epic", "E71_pro.png"), number="02",
                title=("GAS POWER", "GENERATION", "SOLUTIONS"), tag=None,
                items=["THE PLANT MODEL AND CABLE SYSTEMS", "CABLE LINEUP AND DETAIL", "MODULAR GAS POWER",
                       "STANDARDS AND SERVICES"],
                out="SK-3X1_divider_gas_power"),
    "hall": dict(photo=os.path.join(PLANT, "renders", "epic", "E70_pro.png"), number="07",
                 title=("TURBINE", "HALL"), tag="PRODUCT APPLICATION · GT / ST",
                 items=["MV-105 15 KV FEEDERS TO THE GT AUXILIARIES",
                        "ARMOR-X MC-HL AT THE TURBINE ENCLOSURES",
                        "TYPE TC-ER POWER AND CONTROL IN THE TRAYS",
                        "INSTRUMENTATION AND THERMOCOUPLE CABLE"],
                 out="SK-3X1_divider_turbine_hall"),
}


def font(name, pt):
    return ImageFont.truetype(os.path.join(DECK, name), int(round(pt * S)))


def P(*v):
    return tuple(int(round(x * S)) for x in v)


def make(c):
    W, H = P(1440, 810)
    img = Image.new("RGB", (W, H), BG)
    # photo, right, under a dark diagonal (top edge at x 738 pt, bottom at 564 pt)
    ph = Image.open(c["photo"]).convert("RGB")
    pw, phh = P(877.5, 810)
    ph = ph.resize((pw, phh), Image.LANCZOS)
    img.paste(ph, P(562.5, 0))
    d = ImageDraw.Draw(img)
    d.polygon([P(562.5, 0), P(738, 0), P(564, 810), P(562.5, 810)], fill=BG)
    # soft shadow along the diagonal
    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for k in range(int(28 * S)):
        a = int(110 * (1 - k / (28 * S)) ** 2)
        sd.line([(P(738, 0)[0] + k, 0), (P(564, 0)[0] + k, H)], fill=a, width=1)
    img = Image.composite(Image.new("RGB", (W, H), BG), img, sh)
    # watermark
    wm = Image.open(os.path.join(DECK, "watermark.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
    img = img.convert("RGBA")
    img.alpha_composite(wm)
    d = ImageDraw.Draw(img)
    d.rectangle([P(0, 0), P(12, 810)], fill=BAR)
    logo = Image.open(os.path.join(DECK, "southwire_pgs_logo.png")).convert("RGBA").resize(P(300, 74.25), Image.LANCZOS)
    img.alpha_composite(logo, P(96, 54))
    if len(c["title"]) == 2:
        d.text(P(96, 149.2), c["number"], font=font("BarlowCondensed-ExtraBold.ttf", 127.5), fill=BAR, anchor="la")
    else:
        d.text(P(96, 156), c["number"], font=font("BarlowCondensed-ExtraBold.ttf", 60), fill=BAR, anchor="la")
    t = c["title"]
    tfont = font("BarlowCondensed-ExtraBold.ttf", 90)
    ys = (285, 366) if len(t) == 2 else (240, 321, 402)     # three lines: smaller number above
    for k, (yy, line) in enumerate(zip(ys, t)):
        d.text(P(96, yy), line, font=tfont, fill=ORANGE if k == len(t) - 1 else WHITE, anchor="la")
    if c.get("tag"):
        tf = font("BarlowCondensed-ExtraBold.ttf", 30)
        tw = d.textlength(c["tag"], font=tf) / S
        d.rectangle([P(96, 478.5), P(96 + tw + 42, 535.5)], fill=BAR)
        d.text(P(117, 489), c["tag"], font=tf, fill=TAGTXT, anchor="la")
    lf = font("BarlowCondensed-Bold.ttf", 24)
    y_rule = [553.5, 600.75, 648, 695.25, 742.5]
    for yr in y_rule:
        d.rectangle([P(96, yr), P(576, yr + .75)], fill=RULE)
    for k, t in enumerate(c["items"]):
        assert d.textlength(t, font=lf) / S < 478, t
        d.text(P(96, 563.2 + 47.25 * k), t, font=lf, fill=GREY, anchor="la")
    ff = font("Barlow-Regular.ttf", 18)
    d.rectangle([P(0, 773.25), P(770, 810)], fill=FOOTBOX)                    # footer strip (as on the 02 divider)
    d.rectangle([P(0, 0), P(12, 810)], fill=BAR)
    d.text(P(96, 779.2), "Confidential · Do not distribute · © 2026 Southwire Company, LLC. All rights reserved.", font=ff,
           fill=FOOTGREY, anchor="la")
    d.rectangle([P(1163.25, 773.25), P(1440, 810)], fill=FOOTBOX)
    d.text(P(1181.6, 780.8), "stephan.hardt@southwire.com", font=ff, fill=WHITE, anchor="la")
    out = os.path.join(PLANT, "renders", "deck", c["out"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = img.convert("RGB")
    img.save(out + ".png")
    img.save(out + ".pdf", resolution=72 * S)
    print("wrote", out + ".png / .pdf")


if __name__ == "__main__":
    import sys
    for key in (sys.argv[1:] or list(SLIDES)):
        make(SLIDES[key])
