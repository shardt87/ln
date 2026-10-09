"""Brochure v2 ("The Path of Power"): vector layouts in HTML/CSS, printed to PDF by headless Chromium.

Pages in this sample: the cover (8.5 x 11 in), the opening spread (17 x 11 in) and the ARMOR-X anatomy spread.
- One continuous copper line is the brochure's device: it leaves the conductor on the cover, runs the power path
  through the plant on the opening spread (gas yard -> GT and generator -> step-up -> 230 kV), and ends at the
  conductor of the cable it is made of on the anatomy spread. A wayfinding bar at the foot of every spread shows
  where the reader is on that path.
- Images are renders of the model (renders/brochure_v2/K15_pro.png, renders/anatomy/armorx_*.png). Node and callout
  positions come from the Blender cameras (K15 callouts, armorx_anchors.json), so every leader lands on its object.
- Type is live text in Barlow / Barlow Condensed (embedded by Chromium), so the PDF stays vector.

    python blender/brochure_v2.py [--draft DIR]     # DIR: low-res renders for layout proofs
Outputs renders/brochure_v2/: SW_PathOfPower_sample.pdf, and PNG previews of each page.
"""
import argparse
import json
import math
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DECK = os.path.join(HERE, "deck")
OUT = os.path.join(PLANT, "renders", "brochure_v2")
CHROME = "/opt/pw-browsers/chromium"
ap = argparse.ArgumentParser()
ap.add_argument("--draft", default=None, help="directory with K15_pro.png, armorx_hero.png, armorx_end.png, "
                "armorx_anchors.json and K15_pro.labels.json (layout proofs)")
args = ap.parse_args()
SRC = dict(k15=os.path.join(OUT, "K15_pro.png"), k15j=os.path.join(OUT, "K15_pro.labels.json"),
           hero=os.path.join(PLANT, "renders", "anatomy", "armorx_hero.png"),
           end=os.path.join(PLANT, "renders", "anatomy", "armorx_end.png"),
           anch=os.path.join(PLANT, "renders", "anatomy", "armorx_anchors.json"))
if args.draft:
    D = args.draft
    SRC = dict(k15=os.path.join(D, "K15_pro.png"), k15j=os.path.join(D, "K15_pro.labels.json"),
               hero=os.path.join(D, "armorx_hero.png"), end=os.path.join(D, "armorx_end.png"),
               anch=os.path.join(D, "armorx_anchors.json"))
url = lambda p: "file://" + os.path.abspath(p)

HALO = 'stroke="#0e1012" stroke-width="3.2" stroke-opacity=".75" paint-order="stroke" stroke-linejoin="round"'
PX = 96                                    # CSS px per inch
SW, SH = 17 * PX, 11 * PX                  # spread
CW = int(8.5 * PX)                         # single page
COPPER, COPPER_L, INK, WHITE, GREY = "#e39a5f", "#f2b98a", "#0e1012", "#f5f3ef", "#b9bec4"

