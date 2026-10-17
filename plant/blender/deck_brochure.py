"""The wire & cable brochure as 16:9 deck slides, to follow the Strategy Monthly Update cover (deck_divider.py
strategy): same copy, products and model-measured numbers as brochure.py, laid out landscape in the cover's look
(charcoal field, diagonal photo edge, Barlow Condensed, copper). Pictures are the current renders of the SK-3X1
model (renders/epic, renders/cover).

    python blender/deck_brochure.py        # -> renders/deck/brochure_slides/slide_02..12.png + one PDF with the cover
"""
import os

from PIL import Image, ImageDraw

import brochure as B
from brochure import BG, PANEL, COPPER, COPPER_D, WHITE, GREY, DIM, RULE, BOLD, XBOLD, REG, F, photo, tracked, wrap

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
OUT = os.path.join(PLANT, "renders", "deck", "brochure_slides")
COVER_PNG = os.path.join(PLANT, "renders", "deck", "SK-3X1_cover_strategy_update_October.png")
W, H = 2880, 1620                                      # 1440 x 810 pt at 2x, as the cover
M = 120
FOOT = 96                                              # footer band height
NOTE = B.NOTE
INSET_CROP = {"02": (220, 690, 880, 1050)}             # the jacket legends in the current E70 (1170 x 1080)


def para(d, xy, text, font, fill, width, lead=1.4):
    x, y = xy
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += font.size * lead
    return y


def footer(d, n, note=None):
    y = H - FOOT
    d.rectangle([0, y, W, H], fill=BG)
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    tracked(d, (M, y + 30), "SOUTHWIRE  |  POWER GENERATION SOLUTIONS", F(BOLD, 26), DIM, 3)
    s = f"{n:02d}"
    ft = F(BOLD, 28)
    d.text((W - M - d.textlength(s, font=ft), y + 28), s, font=ft, fill=COPPER)
    if note:
        nf = F(REG, 22)
        d.text((W - M - 70 - d.textlength(note, font=nf), y + 33), note, font=nf, fill=DIM)


def photo_right(img, name, x_top, x_bot, focus=(.5, .5), h=H - FOOT, crop=None):
    """Photo on the right of a slanted edge (x_top at the top, x_bot at the bottom), soft shadow on the edge."""
    x0 = min(x_top, x_bot)
    img.paste(photo(name, (W - x0, h), focus, crop), (x0, 0))
    sh = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sh)
    for k in range(40):
        sd.line([(x_top + k, 0), (x_bot + k, h)], fill=int(120 * (1 - k / 40) ** 2), width=1)
    img.paste(Image.new("RGB", img.size, BG), (0, 0), sh)
    ImageDraw.Draw(img).polygon([(0, 0), (x_top, 0), (x_bot, h), (0, h)], fill=BG)


def shade_bottom(img, x0, y0, y1, strength=215):
    """Dark gradient over the lower part of a photo so cards and captions read."""
    g = Image.new("L", (1, y1 - y0))
    g.putdata([int(strength * min(1, (k / (y1 - y0)) * 1.6) ** 1.2) for k in range(y1 - y0)])
    g = g.resize((W - x0, y1 - y0))
    img.paste(Image.new("RGB", g.size, BG), (x0, y0), g)


def tab(d, xy, text):
    tf = F(BOLD, 30)
    tw = tracked(ImageDraw.Draw(Image.new("L", (1, 1))), (0, 0), text, tf, 0, 4)
    x, y = xy
    d.rectangle([x - 22, y - 12, x + tw + 22, y + 46], fill=COPPER_D)
    tracked(d, (x, y), text, tf, WHITE, 4)


def chips(d, xy, items, width):
    x, y = xy
    f = F(BOLD, 24)
    for t in items:
        tw = d.textlength(t, font=f) + 32
        if x + tw > xy[0] + width:
            x, y = xy[0], y + 56
        d.rounded_rectangle([x, y, x + tw, y + 44], radius=6, outline=COPPER, width=2)
        d.text((x + 16, y + 8), t, font=f, fill=WHITE)
        x += tw + 14
    return y + 56


