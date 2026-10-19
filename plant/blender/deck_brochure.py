"""The wire & cable brochure as 16:9 deck slides, to follow the Strategy Monthly Update cover (deck_divider.py
strategy): same copy, products and model-measured numbers as brochure.py, laid out landscape in the cover's look
(charcoal field, diagonal photo edge, Barlow Condensed, copper). Pictures are the current renders of the SW-3X1
model (renders/epic, renders/cover).

    python blender/deck_brochure.py        # -> renders/deck/brochure_slides/slide_02..14.png + one PDF with the cover
"""
import os

from PIL import Image, ImageDraw

import brochure as B
from brochure import BG, PANEL, COPPER, COPPER_D, WHITE, GREY, DIM, RULE, BOLD, XBOLD, REG, F, photo, tracked, wrap

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
OUT = os.path.join(PLANT, "renders", "deck", "brochure_slides")
COVER_PNG = os.path.join(PLANT, "renders", "deck", "SW-3X1_cover_strategy_update_October.png")
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


import credit as _credit
CREDIT = (_credit.NAME.upper(), _credit.EMAIL)         # on every page (the author's decision, Oct 19)


def credit(d, y, x=None):
    """Author credit after the Southwire line in the footer: the email (it spells out the name)."""
    x0 = (M + sum(d.textlength(ch, font=F(BOLD, 26)) + 3 for ch in "SOUTHWIRE  |  POWER GENERATION SOLUTIONS") + 40
          if x is None else x)
    nf = F(BOLD, 26)
    tracked(d, (x0, y), "|", nf, DIM, 3)                     # the email alone: it spells out the name
    xe = x0 + d.textlength("|", font=nf) + 24
    d.text((xe, y - 1), CREDIT[1], font=F(REG, 26), fill=DIM)
    return xe + d.textlength(CREDIT[1], font=F(REG, 26))


def footer(d, n, note=None):
    y = H - FOOT
    d.rectangle([0, y, W, H], fill=BG)
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    tracked(d, (M, y + 30), "SOUTHWIRE  |  POWER GENERATION SOLUTIONS", F(BOLD, 26), DIM, 3)
    credit(d, y + 30)
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
    photo_right(img, "K5_pro.png", 1420, 1180, (.5, .5))
    d = ImageDraw.Draw(img)
    tracked(d, (M, 130), "SW-3X1 POWER CAMPUS", F(BOLD, 30), COPPER, 4)
    d.rectangle([M, 190, M + 96, 199], fill=COPPER)
    big = F(XBOLD, 128)
    d.text((M, 222), "ONE CAMPUS.", font=big, fill=WHITE)
    d.text((M, 352), "EVERY CABLE.", font=big, fill=COPPER)
    y = para(d, (M, 530), "A 3x1 combined-cycle plant with RICE engines, carbon capture, battery storage, a modular "
             "power yard, an LNG terminal and a behind-the-meter data centre: one campus, and from the 230 kV grid "
             "connection to the last instrument loop, all of it runs on cable. The next slides follow that cable "
             "through the plant.", F(REG, 32), GREY, 1060, 1.45)
    y += 40
    pages = {"01": 4, "02": 6, "03": 9, "04": 10, "05": 11, "06": 12}
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


def stats():
    L = B.route_feet()
    wired = sum(1 for it in B.MODEL["items"] if it.get("wiring") and it.get("area") != "L")
    return L, [(f"{L.get('tray', 0) / 5280:.1f} MI", "of cable tray routes on the racks and in the halls"),
               (f"{L.get('buried', 0) / 5280:.1f} MI", "of duct-bank and buried cable routes"),
               (f"{L.get('hv', 0):,.0f} FT", "of 230 kV underground cable routes"),
               (f"{wired}", "pieces of equipment with their own cable applications")]


