#!/usr/bin/env python3
"""Build Southwire_PowerGen_Brochure_NRG_Rev01.pdf â 8-page executive brochure.

Letter landscape 11x8.5 trim + 0.125in bleed all sides -> page box 11.25 x 8.75 in.
Design system: warm white #F6F3EE body, graphite dark pages, copper spot accents,
Helvetica only, three sizes per page max.
"""
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color

IN = 72
PW, PH = 11.25 * IN, 8.75 * IN          # 810 x 630
BLEED = 0.125 * IN                       # 9
M = 54                                   # content margin from page edge (~0.63in inside trim)

def C(hexs):
    hexs = hexs.lstrip('#')
    return Color(int(hexs[0:2], 16)/255, int(hexs[2:4], 16)/255, int(hexs[4:6], 16)/255)

WARM      = C('F6F3EE')
GRAPHITE  = Color(23/255, 25/255, 28/255)   # sampled from source dark pages (seamless with crops)
INK       = C('1A1C22')
GRAY      = C('6E6C66')
GRAY_LT   = C('96938C')
COPPER    = C('C67A43')
COPPER_LT = C('E3A06D')
COPPER_DP = C('9D4E24')
HAIR_DK   = Color(60/255, 63/255, 68/255)
WHITE     = Color(1, 1, 1)
OFFWHITE  = Color(236/255, 234/255, 230/255)

A = 'assets/'
IMG = {k: ImageReader(A + f) for k, f in {
    'hex_top': 'hex_top_fade.png',
    'hex_bottom': 'hex_bottom_fade.png',
    'hex_side': 'hex_side_fade.png',
    'lockup_dark': 'lockup_dark_keyed.png',       # white nrg | Southwire PGS on graphite
    'lockup_light': 'lockup_light.png',     # nrg | Southwire PGS on warm white
    'hero': 'hero_sky.jpg',                 # 3840x2987 sky-extended plant render
}.items()}

FOOTER = 'Stephan Hardt   |   Power Generation Solutions'


# ---------------------------------------------------------------- helpers
def tracked(c, x, y, text, font, size, track, color, align='left'):
    """Draw letter-spaced text; returns width."""
    c.setFont(font, size)
    w = c.stringWidth(text, font, size) + track * max(len(text) - 1, 0)
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(track)
    t.setFillColor(color)
    t.textOut(text)
    t.setCharSpace(0)
    c.drawText(t)
    return w


