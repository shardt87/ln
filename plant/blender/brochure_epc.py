"""EPC edition: 'Built to Pull' - Southwire power-generation cable installation solutions, from reel to energised.

24 pages (US Letter, spreads printed 17 x 11), vector HTML printed by headless Chromium per section and merged, in the
design system of the Path of Power brochures (brochure_zones.py: fonts, colours, plan map, projection):

  1 cover | 2-3 opening (the lifecycle, the job in numbers) | 4-5 Plan (vector cable X-ray of the model)
  6 Deliver | 7 Stage | 8-9 Prefab | 10 Pull (traditional vs SIMpull) | 11 Terminate & test
  12-22 zone playbooks (turbine hall, HRSG, ACC, electrical, switchyard, BOP & fuel gas, CCS, BESS,
        modular power spread by technology, LNG / H2) | 23 Operate & support | 24 back cover

Numbers come from the model and its cable schedule (brochure/zone_numbers.json from brochure/cables_xray.json: routed
home-run cable by zone; plant totals from SW-3X1_Cable_Schedule_and_BOM.xlsx). Southwire product facts are as printed in
the SIMpull Solutions brochure; prefabricated cable systems are generic. Images: renders/epic/*_pro_clean.jpg.

    python blender/brochure_epc.py          # -> renders/brochure_epc/SW_BuiltToPull_EPC.pdf + page previews
"""
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brochure_zones as bz                                     # noqa: E402  (CSS, plan map, projection, colours)

PLANT = bz.PLANT
OUT = os.path.join(PLANT, "renders", "brochure_epc")
EPIC = bz.EPIC
url = bz.url
PX, CW, SW, SH = bz.PX, bz.CW, bz.SW, bz.SH
COPPER, COPPER_L, INK, WHITE, GREY = bz.COPPER, bz.COPPER_L, bz.INK, bz.WHITE, bz.GREY
ZN = json.load(open(os.path.join(PLANT, "brochure", "zone_numbers.json")))
X = json.load(open(os.path.join(PLANT, "brochure", "cables_xray.json")))
XCOL = {'HV 230 kV': '#9b59d0', 'MV 35 kV': '#c0392b', 'MV 25 kV': '#d35400', 'MV 15 kV': '#e8453c', 'MV 5 kV': '#ef8a2c',
        'LV 600 V': '#f2c613', 'DC 2 kV': '#17a589', 'Portable MV': '#f7b733', 'Portable LV': '#a3b1b8', 'Control': '#3a8fd9',
        'Instrumentation': '#36c26b', 'Fire alarm': '#ff3d7f', 'Fibre / data': '#ff9f1a'}
TOT = dict(circuits="5,687", cables="19,715", feet="5.33 M", reels="1,468", miles="1,009", classes="13")
PNAME = {"PLTC": "Instrumentation PLTC / TC-ER", "ITC": "Instrumentation ITC (IS)", "CT": "Control TC-ER #14",
         "CTCT": "Control TC-ER #10 (CT / VT)", "CTAX": "ARMOR-X MC-HL control", "LV": "Type TC-ER 600 V power",
         "LVAX": "ARMOR-X MC-HL 600 V", "LV1C": "XHHW-2 1/C feeder sets", "VFD": "VFD cable 600 V", "TCX": "Thermocouple ext. KX",
         "FA": "Fire alarm FPLR", "FO": "Fibre optic (armored)", "PV": "PV / RHW-2 2 kV DC", "MV15": "MV-105 15 kV",
         "MV35": "MV-105 35 kV", "MV5": "MV-105 5 kV", "MV15AX": "ARMOR-X MC-HL 15 kV", "HV230": "230 kV XLPE",
         "W": "Type W 2 kV (cam-lock)", "SHD": "Type SHD-GC 15 kV", "THHN": "SIMpull THHN/THWN-2", "RTD": "RTD triads",
         "MV25": "MV-105 25 kV", "MV5S": "MV-105 5 kV 1/C"}

CSS = bz.CSS + f"""
.h2 {{ font: 800 40px/.95 BC; color: {WHITE}; text-transform: uppercase; }}
.h2 em, .h3 em {{ font-style: normal; color: {COPPER}; }}
.h3 {{ font: 800 22px/1 BC; color: {WHITE}; text-transform: uppercase; letter-spacing: .02em; }}
.lede {{ font: 400 15px/1.5 B; color: {WHITE}; }}
.li {{ break-inside: avoid; font: 400 11.2px/1.45 B; color: {GREY}; padding: 6px 0 7px 16px; border-top: 1px solid #2c3036; position: relative; }}
.li:before {{ content: ''; position: absolute; left: 0; top: 12px; width: 7px; height: 7px; background: {COPPER}; }}
.li b {{ font: 700 12px/1.3 BC; letter-spacing: .06em; color: {WHITE}; text-transform: uppercase; margin-right: 6px; }}
.num {{ font: 800 40px/1 BC; color: {COPPER}; }}
.numl {{ font: 700 10px/1.2 BC; letter-spacing: .16em; color: {GREY}; text-transform: uppercase; margin-top: 4px; }}
.tag {{ display: inline-block; font: 700 10px/1 BC; letter-spacing: .14em; color: {INK}; background: {COPPER};
        padding: 4px 7px 3px; text-transform: uppercase; }}
.cap {{ font: 400 9.5px/1.4 B; color: #aab0b6; }}
"""


# ------------------------------------------------------------------------------- helpers
def img(name):
    """renders/epic/<name> (or a path) as a print JPEG."""
    p = name if os.path.isabs(name) else os.path.join(EPIC, name)
    return bz.jpg_of(os.path.basename(p), os.path.dirname(p))


def epic(k):
    if k == "K15":
        return img(os.path.join(PLANT, "renders", "brochure_v2", "K15_pro.png"))
    c = os.path.join(EPIC, f"{k}_pro_clean.jpg")
    return img(c if os.path.exists(c) else os.path.join(EPIC, f"{k}_pro.png"))


def foot(page_no, w=CW, left=48, chapter=""):
    return (f'<div class="abs" style="left:{left}px;width:{w - 96}px;bottom:30px;display:flex;justify-content:space-between;'
            f'align-items:center;border-top:1px solid #3a3f45;padding-top:10px"><span class="small">SOUTHWIRE &middot; '
            f'POWER GENERATION SOLUTIONS &middot; BUILT TO PULL{(" &middot; " + chapter) if chapter else ""}</span>'
            f'<span class="small">{page_no}</span></div>')


