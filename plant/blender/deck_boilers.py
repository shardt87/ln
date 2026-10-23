"""Boiler section for the October Strategy deck (owner, Oct 22: "boilers ... greenfield or brownfield, so when I go talk
to these companies I can share that we have solutions for boilers"): two slides in the deck's format (1440 x 810 pt,
dark ground, copper accents, Barlow), from the SW-3X1 boiler scenes and the model's cable schedule.

  1. Boilers: greenfield & brownfield: the three boiler types in the model (HRSG with duct burner, gas-fired package
     boiler, HRSG module replacement) with their cable counts, and what Southwire cable goes to each;
  2. Brownfield: the outage clock is the cost: the module lift, the cable work that rides the same window;
  3. The boiler offering: each product circled where it runs in the boiler scenes, with its Southwire SPEC, a stock
     number for a representative size and a link to the product page (from Southwire's catalogue listings, Oct 2026).

Numbers: brochure/boiler_numbers.json (one HRSG train incl. its feed pumps, SCR blowers, chemical feed, CEMS and duct
burner; the auxiliary boiler), summed from the Cable Schedule sheet. Equipment is generic in the model and on the
slides; OEM names stay in the talking points (renders/deck/boilers/talking_points.md).

  python3 blender/deck_boilers.py   ->  renders/deck/boilers/SW-3X1_boilers.pdf + slide PNGs
"""
import json
import os
import subprocess

import brochure_zones as bz
import credit

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
OUT = os.path.join(PLANT, "renders", "deck", "boilers")
R = os.path.join(PLANT, "renders", "boilers")
url = bz.url
COPPER, COPPER_L, INK, WHITE, GREY = bz.COPPER, bz.COPPER_L, bz.INK, bz.WHITE, bz.GREY
N = json.load(open(os.path.join(PLANT, "brochure", "boiler_numbers.json")))

CSS = bz.CSS + f"""
@page slide {{ size: 20in 11.25in; margin: 0; }}
.slide {{ page: slide; width: 20in; height: 11.25in; }}
.s {{ position: absolute; left: 0; top: 0; width: 1440px; height: 810px; transform: scale(1.333333); transform-origin: 0 0; }}
.h2 {{ font: 800 64px/.92 BC; color: {WHITE}; text-transform: uppercase; }}
.h2 em {{ font-style: normal; color: {COPPER}; }}
.lede {{ font: 400 19px/1.45 B; color: {GREY}; }}
.col {{ position: absolute; }}
.ph {{ width: 100%; object-fit: cover; display: block; }}
.ct {{ font: 800 27px/1 BC; color: {WHITE}; text-transform: uppercase; letter-spacing: .02em; }}
.cnum {{ font: 700 15px/1 BC; letter-spacing: .24em; color: {COPPER}; text-transform: uppercase; }}
.cd {{ font: 400 15px/1.45 B; color: {GREY}; }}
.big {{ font: 800 40px/1 BC; color: {COPPER}; }}
.bigl {{ font: 700 12px/1.2 BC; letter-spacing: .16em; color: {GREY}; text-transform: uppercase; }}
table.m {{ border-collapse: collapse; width: 100%; }}
table.m th {{ font: 700 12px/1.1 BC; letter-spacing: .1em; color: {GREY}; text-transform: uppercase; text-align: center;
             padding: 0 6px 5px; vertical-align: bottom; }}
table.m th:first-child, table.m td:first-child {{ text-align: left; }}
table.m td {{ font: 400 14px/1.2 B; color: {WHITE}; text-align: center; padding: 5px 6px; border-top: 1px solid #2c3036; }}
table.m td:first-child {{ font: 800 17px/1 BC; letter-spacing: .04em; text-transform: uppercase; }}
.dot {{ display: inline-block; width: 13px; height: 13px; border-radius: 7px; background: {COPPER}; }}
.ring {{ display: inline-block; width: 13px; height: 13px; border-radius: 7px; border: 2px solid {COPPER}; }}
.li {{ font: 400 14.5px/1.4 B; color: {GREY}; padding: 8px 0 9px 22px; border-top: 1px solid #2c3036; position: relative; }}
.li:before {{ content: ''; position: absolute; left: 0; top: 15px; width: 9px; height: 9px; background: {COPPER}; }}
.li b {{ font: 800 16.5px/1.2 BC; letter-spacing: .05em; color: {WHITE}; text-transform: uppercase; margin-right: 8px; }}
.cap {{ font: 400 12px/1.35 B; color: #aab0b6; }}
.qr {{ list-style: none; margin-top: 5px; }}
.qr li {{ font: 400 11.6px/1.3 B; color: #d4d8dc; padding-left: 12px; position: relative; margin-top: 3px; }}
.qr li:before {{ content: ''; position: absolute; left: 0; top: 6px; width: 5px; height: 5px; background: {COPPER}; }}
.qr b {{ color: {WHITE}; }}
.foot {{ font: 400 11px/1 B; color: #80868c; letter-spacing: .04em; }}
"""


def img(k):
    full = os.path.join(PLANT, "renders", "boilers_full", f"{k}_pro_clean.jpg")    # full-quality renders when present
    return url(full if os.path.exists(full) else os.path.join(R, f"{k}_pro_clean.jpg"))


def kft(ft):
    return f"{ft / 1000:,.0f},000"


def foot(n, short=False):
    left = ("SW-3X1 MODEL &middot; NOT ENGINEERED" if short else
            "SW-3X1 MODEL &middot; CONCEPTUAL ILLUSTRATION, NOT ENGINEERED &middot; QUANTITIES FROM THE MODEL'S CABLE SCHEDULE")
    return f"""<div class="abs foot" style="left:64px;right:64px;bottom:26px;display:flex;justify-content:space-between;
      border-top:1px solid #2c3036;padding-top:11px"><span>{left}</span><span>{credit.EMAIL} &nbsp;&middot;&nbsp; BOILERS {n}/11</span></div>"""


def slide1():
    h, a = N["hrsg"], N["aux"]
    cols = [
        ("01 &middot; Greenfield", "Heat-recovery boiler", "BH2",
         "Behind every gas turbine: three-pressure HRSG with SCR and a duct burner. Feed pumps at 13.8 kV, drum-level and "
         "thermocouple runs, burner management in a Class I Div 2 skid.",
         f"{h['cables']:,}", "cables per HRSG train", kft(h["ft"]), "ft of cable per train"),
        ("02 &middot; Greenfield or retrofit", "Gas-fired package boiler", "BX1",
         "The plant's auxiliary boiler, the same package sold to industry: burner and BMS, gas train with double block "
         "and bleed, FD fan on a VFD, feedwater pumps, its own MCC e-house.",
         f"{a['cables']:,}", "cables per package boiler", kft(a["ft"]), "ft of cable"),
        ("03 &middot; Brownfield", "Module replacement outage", "BB1",
         "An HP evaporator module lifted out through the opened roof. The cable work rides the same outage window, "
         "so it has to be staged, pre-terminated and pulled fast.",
         "Outage", "critical path", "SIMpull", "+ pre-terminated harnesses"),
    ]
    W, G, X0, TOP, PH = 418, 30, 64, 198, 184
    c = ""
    for k, (num, title, im, desc, b1, l1, b2, l2) in enumerate(cols):
        x = X0 + k * (W + G)
        c += f"""
  <div class="col" style="left:{x}px;top:{TOP}px;width:{W}px">
    <img class="ph" src="{img(im)}" style="height:{PH}px">
    <div class="cnum" style="margin-top:14px">{num}</div>
    <div class="ct" style="margin-top:6px">{title}</div>
    <div class="cd" style="margin-top:8px;height:66px;font-size:14px">{desc}</div>
    <div style="display:flex;gap:26px;margin-top:4px">
      <div><div class="big">{b1}</div><div class="bigl" style="margin-top:4px">{l1}</div></div>
      <div><div class="big">{b2}</div><div class="bigl" style="margin-top:4px">{l2}</div></div></div>
  </div>"""
    D, O = '<span class="dot"></span>', '<span class="ring"></span>'
    rows = [("HRSG + duct burner", D, D, D, D, D, D, D),
            ("Package boiler", "", D, D, D, D, D, D),
            ("Replacement outage", O, D, D, D, D, D, D)]
    heads = ["", "MV-105 15 kV<br>feed pumps", "TC-ER 600 V<br>power &amp; VFD", "ARMOR-X MC-HL<br>gas trains (C1D2)",
             "Control<br>TC-ER", "Instrumentation<br>PLTC &middot; TC ext.", "SIMpull &middot;<br>reel rollers",
             "Pre-terminated<br>harnesses"]
    tb = "<tr>" + "".join(f"<th>{t}</th>" for t in heads) + "</tr>" + "".join(
        "<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Boiler solutions &nbsp;&middot;&nbsp; SW-3X1</div>
  <div class="abs h2" style="left:62px;top:86px">Boilers: <em>greenfield</em> &amp; <em>brownfield</em></div>
  <div class="abs lede" style="left:64px;top:158px;width:1300px;font-size:18px">One cable partner from the new HRSG to the package
    boiler to the outage that replaces a module: the same products, staged and pulled the same way.</div>
  {c}
  <div class="abs" style="left:64px;top:606px;width:1312px">
    <div class="kicker" style="font-size:12px">Cable by boiler type</div>
    <table class="m" style="margin-top:8px;width:1312px">{tb}</table>
    <div class="cap" style="margin-top:6px"><span class="dot" style="width:9px;height:9px"></span> in scope &nbsp;
      <span class="ring" style="width:9px;height:9px;border-width:1.5px"></span> when the outage includes feed-pump
      or MV work</div>
  </div>
  {foot(1)}
</section>"""


def slide2():
    sols = [("Stage before the trip", "cut-to-length reels on SIMpull Cradles and reel rollers, labelled per pull, at the "
                                      "unit before the outage starts"),
            ("Pre-terminate", "factory-made harnesses with QR tags land on the marshalling boxes: test, not terminate, "
                              "on the critical path"),
            ("Pull clean", "SIMpull reels and a sheave at the HRSG wall: one crew, no reel jacks, tension recorded"),
            ("Cut back and recycle", "old cable segregated into recycling bins as the module comes out"),
            ("Conversions", "new burner management and gas trains in Class I Div 2 run in ARMOR-X MC-HL")]
    lis = "".join(f'<div class="li"><b>{a}</b>{b}</div>' for a, b in sols)
    return f"""
<section class="page slide">
  <img class="abs" src="{img('BB1')}" style="left:0;top:0;width:830px;height:810px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:830px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,0) 70%,
       rgba(14,16,18,1) 100%),linear-gradient(180deg,rgba(14,16,18,.55) 0%,rgba(14,16,18,0) 26%)"></div>
  <div class="abs kicker" style="left:48px;top:44px;color:{WHITE}">Brownfield &nbsp;&middot;&nbsp; HRSG 3 outage</div>
  <div class="abs cap" style="left:48px;top:740px;width:560px;color:{WHITE}">HRSG 3: an HP evaporator module lifted out
    through the opened roof by a crawler crane; the new module waits on a lowboy on the ring road.</div>
  <div class="abs kicker" style="left:870px;top:56px">Boiler solutions &nbsp;&middot;&nbsp; replacement</div>
  <div class="abs h2" style="left:868px;top:84px;font-size:52px">The outage clock<br><em>is the cost</em></div>
  <div class="abs lede" style="left:870px;top:200px;width:506px;font-size:16px">On a boiler or HRSG replacement every hour
    of the outage costs. Cable rides the same window, so it moves off the critical path.</div>
  <div class="abs" style="left:870px;top:262px;width:506px">{lis}</div>
  <div class="abs" style="left:870px;top:586px;width:243px;height:122px;border:2px solid {WHITE};overflow:hidden">
    <img src="{img('BB3')}" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs" style="left:1133px;top:586px;width:243px;height:122px;border:2px solid {WHITE};overflow:hidden">
    <img src="{img('BB2')}" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs cap" style="left:870px;top:712px;width:243px">Cable work at the HRSG e-house</div>
  <div class="abs cap" style="left:1133px;top:712px;width:243px">Old module on the hook</div>
  {foot(10, short=True).replace("left:64px", "left:870px")}