def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if c.stringWidth(trial, font, size) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, x, y, text, font, size, leading, maxw, color, align='left'):
    lines = wrap(c, text, font, size, maxw)
    c.setFillColor(color)
    c.setFont(font, size)
    for ln in lines:
        if align == 'center':
            c.drawCentredString(x, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y + leading


def img_w(key, h):
    iw, ih = IMG[key].getSize()
    return h * iw / ih


def light_frame(c, kicker, folio, band=False):
    """Warm-white page base, copper top hairline, header lockup, kicker; footer unless band."""
    c.setFillColor(WARM)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(COPPER)
    c.rect(0, PH - 3.5, PW, 3.5, fill=1, stroke=0)
    lh = 23
    c.drawImage(IMG['lockup_light'], M, PH - 30 - lh, width=img_w('lockup_light', lh),
                height=lh, mask='auto')
    tracked(c, PW - M, PH - 30 - 13, kicker, 'Helvetica-Bold', 7.5, 1.6, COPPER, align='right')
    if not band:
        c.setFillColor(GRAY_LT)
        c.setFont('Helvetica', 6.5)
        c.drawString(M, 30, FOOTER)
        tracked(c, PW - M, 30, folio, 'Helvetica-Bold', 6.5, 1.2, COPPER, align='right')


def dark_band(c, h=76):
    c.setFillColor(GRAPHITE)
    c.rect(0, 0, PW, h, fill=1, stroke=0)


def band_footer(c, folio):
    c.setFillColor(Color(140/255, 138/255, 134/255))
    c.setFont('Helvetica', 6.5)
    c.drawString(M, 14, FOOTER)
    tracked(c, PW - M, 14, folio, 'Helvetica-Bold', 6.5, 1.2, COPPER_LT, align='right')



# ---------------------------------------------------------------- pages
def p1_cover(c):
    c.setFillColor(GRAPHITE)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    th = PW * 785 / 4752
    c.drawImage(IMG['hex_top'], 0, PH - th, width=PW, height=th, mask='auto')
    c.drawImage(IMG['hex_bottom'], 0, 0, width=PW, height=th, mask='auto')

    lw = 200
    lh = lw * 202 / 943
    c.drawImage(IMG['lockup_dark'], PW/2 - lw/2, 472, width=lw, height=lh, mask='auto')

    tracked(c, PW/2, 352, 'ACCELERATING', 'Helvetica-Bold', 40, 6, WHITE, align='center')
    tracked(c, PW/2, 300, 'TIME TO POWER', 'Helvetica-BoldOblique', 40, 6, COPPER_LT, align='center')
    c.setStrokeColor(COPPER)
    c.setLineWidth(1.2)
    c.line(PW/2 - 62, 274, PW/2 + 62, 274)

    c.setFillColor(OFFWHITE)
    c.setFont('Helvetica', 11)
    c.drawCentredString(PW/2, 236, "Accelerating & protecting power readiness across NRG's gas power generation buildout.")
    tracked(c, PW/2, 210,
            'COMBINED CYCLE  ·  SIMPLE CYCLE & PEAKERS  ·  MODULAR POWER  ·  BLACK START  ·  COAL/GAS REPOWER  ·  GREENFIELD & BROWNFIELD',
            'Helvetica', 6.8, 1.1, Color(150/255, 148/255, 144/255), align='center')

    tracked(c, PW/2, 158, 'PRESERVE SCHEDULE CERTAINTY THROUGH ENERGIZATION.',
            'Helvetica-Bold', 8.5, 2.2, COPPER_LT, align='center')

    c.setFillColor(Color(158/255, 156/255, 152/255))
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(PW/2, 84, 'Stephan Hardt   |   Director, Power Generation Solutions   |   www.southwire.com')


def p2_why_now(c):
    light_frame(c, 'WHY NOW', '02', band=True)
    y = PH - 122
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 27)
    c.drawString(M, y, "NRG's growth agenda creates three distinct")
    c.drawString(M, y - 33, 'electrical-delivery environments & power demand.')

    cols = [
        ('1.5 GW', 'TEF PORTFOLIO',
         'One project operating; two targeting mid-2028. Not the entire portfolio under construction.'),
        ('5.4 GW', 'NEWBUILD DEVELOPMENT',
         'Turbine and EPC access supports a development runway through 2032.'),
        ('25.8 GW', 'OPERATING FLEET',
         'Reported operating fleet after the LS Power acquisition; ~1–2 GW of upgrades under evaluation.'),
    ]
    colw = (PW - 2 * M - 2 * 36) / 3
    for i, (num, label, desc) in enumerate(cols):
        x = M + i * (colw + 36)
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 34)
        c.drawString(x, 356, num)
        c.setStrokeColor(COPPER)
        c.setLineWidth(1.4)
        c.line(x + 1, 338, x + 27, 338)
        tracked(c, x, 316, label, 'Helvetica-Bold', 8, 1.5, COPPER_DP)
        para(c, x, 294, desc, 'Helvetica', 9.5, 13.5, colw - 12, GRAY)

    c.setFillColor(GRAY)
    c.setFont('Helvetica', 10)
    c.drawString(M, 204, 'Specifications, capacity, metals hedging, releases, reels, package interfaces and field')
    c.drawString(M, 190, 'readiness still have to converge on COD.  Do not sum the figures — asset states overlap.')
    c.setFillColor(GRAY_LT)
    c.setFont('Helvetica', 6)
    c.drawRightString(PW - M, 100, 'Source: NRG 2Q26, Aug. 4, 2026')

    dark_band(c, 84)
    tracked(c, M, 56, 'DIFFERENT ASSET STATES. ONE REQUIREMENT.',
            'Helvetica-Bold', 8, 1.8, COPPER_LT)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 13.5)
    c.drawString(M, 34, 'Preserve schedule certainty through energization.')
    band_footer(c, '02')