def stat(n, label, w=120):
    return f'<div style="width:{w}px"><div class="num">{n}</div><div class="numl">{label}</div></div>'


def fmt_ft(ft):
    return f"{ft / 1e6:.2f} M" if ft >= 1e6 else f"{ft / 1e3:,.0f} k"


def zstats(keys):
    agg = dict(circ=0, cab=0, ft=0, lmax=0)
    prod = {}
    for k in keys:
        z = ZN[k]
        for f in ("circ", "cab", "ft"):
            agg[f] += z[f]
        agg["lmax"] = max(agg["lmax"], z["lmax"])
        for p, ft in z["prod"]:
            prod[p] = prod.get(p, 0) + ft
    agg["prod"] = sorted(prod.items(), key=lambda t: -t[1])[:4]
    return agg


def numbers_block(keys, w=CW - 96):
    a = zstats(keys)
    top = max(f for _, f in a["prod"]) if a["prod"] else 1
    bars = "".join(f'<div style="display:grid;grid-template-columns:150px 1fr 50px;align-items:center;column-gap:8px;margin:3px 0">'
                   f'<span class="cap" style="color:{GREY}">{PNAME.get(p, p)}</span><span style="height:6px;background:#2c3036">'
                   f'<span style="display:block;height:6px;width:{100 * f / top:.0f}%;background:{COPPER}"></span></span>'
                   f'<span class="cap" style="text-align:right">{fmt_ft(f)}</span></div>' for p, f in a["prod"])
    return f"""<div style="width:{w}px;display:grid;grid-template-columns:repeat(4,1fr) 1.6fr;column-gap:16px;align-items:end">
      {stat(f"{a['circ']:,}", "circuits", 100)}{stat(f"{a['cab']:,}", "cables", 100)}{stat(fmt_ft(a['ft']), "ft routed", 100)}
      {stat(f"{a['lmax']:,}", "ft longest run", 100)}<div>{bars}</div></div>"""


# ------------------------------------------------------------------------------- vector cable X-ray
def xray_svg(w, h, cam, ink=True):
    cam = dict(cam, res=(w, h))
    P = lambda p: bz.project(cam, p)
    out = []
    for it in bz.MODEL["items"]:
        fp, z = it.get("fp"), it.get("z")
        if not fp or len(fp) != 4 or it.get("area") == "L" or it["layer"].startswith(("UNDERGROUND", "OPT_DC", "COAST")):
            continue
        x0, x1, y0, y1 = fp
        if x1 - x0 > 700 or y1 - y0 > 700 or z[1] < .5:
            continue
        top = [P((x0, y0, z[1])), P((x1, y0, z[1])), P((x1, y1, z[1])), P((x0, y1, z[1]))]
        base = [P((x0, y0, 0)), P((x1, y0, 0)), P((x1, y1, 0)), P((x0, y1, 0))]
        d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in top) + " Z"
        d += "".join(f" M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" for a, b in zip(top, base))
        out.append(f'<path d="{d}" fill="none" stroke="#56606a" stroke-width=".35" stroke-opacity=".55"/>')
    # cable paths: coloured by the highest-voltage class they carry, width by the number of cables
    best, count = {}, {}
    for r in X["cables"]:
        pi = r[12]
        if pi is None or pi < 0:
            continue
        best[pi] = min(best.get(pi, 99), r[1])
        count[pi] = count.get(pi, 0) + r[5]
    order = sorted(best, key=lambda pi: -best[pi])
    for pi in order:
        pts = X["paths"][pi]
        pp = [P(pts[i:i + 3]) for i in range(0, len(pts) - 2, 3)]
        col = XCOL[X["classes"][best[pi]]]
        sw = min(2.6, .45 + .14 * math.sqrt(count[pi]))
        d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pp)
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw:.2f}" stroke-opacity=".85" '
                   f'stroke-linejoin="round" stroke-linecap="round"/>')
    bg = f'<rect width="{w}" height="{h}" fill="{INK}"/>' if ink else ""
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{bg}{"".join(out)}</svg>'


def xray_legend():
    return "".join(f'<span style="display:inline-flex;align-items:center;margin:0 14px 6px 0" class="cap">'
                   f'<span style="width:16px;height:3px;background:{c};margin-right:6px"></span>{k}</span>'
                   for k, c in XCOL.items())


# ------------------------------------------------------------------------------- icons (line art)
def ico(kind, s=44, c=COPPER):
    st = f'fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    g = {
        "plan": f'<rect x="9" y="6" width="26" height="33" rx="2" {st}/><path d="M15 15h14M15 21h14M15 27h9" {st}/>',
        "deliver": f'<path d="M4 30V14h22v16M26 20h8l6 6v4h-14" {st}/><circle cx="12" cy="32" r="4" {st}/><circle cx="33" cy="32" r="4" {st}/>',
        "stage": f'<circle cx="22" cy="22" r="15" {st}/><circle cx="22" cy="22" r="5" {st}/><path d="M22 7v10M22 27v10M7 22h10M27 22h10" {st}/>',
        "prefab": f'<path d="M5 15h34v14H5zM5 15l6-7h34l-6 7M39 29l6-7V8" {st}/><path d="M12 15v14M22 15v14M32 15v14" {st}/>',
        "pull": f'<path d="M4 22h24" {st}/><path d="M26 15l8 7-8 7" {st}/><circle cx="38" cy="22" r="3" {st}/><path d="M4 16h10M4 28h10" {st}/>',
        "test": f'<rect x="7" y="9" width="30" height="24" rx="3" {st}/><path d="M13 27l6-10 5 7 4-5 4 8" {st}/><path d="M16 33v5M28 33v5" {st}/>',
        "operate": f'<rect x="5" y="8" width="34" height="22" rx="2" {st}/><path d="M16 36h12M22 30v6M10 22l6-6 5 4 8-8" {st}/>',
    }[kind]
    return f'<svg width="{s}" height="{s}" viewBox="0 0 44 44">{g}</svg>'


STEPS = [("plan", "Plan", "Model, route and size every circuit; plan pulls and reels"),
         ("deliver", "Deliver", "Cut-to-length, paralleled, colour-coded reels to the pull"),
         ("stage", "Stage", "One person moves the reel; no jacks, no pallet jacks"),
         ("prefab", "Prefab", "Spine modules, pre-terminated MV, skids pre-wired"),
         ("pull", "Pull", "No lube, factory heads, safer pullers"),
         ("test", "Terminate & test", "Terminations and test records for turnover"),
         ("operate", "Operate", "Outage support, training, people on site")]