</section>"""


# ------------------------------------------------------------------------------- slide 3: the offering
# Southwire products for the boiler scope. Stock numbers are one representative catalogue size per product (the size
# noted), taken from Southwire's own product listings; other sizes and constructions are on the same SPEC.
PRODUCTS = [
    (1, "MV-105 15 kV", "1/C Cu, 220 mil NL-EPR 133 %, tape shield, SIMpull PVC", "Feed-pump motors, 13.8 kV", "46302",
     "95604599", "500 kcmil", "https://southwire.com/wire-cable/medium-voltage-power-cable/1-c-cu-15kv-220-nlepr-133-simpull-pvc-mv-105/p/95604599"),
    (2, "Type TC-ER power", "3/C Cu XHHW-2 + ground, PVC, 600 V", "Fans, pumps, MCC feeders", "45252", "95305999",
     "12 AWG 3/C", "https://www.southwire.com/wire-cable/power-control/cu-600-1000v-xlpe-insulation-pvc-jacket-xhhw-2-ct-rated-sunlight-resistant-for-direct-burial-silicone-free/p/95305999"),
    (3, "ARMOR-X MC-HL", "Cu XLPE XHHW-2, welded armor, PVC, 600 V, Class I Div 2", "Gas trains, burner skids", "45352",
     "89052799", "8 AWG 4/C", "https://www.southwire.com/wire-cable/armored-power-cable/4-c-cu-600v-xlpe-xhhw-2-armor-x-pvc-power-cable-with-ground/p/89052799"),
    (4, "ARMOR-X MC-HL VFD", "3/C Cu XLPE XHHW-2 + ground, VFD rated", "FD fan on its drive", "45352", "89051899",
     "3/0 3/C", "https://www.southwire.com/wire-cable/armored-power-cable/3-c-cu-600v-xlpe-xhhw-2-armor-x-pvc-power-cable-with-ground-vfd/p/89051899"),
    (5, "Control TC-ER", "Cu XLPE XHHW-2, 600 V", "BMS panels, valves, MOVs", "45053", "89067701", "14 AWG 5/C",
     "https://southwire.com/wire-cable/power-control/spec45053-cu-600v-xlpe-insulation-thermoplastic-cpe-tp-jacket-xhhw-2-ct-rated-sunlight-resistant-for-direct-burial-silicone-free/p/89067701"),
    (6, "Instrumentation PLTC / ITC", "300 V, shielded pairs + overall shield (SPOS)", "Flame scanners, drum level, transmitters",
     "43303", "per pair count", "", "https://www.southwire.com/wire-cable/instrumentation/300v-cu-pvc-pairs-pvc-spos-instrumentation/p/SPEC43303"),
    (7, "Thermocouple extension", "PVC, PLTC multi-pair (KX on request), 105 °C", "HRSG gas-path and tube temperatures",
     "42345", "per construction", "", "https://cabletechsupport.southwire.com/en/cablespec/download_spec/?spec=42345"),
    (8, "SIMpull Cradle", "for 51 / 61 in SIMpull Reels, one-person payoff", "Outage staging and pulls", "SPR-CRDL",
     "67606001", "", "https://www.southwire.com/tools-equipment/material-handling-storage/spr-crdl-simpull-cradle/p/67606001"),
]
# where each product is circled: view -> [(product no., 3D point in the model)]
SPOTS = {
    "BX1": [(2, (946.0, 1496.0, 15.0)), (3, (980.0, 1464.3, 3.0)), (4, (945.5, 1461.7, 9.0)), (5, (967.8, 1475.5, 7.5)),
            (6, (963.2, 1515.0, 14.2))],
    "BH2": [(3, (683.0, 692.85, 2.9)), (5, (691.75, 692.75, 6.5)), (6, (680.0, 692.5, 4.6))],
    "BF1": [(1, (684.4, 630.4, 9.3)), (1, (684.4, 643.6, 9.3))],
    "BB3": [(8, (888.5, 692.5, 1.2)), (6, (889.6, 683.0, 5.6)), (5, (895.0, 680.2, 3.0))],
}
CAPS = {"BX1": "Package boiler AB-1", "BH2": "HRSG duct-burner skid", "BF1": "HRSG feed pumps, 13.8 kV",
        "BB3": "Outage cable work, HRSG 3"}


def cams(keys=None):
    import re
    txt = open(os.path.join(HERE, "pro_look.py")).read()
    out = {}
    for k in keys or SPOTS:
        m = re.search(r'k="%s".*?eye=\(([^)]*)\), target=\(([^)]*)\), lens=([\d.]+)' % k, txt, re.S)
        out[k] = dict(eye=[float(v) for v in m.group(1).split(",")], target=[float(v) for v in m.group(2).split(",")],
                      lens=float(m.group(3)), res=(1920, 1080))
    return out


def slide3():
    C = cams()
    W, H, G, X0, TOP = 314, 150, 18, 64, 150
    tiles = ""
    for k, view in enumerate(SPOTS):
        x = X0 + k * (W + G)
        dots = ""
        for (n, p) in SPOTS[view]:
            u, v = bz.project(C[view], p)
            sc = W / 1920                                                   # object-fit: cover crops top and bottom
            px, py = u * sc, v * sc - (1080 * sc - H) / 2
            px, py = min(max(px, 15), W - 15), min(max(py, 15), H - 15)
            dots += (f'<div class="abs" style="left:{px - 13:.1f}px;top:{py - 13:.1f}px;width:26px;height:26px;'
                     f'border-radius:13px;border:2.5px solid {COPPER};background:rgba(14,16,18,.72);'
                     f'font:800 14px/21px BC;color:{WHITE};text-align:center">{n}</div>')
        tiles += f"""
  <div class="abs" style="left:{x}px;top:{TOP}px;width:{W}px;height:{H}px;overflow:hidden">
    <img src="{img(view)}" style="width:100%;height:100%;object-fit:cover">{dots}</div>
  <div class="abs cap" style="left:{x}px;top:{TOP + H + 6}px;width:{W}px">{CAPS[view]}</div>"""
    rows = ""
    for (n, name, cons, use, spec, stock, size, link) in PRODUCTS:
        st = f"{stock}<span class='sz'>{(' &middot; ' + size) if size else ''}</span>"
        short = link.split("//", 1)[1].split("/")[0].replace("www.", "")
        rows += f"""<tr><td><span class="nb">{n}</span></td><td><div class="pn">{name}</div><div class="pc">{cons}</div></td>
          <td class="pu">{use}</td><td class="ps">{spec}</td><td class="ps">{st}</td>
          <td><a href="{link}">{short} &rsaquo;</a></td></tr>"""
    return f"""