def p3_thesis(c):
    c.drawImage(IMG['hero'], 0, 0, width=PW, height=PH)
    tracked(c, M, PH - 62, 'THE THESIS', 'Helvetica-Bold', 7.5, 1.6, COPPER_DP)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 23)
    c.drawString(M, PH - 94, 'Time to power is an electrical execution problem')
    c.drawString(M, PH - 123, 'before it is a cable-buying problem.')
    bullets = [
        'Interfaces cross packages, zones, POI, contractors and turnover paths.',
        'Late material decisions return as handling, rework and commissioning exposure.',
        'Managing the workstream as a system protects schedule better than isolated purchase-order optimization.',
    ]
    by = PH - 156
    c.setFont('Helvetica', 9.5)
    for b in bullets:
        c.setStrokeColor(COPPER_DP)
        c.setLineWidth(1.4)
        c.line(M + 1, by + 3, M + 13, by + 3)
        c.setFillColor(INK)
        c.setFont('Helvetica', 9.5)
        c.drawString(M + 22, by, b)
        by -= 18

    c.setFillColor(GRAPHITE)
    c.rect(0, 0, PW, 44, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-BoldOblique', 9.5)
    c.drawString(M, 18, 'The plant-wide electrical-delivery partner — cable scope ready for the workface, not merely available at the warehouse.')
    c.setFillColor(GRAY)
    c.setFont('Helvetica', 6.5)
    c.drawRightString(PW - M, PH - 62, FOOTER + '   ·   03')


def p4_risks(c):
    light_frame(c, 'THE THREE RISKS', '04', band=True)
    y = PH - 122
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 27)
    c.drawString(M, y, 'Three execution risks can erode certainty')
    c.drawString(M, y - 33, 'between design and energization.')

    cols = [
        ('01', 'LABOR & DEMAND PRESSURE',
         'AI and electrification power demand collide with long pulls, dense terminations and compressed turnover windows — concentrating labor exactly when flexibility is lowest.'),
        ('02', 'MATERIAL + INSTALLATION FIT',
         'Ratings, routes, reel lengths, accessories and releases must match the workface, not only the BOM — or material arrives right and installs wrong.'),
        ('03', 'FRAGMENTED COORDINATION',
         'Civil, electrical, OEM and contractor decisions can converge after routing and procurement choices are already locked, turning gaps into rework.'),
    ]
    colw = (PW - 2 * M - 2 * 36) / 3
    for i, (num, label, desc) in enumerate(cols):
        x = M + i * (colw + 36)
        tracked(c, x, 346, num, 'Helvetica-Bold', 21, 2, COPPER)
        c.setStrokeColor(COPPER)
        c.setLineWidth(1.4)
        c.line(x + 1, 330, x + 27, 330)
        tracked(c, x, 308, label, 'Helvetica-Bold', 8.5, 1.2, INK)
        para(c, x, 286, desc, 'Helvetica', 9.5, 13.5, colw - 12, GRAY)

    dark_band(c, 84)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 12.5)
    c.drawString(M, 48, 'Late handoffs become schedule and commissioning exposure.')
    tracked(c, M, 28, 'LABOR AVAILABILITY   |   MATERIAL READINESS   |   DECISION TIMING',
            'Helvetica', 7, 1.6, Color(150/255, 148/255, 144/255))
    band_footer(c, '04')