def hardhat(c=COPPER, s=26):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 26 26"><path d="M4 15a9 9 0 0 1 18 0z" fill="{c}"/>'
            f'<rect x="2" y="15" width="22" height="3" rx="1.5" fill="{c}"/><circle cx="13" cy="21" r="4" fill="{c}"/></svg>')


def reel_ico(c="#8a9198", s=20):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 20 20"><rect x="2" y="2" width="16" height="16" rx="2" fill="none" '
            f'stroke="{c}" stroke-width="1.6"/><path d="M5 2v16M15 2v16M5 6h10M5 10h10M5 14h10" stroke="{c}" stroke-width="1.2"/></svg>')


def jack_ico(c="#8a9198", s=20):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 20 20"><path d="M3 18L10 4l7 14M6 12h8" fill="none" stroke="{c}" stroke-width="1.8"/></svg>'


# ------------------------------------------------------------------------------- pages
def cover():
    return f"""
<section class="page single">
  <img class="abs" src="{url(img(COVER))}" style="left:0;top:0;width:{CW}px;height:{SH}px;object-fit:cover;object-position:40% 30%">
  <div class="abs" style="left:0;top:0;width:{CW}px;height:{SH}px;background:linear-gradient(180deg,rgba(14,16,18,.55) 0%,
       rgba(14,16,18,0) 20%,rgba(14,16,18,0) 50%,rgba(14,16,18,.92) 74%)"></div>
  <svg class="abs" style="left:0;top:{SH - 430}px" width="{CW}" height="430"><polygon points="0,140 {CW},40 {CW},430 0,430" fill="{INK}"/>
    <polygon points="0,140 {CW},40 {CW},52 0,152" fill="{COPPER}"/></svg>
  <div class="abs kicker" style="left:48px;top:48px;color:{WHITE}">Southwire &middot; Power Generation Solutions</div>
  <div class="abs h1" style="left:44px;top:{SH - 300}px;font-size:110px">Built<br><em>to pull.</em></div>
  <div class="abs lede" style="left:48px;top:{SH - 92}px;width:600px">Cable installation solutions for power generation,
    from reel to energised.<br><span class="kicker" style="display:inline-block;margin-top:10px">For EPCs and electrical contractors</span></div>
  <div class="abs small" style="right:48px;bottom:30px">SIMPULL &middot; MAXIS &middot; PREFAB &middot; CONTRACTOR SOLUTIONS</div>
</section>"""


def opening():
    half = SW // 2
    steps = "".join(f"""<div style="text-align:left">{ico(k, 46)}<div class="h3" style="font-size:19px;margin-top:8px">
        <span style="color:{COPPER}">{i + 1:02d}</span> {t}</div><div class="cap" style="margin-top:5px;width:150px">{d}</div></div>"""
                    for i, (k, t, d) in enumerate(STEPS))
    return f"""
<section class="page spread">
  <img class="abs" src="{url(epic('K15'))}" style="left:{half}px;top:0;width:{half}px;height:{SH * .62:.0f}px;object-fit:cover">
  <div class="abs" style="left:{half}px;top:0;width:{half}px;height:{SH * .62:.0f}px;background:linear-gradient(90deg,rgba(14,16,18,1) 0%,rgba(14,16,18,0) 18%)"></div>
  <div class="abs kicker" style="left:56px;top:56px">01 &mdash; The job</div>
  <div class="abs h1" style="left:52px;top:84px;font-size:76px">Every circuit.<br><em>Every pull.</em><br>On schedule.</div>
  <div class="abs lede" style="left:56px;top:350px;width:560px">A 1,700 MW combined-cycle campus with carbon capture,
    battery storage and modular power is more than five million feet of cable, nearly six thousand circuits, and
    hundreds of pulls that all have to happen in the right order, in outage windows, around live plant.</div>
  <div class="abs body" style="left:56px;top:476px;width:560px">This brochure follows that cable through a project, from
    the schedule to the energised plant, and then walks the campus zone by zone: what makes installation different there,
    and what Southwire brings to make it safer, faster and cleaner. Every image and number comes from one 3D model of the
    plant and its cable schedule.</div>
  <div class="abs" style="left:56px;top:640px;display:flex;gap:26px">{stat(TOT['circuits'], 'circuits')}{stat(TOT['cables'], 'cables')}
    {stat(TOT['feet'], 'feet of cable')}{stat(TOT['reels'], 'reels (est.)')}{stat(TOT['classes'], 'voltage classes', 110)}</div>
  <div class="abs" style="left:{half + 56}px;top:{SH * .62 + 40:.0f}px;width:{half - 112}px">
    <div class="kicker">From reel to energised</div>
    <div style="margin-top:20px;display:grid;grid-template-columns:repeat(4,1fr);row-gap:22px;column-gap:16px">{steps}</div></div>
  <div class="abs cap" style="left:{half + 56}px;top:{SH * .62 - 30:.0f}px;color:{WHITE}">SW-3X1 campus at golden hour: three H-class
    GTs, HRSGs and ST, ACC, 230 kV switchyard, carbon capture, BESS and modular power.</div>
  {foot("2 &ndash; 3", SW, 56)}
</section>"""


XCAM = dict(eye=(2550, -1150, 1900), target=(1180, 980, 0), lens=27)


def plan():
    half = SW // 2
    return f"""
<section class="page spread">
  <div class="abs" style="left:0;top:0">{xray_svg(SW, SH, XCAM)}</div>
  <div class="abs" style="left:{half + 120}px;top:0;width:{half - 120}px;height:{SH}px;background:linear-gradient(90deg,rgba(14,16,18,0) 0%,rgba(14,16,18,.92) 22%)"></div>
  <div class="abs" style="left:56px;top:56px">{ico('plan', 54)}</div>
  <div class="abs kicker" style="left:122px;top:66px">02 &mdash; Plan</div>
  <div class="abs h2" style="left:122px;top:88px;font-size:46px">See every cable<br><em>before you pull it.</em></div>
  <div class="abs" style="left:56px;bottom:112px;width:900px">{xray_legend()}</div>
  <div class="abs cap" style="left:56px;bottom:70px;width:900px">Cable X-ray of the SW-3X1 model: 908 routed paths carrying
    the home-run cables of the schedule, coloured by voltage class and weighted by cable count. Device tails to local junction
    boxes are counted, not drawn.</div>
  <div class="abs" style="left:{SW - 56 - 440}px;top:150px;width:440px">
    <div class="lede">Pull planning starts long before the first reel ships. On SW-3X1 every circuit is in the model with its
      route, length, size and voltage-drop check, so reels can be cut to the pull and the pull sequence planned.</div>
    <div style="margin-top:18px">
      <div class="li"><b>Configurator Plus web app</b>plan, manage and order feeder reels from any device</div>
      <div class="li"><b>SIMpull Cable Pull Calculator</b>conduit size and fill, pulling tension, sidewall pressure, jam probability, voltage drop, ground sizing</div>
      <div class="li"><b>Voltage Drop and Conduit Fill calculators</b>size conductors and conduit to NEC from the field</div>
      <div class="li"><b>Contractor Solutions Professionals</b>on site to consult on layouts, pulling calculations and set-up</div>
    </div>
    <div class="kicker" style="margin-top:26px">Routed cable by zone</div>
    <div style="margin-top:10px">{zone_bars(440)}</div>
  </div>
  {foot("4 &ndash; 5", SW, 56, "PLAN")}
</section>"""


