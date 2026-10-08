"""Wire & cable brochure for the gas power campus: 12 letter-portrait pages (PNG each + one PDF), in the
branding of the PowerGen deck (dark panel with a diagonal edge, Barlow Condensed, copper accents, logo).

Every picture is a render of the SK-3X1 model (renders/epic, renders/cover); the locator maps and the
"by the numbers" figures are drawn / measured from the model JSON. Product lines follow the legends printed on
the cables in the model and the customer's ARMOR-X list; they are typical and must be confirmed against
current Southwire specifications before release.

    python blender/brochure.py            # all pages -> renders/brochure/
"""
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DECK = os.path.join(HERE, "deck")
EPIC = os.path.join(PLANT, "renders", "epic")
COVER = os.path.join(PLANT, "renders", "cover")
OUT = os.path.join(PLANT, "renders", "brochure")
W, H = 2550, 3300                                     # letter at 300 dpi
M = 170                                               # outer margin
BG, PANEL, COPPER, COPPER_D, WHITE, GREY, DIM, RULE = (
    (14, 16, 18), (20, 22, 25), (227, 154, 95), (180, 88, 31), (245, 243, 239), (201, 205, 210), (138, 143, 149),
    (58, 63, 69))
MODEL = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))


def F(name, px):
    path = os.path.join(DECK, name)
    return ImageFont.truetype(path, int(px))


BOLD, XBOLD, REG = "BarlowCondensed-Bold.ttf", "BarlowCondensed-ExtraBold.ttf", "Barlow-Regular.ttf"


