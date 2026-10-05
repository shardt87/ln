"""Southwire Power Generation Solutions -- NICA contractor booklet.

8 pages, US Letter portrait, saddle-stitched (two 11x17 sheets folded once).
Brand system taken from the Anixter/Wesco deck: charcoal / copper / cream,
Barlow Condensed headlines, Barlow body, numbered sections, copper rules.

Outputs (brochure/out/):
    NICA_booklet_print.pdf    single pages, 0.125 in bleed + crop marks (send to printer)
    NICA_booklet_reader.pdf   trimmed pages, no marks (email / screen)
    NICA_booklet_spreads.pdf  reader spreads (cover, 2-3, 4-5, 6-7, back) for review
    NICA_booklet.pptx         editable, one slide per page, native text and shapes
    png/page_N.png            150-dpi previews

    python3 brochure.py
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "blender", "scripts"))
from content import PAGES  # noqa: E402  (callout label positions per view)

A = os.path.join(HERE, "assets")
F = os.path.join(HERE, "fonts")
RCLEAN = os.path.join(ROOT, "renders", "clean")
OUT = os.path.join(HERE, "out")

PW, PH = 8.5, 11.0
BLEED, SLUG = 0.125, 0.25
M = 0.55                      # inner margin

# ----------------------------------------------------------------- brand
DARK = "#16171B"
DARK2 = "#23262C"
COPPER = "#B5541C"
COPPER_LT = "#E09A5C"
CREAM = "#F4F2EE"
CARD = "#FBFAF7"
INK = "#1B1C20"
MUTED = "#5C5F66"
RULE = "#D9D5CE"
RULE_D = "#3A3E45"
WHITE = "#FFFFFF"
SAND = "#EAE5DC"

FONTS = {"hx": ("BarlowC-XB", "BarlowCondensed-ExtraBold.ttf"),
         "hb": ("BarlowC-B", "BarlowCondensed-Bold.ttf"),
         "hs": ("BarlowC-SB", "BarlowCondensed-SemiBold.ttf"),
         "r": ("Barlow", "Barlow-Regular.ttf"),
         "m": ("Barlow-M", "Barlow-Medium.ttf"),
         "sb": ("Barlow-SB", "Barlow-SemiBold.ttf")}
PPT_FONT = {"hx": ("Barlow Condensed ExtraBold", True), "hb": ("Barlow Condensed", True),
            "hs": ("Barlow Condensed SemiBold", False), "r": ("Barlow", False),
            "m": ("Barlow Medium", False), "sb": ("Barlow SemiBold", True)}

IMG = {
    "cover": os.path.join(A, "p01_x4_994x880.png"),
    "logo": os.path.join(A, "logo_light.png"),
    "plant_zones": os.path.join(A, "p19_x72_2000x1125.png"),
    "cable_systems": os.path.join(A, "p20_x76_2000x1333.png"),
    "modular_block": os.path.join(A, "p26_x98_2000x1124.png"),
    "yard": os.path.join(A, "p28_x104_1000x1080.png"),
    "hv_cable": os.path.join(A, "p23_x85_2000x1333.png"),
    "closing": os.path.join(A, "p35_x124_2000x1125.png"),
}
WATERMARKED = ["cover", "plant_zones", "cable_systems", "modular_block", "yard", "hv_cable"]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ----------------------------------------------------------------- helpers
class Page:
    def __init__(self, n, bg):
        self.n, self.bg, self.el = n, bg, []

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.6, name="", alpha=None):
        self.el.append(dict(kind="rect", x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, name=name, alpha=alpha))

    def text(self, x, y, w, h, s, size, font="r", color=INK, align="left", valign="top", lead=1.2, name="",
             track=0):
        self.el.append(dict(kind="text", x=x, y=y, w=w, h=h, text=s, size=size, font=font, color=color,
                            align=align, valign=valign, lead=lead, name=name, track=track))

    def kicker(self, x, y, w, s, color=COPPER, size=8, name=""):
        self.text(x, y, w, 0.2, s.upper(), size, "hs", color, track=2.2, name=name or "Kicker")

    def head(self, x, y, w, h, s, size=30, color=INK, name="Headline", lead=0.98):
        self.text(x, y, w, h, s.upper(), size, "hx", color, lead=lead, name=name)

    def image(self, x, y, w, h, path, name="", crop=None, clip=None):
        self.el.append(dict(kind="image", x=x, y=y, w=w, h=h, path=path, name=name, crop=crop, clip=clip))

    def marker(self, x, y, n, r=0.11, fill=COPPER, color=WHITE, name=""):
        self.el.append(dict(kind="marker", x=x, y=y, r=r, n=str(n), fill=fill, color=color, name=name))

    def line(self, x1, y1, x2, y2, color=RULE, lw=0.6, name=""):
        self.el.append(dict(kind="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw, name=name))

    def footer(self, dark=False):
        c = MUTED if not dark else "#8E939B"
        self.text(M, PH - 0.42, 5.5, 0.16, "SOUTHWIRE POWER GENERATION SOLUTIONS  ·  NICA", 6.5, "hs", c, track=1.0,
                  name="Footer_Left")
        self.text(PW - M - 0.6, PH - 0.42, 0.6, 0.16, f"{self.n:02d}", 7.5, "hb", c, align="right", name="Footer_Page")
        self.text(M, PH - 0.27, PW - 2 * M, 0.14, "© 2026 Southwire Company, LLC. All rights reserved. "
                  "Illustrations are conceptual and not engineering data.", 5.5, "r", c, name="Footer_Legal")


def card(p, x, y, w, h, dark=False, top=True):
    p.rect(x, y, w, h, fill=DARK2 if dark else CARD, name="Card")
    if top:
        p.rect(x, y, w, 0.045, fill=COPPER, name="Card_Rule")


def cable_icon(p, x, y, jacket, insul=WHITE, core="#C27A4A", w=1.25, h=0.19, name="CableIcon"):
    """Flat cable cutaway icon in the deck's style."""
    p.rect(x, y, w * 0.56, h, fill=jacket, name=name + "_Jacket")
    p.rect(x + w * 0.56, y + h * 0.1, w * 0.12, h * 0.8, fill="#9BA3AA", name=name + "_Screen")
    p.rect(x + w * 0.68, y + h * 0.15, w * 0.14, h * 0.7, fill=insul, name=name + "_Insul")
    p.rect(x + w * 0.82, y + h * 0.3, w * 0.18, h * 0.4, fill=core, name=name + "_Core")