def p5_system(c):
    light_frame(c, 'THE SYSTEM', '05', band=True)
    y = PH - 122
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 27)
    c.drawString(M, y, 'One coordinated flow aligns decisions')
    c.drawString(M, y - 33, 'from planning through turnover.')
    c.setFillColor(GRAY)
    c.setFont('Helvetica', 10.5)
    c.drawString(M, y - 64, 'Southwire connects application support, material planning, sequenced logistics and field')
    c.drawString(M, y - 79, 'readiness — without changing project accountability.')

    steps = [
        ('1', 'PLAN + FORECAST', 'Scope and capacity visibility'),
        ('2', 'APPLICATION ALIGNMENT', 'Codes, duty and alternates'),
        ('3', 'MATERIAL + REEL STRATEGY', 'Routes, cuts and reel plan'),
        ('4', 'RELEASE + LOGISTICS', 'Sequence by zone and milestone'),
        ('5', 'INSTALLATION READINESS', 'Labels, kits and pull planning'),
        ('6', 'FIELD SUPPORT + TURNOVER', 'Feedback, testing and records'),
    ]
    x0, x1 = M + 40, PW - M - 40
    ny = 292
    c.setStrokeColor(COPPER)
    c.setLineWidth(1)
    c.line(x0, ny, x1, ny)
    n = len(steps)
    for i, (num, name, desc) in enumerate(steps):
        x = x0 + i * (x1 - x0) / (n - 1)
        r = 13.5
        c.setFillColor(GRAPHITE if i < n - 1 else COPPER_DP)
        c.circle(x, ny, r, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawCentredString(x, ny - 3.5, num)
        yy = ny - 34
        for ln in wrap(c, name, 'Helvetica-Bold', 8, 90):
            tracked(c, x, yy, ln, 'Helvetica-Bold', 8, 0.8, INK, align='center')
            yy -= 11.5
        yy -= 3
        c.setFillColor(GRAY)
        c.setFont('Helvetica', 7.5)
        for ln in wrap(c, desc, 'Helvetica', 7.5, 88):
            c.drawCentredString(x, yy, ln)
            yy -= 10

    dark_band(c, 84)
    tracked(c, PW/2, 40, 'FIELD-ENGINEER WHAT IS UNIQUE. PREFABRICATE WHAT REPEATS.',
            'Helvetica-Bold', 10, 1.8, COPPER_LT, align='center')
    band_footer(c, '05')


def p6_value(c):
    light_frame(c, 'THE OUTCOME  ·  AN HONEST BASIS', '06')
    y = PH - 116
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 24)
    c.drawString(M, y, 'The value to NRG is fewer execution surprises —')
    c.drawString(M, y - 30, 'not more supplier services.')

    rows = [
        ('ALIGN APPLICATIONS + INTERFACES EARLY', 'Fewer late changes and handoff failures'),
        ('GATE CAPACITY + RELEASES', 'More predictable material availability and sequencing'),
        ('PLAN REELS + REPEATABLE SETS TO THE WORKFACE', 'Less handling and avoidable rework'),
        ('CARRY FIELD RECORDS THROUGH TURNOVER', 'Cleaner commissioning and lifecycle continuity'),
    ]
    ry = y - 76
    xr = M + 350
    for label, outcome in rows:
        tracked(c, M, ry, label, 'Helvetica-Bold', 8, 1.0, INK)
        c.setStrokeColor(COPPER)
        c.setLineWidth(1)
        c.line(xr - 26, ry + 2.5, xr - 12, ry + 2.5)
        c.line(xr - 16, ry + 5.5, xr - 12, ry + 2.5)
        c.line(xr - 16, ry - 0.5, xr - 12, ry + 2.5)
        c.setFillColor(GRAY)
        c.setFont('Helvetica', 9.5)
        c.drawString(xr, ry, outcome)
        c.setStrokeColor(C('D8D2C8'))
        c.setLineWidth(0.6)
        c.line(M, ry - 11, PW - M, ry - 11)
        ry -= 32

    tracked(c, PW/2, 262, 'OUTCOME HYPOTHESES — TO VALIDATE ON ONE LIVE NRG SCOPE',
            'Helvetica-Bold', 8, 1.8, COPPER_DP, align='center')
    boxes = [
        'Adjacent experience indicates where to test — not what NRG will save.',
        'No presumption that the answer is prefab — or that Southwire belongs in the solution.',
    ]
    bw, bh, gap = (PW - 2 * M - 28) / 2, 84, 28
    for i, txt in enumerate(boxes):
        bx = M + i * (bw + gap)
        byt = 236
        c.setStrokeColor(COPPER)
        c.setLineWidth(0.9)
        c.rect(bx, byt - bh, bw, bh, fill=0, stroke=1)
        lines = wrap(c, txt, 'Helvetica', 11.5, bw - 44)
        ty = byt - bh/2 + (len(lines) - 1) * 16 / 2 - 4
        c.setFillColor(INK)
        c.setFont('Helvetica', 11.5)
        for ln in lines:
            c.drawCentredString(bx + bw/2, ty, ln)
            ty -= 16