CSS = f"""
@font-face {{ font-family: BC; src: url({url(os.path.join(DECK, 'BarlowCondensed-Bold.ttf'))}); font-weight: 700; }}
@font-face {{ font-family: BC; src: url({url(os.path.join(DECK, 'BarlowCondensed-ExtraBold.ttf'))}); font-weight: 800; }}
@font-face {{ font-family: B; src: url({url(os.path.join(DECK, 'Barlow-Regular.ttf'))}); font-weight: 400; }}
@page cover {{ size: 8.5in 11in; margin: 0; }}
@page spread {{ size: 17in 11in; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; overflow: hidden; background: {INK}; break-after: page; }}
.cover {{ page: cover; width: 8.5in; height: 11in; }}
.spread {{ page: spread; width: 17in; height: 11in; }}
.bg {{ position: absolute; inset: 0; background-size: cover; background-position: center; }}
.abs {{ position: absolute; }}
.kicker {{ font: 700 15px/1 BC; letter-spacing: .32em; color: {COPPER}; text-transform: uppercase; }}
.h1 {{ font: 800 92px/.9 BC; color: {WHITE}; text-transform: uppercase; letter-spacing: -.005em; }}
.h1 em {{ font-style: normal; color: {COPPER}; }}
.body {{ font: 400 14.5px/1.55 B; color: {GREY}; }}
.tag {{ font: 700 12.5px/1 BC; letter-spacing: .16em; color: {WHITE}; text-transform: uppercase; white-space: nowrap; }}
.tag b {{ color: {COPPER}; font-weight: 700; }}
.stat {{ font: 400 11.5px/1.35 B; color: {WHITE}; width: 130px; margin-top: 4px; }}
.small {{ font: 400 9.5px/1.4 B; color: #8a8f95; }}
.folio {{ font: 700 11px/1 BC; letter-spacing: .24em; color: #8a8f95; text-transform: uppercase; }}
.speck {{ font: 700 11.5px/1.3 BC; letter-spacing: .16em; color: {COPPER}; text-transform: uppercase; }}
.specv {{ font: 400 12.5px/1.35 B; color: {WHITE}; margin-top: 3px; }}
.spec td {{ font: 400 12.5px/1.35 B; color: {GREY}; padding: 6px 18px 6px 0; border-top: 1px solid #2c3036;
           vertical-align: top; }}
.spec td:first-child {{ font: 700 12px/1.35 BC; letter-spacing: .14em; color: {COPPER}; text-transform: uppercase;
                       white-space: nowrap; }}
"""


def glow_defs():
    return """<defs>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="cu" x1="0" x2="1"><stop offset="0" stop-color="#b8692f"/><stop offset=".5" stop-color="#f2b98a"/>
    <stop offset="1" stop-color="#e39a5f"/></linearGradient>
</defs>"""