# ----------------------------------------------------------------- pages
def page_cover():
    p = Page(1, DARK)
    # diagonal hero on the right (clipped polygon in PDF, rectangle in PPTX)
    p.image(3.9, -BLEED, PW - 3.9 + BLEED, PH + 2 * BLEED, IMG["cover"], name="Hero",
            clip=[(4.75, -BLEED), (PW + BLEED, -BLEED), (PW + BLEED, PH + BLEED), (3.9, PH + BLEED)])
    p.image(M, 0.62, 2.55, 2.55 * 324 / 1305, IMG["logo"], name="Logo")
    p.kicker(M, 2.05, 3.2, "NICA  ·  for electrical contractors", COPPER_LT, size=8.5)
    p.rect(M, 2.36, 0.5, 0.03, fill=COPPER, name="Kicker_Rule")
    p.head(M, 2.95, 3.4, 2.6, "Power\nGeneration\nSolutions", 44, "#F4F2EE", lead=0.92)
    p.text(M, 4.95, 3.3, 0.9, "CABLE, KITS AND ASSEMBLIES FOR THE CREWS THAT BUILD AND CONNECT GENERATION", 12,
           "hb", COPPER_LT, lead=1.1, name="Subhead")
    p.text(M, 5.95, 3.2, 1.3, "One cable scope from the switchyard to the control panel: medium-voltage feeders, "
           "tray and control cable, grounding, and prepared kits that arrive ready to land.", 9.5, "r", "#C9CBCF",
           lead=1.3, name="Intro")
    p.text(M, 9.55, 3.0, 0.2, "ACCELERATING TIME TO POWER™", 11, "hb", "#F4F2EE", name="Tagline")
    p.text(M, 9.85, 3.0, 0.5, "Stephan Hardt · Director, Power Generation Solutions\nstephan.hardt@southwire.com  ·  "
           "powergen@southwire.com", 7.5, "r", "#9A9DA3", lead=1.35, name="Contact")
    p.text(M, PH - 0.27, 3.0, 0.14, "© 2026 Southwire Company, LLC. All rights reserved.", 5.5, "r", "#6E7178",
           name="Footer_Legal")
    return p