def p7_who(c):
    light_frame(c, 'WHO WE ARE', '07')
    y = PH - 116
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 25)
    c.drawString(M, y, 'A family-held American manufacturer —')
    c.drawString(M, y - 31, 'from copper rod to finished cable since 1950.')
    c.setFillColor(GRAY)
    c.setFont('Helvetica', 10)
    c.drawString(M, y - 62, 'Roy Richards founded Southwire after the poles his crews built stood wireless for months after World War II.')
    c.drawString(M, y - 77, 'From 12 employees and three secondhand machines in Carrollton, Georgia, Southwire remains family-held')
    c.drawString(M, y - 92, 'and vertically integrated — from copper rod through finished cable.')

    stats = [
        ('1950', 'FOUNDED', INK),
        ('9,000+', 'EMPLOYEES WORLDWIDE', INK),
        ('$9.7B', '2025 REVENUE · FORBES', COPPER_DP),
        ('12', 'INDUSTRIES SERVED', INK),
        ('7', 'COPPER MARK SITES', INK),
    ]
    c.setStrokeColor(C('D8D2C8'))
    c.setLineWidth(0.75)
    c.line(M, 356, PW - M, 356)
    coln = len(stats)
    colw = (PW - 2 * M) / coln
    for i, (val, label, col) in enumerate(stats):
        x = M + i * colw
        c.setFillColor(col)
        c.setFont('Helvetica-Bold', 27)
        c.drawString(x, 306, val)
        tracked(c, x, 284, label, 'Helvetica-Bold', 6.5, 1.1, GRAY)

    proofs = [
        ('COPPER TECHNOLOGY', 'Half of the world’s copper rod passes through a Southwire SCR® system.'),
        ('U.S. POWER GRID', 'We produce half of the wire and cable that moves U.S. electricity.'),
        ('AMERICAN HOMES', 'Half of American homes contain wiring produced by Southwire.'),
    ]
    colw3 = (PW - 2 * M - 2 * 36) / 3
    for i, (label, txt) in enumerate(proofs):
        x = M + i * (colw3 + 36)
        c.setStrokeColor(COPPER)
        c.setLineWidth(1.4)
        c.line(x + 1, 226, x + 27, 226)
        tracked(c, x, 204, label, 'Helvetica-Bold', 8, 1.5, COPPER_DP)
        para(c, x, 182, txt, 'Helvetica', 9.5, 13.5, colw3 - 12, GRAY)

    c.setFillColor(GRAY_LT)
    c.setFont('Helvetica', 8.5)
    c.drawString(M, 108, 'HV underground  ·  MV & LV power  ·  I&C, comms and fiber  ·  classified & circuit integrity  ·  modular & factory-built power  ·  accessories & raceway')