def smooth(pts, t=.5):
    """Catmull-Rom through pts -> SVG cubic path."""
    if len(pts) < 2:
        return ""
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def wayfinding(active, x0=60, x1=SW - 60, y=SH - 40):
    """Foot of every spread: the path of power as a line of stations, the current one lit."""
    st = ["FUEL GAS", "GENERATION · 21 kV", "AUXILIARIES · 15 kV / 600 V", "STEP-UP · 21 / 230 kV", "GRID · 230 kV"]
    n = len(st)
    out = [f'<svg class="abs" style="left:0;top:0" width="{SW}" height="{SH}">',
           f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#3a3f45" stroke-width="1.2"/>']
    for k, s in enumerate(st):
        x = x0 + (x1 - x0) * k / (n - 1)
        on = k == active
        out.append(f'<circle cx="{x}" cy="{y}" r="{5 if on else 3.2}" fill="{COPPER if on else "#5a6067"}"/>')
        anchor = "start" if k == 0 else "end" if k == n - 1 else "middle"
        out.append(f'<text x="{x}" y="{y - 12}" text-anchor="{anchor}" font-family="BC" font-weight="700" '
                   f'font-size="10.5" letter-spacing="2" fill="{COPPER if on else "#7d838a"}">{s}</text>')
    out.append("</svg>")
    return "\n".join(out)


def cover(anch):
    a = anch["anchors"]["end"]
    rx, ry = anch["res"]["end"]
    s = CW / rx
    k = max(("cond0", "cond1", "cond2"), key=lambda n: a[n][0])          # the conductor nearest the right edge
    cx, cy = a[k][0] * s, a[k][1] * s
    H = 11 * PX
    return f"""
<section class="page cover">
  <div class="bg" style="background-image:url({url(SRC['end'])})"></div>
  <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(14,16,18,.96) 0%,rgba(14,16,18,.85) 30%,
       rgba(14,16,18,0) 52%)"></div>
  <svg class="abs" style="left:0;top:0" width="{CW}" height="{H}">{glow_defs()}
    <path d="M{cx:.1f},{cy:.1f} C{cx + 120:.1f},{cy:.1f} {CW - 160},{cy - 40:.1f} {CW + 10},{cy - 40:.1f}"
          stroke="url(#cu)" stroke-width="3.2" fill="none" filter="url(#glow)" stroke-linecap="round"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{COPPER_L}" filter="url(#glow)"/>
  </svg>
  <img class="abs" src="{url(os.path.join(DECK, 'southwire_pgs_logo.png'))}" style="left:56px;top:54px;width:250px">
  <div class="abs kicker" style="left:58px;top:168px">Wire &amp; cable for the gas power campus</div>
  <div class="abs h1" style="left:54px;top:196px;font-size:118px">The path<br><em>of power</em></div>
  <div class="abs" style="left:58px;top:430px;width:64px;height:4px;background:{COPPER}"></div>
  <div class="abs body" style="left:58px;top:448px;width:330px;color:{WHITE}">From the gas yard to the 230 kV line, every
    megawatt a plant makes travels by cable. This is the route, and the cable it runs on.</div>
  <div class="abs" style="left:0;right:0;bottom:0;height:66px;background:linear-gradient(0deg,rgba(14,16,18,.9),rgba(14,16,18,0))"></div>
  <div class="abs kicker" style="left:58px;bottom:34px;color:{WHITE}">Accelerating time to power&trade;</div>
  <div class="abs folio" style="right:58px;bottom:34px">Southwire &middot; Power Generation Solutions</div>
</section>"""


def opening(lab):
    s = SW / lab["rw"]
    nodes = [(c["x"] * s, c["y"] * s, c["num"], c["text"]) for c in lab["callouts"] if c["text"] != "Line 1 entrance"]
    pts = [(x, y) for x, y, _, _ in nodes]
    # path: gas yard -> header -> GT branch -> GT1 -> generator -> GCB -> GSU -> line entrance -> tower, off the page
    gx, gy = pts[0]
    pts = [(SW + 10, gy - 60), (gx + 70, gy - 10)] + pts
    tx, ty = pts[-1]
    pts = pts + [(tx - 120, ty + 60), (tx - 420, SH + 20)]
    by = {t: (x, y) for x, y, _, t in nodes}
    labels = [("Plant gas yard", "Fuel gas", "", 18, -46, "start"),
              ("GT1", "Gas turbine + generator", "21 kV", -26, -70, "end"),
              ("GSU-1", "Step-up transformer", "21 / 230 kV", -70, 22, "end"),
              ("Line 1 terminal tower", "To the grid", "230 kV", 26, -40, "start")]
    svg = [f'<svg class="abs" style="left:0;top:0" width="{SW}" height="{SH}">{glow_defs()}',
           f'<path d="{smooth(pts)}" stroke="url(#cu)" stroke-width="3.4" fill="none" filter="url(#glow)" '
           f'stroke-linecap="round" stroke-linejoin="round"/>']
    for name, t1, t2, dx, dy, anc in labels:
        x, y = by[name]
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{COPPER_L}" stroke="{INK}" stroke-width="1.5"/>')
        lx, ly = x + dx, y + dy
        svg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{WHITE}" stroke-width=".8" '
                   f'opacity=".8"/>')
        svg.append(f'<text x="{lx + (4 if anc == "start" else -4):.1f}" y="{ly - 4:.1f}" text-anchor="{anc}" '
                   f'font-family="BC" font-weight="700" font-size="13" letter-spacing="2.2" fill="{WHITE}" {HALO}>'
                   f'{t1.upper()}</text>')
        if t2:
            svg.append(f'<text x="{lx + (4 if anc == "start" else -4):.1f}" y="{ly + 16:.1f}" text-anchor="{anc}" '
                       f'font-family="BC" font-weight="800" font-size="19" letter-spacing="1" fill="{COPPER}" {HALO}>{t2}</text>')
    svg.append("</svg>")
    return f"""
<section class="page spread">
  <div class="bg" style="background-image:url({url(SRC['k15'])})"></div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse 62% 64% at 0% 0%,
       rgba(14,16,18,.94) 0%,rgba(14,16,18,.82) 45%,rgba(14,16,18,0) 100%)"></div>
  <div class="abs" style="left:0;right:0;bottom:0;height:120px;background:linear-gradient(0deg,rgba(14,16,18,.92),rgba(14,16,18,0))"></div>
  {"".join(svg)}
  <div class="abs kicker" style="left:64px;top:64px">01 &mdash; The path of power</div>
  <div class="abs h1" style="left:60px;top:92px">Every megawatt<br><em>travels by cable.</em></div>
  <div class="abs body" style="left:64px;top:290px;width:470px;color:{WHITE}">
    Gas arrives at the yard and burns in three H-class turbines. Each generator makes power at 21 kV; a
    generator breaker and isolated-phase bus carry it to the step-up transformer, and 230 kV cable and
    conductors take it to the grid. Along the way, miles of medium- and low-voltage cable run every pump,
    fan and valve that keeps the turbines turning.</div>
  <div class="abs" style="left:64px;top:430px;display:flex;gap:42px">
    <div><div class="h1" style="font-size:46px">4.6 MI</div><div class="stat">of cable-tray routes</div></div>
    <div><div class="h1" style="font-size:46px">4.2 MI</div><div class="stat">of duct-bank and buried cable routes</div></div>
    <div><div class="h1" style="font-size:46px">417</div><div class="stat">pieces of equipment, each with its own cable</div></div>
  </div>
  {wayfinding(0)}
  <div class="abs small" style="right:60px;bottom:70px;text-align:right;color:#aab0b6">SK-3X1 campus, rendered from the 3D model.
    Route lengths measured along modelled routes, not cable footage.</div>
</section>"""