<section class="page slide">
  <style>
    table.p {{ border-collapse: collapse; width: 1312px; }}
    table.p th {{ font: 700 11.5px/1 BC; letter-spacing: .14em; color: {GREY}; text-transform: uppercase; text-align: left;
                 padding: 0 8px 7px; }}
    table.p td {{ padding: 3px 8px; border-top: 1px solid #2c3036; vertical-align: middle; }}
    .nb {{ display: inline-block; width: 24px; height: 24px; border-radius: 12px; border: 2.5px solid {COPPER};
           font: 800 13px/19px BC; color: {WHITE}; text-align: center; }}
    .pn {{ font: 800 15.5px/1.05 BC; color: {WHITE}; text-transform: uppercase; letter-spacing: .03em; }}
    .pc {{ font: 400 10.5px/1.25 B; color: {GREY}; margin-top: 1px; }}
    .pu {{ font: 400 12.5px/1.3 B; color: {WHITE}; }}
    .ps {{ font: 700 15px/1.1 BC; color: {COPPER}; letter-spacing: .04em; white-space: nowrap; }}
    .sz {{ font: 400 11px/1 B; color: {GREY}; letter-spacing: 0; }}
    table.p a {{ font: 700 12.5px/1 BC; letter-spacing: .06em; color: {COPPER_L}; text-decoration: none; }}
  </style>
  <div class="abs kicker" style="left:64px;top:52px">Boiler solutions &nbsp;&middot;&nbsp; the offering</div>
  <div class="abs h2" style="left:62px;top:80px;font-size:52px">The cable at <em>every spot</em></div>
  {tiles}
  <table class="p abs" style="left:64px;top:{TOP + H + 26}px">
    <tr><th></th><th>Product</th><th>Where it runs</th><th>SPEC</th><th>Southwire stock # &middot; size</th><th>Spec sheet</th></tr>
    {rows}</table>
  <div class="abs cap" style="left:64px;top:735px;width:1312px">Stock numbers are one catalogue size per product, from
    Southwire's product listings; every size and construction is on the same SPEC. Confirm current stock with Southwire
    customer service before quoting.</div>
  {foot(11)}
</section>"""


# ------------------------------------------------------------------------------- slide: interconnection to the HRSG
# The ISO1 render (plant faded to clay, HRSG trains in their own finish, cables glowing) with the model's routed cable
# paths (brochure/cables_xray.json, written by cable_schedule.py) drawn over it by voltage class, and numbered spots.
XCOL = {'HV 230 kV': '#b06ae0', 'MV 35 kV': '#e0503a', 'MV 25 kV': '#e86a2c', 'MV 15 kV': '#f05a28', 'MV 5 kV': '#f2892e',
        'LV 600 V': '#f2c613', 'DC 2 kV': '#17a589', 'Portable MV': '#f7b733', 'Portable LV': '#a3b1b8', 'Control': '#3a8fd9',
        'Instrumentation': '#36c26b', 'Fire alarm': '#ff3d7f', 'Fibre / data': '#ff9f1a'}
ISO_SPOTS = [(1, "GSUs and 230 kV ties", "step-up transformers, the lines to the switchyard", (790, 345, 36)),
             (2, "Generators and 21 kV bus", "IPB, unit aux transformers, excitation", (790, 432, 40)),
             (3, "Gas turbines", "instrument, control and aux power on every unit", (790, 497, 40)),
             (4, "Hall MV and LV trays", "13.8 kV feeders, MCC power, control", (880, 520, 48)),
             (5, "HRSG trains", "feed pumps, duct burners, drums, SCR, CEMS", (790, 690, 100)),
             (6, "HRSG e-houses", "MCCs and DCS I/O per unit", (568, 632, 16)),
             (7, "Main cable rack", "MV, LV, control and fibre to the units", (880, 838, 44))]


def slide_iso():
    import math as _m
    X = json.load(open(os.path.join(PLANT, "brochure", "cables_xray.json")))
    cam = dict(cams(["ISO1"])["ISO1"], res=(1440, 810))
    P = lambda p: bz.project(cam, p)
    best, count = {}, {}
    for r in X["cables"]:
        pi = r[12]
        if pi is None or pi < 0:
            continue
        best[pi] = min(best.get(pi, 99), r[1])
        count[pi] = count.get(pi, 0) + r[5]
    used, paths = set(), []
    for pi in sorted(best, key=lambda q: -best[q]):
        pts = X["paths"][pi]
        xyz = [pts[i:i + 3] for i in range(0, len(pts) - 2, 3)]
        if not any(380 < q[0] < 1520 and -10 < q[1] < 880 for q in xyz):           # the power block and the switchyard
            continue
        pp = [P(q) for q in xyz]
        if not any(0 <= a <= 1440 and 0 <= b <= 810 for a, b in pp):
            continue
        cls = X["classes"][best[pi]]
        used.add(cls)
        sw = min(2.8, .7 + .16 * _m.sqrt(count[pi]))
        d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pp)
        paths.append(f'<path d="{d}" stroke="{XCOL[cls]}" stroke-width="{sw:.2f}"/>')
    svg_paths = "".join(paths)
    spots = ""
    for (n, t, sub, p) in ISO_SPOTS:
        u, v = P(p)
        spots += (f'<div class="abs" style="left:{u - 17:.0f}px;top:{v - 17:.0f}px;width:34px;height:34px;border-radius:17px;'
                  f'border:3px solid {COPPER};background:rgba(14,16,18,.82);font:800 18px/28px BC;color:{WHITE};'
                  f'text-align:center;box-shadow:0 0 0 4px rgba(227,154,95,.25)">{n}</div>')
    items = "".join(f'<div class="li" style="padding:7px 0 8px 34px;font-size:13px"><span class="abs" style="left:0;top:7px;'
                     f'width:24px;height:24px;border-radius:12px;border:2.5px solid {COPPER};font:800 13px/19px BC;color:{WHITE};'
                     f'text-align:center">{n}</span><b style="font-size:15px">{t}</b><br>{sub}</div>'
                     for (n, t, sub, p) in ISO_SPOTS).replace('.li:before', '')
    leg = "".join(f'<span style="display:inline-flex;align-items:center;margin:0 12px 6px 0" class="cap">'
                  f'<span style="width:18px;height:4px;border-radius:2px;background:{c};margin-right:6px"></span>{k}</span>'
                  for k, c in XCOL.items() if k in used)
    h = N["hrsg"]
    return f"""
<section class="page slide">
  <style> .iso .li:before {{ display: none; }} </style>
  <img class="abs" src="{img('ISO1')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  <svg class="abs" width="1440" height="810" viewBox="0 0 1440 810" style="left:0;top:0">
    <defs><filter id="gl" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="3.2"/></filter></defs>
    <g fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".4" filter="url(#gl)">{svg_paths}</g>
    <g fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".82">{svg_paths}</g>
  </svg>
  {spots}
  <div class="abs" style="left:0;top:0;width:1440px;height:200px;background:linear-gradient(180deg,rgba(14,16,18,.92) 0%,
       rgba(14,16,18,.6) 60%,rgba(14,16,18,0) 100%)"></div>
  <div class="abs" style="left:1050px;top:0;width:390px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,0) 0%,
       rgba(14,16,18,.88) 18%,rgba(14,16,18,.94) 100%)"></div>
  <div class="abs kicker" style="left:64px;top:46px">Boiler solutions &nbsp;&middot;&nbsp; turbines to boilers</div>
  <div class="abs h2" style="left:62px;top:74px;font-size:50px">From the interconnection <em>to the HRSG</em></div>
  <div class="abs lede" style="left:64px;top:130px;width:960px;font-size:15px">Every routed cable in the model from the
    230 kV ties through the opened turbine hall to the boilers, by voltage class. Turbines and HRSG trains in full; the rest faded.</div>
  <div class="abs iso" style="left:1100px;top:118px;width:290px">{items}</div>
  <div class="abs" style="left:1100px;top:560px;width:290px">
    <div class="big" style="font-size:38px">{h['cables']:,}</div><div class="bigl" style="margin-top:4px">cables per HRSG train</div>
    <div class="big" style="font-size:38px;margin-top:12px">{kft(h['ft'])}</div><div class="bigl" style="margin-top:4px">ft of cable per train</div></div>
  <div class="abs" style="left:0;top:660px;width:1100px;height:150px;background:linear-gradient(180deg,rgba(14,16,18,0) 0%,
       rgba(14,16,18,.85) 45%,rgba(14,16,18,.92) 100%)"></div>
  <div class="abs" style="left:64px;top:724px;width:980px">{leg}</div>
  {foot(2)}
</section>"""


# ------------------------------------------------------------------------------- HRSG hero (iso) and elevation slides
# HRSG 1 train in its own finish, every cable glowing copper / amber, the rest of the plant faded (ISO1 / ELV1 in
# pro_look.py, ghost view of the render script). Numbered details are placed from the model's coordinates; the number
# after each detail points to the product on the offering slide.
HERO_SPOTS = [(1, "Feed pumps, 13.8 kV", "MV terminal boxes off the drop tray", "1", (684.4, 637, 9)),
              (2, "Duct burner", "gas header, 8 runners, igniters and flame scanners", "5 · 6", (664.6, 636, 46)),
              (3, "Duct-burner skid and BMS", "double block and bleed, Class I Div 2", "3 · 5", (683, 695, 4)),
              (4, "Drums and roof valves", "drum-level transmitters, motor-operated stop valves", "2 · 6", (662.6, 700, 92)),
              (5, "Riser tray to the roof", "control, instrument and thermocouple cable", "5 · 6 · 7", (670.3, 626, 82)),
              (6, "Chemical feed", "metering-pump motors", "2", (683, 674, 6)),
              (7, "SCR dilution-air blowers", "480 V motors", "2 · 4", (687, 715, 5)),
              (8, "CEMS shelter", "analyzers and stack probes", "6", (656, 813, 8))]
ELEV_SPOTS = [(1, "HRSG e-house R2A", "MCCs and DCS I/O for the unit", "2 · 5", (568, 632, 10)),
              (2, "EL 42 control tray", "into the west-wall marshalling box", "5 · 6", (595.6, 690, 41)),
              (3, "Ammonia injection grid", "AIG header and lances, SCR", "5 · 6", (594.8, 664, 55)),
              (4, "Blowdown tank", "level and valve control", "5 · 6", (582, 710, 12)),
              (5, "Drums and roof valves", "level transmitters, MOVs", "2 · 6", (630, 700, 96)),
              (6, "Stack and CEMS ports", "sample lines, probes", "6", (630, 790, 120)),
              (7, "GT exhaust to the HRSG", "inlet duct thermocouples", "7", (630, 548, 34))]


def spot_html(cam, spots, r=17):
    out = ""
    for (n, t, sub, prod, p) in spots:
        u, v = bz.project(cam, p)
        u, v = min(max(u, 24), 1036), min(max(v, 24), 786)
        out += (f'<div class="abs" style="left:{u - r:.0f}px;top:{v - r:.0f}px;width:{2 * r}px;height:{2 * r}px;'
                f'border-radius:{r}px;border:3px solid {COPPER};background:rgba(14,16,18,.84);font:800 18px/{2 * r - 6}px BC;'
                f'color:{WHITE};text-align:center;box-shadow:0 0 0 5px rgba(227,154,95,.28)">{n}</div>')
    return out


APPNAME = {"1": "MV-105 15 kV", "2": "TC-ER power", "3": "ARMOR-X MC-HL", "4": "MC-HL VFD", "5": "Control TC-ER",
           "6": "Instrumentation PLTC", "7": "Thermocouple ext.", "—": "XHHW-2 1/C 500 kcmil"}


def apps(prod):
    """The cable applications behind a spot's product numbers, named (numbers as on the offering slide)."""
    return " &nbsp;".join(f'<span style="color:{COPPER}">{APPNAME[k]}</span>'
                          + (f'<sup style="font-size:9px;color:{GREY}"> {k}</sup>' if k != "—" else "")
                          for k in prod.split(" · "))


def spot_list(spots):
    return "".join(
        f'<div style="position:relative;padding:6px 0 7px 36px;border-top:1px solid #2c3036">'
        f'<span class="abs" style="left:0;top:8px;width:25px;height:25px;border-radius:13px;border:2.5px solid {COPPER};'
        f'font:800 13px/20px BC;color:{WHITE};text-align:center">{n}</span>'
        f'<div style="font:800 15px/1.1 BC;color:{WHITE};text-transform:uppercase;letter-spacing:.03em">{t}</div>'
        f'<div style="font:400 11.5px/1.3 B;color:{GREY};margin-top:2px">{sub}</div>'
        f'<div style="font:700 11.5px/1.25 BC;letter-spacing:.04em;margin-top:2px">{apps(prod)}</div></div>'
        for (n, t, sub, prod, p) in spots)