ZLIST = [("Turbine hall", ["HALL"]), ("HRSG & stacks", ["HRSG"]), ("ACC", ["ACC"]), ("Electrical buildings", ["ELEC"]),
         ("230 kV switchyard", ["SWYD"]), ("BOP, water & fuel gas", ["BOP", "FUEL"]), ("Carbon capture", ["CCS"]),
         ("BESS", ["BESS"]), ("Modular power", ["MOD-RICE", "MOD-SC", "MOD-TM", "MOD-PORT", "MOD-FC", "MOD-BS", "MOD-COLL"]),
         ("LNG & hydrogen", ["LNGH2"])]


def zone_bars(w):
    rows = [(n, zstats(k)["ft"]) for n, k in ZLIST]
    top = max(f for _, f in rows)
    return "".join(f'<div style="display:grid;grid-template-columns:150px 1fr 60px;align-items:center;column-gap:8px;margin:4px 0">'
                   f'<span class="cap" style="color:{WHITE}">{n}</span><span style="height:8px;background:#2c3036"><span style="display:block;'
                   f'height:8px;width:{100 * f / top:.0f}%;background:{COPPER}"></span></span><span class="cap" style="text-align:right">'
                   f'{fmt_ft(f)} ft</span></div>' for n, f in rows)


def chapter_single(no, kind, title, head, lede, items, hero, hero_cap, inset=None, inset_cap="", page="", extra="", hero_h=560,
                   pos="50%"):
    ins = ""
    if inset:
        ins = f"""<div class="abs" style="right:48px;top:{hero_h - 150}px;width:260px;height:170px;border:2px solid {WHITE};overflow:hidden">
          <img src="{url(inset)}" style="width:100%;height:100%;object-fit:cover"></div>
          <div class="abs cap" style="right:48px;top:{hero_h + 26}px;width:260px;text-align:right">{inset_cap}</div>"""
    lis = "".join(f'<div class="li"><b>{a}</b>{b}</div>' for a, b in items)
    return f"""
<section class="page single">
  <img class="abs" src="{url(hero)}" style="left:0;top:0;width:{CW}px;height:{hero_h}px;object-fit:cover;object-position:50% {pos}">
  <div class="abs" style="left:0;top:0;width:{CW}px;height:{hero_h}px;background:linear-gradient(180deg,rgba(14,16,18,.7) 0%,
       rgba(14,16,18,0) 22%,rgba(14,16,18,0) 70%,rgba(14,16,18,1) 100%)"></div>
  <div class="abs" style="left:44px;top:38px">{ico(kind, 46, WHITE)}</div>
  <div class="abs kicker" style="left:100px;top:52px;color:{WHITE}">{no} &mdash; {title}</div>
  <div class="abs cap" style="left:48px;top:{hero_h - 40}px;width:{CW - 380}px;color:{WHITE}">{hero_cap}</div>
  {ins}
  <div class="abs h2" style="left:48px;top:{hero_h + 14}px;width:{CW - 96}px">{head}</div>
  <div class="abs lede" style="left:48px;top:{hero_h + 108}px;width:{CW - 96}px;font-size:13.5px">{lede}</div>
  <div class="abs" style="left:48px;top:{hero_h + 196}px;width:{CW - 96}px;column-count:2;column-gap:28px">{lis}</div>
  {extra}
  {foot(page, CW, 48, title.upper())}
</section>"""


def deliver():
    return chapter_single(
        "03", "deliver", "Deliver", "The right reel,<br><em>at the right pull.</em>",
        "Reels arrive cut to the length of the pull, paralleled and colour-coded, labelled for the location they feed, and on "
        "payoffs that roll straight to the conduit. On SW-3X1 the SIMpull Truck brings the 13.8 kV collector replacement reels "
        "to the modular-yard pull.",
        [("Simple Distribution", "five fully stocked customer service centers across the US"),
         ("Simple Delivery", "colour, paralleled, cut-to-length reels with SIMpull Heads, delivered on SIMpull payoffs on the SIMpull Truck"),
         ("SIMpull Stack reels", "one reel, up to five coloured conductors per pull and up to four pulls, shrink-wrapped between layers"),
         ("Labelled reels", "each reel tagged for its location, so the job site knows where it goes"),
         ("Rip CHIP", "removes the protective wrap without knives"),
         ("Fewer reels on the job", "less scrap and clean-up, fewer reels to move and set up")],
        epic("E64"), "Modular yard: the SIMpull Truck brings the feeder reels to the 13.8 kV cable pull.",
        epic("E58"), "Reel yard: SIMpull Reels coming off the truck.", "6")


def stage():
    return chapter_single(
        "04", "stage", "Stage", "One person.<br><em>No jacks.</em>",
        "Set-up used to mean reel jacks, axles, pallet jacks and a crew. Staged on SW-3X1's reel yard: SIMpull Reels on Cradles, "
        "45K and 30K Reel Rollers carrying the MV steel reels, SIMpull Flanges on wooden reels and Stack reels on JAX stands, "
        "with the temporary power and lighting to run the yard.",
        [("SIMpull Reel", "61 x 32 in, up to 6,000 lb, moved by one person, fits through 36 in doors"),
         ("SIMpull Cradle", "holds the 61 in reel, pays off directly, forklift and pallet-truck manoeuvrable"),
         ("SIMpull Flange", "shaftless, field-installable on wooden or plastic reels up to 34 in and 2,000 lb"),
         ("RR-SW45 / RR-SW30 Reel Rollers", "45,000 / 30,000 lb, VFD pendant from outside the wire path, stackable"),
         ("Maxis JAX / PRO-JAX", "reel stands that lift reels safely; PRO-JAX to 10,000 lb"),
         ("Temporary power & lighting", "generator to cam-lock cords, 480 V carts, distribution boxes, work lights")],
        img(B5), "The RR-SW45 Reel Roller: a 35 kV MV-105 steel reel on driven rollers, pendant in reach, operator out of the bite.",
        epic("E89"), "Reel yard staging on the SW-3X1 laydown pad.", "7", hero_h=620, pos="72%")