def where(n):
    """The reveal: the same plant with the steel taken away, only the cable network left, lit in copper."""
    img = Image.new("RGB", (W, H), BG)
    photo_right(img, "xray_reveal.jpg", 1240, 1000, (.5, .5))
    d = ImageDraw.Draw(img)
    tracked(d, (M, 110), "THE PLANT AT A GLANCE", F(BOLD, 30), COPPER, 4)
    d.rectangle([M, 170, M + 96, 179], fill=COPPER)
    big = F(XBOLD, 118)
    d.text((M, 200), "WHERE THE", font=big, fill=WHITE)
    d.text((M, 320), "CABLE GOES.", font=big, fill=COPPER)
    y = para(d, (M, 490), "Take the steel away and this is what is left: one network, from the 230 kV grid "
             "connection to the last instrument loop, in every zone of the campus.", F(REG, 30), GREY, 900, 1.42)
    y += 40
    d.line([(M, y), (M + 900, y)], fill=RULE, width=2)
    tracked(d, (M, y + 26), "BY THE NUMBERS", F(BOLD, 30), COPPER, 4)
    _, st = stats()
    y += 90
    sw = 450
    for k, (v, t) in enumerate(st):
        x = M + (k % 2) * sw
        yy = y + (k // 2) * 220
        d.text((x, yy), v, font=F(XBOLD, 80), fill=WHITE)
        para(d, (x, yy + 98), t, F(REG, 24), GREY, sw - 50, 1.3)
    para(d, (M, H - FOOT - 90), "Route lengths measured along the modelled tray, duct-bank and cable routes "
         "(not cable footage); data-centre campus excluded. Picture: the 3D model in cable X-ray.", F(REG, 20), DIM, 900, 1.35)
    footer(d, n)
    return img


def bookend(n):
    """Close: the whole campus as cable, with the cover's claim."""
    img = Image.new("RGB", (W, H), BG)
    pw = 2200                                        # photo on the right two thirds, fading into the field
    img.paste(photo("xray_bookend.jpg", (pw, H - FOOT), (.7, .5)), (W - pw, 0))
    fw = 900
    g = Image.new("L", (fw, 1))
    g.putdata([int(255 * (1 - k / fw) ** 1.3) for k in range(fw)])
    img.paste(Image.new("RGB", (fw, H - FOOT), BG), (W - pw, 0), g.resize((fw, H - FOOT)))
    d = ImageDraw.Draw(img)
    tracked(d, (M, 380), "SW-3X1 POWER CAMPUS", F(BOLD, 30), COPPER, 4)
    d.rectangle([M, 440, M + 96, 449], fill=COPPER)
    big = F(XBOLD, 140)
    d.text((M, 470), "EVERY MEGAWATT", font=big, fill=WHITE)
    d.text((M, 610), "TRAVELS THROUGH", font=big, fill=WHITE)
    d.text((M, 750), "A CABLE.", font=big, fill=COPPER)
    L, _ = stats()
    total = (L.get("tray", 0) + L.get("buried", 0) + L.get("hv", 0)) / 5280
    d.text((M, 980), f"{total:.0f} MILES", font=F(XBOLD, 96), fill=WHITE)
    para(d, (M, 1090), "of modelled cable routes on one campus, from the 230 kV grid connection to the last "
         "instrument loop.", F(REG, 30), GREY, 1000, 1.4)
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
    d.rectangle([mx - 2, iy - 2, mx + mw + 2, iy + mh + 2], fill=(18, 20, 23), outline=RULE, width=2)
    loc = os.path.join(PLANT, "renders", "cover", f"xray_loc{z['n']}.jpg")
    if os.path.exists(loc):                        # the campus X-ray with this zone lit in copper (as slide 3)
        img.paste(photo(loc, (mw, mh), (.5, .5)), (mx, iy))
    else:
        mp = B.plan_map((mw, mh), z["areas"])
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


def hall_inside(n):
    """Inside the turbine hall: the whole hall from the bridge crane over the laydown bay to the steam turbine (camera HALL9, cutaway: south wall and roof lifted), the visible cable energised in copper
    (hero_cable.py), callouts projected from the model, and the hall's cable numbers measured from the model."""
    import math
    img = Image.new("RGB", (W, H), BG)
    x_top, x_bot = 1240, 1000
    photo_right(img, "HALL9_hero_cable.jpg", x_top, x_bot, (.15, .5))
    ox = min(x_top, x_bot)                           # photo's left edge on the slide
    d = ImageDraw.Draw(img)
    # callouts: model points through the HALL1 camera (sensor fit on the longer side, as Blender's AUTO)
    eye, tgt, lens = (430, 232, 275), (770, 470, 28), 24          # camera HALL9
    f = [t - e for t, e in zip(tgt, eye)]
    fl = math.sqrt(sum(v * v for v in f)); f = [v / fl for v in f]
    r = [f[1], -f[0], 0]; rl = math.hypot(r[0], r[1]); r = [v / rl for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    sw, sh = 1920, 1440                              # render size; cover-fit into the photo box as photo() does
    bw, bh = W - ox, H - FOOT
    sc = max(bw / sw, bh / sh)
    cx0 = (sw * sc - bw) * .15
    cy0 = (sh * sc - bh) * .5
    k = lens / 36 * sw
    def proj(p):
        dv = [a - b for a, b in zip(p, eye)]
        z = sum(a * b for a, b in zip(dv, f))
        px = sw / 2 + sum(a * b for a, b in zip(dv, r)) / z * k
        py = sh / 2 - sum(a * b for a, b in zip(dv, u)) / z * k
        return ox + px * sc - cx0, py * sc - cy0
    for name, p, dy in (("BRIDGE CRANE", (518, 481, 96), -90), ("GT1", (636, 497, 38), -90), ("GT2", (796, 497, 38), -90), ("GT3", (956, 497, 38), -90),
                        ("STEAM TURBINE", (1050, 506, 40), 90)):       # ST label below: the wall sign is above it
        x, y = proj(p)
        if not (ox + 60 < x < W - 120 and 160 < y < H - FOOT - 60):
            continue
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=COPPER)
        d.line([(x, y), (x, y + dy)], fill=COPPER, width=3)
        tf = F(BOLD, 28)
        tw = d.textlength(name, font=tf) + 2 * len(name) + 34      # tracked text plus padding
        yb = y + dy - 50 if dy < 0 else y + dy
        d.rectangle([x - 4, yb, x - 4 + tw, yb + 50], fill=(20, 22, 25))
        tracked(d, (x + 10, yb + 8), name, tf, WHITE, 2)
    tab(d, (M + 4, 104), "02  ·  POWER ISLAND  ·  INSIDE THE HALL")
    d.rectangle([M, 210, M + 96, 219], fill=COPPER)
    big = F(XBOLD, 112)
    d.text((M, 240), "THREE TURBINES.", font=big, fill=WHITE)
    d.text((M, 356), "ONE TRAY STACK.", font=big, fill=COPPER)
    para(d, (M, 520), "Three H-class gas turbines and the steam turbine share one hall. Every auxiliary drive, "
         "enclosure fan, lube-oil skid and protection relay is fed from the tray stack that runs the length of "
         "the hall at EL 30 to 48: medium voltage on top, 600 V power below, control and instrumentation at the "
         "bottom.", F(REG, 29), GREY, 960, 1.42)
    # numbers measured from the model inside the hall footprint
    X0, X1, Y0, Y1 = 480, 1100, 370, 560
    Lt = {}
    for rt in B.MODEL["routes"]:
        pts = rt["points"]
        for a, b in zip(pts, pts[1:]):
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if X0 <= mx <= X1 and Y0 <= my <= Y1:
                Lt[rt["type"]] = Lt.get(rt["type"], 0) + math.dist(a, b)
    tray = sum(v for t, v in Lt.items() if t.endswith("_tray"))
    wired = sum(1 for it in B.MODEL["items"] if it.get("wiring") and it.get("fp") and len(it["fp"]) == 4
                and not isinstance(it["fp"][0], list) and X0 <= (it["fp"][0] + it["fp"][1]) / 2 <= X1
                and Y0 <= (it["fp"][2] + it["fp"][3]) / 2 <= Y1)
    st = [(f"{tray:,.0f} FT", "of cable tray inside the hall"),
          (f"{Lt.get('mv_tray', 0):,.0f} FT", "of it 15 kV medium-voltage tray"),
          (f"{Lt.get('ipb', 0):,.0f} FT", "of isolated-phase bus, generators to GSUs"),
          (f"{wired}", "pieces of equipment in the hall with their own cable")]
    y0 = 860
    cw = 480
    d.line([(M, y0 - 30), (M + 960, y0 - 30)], fill=RULE, width=2)
    tracked(d, (M, y0 - 4), "THE HALL BY THE NUMBERS", F(BOLD, 28), COPPER, 4)
    for i, (v, t) in enumerate(st):
        x = M + (i % 2) * cw
        yy = y0 + 64 + (i // 2) * 220
        d.text((x, yy), v, font=F(XBOLD, 80), fill=WHITE)
        para(d, (x, yy + 98), t, F(REG, 25), GREY, cw - 60, 1.3)
    footer(d, n, "Lengths measured along the modelled routes inside the hall.")
    return img


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
    para(d, (M, H - FOOT - 112), "Renders are conceptual illustrations from the SW-3X1 3D model: not engineered, "
         "not for construction. Product constructions are typical; confirm ratings, sizes and listings against "
         "current Southwire specifications. ARMOR-X and SIMpull are registered trademarks of Southwire Company, LLC.",
         F(REG, 20), DIM, 1540, 1.4)
    footer(d, n)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    z = {q["n"]: q for q in B.ZONES}
    slides = [overview(2), where(3), zone(z["01"], 4), grid_detail(5), zone(z["02"], 6), hall_detail(7), hall_inside(8),
              zone(z["03"], 9), zone(z["04"], 10), zone(z["05"], 11), zone(z["06"], 12), bookend(13), index(14)]
    for k, s in enumerate(slides, 2):
        s.save(os.path.join(OUT, f"slide_{k:02d}.png"))
        s.resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(OUT, f"slide_{k:02d}_preview.jpg"), quality=88)
    # the cover carries the credit in its own block (deck_divider.py: name, role, email)
    pages = [Image.open(COVER_PNG).convert("RGB").resize((W, H), Image.LANCZOS)] if os.path.exists(COVER_PNG) else []
    pages += slides
    pdf = os.path.join(PLANT, "renders", "deck", "SW-3X1_Strategy_Update_October_2026.pdf")
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=144)
    print("wrote", pdf, len(pages), "slides")


if __name__ == "__main__":
    main()