def finish(ph):
    import random
    w, h = ph.size
    rnd = random.Random(7)
    g = Image.new("L", (w // 2, h // 2))
    g.putdata([128 + int(rnd.gauss(0, 9)) for _ in range((w // 2) * (h // 2))])
    g = g.resize((w, h), Image.BILINEAR)
    return Image.blend(ph, Image.merge("RGB", (g, g, g)), .03)


def photo(name, box, focus=(.5, .5), crop=None):
    """Load a render and cover-fit it into box=(w, h); focus = where to keep (0..1); crop = source pixel box."""
    p = name if os.path.isabs(name) else next(q for q in (os.path.join(EPIC, name), os.path.join(COVER, name))
                                              if os.path.exists(q))
    im = Image.open(p).convert("RGB")
    if crop:
        im = im.crop(crop)
    bw, bh = box
    s = max(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    ox = int((im.width - bw) * focus[0])
    oy = int((im.height - bh) * focus[1])
    return finish(im.crop((ox, oy, ox + bw, oy + bh)))


def tracked(d, xy, text, font, fill, track=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x


def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def para(d, xy, text, font, fill, width, lead=1.42):
    x, y = xy
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += font.size * lead
    return y


def logo(img, xy, w):
    lg = Image.open(os.path.join(DECK, "southwire_pgs_logo.png")).convert("RGBA")
    lg = lg.resize((w, round(lg.height * w / lg.width)), Image.LANCZOS)
    img.paste(lg, xy, lg)


def footer(d, page, note=None):
    y = H - 150
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    tracked(d, (M, y + 34), "SOUTHWIRE  |  POWER GENERATION SOLUTIONS", F(BOLD, 34), DIM, 3)
    s = f"{page:02d}"
    ft = F(BOLD, 34)
    d.text((W - M - d.textlength(s, font=ft), y + 34), s, font=ft, fill=COPPER)
    if note:
        nf = F(REG, 26)
        d.text((W - M - 90 - d.textlength(note, font=nf), y + 40), note, font=nf, fill=DIM)


def diagonal_panel(img, y_left, y_right, shadow=True):
    """Dark panel from a slanted top edge to the page bottom (the deck's diagonal, turned for portrait)."""
    d = ImageDraw.Draw(img)
    if shadow:
        sh = Image.new("L", img.size, 0)
        sd = ImageDraw.Draw(sh)
        for k in range(60):
            a = int(120 * (1 - k / 60) ** 2)
            sd.line([(0, y_left - k), (W, y_right - k)], fill=a, width=1)
        img.paste(Image.new("RGB", img.size, BG), (0, 0), sh)
    d.polygon([(0, y_left), (W, y_right), (W, H), (0, H)], fill=BG)


def plan_map(size, hi_areas=(), numbers=None, accent=COPPER, soft=False):
    """Top-down plan of the campus drawn from the model: every item footprint, the highlighted zone in copper,
    optional numbered markers {num: (x, y)} in plant feet."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, x1, y0, y1 = -40, 3420, -60, 1960
    s = min((w - 20) / (x1 - x0), (h - 20) / (y1 - y0))
    ox = (w - (x1 - x0) * s) / 2
    oy = (h - (y1 - y0) * s) / 2
    P = lambda x, y: (ox + (x - x0) * s, oy + (y1 - y) * s)
    d.rectangle([P(0, 1920), P(2420, 0)], outline=(90, 96, 102), width=2)             # compound fence
    for it in MODEL["items"]:
        f = it.get("fp")
        if not f or len(f) != 4 or it["layer"] in ("SITE", "UNDERGROUND", "OPT_UNDERGROUND") or it["layer"].endswith("ROUTES"):
            continue
        if (f[1] - f[0]) > 900 or (f[3] - f[2]) > 900 or it["z"][1] < .6:
            continue
        a = it.get("area", "")
        hl = a in hi_areas
        col = ((150, 98, 64, 255) if soft else accent + (255,)) if hl else ((84, 90, 96, 255) if a != "L" else (62, 67, 72, 255))
        d.rectangle([P(f[0], f[3]), P(f[1], f[2])], fill=col)
    for it in MODEL["items"]:                                                         # roads
        if it["layer"] == "SITE" and "road" in it["name"].lower():
            f = it["fp"]
            d.rectangle([P(f[0], f[3]), P(f[1], f[2])], fill=(44, 48, 52, 255))
    if numbers:
        nf = F(XBOLD, int(h * .075))
        for num, (x, y) in numbers.items():
            cx, cy = P(x, y)
            r = h * .055
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COPPER + (255,), outline=WHITE + (255,), width=5)
            tw = d.textlength(num, font=nf)
            d.text((cx - tw / 2, cy - nf.size * .6), num, font=nf, fill=WHITE + (255,))
    return img


def chips(d, xy, items, width):
    """Spec chips: small outlined boxes in a row (wrapping)."""
    x, y = xy
    f = F(BOLD, 34)
    for t in items:
        tw = d.textlength(t, font=f) + 44
        if x + tw > xy[0] + width:
            x, y = xy[0], y + 78
        d.rounded_rectangle([x, y, x + tw, y + 60], radius=8, outline=COPPER, width=3)
        d.text((x + 22, y + 10), t, font=f, fill=WHITE)
        x += tw + 18
    return y + 78


# ---------------------------------------------------------------------------------------------------------------
# zones: hero, inset, copy, products, locator areas
ZONES = [
    dict(n="01", kicker="GRID CONNECTION", title=("230 kV", "TO THE GRID"), hero="E60_pro.png", hf=(.5, .55),
         inset="E19_pro.png", inset_cap="Generator step-up transformers facing the switchyard",
         areas=("C",), page=4,
         intro="The plant's output leaves through four generator step-up transformers and a breaker-and-a-half "
               "230 kV switchyard. Where the line runs underground, high-voltage XLPE cable rises on cleated "
               "risers to sealing ends and surge arresters.",
         points=[("HV XLPE transmission cable", "Copper conductor, XLPE insulation, aluminium laminate moisture "
                  "barrier and HDPE jacket for the buried 230 kV run."),
                 ("Fewer joints", "Long continuous lengths keep splices out of the duct bank."),
                 ("One supplier", "Cable, accessories and field support for the complete circuit.")],
         chips=["230 kV", "2500 KCMIL CU", "XLPE", "AL LAMINATE", "ICEA S-108-720", "4/0 BARE CU GROUND"]),
    dict(n="02", kicker="POWER ISLAND  ·  TURBINE HALL", title=("ARMOR-X", "IN THE TRAY"), hero="E70_pro.png",
         hf=(.5, .62), inset="E70_pro.png", inset_crop=(380, 1080, 1560, 1500),
         inset_cap="The legend on every jacket: ARMOR-X MC-HL 15 kV beside MV-105",
         areas=("A",), page=6,
         intro="Three H-class gas turbines and a steam turbine share one hall. 15 kV ARMOR-X MC-HL and MV-105 run "
               "from the 13.8 kV switchgear across the tray stack to every auxiliary drive, with 600 V ARMOR-X "
               "and Type TC-ER for power and control in the gas-turbine enclosures.",
         points=[("Hazardous-location rated", "MC-HL: continuously welded, corrugated aluminium armor under a "
                  "PVC jacket, for the Class I, Div. 2 areas around the gas turbines."),
                 ("No conduit", "Armored cable goes straight into the tray: fewer trades, faster pulls."),
                 ("Readable everywhere", "Printed legend on the jacket for identification at every drop.")],
         chips=["15 kV MV-105 133% · RED PVC", "600 V CSA RA90-HL · BLACK PVC", "UL 1569 / UL 2225", "TYPE TC-ER",
                "MV-105 · UL 1072"]),
    dict(n="03", kicker="CARBON CAPTURE", title=("CABLE THAT", "RUNS CCS"), hero="E68_pro.png", hf=(.5, .45),
         inset="E57_pro.png", inset_cap="CCS transformers T-1 / T-2: 230 kV terminations and the tray riser",
         areas=("G",), page=8,
         intro="Absorbers, strippers and 16 MW booster fans: post-combustion capture adds a second plant's worth "
               "of motors, drives and instruments, all fed from the CCS rack.",
         points=[("ARMOR-X on the rack", "Jacketed armor for the process area's power circuits."),
                 ("15 kV feeders", "MV-105 to the fans and the CO2 compressors."),
                 ("Instrumentation", "PLTC and Type TC-ER for the absorber and regeneration loops.")],
         chips=["230 kV XLPE", "15 kV MV-105", "600 V ARMOR-X", "TYPE TC-ER", "PLTC"]),
    dict(n="04", kicker="BATTERY STORAGE", title=("DC IN THE", "TRENCH"), hero="E65_pro.png", hf=(.5, .5),
         inset="E62_pro.png", inset_cap="PCS / MV skid: 34.5 kV elbow terminations to the collector",
         areas=("H",), page=9,
         intro="The battery yard pairs containers with power-conversion skids. 1,500 V DC conductors run in "
               "precast trenches; 35 kV MV-105 collects the skids to the BESS substation.",
         points=[("PV / RHW-2", "Sunlight- and moisture-resistant 2 kV conductors for the DC side."),
                 ("MV collection", "35 kV MV-105 loop feeds with load-break elbows."),
                 ("Pulled on site", "Crews pay off from reels straight into the open trench.")],
         chips=["2 kV PV / RHW-2", "UL 4703", "35 kV MV-105", "UL 1072"]),
    dict(n="05", kicker="MODULAR & TEMPORARY POWER", title=("POWER THAT", "MOVES"), hero="E77_pro.png", hf=(.5, .5),
         inset="E78_pro.png", inset_cap="Type W sets with cam-lock plugs into the 480 V switchboard",
         areas=("I",), page=10,
         intro="Gensets, trailer turbines and bridge-power fleets come and go. Portable power cable lies on the "
               "pad, crosses lanes under drive-over protectors and plugs in with cam-locks; bridge units feed "
               "through ground trays to the permanent duct bank.",
         points=[("Type SHD-GC", "Flexible 15 kV portable power cable for the MV feeders."),
                 ("Type W", "2000 V single conductors with cam-lock connections for 480 V hookups."),
                 ("MV-105 leads", "Generator leads from the TM2500 terminal boxes in ground trays.")],
         chips=["15 kV SHD-GC", "ICEA S-75-381", "2000 V TYPE W", "CAM-LOCK", "15 kV MV-105"]),
    dict(n="06", kicker="INSTALLED FASTER", title=("ACCELERATING", "TIME TO POWER™"), hero="E64_pro.png",
         hf=(.5, .5), inset="E58_pro.png", inset_cap="The cable reel yard: SIMpull Reels staged for the pulls",
         areas=("I",), page=11,
         intro="Schedule is decided in the field. The SIMpull Truck delivers multi-conductor SIMpull Reels and "
               "pays them off at the pull, so a feeder goes in with one setup instead of three.",
         points=[("SIMpull Reels", "Paralleled conductors on one reel: one pull per feeder."),
                 ("SIMpull Truck", "Delivery, payoff and reel return in one vehicle."),
                 ("Fewer setups", "Less reel handling on site, faster energization.")],
         chips=["SIMPULL® REELS", "SIMPULL TRUCK", "JOBSITE SERVICES"]),
]
NOTE = "Product data typical; confirm against current Southwire specifications."


def zone_page(z):
    img = Image.new("RGB", (W, H), BG)
    hero_h = 1880
    img.paste(photo(z["hero"], (W, hero_h), z["hf"]), (0, 0))
    diagonal_panel(img, 1560, 1840)
    d = ImageDraw.Draw(img)
    # zone tab on the photo
    tf = F(BOLD, 40)
    tab = f"{z['n']}  ·  {z['kicker']}"
    tw = tracked(ImageDraw.Draw(Image.new("L", (1, 1))), (0, 0), tab, tf, 0, 4)
    d.rectangle([M - 30, 150, M + tw + 30, 228], fill=COPPER_D)
    tracked(d, (M, 164), tab, tf, WHITE, 4)
    # title block (left)
    y = 1700
    d.rectangle([M, y, M + 120, y + 12], fill=COPPER)
    y += 50
    big = F(XBOLD, 170)
    d.text((M, y), z["title"][0], font=big, fill=WHITE)
    d.text((M, y + 170), z["title"][1], font=big, fill=COPPER)
    y += 400
    y = para(d, (M, y), z["intro"], F(REG, 44), GREY, 1300)
    # three points
    y += 50
    for k, (head, body) in enumerate(z["points"]):
        d.text((M, y), f"{k + 1:02d}", font=F(XBOLD, 54), fill=COPPER)
        d.text((M + 100, y + 4), head.upper(), font=F(BOLD, 48), fill=WHITE)
        y = para(d, (M + 100, y + 66), body, F(REG, 38), GREY, 1200, 1.38) + 34
    # right column: inset photo, caption, chips, locator
    cx, cw = 1600, W - M - 1600
    cy = 1960
    ins = photo(z["inset"], (cw, 520), (.5, .5), z.get("inset_crop"))
    img.paste(ins, (cx, cy))
    d.rectangle([cx - 3, cy - 3, cx + cw + 3, cy + 523], outline=COPPER, width=4)
    cy = para(d, (cx, cy + 550), z["inset_cap"], F(REG, 32), DIM, cw, 1.35) + 30
    cy = int(chips(d, (cx, int(cy)), z["chips"], cw) + 20)
    mh = min(int(cw * .58), H - 200 - 60 - cy)                        # keep clear of the footer
    mp = plan_map((cw, mh), z["areas"])
    img.paste(mp, (cx, cy), mp)
    tracked(d, (cx, cy + mh + 8), "WHERE IN THE PLANT", F(BOLD, 28), DIM, 3)
    footer(d, z["page"], NOTE)
    return img


def detail_page(page):
    """Second power-island page: three photos and the product cards for the turbine hall."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    img.paste(photo("E66_pro.png", (W, 1300), (.5, .55)), (0, 0))
    hw = (W - 2 * M - 40) // 2
    img.paste(photo("E67_pro.png", (hw, 760), (.6, .6)), (M, 1340))
    img.paste(photo("E23_pro.png", (hw, 760), (.5, .5)), (M + hw + 40, 1340))
    cap = F(REG, 30)
    d.text((M, 2112), "ARMOR-X and MV-105 in the EL 48 tray over GT1", font=cap, fill=DIM)
    d.text((M + hw + 40, 2112), "Tray stack along the hall north wall, drops to the GT skids", font=cap, fill=DIM)
    tracked(d, (M, 1200), "OUTAGE PULL  ·  NEW 13.8 kV FEEDER FROM THE LAYDOWN BAY UP INTO THE TRAY", F(BOLD, 38), WHITE, 3)
    y = 2210
    tracked(d, (M, y), "WHAT RUNS IN THE TURBINE HALL", F(BOLD, 44), COPPER, 4)
    y += 90
    cards = [("ARMOR-X® MC-HL 15 kV", "500 KCMIL 3/C CU · NL-EPR 25% TAPE SHIELD · GROUND · RED PVC",
              "MV feeders to auxiliary drives through the gas-turbine areas"),
             ("ARMOR-X® MC-HL 600 V", "#14 AWG TO 750 KCMIL · XHHW-2 · CSA RA90-HL · BLACK PVC",
              "Motor and power circuits on the enclosures and skids"),
             ("MV-105 15 kV 133%", "1/C 500 KCMIL CU · EPR · TAPE SHIELD · PVC · UL 1072",
              "Switchgear to transformers and large motors"),
             ("TYPE TC-ER", "600 V POWER AND CONTROL · EXPOSED-RUN RATED",
              "Control, protection and instrument circuits along the tray")]
    cw = (W - 2 * M - 40) // 2
    for k, (head, spec, use) in enumerate(cards):
        x = M + (k % 2) * (cw + 40)
        yy = y + (k // 2) * 330
        d.rectangle([x, yy, x + cw, yy + 300], fill=PANEL)
        d.rectangle([x, yy, x + 10, yy + 300], fill=COPPER)
        d.text((x + 50, yy + 36), head, font=F(XBOLD, 60), fill=WHITE)
        d.text((x + 50, yy + 120), spec, font=F(BOLD, 31), fill=COPPER)
        para(d, (x + 50, yy + 180), use, F(REG, 34), GREY, cw - 90)
    footer(d, page, NOTE)
    return img


def cover():
    img = Image.new("RGB", (W, H), BG)
    img.paste(photo("K11_pro.png", (W, 2350), (.36, .5)), (0, H - 2350))
    d = ImageDraw.Draw(img)
    # dark panel from the top with the diagonal lower edge
    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for k in range(70):
        sd.line([(0, 1560 + k), (W, 1180 + k)], fill=int(130 * (1 - k / 70) ** 2), width=1)
    img.paste(Image.new("RGB", (W, H), BG), (0, 0), sh)
    d.polygon([(0, 0), (W, 0), (W, 1180), (0, 1560)], fill=BG)
    logo(img, (M, 170), 900)
    d.rectangle([M, 520, M + 150, 534], fill=COPPER)
    tracked(d, (M, 580), "POWER GENERATION SOLUTIONS", F(BOLD, 52), GREY, 6)
    big = F(XBOLD, 230)
    d.text((M, 660), "WIRE & CABLE", font=big, fill=WHITE)
    d.text((M, 880), "FOR GAS POWER", font=big, fill=COPPER)
    tracked(d, (M, 1150), "GAS POWER CAMPUS  ·  FROM THE GRID TO THE STACK", F(BOLD, 56), WHITE, 4)
    tracked(d, (M, 1240), "ACCELERATING TIME TO POWER™", F(XBOLD, 64), COPPER, 4)
    # bottom strip
    d.rectangle([0, H - 170, W, H], fill=BG)
    tracked(d, (M, H - 120), "SOUTHWIRE.COM  |  POWER GENERATION SOLUTIONS", F(BOLD, 40), GREY, 4)
    return img


def overview_left(page):
    img = Image.new("RGB", (W, H), BG)
    img.paste(photo("K5_pro.png", (W, 1800), (.5, .5)), (0, 0))
    diagonal_panel(img, 1500, 1760)
    d = ImageDraw.Draw(img)
    y = 1660
    d.rectangle([M, y, M + 120, y + 12], fill=COPPER)
    big = F(XBOLD, 170)
    d.text((M, y + 50), "ONE CAMPUS.", font=big, fill=WHITE)
    d.text((M, y + 220), "EVERY CABLE.", font=big, fill=COPPER)
    y = para(d, (M, y + 460), "A 3x1 combined-cycle plant with carbon capture, battery storage, a modular "
             "power yard, an LNG terminal and a behind-the-meter data centre: one campus, and from the 230 kV "
             "grid connection to the last instrument loop, all of it runs on cable. This brochure follows that "
             "cable through the plant.", F(REG, 46), GREY, W - 2 * M)
    y += 60
    rows = [(z["n"], z["kicker"], z["page"]) for z in ZONES]
    for n, k, p in rows:
        d.line([(M, y), (W - M, y)], fill=RULE, width=2)
        d.text((M, y + 22), n, font=F(XBOLD, 56), fill=COPPER)
        tracked(d, (M + 120, y + 28), k, F(BOLD, 50), WHITE, 3)
        s = f"PAGE {p:02d}"
        d.text((W - M - d.textlength(s, font=F(BOLD, 40)), y + 34), s, font=F(BOLD, 40), fill=DIM)
        y += 104
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    footer(d, page)
    return img


def route_feet():
    L = {}
    for r in MODEL["routes"]:
        if r["layer"].startswith("OPT_DC"):
            continue
        n = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(r["points"], r["points"][1:]))
        t = r["type"]
        key = ("tray" if t in ("mv_tray", "lv_tray", "control_tray") and r["z"] > 0 else
               "hv" if t == "hv_cable" else
               "surface" if r.get("surface") else
               "buried" if t in ("duct_bank", "mvlv_cable", "lv_tray") and r["z"] < 0 else None)
        if key:
            L[key] = L.get(key, 0) + n
    return L


def overview_right(page):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    tracked(d, (M, 190), "THE PLANT AT A GLANCE", F(BOLD, 48), COPPER, 5)
    d.text((M, 260), "WHERE THE CABLE GOES", font=F(XBOLD, 150), fill=WHITE)
    cent = {}
    for z in ZONES[:5]:
        xs, ys = [], []
        for it in MODEL["items"]:
            f = it.get("fp")
            if it.get("area") in z["areas"] and f and len(f) == 4 and (f[1] - f[0]) < 400 and it["z"][1] > 2:
                xs.append((f[0] + f[1]) / 2)
                ys.append((f[2] + f[3]) / 2)
        cent[z["n"]] = (sorted(xs)[len(xs) // 2], sorted(ys)[len(ys) // 2])
    mw = W - 2 * M
    mp = plan_map((mw, int(mw * .62)), sum((z["areas"] for z in ZONES[:5]), ()), cent, soft=True)
    img.paste(mp, (M, 520), mp)
    y = 520 + int(mw * .62) + 30
    tracked(d, (M, y), "SK-3X1 CAMPUS PLAN, DRAWN FROM THE 3D MODEL  ·  NORTH UP", F(BOLD, 30), DIM, 3)
    leg = [(z["n"], z["kicker"].split("  ·  ")[0]) for z in ZONES[:5]]
    y += 80
    for k, (n, t) in enumerate(leg):
        x = M + (k % 3) * (mw // 3)
        yy = y + (k // 3) * 80
        d.text((x, yy), n, font=F(XBOLD, 48), fill=COPPER)
        d.text((x + 80, yy + 4), t, font=F(BOLD, 44), fill=WHITE)
    # by the numbers
    L = route_feet()
    wired = sum(1 for it in MODEL["items"] if it.get("wiring") and it.get("area") != "L")
    stats = [(f"{L.get('tray', 0) / 5280:.1f} MI", "of cable tray routes on the racks and in the halls"),
             (f"{L.get('buried', 0) / 5280:.1f} MI", "of duct-bank and buried cable routes"),
             (f"{L.get('hv', 0):,.0f} FT", "of 230 kV underground cable routes"),
             (f"{wired}", "pieces of equipment with their own cable applications")]
    y = 2420
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    tracked(d, (M, y + 40), "BY THE NUMBERS", F(BOLD, 44), COPPER, 5)
    y += 130
    sw = mw // 4
    for k, (v, t) in enumerate(stats):
        x = M + k * sw
        d.text((x, y), v, font=F(XBOLD, 120), fill=WHITE)
        para(d, (x, y + 150), t, F(REG, 34), GREY, sw - 50, 1.35)
    d.text((M, H - 230), "Route lengths measured along the modelled tray, duct-bank and cable routes (not cable "
           "footage); data-centre campus excluded.", font=F(REG, 28), fill=DIM)
    footer(d, page)
    return img


def grid_detail(page):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    img.paste(photo("E20_pro.png", (W, 1400), (.5, .5)), (0, 0))
    hw = (W - 2 * M - 40) // 2
    img.paste(photo("E4_pro.png", (hw, 760), (.5, .5)), (M, 1440))
    img.paste(photo("E31_pro.png", (hw, 760), (.5, .5)), (M + hw + 40, 1440))
    cap = F(REG, 30)
    d.text((M, 2212), "Along the switchyard at eye level", font=cap, fill=DIM)
    d.text((M + hw + 40, 2212), "Bay D2: breakers, disconnects, trench to the relay house", font=cap, fill=DIM)
    tracked(d, (M, 1300), "THE 230 kV SWITCHYARD  ·  SIX BREAKER-AND-A-HALF DIAMETERS", F(BOLD, 38), WHITE, 3)
    y = 2310
    tracked(d, (M, y), "WHAT RUNS AT THE GRID CONNECTION", F(BOLD, 44), COPPER, 4)
    y += 90
    cards = [("HV XLPE 230 kV", "1/C 2500 KCMIL CU · XLPE · CU WIRE SHIELD · AL LAMINATE · HDPE",
              "Underground 230 kV circuits and the CCS / modular-yard ties"),
             ("BARE COPPER", "4/0 AWG GROUND GRID · RODS · RISERS",
              "Station ground grid under the yard and every structure"),
             ("TYPE TC-ER CONTROL", "600 V MULTICONDUCTOR · EXPOSED-RUN RATED",
              "Breaker and relay circuits in the yard trenches"),
             ("MV-105 35 kV", "1/C 500 KCMIL AL · EPR 133% · 1/3 CN · LLDPE",
              "Station service and collector feeders")]
    cw = (W - 2 * M - 40) // 2
    for k, (head, spec, use) in enumerate(cards):
        x = M + (k % 2) * (cw + 40)
        yy = y + (k // 2) * 330
        d.rectangle([x, yy, x + cw, yy + 300], fill=PANEL)
        d.rectangle([x, yy, x + 10, yy + 300], fill=COPPER)
        d.text((x + 50, yy + 36), head, font=F(XBOLD, 60), fill=WHITE)
        d.text((x + 50, yy + 120), spec, font=F(BOLD, 31), fill=COPPER)
        para(d, (x + 50, yy + 180), use, F(REG, 34), GREY, cw - 90)
    footer(d, page, NOTE)
    return img


def back(page):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    img.paste(photo("K1_pro.png", (W, 900), (.5, .5)), (0, 0))
    diagonal_panel(img, 820, 900)
    tracked(d, (M, 1000), "PRODUCT INDEX", F(BOLD, 48), COPPER, 5)
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
    cols = (M, M + 560, M + 1520, M + 1820)
    y = 1090
    hf = F(BOLD, 32)
    for x, t in zip(cols, ("ZONE", "PRODUCT", "VOLTAGE", "STANDARD")):
        tracked(d, (x, y), t, hf, DIM, 3)
    y += 60
    for z, p, v, s in rows:
        if z:
            d.line([(M, y), (W - M, y)], fill=RULE, width=2)
        d.text((cols[0], y + 18), z, font=F(BOLD, 36), fill=COPPER)
        d.text((cols[1], y + 16), p, font=F(REG, 38), fill=WHITE)
        d.text((cols[2], y + 16), v, font=F(REG, 38), fill=GREY)
        d.text((cols[3], y + 16), s, font=F(REG, 38), fill=GREY)
        y += 80
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 100
    logo(img, (M, y), 760)
    cx = 1380
    d.text((cx, y - 6), "Stephan Hardt", font=F(XBOLD, 60), fill=WHITE)
    d.text((cx, y + 70), "Power Generation Solutions", font=F(REG, 40), fill=GREY)
    d.text((cx, y + 126), "stephan.hardt@southwire.com", font=F(REG, 40), fill=COPPER)
    y += 300
    para(d, (M, y), "Renders are conceptual illustrations from the SK-3X1 3D model: not engineered, not for "
         "construction. Product constructions shown on cable jackets and in this index are typical; confirm "
         "ratings, sizes and listings against current Southwire specifications before use. ARMOR-X and SIMpull "
         "are registered trademarks of Southwire Company, LLC.", F(REG, 30), DIM, W - 2 * M, 1.45)
    d.text((M, H - 260), "© 2026 Southwire Company, LLC. All rights reserved.  ·  Draft for review",
           font=F(REG, 30), fill=DIM)
    footer(d, page)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    z = {q["n"]: q for q in ZONES}
    pages = [cover(), overview_left(2), overview_right(3), zone_page(z["01"]), grid_detail(5), zone_page(z["02"]),
             detail_page(7), zone_page(z["03"]), zone_page(z["04"]), zone_page(z["05"]), zone_page(z["06"]), back(12)]
    for k, p in enumerate(pages, 1):
        p.save(os.path.join(OUT, f"page_{k:02d}.jpg"), quality=92)
    pdf = os.path.join(OUT, "Southwire_Gas_Power_Campus_Cable_Brochure.pdf")
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=300)
    print("wrote", pdf)


if __name__ == "__main__":
    main()