def prefab():
    half = SW // 2
    lis = "".join(f'<div class="li"><b>{a}</b>{b}</div>' for a, b in [
        ("Cable spine modules", "40 ft frames with three ladder-tray tiers, cable laid and tied at the shop, coiled tails at the joint; set, spliced, done"),
        ("Pre-terminated MV assemblies", "cut to length, factory terminations, tested and capped before they ship"),
        ("Skid pre-wire", "JBs, skid-edge tray, conduit and tagged tails at waist height under cover; IR and continuity recorded before the pick"),
        ("Shipping-split interconnects", "PDC e-house splits arrive with pre-terminated interconnects coiled at the split"),
        ("Prefab conduit racks", "multi-conduit bundles on frames, set like structure")])
    return f"""
<section class="page spread">
  <img class="abs" src="{url(epic('E92'))}" style="left:0;top:0;width:{half}px;height:{SH}px;object-fit:cover;object-position:60% 50%">
  <div class="abs" style="left:0;top:0;width:{half}px;height:{SH}px;background:linear-gradient(180deg,rgba(14,16,18,.85) 0%,rgba(14,16,18,0) 30%,rgba(14,16,18,0) 78%,rgba(14,16,18,.9) 100%)"></div>
  <div class="abs" style="left:52px;top:44px">{ico('prefab', 52, WHITE)}</div>
  <div class="abs kicker" style="left:116px;top:58px;color:{WHITE}">05 &mdash; Prefab</div>
  <div class="abs h1" style="left:52px;top:104px;font-size:78px">Pull it once.<br><em>At the shop.</em></div>
  <div class="abs cap" style="left:56px;bottom:46px;width:620px;color:{WHITE}">Modular-yard expansion: spine module 5 of 9 comes
    down on its bents, modules 1-4 already set from the MOD-EH e-house; electricians on the boom lift take the coiled tails.</div>
  <div class="abs" style="left:{half + 48}px;top:48px;width:{half - 96}px;height:330px;overflow:hidden"><img src="{url(epic('E95'))}"
     style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs cap" style="left:{half + 48}px;top:384px;width:{half - 96}px">Skid pre-wire workstation beside the inlet
    chillers and the cable reel yard, away from energised plant: skids wired under cover, tested skids ready to set, a PDC e-house in shipping splits.</div>
  <div class="abs" style="left:{half + 48}px;top:428px;width:250px;height:150px;overflow:hidden"><img src="{url(epic('E94'))}"
     style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs" style="left:{half + 312}px;top:428px;width:250px;height:150px;overflow:hidden"><img src="{url(epic('E93'))}"
     style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs" style="left:{half + 576}px;top:428px;width:{half - 624}px;height:150px;overflow:hidden"><img src="{url(epic('E96'))}"
     style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs lede" style="left:{half + 48}px;top:604px;width:{half - 96}px;font-size:14px">Every hour of cable work moved
    off the critical path and into a shop or a laydown is an hour that does not happen at height, in an outage window, or
    next to live equipment.</div>
  <div class="abs" style="left:{half + 48}px;top:676px;width:{half - 96}px;column-count:2;column-gap:28px">{lis}</div>
  <div class="abs small" style="left:{half + 48}px;bottom:62px;width:{half - 96}px">Prefabricated cable systems are shown
    generically; scope and product names to be confirmed with Southwire.</div>
  {foot("8 &ndash; 9", SW, 56, "PREFAB")}
</section>"""


def pull():
    def side(title, crew, items, note, hl):
        heads = "".join(hardhat(COPPER if hl else "#8a9198", 24) for _ in range(crew))
        gear = "".join(items)
        return f"""<div style="border:1px solid #3a3f45;padding:12px 14px 10px">
          <div class="tag" style="background:{COPPER if hl else '#5b636b'};color:{INK if hl else WHITE}">{title}</div>
          <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:2px">{heads}</div>
          <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:3px">{gear}</div>
          <div class="cap" style="margin-top:6px">{note}</div></div>"""
    trad = side("Traditional", 7, [reel_ico() for _ in range(15)] + [jack_ico() for _ in range(5)],
                "Feeders the traditional way: 15 reels, 1 pallet jack, 5 reel jack stands, 5 axles, 7 electricians.", False)
    simp = side("SIMpull Reel Payoff", 2, [reel_ico(COPPER, 26)],
                "1 SIMpull Reel Payoff, 2 electricians. Example as published in the Southwire SIMpull Solutions brochure.", True)
    extra = f"""<div class="abs" style="left:48px;top:{SH - 250}px;width:{CW - 96}px;display:grid;grid-template-columns:1.35fr 1fr;column-gap:14px">{trad}{simp}</div>"""
    return chapter_single(
        "06", "pull", "Pull", "No lube. Factory heads.<br><em>Fewer hands.</em>",
        "On SW-3X1 the welding-shop feeder goes in as five paralleled SIMpull THHN conductors off one SIMpull Reel, factory "
        "SIMpull Heads straight into the wireway, a tension monitor and a Triggers switch on the pull.",
        [("SIMpull THHN, NoLube", "installs without pulling lubricant into conduit; installation performance guaranteed"),
         ("SIMpull Head grips", "factory-installed, low-profile, staggered; about 3 ft of cable per phase not wasted"),
         ("CoilPAK and BARREL", "pay off straight from the package; BARREL up to 7 conductors for home runs"),
         ("Maxis XD10 / XD1 / Feeder", "up to 10,000 lb; drill-powered 600 lb constant for branch circuits"),
         ("Extreme Duty Tension Monitor", "10,000 lb working load, USB data for the pull record"),
         ("Triggers wireless safety switch", "controls input power to job-site equipment")],
        img(B2), "Factory SIMpull Heads on paralleled SIMpull THHN going into the wireway: no lube, no field-made pulling head.",
        None, "", "10", extra=extra, hero_h=470, pos="62%")