def panel(kicker, title, lede, spots, extra=""):
    return f"""
  <div class="abs" style="left:1040px;top:0;width:400px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,0) 0%,
       rgba(14,16,18,.9) 12%,rgba(14,16,18,.96) 100%)"></div>
  <div class="abs kicker" style="left:1086px;top:46px;font-size:12px">{kicker}</div>
  <div class="abs h2" style="left:1084px;top:70px;font-size:40px;width:300px">{title}</div>
  <div class="abs lede" style="left:1086px;top:168px;width:300px;font-size:13px">{lede}</div>
  <div class="abs" style="left:1086px;top:{262}px;width:300px">{spots}</div>
  {extra}"""


def slide_hero():
    cam = dict(cams(["ISO1"])["ISO1"], res=(1440, 810))
    h = N["hrsg"]
    lede = ("One HRSG train and everything wired to it: cable in copper (MV) and amber (LV, control, instruments), "
            "the rest of the plant faded.")
    extra = f"""<div class="abs" style="left:48px;top:640px;display:flex;gap:28px;padding:14px 20px;background:rgba(14,16,18,.82);border-radius:4px">
      <div><div class="big" style="font-size:30px">{h['cables']:,}</div><div class="bigl">cables / train</div></div>
      <div><div class="big" style="font-size:30px">{kft(h['ft'])}</div><div class="bigl">ft / train</div></div></div>"""
    return f"""
<section class="page slide">
  <img class="abs" src="{img('ISO1')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  {spot_html(cam, HERO_SPOTS)}
  {panel("Boiler solutions &nbsp;&middot;&nbsp; HRSG", "The HRSG, <em>every cable</em>", lede, spot_list(HERO_SPOTS).replace("padding:6px 0 7px 36px", "padding:4px 0 5px 36px"), extra).replace("top:262px", "top:222px")}
  <div class="abs" style="left:0;top:730px;width:1040px;height:80px;background:linear-gradient(180deg,rgba(14,16,18,0),rgba(14,16,18,.95) 55%)"></div>
  {foot(4).replace("right:64px", "right:420px")}
</section>"""


def slide_elev():
    cam = dict(cams(["ELV1"])["ELV1"], res=(1440, 810))
    P = lambda p: bz.project(cam, p)
    scale = ""
    x0 = P((552, 600, 0))[0] - 40
    for (z, lab) in ((0, "GRADE"), (42, "EL 42 &middot; control tray"), (86, "EL 86 &middot; casing roof"), (180, "EL 180 &middot; stack top")):
        u, v = P((552, 600, z)) if z < 150 else P((630, 790, z))
        scale += (f'<div class="abs" style="left:24px;top:{v:.0f}px;width:{max(60, u - 24):.0f}px;border-top:1px dashed rgba(227,154,95,.75)"></div>'
                  f'<div class="abs" style="left:24px;top:{v - 20:.0f}px;font:700 11px/1 BC;letter-spacing:.12em;color:{WHITE};'
                  f'background:rgba(14,16,18,.78);padding:4px 7px 3px">{lab}</div>')
    lede = ("The same train at a low angle from the west: e-house, the tray into the marshalling box, the ammonia grid, "
            "drums and stack. Cable in copper and amber, the rest faded.")
    return f"""
<section class="page slide">
  <img class="abs" src="{img('ELV1')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  {scale}
  {spot_html(cam, ELEV_SPOTS)}
  {panel("Boiler solutions &nbsp;&middot;&nbsp; elevation", "The train <em>in elevation</em>", lede, spot_list(ELEV_SPOTS))}
  <div class="abs" style="left:0;top:730px;width:1040px;height:80px;background:linear-gradient(180deg,rgba(14,16,18,0),rgba(14,16,18,.95) 55%)"></div>
  {foot(5).replace("right:64px", "right:420px")}
</section>"""


# ------------------------------------------------------------------------------- the wiring diagram (one-line / riser)
# Every leg from the switchgear room to the field, read from the Cable Schedule sheet (run length as the workbook's
# formula: ROUNDUP((route + drops + 2 x 10 ft) x 1.1, -10) x sets x cables per set):
# - the HRSG 1 train (HRSG 1, its feed pumps, SCR blowers, chemical feed, blowdown, CEMS, duct burner): 705 cables;
# - what feeds the room: the T-R2A 13.8 kV primary, its 480 V secondary into LC-R2A, the transformer's own fans,
#   controls and monitoring, the DCS fibre from the control room and the e-house's own wiring. R2A also serves the
#   GT1 unit loads, so these legs are shown but kept out of the train total.
TRAIN = r"HRSG[- ]1\b|BFP-1|SCRB-1|CEMS-1|STK-1|HRSG 1 "


def legs():
    import math
    import re
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(PLANT, "brochure", "SW-3X1_Cable_Schedule_and_BOM.xlsx"), read_only=True)
    rm = {r[0]: r[1] for r in wb["Read Me"].iter_rows(min_row=12, max_row=13, values_only=True)}
    allow, end = float(list(rm.values())[0]), float(list(rm.values())[1])
    out = {}

    def put(k, r):
        n = r[13] * r[14]
        ft = math.ceil(((r[19] or 0) + (r[20] or 0) + 2 * end) * (1 + allow) / 10) * 10 * n
        a = out.setdefault(k, dict(cables=0, ft=0, rows=[]))
        a["cables"] += n
        a["ft"] += ft
        a["rows"].append(r[0])
    for r in list(wb["Cable Schedule"].iter_rows(values_only=True))[1:]:
        ends = " ".join(str(r[k]) for k in (4, 5, 6, 7))
        svc, cls, prod = str(r[3]), r[8], str(r[9])
        if "T-R2A unit / load-centre transformer primary" in svc:
            put("primary", r)
        elif svc.startswith("T-R2A 480 V secondary"):
            put("secondary", r)
        elif "T-R2A" in ends:
            put("traux", r)
        elif r[4] == "CR" and r[6] == "R2A":
            put("fibre_r2a", r)
        elif r[4] == "R2A" and r[6] == "R2A":
            put("room_bw" if cls == "Building wire" else "room", r)
        elif re.search(TRAIN, ends):
            k = {"MV 15 kV": "mv", "LV 600 V": "lv", "Control": "ctrl"}.get(cls)
            if cls == "Instrumentation":
                k = "tcx" if "Thermocouple" in prod else "inst"
            put(k or "misc", r)
    return out


L = legs()
_train = sum(L[k]["cables"] for k in ("mv", "lv", "ctrl", "inst", "tcx", "misc"))
assert _train == N["hrsg"]["cables"], (_train, N["hrsg"]["cables"])     # same train as the hero slide
SUPPLY = [  # (key, label, colour, product, field)
    ("primary", "MV-105 15 kV", "#f05a28", "1", "SWGR-13.8-1 to T-R2A, 13.8 kV primary"),
    ("secondary", "XHHW-2 1/C 500 kcmil", "#f2c613", "—", "T-R2A 480 V secondary into LC-R2A, 10 sets x 4"),
    ("traux", "TC-ER power · control · PLTC", "#9aa3ab", "2 · 5 · 6", "T-R2A fans, controls, temperature / gas monitoring"),
    ("fibre_r2a", "Fibre", "#ff9f1a", "—", "Control room to the R2A DCS network cabinet"),
    ("room_bw", "SIMpull THHN · building wire", "#c58bff", "—", "Lighting, receptacles, small power inside R2A"),
    ("room", "TC-ER · FPLR", "#c58bff", "2 · 5", "Panel feeder, control and fire-alarm loop inside R2A"),
]
APP = [  # (key, application, colour, product numbers, field)
    ("mv", "MV-105 15 kV", "#f05a28", "1", "Feed pumps BFP-1A / 1B, 13.8 kV"),
    ("lv", "TC-ER 600 V power · VFD", "#f2c613", "2 · 4", "Motors, MOVs, heaters: SCR blowers, chemical feed, blowdown, CEMS"),
    ("ctrl", "Control TC-ER · ARMOR-X MC-HL", "#3a8fd9", "5 · 3", "Valves, MOVs, burner management, local stations"),
    ("inst", "Instrumentation PLTC / ITC · RTD", "#36c26b", "6", "Field junction boxes to transmitters, flame scanners, RTDs"),
    ("tcx", "Thermocouple extension", "#17a589", "7", "Gas-path, tube-metal and duct thermocouples"),
    ("misc", "Fibre · fire alarm · THHN", "#ff9f1a", "—", "CEMS shelter: data to the control room, detection, lighting"),
]

# the e-house cutaway (RA1): each leg where it runs in the room
ROOM_SPOTS = [
    (1, "13.8 kV primary", "MV-105 off the EL 36 tray into T-R2A", "1", (561.0, 677.4, 14)),
    (2, "480 V secondary", "10 sets of 4 x 1/C 500 kcmil", "—", (560.0, 657.5, 12.7)),
    (3, "Main breaker", "the 40 cables drop into LC-R2A", "—", (582.0, 649.6, 11.2)),
    (4, "LC-R2A feeders", "to MCCs, VFDs, UPS and panels", "2", (580.4, 638.0, 11.0)),
    (5, "MCC drops", "power and control into each bucket", "2 · 5", (582.0, 620.0, 11.0)),
    (6, "VFD and MCC-2", "SCR blowers, chemical feed, blowdown", "2 · 4", (569.9, 628.0, 11.2)),
    (7, "Marshalling", "home-run multipairs from the field JBs", "6 · 7", (566.5, 636.0, 11.6)),
    (8, "Out to the field", "power via the north wall, instruments via the roof", "2 · 5 · 6", (575.75, 644.0, 13.4)),
    (9, "UPS, DC and panels", "125 V DC, 120 V AC UPS, lighting", "2 · 5", (553.6, 630.0, 9.0)),
]