def framed(img, d, name, xy, size, focus=(.5, .5), crop=None, cap=None, capw=None):
    x, y = xy
    img.paste(photo(name, size, focus, crop), (x, y))
    d.rectangle([x - 2, y - 2, x + size[0] + 2, y + size[1] + 2], outline=COPPER, width=3)
    if cap:
        return para(d, (x, y + size[1] + 14), cap, F(REG, 22), GREY, capw or size[0], 1.3)
    return y + size[1]


def cards(d, xy, cw, ch, items, cols=2, gap=24):
    for k, (head, spec, use) in enumerate(items):
        x = xy[0] + (k % cols) * (cw + gap)
        y = xy[1] + (k // cols) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=PANEL)
        d.rectangle([x, y, x + 8, y + ch], fill=COPPER)
        d.text((x + 34, y + 22), head, font=F(XBOLD, 42), fill=WHITE)
        sy = para(d, (x + 34, y + 78), spec, F(BOLD, 22), COPPER, cw - 60, 1.3)
        para(d, (x + 34, sy + 6), use, F(REG, 24), GREY, cw - 60, 1.32)


# ------------------------------------------------------------------------------------------------------------ slides
def overview(n):
    img = Image.new("RGB", (W, H), BG)
    photo_right(img, "HX1_pro.png", 1420, 1180, (.55, .35))      # HRSG 2, stacks and CCS up close (was the K5 aerial)
    d = ImageDraw.Draw(img)
    tracked(d, (M, 130), "SK-3X1 POWER CAMPUS", F(BOLD, 30), COPPER, 4)
    d.rectangle([M, 190, M + 96, 199], fill=COPPER)
    big = F(XBOLD, 128)
    d.text((M, 222), "ONE CAMPUS.", font=big, fill=WHITE)
    d.text((M, 352), "EVERY CABLE.", font=big, fill=COPPER)
    y = para(d, (M, 530), "A 3x1 combined-cycle plant with RICE engines, carbon capture, battery storage, a modular "
             "power yard, an LNG terminal and a behind-the-meter data centre: one campus, and from the 230 kV grid "
             "connection to the last instrument loop, all of it runs on cable. The next slides follow that cable "
             "through the plant.", F(REG, 32), GREY, 1060, 1.45)
    y += 40
    pages = {"01": 4, "02": 6, "03": 8, "04": 9, "05": 10, "06": 11}
    for z in B.ZONES:
        d.line([(M, y), (M + 1060, y)], fill=RULE, width=2)
        d.text((M, y + 16), z["n"], font=F(XBOLD, 40), fill=COPPER)
        tracked(d, (M + 86, y + 20), z["kicker"], F(BOLD, 34), WHITE, 3)
        s = f"SLIDE {pages[z['n']]:02d}"
        d.text((M + 1060 - d.textlength(s, font=F(BOLD, 26)), y + 26), s, font=F(BOLD, 26), fill=DIM)
        y += 76
    d.line([(M, y), (M + 1060, y)], fill=RULE, width=2)
    footer(d, n)
    return img


def where(n):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    tracked(d, (M, 110), "THE PLANT AT A GLANCE", F(BOLD, 30), COPPER, 4)
    d.text((M, 150), "WHERE THE CABLE GOES", font=F(XBOLD, 112), fill=WHITE)
    cent = {}
    for z in B.ZONES[:5]:
        xs, ys = [], []
        for it in B.MODEL["items"]:
            f = it.get("fp")
            if it.get("area") in z["areas"] and f and len(f) == 4 and (f[1] - f[0]) < 400 and it["z"][1] > 2:
                xs.append((f[0] + f[1]) / 2)
                ys.append((f[2] + f[3]) / 2)
        cent[z["n"]] = (sorted(xs)[len(xs) // 2], sorted(ys)[len(ys) // 2])
    mw, mh = 1640, 1060
    mp = B.plan_map((mw, mh), sum((z["areas"] for z in B.ZONES[:5]), ()), cent, soft=True)
    img.paste(mp, (M - 10, 300), mp)
    tracked(d, (M, 300 + mh + 10), "SK-3X1 CAMPUS PLAN, DRAWN FROM THE 3D MODEL  ·  NORTH UP", F(BOLD, 22), DIM, 3)
    # right column: legend and the numbers
    cx = 1880
    cw = W - M - cx
    y = 330
    for z in B.ZONES[:5]:
        d.text((cx, y), z["n"], font=F(XBOLD, 40), fill=COPPER)
        d.text((cx + 74, y + 4), z["kicker"].split("  ·  ")[0], font=F(BOLD, 36), fill=WHITE)
        y += 62
    y += 30
    d.line([(cx, y), (W - M, y)], fill=RULE, width=2)
    tracked(d, (cx, y + 26), "BY THE NUMBERS", F(BOLD, 30), COPPER, 4)
    L = B.route_feet()
    wired = sum(1 for it in B.MODEL["items"] if it.get("wiring") and it.get("area") != "L")
    stats = [(f"{L.get('tray', 0) / 5280:.1f} MI", "of cable tray routes on the racks and in the halls"),
             (f"{L.get('buried', 0) / 5280:.1f} MI", "of duct-bank and buried cable routes"),
             (f"{L.get('hv', 0):,.0f} FT", "of 230 kV underground cable routes"),
             (f"{wired}", "pieces of equipment with their own cable applications")]
    y += 90
    sw = cw // 2
    for k, (v, t) in enumerate(stats):
        x = cx + (k % 2) * sw
        yy = y + (k // 2) * 230
        d.text((x, yy), v, font=F(XBOLD, 84), fill=WHITE)
        para(d, (x, yy + 104), t, F(REG, 24), GREY, sw - 40, 1.3)
    para(d, (cx, H - FOOT - 100), "Route lengths measured along the modelled tray, duct-bank and cable routes "
         "(not cable footage); data-centre campus excluded.", F(REG, 20), DIM, cw, 1.35)
    footer(d, n)
    return img


def zone(z, n):
    img = Image.new("RGB", (W, H), BG)
    photo_right(img, z["hero"], 1300, 1080, z["hf"])
    shade_bottom(img, 1080, 980, H - FOOT)
    d = ImageDraw.Draw(img)
    tab(d, (M + 4, 104), f"{z['n']}  ·  {z['kicker']}")
    y = 210
    d.rectangle([M, y, M + 96, y + 9], fill=COPPER)
    big = F(XBOLD, 118)
    d.text((M, y + 30), z["title"][0], font=big, fill=WHITE)
    d.text((M, y + 150), z["title"][1], font=big, fill=COPPER)
    y = para(d, (M, y + 310), z["intro"], F(REG, 29), GREY, 1000, 1.42) + 34
    for k, (head, body) in enumerate(z["points"]):
        d.text((M, y), f"{k + 1:02d}", font=F(XBOLD, 38), fill=COPPER)
        d.text((M + 72, y + 2), head.upper(), font=F(BOLD, 34), fill=WHITE)
        y = para(d, (M + 72, y + 48), body, F(REG, 26), GREY, 930, 1.36) + 22
    chips(d, (M, int(y) + 10), z["chips"], 1000)
    # bottom right: inset photo and the locator map, over the shaded photo
    iw, ih = 600, 340
    ix, iy = 1500, H - FOOT - 60 - ih - 60
    crop = INSET_CROP.get(z["n"], z.get("inset_crop"))
    framed(img, d, z["inset"], (ix, iy), (iw, ih), (.5, .5), crop, z["inset_cap"])
    mw, mh = 560, 340
    mx = W - M - mw
    mp = B.plan_map((mw, mh), z["areas"])
    d.rectangle([mx - 2, iy - 2, mx + mw + 2, iy + mh + 2], fill=(18, 20, 23), outline=RULE, width=2)
    img.paste(mp, (mx, iy), mp)
    tracked(d, (mx, iy + mh + 16), "WHERE IN THE PLANT", F(BOLD, 22), DIM, 3)
    footer(d, n, NOTE)
    return img


def detail(n, hero, hf, heading, pics, title, items):
    """Hero across the top, two pictures and four product cards below."""
    img = Image.new("RGB", (W, H), BG)
    hh = 820
    img.paste(photo(hero, (W, hh), hf), (0, 0))
    g = Image.new("L", (1, 220))
    g.putdata([int(200 * (k / 220) ** 1.5) for k in range(220)])
    img.paste(Image.new("RGB", (W, 220), BG), (0, hh - 220), g.resize((W, 220)))
    d = ImageDraw.Draw(img)
    tracked(d, (M, hh - 70), heading, F(BOLD, 30), WHITE, 3)
    y0 = hh + 40
    pw, ph = 600, 380
    for k, (name, focus, cap) in enumerate(pics):
        framed(img, d, name, (M + k * (pw + 30), y0), (pw, ph), focus, cap=cap)
    cx = M + 2 * (pw + 30) + 30
    tracked(d, (cx, y0 - 6), title, F(BOLD, 30), COPPER, 4)
    cw = (W - M - cx - 24) // 2
    cards(d, (cx, y0 + 50), cw, 290, items)
    footer(d, n, NOTE)
    return img


def grid_detail(n):
    return detail(n, "E20_pro.png", (.5, .5), "THE 230 kV SWITCHYARD  ·  SIX BREAKER-AND-A-HALF DIAMETERS",
                  [("E4_pro.png", (.5, .5), "Along the switchyard at eye level"),
                   ("E31_pro.png", (.5, .5), "Bay D2: breakers, disconnects, trench to the relay house")],
                  "WHAT RUNS AT THE GRID CONNECTION",
                  [("HV XLPE 230 kV", "1/C 2500 KCMIL CU · XLPE · CU WIRE SHIELD · AL LAMINATE · HDPE",
                    "Underground 230 kV circuits and the CCS / modular-yard ties"),
                   ("BARE COPPER", "4/0 AWG GROUND GRID · RODS · RISERS",
                    "Station ground grid under the yard and every structure"),
                   ("TYPE TC-ER CONTROL", "600 V MULTICONDUCTOR · EXPOSED-RUN RATED",
                    "Breaker and relay circuits in the yard trenches"),
                   ("MV-105 35 kV", "1/C 500 KCMIL AL · EPR 133% · 1/3 CN · LLDPE",
                    "Station service and collector feeders")])


def hall_detail(n):
    return detail(n, "E66_pro.png", (.5, .55),
                  "OUTAGE PULL  ·  NEW 13.8 kV FEEDER FROM THE LAYDOWN BAY UP INTO THE TRAY",
                  [("E67_pro.png", (.6, .6), "ARMOR-X and MV-105 in the EL 48 tray over GT1"),
                   ("E23_pro.png", (.5, .5), "Tray stack along the hall north wall, drops to the GT skids")],
                  "WHAT RUNS IN THE TURBINE HALL",
                  [("ARMOR-X® MC-HL 15 kV", "500 KCMIL 3/C CU · NL-EPR 25% TAPE SHIELD · GROUND · RED PVC",
                    "MV feeders to auxiliary drives through the gas-turbine areas"),
                   ("ARMOR-X® MC-HL 600 V", "#14 AWG TO 750 KCMIL · XHHW-2 · CSA RA90-HL · BLACK PVC",
                    "Motor and power circuits on the enclosures and skids"),
                   ("MV-105 15 kV 133%", "1/C 500 KCMIL CU · EPR · TAPE SHIELD · PVC · UL 1072",
                    "Switchgear to transformers and large motors"),
                   ("TYPE TC-ER", "600 V POWER AND CONTROL · EXPOSED-RUN RATED",
                    "Control, protection and instrument circuits along the tray")])


def index(n):
    img = Image.new("RGB", (W, H), BG)
    photo_right(img, "K1_pro.png", 1960, 1760, (.5, .5))
    d = ImageDraw.Draw(img)
    tracked(d, (M, 110), "PRODUCT INDEX", F(BOLD, 30), COPPER, 4)
    d.text((M, 150), "ONE SUPPLIER, GRID TO STACK", font=F(XBOLD, 84), fill=WHITE)
    rows = [("GRID CONNECTION", "HV XLPE transmission cable", "230 kV", "ICEA S-108-720"),
            ("", "Bare copper grounding", "4/0 AWG", "—"),
            ("POWER ISLAND", "ARMOR-X® MC-HL, red PVC", "15 kV", "UL 1569 / 2225"),
            ("", "ARMOR-X® MC-HL, black PVC, CSA RA90-HL", "600 V", "UL 1569 / 2225"),
            ("", "MV-105 EPR 133%", "15 kV", "UL 1072"),
            ("", "Type TC-ER power and control", "600 V", "UL 1277"),
            ("CARBON CAPTURE", "ARMOR-X, MV-105, TC-ER, PLTC", "300 V – 15 kV", "UL 13 / 1072 / 1277"),
            ("BATTERY STORAGE", "PV / RHW-2 DC conductor", "2 kV", "UL 4703"),
            ("", "MV-105 collection", "35 kV", "UL 1072"),
            ("MODULAR POWER", "Type SHD-GC portable power cable", "15 kV", "ICEA S-75-381"),
            ("", "Type W portable power cable", "2000 V", "UL 1650"),
            ("INSTALLATION", "SIMpull® Reels and SIMpull Truck", "—", "—")]
    cols = (M, M + 330, M + 1000, M + 1210)
    y = 290
    for x, t in zip(cols, ("ZONE", "PRODUCT", "VOLTAGE", "STANDARD")):
        tracked(d, (x, y), t, F(BOLD, 22), DIM, 3)
    y += 40
    for z, p, v, s in rows:
        if z:
            d.line([(M, y), (M + 1540, y)], fill=RULE, width=2)
        d.text((cols[0], y + 12), z, font=F(BOLD, 25), fill=COPPER)
        d.text((cols[1], y + 10), p, font=F(REG, 27), fill=WHITE)
        d.text((cols[2], y + 10), v, font=F(REG, 27), fill=GREY)
        d.text((cols[3], y + 10), s, font=F(REG, 27), fill=GREY)
        y += 56
    d.line([(M, y), (M + 1540, y)], fill=RULE, width=2)
    y += 50
    B.logo(img, (M, y), 520)
    d.text((M + 640, y - 4), "Stephan Hardt", font=F(XBOLD, 44), fill=WHITE)
    d.text((M + 640, y + 54), "Power Generation Solutions", font=F(REG, 28), fill=GREY)
    d.text((M + 640, y + 94), "stephan.hardt@southwire.com", font=F(REG, 28), fill=COPPER)
    para(d, (M, H - FOOT - 112), "Renders are conceptual illustrations from the SK-3X1 3D model: not engineered, "
         "not for construction. Product constructions are typical; confirm ratings, sizes and listings against "
         "current Southwire specifications. ARMOR-X and SIMpull are registered trademarks of Southwire Company, LLC.",
         F(REG, 20), DIM, 1540, 1.4)
    footer(d, n)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    z = {q["n"]: q for q in B.ZONES}
    slides = [overview(2), where(3), zone(z["01"], 4), grid_detail(5), zone(z["02"], 6), hall_detail(7),
              zone(z["03"], 8), zone(z["04"], 9), zone(z["05"], 10), zone(z["06"], 11), index(12)]
    for k, s in enumerate(slides, 2):
        s.save(os.path.join(OUT, f"slide_{k:02d}.png"))
        s.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(OUT, f"slide_{k:02d}_preview.jpg"), quality=88)
    pages = ([Image.open(COVER_PNG).convert("RGB").resize((W, H), Image.LANCZOS)] if os.path.exists(COVER_PNG) else []) + slides
    pdf = os.path.join(PLANT, "renders", "deck", "SK-3X1_Strategy_Update_October_2026.pdf")
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=144)
    print("wrote", pdf, len(pages), "slides")


if __name__ == "__main__":
    main()