def terminate():
    return chapter_single(
        "07", "test", "Terminate & test", "Terminated, tested,<br><em>recorded.</em>",
        "Turnover is a package of test records. Pre-terminated assemblies arrive tested; skid wiring is meggered at the bench "
        "before the pick; tension-monitor data documents each pull. In the field: MV elbows at the BESS skids, 230 kV sealing "
        "ends at the switchyard, bottom-entry terminations under the switchgear.",
        [("Pre-terminated MV", "factory terminations, tested and capped; fewer field terminations at height"),
         ("Bench testing", "insulation resistance and continuity recorded at the pre-wire workstation"),
         ("Pull records", "tension monitor logs with each pull, ready for the turnover file"),
         ("Printed legends", "every jacket identified in the tray for QA walk-downs"),
         ("ARMOR-X MC-HL", "armored, jacketed cable for trays, racks and hazardous areas"),
         ("230 kV terminations", "cleated risers, sealing ends, arresters, link boxes")],
        epic("E62"), "BESS PCS / MV skid: 34.5 kV elbow terminations to the collector circuit.",
        epic("E60"), "230 kV XLPE sealing ends at the switchyard.", "11")


# ------------------------------------------------------------------------------- zones
def zone_page(n, of, name, sub, keys, hero, hero_cap, inset, inset_cap, diff, sols, page):
    lis = "".join(f'<div class="li"><b>{a}</b>{b}</div>' for a, b in sols)
    dots = "".join(f'<span style="display:inline-block;width:{22 if i == n else 7}px;height:4px;margin-right:5px;'
                   f'background:{COPPER if i == n else "#3a3f45"};border-radius:2px"></span>' for i in range(1, of + 1))
    hh = 600
    return f"""
<section class="page single">
  <img class="abs" src="{url(hero)}" style="left:0;top:0;width:{CW}px;height:{hh}px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:{CW}px;height:{hh}px;background:linear-gradient(180deg,rgba(14,16,18,.7) 0%,
       rgba(14,16,18,0) 22%,rgba(14,16,18,0) 66%,rgba(14,16,18,1) 100%)"></div>
  <div class="abs kicker" style="left:48px;top:42px;color:{WHITE}">Zone playbook {n:02d} of {of:02d} &nbsp;&middot;&nbsp; {sub}</div>
  <div class="abs" style="right:48px;top:{hh - 168}px;width:230px;height:140px;border:2px solid {WHITE};overflow:hidden">
    <img src="{url(inset)}" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs cap" style="right:48px;top:{hh - 22}px;width:230px;text-align:right">{inset_cap}</div>
  <div class="abs cap" style="left:48px;top:{hh - 44}px;width:{CW - 340}px;color:{WHITE}">{hero_cap}</div>
  <div class="abs h1" style="left:46px;top:{hh + 6}px;font-size:{60 if len(name) < 16 else 48}px">{name}</div>
  <div class="abs" style="left:48px;top:{hh + 78}px">{numbers_block(keys)}</div>
  <div class="abs kicker" style="left:48px;top:{hh + 168}px">What's different here</div>
  <div class="abs body" style="left:48px;top:{hh + 190}px;width:{CW - 96}px;font-size:13px">{diff}</div>
  <div class="abs kicker" style="left:48px;top:{hh + 262}px">The installation solution</div>
  <div class="abs" style="left:48px;top:{hh + 284}px;width:{CW - 96}px;column-count:2;column-gap:28px">{lis}</div>
  <div class="abs" style="left:48px;width:{CW - 96}px;bottom:30px;display:flex;justify-content:space-between;align-items:center;
       border-top:1px solid #3a3f45;padding-top:10px"><span>{dots}</span><span class="small">ROUTED HOME-RUN CABLE FROM THE SW-3X1
       MODEL &middot; {page}</span></div>
</section>"""