def slide_room():
    cam = dict(cams(["RA1"])["RA1"], res=(1440, 810))
    lab = {1: "primary", 2: "secondary"}
    spots = []
    for (n, t, sub, prod, p) in ROOM_SPOTS:
        if n in lab:
            sub += f" &middot; {L[lab[n]]['cables']} cables, {L[lab[n]]['ft']:,} ft"
        spots.append((n, t, sub, prod, p))
    inset = os.path.join(PLANT, "renders", "boilers_full", "RA2_pro_clean.jpg")
    inset = url(inset if os.path.exists(inset) else os.path.join(R, "RA2_pro_clean.jpg"))
    lede = "Roof and two walls lifted off the HRSG 1 e-house: every cable leg, transformer to section."
    extra = f"""<div class="abs" style="left:40px;top:560px;width:340px;height:192px;border:2px solid {COPPER};border-radius:4px;overflow:hidden">
      <img src="{inset}" style="width:100%;height:100%;object-fit:cover;display:block"></div>
      <div class="abs cap" style="left:40px;top:540px;width:360px;font-size:10.5px;color:#fff;text-shadow:0 1px 3px #000">Inside: LC-R2A and MCC-R2A-1 (right), VFDs (left), trays overhead</div>"""
    return f"""
<section class="page slide">
  <img class="abs" src="{img('RA1')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  {spot_html(cam, spots)}
  {panel("Boiler solutions &nbsp;&middot;&nbsp; the e-house", "Inside <em>the room</em>", lede, spot_list(spots).replace("padding:6px 0 7px 36px", "padding:4px 0 5px 36px"), extra).replace("top:262px", "top:218px").replace("top:168px", "top:160px")}
  <div class="abs" style="left:0;top:730px;width:1040px;height:80px;background:linear-gradient(180deg,rgba(14,16,18,0),rgba(14,16,18,.95) 55%)"></div>
  {foot(6).replace("right:64px", "right:420px")}
</section>"""


