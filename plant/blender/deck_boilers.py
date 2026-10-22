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
.foot {{ font: 400 11px/1 B; color: #80868c; letter-spacing: .04em; }}
"""


def img(k):
    return url(os.path.join(R, f"{k}_pro_clean.jpg"))


def kft(ft):
    return f"{ft / 1000:,.0f},000"


def foot(n, short=False):
    left = ("SW-3X1 MODEL &middot; NOT ENGINEERED" if short else
            "SW-3X1 MODEL &middot; CONCEPTUAL ILLUSTRATION, NOT ENGINEERED &middot; QUANTITIES FROM THE MODEL'S CABLE SCHEDULE")
    return f"""<div class="abs foot" style="left:64px;right:64px;bottom:26px;display:flex;justify-content:space-between;
      border-top:1px solid #2c3036;padding-top:11px"><span>{left}</span><span>{credit.EMAIL} &nbsp;&middot;&nbsp; BOILERS {n}/3</span></div>"""


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
  {foot(2, short=True).replace("left:64px", "left:870px")}
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


def cams():
    import re
    txt = open(os.path.join(HERE, "pro_look.py")).read()
    out = {}
    for k in SPOTS:
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
  {foot(3)}
</section>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    import pymupdf
    head = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
    out = pymupdf.open()
    for i, sec in enumerate((slide1(), slide2(), slide3())):
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