ZONES = [
    ("Turbine hall", "Power block", ["HALL"], "E66", "GT1 outage: a new 13.8 kV feeder off the RR-SW45 in the laydown bay, up into the EL 48 MV tray.",
     "E97", "Under the deck: stairs and stiles between units.",
     "Outage windows and a crowded hall. MV feeders climb from the laydown bay to trays at EL 41-49 over the machines; reels "
     "are big, floor space is small, and every pull competes with the outage critical path.",
     [("RR-SW45 in the laydown bay", "turns the steel reel from the pendant, operator out of the bite"),
      ("Maxis XD10 + tension monitor", "at the tray drop, pull recorded for turnover"),
      ("Cut-to-length outage reels", "sized and labelled per pull, staged before the unit trips"),
      ("ARMOR-X and MV-105 with legends", "tray identification for QA walk-downs")]),
    ("HRSG & stacks", "Power block", ["HRSG"], "E26", "HRSG 1 west wall: buckstays, SCR doors, downcomers, blowdown tank.",
     "E28", "Stack platforms and the CEMS shelter.",
     "The densest instrumentation on the site: drum levels, thermocouples, CEMS and valve positions on platforms up the "
     "casing, many short runs to junction boxes, then multi-pair home runs to the electrical buildings.",
     [("Cut-to-length instrument reels", "labelled per JB, no wasted tails on the platforms"),
      ("Pre-wired JB skids", "terminated and checked at the bench, set on the platform"),
      ("Maxis XD1", "drill-powered pulls for the short conduit runs at height"),
      ("Prefab conduit racks", "platform conduit set like structure")]),
    ("ACC", "Air-cooled condenser", ["ACC"], "E34", "ACC south-east corner: street risers, stair tower, fan bells under the deck.",
     "E84", "R4: 92 fan VFDs, output trays overhead.",
     "Repetition: 80 fan cells and 12 aux coolers, each with a VFD feeder, control and vibration cables along the fan-bridge "
     "ladders. Identical pulls reward identical reels.",
     [("Stack and paralleled reels", "one reel per street, each pull cut to the cell"),
      ("VFD cable", "symmetrical grounds and shield for the drive outputs"),
      ("Reel labels by cell", "the reel tells the crew where it goes"),
      ("Reel rollers on the deck access road", "staged at the riser, no jacks")]),
    ("Electrical buildings", "R1, R2, R3, R4", ["ELEC"], "E82", "R1: 13.8 kV and 4.16 kV metal-clad lineups across the operating aisle.",
     "E85", "R1 from above, roof and wall off.",
     "Where everything lands: bottom-entry MV terminations over the cable basement, paralleled LV feeder sets to the load "
     "centres and MCCs, and hundreds of control and instrument cables into a few rooms.",
     [("SIMpull paralleled feeder sets", "colour-coded, cut to length, SIMpull Heads factory-fitted"),
      ("Pre-terminated MV", "fewer terminations in the basement"),
      ("NoLube XHHW-2 / THHN", "into conduit without lubricant"),
      ("CoilPAK and BARREL", "lighting, receptacles and small power")]),
    ("230 kV switchyard", "Grid interface", ["SWYD"], "E31", "Bay D2: breakers, disconnects and the control-cable trench to the relay house.",
     "E60", "230 kV XLPE sealing ends.",
     "Two worlds: 230 kV XLPE on heavy steel reels, and hundreds of control and CT / VT circuits in precast trenches from every "
     "breaker back to the relay house.",
     [("RR-SW45 for steel reels", "45,000 lb, stackable, remote pendant"),
      ("Tension-monitored HV pulls", "sidewall pressure planned with the Cable Pull Calculator"),
      ("Control cable cut per bay", "reels labelled by diameter and breaker"),
      ("Contractor Solutions Professionals", "pulling calculations and set-up on site")]),
    ("BOP, water & fuel gas", "Water / utilities / fuel", ["BOP", "FUEL"], "E35", "Tank farm: raw, fire / service and demin water, the fire pump house.",
     "E11", "Plant gas yard: hazardous area.",
     "Many small motor feeders, lighting and receptacles across a spread-out site; in the gas yard and M&R, Class I Div 2 "
     "areas with buried conduit and armored cable.",
     [("CoilPAK, BARREL, wire wagon", "small power and lighting off the package, no broken spools"),
      ("ARMOR-X MC-HL", "hazardous-area power and control"),
      ("SIMpull NoLube in buried conduit", "long underground runs without lube"),
      ("Temporary power and lighting", "for the spread-out work fronts")]),
    ("Carbon capture", "CCS island", ["CCS"], "E39", "Train A: flue duct into the DCC, booster fan, overhead duct to the absorber.",
     "E56", "Absorber A: tray riser and platform lights.",
     "The largest new-build scope on the site: long rack runs up to 2,850 ft, a dense instrument count on absorbers and "
     "strippers, big blower and compressor drives. Built while the plant runs.",
     [("Prefab cable spine on the CCS rack", "modules set with the steel, cable already laid"),
      ("ARMOR-X on racks", "armored runs without conduit"),
      ("Reel rollers and Stack reels", "staged by rack bay"),
      ("Pull planning", "long-run tensions checked before the reels are cut")]),
    ("BESS", "Battery storage", ["BESS"], "E65", "Crew pulling 1,500 V DC conductor into the precast trench.",
     "E62", "PCS / MV skid elbows.",
     "Dozens of identical DC runs from containers to inverters, MV collector circuits to the e-house, and fast schedules.",
     [("Cut-to-length paralleled DC reels", "one reel per block, labelled"),
      ("Maxis JAX stands", "at the trench edge, no red jacks"),
      ("SIMpull Head grips", "pre-made, no field heads in the trench"),
      ("PV / RHW-2 2 kV and MV-105 35 kV", "DC and collector cable")]),
    ("LNG & hydrogen", "Fuel supply", ["LNGH2"], "E45", "LNG satellite: unloading arms, vaporizers, tanks in the impoundment.",
     "E46", "Green hydrogen: electrolyzers and compressors.",
     "Hazardous and cryogenic areas, intrinsically safe instrumentation, and the longest runs on the site, up to 5,160 ft "
     "to the send-out and electrolyzer buildings.",
     [("ARMOR-X MC-HL", "hazardous-area power and control"),
      ("ITC / PLTC (IS)", "intrinsically safe instrument runs"),
      ("Long-length reels on rollers", "fewer splices on the long runs"),
      ("Cable Pull Calculator", "tensions and sidewall pressure for the long pulls")]),
]


def modular_spread():
    half = SW // 2
    types = [("Permanent: RICE and simple-cycle", ["MOD-RICE", "MOD-SC", "MOD-COLL"], "E14",
              "8 RICE engines and two 50 MW-class aeroderivative units: buried duct banks to the collector, skids pre-wired in the laydown, the "
              "prefab spine for LV / control / fibre.", "Prefab spine, skid pre-wire, SIMpull NoLube in duct banks"),
             ("Bridge & temporary: trailer turbines, gensets, portable pad", ["MOD-TM", "MOD-PORT"], "E77",
              "Power for months, not decades: cable on grade in ground trays, Type SHD-GC 15 kV and Type W with cam-locks, "
              "drive-over protectors.", "SHD-GC, Type W, cam-locks, temporary power & lighting"),
             ("Small factory skids: fuel cells, microturbines", ["MOD-FC"], "E17",
              "Factory-built modules with short, repetitive connections: pre-wired, tested, set and connected.",
              "Pre-wired skids, CoilPAK / BARREL for small power"),
             ("Black start & emergency gensets", ["MOD-BS"], "E33", "Critical circuits that must work first time: tested and recorded.",
              "Tested assemblies, records for turnover")]
    cards = ""
    for t, keys, im, txt, sol in types:
        a = zstats(keys)
        cards += f"""<div style="display:grid;grid-template-columns:280px 1fr;column-gap:18px;border-top:1px solid #2c3036;padding:14px 0">
          <div style="width:280px;height:168px;overflow:hidden"><img src="{url(epic(im))}" style="width:100%;height:100%;object-fit:cover"></div>
          <div><div class="h3" style="font-size:19px">{t}</div><div class="cap" style="margin-top:6px;color:{GREY};font-size:11.5px">{txt}</div>
            <div style="margin-top:8px;display:flex;gap:20px;align-items:end">{stat(f"{a['circ']:,}", "circuits", 80)}
              {stat(fmt_ft(a['ft']), "ft routed", 90)}<div class="cap" style="color:{COPPER_L};width:220px">{sol}</div></div></div></div>"""
    return f"""
<section class="page spread">
  <img class="abs" src="{url(epic('E80'))}" style="left:0;top:0;width:{half}px;height:{SH}px;object-fit:cover;object-position:50% 50%">
  <div class="abs" style="left:0;top:0;width:{half}px;height:{SH}px;background:linear-gradient(180deg,rgba(14,16,18,.96) 0%,rgba(14,16,18,.9) 30%,rgba(14,16,18,.25) 52%,rgba(14,16,18,.2) 76%,rgba(14,16,18,.95) 100%)"></div>
  <div class="abs kicker" style="left:56px;top:56px;color:{WHITE}">Zone playbook 09 of 10 &nbsp;&middot;&nbsp; Modular power</div>
  <div class="abs h1" style="left:52px;top:86px;font-size:84px">Modular<br><em>power.</em></div>
  <div class="abs lede" style="left:56px;top:290px;width:560px">Six technologies, three ways of cabling them. What changes
    is how long the power is meant to stay: permanent units get duct banks and prefab; bridge power goes on grade; factory
    skids arrive pre-wired.</div>
  <div class="abs" style="left:56px;bottom:66px">{numbers_block(["MOD-RICE", "MOD-SC", "MOD-TM", "MOD-PORT", "MOD-FC", "MOD-BS", "MOD-COLL"], half - 112)}</div>
  <div class="abs" style="left:{half + 48}px;top:48px;width:{half - 96}px">{cards}</div>
  <div class="abs" style="left:{half + 48}px;top:{SH - 186}px;width:{half - 96}px;height:112px;overflow:hidden;display:grid;
       grid-template-columns:1fr 1fr 1fr;gap:8px"><img src="{url(epic('E92'))}" style="width:100%;height:100%;object-fit:cover">
       <img src="{url(epic('E72'))}" style="width:100%;height:100%;object-fit:cover"><img src="{url(epic('E78'))}"
       style="width:100%;height:100%;object-fit:cover"></div>
  {foot("20 &ndash; 21", SW, 56, "ZONE PLAYBOOK")}
</section>"""