def slide_diagram():
    epic = lambda k: url(os.path.join(PLANT, "renders", "epic", f"{k}_pro_clean.jpg"))
    X_SW0, X_SW1, Y_SW0, Y_SW1 = 190, 410, 176, 436                    # R1 switchgear room node
    X_E0, X_E1, Y_E0, Y_E1 = 600, 850, 250, 556                        # R2A e-house node
    XF0, XF1 = 1006, 1376                                               # field column
    rows = [176 + 64 * k for k in range(7)]
    lines, nodes = "", ""

    def wire(pts, col, w=4):
        return (f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="{w}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')
    tag = lambda x, y, txt, col: (f'<div class="abs" style="left:{x}px;top:{y}px;font:700 11px/1 BC;letter-spacing:.05em;'
                                  f'color:{INK};background:{col};padding:4px 7px 3px;border-radius:3px;white-space:nowrap">{txt}</div>')
    fmt = lambda k: f"{L[k]['cables']} CABLES &middot; {L[k]['ft']:,} FT"
    # generator -> switchgear
    lines += wire([(160, 296), (X_SW0, 296)], "#b06ae0", 5)
    # switchgear -> feed pumps (field row 0)
    lines += wire([(X_SW1, rows[0] + 18), (XF0, rows[0] + 18)], APP[0][2], 5)
    nodes += tag(470, rows[0] + 4, f"MV-105 15 KV &middot; {fmt('mv')} &middot; 1", APP[0][2])
    # switchgear -> T-R2A (primary) -> R2A (secondary)
    lines += wire([(X_SW1, 382), (500, 382), (500, 452), (522, 452)], SUPPLY[0][2], 5)
    nodes += tag(420, 396, f"PRIMARY &middot; MV-105 &middot; {fmt('primary')}", SUPPLY[0][2])
    lines += wire([(572, 452), (X_E0, 452)], SUPPLY[1][2], 7)
    nodes += tag(330, 492, f"SECONDARY &middot; 1/C 500 KCMIL &middot; {fmt('secondary')}", SUPPLY[1][2])
    nodes += (f'<div class="abs" style="left:522px;top:424px;width:50px;height:56px;border:2px solid {GREY};border-radius:25px;'
              f'background:#15181b;font:800 10px/1.1 BC;color:{WHITE};text-align:center;padding-top:11px">T-R2A<br>'
              f'<span style="font-weight:700;color:{GREY}">13.8/<br>0.48</span></div>')
    # T-R2A aux leg
    lines += wire([(547, 480), (547, 600), (XF0 - 60, 600), (XF0 - 60, rows[5] + 18), (XF0, rows[5] + 18)], SUPPLY[2][2], 3)
    # e-house -> field rows 1-4
    for k in range(1, 5):
        y = rows[k] + 18
        ys = 290 + (k - 1) * 40
        lines += wire([(X_E1, ys), (930 + 8 * k, ys), (930 + 8 * k, y), (XF0, y)], APP[k][2], 4)
    # control room: fibre to R2A and to CEMS (row 6)
    lines += wire([(410, 650), (725, 650), (725, Y_E1)], SUPPLY[3][2], 3)
    nodes += tag(470, 658, f"DCS FIBRE &middot; {fmt('fibre_r2a').replace('1 CABLES', '1 CABLE')}", SUPPLY[3][2])
    lines += wire([(410, 640), (980, 640), (980, rows[6] + 18), (XF0, rows[6] + 18)], APP[5][2], 3)
    # source node
    nodes += (f'<div class="abs" style="left:40px;top:264px;width:120px;height:64px;border:2px solid #b06ae0;border-radius:6px;'
              f'padding:9px 10px;background:rgba(176,106,224,.08)"><div class="ct" style="font-size:15px">GSU-1 &middot; UAT-1</div>'
              f'<div class="cd" style="font-size:11px">21 / 13.8 kV</div></div>')
    # switchgear room node with the render
    nodes += (f'<div class="abs" style="left:{X_SW0}px;top:{Y_SW0}px;width:{X_SW1 - X_SW0}px;height:{Y_SW1 - Y_SW0}px;'
              f'border:2px solid {COPPER};border-radius:6px;overflow:hidden;background:#15181b">'
              f'<img src="{epic("E82")}" style="width:100%;height:140px;object-fit:cover;display:block">'
              f'<div style="padding:10px 12px"><div class="cnum">Switchgear room R1</div>'
              f'<div class="ct" style="font-size:19px;margin-top:5px">SWGR-13.8-1</div>'
              f'<div class="cd" style="font-size:11.5px;margin-top:4px">13.8 kV metal-clad: the feed-pump breakers and the '
              f'T-R2A transformer feeder</div></div></div>')
    # e-house node with the cutaway render and the room's own wiring
    nodes += (f'<div class="abs" style="left:{X_E0}px;top:{Y_E0}px;width:{X_E1 - X_E0}px;height:{Y_E1 - Y_E0}px;'
              f'border:2px solid {COPPER};border-radius:6px;overflow:hidden;background:#15181b">'
              f'<img src="{img("RA1")}" style="width:100%;height:126px;object-fit:cover;display:block">'
              f'<div style="padding:9px 12px"><div class="cnum">HRSG e-house R2A</div>'
              f'<div class="ct" style="font-size:18px;margin-top:4px">LC-R2A &middot; MCCs &middot; VFDs &middot; DCS</div>'
              f'<div class="cd" style="font-size:11px;margin-top:3px">480 V switchgear, starters, drives, UPS / DC, marshalling</div>'
              f'<div style="font:400 10.5px/1.35 B;color:{GREY};margin-top:6px;border-top:1px solid #2c3036;padding-top:5px">'
              f'<span style="color:{SUPPLY[4][2]};font-weight:700">In the room:</span> lighting and receptacles, '
              f'{L["room_bw"]["ft"]:,} ft THHN; panel feeder, control, fire-alarm loop, {L["room"]["ft"]:,} ft</div></div></div>')
    # control room node
    nodes += (f'<div class="abs" style="left:190px;top:618px;width:220px;height:52px;border:2px solid {APP[5][2]};border-radius:6px;'
              f'padding:8px 12px;background:#15181b"><div class="ct" style="font-size:15px">Main control room</div>'
              f'<div class="cd" style="font-size:11px">DCS servers, CEMS data</div></div>')
    # field nodes: rows 0-4 = train, 5 = T-R2A aux, 6 = CEMS fibre / FA / THHN
    fr = [APP[0], APP[1], APP[2], APP[3], APP[4], SUPPLY[2], APP[5]]
    for k, (key, app, col, prod, field) in enumerate(fr):
        y = rows[k]
        nodes += (f'<div class="abs" style="left:{XF0}px;top:{y}px;width:{XF1 - XF0}px;height:56px;border-left:5px solid {col};'
                  f'background:#15181b;padding:6px 12px 5px">'
                  f'<div style="font:800 14px/1.1 BC;color:{WHITE};text-transform:uppercase;letter-spacing:.03em">{field}</div>'
                  f'<div style="font:400 11px/1.3 B;color:{GREY};margin-top:3px"><span style="color:{col};font-weight:700">{app}</span>'
                  f' &middot; {L[key]["cables"]:,} cables &middot; {L[key]["ft"]:,} ft &nbsp;<span style="font:700 12px/1 BC;color:{COPPER}">{prod}</span></div></div>')
    # exploded breakdown: the train by application, then what feeds the room
    tr = [(a[1], a[2], L[a[0]]["ft"]) for a in APP]
    su = [(a[1], a[2], L[a[0]]["ft"]) for a in SUPPLY]
    t_tr, t_su = sum(f for *_, f in tr), sum(f for *_, f in su)
    bars = ""
    x = 64
    W = 1312 - 12
    for grp in (sorted(tr, key=lambda a: -a[2]), sorted(su, key=lambda a: -a[2])):
        for (app, col, ft) in grp:
            w = W * ft / (t_tr + t_su)
            lab = f"{app.split(' ·')[0]} {ft / 1000:,.1f}k" if w > 130 else (f"{ft / 1000:,.1f}k" if w > 34 else "")
            bars += (f'<div class="abs" style="left:{x:.1f}px;top:714px;width:{max(w - 2, 1.5):.1f}px;height:28px;background:{col};'
                     f'font:700 11.5px/28px BC;letter-spacing:.05em;color:{INK};padding-left:7px;overflow:hidden;white-space:nowrap">'
                     f'{lab}</div>')
            x += w
        x += 12
    n_su = sum(L[a[0]]["cables"] for a in SUPPLY)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:52px">Boiler solutions &nbsp;&middot;&nbsp; how it is wired</div>
  <div class="abs h2" style="left:62px;top:80px;font-size:50px">Switchgear room <em>to the HRSG</em></div>
  <div class="abs lede" style="left:64px;top:136px;width:900px;font-size:14px">Every leg, from the 13.8 kV breaker to the field
    devices, by cable application: Southwire product (numbers as on the offering slide), cable count and footage from the
    model's schedule.</div>
  <svg class="abs" width="1440" height="810" viewBox="0 0 1440 810" style="left:0;top:0">{lines}</svg>
  {nodes}
  <div class="abs kicker" style="left:64px;top:690px;font-size:12px">The HRSG 1 train: {_train:,} cables, ~{round(t_tr, -3):,.0f} ft</div>
  <div class="abs kicker" style="right:64px;top:690px;font-size:12px;color:{GREY};text-align:right">+ feeding the room: {n_su} cables, {t_su:,} ft</div>
  {bars}
  <div class="abs cap" style="left:64px;top:748px;width:1312px">R2A also serves the GT1 unit loads, so the T-R2A primary and
    secondary, the transformer auxiliaries, the DCS fibre and the room's own wiring are shown here but are not in the train total.
    Schedule rows: {", ".join(L["primary"]["rows"] + L["secondary"]["rows"])} and the rest by tag.</div>
  {foot(7)}
</section>"""


# ------------------------------------------------------------------------------- how an HRSG works (basics)
# Typical three-pressure reheat HRSG behind a heavy-duty gas turbine; temperatures and pressures are typical ranges.
SECTIONS = [  # (label, sub, gas temperature after the section, colour, drum, cable at this section)
    ("Duct burner", "supplementary firing", "up to 1,600 °F", "#ff7a3d", None, "MC-HL to the gas train; scanner pairs"),
    ("HP superheater + reheater", "dries and superheats steam", "~1,000 °F", "#f05a28", None, "thermocouple ext., tube metals"),
    ("HP evaporator", "boils water at HP", "~700 °F", "#e39a5f", "HP", "drum level, 2-of-3; MOVs"),
    ("SCR + CO catalyst", "NOx and CO removal", "600-750 °F window", "#b06ae0", None, "blowers on VFDs; AIG valves"),
    ("HP econ. + IP", "preheats HP water; IP steam", "~500 °F", "#3a8fd9", "IP", "MOVs, transmitters"),
    ("LP evaporator", "low-pressure steam", "~320 °F", "#36c26b", "LP", "drum level; LP valves"),
    ("Condensate preheater", "last heat out of the gas", "~180 °F", "#17a589", None, "temperatures; recirc pumps"),
]


def slide_basics():
    X0, Y0, W, H = 64, 214, 1312, 470
    svg = ""
    # gas turbine exhaust and inlet duct (diverging)
    svg += f'<polygon points="{X0},{Y0 + 150} {X0 + 120},{Y0 + 150} {X0 + 180},{Y0 + 70} {X0 + 180},{Y0 + 300} {X0 + 120},{Y0 + 230} {X0},{Y0 + 230}" fill="#2a2f35" stroke="#59606a"/>'
    svg += f'<text x="{X0 + 8}" y="{Y0 + 140}" fill="{GREY}" font-family="BC" font-weight="700" font-size="13" letter-spacing="1">GAS TURBINE EXHAUST</text>'
    svg += f'<text x="{X0 + 8}" y="{Y0 + 196}" fill="{WHITE}" font-family="BC" font-weight="800" font-size="22">~1,100 °F</text>'
    svg += f'<text x="{X0 + 8}" y="{Y0 + 216}" fill="{GREY}" font-family="B" font-size="11">~1,500-2,000 lb/s per gas turbine</text>'
    # sections
    cx0, cw = X0 + 186, 118
    for k, (lab, sub, t, col, drum, cab) in enumerate(SECTIONS):
        x = cx0 + k * (cw + 6)
        svg += f'<rect x="{x}" y="{Y0 + 70}" width="{cw}" height="230" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-width="2"/>'
        for r in range(9):                                                  # tube rows
            svg += f'<line x1="{x + 14 + r * 11}" y1="{Y0 + 84}" x2="{x + 14 + r * 11}" y2="{Y0 + 286}" stroke="{col}" stroke-opacity=".55" stroke-width="2.4"/>'
        svg += (f'<foreignObject x="{x + 4}" y="{Y0 + 196}" width="{cw - 8}" height="100"><div xmlns="http://www.w3.org/1999/xhtml" '
                f'style="background:rgba(14,16,18,.86);padding:5px 6px;font:800 13px/1.05 BC;color:{WHITE};text-transform:uppercase">'
                f'{lab}<div style="font:400 10.5px/1.25 B;color:{GREY};text-transform:none;margin-top:3px">{sub}</div></div></foreignObject>')
        svg += f'<text x="{x + cw / 2}" y="{Y0 + 324}" text-anchor="middle" fill="{COPPER}" font-family="BC" font-weight="800" font-size="15">{t}</text>'
        svg += (f'<foreignObject x="{x - 2}" y="{Y0 + 336}" width="{cw + 4}" height="44"><div xmlns="http://www.w3.org/1999/xhtml" '
                f'style="font:400 10.5px/1.25 B;color:#c9ced3;text-align:center">{cab}</div></foreignObject>')
        if drum:
            dx = x + cw / 2
            svg += f'<rect x="{dx - 44}" y="{Y0 + 16}" width="88" height="30" rx="15" fill="#3c434b" stroke="{WHITE}" stroke-width="1.5"/>'
            svg += f'<text x="{dx}" y="{Y0 + 36}" text-anchor="middle" fill="{WHITE}" font-family="BC" font-weight="800" font-size="14">{drum} DRUM</text>'
            svg += f'<line x1="{dx - 20}" y1="{Y0 + 46}" x2="{dx - 20}" y2="{Y0 + 70}" stroke="{WHITE}" stroke-width="2"/>'
            svg += f'<line x1="{dx + 20}" y1="{Y0 + 46}" x2="{dx + 20}" y2="{Y0 + 70}" stroke="{WHITE}" stroke-width="2"/>'
    # stack
    sx = cx0 + 7 * (cw + 6) + 6
    svg += f'<rect x="{sx}" y="{Y0 - 26}" width="52" height="326" fill="#2a2f35" stroke="#59606a"/>'
    svg += f'<text x="{sx + 26}" y="{Y0 - 34}" text-anchor="middle" fill="{GREY}" font-family="BC" font-weight="700" font-size="13" letter-spacing="1">STACK</text>'
    svg += f'<text x="{sx + 26}" y="{Y0 + 324}" text-anchor="middle" fill="{COPPER}" font-family="BC" font-weight="800" font-size="15">~180 °F</text>'
    svg += (f'<foreignObject x="{sx - 8}" y="{Y0 + 336}" width="72" height="44"><div xmlns="http://www.w3.org/1999/xhtml" '
            f'style="font:400 10.5px/1.25 B;color:#c9ced3;text-align:center">CEMS: analyzers, fibre</div></foreignObject>')
    # gas-flow arrow
    ay = Y0 + 58
    svg += f'<line x1="{X0 + 190}" y1="{ay}" x2="{sx - 12}" y2="{ay}" stroke="{COPPER}" stroke-width="2.5" stroke-dasharray="8 6"/>'
    svg += f'<polygon points="{sx - 12},{ay - 6} {sx},{ay} {sx - 12},{ay + 6}" fill="{COPPER}"/>'
    svg += f'<text x="{X0 + 196}" y="{ay - 8}" fill="{COPPER}" font-family="BC" font-weight="700" font-size="12" letter-spacing="1.5">GAS FLOW, COOLING</text>'
    # water / steam loop (below)
    wy = Y0 + 410
    svg += f'<line x1="{sx + 20}" y1="{wy}" x2="{X0 + 200}" y2="{wy}" stroke="#4aa3ff" stroke-width="3"/>'
    svg += f'<polygon points="{X0 + 200},{wy - 7} {X0 + 186},{wy} {X0 + 200},{wy + 7}" fill="#4aa3ff"/>'
    svg += (f'<text x="{sx + 18}" y="{wy - 10}" text-anchor="end" fill="#4aa3ff" font-family="BC" font-weight="700" font-size="13" '
            f'letter-spacing="1">WATER IN AT THE COLD END (FEED PUMPS) &#8594; ECONOMIZERS &#8594; DRUMS &#8594; EVAPORATORS &#8594; SUPERHEATERS &#8594; STEAM OUT AT THE HOT END</text>')
    svg += (f'<text x="{X0}" y="{wy + 28}" fill="{WHITE}" font-family="B" font-size="13">Steam to the steam turbine, typical: '
            f'<tspan fill="{COPPER}" font-weight="700">HP ~1,800-2,400 psig, ~1,050 °F</tspan> &#183; '
            f'<tspan fill="{COPPER}" font-weight="700">reheat / IP ~400-600 psig, ~1,050 °F</tspan> &#183; '
            f'<tspan fill="{COPPER}" font-weight="700">LP ~50-80 psig</tspan></text>')
    facts = [("~1/3", "of a combined-cycle plant's output comes from HRSG steam, with no extra fuel (duct firing aside)"),
             ("~60 %+", "combined-cycle efficiency, against ~40 % for the gas turbine alone"),
             ("3 x 3", "three pressures, three drums; each drum level measured three ways, typically voted 2-out-of-3"),
             ("~1 hour", "a hot start: about an hour: every start cycles the tubes, which is why tube-metal thermocouples matter")]
    tiles = "".join(f'<div style="flex:1;border-left:3px solid {COPPER};padding:2px 0 2px 12px"><div class="big" style="font-size:28px">'
                    f'{a}</div><div class="cd" style="font-size:11.5px;margin-top:4px">{b}</div></div>' for a, b in facts)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:52px">Boiler solutions &nbsp;&middot;&nbsp; the basics</div>
  <div class="abs h2" style="left:62px;top:80px;font-size:50px">How an HRSG <em>works</em></div>
  <div class="abs lede" style="left:64px;top:136px;width:640px;font-size:13.5px">The exhaust crosses rows of finned tubes, hottest
    sections first; water enters at the cold end and leaves as superheated steam at the hot end. Below each section: the cable it needs.</div>
  <div class="abs" style="left:700px;top:22px;width:676px;border:2px solid {COPPER};border-radius:6px;background:rgba(227,154,95,.07);
       padding:8px 16px 9px;display:flex;gap:22px">
    <div style="flex:1.15"><div class="cnum">What it is</div><ul class="qr">
      <li><b>Without it:</b> ~60 % of the fuel's energy goes up the stack as ~1,100 °F exhaust (~40 % efficient).</li>
      <li><b>With it:</b> a boiler heated by that exhaust; its steam drives the steam turbine.</li>
      <li><b>The payoff:</b> ~1/3 more power from the same fuel (~60 %+ efficient).</li></ul></div>
    <div style="flex:1"><div class="cnum">Fun facts</div><ul class="qr">
      <li>Fuel, CO2 and cost per MWh drop by about a third.</li>
      <li>The NOx catalyst (SCR) lives <b>inside</b> it, where the gas is just the right temperature.</li>
      <li>Duct burners can fire extra gas for peak demand.</li>
      <li style="color:{COPPER}">No HRSG: a gas-turbine plant. With one: combined cycle.</li></ul></div></div>
  <svg class="abs" width="1440" height="810" viewBox="0 0 1440 810" style="left:0;top:0;overflow:visible">{svg}</svg>
  <div class="abs" style="left:64px;top:664px;width:1312px;display:flex;gap:22px">{tiles}</div>
  <div class="abs cap" style="left:64px;top:740px;width:1312px">Typical three-pressure reheat HRSG with SCR behind an H-class
    gas turbine; section order, temperatures and pressures vary by design.</div>
  {foot(2)}
</section>"""


# ------------------------------------------------------------------------------- the whole cycle: what goes in, what comes out
# SW-3X1 is 3 x 1: three H-class gas turbines, three HRSGs, one steam turbine, an 80-cell air-cooled condenser.
# Ratings typical (model info: GTG 350-450 MVA, STG 550-650 MVA, 21 kV, GSUs 21 / 230 kV).
def slide_cycle():
    def box(x, y, w, h, col, title, sub, big=""):
        return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:2px solid {col};border-radius:6px;'
                f'background:#15181b;padding:9px 12px"><div style="font:800 17px/1.05 BC;color:{WHITE};text-transform:uppercase;'
                f'letter-spacing:.03em">{title}</div><div style="font:400 11.5px/1.35 B;color:{GREY};margin-top:4px">{sub}</div>'
                f'{big}</div>')

    def pill(x, y, txt, col, fg=INK):
        return (f'<div class="abs" style="left:{x}px;top:{y}px;font:700 11.5px/1 BC;letter-spacing:.05em;color:{fg};background:{col};'
                f'padding:5px 8px 4px;border-radius:3px;white-space:nowrap;text-transform:uppercase">{txt}</div>')

    def line(pts, col, w=5, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="{w}"'
                f' stroke-linejoin="round"{d} marker-end="url(#ah{col[1:]})"/>')
    cols = {"gas": "#f2c613", "air": "#9aa3ab", "exh": "#ff7a3d", "stm": "#e5484d", "spent": "#8fd3ff", "cond": "#3a8fd9",
            "pwr": "#b06ae0", "heat": "#c9ced3"}
    marks = "".join(f'<marker id="ah{c[1:]}" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto" markerUnits="userSpaceOnUse">'
                    f'<path d="M0,2 L13,8 L0,14 z" fill="{c}"/></marker>' for c in set(cols.values()))
    L_ = ""
    L_ += line([(176, 252), (238, 252)], cols["gas"])                                  # gas in
    L_ += line([(176, 312), (238, 312)], cols["air"])                                  # air in
    L_ += line([(440, 282), (520, 282)], cols["exh"], 9)                               # GT exhaust to HRSG
    L_ += line([(690, 214), (690, 168)], cols["exh"], 6)                               # stack out
    L_ += line([(752, 250), (858, 250)], cols["stm"], 7)                               # steam to ST
    L_ += line([(858, 314), (752, 314)], cols["stm"], 3, "6 5")                        # cold reheat back to the HRSG
    L_ += line([(1062, 280), (1126, 280)], cols["spent"], 9, "10 6")                   # spent steam to ACC
    L_ += line([(1240, 214), (1240, 168)], cols["heat"], 5, "4 6")                     # heat to air
    L_ += line([(1240, 352), (1240, 566), (650, 566), (650, 356)], cols["cond"], 6)    # condensate back to the HRSG
    L_ += line([(1330, 640), (1330, 580), (1252, 580)], cols["cond"], 3, "3 5")        # makeup water
    L_ += line([(338, 336), (338, 396)], cols["pwr"], 4)                               # GT shaft to generator
    L_ += line([(960, 336), (960, 396)], cols["pwr"], 4)                               # ST shaft to generator
    L_ += line([(338, 464), (338, 516), (1060, 516), (1060, 472), (1096, 472)], cols["pwr"], 5)   # power to the GSUs
    L_ += line([(960, 464), (960, 516)], cols["pwr"], 5)
    L_ += line([(1296, 470), (1370, 470)], cols["pwr"], 5)
    nodes = ""
    nodes += box(40, 222, 136, 58, cols["gas"], "Natural gas", "fuel in")
    nodes += box(40, 288, 136, 58, cols["air"], "Air", "drawn in, filtered")
    nodes += box(238, 224, 202, 112, COPPER, "Gas turbines x 3", "H-class: burns gas in compressed air, spins a generator; "
                 "exhaust leaves at ~1,100 °F")
    nodes += box(520, 214, 232, 142, COPPER, "HRSGs x 3", "recover the exhaust heat: water in, steam out at three pressures "
                 "(HP / IP / LP, ~1,050 °F)")
    nodes += box(858, 224, 204, 112, COPPER, "Steam turbine x 1", "steam from all three HRSGs expands through HP, IP and LP "
                 "casings and spins one more generator")
    nodes += box(1126, 214, 230, 138, "#8fd3ff", "Air-cooled condenser", "80 cells, 80 fans: cools the spent steam back into "
                 "water under vacuum")
    for (x, lab) in ((300, "GT generators 21 kV"), (922, "ST generator 21 kV")):
        nodes += (f'<div class="abs" style="left:{x}px;top:400px;width:76px;height:64px;border:2px solid {cols["pwr"]};border-radius:32px;'
                  f'background:#15181b;font:800 22px/60px BC;color:{WHITE};text-align:center">G</div>')
        nodes += f'<div class="abs cap" style="left:{x + 84}px;top:416px;width:110px">{lab}</div>'
    nodes += box(1100, 444, 196, 56, cols["pwr"], "GSUs 21 / 230 kV", "step up to the grid")
    nodes += pill(1100, 506, "Out: electricity to the grid", cols["pwr"], WHITE)
    nodes += pill(604, 136, "Out: stack gas ~180 °F (CO2, water vapour; NOx cut by the SCR)", cols["exh"])
    nodes += pill(1150, 136, "Out: heat to the air", cols["heat"])
    nodes += pill(762, 222, "Steam", cols["stm"], WHITE)
    nodes += pill(764, 322, "Reheat", cols["stm"], WHITE)
    nodes += pill(1052, 302, "Spent steam", cols["spent"])
    nodes += pill(448, 254, "Exhaust", cols["exh"])
    nodes += pill(380, 528, "~2/3 of the output", COPPER)
    nodes += pill(800, 528, "~1/3, from the HRSG steam", COPPER)
    nodes += pill(700, 578, "Condensate pumps return the water to the HRSG's LP end; the 13.8 kV feed pumps lift it to HP / IP", cols["cond"], WHITE)
    nodes += pill(1196, 646, "In: makeup water (small)", cols["cond"], WHITE)
    q = [("Is it still steam?", "Leaving the turbine it is spent steam: ~100-150 °F, below atmospheric pressure, part water "
          "already. The air-cooled condenser turns it back into water."),
         ("A closed loop", "The same water goes round and round: pump, HRSG, turbine, condenser. Only a little makeup water "
          "replaces blowdown losses."),
         ("Where the power comes from", "Fuel is burned only in the gas turbines (and duct burners). The steam turbine adds "
          "about half again on top, from heat that would otherwise go up the stack."),
         ("The cable on the loop", "21 kV isolated-phase bus to the GSUs; MV-105 to the feed pumps; VFD cable to 80 condenser fans; "
          "instruments on every pump, valve and level.")]
    tiles = "".join(f'<div style="flex:1;border-left:3px solid {COPPER};padding:2px 0 2px 12px"><div style="font:800 15px/1.1 BC;'
                    f'color:{WHITE};text-transform:uppercase;letter-spacing:.03em">{a}</div><div class="cd" style="font-size:11.5px;'
                    f'margin-top:4px">{b}</div></div>' for a, b in q)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:52px">Boiler solutions &nbsp;&middot;&nbsp; the whole cycle</div>
  <div class="abs h2" style="left:62px;top:80px;font-size:50px">What goes in, <em>what comes out</em></div>
  <div class="abs lede" style="left:64px;top:136px;width:520px;font-size:13.5px">SW-3X1 is a 3 x 1 combined cycle: three gas
    turbines, three HRSGs, one steam turbine.</div>
  <svg class="abs" width="1440" height="810" viewBox="0 0 1440 810" style="left:0;top:0;overflow:visible"><defs>{marks}</defs>{L_}</svg>
  {nodes}
  <div class="abs" style="left:64px;top:674px;width:1312px;display:flex;gap:22px">{tiles}</div>
  {foot(3)}