def anatomy(anch):
    a = anch["anchors"]["hero"]
    rx, ry = anch["res"]["hero"]
    s = SW / rx
    P = {k: (v[0] * s, v[1] * s) for k, v in a.items()}
    items = [("jacket", "Red PVC jacket", "Sunlight resistant, printed legend every foot"),
             ("armor", "Corrugated aluminium armor", "Continuously welded: impervious, crush-resistant, MC-HL"),
             ("tape", "Copper tape shield", "Helically applied, 25% overlap"),
             ("ins_shield", "Insulation shield", "Extruded semiconducting layer"),
             ("insulation", "NL-EPR insulation", "15 kV, 133% insulation level"),
             ("cond_shield", "Conductor shield", "Extruded semiconducting layer"),
             ("conductor", "500 kcmil copper", "37-strand compressed conductor")]
    svg = [f'<svg class="abs" style="left:0;top:0" width="{SW}" height="{SH}">{glow_defs()}']
    xs = sorted(P[k][0] for k, _, _ in items)
    for i, (k, t1, t2) in enumerate(items):
        x, y = P[k]
        ly = 196 if i % 2 == 0 else 268                       # two label tiers above the cable
        svg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ly + 26}" stroke="{COPPER}" stroke-width="1"/>')
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{COPPER_L}" stroke="{INK}" stroke-width="1.4"/>')
        svg.append(f'<text x="{x - 2:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="BC" font-weight="800" '
                   f'font-size="13" letter-spacing="1.8" fill="{WHITE}">{t1.upper()}</text>')
        svg.append(f'<text x="{x - 2:.1f}" y="{ly + 16:.1f}" text-anchor="middle" font-family="B" font-size="10" '
                   f'fill="{GREY}">{t2}</text>')
    # the copper line arrives from the left page edge and ends in the conductor
    cx, cy = P["conductor"]
    svg.append(f'<path d="M-10,{SH - 150} C{SW * .35},{SH - 150} {SW * .62},{SH - 210} {cx - 60},{cy + 150} '
               f'S{cx},{cy + 40} {cx},{cy}" stroke="url(#cu)" stroke-width="2.6" fill="none" filter="url(#glow)" opacity=".85"/>')
    svg.append("</svg>")
    rows = [("Voltage", "15 kV, 133% insulation level (MV-105)"),
            ("Conductor", "3 x 500 kcmil compressed copper, 37 strands"),
            ("Insulation", "Non-lead EPR, extruded semiconducting shields"),
            ("Shield", "Copper tape, 25% overlap"),
            ("Ground", "1 x #1 AWG bare copper"),
            ("Armor", "Continuously welded corrugated aluminium"),
            ("Jacket", "Red PVC, sunlight resistant"),
            ("Listing", "Type MC-HL (UL 1569 / UL 2225) or MV-105 (UL 1072)")]
    cells = "".join(f'<div><div class="speck">{k}</div><div class="specv">{v}</div></div>' for k, v in rows)
    return f"""
<section class="page spread">
  <div class="bg" style="background-image:url({url(SRC['hero'])})"></div>
  {"".join(svg)}
  <div class="abs kicker" style="left:64px;top:64px">02 &mdash; Anatomy of a 15 kV feeder</div>
  <div class="abs h1" style="left:60px;top:92px;font-size:84px">Armor-X<sup style="font-size:.35em;vertical-align:1.6em">&reg;</sup><br><em>opened up.</em></div>
  <div class="abs body" style="left:64px;top:282px;width:400px;color:{WHITE}">
    In the turbine hall the 13.8 kV auxiliaries run on 15 kV ARMOR-X: three shielded EPR cores and a ground under
    a continuously welded aluminium armor and a red PVC jacket. Armored, it lays straight into the tray with no
    conduit, and it is rated for the Class I, Division 2 areas around the gas turbines.</div>
  <div class="abs" style="left:0;right:0;bottom:0;height:300px;background:linear-gradient(0deg,rgba(14,16,18,.95) 0%,
       rgba(14,16,18,.85) 45%,rgba(14,16,18,0) 100%)"></div>
  <div class="abs" style="left:64px;right:64px;bottom:86px;display:grid;grid-template-columns:repeat(4,1fr);
       column-gap:36px;row-gap:14px;border-top:1px solid #3a3f45;padding-top:14px">{cells}</div>
  {wayfinding(2)}
  <div class="abs small" style="right:64px;top:64px;text-align:right;width:380px">Typical construction from the
    customer's ARMOR-X list (500-37 3/C CPRESS CU NL-EPR 25% T/S 1X#1 CU GW, red PVC). Confirm against current
    Southwire specifications. Studio render of the cable model, not a photograph.</div>
</section>"""


def jpeg_sources():
    from PIL import Image
    d = os.path.join(OUT, "_img")
    os.makedirs(d, exist_ok=True)
    for k in ("k15", "hero", "end"):
        q = os.path.join(d, os.path.splitext(os.path.basename(SRC[k]))[0] + ".jpg")
        if not os.path.exists(q) or os.path.getmtime(q) < os.path.getmtime(SRC[k]):
            Image.open(SRC[k]).convert("RGB").save(q, quality=90, subsampling=0)
        SRC[k] = q


def main():
    os.makedirs(OUT, exist_ok=True)
    jpeg_sources()
    anch = json.load(open(SRC["anch"]))
    lab = json.load(open(SRC["k15j"]))
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + \
        cover(anch) + opening(lab) + anatomy(anch) + "</body></html>"
    hp = os.path.join(OUT, "sample.html")
    open(hp, "w").write(html)
    pdf = os.path.join(OUT, "SW_PathOfPower_sample.pdf")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}", url(hp)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", pdf)


if __name__ == "__main__":
    main()
