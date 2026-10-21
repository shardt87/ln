"""'Built for the next generation of power': a 6-page section for the brochure (owner, Oct 20): the campus as a
modernised power plant - what changed from the plants of the last decades, the new technology and the cable behind
it, green hydrogen and carbon capture, faster and smarter construction (prefab, pre-wired pads, the Southwire tools),
and sustainability with Southwire's Formula E partnership.

Design system and helpers of the EPC edition (brochure_epc.py / brochure_zones.py). US Letter pages:
  1 opener | 2 then / now | 3 the modern campus | 4 decarbonisation | 5 built faster, built smarter
  6 sustainability and Formula E (photo / logo placeholder until brand approval)

Images: renders/nextgen/_src/*_pro_clean.jpg (fresh: E123, SC3, SC7, AW1, T5G1) and renders/epic (CCS, H2).
Plant figures as on the campus information sign (approximate). Formula E facts as published by Southwire and Formula E
(March 2023 announcement); its sustainability claims are quoted as the series' own.

    python blender/brochure_nextgen.py      # -> renders/nextgen/SW_NextGenPower.pdf + page previews
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brochure_epc as be                                       # noqa: E402
import brochure_zones as bz                                     # noqa: E402

PLANT = bz.PLANT
OUT = os.path.join(PLANT, "renders", "nextgen")
SRC = os.path.join(OUT, "_src")
url = bz.url
CW, SH = bz.CW, bz.SH
COPPER, INK, WHITE, GREY = bz.COPPER, bz.INK, bz.WHITE, bz.GREY
CSS = be.CSS + f"""
.row {{ display: grid; grid-template-columns: 150px 1fr 1fr; border-top: 1px solid #2c3036; }}
.row div {{ padding: 9px 10px 9px 0; font: 400 11.5px/1.4 B; color: {GREY}; }}
.row .k {{ font: 700 12px/1.3 BC; letter-spacing: .08em; color: {WHITE}; text-transform: uppercase; }}
.row .now {{ color: {WHITE}; }}
.hd div {{ font: 700 11px/1 BC !important; letter-spacing: .2em; color: {COPPER} !important; text-transform: uppercase; }}
.ph {{ border: 2px dashed #5b6168; display: flex; align-items: center; justify-content: center; text-align: center;
       font: 700 12px/1.5 BC; letter-spacing: .14em; color: #7d848b; text-transform: uppercase; }}
"""


def src(k):
    p = os.path.join(SRC, f"{k}_pro_clean.jpg")
    return be.img(p if os.path.exists(p) else os.path.join(SRC, f"{k}_pro.png"))


def foot(page_no):
    return (f'<div class="abs" style="left:48px;width:{CW - 96}px;bottom:30px;display:flex;justify-content:space-between;'
            f'align-items:center;border-top:1px solid #3a3f45;padding-top:10px"><span class="small">SOUTHWIRE &middot; '
            f'POWER GENERATION SOLUTIONS &middot; NEXT-GENERATION POWER</span><span class="small">{page_no}</span></div>')


def chapter(no, title, head, lede, items, hero, hero_cap, inset=None, inset_cap="", page="", hero_h=540, pos="50%"):
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
  <div class="abs kicker" style="left:48px;top:52px;color:{WHITE}">{no} &mdash; {title}</div>
  <div class="abs cap" style="left:48px;top:{hero_h - 40}px;width:{CW - 380}px;color:{WHITE}">{hero_cap}</div>
  {ins}
  <div class="abs h2" style="left:48px;top:{hero_h + 14}px;width:{CW - 96}px">{head}</div>
  <div class="abs lede" style="left:48px;top:{hero_h + 108}px;width:{CW - 96}px;font-size:13.5px">{lede}</div>
  <div class="abs" style="left:48px;top:{hero_h + 200}px;width:{CW - 96}px;column-count:2;column-gap:28px">{lis}</div>
  {foot(page)}
</section>"""


# ------------------------------------------------------------------------------- pages
def opener():
    return f"""
<section class="page single">
  <img class="abs" src="{url(src('E123'))}" style="left:0;top:0;width:{CW}px;height:{SH}px;object-fit:cover;object-position:55% 40%">
  <div class="abs" style="left:0;top:0;width:{CW}px;height:{SH}px;background:linear-gradient(180deg,rgba(14,16,18,.6) 0%,
       rgba(14,16,18,0) 22%,rgba(14,16,18,0) 48%,rgba(14,16,18,.95) 72%)"></div>
  <svg class="abs" style="left:0;top:{SH - 420}px" width="{CW}" height="420"><polygon points="0,130 {CW},40 {CW},420 0,420" fill="{INK}"/>
    <polygon points="0,130 {CW},40 {CW},52 0,142" fill="{COPPER}"/></svg>
  <div class="abs kicker" style="left:48px;top:48px;color:{WHITE}">Southwire &middot; Power Generation Solutions</div>
  <div class="abs h1" style="left:44px;top:{SH - 352}px;font-size:70px">Built for the<br><em>next generation</em><br>of power.</div>
  <div class="abs lede" style="left:48px;top:{SH - 118}px;width:{CW - 96}px">The power plant has changed. One gas plant
    selling megawatt-hours has become a campus: efficient combined cycle, fast modular power, battery storage, carbon
    capture, green hydrogen and the data centres that now drive demand. Here is what changed, and the cable that makes it work.</div>
</section>"""


ROWS = [("The plant", "One gas plant, one product: MWh", "A campus: ~1,350 MW combined cycle, ~339 MW modular power, battery storage, a data centre"),
        ("Flexibility", "Baseload, slow starts", "RICE engines and aeroderivatives on in minutes; batteries absorb the swings"),
        ("Emissions", "Treated as a cost of running", "Carbon capture on the HRSG exhaust; hydrogen blended into the gas turbines"),
        ("Fuel", "Natural gas only", "Gas today, green hydrogen from a 25 MW electrolyser on site, hydrogen-ready turbines"),
        ("Cable install", "Pulled piece by piece, on site", "Prefab cable modules, pre-terminated MV, pads pre-wired before the equipment arrives"),
        ("Set-up", "Reel jacks, axles and a crew", "SIMpull Reels, BARRELs and CoilPAKs one person moves; Maxis pullers and feeders"),
        ("Connectivity", "Copper and paper, manual rounds", "Fibre backbone, private 5G / LTE, licence-plate cameras, access control"),
        ("Design", "2D drawings, field-routed cable", "One 3D model: every circuit routed, sized and scheduled before the first pull")]


def then_now():
    rows = "".join(f'<div class="row"><div class="k">{k}</div><div>{a}</div><div class="now">{b}</div></div>' for k, a, b in ROWS)
    return f"""
<section class="page single">
  <div class="abs kicker" style="left:48px;top:52px">01 &mdash; What changed</div>
  <div class="abs h2" style="left:48px;top:84px;width:{CW - 96}px;font-size:46px">Then and <em>now.</em></div>
  <div class="abs lede" style="left:48px;top:150px;width:{CW - 96}px;font-size:13.5px">Plants built in the last
    decades were designed to run steady and sell energy. The plant of the next generation has to start fast, follow
    renewables, cut its emissions and power new loads, and it has to be built faster. Every one of those changes runs
    on cable.</div>
  <div class="abs" style="left:48px;top:250px;width:{CW - 96}px">
    <div class="row hd"><div></div><div>Then</div><div>Now: SW-3X1</div></div>{rows}</div>
  <div class="abs" style="left:48px;top:{SH - 290}px;width:{(CW - 112) // 2}px;height:170px;overflow:hidden">
    <img src="{url(src('SC3'))}" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="abs" style="left:{48 + (CW - 112) // 2 + 16}px;top:{SH - 290}px;width:{(CW - 112) // 2}px;height:170px;overflow:hidden">
    <img src="{url(src('T5G1'))}" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%"></div>
  <div class="abs cap" style="left:48px;top:{SH - 112}px;width:{(CW - 112) // 2}px">Simple-cycle pair, stacks together and
    inlets outboard: fast-start power beside the combined cycle.</div>
  <div class="abs cap" style="left:{48 + (CW - 112) // 2 + 16}px;top:{SH - 112}px;width:{(CW - 112) // 2}px">Private 5G /
    LTE monopole: the plant network for cameras, sensors and crews.</div>
  {foot(2)}
</section>"""


def campus():
    return chapter(
        "02", "The modern campus", "One campus.<br><em>Many technologies.</em>",
        "SW-3X1 pairs an efficient 3x1 H-class combined cycle with modular power that starts in minutes, battery storage "
        "that absorbs the swings, and the behind-the-meter data centre that is today's fastest-growing load. Each one is "
        "a different cable job, from 230 kV to Cat 6A.",
        [("Combined cycle", "3 H-class gas turbines, 3 HRSGs, 1 steam turbine: ~1,350 MW of efficient baseload"),
         ("Modular power", "RICE engines 144 MW, simple cycle 100 MW, mobile turbines 70 MW, gensets, fuel cells"),
         ("Battery storage", "~60 MW / 120 MWh to smooth renewables and bridge starts"),
         ("Data centre", "~150 MW of IT load fed behind the meter from the modular yard"),
         ("Reserved for growth", "SC-3 / SC-4 pad poured and pre-wired: phase two plugs in"),
         ("The cable", "HV, MV-105, TC-ER, ARMOR-X MC-HL, DC, instrumentation, fibre: one schedule, one supplier")],
        be.img(os.path.join(PLANT, "renders", "cover", "HX1_hero_cable.jpg")),
        "The power block with its cable runs highlighted in copper.",
        src("SC3"), "Fast-start simple-cycle pair in the modular yard.", "3")


def decarb():
    ep = os.path.join(PLANT, "renders", "epic")
    return chapter(
        "03", "Decarbonisation", "Lower carbon,<br><em>built in.</em>",
        "Carbon capture takes CO2 out of the exhaust before it reaches the stack. A 25 MW PEM electrolyser makes green "
        "hydrogen on site from renewable or surplus power, and the gas turbines are ready to burn it blended with natural "
        "gas. Each system brings its own cable: hazardous-area, high-current DC and dense instrumentation.",
        [("Carbon capture", "amine absorbers on the HRSG exhaust, strippers, CO2 compression for transport"),
         ("Green hydrogen", "25 MW PEM electrolysis, ~10.8 t / day, rectifiers and DC buses"),
         ("Hydrogen-ready", "receiving station, blending skid and hydrogen-capable turbines"),
         ("Hazardous areas", "ARMOR-X MC-HL power and control where gas and hydrogen are handled"),
         ("High-current DC", "2 kV DC conductors from rectifiers to stacks on dedicated tray"),
         ("Instrumentation", "shielded PLTC / ITC for the analysers, ESD and safety systems")],
        be.img(os.path.join(ep, "E118_pro_clean.jpg")),
        "Carbon capture: absorbers A-C, strippers and compression beyond.",
        be.img(os.path.join(ep, "E106_pro_clean.jpg")), "Electrolyser hall: PEM skids, rectifiers and the DC cable trays.", "4")


def faster():
    return chapter(
        "04", "Built faster, built smarter", "Wired before<br><em>it arrives.</em>",
        "The modern plant is built in parallel. Cable systems are made in the factory, tested, and set on pads that are "
        "pre-wired before the equipment lands; inside, the crews pull with tools that take the jacks, lube and guesswork "
        "out of the job. On SW-3X1 the SC-4 pad shows it: everything but the turbine is in.",
        [("Prefab cable modules", "40 ft factory modules: power, control and fibre tiers laid, tied and tested"),
         ("Plug-and-play pads", "pigtails coiled and tagged at every landing: set, connect, energise"),
         ("SIMpull", "cut-to-length, paralleled reels and BARRELs, no lube, factory pulling heads"),
         ("Maxis", "XD10 pullers and feeders with tension monitoring and Triggers safety switch"),
         ("Digital model", "every circuit routed and sized in one model; the schedule and BOM come from it"),
         ("Fit-out", "MC branch circuits, Cat 6A, FPLR fire alarm and fibre, from the same supplier")],
        src("SC7"), "SC-4 reserved pad: prefab cable modules installed, pigtails waiting at each landing point.",
        src("AW1"), "Office fit-out: MC, Cat 6A on J-hooks, SIMpull and Maxis on the floor.", "5")


def sustain():
    return f"""
<section class="page single">
  <div class="abs kicker" style="left:48px;top:52px">05 &mdash; Sustainability</div>
  <div class="abs h2" style="left:48px;top:84px;width:{CW - 96}px;font-size:46px">From the track<br><em>to the turbine.</em></div>
  <div class="abs lede" style="left:48px;top:206px;width:{CW - 96}px;font-size:13.5px">Sustainability at Southwire is a
    commitment, not a campaign: making cable responsibly, helping customers build with less waste, and putting
    electrification to work wherever it is needed, from the grid to the race track.</div>
  <div class="abs ph" style="left:48px;top:300px;width:{CW - 96}px;height:250px"><div>Formula E photo + logo<br>
    <span style="font-weight:400;letter-spacing:.06em">insert after brand approval</span></div></div>
  <div class="abs" style="left:48px;top:574px;width:{CW - 96}px;column-count:2;column-gap:28px">
    <div class="li"><b>Formula E</b>Southwire is Formula E's Official Wire and Cable Provider, announced in March 2023
      for the 2022/23 season.</div>
    <div class="li"><b>Net-zero racing</b>Formula E describes itself as carbon neutral since its first season in 2014,
      and as the most sustainable sport (Global Sustainability Benchmark in Sports, 2023).</div>
    <div class="li"><b>Same know-how</b>The electrification that powers an all-electric race series is the same that
      powers batteries, electrolysers and the cable runs of a modern plant.</div>
    <div class="li"><b>Less waste on site</b>Cut-to-length reels, returnable reels and payoffs, no pulling lube, fewer
      reels to handle and dispose of.</div>
    <div class="li"><b>Built in the plant</b>Prefab and pre-wired pads move work into the factory: fewer hours on site,
      safer crews, less rework.</div>
    <div class="li"><b>Southwire sustainability</b>The company's sustainability commitments: see southwire.com for the
      current programme.</div></div>
  <div class="abs h3" style="left:48px;top:{SH - 128}px;width:{CW - 96}px;font-size:26px">Southwire: wiring the
    <em>energy transition.</em></div>
  <div class="abs small" style="left:48px;top:{SH - 90}px;width:{CW - 96}px">Plant images and figures from the SW-3X1
    conceptual 3D model: illustration, not engineered, ratings approximate. Formula E facts as published by Southwire and
    Formula E; sustainability claims are the series' own.</div>
  {foot(6)}
</section>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    bz.OUT = OUT
    pages = [opener(), then_now(), campus(), decarb(), faster(), sustain()]
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + "".join(pages) + "</body></html>"
    hp = os.path.join(OUT, "next_gen.html")
    open(hp, "w").write(html)
    import pymupdf
    head, rest = html.split("<body>", 1)
    out = pymupdf.open()
    for i, sec in enumerate(re.findall(r"<section.*?</section>", rest, re.S)):
        hp_i = hp.replace(".html", f"_{i}.html")
        open(hp_i, "w").write(head + "<body>" + sec + "</body></html>")
        pdf_i = hp_i.replace(".html", ".pdf")
        subprocess.run([bz.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf_i}", url(hp_i)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.insert_pdf(pymupdf.open(pdf_i))
        os.remove(pdf_i)
        os.remove(hp_i)
    pdf = os.path.join(OUT, "SW_NextGenPower.pdf")
    out.save(pdf, garbage=3, deflate=True)
    sys.path.insert(0, os.path.join(PLANT, "tools"))
    import stamp_credit
    stamp_credit.stamp(pdf)                                         # author credit on pages 2 onward
    for i, pg in enumerate(out):
        pg.get_pixmap(dpi=40).save(os.path.join(OUT, f"prev_{i + 1:02d}.png"))
    print("wrote", pdf, len(out), "pages")


if __name__ == "__main__":
    main()