</section>"""


# ------------------------------------------------------------------------------- the electrical system: levels and ratings
# Ratings as modelled (typical, not engineered): Load List / Cable Schedule sheets, swgr_rooms.py / r2a_interior.py
# nameplates. Each level with what it is and the cable it drives.
LEVELS = [  # (voltage, colour, equipment and ratings, what it feeds / current, the cable it drives)
    ("230 kV", "#8e98a3", "GSU-1, 21 / 230 kV step-up", "Plant to the grid, overhead line",
     "Overhead conductor (outside the HRSG scope)"),
    ("21 kV", "#b06ae0", "GT1 generator, isolated-phase bus; UAT-1 21 / 13.8 kV, 40 MVA",
     "UAT-1 secondary 1,674 A into SWGR-13.8-1", "4 sets of 3 x 1/C 750 kcmil MV-105"),
    ("13.8 kV", "#f05a28", "SWGR-13.8-1: metal-clad, 1,200 A, 40 kA, arc-resistant",
     "Feed pumps BFP-1A / 1B, 5,000 kW each, direct-on-line, 232 A; T-R2A primary, 105 A",
     "3 x 1/C 250 kcmil MV-105 per pump; 3 x 1/C #2 to T-R2A"),
    ("480 V", "#f2c613", "T-R2A 2,500 kVA &rarr; LC-R2A 4,000 A main, 65 kA &rarr; MCC-R2A-1 / -2, 800 A, 65 kA; VFDs",
     "Secondary 3,007 A; SCR blowers 2 x 110 kW (156 A); 45 HRSG MOVs; feed-pump and chemical-feed auxiliaries; "
     "welding receptacles",
     "10 sets of 4 x 1/C 500 kcmil; 3/0 TC-ER / MC-HL VFD; #10 TC-ER to each MOV"),
    ("120 V AC / 125 V DC", "#3a8fd9", "UPS-R2A 10 kVA; 125 V DC battery, 60 cells; DC and UPS panels",
     "DCS, F&G node, breaker trip and close, burner-management power",
     "1/C #6 and control TC-ER 14 AWG"),
    ("Signals", "#36c26b", "4-20 mA / HART, thermocouple millivolts, 24 V DC discretes",
     "Drum level, pressures, flame scanners, gas-path and tube-metal temperatures",
     "439 instrument + 84 thermocouple-extension cables, shielded pairs"),
]


def slide_system():
    rows = ""
    for (v, col, eq, feeds, cab) in LEVELS:
        rows += (f'<div style="display:flex;align-items:stretch;border-top:1px solid #2c3036;min-height:62px">'
                 f'<div style="width:150px;display:flex;align-items:center"><span style="font:800 16px/1 BC;color:{INK};'
                 f'background:{col};padding:6px 10px 5px;border-radius:3px;letter-spacing:.03em">{v}</span></div>'
                 f'<div style="width:300px;padding:8px 14px 8px 0;font:700 14px/1.25 BC;color:{WHITE};letter-spacing:.02em">{eq}</div>'
                 f'<div style="width:300px;padding:8px 14px 8px 0;font:400 12px/1.35 B;color:{GREY}">{feeds}</div>'
                 f'<div style="flex:1;padding:8px 0;font:700 13px/1.3 BC;color:{COPPER};letter-spacing:.02em">{cab}</div></div>')
    h = N["hrsg"]
    inst = L["inst"]["cables"] + L["tcx"]["cables"]
    inst_ft = L["inst"]["ft"] + L["tcx"]["ft"]
    facts = [
        ("750 kW", "connected at 480 V on one HRSG train, 77 circuits"),
        ("2 x 5 MW", "feed pumps: the largest motors on the train, at 13.8 kV"),
        ("3,007 A", "on the T-R2A secondary: 40 cables of 500 kcmil"),
        (f"{100 * inst / h['cables']:.0f} %", f"of the train's cables are instrument or thermocouple pairs ({100 * inst_ft / h['ft']:.0f} % of the footage)"),
        ("8.4 / 24.6", "cal/cm² arc flash at 13.8 kV / 480 V (equipment labels)"),
    ]
    tiles = "".join(f'<div style="flex:1;border-left:3px solid {COPPER};padding:2px 0 2px 12px"><div class="big" style="font-size:30px">'
                    f'{a}</div><div class="cd" style="font-size:11.5px;margin-top:4px">{b}</div></div>' for a, b in facts)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:52px">Boiler solutions &nbsp;&middot;&nbsp; the electrical system</div>
  <div class="abs h2" style="left:62px;top:80px;font-size:50px">Levels, ratings <em>and the cable they drive</em></div>
  <div class="abs lede" style="left:64px;top:136px;width:1100px;font-size:14px">One HRSG train from the generator down to the
    field signals: each voltage level, the equipment and its rating, what it feeds, and the cable that follows.</div>
  <div class="abs" style="left:64px;top:186px;width:1312px">
    <div style="display:flex;font:700 12px/1.1 BC;letter-spacing:.1em;color:{GREY};text-transform:uppercase;padding-bottom:6px">
      <div style="width:150px">Level</div><div style="width:300px">Equipment &middot; rating</div>
      <div style="width:300px">Feeds &middot; current</div><div style="flex:1">Cable it drives</div></div>{rows}</div>
  <div class="abs" style="left:64px;top:636px;width:1312px;display:flex;gap:22px">{tiles}</div>
  <div class="abs cap" style="left:64px;top:744px;width:1312px">Ratings are the model's typical values (Load List and nameplates),
    not engineered. Real plants vary: many put the feed pumps on a 4.16 or 6.9 kV bus.</div>
  {foot(8)}
</section>"""