def page_plant():
    p = Page(2, DARK)
    p.kicker(M, 0.62, 4, "The plant is the model", COPPER_LT)
    p.head(M, 0.86, PW - 2 * M, 0.9, "16 zones. 75 equipment nodes.\nOne connected cable scope.", 27, "#F4F2EE")
    PWd = PW - 2 * M - 0.9
    p.image(M + 0.45, 1.9, PWd, PWd * 1125 / 2000, IMG["plant_zones"], name="Plant_Render")
    zones = ["Switchyard, GSU & grid tie", "BESS yard", "Reel staging & prefab", "Admin & control room", "E-house",
             "HRSG trains & stacks", "Turbine hall", "GT air inlets", "MCC, VFD & UPS room", "Modular power yard",
             "Air-cooled condenser", "Chillers & cooling towers", "Water treatment", "Carbon capture (CCS)",
             "Gas metering", "Cable corridor & MV"]
    y0 = 1.9 + PWd * 1125 / 2000 + 0.18
    colw = (PW - 2 * M) / 3
    for i, z in enumerate(zones):
        cx = M + (i % 3) * colw
        cy = y0 + (i // 3) * 0.26
        p.text(cx, cy, 0.3, 0.2, f"{i+1:02d}", 8.5, "hb", COPPER_LT, name=f"Zone_{i+1}_N")
        p.text(cx + 0.32, cy + 0.01, colw - 0.4, 0.3, z, 7.8, "r", "#D5D7DB", name=f"Zone_{i+1}")
    yb = y0 + 6 * 0.26 + 0.08
    p.line(M, yb, PW - M, yb, RULE_D)
    p.text(M, yb + 0.1, PW - 2 * M, 0.5,
           "Every zone above is wired. The contractor's share of that scope runs from the switchyard to the last "
           "terminal block: feeders, tray cable, control and instrumentation, grounding, and the prepared kits and "
           "assemblies that shorten the work inside each enclosure.", 9, "r", "#C9CBCF", lead=1.3, name="Plant_Copy")
    p.text(M, yb + 0.62, PW - 2 * M, 0.2, "PLANT  ·  EQUIPMENT  ·  CABLE  ·  DELIVERY", 9, "hb", COPPER_LT, track=1.2,
           name="Plant_Strap")
    yw = yb + 0.95
    p.kicker(M, yw, 4, "Why now", COPPER_LT)
    stats = [("378 GW", "US gas power in development, mid-2026"), ("52 GW", "under construction, the largest gas build in the world"),
             ("Up to 7 yrs", "quoted lead time for some large gas turbines"), ("< 1%", "of plant capex is wire and cable, on the critical path to first power")]
    sw = (PW - 2 * M - 3 * 0.15) / 4
    for i, (k, v) in enumerate(stats):
        x = M + i * (sw + 0.15)
        p.rect(x, yw + 0.28, sw, 1.1, fill=DARK2, name=f"Stat_{i}")
        p.rect(x, yw + 0.28, sw, 0.04, fill=COPPER if i else "#7A8088", name=f"Stat_{i}_Rule")
        p.text(x + 0.14, yw + 0.4, sw - 0.28, 0.4, k, 20, "hx", COPPER_LT if i else "#F4F2EE", name=f"Stat_{i}_K")
        p.text(x + 0.14, yw + 0.8, sw - 0.28, 0.6, v, 7, "r", "#C9CBCF", lead=1.25, name=f"Stat_{i}_V")
    p.text(M, yw + 1.44, PW - 2 * M, 0.3, "Sources: Grid Strategies 2025; Global Energy Monitor, Aug 2026; S&P Global Commodity Insights, "
           "May 2025; Southwire planning assumption for cable share. Early-stage proposals will not all be built.", 5.8, "r", "#8E939B",
           lead=1.3, name="Stat_Sources")
    p.footer(dark=True)
    return p


def page_systems():
    p = Page(3, CREAM)
    p.kicker(M, 0.62, 4, "Seven cable systems in one plant")
    p.head(M, 0.86, PW - 2 * M, 0.5, "Every megawatt travels through a cable", 27)
    iw = 4.2
    p.image(M, 1.5, iw, iw * 1333 / 2000, IMG["cable_systems"], name="Systems_Render")
    sysl = [("Control & instrumentation", "#2E7BD1"), ("LV power & VFD cable", "#C9A227"),
            ("Medium-voltage feeders", "#D9741F"), ("Fire-rated & specialty", "#7B4FC8"),
            ("High-voltage XLPE cable", "#D33A3A"), ("Fibre optic", "#2E9E6B"), ("Overhead conductor & OPGW", "#D33A3A")]
    lx = M + iw + 0.25
    for i, (s, c) in enumerate(sysl):
        y = 1.52 + i * 0.39
        p.marker(lx + 0.11, y + 0.13, i + 1, 0.11, fill=c)
        p.text(lx + 0.34, y + 0.03, PW - M - lx - 0.34, 0.25, s, 10, "sb", INK, name=f"System_{i+1}")
        p.line(lx, y + 0.35, PW - M, y + 0.35, RULE)
    p.text(M, 1.5 + iw * 1333 / 2000 + 0.06, iw, 0.16, "ILLUSTRATIVE 1×1 COMBINED CYCLE BLOCK · CABLE DIAMETERS EXAGGERATED",
           6, "hs", MUTED, track=1.2, name="Systems_Caption")
    # challenge table
    yt = 4.65
    p.kicker(M, yt, 4, "What the site asks of the cable")
    colw = (PW - 2 * M - 0.3) / 2
    for ci, (title, rows) in enumerate((
        ("Combined cycle plants", [("Heat", "Routes beside turbines, HRSGs and steam lines"),
                                   ("Daily cycling", "Frequent starts stress terminations and joints"),
                                   ("Fire and smoke", "Flame-retardant, low-smoke cable in halls and control rooms"),
                                   ("Electrical noise", "Drives and switchgear next to DCS and protection")]),
        ("Modular gas power", [("Compact skids", "Flexible cable with tight bend radii"),
                               ("Vibration", "Fine stranding and secure glands for engines"),
                               ("Harsh sites", "Oil, fuel, sunlight and wide temperature ranges"),
                               ("Speed to power", "Pre-terminated, tested harnesses cut site hours")]))):
        x = M + ci * (colw + 0.3)
        p.rect(x, yt + 0.3, colw, 0.42, fill=DARK, name=f"Chal_{ci}_Head")
        p.rect(x, yt + 0.72, colw, 0.03, fill=COPPER, name=f"Chal_{ci}_Rule")
        p.text(x + 0.15, yt + 0.37, colw - 0.3, 0.3, title.upper(), 13, "hb", "#F4F2EE", name=f"Chal_{ci}_Title")
        for ri, (k, v) in enumerate(rows):
            y = yt + 0.88 + ri * 0.47
            p.text(x, y, 1.25, 0.3, k.upper(), 8.5, "hb", INK, name=f"Chal_{ci}_{ri}_K")
            p.text(x + 1.25, y + 0.01, colw - 1.25, 0.45, v, 7.8, "r", MUTED, lead=1.25, name=f"Chal_{ci}_{ri}_V")
            p.line(x, y + 0.4, x + colw, y + 0.4, RULE)
    # value strip
    yv = yt + 0.88 + 4 * 0.47 + 0.12
    p.rect(M, yv, PW - 2 * M, 0.85, fill=DARK, name="Value_Box")
    p.rect(M, yv, 0.05, 0.85, fill=COPPER, name="Value_Bar")
    p.text(M + 0.22, yv + 0.12, PW - 2 * M - 0.4, 0.25, "WHY IT MATTERS ON SITE", 8, "hs", COPPER_LT, track=2,
           name="Value_K")
    p.text(M + 0.22, yv + 0.33, PW - 2 * M - 0.4, 0.5,
           "One supplier across voltage classes means one spec review, one reel plan and one point of contact when "
           "the schedule moves. Cable inside packaged equipment is bought months before the field-cable RFQ, so the "
           "earlier the conversation, the more of the work can arrive prepared.", 8.5, "r", "#D5D7DB", lead=1.3,
           name="Value_Copy")
    yd = yv + 0.85 + 0.22
    p.kicker(M, yd, 4, "Cable in detail")
    dets = [("p23_x85_2000x1333.png", "HV single-core XLPE. Triple-extruded insulation, copper wire screen, water-blocking under a PE jacket."),
            ("p23_x87_2000x1333.png", "MV three-core for large auxiliary motors."),
            ("p23_x88_2000x1333.png", "Circuit integrity for fire and shutdown circuits.")]
    dw = (PW - 2 * M - 2 * 0.15) / 3
    for i, (fn, cap) in enumerate(dets):
        x = M + i * (dw + 0.15)
        p.image(x, yd + 0.26, dw, dw * 0.5, os.path.join(A, fn), name=f"Detail_{i}", crop=(0, 330, 2000, 1000))
        p.text(x, yd + 0.26 + dw * 0.5 + 0.05, dw, 0.4, cap, 6.8, "r", MUTED, lead=1.25, name=f"Detail_{i}_Cap")
    p.footer()
    return p


def page_families():
    p = Page(4, CREAM)
    p.text(M, 0.62, PW - 2 * M, 0.5, "", 1)
    p.el.append(dict(kind="text", x=M, y=0.62, w=PW - 2 * M, h=0.5, text="ONE SUPPLIER. EVERY CIRCUIT.", size=30,
                     font="hx", color=INK, align="left", valign="top", lead=1.0, name="Headline", track=0,
                     rich=[("ONE SUPPLIER. ", COPPER), ("EVERY CIRCUIT.", INK)]))
    fams = [("HV", "69–345 kV", "XLPE from step-up transformer to switchyard", "AEIC CS9 · ICEA S-108-720", "#1B1C20"),
            ("MV", "5–35 kV", "Feeders to pumps, fans, compressors and GT start-up", "UL 1072 · ICEA S-93-639", "#C8281E"),
            ("LV", "Power & VFD", "MCC feeders, VFD motor leads, lighting", "UL 1277 TC-ER · UL 44 XHHW-2", "#1B1C20"),
            ("C&I", "Control", "Shielded pairs, triads and thermocouple extension", "UL 2250 ITC · UL 13 PLTC", "#2E7BD1"),
            ("FR", "Fire-rated", "2-hour circuit integrity for fire pumps, alarms, ESD", "UL 2196 · IEC 60331", "#E8762A"),
            ("FO", "Fibre", "Relay links, plant network and OPGW", "ICEA S-87-640 · IEEE 1138", "#1B1C20"),
            ("MX", "Modular", "Flexible, oil-resistant cable and harnesses for skids", "Class K stranding · UL 1277", "#3A3E45"),
            ("GR", "Grounding", "Bare copper grid and equipment bonding", "IEEE 80 · IEEE 665", "#6B7580")]
    cw, ch, gap = (PW - 2 * M - 3 * 0.18) / 4, 2.25, 0.2
    for i, (tag, nm, desc, std, col) in enumerate(fams):
        x = M + (i % 4) * (cw + gap)
        y = 1.35 + (i // 4) * (ch + gap)
        card(p, x, y, cw, ch)
        cable_icon(p, x + 0.14, y + 0.2, col, name=f"Fam_{tag}_Icon")
        p.el.append(dict(kind="text", x=x + 0.14, y=y + 0.52, w=cw - 0.28, h=0.3, text=f"{tag} {nm.upper()}", size=14,
                         font="hb", color=INK, align="left", valign="top", lead=1.0, name=f"Fam_{tag}_Title", track=0,
                         rich=[(tag + " ", COPPER), (nm.upper(), INK)]))
        p.text(x + 0.14, y + 0.9, cw - 0.28, 0.75, desc, 8.5, "r", MUTED, lead=1.3, name=f"Fam_{tag}_Desc")
        p.text(x + 0.14, y + ch - 0.42, cw - 0.28, 0.35, std, 6.8, "sb", INK, lead=1.2, name=f"Fam_{tag}_Std")
    # standards table
    yt = 1.35 + 2 * ch + gap + 0.4
    p.kicker(M, yt, 5, "Built to North American specs")
    rows = [("HV 69–345 kV", "AEIC CS9 · ICEA S-108-720", "IEC 60840 · IEC 62067"),
            ("MV 5–35 kV", "UL 1072 · ICEA S-93-639", "IEC 60502-2"),
            ("LV power & VFD", "UL 1277 TC-ER · UL 44 XHHW-2", "IEC 60502-1"),
            ("Control & instrumentation", "UL 2250 ITC · UL 13 PLTC", "EN 50288-7"),
            ("Fire-rated", "UL 2196 circuit integrity", "IEC 60331"),
            ("Flame propagation", "IEEE 1202 · UL 1685", "IEC 60332-3"),
            ("Fibre & OPGW", "ICEA S-87-640 · IEEE 1138", "ITU-T G.652.D"),
            ("Grounding", "IEEE 80 · IEEE 665", "IEC 61936-1")]
    cols = [(M, 2.3), (M + 2.35, 3.0), (M + 5.45, PW - M - (M + 5.45))]
    yh = yt + 0.28
    p.rect(M, yh, PW - 2 * M, 0.24, fill=DARK, name="Std_Head")
    for (x, w), t in zip(cols, ("Cable family", "North American standards", "International")):
        p.text(x + 0.08, yh + 0.045, w, 0.2, t, 8, "sb", "#F4F2EE", name="Std_H_" + t[:5])
    for ri, r in enumerate(rows):
        y = yh + 0.24 + ri * 0.27
        if ri % 2 == 0:
            p.rect(M, y, PW - 2 * M, 0.27, fill=SAND, name=f"Std_R{ri}_Bg")
        for (x, w), t in zip(cols, r):
            p.text(x + 0.08, y + 0.065, w, 0.2, t, 8.5, "r", INK, name=f"Std_R{ri}_{x:.1f}")
    p.text(M, yh + 0.24 + 8 * 0.27 + 0.08, PW - 2 * M, 0.16, "CONFIRM LISTINGS PER PRODUCT DATASHEET", 6.5, "hs",
           MUTED, track=1.4, name="Std_Note")
    p.footer()
    return p


def page_channel():
    p = Page(5, CREAM)
    p.kicker(M, 0.62, 4, "From reel to termination")
    p.head(M, 0.86, PW - 2 * M, 0.9, "Built for the way\ncontractors build", 30)
    iw = 3.3
    p.image(M, 1.95, iw, iw * 1080 / 1000, IMG["yard"], name="Yard_Render")
    p.rect(M, 1.95 + iw * 1080 / 1000 + 0.45, iw, 0.03, fill=COPPER, name="Yard_Rule")
    p.text(M, 1.95 + iw * 1080 / 1000 + 0.58, iw, 1.6, "Cable inside packaged equipment is bought months before the EPC issues its field-cable RFQ. The earlier the conversation with the package builder and the contractor, the more of the work can arrive prepared.", 9, "r", INK, lead=1.35, name="Yard_Copy")
    p.text(M, 1.95 + iw * 1080 / 1000 + 0.06, iw, 0.3, "REEL STAGING AND PREFAB AREA · RENDERED ILLUSTRATION", 6,
           "hs", MUTED, track=1.2, name="Yard_Caption")
    svc = [("Spec support", "Cable sizing, derating and spec reviews with the engineer of record before the cable schedule is frozen"),
           ("Cut-to-length", "Reel lengths planned against the cable schedule, so pulls start without re-cutting"),
           ("Harness kits", "Pre-terminated, labelled kits for skids, panels and enclosures"),
           ("Stocking program", "Core control and power constructions held locally through the channel"),
           ("Project logistics", "Reel tracking and deliveries sequenced to the installation plan"),
           ("Field support", "Pulling calculations, termination guidance and commissioning tests")]
    lx = M + iw + 0.3
    lw = PW - M - lx
    for i, (k, v) in enumerate(svc):
        y = 1.95 + i * 0.9
        p.rect(lx, y, lw, 0.03, fill=COPPER, name=f"Svc_{i}_Rule")
        p.text(lx, y + 0.1, 0.45, 0.3, f"{i+1:02d}", 15, "hb", COPPER, name=f"Svc_{i}_N")
        p.text(lx + 0.45, y + 0.12, lw - 0.45, 0.25, k.upper(), 12, "hb", INK, name=f"Svc_{i}_K")
        p.text(lx + 0.45, y + 0.38, lw - 0.45, 0.48, v, 8.5, "r", MUTED, lead=1.3, name=f"Svc_{i}_V")
    # modular strip
    ym = 1.95 + 6 * 0.9 + 0.2
    p.rect(M, ym, PW - 2 * M, 0.42, fill=DARK, name="Mod_Head")
    p.rect(M, ym + 0.42, PW - 2 * M, 0.03, fill=COPPER, name="Mod_Rule")
    p.text(M + 0.15, ym + 0.08, PW - 2 * M, 0.3, "POWER THAT SHIPS IN A CONTAINER", 13, "hb", "#F4F2EE", name="Mod_Title")
    feats = [("Pre-terminated", "Cut, terminated, tested and labelled in the factory"),
             ("Flexible", "Fine stranding and tight bend radii for dense skids"),
             ("Vibration-proof", "Built for engines and aeroderivative packages"),
             ("Site-rated", "Oil-, fuel- and sunlight-resistant jackets")]
    fw = (PW - 2 * M) / 4
    for i, (k, v) in enumerate(feats):
        x = M + i * fw
        p.text(x + 0.05, ym + 0.58, fw - 0.15, 0.2, k.upper(), 9.5, "hb", INK, name=f"Feat_{i}_K")
        p.text(x + 0.05, ym + 0.78, fw - 0.15, 0.5, v, 7.8, "r", MUTED, lead=1.25, name=f"Feat_{i}_V")
    steps = ["Design", "Cut & terminate", "Test & label", "Install on site"]
    ys = ym + 1.3
    sw = (PW - 2 * M - 3 * 0.08) / 4
    for i, s in enumerate(steps):
        x = M + i * (sw + 0.08)
        last = i == 3
        p.rect(x, ys, sw, 0.42, fill=COPPER if last else DARK2, name=f"Step_{i}")
        p.text(x + 0.12, ys + 0.11, sw - 0.2, 0.25, s.upper(), 10, "hb", "#F4F2EE", name=f"Step_{i}_T")
    p.footer()
    return p


def _lane(p, y, key, title, bullets, first, side):
    """One application lane: render with numbered markers + text column."""
    page = next(pg for pg in PAGES if pg["key"] == key)
    meta = json.load(open(os.path.join(RCLEAN, page["view"] + ".json")))
    sx, sy = meta["size"]
    iw = 3.45
    ih = iw * sy / sx
    ix = M if side == "L" else PW - M - iw
    tx = M + iw + 0.28 if side == "L" else M
    tw = PW - 2 * M - iw - 0.28
    p.image(ix, y, iw, ih, os.path.join(RCLEAN, page["view"] + ".png"), name=f"Lane_{key}_Render")
    for c in meta["callouts"]:
        ax = ix + c["anchor_px"][0] / sx * iw
        ay = y + c["anchor_px"][1] / sy * ih
        p.el.append(dict(kind="dot", x=ax, y=ay, r=0.028, name=f"Lane_{key}_Dot{c['n']}"))
        # marker offset toward the nearer free side
        lab = page.get("labels", {}).get(c["n"], c["label_norm"])
        mx = ix + lab[0] * iw
        my = y + lab[1] * ih
        mx = min(max(mx, ix + 0.14), ix + iw - 0.14)
        my = min(max(my, y + 0.14), y + ih - 0.14)
        p.line(mx, my, ax, ay, INK, 0.8, name=f"Lane_{key}_Leader{c['n']}")
        p.marker(mx, my, c["n"], 0.105, fill=COPPER, name=f"Lane_{key}_M{c['n']}")
    p.rect(tx, y, tw, 0.03, fill=COPPER, name=f"Lane_{key}_Rule")
    p.text(tx, y + 0.1, tw, 0.3, title.upper(), 13.5, "hb", INK, name=f"Lane_{key}_Title")
    for i, b in enumerate(bullets):
        by = y + 0.46 + i * 0.5
        p.marker(tx + 0.1, by + 0.09, i + 1, 0.095, fill=INK, name=f"Lane_{key}_B{i+1}_M")
        p.text(tx + 0.3, by, tw - 0.3, 0.48, b, 8, "r", INK, lead=1.25, name=f"Lane_{key}_B{i+1}")
    fy = y + ih - 0.42
    p.rect(tx, fy, tw, 0.42, fill=SAND, name=f"Lane_{key}_FirstBox")
    p.rect(tx, fy, 0.04, 0.42, fill=COPPER, name=f"Lane_{key}_FirstBar")
    p.text(tx + 0.14, fy + 0.05, tw - 0.2, 0.12, "FIRST STEP", 6, "hs", COPPER, track=1.6, name=f"Lane_{key}_FirstK")
    p.text(tx + 0.14, fy + 0.17, tw - 0.2, 0.25, first, 7.5, "sb", INK, lead=1.2, name=f"Lane_{key}_First")
    return ih


LANES = [
    ("IEM", "Switchgear & control panels",
     ["Control conductors cut, stripped, ferruled and marked from the wiring schedule, identified at both ends.",
      "Kits packed by cubicle or build step, so the bench holds what that section needs and nothing else.",
      "Inspection points and test records agreed up front and tied to each kit label."],
     "Bring one representative wiring schedule and pick a pilot section."),
    ("CAT", "Generator packages",
     ["Output leads cut, terminated and identified to the terminal-box arrangement.",
      "Engine, regulator and remote-control wiring grouped by option and routed to a defined harness drawing.",
      "A defined hand-off at the cable exit: what ships with the set, what the installer connects."],
     "Review the terminal-box and control-wiring scope of one generator platform."),
    ("SIEMENS", "E-houses & modular skids",
     ["Cables routed and terminated within each shipping section before it leaves the factory.",
      "Split-crossing feeders and control cables prepared, identified and staged for the reconnection sequence.",
      "External feeders, cable transits and grounding pads defined as a clear site interface."],
     "Walk one skid's interconnection list and installation sequence."),
    ("ASCO", "Transfer & distribution equipment",
     ["Normal-source, generator-source and load terminations documented so installer-supplied cable can be prepared consistently.",
      "Generator feeders and a separately routed engine-start cable evaluated as one package.",
      "Factory-supplied versus installer-supplied scope confirmed before the cable is cut."],
     "Define the scope split for one transfer-switch configuration."),
    ("MOSEBACH", "Temporary power & testing",
     ["Portable single-conductor sets built to length, with connectors and matching identification at both ends.",
      "Separate generator-input and load-bank ports; the load bank stays a configurable test load.",
      "Coiled sets, labels and inspection records kept together for repeated deployments."],
     "Review duty, connectors and lead lengths for one test setup."),
    ("WESCO", "Staged supply & assembly",
     ["Each module or section tied to its own cable and kit list from the drawings.",
      "Reels and kits identified to the program, section and installation step.",
      "Deliveries planned against the build sequence rather than one bulk shipment."],
     "Pick one program and define who prepares, who delivers and who installs."),
]


def page_apps(n, lanes, first_page):
    p = Page(n, CREAM)
    if first_page:
        p.kicker(M, 0.62, 5, "Applications to evaluate")
        p.head(M, 0.86, PW - 2 * M, 0.5, "Where prepared cable fits the job", 27)
        p.text(M, 1.4, PW - 2 * M, 0.4,
               "Six places on a generation project where cable, kits or assemblies can arrive prepared instead of "
               "being cut and dressed on site. Each is an application to evaluate against your drawings, not a catalog item.",
               8.5, "r", MUTED, lead=1.3, name="Apps_Intro")
        y = 2.0
    else:
        p.kicker(M, 0.62, 5, "Applications to evaluate  ·  continued")
        y = 0.95
    for i, (key, title, bullets, first) in enumerate(lanes):
        ih = _lane(p, y, key, title, bullets, first, "L" if i % 2 == 0 else "R")
        y += ih + 0.28
    if not first_page:
        p.rect(M, y - 0.05, PW - 2 * M, 0.5, fill=DARK, name="Legend_Box")
        p.rect(M, y - 0.05, 0.05, 0.5, fill=COPPER, name="Legend_Bar")
        p.text(M + 0.2, y + 0.02, PW - 2 * M - 0.3, 0.4,
               "Blue conductors, amber highlights and the kits shown are presentation devices, not conductor "
               "identification or qualified products. Ratings, sizes, clearances and terminations remain subject to "
               "application engineering.", 7.5, "r", "#D5D7DB", lead=1.3, name="Legend_Text")
    p.footer()
    return p


def page_back():
    p = Page(8, DARK)
    p.image(-BLEED, -BLEED, PW + 2 * BLEED, (PW + 2 * BLEED) * 1125 / 2000, IMG["closing"], name="Closing_Art",
            crop=(0, 0, 2000, 1125))
    yt = (PW + 2 * BLEED) * 1125 / 2000 - BLEED + 0.15
    p.rect(M, yt, PW - 2 * M, 0.03, fill=COPPER, name="Back_Rule")
    p.kicker(M, yt + 0.2, 4, "Value proposition", COPPER_LT)
    p.head(M, yt + 0.45, 4.2, 0.9, "Accelerating\ntime to power", 30, "#F4F2EE")
    vals = [("Less installation time", "Prefab and standard designs across projects"),
            ("Material readiness", "Reel IDs, kits and sequenced delivery"),
            ("Supply certainty", "Forecasts tied to a confirmed supply plan"),
            ("Execution speed", "Earlier decisions and repeat designs")]
    for i, (k, v) in enumerate(vals):
        y = yt + 1.55 + i * 0.62
        p.text(M, y, 4.0, 0.22, k.upper(), 11, "hb", "#F4F2EE", name=f"Val_{i}_K")
        p.text(M, y + 0.22, 4.0, 0.25, v, 8, "r", "#C9CBCF", name=f"Val_{i}_V")
        p.line(M, y + 0.5, M + 3.9, y + 0.5, RULE_D)
    # next step + contact
    cx = M + 4.35
    cw = PW - M - cx
    p.rect(cx, yt + 0.45, cw, 2.05, fill=DARK2, name="Next_Box")
    p.rect(cx, yt + 0.45, cw, 0.04, fill=COPPER, name="Next_Rule")
    p.text(cx + 0.18, yt + 0.6, cw - 0.36, 0.2, "AT THE SHOW, OR AFTER", 8, "hs", COPPER_LT, track=2, name="Next_K")
    p.text(cx + 0.18, yt + 0.85, cw - 0.36, 1.6,
           "Bring one drawing: a wiring schedule, a cable schedule or a skid interconnection list. We will walk it "
           "together, mark what could arrive prepared, and agree a first pilot with named owners on both sides.",
           9, "r", "#E4E5E8", lead=1.35, name="Next_Copy")
    p.rect(cx, yt + 2.7, cw, 1.55, fill=CARD, name="Contact_Box")
    p.text(cx + 0.18, yt + 2.82, cw - 1.55, 0.22, "Stephan Hardt", 12, "hb", INK, name="Contact_Name")
    p.text(cx + 0.18, yt + 3.06, cw - 1.55, 0.45, "Director, Power Generation Solutions\nSouthwire Company, LLC", 7.5, "r",
           MUTED, lead=1.3, name="Contact_Title")
    p.text(cx + 0.18, yt + 3.55, cw - 1.55, 0.5, "stephan.hardt@southwire.com\npowergen@southwire.com", 7.5, "sb", COPPER,
           lead=1.35, name="Contact_Email")
    p.rect(cx + cw - 1.3, yt + 2.85, 1.12, 1.12, fill=None, line="#9AA3AA", name="QR_Placeholder")
    p.text(cx + cw - 1.3, yt + 2.85, 1.12, 1.12, "QR CODE\nplaceholder\n(approved URL)", 6, "r", MUTED, align="center",
           valign="middle", lead=1.3, name="QR_Text")
    p.text(M, PH - 0.42, PW - 2 * M, 0.16, "WE DELIVER POWER RESPONSIBLY", 7, "hs", "#8E939B", track=1.6, name="Footer_Left")
    p.text(M, PH - 0.27, PW - 2 * M, 0.14, "© 2026 Southwire Company, LLC. All rights reserved. Illustrations are "
           "conceptual and not engineering data. Confirm listings per product datasheet. Applications shown are concepts "
           "for evaluation, not qualified products.", 5.5, "r", "#8E939B", name="Footer_Legal")
    return p


def build_pages():
    return [page_cover(), page_plant(), page_systems(), page_families(), page_channel(),
            page_apps(6, LANES[:3], True), page_apps(7, LANES[3:], False), page_back()]


# ----------------------------------------------------------------- PDF
def to_pdf(pages, path, marks):
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, Color
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    for k, (nm, fn) in FONTS.items():
        if nm not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(nm, os.path.join(F, fn)))
    off = BLEED + SLUG if marks else 0.0
    pw, ph = PW + 2 * off, PH + 2 * off
    c = canvas.Canvas(path, pagesize=(pw * 72, ph * 72))
    c.setTitle("Southwire Power Generation Solutions - NICA booklet")
    I = lambda v: v * 72
    X = lambda x: (x + off) * 72
    Y = lambda y: (PH - y + off) * 72
    overflow = []
    for p in pages:
        b = BLEED if marks else 0
        c.setFillColor(HexColor(p.bg))
        c.rect(X(-b), Y(PH + b), I(PW + 2 * b), I(PH + 2 * b), stroke=0, fill=1)
        # clip everything to the bleed box
        c.saveState()
        cp = c.beginPath()
        cp.rect(X(-b), Y(PH + b), I(PW + 2 * b), I(PH + 2 * b))
        c.clipPath(cp, stroke=0)
        for e in p.el:
            k = e["kind"]
            if k == "rect":
                if e.get("fill"):
                    col = HexColor(e["fill"])
                    if e.get("alpha"):
                        col = Color(col.red, col.green, col.blue, alpha=e["alpha"])
                    c.setFillColor(col)
                if e.get("line"):
                    c.setStrokeColor(HexColor(e["line"]))
                    c.setLineWidth(e.get("lw", 0.6))
                c.rect(X(e["x"]), Y(e["y"] + e["h"]), I(e["w"]), I(e["h"]), stroke=1 if e.get("line") else 0,
                       fill=1 if e.get("fill") else 0)
            elif k == "line":
                c.setStrokeColor(HexColor(e["color"]))
                c.setLineWidth(e["lw"])
                c.line(X(e["x1"]), Y(e["y1"]), X(e["x2"]), Y(e["y2"]))
            elif k == "image":
                src = e["path"]
                if e.get("crop"):
                    from PIL import Image as _Im
                    src = os.path.join(OUT, "_tmp", f"crop_{p.n}_{e['name']}.png")
                    os.makedirs(os.path.dirname(src), exist_ok=True)
                    _Im.open(e["path"]).crop(e["crop"]).save(src)
                c.saveState()
                if e.get("clip"):
                    pth = c.beginPath()
                    pts = e["clip"]
                    pth.moveTo(X(pts[0][0]), Y(pts[0][1]))
                    for q in pts[1:]:
                        pth.lineTo(X(q[0]), Y(q[1]))
                    pth.close()
                    c.clipPath(pth, stroke=0)
                c.drawImage(src, X(e["x"]), Y(e["y"] + e["h"]), I(e["w"]), I(e["h"]), mask="auto")
                c.restoreState()
            elif k == "dot":
                c.setFillColor(HexColor(COPPER))
                c.setStrokeColor(HexColor(WHITE))
                c.setLineWidth(0.8)
                c.circle(X(e["x"]), Y(e["y"]), I(e["r"]), stroke=1, fill=1)
            elif k == "marker":
                c.setFillColor(HexColor(e["fill"]))
                c.setStrokeColor(HexColor(WHITE))
                c.setLineWidth(1.0)
                c.circle(X(e["x"]), Y(e["y"]), I(e["r"]), stroke=1, fill=1)
                c.setFillColor(HexColor(e["color"]))
                fs = e["r"] * 72 * 1.05
                c.setFont("BarlowC-B", fs)
                c.drawCentredString(X(e["x"]), Y(e["y"]) - fs * 0.36, e["n"])
            elif k == "text":
                fn = FONTS[e["font"]][0]
                if e.get("track"):
                    c.saveState()
                    c.setFillColor(HexColor(e["color"]))
                    c.setFont(fn, e["size"])
                    tx = c.beginText()
                    tx.setCharSpace(e["track"] * 0.5)
                    xx = X(e["x"])
                    if e["align"] == "right":
                        wdt = pdfmetrics.stringWidth(e["text"], fn, e["size"]) + e["track"] * 0.5 * len(e["text"])
                        xx = X(e["x"] + e["w"]) - wdt
                    tx.setTextOrigin(xx, Y(e["y"]) - e["size"])
                    tx.textLine(e["text"])
                    tx.setCharSpace(0)
                    c.drawText(tx)
                    c.restoreState()
                    continue
                al = {"left": TA_LEFT, "center": TA_CENTER, "right": TA_RIGHT}[e["align"]]
                st = ParagraphStyle("s", fontName=fn, fontSize=e["size"], leading=e["size"] * e["lead"],
                                    textColor=HexColor(e["color"]), alignment=al)
                if e.get("rich"):
                    txt = "".join(f'<font color="{col}">{t}</font>' for t, col in e["rich"])
                else:
                    txt = e["text"].replace("&", "&amp;").replace("<", "&lt;").replace("\n", "<br/>")
                para = Paragraph(txt, st)
                w, h = para.wrap(I(e["w"]), I(e["h"]) * 6)
                if h > I(e["h"]) + 2:
                    overflow.append((p.n, e["name"], round(h / 72, 2), e["h"]))
                yy = e["y"]
                if e["valign"] == "middle":
                    yy = e["y"] + (e["h"] - h / 72) / 2
                para.drawOn(c, X(e["x"]), Y(yy) - h)
        c.restoreState()
        if marks:
            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(0.25)
            L = I(0.18)
            g = I(BLEED + 0.03)
            for (x, y) in ((X(0), Y(0)), (X(PW), Y(0)), (X(0), Y(PH)), (X(PW), Y(PH))):
                sx = -1 if x == X(0) else 1
                sy = 1 if y == Y(0) else -1
                c.line(x + sx * g, y, x + sx * (g + L), y)
                c.line(x, y + sy * g, x, y + sy * (g + L))
            c.setFont("Barlow", 6)
            c.setFillColor(HexColor("#000000"))
            c.drawString(X(0), I(0.08), f"Southwire PGS · NICA booklet · page {p.n} · trim 8.5 x 11 in · bleed 0.125 in")
        c.showPage()
    c.save()
    return overflow


def to_spreads(reader_pdf, path):
    import pymupdf
    src = pymupdf.open(reader_pdf)
    out = pymupdf.open()
    order = [[1], [2, 3], [4, 5], [6, 7], [8]]
    for grp in order:
        pg = out.new_page(width=PW * 72 * len(grp), height=PH * 72)
        for i, n in enumerate(grp):
            pg.show_pdf_page(pymupdf.Rect(i * PW * 72, 0, (i + 1) * PW * 72, PH * 72), src, n - 1)
    out.save(path)


# ----------------------------------------------------------------- PPTX
def to_pptx(pages, path):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from PIL import Image
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(PW), Inches(PH)
    blank = prs.slide_layouts[6]
    RGB = lambda h: RGBColor(*hexrgb(h))
    tmpdir = os.path.join(OUT, "_tmp")
    os.makedirs(tmpdir, exist_ok=True)
    for p in pages:
        s = prs.slides.add_slide(blank)
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = RGB(p.bg)
        for e in p.el:
            k = e["kind"]
            x, y = e.get("x", 0), e.get("y", 0)
            if k == "image":
                # clamp into the slide
                x0, y0 = max(x, 0), max(y, 0)
                x1, y1 = min(x + e["w"], PW), min(y + e["h"], PH)
                im = Image.open(e["path"])
                if e.get("crop"):
                    im = im.crop(e["crop"])
                W, H = im.size
                box = (int((x0 - x) / e["w"] * W), int((y0 - y) / e["h"] * H),
                       int((x1 - x) / e["w"] * W), int((y1 - y) / e["h"] * H))
                src = e["path"]
                if box != (0, 0, W, H) or e.get("crop"):
                    src = os.path.join(tmpdir, f"p{p.n}_{e['name']}.png")
                    im.crop(box).save(src)
                pic = s.shapes.add_picture(src, Inches(x0), Inches(y0), Inches(x1 - x0), Inches(y1 - y0))
                pic.name = e["name"] or "Image"
            elif k == "rect":
                x0, y0 = max(x, 0), max(y, 0)
                x1, y1 = min(x + e["w"], PW), min(y + e["h"], PH)
                shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0), Inches(y0), Inches(x1 - x0), Inches(y1 - y0))
                if e.get("fill"):
                    shp.fill.solid()
                    shp.fill.fore_color.rgb = RGB(e["fill"])
                else:
                    shp.fill.background()
                if e.get("line"):
                    shp.line.color.rgb = RGB(e["line"])
                    shp.line.width = Pt(e.get("lw", 0.6))
                else:
                    shp.line.fill.background()
                shp.shadow.inherit = False
                shp.name = e["name"] or "Rect"
            elif k == "line":
                ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e["x1"]), Inches(e["y1"]), Inches(e["x2"]), Inches(e["y2"]))
                ln.line.color.rgb = RGB(e["color"])
                ln.line.width = Pt(e["lw"])
                ln.name = e["name"] or "Line"
            elif k in ("dot", "marker"):
                r = e["r"]
                shp = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x - r), Inches(y - r), Inches(2 * r), Inches(2 * r))
                shp.fill.solid()
                shp.fill.fore_color.rgb = RGB(e.get("fill", COPPER))
                shp.line.color.rgb = RGB(WHITE)
                shp.line.width = Pt(1.0)
                shp.shadow.inherit = False
                shp.name = e["name"] or k
                if k == "marker":
                    tf = shp.text_frame
                    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                    pp = tf.paragraphs[0]
                    pp.alignment = PP_ALIGN.CENTER
                    run = pp.add_run()
                    run.text = e["n"]
                    run.font.size = Pt(r * 72 * 1.05)
                    run.font.bold = True
                    run.font.name = "Barlow Condensed"
                    run.font.color.rgb = RGB(e["color"])
            elif k == "text":
                tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(e["w"]), Inches(e["h"]))
                tb.name = e["name"] or "Text"
                tf = tb.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE if e["valign"] == "middle" else MSO_ANCHOR.TOP
                fname, bold = PPT_FONT[e["font"]]
                runs = e.get("rich") or [(ln_, e["color"]) for ln_ in [e["text"]]]
                lines = [e["text"]] if e.get("rich") else e["text"].split("\n")
                for li, line in enumerate(lines):
                    pp = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                    pp.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[e["align"]]
                    pp.line_spacing = e["lead"]
                    segs = e["rich"] if e.get("rich") else [(line, e["color"])]
                    for t, col in segs:
                        run = pp.add_run()
                        run.text = t
                        run.font.size = Pt(e["size"])
                        run.font.bold = bold
                        run.font.name = fname
                        run.font.color.rgb = RGB(col)
                        if e.get("track"):
                            rPr = run._r.get_or_add_rPr()
                            rPr.set("spc", str(int(e["track"] * 50)))
        s.notes_slide.notes_text_frame.text = (
            f"NICA booklet page {p.n}. Fonts: Barlow Condensed / Barlow (Google Fonts, SIL OFL) - install for exact "
            "rendering. Deck renders carry a faint baked 'Stephan Hardt' mark; replace with clean originals before print.")
    prs.save(path)


def main():
    os.makedirs(os.path.join(OUT, "png"), exist_ok=True)
    pages = build_pages()
    over = to_pdf(pages, os.path.join(OUT, "NICA_booklet_print.pdf"), marks=True)
    to_pdf(pages, os.path.join(OUT, "NICA_booklet_reader.pdf"), marks=False)
    to_spreads(os.path.join(OUT, "NICA_booklet_reader.pdf"), os.path.join(OUT, "NICA_booklet_spreads.pdf"))
    to_pptx(pages, os.path.join(OUT, "NICA_booklet.pptx"))
    import pymupdf
    d = pymupdf.open(os.path.join(OUT, "NICA_booklet_reader.pdf"))
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=150).save(os.path.join(OUT, "png", f"page_{i+1}.png"))
    for o in over:
        print("OVERFLOW", o)
    print("pages:", len(pages), "watermarked deck renders in use:", WATERMARKED)


if __name__ == "__main__":
    main()