def operate():
    return chapter_single(
        "08", "operate", "Operate & support", "We are where<br><em>you are.</em>",
        "The plant runs for decades and every outage brings cable back to the critical path. Southwire stays on the job: "
        "people on site, training for the crews, distribution close by, and a guarantee behind the cable.",
        [("Contractor Solutions Professionals", "on the jobsite for layouts, pulling calculations and set-up, with equipment to demo"),
         ("Southwire Solutions University", "hands-on training at the Thorn Customer Solutions Center, Carrollton, GA (15,000 sq ft)"),
         ("SIMpull Product Performance Guarantee", "SIMpull conductors install without lubricant as specified, or Southwire reimburses direct replacement costs (terms apply)"),
         ("Outage support", "cut-to-length reels, SIMpull Truck delivery and reel rollers staged ahead of the trip"),
         ("Simple Distribution", "five customer service centers"),
         ("Tools & equipment", "Maxis pullers, Triggers, temporary power and lighting")],
        epic("E87"), "Main control room: over the operator's shoulder, the plant on the video wall.",
        epic("E86"), "Six-position console and the 16-cube wall.", "23")


def back():
    return f"""
<section class="page single">
  <img class="abs" src="{url(epic('K15'))}" style="left:0;top:0;width:{CW}px;height:{SH}px;object-fit:cover;object-position:50% 40%">
  <div class="abs" style="left:0;top:0;width:{CW}px;height:{SH}px;background:linear-gradient(180deg,rgba(14,16,18,.2) 0%,rgba(14,16,18,.4) 45%,rgba(14,16,18,.96) 70%)"></div>
  <div class="abs h1" style="left:46px;top:{SH - 400}px;font-size:66px">Don't just pull.<br><em>Pull ahead.</em></div>
  <div class="abs lede" style="left:48px;top:{SH - 250}px;width:560px">Southwire Power Generation Solutions: cable, installation
    solutions and people for the plants that power everything else.</div>
  <div class="abs" style="left:48px;top:{SH - 170}px;font:800 22px/1.3 BC;color:{WHITE};letter-spacing:.04em">SOUTHWIRE.COM &nbsp;|&nbsp; (855) 798-6657</div>
  <div class="abs" style="left:48px;top:{SH - 120}px;border:2px solid {WHITE};padding:8px 12px;font:800 15px/1.15 BC;color:{WHITE};
       letter-spacing:.06em">BUILT FOR DURABILITY.<br>BUILT FOR RELIABILITY.<br>BUILT FOR WORK.</div>
  <div class="abs small" style="right:48px;bottom:30px;width:320px;text-align:right">Images and quantities from the SW-3X1 conceptual
    3D model: illustration, not engineered, not for construction. Product data as published by Southwire; confirm against
    current specifications.</div>
</section>"""


COVER = os.path.join(PLANT, "renders", "brochure_epc", "_src", "B1_pro_clean.jpg")
B2 = os.path.join(PLANT, "renders", "brochure_epc", "_src", "B2_pro_clean.jpg")
B5 = os.path.join(PLANT, "renders", "brochure_epc", "_src", "B5_pro_clean.jpg")


def main():
    os.makedirs(OUT, exist_ok=True)
    bz.OUT = OUT
    pages = [cover(), opening(), plan(), deliver(), stage(), prefab(), pull(), terminate()]
    pn = 12
    for k, z in enumerate(ZONES):
        if z[0] == "LNG & hydrogen":
            pages.append(modular_spread())
            pn += 2
        name, sub, keys, hero, hc, ins, ic, diff, sols = z
        n = k + 1 if z[0] != "LNG & hydrogen" else 10
        pages.append(zone_page(n, 10, name, sub, keys, epic(hero), hc, epic(ins), ic, diff, sols, str(pn)))
        pn += 1
    pages += [operate(), back()]
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + "".join(pages) + "</body></html>"
    hp = os.path.join(OUT, "built_to_pull.html")
    open(hp, "w").write(html)
    import pymupdf
    head, rest = html.split("<body>", 1)
    out = pymupdf.open()
    secs = re.findall(r"<section.*?</section>", rest, re.S)
    for i, sec in enumerate(secs):
        hp_i = hp.replace(".html", f"_{i}.html")
        open(hp_i, "w").write(head + "<body>" + sec + "</body></html>")
        pdf_i = hp_i.replace(".html", ".pdf")
        subprocess.run([bz.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf_i}", url(hp_i)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.insert_pdf(pymupdf.open(pdf_i))
        os.remove(pdf_i)
        os.remove(hp_i)
    pdf = os.path.join(OUT, "SW_BuiltToPull_EPC.pdf")
    out.save(pdf, garbage=3, deflate=True)
    import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), "tools"))
    import stamp_credit; stamp_credit.stamp(pdf)                       # author credit on every page
    for i, pg in enumerate(out):
        pg.get_pixmap(dpi=40).save(os.path.join(OUT, f"prev_{i + 1:02d}.png"))
    print("wrote", pdf, len(out), "sheets")


if __name__ == "__main__":
    main()