# ------------------------------------------------------------------------------- what the spec calls for
# Requirements an owner / EPC cable specification calls up for the HRSG section, per application, and the Southwire
# answer. Sources: references/boilers/README.md (public one-lines, HRSG package spec, sample Division 26 specs, standards).
SPEC = [  # (colour, application, where on the HRSG, what the spec calls for, Southwire answer)
    ("#f05a28", "MV power, 15 kV", "Feed-pump motors; the T-R2A primary",
     "1/C Cu, EPR insulation, <b>133 % level</b>, 90 °C, tape shield, PVC jacket. ICEA S-93-639, UL 1072 (MV-105). "
     "Terminations IEEE 48; acceptance test VLF (IEEE 400.2) / NETA ATS",
     "MV-105 15 kV, 220 mil NL-EPR 133 %, SIMpull &middot; SPEC 46302"),
    ("#f2c613", "480 V feeders and power", "T-R2A secondary, LC-R2A to MCCs, motors and MOVs",
     "Cu XHHW-2, 90 °C wet / dry, sized at <b>125 %</b> of full load; voltage drop &le; 3 %. ICEA S-95-658, UL 44 / UL 1277; "
     "10+ parallel sets: compare with bus duct",
     "XHHW-2 1/C (SIMpull) &middot; Type TC-ER 3/C + ground &middot; SPEC 45252"),
    ("#3a8fd9", "Tray cable: power and control", "Every tray between the e-house and the HRSG",
     "Type TC-ER (UL 1277) so it may leave the tray as an exposed run to the equipment (NEC 336.10); sunlight resistant, "
     "direct burial; <b>IEEE 1202 / UL 1685</b> 70,000 Btu/h vertical-tray flame test",
     "Control TC-ER 14 AWG multiconductor &middot; SPEC 45053"),
    ("#b06ae0", "Hazardous area: gas train, duct burner", "Duct-burner fuel skid, BMS panel to the valves",
     "Class I Div 2 wiring methods per NEC 501.10(B); MC-HL (UL 1569 + UL 2225) also qualifies for Div 1. Burner "
     "management per <b>NFPA 85</b>, duct burner UL 295, listed fittings",
     "ARMOR-X MC-HL, welded armor &middot; SPEC 45352"),
    ("#e39a5f", "Variable-frequency drives", "SCR dilution-air blowers, FD fans",
     "VFD-rated: symmetrical three-ground construction, overall shield or continuous armor for the common-mode current, "
     "XLPE insulation for reflected-wave peaks",
     "ARMOR-X MC-HL VFD &middot; TC-ER VFD &middot; SPEC 45352"),
    ("#36c26b", "Instrumentation, 4-20 mA / HART", "Drum level, pressures, flame scanners, analyzers",
     "<b>Individually shielded</b> twisted pairs + overall shield, drain wires; 300 V PLTC (UL 13, NEC 725) or ITC; "
     "ICEA S-73-532; segregated from power in tray",
     "Instrumentation PLTC, SPOS &middot; SPEC 43303"),
    ("#17a589", "Thermocouple extension", "Gas-path, tube-metal and duct temperatures",
     "Alloy matched to the thermocouple (type K = KX), ANSI MC96.1 / ASTM E230 colour code; <b>never copper</b>; "
     "shielded pairs; PLTC; 105 °C near the casing",
     "Thermocouple extension, PLTC multi-pair &middot; SPEC 42345 / 42350"),
    ("#ff9f1a", "Fire alarm, fibre, building wire", "F&G loops, CEMS data, e-house lighting",
     "FPLR / FPLP (NEC 760, NFPA 72); single-mode fibre, armored in tray; THHN / THWN-2 in conduit (UL 83)",
     "SIMpull THHN / THWN-2 &middot; fire-alarm and fibre cable"),
]


def slide_spec():
    rows = ""
    for (col, app, where, req, sw) in SPEC:
        rows += (f'<tr><td style="border-left:5px solid {col};padding-left:10px"><div style="font:800 15px/1.1 BC;color:{WHITE};'
                 f'text-transform:uppercase;letter-spacing:.03em">{app}</div><div style="font:400 11px/1.3 B;color:{GREY};'
                 f'margin-top:3px">{where}</div></td>'
                 f'<td style="font:400 12px/1.38 B;color:#d4d8dc;text-align:left">{req}</td>'
                 f'<td style="font:700 13px/1.3 BC;color:{COPPER};text-align:left;letter-spacing:.02em">{sw}</td></tr>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:52px">Boiler solutions &nbsp;&middot;&nbsp; the specification</div>
  <div class="abs h2" style="left:62px;top:80px;font-size:50px">What the spec <em>calls for</em></div>
  <div class="abs lede" style="left:64px;top:136px;width:1000px;font-size:14px">Every cable application on the HRSG, the
    requirements an owner's or EPC's cable specification writes for it, and the Southwire product built to meet them.</div>
  <div class="abs" style="left:64px;top:184px;width:1312px">
    <table class="m" style="table-layout:fixed"><colgroup><col style="width:270px"><col style="width:700px"><col></colgroup>
      <tr><th>Application &middot; where</th><th style="text-align:left">What the specification calls for</th>
          <th style="text-align:left">Southwire</th></tr>{rows}</table></div>
  <div class="abs" style="left:64px;top:680px;width:1312px;display:flex;gap:28px;border-top:2px solid {COPPER};padding-top:12px">
    <div style="flex:1.25"><div class="cnum">Checked against a real plant</div><div class="cd" style="font-size:12.5px;margin-top:5px">
      A recent US utility combined-cycle filing shows the same structure: <b style="color:{WHITE}">HRSG MCCs A / B</b> fed
      from 480 V switchgear through 2,500 / 3,300 kVA transformers off the auxiliary bus (6.9 kV there, 13.8 kV here).</div></div>
    <div style="flex:1"><div class="cnum">Design and install</div><div class="cd" style="font-size:12.5px;margin-top:5px">
      Raceway and cable design for generating stations: IEEE 422. Grounding: IEEE 80 / 665. Area classification:
      NEC 500, API RP 500. Field acceptance: NETA ATS.</div></div>
  </div>
  {foot(9)}
</section>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    import pymupdf
    head = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
    out = pymupdf.open()
    for i, sec in enumerate((slide1(), slide_basics(), slide_cycle(), slide_hero(), slide_elev(), slide_room(), slide_diagram(), slide_system(), slide_spec(), slide2(), slide3())):
        hp = os.path.join(OUT, f"_s{i}.html")
        sec = sec.replace('<section class="page slide">', '<section class="page slide"><div class="s">', 1).replace(
            "</section>", "</div></section>")
        open(hp, "w").write(head + sec + "</body></html>")
        pdf = hp.replace(".html", ".pdf")
        subprocess.run([bz.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", url(hp)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.insert_pdf(pymupdf.open(pdf))
        os.remove(pdf)
        os.remove(hp)
    p = os.path.join(OUT, "SW-3X1_boilers.pdf")
    out.save(p, garbage=3, deflate=True)
    for i, pg in enumerate(out):
        pg.get_pixmap(dpi=96).save(os.path.join(OUT, f"SW-3X1_boilers_{i + 1}.png"))
    print("wrote", p, len(out), "slides", out[0].rect)


if __name__ == "__main__":
    main()