def p8_ask(c):
    c.setFillColor(GRAPHITE)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    sw = PH * 548 / 2640
    c.drawImage(IMG['hex_side'], 0, 0, width=sw, height=PH, mask='auto')
    c.setStrokeColor(COPPER)
    c.setLineWidth(1.4)
    c.line(sw + 4, 0, sw + 4, PH)

    lw = 168
    lh = lw * 202 / 943
    c.drawImage(IMG['lockup_dark'], PW - M - lw, PH - 48 - lh, width=lw, height=lh, mask='auto')

    x0 = sw + 56
    tracked(c, x0, PH - 88, 'THE ASK', 'Helvetica-Bold', 7.5, 1.6, COPPER_LT)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 29)
    c.drawString(x0, PH - 128, 'ONE SITE WALK.  ONE HOUR.')
    c.drawString(x0, PH - 165, 'NO SALES PRESENTATION.')
    c.setStrokeColor(COPPER)
    c.setLineWidth(1.2)
    c.line(x0, PH - 190, x0 + 64, PH - 190)

    c.setFillColor(OFFWHITE)
    c.setFont('Helvetica', 10.5)
    c.drawString(x0, PH - 216, 'NRG selects the starting scope — one live package, conversion/uprate screen or planned-')
    c.drawString(x0, PH - 231, 'outage replacement — and brings the people closest to execution.')

    walk = ['SELECT SCOPE', 'WALK THE WORK', 'MAP THE RISK', 'DECIDE']
    wx0, wx1, wy = x0 + 12, PW - M - 30, 344
    c.setStrokeColor(COPPER)
    c.setLineWidth(0.9)
    c.line(wx0, wy, wx1, wy)
    for i, wlabel in enumerate(walk):
        x = wx0 + i * (wx1 - wx0) / (len(walk) - 1)
        c.setFillColor(COPPER_DP if i == len(walk) - 1 else Color(50/255, 53/255, 58/255))
        c.circle(x, wy, 10.5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawCentredString(x, wy - 3, str(i + 1))
        tracked(c, x, wy - 26, wlabel, 'Helvetica-Bold', 6.8, 1.0, OFFWHITE, align='center')

    rows = [
        ('INPUT', 'One live scope'),
        ('OUTPUT', 'Written execution-risk read-back — milestone exposure, route, reel + release constraints'),
        ('DECISION', 'Stop, standardize or define a bounded pilot'),
    ]
    ry = 268
    for label, val in rows:
        tracked(c, x0, ry, label, 'Helvetica-Bold', 8, 1.6, COPPER_LT)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawString(x0 + 92, ry - 1, val)
        c.setStrokeColor(HAIR_DK)
        c.setLineWidth(0.6)
        c.line(x0, ry - 13, PW - M, ry - 13)
        ry -= 40

    tracked(c, x0, 122, 'NO PRICING EXERCISE. NO BROAD COMMERCIAL COMMITMENT.',
            'Helvetica-Bold', 9, 1.6, COPPER_LT)

    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawString(x0, 82, 'Stephan Hardt   |   Director, Power Generation Solutions')
    c.setFillColor(Color(168/255, 166/255, 162/255))
    c.setFont('Helvetica', 8.5)
    c.drawString(x0, 66, 'stephan.hardt@southwire.com   |   +1 470-439-8488')


# ---------------------------------------------------------------- build
def build(path='Southwire_PowerGen_Brochure_NRG_Rev01.pdf'):
    c = rl_canvas.Canvas(path, pagesize=(PW, PH))
    c.setAuthor('Stephan Hardt')
    c.setTitle('Accelerating Time to Power — NRG | Southwire Power Generation Solutions')
    c.setSubject('SWR-PG-BROCHURE-NRG Rev 01')
    for draw in [p1_cover, p2_why_now, p3_thesis, p4_risks, p5_system, p6_value, p7_who, p8_ask]:
        draw(c)
        c.setTrimBox([BLEED, BLEED, PW - BLEED, PH - BLEED])
        c.setCropBox([0, 0, PW, PH])
        c.showPage()
    c.save()
    print('built', path)


if __name__ == '__main__':
    build()
