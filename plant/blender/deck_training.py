"""Nov 11 internal training "Inside Power Generation" (presentation/Nov11_run_of_show.md): 59 slides at 1440 x 810 (main 1-52, backup 53-59),
same look as the boiler deck. Reuses the boiler-deck slides for the fundamentals and the cable takeaways (their footers
re-numbered), the 16-zone overview, and the model renders for the seven tour stops; new: title, agenda, six market slides
(from the Oct 6 PowerGen channel deck), one slide per tour stop, the whole
plant in one number (from the cable schedule), three things to remember.

    python3 blender/deck_training.py      -> renders/deck/training/SW-3X1_Nov11_training.pdf (+ PNG per slide)
"""
import math
import os
import re
import subprocess

import brochure_zones as bz
import credit
import deck_boilers as db

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
OUT = os.path.join(PLANT, "renders", "deck", "training")
COPPER, INK, WHITE, GREY = bz.COPPER, bz.INK, bz.WHITE, bz.GREY
TITLE = "INSIDE POWER GENERATION"
LOGO = bz.url(os.path.join(HERE, "deck", "southwire_pgs_logo.png"))       # Southwire Power Generation Solutions (white type)


def pic(rel):
    """The newest render of a view: the full-quality boilers_full copy, the raw *_pro.png (the Oct 17 full renders the
    strategy deck and brochure use) or the finished *_pro_clean.jpg, whichever was written last."""
    d, f = os.path.split(os.path.join(PLANT, rel))
    k = f.split("_pro")[0] if "_pro" in f else None
    cands = [os.path.join(PLANT, rel), os.path.join(PLANT, "renders", "boilers_full", f)]
    if k:
        cands += [os.path.join(d, f"{k}_pro.png"), os.path.join(d, f"{k}_pro_clean.jpg")]
    cands = [c for c in cands if os.path.exists(c)]
    if not cands:
        raise FileNotFoundError(rel)
    path = max(cands, key=os.path.getmtime)
    if os.path.getsize(path) > 250e3:                                  # embed at slide resolution to keep the PDF small
        import tempfile
        from PIL import Image
        im = Image.open(path)
        icon = "/icons/" in path                                        # cable icons keep their transparency
        out = os.path.join(tempfile.gettempdir(), "deck_training_" + os.path.basename(os.path.dirname(path)) + "_"
                           + os.path.splitext(os.path.basename(path))[0] + (".png" if icon else ".jpg"))
        if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(path):
            im.thumbnail((360, 360) if icon else (1920, 1920))
            (im.save(out) if icon else im.convert("RGB").save(out, quality=84))
        path = out
    return bz.url(path)


def capimg(src, w, h, cap, pos="50% 50%", extra=""):
    """A picture with its name on it: small renders are only readable with a caption."""
    return (f'<div style="position:relative;width:{w}px;height:{h}px;{extra}"><img src="{pic(src)}" style="width:{w}px;height:{h}px;object-fit:cover;'
            f'object-position:{pos};display:block"><div style="position:absolute;left:0;right:0;bottom:0;padding:16px 10px 6px;'
            f'background:linear-gradient(180deg,rgba(14,16,18,0),rgba(14,16,18,.88));font:700 13px/1 BC;letter-spacing:.08em;color:#f4f1ec;'
            f'text-transform:uppercase">{cap}</div></div>')


def foot(n, N, left="SW-3X1 MODEL &middot; CONCEPTUAL ILLUSTRATION, NOT ENGINEERED &middot; INTERNAL TRAINING"):
    return (f'<div class="abs foot" style="left:64px;right:64px;bottom:26px;display:flex;justify-content:space-between;'
            f'border-top:1px solid #2c3036;padding-top:11px"><span>{left}</span><span>{credit.EMAIL} &nbsp;&middot;&nbsp; '
            f'{TITLE} {n}/{N}</span></div>')


def placeholder(w, h, text):
    return (f'<div style="width:{w}px;height:{h}px;border:2px dashed #f2c200;border-radius:6px;display:flex;align-items:center;'
            f'justify-content:center;text-align:center;font:700 12px/1.35 BC;letter-spacing:.08em;color:#f2c200;'
            f'text-transform:uppercase;padding:8px">{text}</div>')


# ---------------------------------------------------------------------------------------------------------------- slides
def s_title():
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/brochure_epc/_img/K15_pro.jpg')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover;object-position:50% 62%">
  <div class="abs" style="left:0;top:0;width:1440px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,.95) 0%,
       rgba(14,16,18,.82) 34%,rgba(14,16,18,0) 62%)"></div>
  <img class="abs" src="{LOGO}" style="left:72px;top:58px;width:300px">
  <div class="abs kicker" style="left:72px;top:170px;font-size:14px">Southwire internal training &nbsp;&middot;&nbsp; November 11, 2026</div>
  <div class="abs h2" style="left:70px;top:204px;font-size:92px;width:760px">Inside power <em>generation</em></div>
  <div class="abs lede" style="left:72px;top:414px;width:520px;font-size:21px">A guided tour of a gas power campus: how it works,
    the equipment and electrical systems, and where wire and cable go.</div>
  <div class="abs" style="left:72px;top:556px;font:700 15px/1.5 BC;letter-spacing:.14em;color:{WHITE};text-transform:uppercase">
    1:30 &ndash; 2:30 PM &nbsp;&middot;&nbsp; Zoom<br><span style="color:{GREY}">Hosted by Stephan Hardt</span></div>
</section>"""


AGENDA = [("1:30", "Welcome", "why this matters", "2"),
          ("1:32", "Market and fundamentals", "how power is made, the gas build; the machines, the grid, cable, who buys", "28"),
          ("2:00", "The 3D tour", "seven stops: what it does, its electrical system, its cable", "18"),
          ("2:18", "Wire and cable takeaways", "the whole plant in one number, products, pain points", "6"),
          ("2:24", "Q&amp;A", "questions from the chat", "6")]


def s_agenda(n, N):
    rows = "".join(f'<div style="display:flex;gap:28px;align-items:baseline;padding:20px 0;border-top:1px solid #2c3036">'
                   f'<div style="width:90px;font:800 30px/1 BC;color:{COPPER}">{t}</div>'
                   f'<div style="flex:1"><div style="font:800 30px/1 BC;color:{WHITE};text-transform:uppercase;letter-spacing:.02em">{h}</div>'
                   f'<div style="font:400 16px/1.4 B;color:{GREY};margin-top:6px">{s}</div></div>'
                   f'<div style="font:700 15px/1 BC;letter-spacing:.14em;color:{GREY}">{m} MIN</div></div>' for t, h, s, m in AGENDA)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Today &nbsp;&middot;&nbsp; 60 minutes</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">The <em>hour</em></div>
  <div class="abs" style="left:64px;top:176px;width:1000px">{rows}</div>
  <div class="abs lede" style="left:1110px;top:186px;width:270px;font-size:15px">No engineering background needed. At every stop
    you get three things: <b style="color:{WHITE}">what it does</b>, its <b style="color:{WHITE}">electrical system</b>, and
    <b style="color:{WHITE}">the cable</b>.<br><br>Questions in the chat; we answer them at the end.</div>
  {foot(n, N)}
</section>"""


def s_why(n, N):
    cards = [("Demand is growing again", "Data centres and AI, manufacturing coming back, electrification of everything.",
              "Market figure: load growth / data-centre demand, from Southwire market intelligence"),
             ("Firm power", "Gas plants run when they are needed, day or night, and back up wind and solar.",
              "Market figure: new gas capacity planned / under construction"),
             ("Three ways it buys cable", "New gas plants, modular and behind-the-meter power at the customer, and upgrades of "
              "the existing fleet.", "Market figure: size of the power-generation cable market for Southwire")]
    html = ""
    for k, (h, t, ph) in enumerate(cards):
        x = 64 + k * 444
        html += (f'<div class="abs" style="left:{x}px;top:214px;width:420px;height:420px;background:#181b1f;border-top:3px solid {COPPER};'
                 f'border-radius:3px;padding:24px 26px;box-sizing:border-box">'
                 f'<div class="cnum">0{k + 1}</div><div class="ct" style="font-size:30px;margin-top:10px">{h}</div>'
                 f'<div class="cd" style="font-size:16px;margin-top:12px">{t}</div>'
                 f'<div style="position:absolute;left:26px;right:26px;bottom:26px">{placeholder(368, 150, ph)}</div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals and market</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Why gas, <em>why now</em></div>
  <div class="abs lede" style="left:64px;top:162px;width:1100px;font-size:17px">Message: new gas build, modular and behind-the-meter
    generation, and upgrades to the existing fleet all need cable.</div>
  {html}
  {foot(n, N)}
</section>"""


# Market section: from the Oct 6 PowerGen channel deck (pages 3, 5-10, 14), restyled; OEM, owner and EPC names stay in
# the talking points (presentation/Nov11_run_of_show.md), not on the slides.
SRC = "font:400 12px/1.4 B;color:#80868c"
ADDED = [1.9, 3.0, 5.0, 8.9, 21.9, 40.0, 57.0, 48.9, 20.0, 15.0, 8.9, 8.9, 8.9, 8.9, 7.0, 8.9, 8.9, 7.0, 6.1, 6.4, 8.6,
         11.1, 19.2, 8.3, 7.0, 6.4, 5.6, 8.6, 3.9, 3.6, 6.3]               # US gas GW added per year, 1996-2026 (provisional)
POS = [(2026, 98, 0, 13.2), (2027, 133, 0, 17.0), (2028, 165, 4, 20.7), (2029, 157, 13, 21.2), (2030, 83, 31, 14.7),
       (2031, 21, 53, 9.5), (2032, 10, 78, 11.1), (2033, 5, 97, 13.2), (2034, 1, 109, 14.3), (2035, 0, 115, 14.9)]


def tile(x, y, w, h, kick, big, txt, hot=False, sub=""):
    bg = "#b4591f" if hot else "#181b1f"
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};border-top:4px solid '
            f'{"#e39a5e" if hot else COPPER};padding:22px 24px;box-sizing:border-box">'
            f'<div class="cnum" style="color:{WHITE if hot else GREY}">{kick}</div>'
            f'<div style="font:800 64px/1 BC;color:{WHITE if hot else COPPER};margin:14px 0 10px">{big}</div>'
            f'<div class="cd" style="font-size:17px;color:{WHITE if hot else GREY}">{txt}</div>'
            f'{f"<div class=cd style=margin-top:8px;font-size:14px>{sub}</div>" if sub else ""}</div>')




FAMILIES = [("Thermal", "#b4591f", "Heat spins a turbine and a generator.",
             [("Natural gas", "firm", True), ("Coal", "firm", False), ("Nuclear", "firm", False), ("Biomass and waste", "firm", False),
              ("Geothermal", "firm", False), ("Oil / diesel", "firm", False)]),
            ("Water and wind", "#2f63b5", "Moving water or air spins the turbine.",
             [("Hydro", "firm*", False), ("Wind, onshore and offshore", "variable", False)]),
            ("Direct", "#c9a227", "No turbine: sunlight or chemistry makes DC.",
             [("Solar PV", "variable", False), ("Fuel cells", "firm", False)]),
            ("Storage", "#5d636a", "Shifts power in time; it does not make it.",
             [("Batteries (BESS)", "hours", False), ("Pumped hydro", "hours", False)])]


def s_sources(n, N):
    cols = ""
    xs, ws = [64, 456, 784, 1086], [376, 312, 286, 290]
    fimg = {"Thermal": "renders/epic/E21_pro_clean.jpg", "Direct": "renders/epic/E16_pro_clean.jpg", "Storage": "renders/epic/E41_pro_clean.jpg"}
    for (fam, col, how, techs), x, w in zip(FAMILIES, xs, ws):
        chips = ""
        for t, tag, hot in techs:
            chips += (f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding:8px 14px;'
                      f'background:{"#2a1d14" if hot else "#1f2328"};border:1px solid {"#b4591f" if hot else "#2c3036"};border-radius:4px">'
                      f'<span style="font:700 18px/1 BC;color:{COPPER if hot else WHITE};text-transform:uppercase">{t}</span>'
                      f'<span style="font:700 11px/1 BC;letter-spacing:.12em;color:{GREY};text-transform:uppercase">{tag}</span></div>')
            if hot:
                chips += (f'<div style="margin:6px 0 2px 14px;font:400 13.5px/1.4 B;color:{GREY}">simple cycle &middot; combined cycle &middot; engines &middot; aero '
                          f'<b style="color:{COPPER};font-weight:700">&larr; today</b></div>')
        cols += (f'<div class="abs" style="left:{x}px;top:170px;width:{w}px">'
                 f'<div style="display:flex;align-items:center;gap:16px;height:80px;margin-bottom:6px">'
                 + f'<div style="width:70px;height:70px;border-radius:50%;background:{col};flex:none"></div>'
                 + f'<div><div style="font:800 26px/1 BC;color:{WHITE};text-transform:uppercase">{fam}</div>'
                 f'<div class="cd" style="font-size:14px;margin-top:6px">{how}</div></div></div>{chips}</div>')
    notes = [(456, 312, "Not on our campus; Southwire cables them too: hydro, onshore and offshore wind."),
             (784, 286, "In SW-3X1: the fuel-cell bank in the modular yard."),
             (1086, 290, "In SW-3X1: the battery (BESS) yard.")]
    cols += "".join(f'<div class="abs" style="left:{x}px;top:346px;width:{w}px"><img src="{pic(p)}" style="width:{w}px;height:136px;object-fit:cover;display:block">'
                    f'<div style="font:700 11px/1.2 BC;letter-spacing:.1em;color:{GREY};text-transform:uppercase;margin-top:6px">{t}</div></div>'
                    for x, w, p, t in [(784, 286, "renders/epic/E10_pro_clean.jpg", "Solar carport and EV chargers"), (1086, 290, "renders/epic/E41_pro.png", "The battery yard")])
    cols += "".join(f'<div class="abs" style="left:{x}px;top:516px;width:{w}px;border-top:2px solid #2c3036;padding-top:10px">'
                    f'<div class="cd" style="font-size:13.5px">{t}</div></div>' for x, w, t in notes)
    cols += (f'<div class="abs" style="left:456px;top:592px;width:920px;font:700 14px/1.3 BC;letter-spacing:.08em;color:{COPPER};text-transform:uppercase">'
             f'Gas, engines, aeroderivatives and package boilers: all thermal, all on our campus</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; step back</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">How electricity is made: <em>four families</em></div>
  {cols}
  <div class="abs" style="left:64px;top:628px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};padding:12px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:16px"><b style="color:{WHITE}">Almost all of them spin a magnet inside a coil: a generator.</b> Solar PV, fuel cells and
      batteries make DC and need inverters. Firm sources run on demand; variable ones follow the weather. <b style="color:{WHITE}">Every one of them ends in cable.</b></div></div>
  <div class="abs" style="left:64px;top:716px;{SRC}">Firm = can run on demand. *Hydro depends on water and season. Storage runs for hours, then recharges.</div>
  {foot(n, N)}
</section>"""


# The whole system, before the zoom on gas: EIA 2025 utility-scale generation shares and 2026 planned additions.
MIX = [("Natural gas", 41, "firm"), ("Nuclear", 18, "firm"), ("Coal", 17, "firm"), ("Wind", 11, "variable"),
       ("Solar", 7, "variable"), ("Hydro", 6, "firm*")]
ADDS = [("Solar", 43.4, "#e8a874"), ("Batteries", 24.0, "#8e98a3"), ("Wind", 11.8, "#5d636a"), ("Gas", 6.3, "#b4591f")]


def s_system(n, N):
    rows = ""
    for k, (src, v, tag) in enumerate(MIX):
        y = 222 + k * 56
        hot = k == 0
        rows += (f'<div class="abs" style="left:64px;top:{y}px;width:150px;font:700 20px/36px BC;color:{COPPER if hot else WHITE};text-transform:uppercase">{src}</div>'
                 f'<div class="abs" style="left:214px;top:{y + 8}px;width:72px;height:20px;border:1px solid {"#b4591f" if tag == "firm" else "#5d636a"};'
                 f'border-radius:10px;font:700 11px/20px BC;letter-spacing:.12em;text-align:center;color:{GREY};text-transform:uppercase">{tag}</div>'
                 f'<div class="abs" style="left:300px;top:{y + 2}px;width:{v * 8:.0f}px;height:32px;background:{"#b4591f" if hot else "#5d636a"};border-radius:0 3px 3px 0"></div>'
                 f'<div class="abs" style="left:{310 + v * 8:.0f}px;top:{y}px;font:800 22px/36px BC;color:{WHITE}">{v}%</div>')
    tot = sum(v for _, v, _ in ADDS)
    seg, x = "", 760
    for src, v, col in ADDS:
        w = 616 * v / tot
        seg += (f'<div class="abs" style="left:{x:.0f}px;top:256px;width:{w - 3:.0f}px;height:58px;background:{col}"></div>'
                f'<div class="abs" style="left:{x:.0f}px;top:326px;width:{max(w, 70):.0f}px;font:800 22px/1 BC;color:{COPPER if src == "Gas" else WHITE}">{v:g}</div>'
                f'<div class="abs" style="left:{x:.0f}px;top:352px;width:{max(w, 70):.0f}px;font:700 13px/1 BC;letter-spacing:.08em;color:{GREY};text-transform:uppercase">{src}</div>')
        x += w
    why = [("Firm", "Gas runs when it is called: day or night, any weather. Wind and solar follow the weather; batteries cover hours, not days."),
           ("The backbone", "41% of US electricity today, and the backup that lets more wind and solar onto the grid."),
           ("The next wave", "Data centres need firm power around the clock: 378 GW of gas is in development, much of it built later this decade.")]
    w3 = "".join(f'<div class="abs" style="left:{760 + k * 210}px;top:420px;width:196px;border-top:3px solid {COPPER};padding-top:10px">'
                 f'<div class="ct" style="font-size:20px">{h}</div><div class="cd" style="font-size:13.5px;margin-top:6px">{t}</div></div>'
                 for k, (h, t) in enumerate(why))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; the mix</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:54px;width:1320px">The mix today, <em>and why we zoom in on gas</em></div>
  <div class="abs cnum" style="left:64px;top:190px;color:{WHITE}">Share of US electricity, 2025</div>
  {rows}
  <div class="abs cd" style="left:64px;top:566px;width:640px;font-size:13px">Firm = can run on demand. *Hydro depends on water and season.
    Batteries store power; they do not make it.</div>
  <div class="abs cnum" style="left:760px;top:190px;color:{WHITE}">New capacity planned for 2026 &middot; {tot:.0f} GW</div>
  <div class="abs cd" style="left:760px;top:212px;width:616px;font-size:14px">Most of what gets added is solar and batteries. Gas is a small share of the GW, and the one that runs on demand.</div>
  {seg}{w3}
  <div class="abs" style="left:64px;top:620px;width:1312px;background:#2a1d14;border-left:4px solid {COPPER};padding:13px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:17px"><b style="color:{WHITE}">Southwire cables every one of these:</b> solar, wind, storage, transmission and distribution.
      <b style="color:{WHITE}">Today we focus on gas</b>: firm power, a boom-scale build, and some of the most cable-dense plants on the grid.</div></div>
  <div class="abs" style="left:64px;top:732px;{SRC}">EIA, Electricity explained (2025 utility-scale generation, rounded) and Today in Energy, Feb 2026 (planned 2026 additions; developers' plans, not all will be built).</div>
  {foot(n, N)}
</section>"""


def s_glance(n, N):
    t = [("The market", "378 GW", "US gas power in development; 52 GW already under construction"),
         ("The cable", "~$1.2B", "core wire &amp; cable, 2026&ndash;2035, at $8&ndash;13M per GW"),
         ("The pipeline", "386", "gas projects we track in 40 states, every owner type"),
         ("The traction", "$50M+", "booked in Q3; $30M in September alone")]
    html = "".join(tile(64 + k * 334, 250, 310, 270, *v, hot=(k == 1)) for k, v in enumerate(t))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals and market &nbsp;&middot;&nbsp; at a glance</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px;width:1300px">A boom-scale gas build, and <em>cable is on the critical path</em></div>
  {html}
  <div class="abs" style="left:64px;top:566px;font:800 26px/1.2 BC;color:{WHITE};text-transform:uppercase;width:1300px">Today's goal:
    <span style="color:{COPPER}">know the plant, so you can follow the cable through it</span></div>
  <div class="abs" style="left:64px;top:700px;{SRC}">Global Energy Monitor, Aug 2026; Southwire PowerGen planning model and internal figures, 2026.</div>
  {foot(n, N)}
</section>"""


def s_load(n, N):
    stats = [("166 GW", "US peak load growth forecast by 2030", "about 90 GW of it from data centres"),
             ("378 GW", "US gas power in development, mid-2026", "189 GW tied to data centres"),
             ("52 GW", "under construction, up 76% in H1 2026", "the largest gas build in the world"),
             ("Up to 7 yrs", "quoted lead time for some large gas turbines", "procurement decisions are being made now")]
    st = "".join(f'<div class="abs" style="left:{64 + k * 334}px;top:176px;width:310px;border-top:4px solid {COPPER};padding-top:14px">'
                 f'<div style="font:800 54px/1 BC;color:{COPPER}">{a}</div><div class="cd" style="font-size:16px;color:{WHITE};margin-top:8px">{b}</div>'
                 f'<div class="cd" style="font-size:14px;margin-top:4px">{c}</div></div>' for k, (a, b, c) in enumerate(stats))
    x0, base, bw, step, sc = 70, 690, 30, 40.6, 2.6
    bars = ""
    for k, v in enumerate(ADDED):
        y = 1996 + k
        col = "#b4591f" if 2000 <= y <= 2004 else ("#e39a5e" if y == 2026 else "#5d636a")
        bars += f'<div class="abs" style="left:{x0 + k * step:.0f}px;top:{base - v * sc:.0f}px;width:{bw}px;height:{v * sc:.0f}px;background:{col};border-radius:3px 3px 0 0"></div>'
        if y % 5 == 0 or y in (1996, 2026):
            bars += f'<div class="abs" style="left:{x0 + k * step - 10:.0f}px;top:{base + 8}px;width:50px;text-align:center;{SRC};font-size:13px">{y}</div>'
    bars += (f'<div class="abs" style="left:{x0 + 6 * step - 4:.0f}px;top:{base - 57 * sc - 22:.0f}px;font:800 17px/1 BC;color:{WHITE}">57</div>'
             f'<div class="abs" style="left:{x0 + 30 * step - 1:.0f}px;top:{base - 6.3 * sc - 22:.0f}px;font:800 17px/1 BC;color:{WHITE}">6.3</div>'
             f'<div class="abs" style="left:{x0}px;top:{base + 1}px;width:{30 * step + bw:.0f}px;height:1px;background:#3a3f45"></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Market context</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">Load growth is pulling <em>gas power forward</em></div>
  {st}
  <div class="abs cnum" style="left:64px;top:420px;color:{WHITE}">US gas capacity added per year, GW &middot; provisional</div>
  {bars}
  <div class="abs" style="left:420px;top:470px;font:800 22px/1 BC;color:{COPPER};text-transform:uppercase">2000&ndash;04 merchant boom</div>
  <div class="abs cd" style="left:420px;top:498px;font-size:15px">188 GW built &middot; 37.6 GW a year &middot; peak 57 GW in 2002</div>
  <div class="abs" style="left:900px;top:540px;font:800 22px/1 BC;color:{WHITE};text-transform:uppercase">2015&ndash;25 run-rate: 8.1 GW a year</div>
  <div class="abs cd" style="left:900px;top:568px;font-size:15px">Today's pipeline needs a boom-scale build again</div>
  <div class="abs" style="left:64px;top:728px;{SRC}">Grid Strategies, 2025; Global Energy Monitor, Aug 2026; S&amp;P Global, May 2025. History: EIA and Southwire provisional series, to be verified.</div>
  {foot(n, N)}
</section>"""


def s_backlog(n, N):
    oems = [("Turbine OEM 1", 116, "116 GW"), ("Turbine OEM 2", 69, "~69 GW"), ("Turbine OEM 3", 35, "35 GW")]
    rows = "".join(f'<div class="abs" style="left:64px;top:{196 + k * 66}px;width:220px;font:700 22px/48px BC;color:{WHITE};text-transform:uppercase">{a}</div>'
                   f'<div class="abs" style="left:300px;top:{196 + k * 66}px;width:{v * 6.2:.0f}px;height:48px;background:#b4591f;border-radius:0 3px 3px 0"></div>'
                   f'<div class="abs" style="left:{316 + v * 6.2:.0f}px;top:{196 + k * 66}px;font:800 30px/48px BC;color:{WHITE}">{t}</div>'
                   for k, (a, v, t) in enumerate(oems))
    t = [("Modular", "+72%", "power-generation sales at the largest engine-generator maker, Q2 2026"),
         ("Behind the meter", "2.3 GW", "modular gas fleet for Texas AI data centres, plus 1 GW for another campus"),
         ("Packaged", "500 MW", "standard modular gas-turbine plant, offered as a product")]
    html = "".join(tile(64 + k * 444, 440, 420, 220, *v) for k, v in enumerate(t))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">OEM order books</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Turbine backlogs <em>are full</em></div>
  <div class="abs" style="left:1130px;top:200px;width:250px" ><div class="cd" style="font-size:15px">The three large-frame turbine OEMs
    together hold <b style="color:{WHITE}">about 220 GW</b> of gas turbines in backlog and slot reservations. Modular and packaged gas
    power is growing beside them.</div></div>
  {rows}
  {html}
  <div class="abs" style="left:64px;top:700px;{SRC}">OEM releases, Q2&ndash;Q3 2026 (firm backlog plus slot reservations; gas-turbine backlog; large-frame backlog); Utility Dive, Aug 2026; POWER, Oct 2025 and Feb 2026.</div>
  {foot(n, N)}
</section>"""


def s_prize(n, N):
    steps = [("Capacity", "93.7 GW", "modeled additions through 2036, from the 378 GW pipeline: 90% of the 52 GW building, 13.5% of the rest"),
             ("Plant investment", "~$180B", "93.7 GW &times; $1,923/kW blended (combined cycle, peakers, engines)"),
             ("Wire &amp; cable", "$0.75&ndash;1.2B", "$8&ndash;13M per GW: under 1% of plant capex, on the critical path to first power")]
    html = "".join(tile(64, 168 + k * 172, 400, 156, *v, hot=(k == 2)).replace("font:800 64px", "font:800 46px").replace(
        "margin:14px 0 10px", "margin:8px 0 6px").replace("font-size:17px", "font-size:14px") for k, v in enumerate(steps))
    x0, base, sc, bw, step = 560, 640, 2.3, 54, 82
    bars = ""
    for k, (y, nm, al, gw) in enumerate(POS):
        x = x0 + k * step
        bars += (f'<div class="abs" style="left:{x}px;top:{base - nm * sc:.0f}px;width:{bw}px;height:{nm * sc:.0f}px;background:#b4591f"></div>'
                 f'<div class="abs" style="left:{x}px;top:{base - (nm + al) * sc:.0f}px;width:{bw}px;height:{al * sc:.0f}px;background:#5d636a;border-radius:3px 3px 0 0"></div>'
                 f'<div class="abs" style="left:{x - 10}px;top:{base - (nm + al) * sc - 24:.0f}px;width:{bw + 20}px;text-align:center;font:800 16px/1 BC;color:{WHITE}">${nm + al}M</div>'
                 f'<div class="abs" style="left:{x - 10}px;top:{base + 8}px;width:{bw + 20}px;text-align:center;font:700 15px/1 BC;color:{WHITE}">{y}</div>'
                 f'<div class="abs" style="left:{x - 10}px;top:{base + 28}px;width:{bw + 20}px;text-align:center;{SRC}">{gw} GW</div>')
    key = (f'<div class="abs" style="left:560px;top:176px;font:700 14px/1 BC;letter-spacing:.1em;color:{GREY};text-transform:uppercase">'
           f'<span style="display:inline-block;width:12px;height:12px;background:#b4591f;margin-right:8px"></span>Named projects $673M'
           f'<span style="display:inline-block;width:12px;height:12px;background:#5d636a;margin:0 8px 0 26px"></span>Future-project allowance $501M</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Sizing the opportunity &nbsp;&middot;&nbsp; conservative planning case</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">~$1.2B of core gas cable, <em>2026&ndash;2035</em></div>
  {html}
  {key}
  {bars}
  <div class="abs" style="left:560px;top:{base + 1}px;width:{9 * step + bw}px;height:1px;background:#3a3f45"></div>
  <div class="abs" style="left:560px;top:690px;width:820px;{SRC}">Core cable by purchase-order year; below each year, modeled PO-year GW (not installed GW).
    GW &times; $/kW &times; addressable share &times; win probability. OEM internal wiring and HV excluded.</div>
  <div class="abs" style="left:64px;top:728px;{SRC}">Global Energy Monitor, Aug 2026; completion rates, blended cost and cable rates are Southwire planning assumptions.</div>
  {foot(n, N)}
</section>"""


def s_where(n, N):
    reg = [("Announced", 140.6), ("Under construction", 45.6), ("Approved &middot; NTP", 9.4), ("Permit application", 7.3), ("Operating", 3.0)]
    r = "".join(f'<div class="abs" style="left:64px;top:{230 + k * 50}px;width:200px;font:700 17px/34px BC;color:{WHITE};text-transform:uppercase">{a}</div>'
                f'<div class="abs" style="left:270px;top:{230 + k * 50}px;width:{v * 2.1:.0f}px;height:34px;background:{"#b4591f" if k == 0 else "#5d636a"}"></div>'
                f'<div class="abs" style="left:{280 + v * 2.1:.0f}px;top:{230 + k * 50}px;font:800 20px/34px BC;color:{WHITE}">{v}</div>'
                for k, (a, v) in enumerate(reg))
    states = [("TX", 55.5), ("LA", 16.3), ("WV", 13.4), ("IN", 10.3), ("OH", 10.3), ("PA", 10.0), ("NC", 9.4), ("GA", 7.9), ("AZ", 6.1)]
    s_ = "".join(f'<div class="abs" style="left:780px;top:{230 + k * 38}px;width:40px;font:800 18px/28px BC;color:{WHITE}">{a}</div>'
                 f'<div class="abs" style="left:830px;top:{230 + k * 38}px;width:{v * 7:.0f}px;height:28px;background:#b4591f"></div>'
                 f'<div class="abs" style="left:{840 + v * 7:.0f}px;top:{230 + k * 38}px;font:800 18px/28px BC;color:{WHITE}">{v}</div>'
                 for k, (a, v) in enumerate(states))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">The project register</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">205.8 GW eligible, <em>most of it still early</em></div>
  <div class="abs cnum" style="left:64px;top:196px;color:{WHITE}">By status &middot; gross GW, COD 2026&ndash;2035</div>
  {r}
  <div class="abs" style="left:64px;top:500px;font:800 64px/1 BC;color:{COPPER}">68%</div>
  <div class="abs cd" style="left:220px;top:508px;width:440px;font-size:16px"><b style="color:{WHITE}">of eligible capacity is only announced.</b>
    Being on the register does not mean a cable package is open; it means a conversation to start.</div>
  <div class="abs cnum" style="left:780px;top:196px;color:{WHITE}">Top states &middot; gross GW, 386 projects</div>
  {s_}
  <div class="abs cd" style="left:780px;top:590px;width:600px;font-size:15px">Greenfield 137 GW, brownfield 69 GW. Utilities reuse old
    sites (coal-site repowers, expansions); independent and behind-the-meter developers mostly build new, often on data-centre campuses.</div>
  <div class="abs" style="left:64px;top:728px;{SRC}">Southwire PowerGen register, Sep 11, 2026: 386 records across 305 site groups; gross GW, unweighted.</div>
  {foot(n, N)}
</section>"""


# Tile map from the Oct 6 deck, page 10: (state, column, row, gross GW or None)
TILES = [("WI", 6, 0, 4.4), ("VT", 10, 0, None), ("ME", 11, 0, None),
         ("WA", 1, 1, None), ("ID", 2, 1, 1.6), ("MT", 3, 1, None), ("ND", 4, 1, 2.2), ("MN", 5, 1, None), ("IL", 6, 1, 1.4),
         ("MI", 7, 1, 1.1), ("NY", 9, 1, None), ("MA", 10, 1, None), ("NH", 11, 1, None),
         ("OR", 1, 2, None), ("NV", 2, 2, 1.9), ("WY", 3, 2, 3.5), ("SD", 4, 2, None), ("IA", 5, 2, 3.0), ("IN", 6, 2, 10.3),
         ("OH", 7, 2, 10.3), ("PA", 8, 2, 10.0), ("NJ", 9, 2, None), ("CT", 10, 2, None), ("RI", 11, 2, None),
         ("CA", 1, 3, None), ("UT", 2, 3, 4.4), ("CO", 3, 3, 1.6), ("NE", 4, 3, 1.7), ("MO", 5, 3, 4.0), ("KY", 6, 3, 2.9),
         ("WV", 7, 3, 13.4), ("VA", 8, 3, 5.2), ("MD", 9, 3, None), ("DE", 10, 3, None),
         ("AZ", 2, 4, 6.1), ("NM", 3, 4, 2.8), ("KS", 4, 4, 1.4), ("AR", 5, 4, 1.8), ("TN", 6, 4, 3.2), ("NC", 7, 4, 9.4),
         ("SC", 8, 4, 4.6), ("DC", 9, 4, None),
         ("OK", 4, 5, 4.2), ("LA", 5, 5, 16.3), ("MS", 6, 5, 3.7), ("AL", 7, 5, None), ("GA", 8, 5, 7.9),
         ("AK", 0, 6, 2.7), ("HI", 1, 6, None), ("TX", 4, 6, 55.5), ("FL", 9, 6, 1.2)]
HEAT = [(20, "#7a2e0c", "&gt; 20 GW"), (10, "#b4591f", "10&ndash;20"), (5, "#d97b3a", "5&ndash;10"), (2, "#e8a874", "2&ndash;5"),
        (0, "#f1cfb0", "&lt; 2"), (None, "#2a2e33", "None")]


def heat(v):
    if v is None:
        return HEAT[-1][1]
    return next(c for t, c, _ in HEAT if t is not None and v > t or t == 0)


def s_map(n, N):
    x0, y0, c = 64, 196, 62
    tiles = ""
    for st, col, row, v in TILES:
        bg = heat(v)
        ink = WHITE if v is None or v > 5 else "#1a1c1f"
        tiles += (f'<div class="abs" style="left:{x0 + col * c}px;top:{y0 + row * c}px;width:{c - 4}px;height:{c - 4}px;background:{bg};'
                  f'border-radius:3px;text-align:center"><div style="font:700 13px/1 BC;color:{ink if v is not None else "#80868c"};margin-top:12px">{st}</div>'
                  + (f"<div style='font:800 17px/1 BC;color:{ink};margin-top:5px'>{v}</div>" if v is not None else "") + '</div>')
    leg = "".join(f'<span style="display:inline-block;width:13px;height:13px;background:{col};margin:0 6px 0 16px;vertical-align:-2px"></span>{t}'
                  for _, col, t in HEAT)
    owners = [("IPP", 51, 15), ("Behind the meter", 55, 8), ("Utility (IOU)", 23, 36), ("Co-op / public", 8, 9)]
    ob = "".join(f'<div class="abs" style="left:880px;top:{226 + k * 52}px;font:700 16px/1 BC;color:{WHITE};text-transform:uppercase">{a}'
                 f'<span style="float:right;font:400 13px/1 B;color:{GREY};text-transform:none;margin-left:20px">{g} new &middot; {r} reuse</span></div>'
                 f'<div class="abs" style="left:880px;top:{246 + k * 52}px;width:{g * 6.4:.0f}px;height:14px;background:#b4591f"></div>'
                 f'<div class="abs" style="left:{880 + g * 6.4:.0f}px;top:{246 + k * 52}px;width:{r * 6.4:.0f}px;height:14px;background:#5d636a"></div>'
                 for k, (a, g, r) in enumerate(owners))
    sites = [("Greenfield, grid-connected", 77.0), ("Data-centre / BTM campus", 54.5), ("Coal-site repower", 41.3),
             ("Expansion at an operating plant", 21.4), ("Industrial captive and site reuse", 11.6)]
    sb = "".join(f'<div class="abs" style="left:880px;top:{474 + k * 34}px;width:330px;font:400 15px/24px B;color:{GREY}">'
                 f'<span style="display:inline-block;width:10px;height:10px;background:{"#b4591f" if k < 2 else "#5d636a"};margin-right:10px"></span>{a}</div>'
                 f'<div class="abs" style="left:1230px;top:{474 + k * 34}px;width:150px;text-align:right;font:800 20px/24px BC;color:{WHITE}">{v}</div>'
                 for k, (a, v) in enumerate(sites))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Project concentration</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">Where the build is, <em>who owns it, what kind of site</em></div>
  <div class="abs cnum" style="left:64px;top:166px;color:{WHITE}">Gross GW by state &middot; 386 projects, COD 2026&ndash;2035</div>
  {tiles}
  <div class="abs" style="left:48px;top:{y0 + 7 * c + 8}px;font:700 13px/1 BC;letter-spacing:.06em;color:{GREY}">{leg}</div>
  <div class="abs cnum" style="left:880px;top:196px;color:{WHITE}">Owner &times; site &middot; gross GW
    <span style="color:{GREY};letter-spacing:.06em">&nbsp; <span style="color:#d97b3a">&#9632;</span> greenfield 137 &nbsp;<span style="color:#80868c">&#9632;</span> brownfield 69</span></div>
  {ob}
  <div class="abs" style="left:880px;top:444px;font:800 16px/1 BC;color:{COPPER};text-transform:uppercase">Utilities reuse old sites; IPPs and BTM build new</div>
  {sb}
  <div class="abs" style="left:64px;top:728px;{SRC}">Southwire PowerGen register, Sep 11, 2026. Gross GW, unweighted. Site classes provisional (Rev01).</div>
  {foot(n, N)}
</section>"""


def s_q3(n, N):
    t = [("Projects tracked", "386", "new gas generation in 40 states, all owner types"),
         ("Priority pursuits", "17", "validated, about $200M of cable potential"),
         ("Booked in Q3", "$50M+", "gas power cable orders, July to September", ),
         ("September", "$30M", "booked in one month")]
    html = "".join(tile(64 + k * 334, 186, 310, 270, *v, hot=(k == 2)) for k, v in enumerate(t))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Southwire progress &nbsp;&middot;&nbsp; Q3 2026</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">From discovery to execution <em>in six months</em></div>
  {html}
  <div class="abs lede" style="left:64px;top:500px;width:1100px;font-size:19px">Power Generation became its own Southwire vertical in early
    2026. Owner conversations showed that cable is <b style="color:{WHITE}">specified and bought through EPCs and package builders</b>,
    so the pursuit model now follows that path. What you see in the next 40 minutes is what those buyers build.</div>
  <div class="abs" style="left:64px;top:728px;{SRC}">Southwire internal figures, 2026.</div>
  {foot(n, N)}
</section>"""


# Fundamentals from the PowerGen thermal narrative (Oct 2026, pages 1-4), restyled.
def circ(t, d=46, bg=COPPER, ink="#121417", fs=20):
    return (f'<div style="width:{d}px;height:{d}px;border-radius:50%;background:{bg};color:{ink};font:800 {fs}px/{d}px BC;'
            f'text-align:center;display:inline-block">{t}</div>')


def s_blackbox(n, N):
    """Definitions: every power plant is source -> conversion (the black box) -> power. Opens the fundamentals."""
    def node(x, big, lab, sub, bg):
        return (f'<div class="abs" style="left:{x}px;top:214px;width:300px;text-align:center">'
                f'<div style="margin:0 auto;width:190px;height:190px;border-radius:50%;background:{bg};display:flex;align-items:center;'
                f'justify-content:center;font:800 32px/1 BC;color:{WHITE};text-transform:uppercase">{big}</div>'
                f'<div style="font:800 26px/1 BC;color:{WHITE};text-transform:uppercase;margin-top:24px">{lab}</div>'
                f'<div class="cd" style="font-size:16px;margin-top:10px">{sub}</div></div>')
    arrow = lambda x: f'<div class="abs" style="left:{x}px;top:307px;width:110px;height:3px;background:{COPPER}"></div><div class="abs" style="left:{x + 102}px;top:299px;width:0;height:0;border-left:16px solid {COPPER};border-top:9px solid transparent;border-bottom:9px solid transparent"></div>'
    box = (f'<div class="abs" style="left:590px;top:214px;width:260px;height:190px;background:#0b0c0e;border:3px solid {COPPER};'
           f'border-radius:6px;display:flex;align-items:center;justify-content:center;font:800 44px/1 BC;color:{WHITE};text-align:center">BLACK<br>BOX</div>'
           f'<div class="abs" style="left:570px;top:428px;width:300px;text-align:center"><div style="font:800 26px/1 BC;color:{WHITE};text-transform:uppercase">Conversion</div>'
           f'<div class="cd" style="font-size:16px;margin-top:10px">The machine that turns the source into electricity: a turbine and generator, '
           f'an engine, a solar panel, a fuel cell.</div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; definitions</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Every power plant <em>is this</em></div>
  <div class="abs lede" style="left:64px;top:160px;width:1200px">Input &rarr; conversion &rarr; output. The complexity is what's inside the box, and what's around it.</div>
  {node(190, "Source", "Input", "The energy that goes in: fuel (gas, coal, uranium, biomass) or nature (sun, wind, water).", "#3b7a4a")}
  {arrow(470)}{box}{arrow(862)}
  {node(950, "Power", "Output", "Electricity out: to the grid through a switchyard, or straight to a load behind the meter.", "#2f63b5")}
  <div class="abs" style="left:64px;top:628px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};padding:13px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:17px">Every plant, from a gas turbine to a solar farm, fits this picture. <b style="color:{WHITE}">What changes is the source and the machine in the box.</b>
      Next: the four families of power generation, then we open the box of a gas plant.</div></div>
  {foot(n, N)}
</section>"""


ANATOMY = [("Fuel infrastructure", ["Gas production, pipelines, compression", "Storage and LNG logistics", "Plant-gate fuel delivery"]),
           ("Fuel input", ["Natural gas, coal, oil / diesel", "Hydrogen blends", "Biomass where it applies"]),
           ("Thermal conversion", ["Frame and aero gas turbines, engines (RICE)", "Combined cycle: GT + HRSG + ST", "Modular and H2-ready packages"]),
           ("Electricity output", ["Dispatchable AC power", "Stable, reliable load", "Baseload, mid-merit or peaking"]),
           ("Delivery &amp; flexibility", ["Transmission and distribution", "MV / LV delivery, behind-the-meter on site", "Storage and flexibility support"]),
           ("End use / off-take", ["Utilities, IPPs, industrial loads", "Data centres and other off-takers", "Critical infrastructure"])]


def s_anatomy(n, N):
    cards = ""
    bimg = ["renders/epic/E109_pro_clean.jpg", "renders/epic/E108_pro_clean.jpg", "renders/epic/E21_pro.png", "renders/epic/E24_pro.png",
            "renders/epic/E20_pro.png", "renders/epic/E47_pro_clean.jpg"]
    for k, (h, items) in enumerate(ANATOMY):
        x = 64 + k * 220
        hot = k in (3, 4)
        li = "".join(f'<div class="cd" style="font-size:15px;margin-top:10px;padding-left:14px;position:relative">'
                     f'<span style="position:absolute;left:0;top:7px;width:6px;height:6px;background:{COPPER}"></span>{t}</div>' for t in items)
        cards += (f'<div class="abs" style="left:{x}px;top:200px;width:204px;height:400px;background:#181b1f;border-top:4px solid '
                  f'{COPPER if hot else "#5d636a"};padding:22px 18px;box-sizing:border-box">{circ(k, bg=COPPER if hot else "#5d636a", ink=WHITE if not hot else "#121417")}'
                  f'<div class="ct" style="font-size:23px;margin:18px 0 6px;min-height:46px">{h}</div>{li}</div>')
        if k < 5:
            cards += f'<div class="abs" style="left:{x + 206}px;top:388px;font:800 18px/1 BC;color:{COPPER}">&rsaquo;</div>'
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Open the box: <em>the physical anatomy</em></div>
  <div class="abs lede" style="left:64px;top:156px;width:1200px;font-size:17px">From fuel infrastructure to dispatchable electricity and end-use demand.</div>
  {cards}
  <div class="abs lede" style="left:64px;top:632px;width:1300px;font-size:18px">Same physics on every project: gas turbine, combined cycle or engines.
    <b style="color:{WHITE}">What changes is who owns it.</b></div>
  {foot(n, N)}
</section>"""


def s_owners(n, N):
    eq = [("ProjectCo", "one company per plant"), ("Asset", "conversion plant"), ("Contract", "power purchase agreement"), ("Customer", "off-taker / load"),
          ("Capital", "investors, tax equity"), ("Market", "ERCOT, PJM, MISO")]
    e = "".join(f'<div style="display:inline-block;vertical-align:top;width:150px;text-align:center">'
                f'<div style="font:800 24px/1 BC;color:{WHITE};text-transform:uppercase">{a}</div><div class="cd" style="font-size:14px;margin-top:6px">{b}</div></div>'
                + (f'<div style="display:inline-block;vertical-align:top;width:22px;font:800 24px/1 BC;color:{COPPER}">+</div>' if k < 5 else "")
                for k, (a, b) in enumerate(eq))
    arch = [("IOUs / co-ops", "Regulated", ["Utility-led, rate-based ownership", "Own and operate generation", "Buy like utilities: standards, cycles"]),
            ("Hybrid IPPs", "Mixed model", ["Utility-affiliated IPP subsidiaries", "Bridge regulated and competitive", "Two buying behaviours"]),
            ("Pure IPPs", "Competitive", ["Privately owned, investor-backed projects", "A direct fit with the project equation", "Speed and cost drive decisions"])]
    cards = ""
    for k, (h, tag, items) in enumerate(arch):
        hot = k == 2
        li = "".join(f'<div class="cd" style="font-size:16px;margin-top:10px;padding-left:14px;position:relative">'
                     f'<span style="position:absolute;left:0;top:8px;width:6px;height:6px;background:{COPPER}"></span>{t}</div>' for t in items)
        cards += (f'<div class="abs" style="left:{64 + k * 444}px;top:428px;width:420px;height:212px;background:{"#2a1d14" if hot else "#181b1f"};'
                  f'border-top:4px solid {COPPER if hot else "#5d636a"};{"border:1px solid #b4591f;border-top:4px solid " + COPPER + ";" if hot else ""}padding:22px 26px;box-sizing:border-box">'
                  f'<div class="ct" style="font-size:28px">{h} <span style="font:700 14px/1 BC;letter-spacing:.14em;color:{COPPER};margin-left:10px">{tag}</span></div>{li}</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; who buys</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Same physics, <em>different owners</em></div>
  <div class="abs lede" style="left:64px;top:156px;width:1300px;font-size:17px">The owner decides how the project is structured, and how it gets bought.
    An independent power producer (IPP) builds each plant as its own company, sells the power on contract or into a market, and funds it with investors.</div>
  <div class="abs" style="left:64px;top:226px;width:1312px;height:150px;background:#181b1f;border-top:4px solid {COPPER};padding:20px 26px;box-sizing:border-box">
    <div class="cnum">The structural equation</div>
    <div style="margin-top:26px;white-space:nowrap"><div style="display:inline-block;vertical-align:top;width:170px;font:800 28px/1 BC;color:{COPPER};text-transform:uppercase">Thermal IPP =</div>{e}</div></div>
  <div class="abs cnum" style="left:64px;top:400px;color:{WHITE}">Power owner archetypes</div>
  {cards}
  <div class="abs" style="left:952px;top:652px;font:700 14px/1 BC;letter-spacing:.1em;color:{COPPER};text-transform:uppercase">Our sales focus for competitive thermal power</div>
  {foot(n, N)}
</section>"""


def s_corridor(n, N):
    up = "".join(f'<div class="abs" style="left:{64 + k * 104}px;top:206px;width:94px;height:330px;background:#15171a;border-top:4px solid #3a3f45;'
                 f'text-align:center;padding-top:20px;box-sizing:border-box">{circ(k, 38, "#3a3f45", "#80868c", 17)}'
                 f'<div style="font:700 15px/1.2 BC;color:#80868c;text-transform:uppercase;margin-top:14px">{t}</div></div>'
                 for k, t in enumerate(["Fuel infra", "Fuel input", "Thermal conversion"]))
    zones = [("3", "Electricity output", ["Generator leads", "Power collection and busbar", "Grounding systems"]),
             ("4A", "Plant electrical &amp; interconnection", ["GSU transformer, switchyard", "MV / HV cable and tray", "E-houses, controls, BESS tie-ins"]),
             ("4B", "Utility / grid delivery", ["Gen-tie to the POI", "Transmission and distribution cable", "Substation solutions"])]
    z = ""
    for k, (num, h, items) in enumerate(zones):
        x = 440 + k * 318
        li = "".join(f'<div class="cd" style="font-size:15px;margin-top:9px;padding-left:14px;position:relative">'
                     f'<span style="position:absolute;left:0;top:7px;width:6px;height:6px;background:{COPPER}"></span>{t}</div>' for t in items)
        z += (f'<div class="abs" style="left:{x}px;top:250px;width:296px;height:200px;background:#1f2328;padding:18px 20px;box-sizing:border-box">'
              f'{circ(num, 44, COPPER, "#121417", 18)}<div class="ct" style="font-size:22px;margin-top:12px">{h}</div>{li}</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; where the cable is</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Where Southwire wins: <em>the POI corridor</em></div>
  <div class="abs lede" style="left:64px;top:156px;width:1250px;font-size:17px">The cable story lives between electricity output and the grid:
    plant electrical, gen-tie and utility delivery.</div>
  {up}
  <div class="abs" style="left:64px;top:548px;font:italic 400 14px/1 B;color:#80868c">Upstream: not our fight</div>
  <div class="abs" style="left:372px;top:362px;font:800 30px/1 BC;color:{COPPER}">&rarr;</div>
  <div class="abs" style="left:420px;top:198px;width:976px;height:350px;background:#181b1f;border-top:4px solid {COPPER}"></div>
  <div class="abs cnum" style="left:440px;top:218px">The Southwire corridor</div>
  {z}
  <div class="abs" style="left:1072px;top:240px;width:0;height:290px;border-left:2px dashed {COPPER}"></div>
  <div class="abs" style="left:440px;top:470px;width:610px;height:54px;background:#b4591f;padding:0 18px;box-sizing:border-box;
       font:800 19px/54px BC;color:{WHITE};text-transform:uppercase">HV underground: gen-tie and plant-to-POI</div>
  <div class="abs" style="left:1050px;top:470px;width:44px;height:54px;background:{WHITE};font:800 17px/54px BC;color:#121417;text-align:center">POI</div>
  <div class="abs cd" style="left:440px;top:530px;font-size:13px">Plant / EPC scope</div>
  <div class="abs cd" style="left:1104px;top:530px;font-size:13px">Utility / transmission-owner scope</div>
  <div class="abs" style="left:64px;top:600px;width:1332px;background:#2a1d14;border-left:4px solid {COPPER};padding:16px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:17px"><b style="color:{WHITE}">Every MW that leaves the black box crosses this corridor.</b> Cable intensity
      concentrates at 3 &rarr; 4A &rarr; 4B, the same span where the POI boundary blurs scope, and where we help EPCs and IPPs.</div></div>
  {foot(n, N)}
</section>"""



def s_box(n, N):
    """Every thermal project is a black box, opened: input / conversion / output over the six anatomy steps."""
    bands = [(0, 2, "Input", "fuel / energy source", "#3b7a4a"), (2, 1, "Black box", "thermal conversion", "#0b0c0e"),
             (3, 3, "Output", "dispatchable power, delivered", "#2f63b5")]
    b = ""
    for k0, w, lab, sub, bg in bands:
        x = 64 + k0 * 220
        bord = f"border:3px solid {COPPER};" if lab == "Black box" else ""
        b += (f'<div class="abs" style="left:{x}px;top:176px;width:{w * 220 - 16}px;height:72px;background:{bg};{bord}border-radius:4px;'
              f'box-sizing:border-box;text-align:center;padding-top:12px"><div style="font:800 26px/1 BC;color:{WHITE};text-transform:uppercase">{lab}</div>'
              f'<div style="font:400 14px/1 B;color:#d6d9dc;margin-top:7px">{sub}</div></div>')
    cards = ""
    BCAP = ["M&amp;R station", "Plant gas yard", "Turbine hall", "Generator bus", "230 kV switchyard", "Data centre"]
    bimg = ["renders/epic/E109_pro_clean.jpg", "renders/epic/E108_pro_clean.jpg", "renders/epic/E21_pro.png", "renders/epic/E24_pro.png",
            "renders/epic/E20_pro.png", "renders/epic/E47_pro_clean.jpg"]
    for k, (h, items) in enumerate(ANATOMY):
        x = 64 + k * 220
        li = "".join(f'<div class="cd" style="font-size:15px;margin-top:9px;padding-left:14px;position:relative">'
                     f'<span style="position:absolute;left:0;top:7px;width:6px;height:6px;background:{COPPER}"></span>{t}</div>' for t in items)
        cards += (f'<div class="abs" style="left:{x}px;top:264px;width:204px;height:384px;background:#181b1f;border-top:4px solid {COPPER};box-sizing:border-box">'
                  f'{capimg(bimg[k], 204, 124, BCAP[k])}'
                  f'<div style="padding:10px 16px;position:relative"><div style="position:absolute;top:-22px;right:12px">{circ(k, 38, COPPER, "#121417", 17)}</div>'
                  f'<div class="ct" style="font-size:20px;margin:8px 0 2px;min-height:40px">{h}</div>{li}</div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">Open the box: <em>the physical anatomy</em></div>
  {b}{cards}
  <div class="abs lede" style="left:64px;top:664px;width:1300px;font-size:16px">Back to the black box, now for gas. Gas turbine, combined cycle or engines: <b style="color:{WHITE}">the same physics on every project.</b>
    What changes is the machine in the box, and who owns it.</div>
  {foot(n, N)}
</section>"""


TYPES = [("Simple cycle", "the peaker", "50&ndash;400 MW per gas turbine", "~35&ndash;40%", "10&ndash;30 min", "Peaking, mid-merit",
          "A gas turbine alone: exhaust goes straight up the stack"),
         ("Combined cycle", "the workhorse", "300&ndash;1,500+ MW per block", "~55&ndash;64%", "about 1&ndash;3 hours", "Baseload, mid-merit",
          "Gas turbines + HRSGs + steam turbine: the SW-3X1 power block"),
         ("Engines (RICE)", "the sprinter", "2&ndash;20 MW per engine, in banks", "~40&ndash;50%", "about 5 min", "Peaking, data-centre firming",
          "Big gas engines in a hall: the modular yard"),
         ("Aeroderivative", "the jet", "30&ndash;60 MW per unit", "~38&ndash;42%", "5&ndash;10 min", "Peaking, fast backup",
          "A jet engine on the ground: the modular yard")]


def s_types(n, N):
    labels = ["Unit size", "Efficiency", "Start to full load", "Runs as", "In the model"]
    head = "".join(f'<div class="abs" style="left:{300 + k * 272}px;top:172px;width:256px;border-top:4px solid {COPPER if k == 1 else "#5d636a"};'
                   f'padding-top:12px"><div style="font:800 28px/1 BC;color:{COPPER if k == 1 else WHITE};text-transform:uppercase">{t[0]}</div>'
                   f'<div class="cnum" style="margin-top:6px;color:{GREY}">{t[1]}</div></div>' for k, t in enumerate(TYPES))
    rows = ""
    for r, lab in enumerate(labels):
        y = 262 + r * 70
        rows += (f'<div class="abs" style="left:64px;top:{y}px;width:1312px;height:1px;background:#2c3036"></div>'
                 f'<div class="abs" style="left:64px;top:{y + 14}px;width:220px;font:700 15px/1.2 BC;letter-spacing:.12em;color:{GREY};text-transform:uppercase">{lab}</div>')
        for k, t in enumerate(TYPES):
            big = r < 3
            rows += (f'<div class="abs" style="left:{300 + k * 272}px;top:{y + 12}px;width:256px;'
                     f'{"font:800 22px/1.15 BC;color:" + WHITE if big else "font:400 15px/1.35 B;color:" + GREY}">{t[2 + r]}</div>')
    units = (f'<div class="abs" style="left:64px;top:612px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};padding:12px 22px;box-sizing:border-box">'
             f'<div class="cd" style="font-size:16px"><b style="color:{WHITE}">Units that stick:</b> 1 GW = 1,000 MW = 1,000,000 kW. '
             f'<b style="color:{WHITE}">MW</b> is power (how hard it runs right now); <b style="color:{WHITE}">MWh</b> is energy (power &times; hours). '
             f'Efficiency is how much of the fuel\'s energy leaves as electricity; the rest goes up the stack as heat.</div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; the machines in the box</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">Four ways to <em>burn gas for power</em></div>
  {head}{rows}{units}
  <div class="abs" style="left:64px;top:714px;{SRC}">Typical ranges for new US units; efficiency on a lower-heating-value basis. Starts vary with design and how hot the unit is.</div>
  {foot(n, N)}
</section>"""


def follow_numbers():
    """Cable footage of the SW-3X1 schedule by plant area, grouped along the black-box flow."""
    import openpyxl
    rows = list(openpyxl.load_workbook(os.path.join(PLANT, "brochure", "SW-3X1_Cable_Schedule_and_BOM.xlsx"),
                                       read_only=True)["Cable Schedule"].iter_rows(values_only=True))[1:]
    ft = lambda r: math.ceil(((r[19] or 0) + (r[20] or 0) + 20) * 1.1 / 10) * 10 * r[13] * r[14]
    groups = [("Fuel in", "gas yard, metering, LNG and fuel supply", "DK"),
              ("The black box", "turbine hall, HRSGs, cooling, water, inlet chilling", "ABEJ"),
              ("Out to the grid", "GSUs, switchyard, gen-tie to the POI", "C"),
              ("On-site delivery", "battery yard, modular and behind-the-meter power", "HI"),
              ("Around it all", "control and service buildings, carbon capture", "FG")]
    tot = {g: [0, 0] for g, _, _ in groups}
    for r in rows:
        g = next(g for g, _, zs in groups if str(r[1]) in zs)
        tot[g][0] += ft(r)
        tot[g][1] += r[13] * r[14]
    return [(g, d, tot[g][0], tot[g][1]) for g, d, _ in groups]


def s_follow(n, N):
    data = follow_numbers()
    all_ft = sum(v for _, _, v, _ in data)
    mx = max(v for _, _, v, _ in data)
    rows = ""
    for k, (g, d, v, c) in enumerate(data):
        y = 196 + k * 84
        hot = g == "The black box"
        rows += (f'<div class="abs" style="left:64px;top:{y}px;width:300px"><div style="font:800 24px/1 BC;color:{COPPER if hot else WHITE};text-transform:uppercase">{g}</div>'
                 f'<div class="cd" style="font-size:14px;margin-top:6px">{d}</div></div>'
                 f'<div class="abs" style="left:380px;top:{y + 4}px;width:{480 * v / mx:.0f}px;height:40px;background:{"#b4591f" if hot else "#5d636a"};border-radius:0 4px 4px 0"></div>'
                 f'<div class="abs" style="left:{392 + 480 * v / mx:.0f}px;top:{y + 4}px;font:800 24px/40px BC;color:{WHITE}">{v / 5280:,.0f} mi'
                 f'<span style="font:400 14px/1 B;color:{GREY};margin-left:12px">{100 * v / all_ft:.0f}% &middot; {c:,} cables</span></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; where the cable is</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">Follow the power: <em>the cable is everywhere</em></div>
  <div class="abs cnum" style="left:64px;top:166px;color:{WHITE}">The whole SW-3X1 campus by plant area, from the model's cable schedule ({all_ft / 5280:,.0f} miles)</div>
  {rows}
  <div class="abs" style="left:1150px;top:196px;width:226px;background:#181b1f;border-top:4px solid {COPPER};padding:18px 20px;box-sizing:border-box">
    <div class="ct" style="font-size:22px">The POI</div>
    <div class="cd" style="font-size:14px;margin-top:8px"><b style="color:{WHITE}">Point of interconnection:</b> where the plant meets the grid.
      The plant side is the owner's and EPC's scope; past it, the utility or transmission owner builds and buys.</div>
    <div class="cd" style="font-size:14px;margin-top:10px">The gen-tie (often HV underground) runs from the switchyard to the POI, and the scope line
      there is often blurred: a place we help.</div></div>
  <div class="abs" style="left:64px;top:630px;width:1312px;background:#2a1d14;border-left:4px solid {COPPER};padding:14px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:17px"><b style="color:{WHITE}">Most of the cable is inside the box</b>: thousands of instrument, control and
      motor circuits in the turbine hall and HRSGs. The grid connection carries the biggest cables; the power block carries the most.</div></div>
  {foot(n, N)}
</section>"""


PHASES = [("Develop", "site, permits, interconnection request, fuel and water", "Owner / developer", "years: the interconnection queue is often the long pole"),
          ("Finance", "PPA or rate case, turbine slot, financing decision (FID)", "Owner, lenders, OEM", "turbines are reserved years ahead"),
          ("Engineer", "owner's engineer writes the specs; the EPC does detailed design", "Owner's engineer, EPC", "cable is specified here"),
          ("Procure", "EPC and package builders buy equipment and bulk materials", "EPC, OEMs, package builders", "cable is bought here"),
          ("Build", "civil, mechanical, then electrical: trays, pulls, terminations", "EPC and electrical contractor", "cable pulls sit on the critical path"),
          ("Operate", "commercial operation (COD), outages, upgrades, repowering", "Owner / operator", "replacement and brownfield work")]


def s_buy(n, N):
    html = ""
    pimg = ["renders/nextgen/_src/E123_pro_clean.jpg", "renders/epic/E22_pro.png", "renders/epic/E88_pro_clean.jpg", "renders/epic/E89_pro_clean.jpg",
            "renders/epic/E92_pro_clean.jpg", "renders/epic/E86_pro_clean.jpg"]
    PCAP = ["The site", "The turbine order", "Engineering", "The reel yard", "Cable spine going in", "Control room"]
    for k, (h, what, who, note) in enumerate(PHASES):
        x = 64 + k * 220
        hot = k in (2, 3)
        html += f'<div class="abs" style="left:{x}px;top:262px;border-bottom:3px solid {COPPER if hot else "#3a3f45"}">{capimg(pimg[k], 204, 122, PCAP[k])}</div>'
        html += (f'<div class="abs" style="left:{x}px;top:190px;width:204px;height:62px;background:{"#b4591f" if hot else "#2a2e33"};'
                 f'clip-path:polygon(0 0,92% 0,100% 50%,92% 100%,0 100%,{"0" if k == 0 else "8%"} 50%);padding:0 0 0 {16 if k == 0 else 26}px;box-sizing:border-box;'
                 f'font:800 21px/62px BC;color:{WHITE};text-transform:uppercase">{h}</div>'
                 f'<div class="abs" style="left:{x}px;top:398px;width:200px"><div class="cd" style="font-size:14px;color:{WHITE}">{what}</div>'
                 f'<div class="cnum" style="margin-top:10px;font-size:12px;color:{GREY}">Who</div><div class="cd" style="font-size:14px;margin-top:3px">{who}</div>'
                 f'<div style="margin-top:10px;font:700 15px/1.25 BC;color:{COPPER if hot else GREY};text-transform:uppercase">{note}</div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; who buys, and when</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">One company specifies the cable, <em>another one buys it</em></div>
  {html}
  <div class="abs" style="left:64px;top:630px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};padding:14px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:16px"><b style="color:{WHITE}">The owner pays, the owner's engineer writes the spec, the EPC or package builder places
      the order.</b> Be in the spec early, and be ready when the EPC buys: by then the schedule is tight and cable is on the critical path.</div></div>
  {foot(n, N)}
</section>"""



SITES = [("New site", "Greenfield, grid-connected", 77.0, "renders/cover/K1_pro.png",
          "A new plant on open land, tied to the grid.", "Everything is new: the full cable schedule, the switchyard and an HV gen-tie to the POI."),
         ("New site", "Data-centre / behind-the-meter campus", 54.5, "renders/epic/E47_pro_clean.jpg",
          "Power built next to the load it serves.", "Modular engines, turbines and batteries; MV collection to the campus; fast schedules, bought by package builders."),
         ("Existing site", "Coal-site repower", 41.3, "renders/boilers/BR1_pro_clean.jpg",
          "New gas units on a retired coal or boiler site.", "Reuses the land, water and grid connection; new plant cable tied into an old switchyard."),
         ("Existing site", "Expansion at an operating plant", 21.4, "renders/modular/MP1_pro_clean.jpg",
          "New units beside ones that keep running.", "Work around live equipment; tie-ins wait for outages; shared switchyard and controls."),
         ("Existing site", "Industrial captive and site reuse", 11.6, "renders/boilers/BX1_pro_clean.jpg",
          "Power, often with steam, for a factory or refinery.", "Hazardous areas (MC-HL), tight routes, the host plant's own standards.")]


def s_sites(n, N):
    html = ""
    for k, (grp, h, gw, im, what, cab) in enumerate(SITES):
        x = 64 + k * 266
        new_site = grp == "New site"
        html += (f'<div class="abs" style="left:{x}px;top:214px;width:250px;height:420px;background:#181b1f;border-top:4px solid '
                 f'{COPPER if new_site else "#8e98a3"}">'
                 f'<img src="{pic(im)}" style="width:250px;height:120px;object-fit:cover;display:block">'
                 f'<div style="padding:14px 16px">'
                 f'<div style="font:800 40px/1 BC;color:{COPPER if new_site else WHITE}">{gw} <span style="font-size:18px;color:{GREY}">GW</span></div>'
                 f'<div class="ct" style="font-size:20px;margin-top:8px;min-height:40px">{h}</div>'
                 f'<div class="cd" style="font-size:14px;color:{WHITE};margin-top:8px">{what}</div>'
                 f'<div class="cd" style="font-size:13.5px;margin-top:8px">{cab}</div></div></div>')
    grp = (f'<div class="abs" style="left:64px;top:180px;width:516px;font:800 20px/1 BC;color:{COPPER};text-transform:uppercase;letter-spacing:.04em">'
           f'Greenfield &middot; new sites <span style="font:400 14px/1 B;color:{GREY};text-transform:none;letter-spacing:0">&nbsp; 137 GW in the register</span></div>'
           f'<div class="abs" style="left:596px;top:180px;width:780px;font:800 20px/1 BC;color:#c4cbd2;text-transform:uppercase;letter-spacing:.04em">'
           f'Brownfield &middot; existing sites <span style="font:400 14px/1 B;color:{GREY};text-transform:none;letter-spacing:0">&nbsp; 69 GW in the register</span></div>')
    band = (f'<div class="abs" style="left:64px;top:648px;width:1312px;background:#2a1d14;border-left:4px solid {COPPER};padding:12px 22px;box-sizing:border-box">'
            f'<div class="cd" style="font-size:16px"><b style="color:{WHITE}">And on plants already running:</b> outages, HRSG module replacements, upgrades and '
            f'conversions. There the outage clock is the cost, so cable is staged, pre-terminated and pulled fast. Utilities mostly reuse old sites; '
            f'IPPs and behind-the-meter developers mostly build new.</div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; kinds of project</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">Greenfield and brownfield: <em>five kinds of site</em></div>
  {grp}{html}{band}
  <div class="abs" style="left:64px;top:732px;{SRC}">Gross GW by site class, Southwire PowerGen register, Sep 11, 2026 (205.8 GW eligible, COD 2026&ndash;2035). Site classes provisional (Rev01).</div>
  {foot(n, N)}
</section>"""


def s_overview(n, N):
    route = "".join(f'<div style="display:flex;gap:18px;align-items:baseline;padding:10px 0;border-top:1px solid #2c3036">'
                    f'<div style="width:24px;font:800 22px/1 BC;color:{COPPER}">{k + 1}</div>'
                    f'<div style="font:700 19px/1.2 BC;color:{WHITE};text-transform:uppercase;letter-spacing:.03em">{st[0]}</div></div>'
                    for k, st in enumerate(STOPS))
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/cover/K1_pro.png')}" style="left:0;top:0;width:960px;height:765px;object-fit:cover;object-position:50% 70%">
  <div class="abs" style="left:640px;top:0;width:320px;height:765px;background:linear-gradient(90deg,rgba(14,16,18,0),#0e1012)"></div>
  <div class="abs kicker" style="left:990px;top:64px">The campus &nbsp;&middot;&nbsp; from the sea to the grid</div>
  <div class="abs h2" style="left:988px;top:92px;font-size:52px;width:420px">One site, <em>seven stops</em></div>
  <div class="abs" style="left:990px;top:250px;width:400px">{route}</div>
  <div class="abs lede" style="left:990px;top:650px;width:400px;font-size:15px">LNG arrives by ship at the marine terminal; the
    power leaves on 230 kV lines. Everything in between runs on cable.</div>
  {foot(n, N)}
</section>"""


STOPS = [
    ("Grid connection and switchyard", "renders/epic/E20_pro_clean.jpg",
     "Sends the plant's power to the 230 kV grid.",
     ["Generator step-up transformers: 21 kV up to 230 kV", "Breakers, disconnects, and a control house with protection relays"],
     ["HV conductor and 230 kV cable", "Control and relay cable from every breaker to the control house", "Fibre; the buried bare-copper ground grid"],
     "Every breaker out here has a bundle of control cable running back to the control house."),
    ("Turbine hall", "renders/cover/HALL9_hero_cable.jpg",
     "Three H-class gas turbines and one steam turbine turn the generators.",
     ["Isolated-phase bus from the generators to the step-up transformers", "Unit auxiliary transformers feed the 13.8 kV switchgear",
      "Static starters spin the gas turbines up"],
     ["MV-105 to big motors and transformers", "TC-ER power and control to the lube-oil and hydraulic skids",
      "Thousands of instrument pairs: vibration, temperatures"],
     "The machines make the power; the cable keeps them running and tells us how they feel."),
    ("HRSG and its e-house", "renders/boilers_iso/ISO1_pro_clean.jpg",
     "Turns turbine exhaust heat into steam; the SCR inside cuts NOx.",
     ["Two 13.8 kV feed pumps", "A transformer feeds the e-house: 480 V switchgear, MCCs, drives, DCS", "CEMS shelter at the stack"],
     ["One HRSG train: 707 cables, about 157,000 ft", "About three quarters are instrument and thermocouple pairs",
      "ARMOR-X MC-HL at the duct-burner gas skid"],
     "One boiler train is about 30 miles of cable, and most of it is small instrument cable."),
    ("Cooling and water", "renders/epic/E34_pro_clean.jpg",
     "The air-cooled condenser turns spent steam back into water: 80 fans, no cooling-tower water.",
     ["The R4 e-house: four VFD lineups drive the 80 fan motors", "Water-treatment MCCs"],
     ["VFD-rated cable to every fan (ARMOR-X MC-HL VFD, TC-ER VFD)", "Power and control in the water plant"],
     "Variable-frequency drives mean VFD-rated cable; ordinary cable fails early here."),
    ("Modular generation", "renders/epic/E77_pro.png",
     "Fast-start, flexible power beside the big plant.",
     ["Gas engines in a hall, aeroderivative and industrial gas-turbine packages, containers, trailers, fuel cells, microturbines",
      "Each unit on the 13.8 kV collector; inverters for the battery and fuel cells"],
     ["MV collection cable; DC cable at the battery and fuel cells", "Factory pre-wired skids and plug-in modules",
      "Pre-terminated and cut-to-length cable"],
     "Modular means factory pre-wiring: our opportunity for pre-terminated, cut-to-length cable."),
    ("Behind the meter: the data centre", "renders/epic/E47_pro_clean.jpg",
     "A data-centre campus powered directly by the plant's modular units, with the grid as backup.",
     ["13.8 to 34.5 kV step-up transformers and double-bus switchgear", "A 40 MW battery absorbs load steps",
      "Two data halls fed 2N through pad-mount transformers and UPS"],
     ["35 kV MV cable", "Large LV feeders to the UPS skids", "Fibre everywhere"],
     "Data centres are why gas is growing again, and they are cable-dense on both the A and the B side."),
    ("Fuel: gas yard and LNG", "renders/epic/E108_pro_clean.jpg",
     "Brings the fuel in and conditions it; an LNG satellite holds about three hours of backup fuel.",
     ["Metering and regulating station; the LNG e-house (13.8 kV / 480 V)", "Pumps, vaporizers, boil-off compressor"],
     ["ARMOR-X MC-HL for Class I Div 1 and 2", "TC-ER control, PLTC instrumentation and fire alarm on one strut rack"],
     "Wherever there's gas, the cable has to be rated for it."),
]


def s_stop(k, n, N):
    name, im, does, elec, cab, line = STOPS[k]
    li = lambda xs: "".join(f'<div class="li" style="font-size:16px;line-height:1.35;padding:7px 0 8px 20px">{x}</div>' for x in xs)
    sec = lambda h, body: (f'<div style="margin-top:22px"><div style="font:800 15px/1 BC;letter-spacing:.2em;color:{COPPER};'
                           f'text-transform:uppercase">{h}</div>{body}</div>')
    body = (f'<div style="font:400 19px/1.4 B;color:{WHITE}">{does}</div>' + sec("Electrical system", li(elec))
            + sec("Where the cable goes", li(cab)))
    return f"""
<section class="page slide">
  <img class="abs" src="{pic(im)}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:1440px;height:200px;background:linear-gradient(180deg,rgba(14,16,18,.85),rgba(14,16,18,0))"></div>
  <div class="abs" style="left:48px;top:36px;font:800 120px/1 BC;color:{COPPER};text-shadow:0 2px 10px rgba(0,0,0,.6)">{k + 1}</div>
  <div class="abs kicker" style="left:130px;top:52px;color:{WHITE}">Tour stop {k + 1} of 7</div>
  <div class="abs h2" style="left:128px;top:76px;font-size:46px;width:800px;text-shadow:0 2px 10px rgba(0,0,0,.6)">{name}</div>
  <div class="abs" style="left:1000px;top:0;width:440px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,0) 0%,
       rgba(14,16,18,.92) 10%,rgba(14,16,18,.97) 100%)"></div>
  <div class="abs" style="left:1040px;top:96px;width:356px">{body}</div>
  <div class="abs" style="left:48px;top:650px;width:900px;padding:14px 20px;background:rgba(14,16,18,.86);border-left:4px solid {COPPER};
       font:700 21px/1.3 BC;color:{WHITE};letter-spacing:.01em">&ldquo;{line}&rdquo;</div>
  <div class="abs" style="left:0;top:730px;width:1000px;height:80px;background:linear-gradient(180deg,rgba(14,16,18,0),rgba(14,16,18,.95) 55%)"></div>
  {foot(n, N).replace(" &middot; INTERNAL TRAINING", "")}
</section>"""


def schedule_numbers():
    import openpyxl
    rows = list(openpyxl.load_workbook(os.path.join(PLANT, "brochure", "SW-3X1_Cable_Schedule_and_BOM.xlsx"),
                                       read_only=True)["Cable Schedule"].iter_rows(values_only=True))[1:]
    ft = lambda r: math.ceil(((r[19] or 0) + (r[20] or 0) + 20) * 1.1 / 10) * 10 * r[13] * r[14]
    groups = {"Instrumentation": 0, "LV 600 V power": 0, "Control": 0, "MV / HV": 0, "Fibre, fire alarm, other": 0}
    for r in rows:
        c = str(r[8])
        g = ("Instrumentation" if c.startswith("Instr") else "LV 600 V power" if c.startswith("LV") else "Control"
             if c.startswith("Control") else "MV / HV" if c.startswith(("MV", "HV")) else "Fibre, fire alarm, other")
        groups[g] += ft(r)
    return len(rows), sum(r[13] * r[14] for r in rows), sum(groups.values()), groups


def s_number(n, N):
    runs, cables, total, groups = schedule_numbers()
    mx = max(groups.values())
    bars = ""
    for g, v in sorted(groups.items(), key=lambda kv: -kv[1]):
        w = 470 * v / mx
        bars += (f'<div style="display:flex;align-items:center;gap:16px;margin-top:22px">'
                 f'<div style="width:230px;font:700 16px/1.1 BC;color:{WHITE};text-transform:uppercase;letter-spacing:.04em;text-align:right">{g}</div>'
                 f'<div style="width:{w:.0f}px;height:26px;background:{COPPER};border-radius:0 4px 4px 0"></div>'
                 f'<div style="font:800 20px/1 BC;color:{WHITE}">{v / 1e6:.1f} M ft</div></div>')
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/nextgen/_src/E123_pro_clean.jpg')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover;filter:brightness(.22) saturate(.4)">
  <div class="abs kicker" style="left:64px;top:56px">Wire and cable takeaways</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">The whole campus in <em>one number</em></div>
  <div class="abs" style="left:64px;top:200px">
    <div style="font:800 128px/1 BC;color:{COPPER}">{total / 1e6:.1f}M</div>
    <div style="font:700 18px/1.2 BC;letter-spacing:.16em;color:{GREY};text-transform:uppercase;margin-top:6px">feet of cable
      &nbsp;&middot;&nbsp; about {total / 5280:,.0f} miles</div>
    <div style="display:flex;gap:44px;margin-top:40px">
      <div><div class="big">{runs:,}</div><div class="bigl">cable runs</div></div>
      <div><div class="big">{cables:,}</div><div class="bigl">cables</div></div></div>
    <div class="lede" style="width:420px;margin-top:40px;font-size:16px">From the model's cable schedule: every circuit on the campus,
      from the 230 kV switchyard to the last thermocouple.</div>
  </div>
  <div class="abs" style="left:560px;top:206px;width:840px">
    <div style="font:700 13px/1 BC;letter-spacing:.2em;color:{GREY};text-transform:uppercase;margin-left:246px">Footage by cable type</div>
    {bars}
    <div class="lede" style="margin:34px 0 0 246px;width:560px;font-size:16px;color:{WHITE}">Most of the footage is small cable:
      instrument and control. MV is the high-value part, but it isn't the volume.</div>
  </div>
  {foot(n, N)}
</section>"""


def s_close(n, N):
    three = [("Gas is growing again", "driven by data centres and the need for firm power."),
             ("Most of a plant's cable is small", "instrument and control; the big MV and power cable is the smaller share."),
             ("Southwire covers the whole plant", "one supplier, staged on SIMpull reels, spec-compliant from MV down to the thermocouple.")]
    html = "".join(f'<div style="display:flex;gap:26px;padding:24px 0;border-top:1px solid #2c3036"><div style="font:800 64px/.9 BC;'
                   f'color:{COPPER};width:54px">{k + 1}</div><div><div style="font:800 32px/1.05 BC;color:{WHITE};text-transform:uppercase">'
                   f'{h}</div><div style="font:400 17px/1.4 B;color:{GREY};margin-top:6px">{t}</div></div></div>'
                   for k, (h, t) in enumerate(three))
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/epic/E7_pro.png')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:1440px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,.96) 0%,rgba(14,16,18,.9) 55%,rgba(14,16,18,.55) 100%)"></div>
  <div class="abs kicker" style="left:64px;top:56px">Three things to remember</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Take <em>away</em></div>
  <div class="abs" style="left:64px;top:176px;width:860px">{html}</div>
  <div class="abs" style="left:990px;top:190px;width:390px;height:440px;background:rgba(24,27,31,.92);border-top:3px solid {COPPER};padding:30px;box-sizing:border-box">
    <img src="{LOGO}" style="width:300px;margin-bottom:26px">
    <div class="h2" style="font-size:72px">Q&amp;A</div>
    <div class="lede" style="font-size:16px;margin-top:18px">Questions from the chat. The recording and the 3D viewer link will be
      shared after the session.</div>
    <div style="font:700 15px/1.6 BC;letter-spacing:.06em;color:{WHITE};margin-top:34px">Stephan Hardt<br>
      <span style="color:{COPPER}">{credit.EMAIL}</span></div></div>
  {foot(n, N)}
</section>"""



# ---------------------------------------------------------------- framing slides (Oct 25): why you, dividers, offer, install, quiz, resources, sources
def s_why_you(n, N):
    roles = [("Sales and account managers", "Talk plant: name the zones, the buyers and the cable in each. Ask who the EPC is and when the cable package releases."),
             ("Customer service and inside sales", "Recognise a power-generation order: MV-105, ARMOR-X, TC-ER, instrumentation by the mile, reels per pull."),
             ("Supply chain and plants", "Long runs, many reels, schedule-critical: cut-to-length, SIMpull and on-time delivery decide the job."),
             ("Marketing, product and leadership", "Where the growth is: a boom-scale gas build, behind-the-meter power, and the fleet that needs upgrades.")]
    html = "".join(f'<div class="abs" style="left:{64 + (k % 2) * 664}px;top:{196 + (k // 2) * 200}px;width:648px;height:184px;background:#181b1f;'
                   f'border-top:4px solid {COPPER};padding:22px 26px;box-sizing:border-box">{db_circ(k + 1)}'
                   f'<div class="ct" style="font-size:26px;margin-top:12px">{h}</div><div class="cd" style="font-size:16px;margin-top:8px">{t}</div></div>'
                   for k, (h, t) in enumerate(roles))
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Welcome &nbsp;&middot;&nbsp; why this matters</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">What you will take <em>from this hour</em></div>
  {html}
  <div class="abs" style="left:64px;top:620px;width:1312px;background:#2a1d14;border-left:4px solid {COPPER};padding:14px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:18px"><b style="color:{WHITE}">No engineering background needed.</b> By the end you can walk a customer through a gas plant,
      point to where the cable goes, and know who buys it.</div></div>
  {foot(n, N)}
</section>"""


def db_circ(t):
    return (f'<div style="width:36px;height:36px;border-radius:50%;background:{COPPER};color:#121417;font:800 17px/36px BC;text-align:center">{t}</div>')


def s_div(n, N, num, title, em, sub, img, pos="50% 50%"):
    return f"""
<section class="page slide">
  <img class="abs" src="{pic(img)}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover;object-position:{pos}">
  <div class="abs" style="left:0;top:0;width:1440px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,.94) 0%,rgba(14,16,18,.75) 40%,rgba(14,16,18,.1) 75%)"></div>
  <div class="abs" style="left:72px;top:250px;font:800 150px/1 BC;color:{COPPER};opacity:.9">{num}</div>
  <div class="abs h2" style="left:70px;top:420px;font-size:80px;width:900px">{title} <em>{em}</em></div>
  <div class="abs lede" style="left:72px;top:530px;width:620px;font-size:20px">{sub}</div>
  {foot(n, N)}
</section>"""


OFFER_ICON = ["hv_xlpe", "mv105", "tc_er", "pltc", "armorx600", "pv", "shdgc", None]
OFFER = [("Grid connection", "HV XLPE transmission cable (230 kV) &middot; bare copper grounding", "C"),
         ("Power island: MV", "MV-105 EPR 133% (5&ndash;35 kV) &middot; ARMOR-X MC-HL 15 kV", "A"),
         ("Power island: LV and drives", "Type TC-ER power &middot; ARMOR-X MC-HL 600 V &middot; VFD-rated cable", "A"),
         ("Control and instrumentation", "TC-ER control &middot; PLTC / ITC shielded pairs &middot; thermocouple extension", "A"),
         ("Hazardous areas", "ARMOR-X MC-HL, Class I Div 2: gas skids, fuel yards, burner fronts", "D"),
         ("Battery storage", "PV / RHW-2 DC conductor (2 kV) &middot; MV-105 collection (35 kV)", "H"),
         ("Modular and temporary power", "Type SHD-GC portable MV &middot; Type W &middot; cam-lock sets", "I"),
         ("Installation", "SIMpull reels and SIMpull truck &middot; cut-to-length &middot; pre-terminated harness kits", "")]


def s_offer(n, N):
    rows = ""
    for k, (area, prod, _) in enumerate(OFFER):
        y = 186 + k * 58
        rows += (f'<div class="abs" style="left:64px;top:{y}px;width:1312px;height:1px;background:#2c3036"></div>'
                 + (f'<img class="abs" src="{pic("renders/icons/" + OFFER_ICON[k] + ".png")}" style="left:58px;top:{y + 3}px;width:52px;height:52px;object-fit:contain">' if OFFER_ICON[k] else "")
                 + f'<div class="abs" style="left:124px;top:{y + 15}px;width:310px;font:800 21px/1 BC;color:{COPPER if k == 7 else WHITE};text-transform:uppercase">{area}</div>'
                 f'<div class="abs cd" style="left:440px;top:{y + 15}px;width:936px;font-size:17px;color:#e6e3dd">{prod}</div>')
    svc = ["Spec support: sizing, derating, spec reviews", "Cut-to-length against the cable schedule", "Harness kits, pre-terminated and labelled",
           "Project logistics: reel tracking, sequenced deliveries", "Field support: pulling calcs, terminations, tests"]
    sv = " &nbsp;&middot;&nbsp; ".join(svc)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Wire and cable &nbsp;&middot;&nbsp; the offer</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">One supplier, <em>grid to thermocouple</em></div>
  {rows}
  <div class="abs" style="left:64px;top:660px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};padding:12px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:15px"><b style="color:{WHITE}">Plus the services:</b> {sv}.</div></div>
  <div class="abs" style="left:64px;top:736px;{cand_src()}">Typical Southwire families for each application; confirm constructions, sizes and listings against current Southwire specifications.</div>
  {foot(n, N)}
</section>"""


def cand_src():
    return "font:400 12px/1.4 B;color:#80868c"


def s_simpull(n, N):
    pts = [("SIMpull reels", "Several conductors paralleled on one reel: one pull per feeder instead of one per conductor."),
           ("SIMpull truck", "Delivery, payoff and reel return in one vehicle."),
           ("Cut-to-length", "Reels cut and labelled to the cable schedule, pull by pull: less waste, no field measuring."),
           ("Pre-terminated", "Factory-made, tested harnesses for skids and panels: on the critical path you test instead of terminate.")]
    li = "".join(f'<div style="margin-top:16px;border-left:4px solid {COPPER};padding-left:14px"><div class="ct" style="font-size:22px">{h}</div>'
                 f'<div class="cd" style="font-size:15px;margin-top:5px">{t}</div></div>' for h, t in pts)
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/epic/E64_pro.png')}" style="left:0;top:0;width:820px;height:765px;object-fit:cover">
  <div class="abs" style="left:620px;top:0;width:220px;height:765px;background:linear-gradient(90deg,rgba(14,16,18,0),#0e1012)"></div>
  <img class="abs" src="{pic('renders/epic/E58_pro.png')}" style="left:40px;top:520px;width:360px;height:200px;object-fit:cover;border:3px solid #0e1012">
  <div class="abs" style="left:40px;top:724px;font:700 12px/1 BC;letter-spacing:.08em;color:#d6d9dc;text-transform:uppercase">The reel yard: SIMpull reels staged for the pulls</div>
  <div class="abs" style="left:880px;top:56px;width:500px">
    <div class="kicker">Wire and cable &nbsp;&middot;&nbsp; installed faster</div>
    <div class="h2" style="font-size:50px;margin-top:10px">Accelerating <em>time to power</em></div>
    <div class="lede" style="font-size:16px;margin-top:12px">Cable is decided in the field, on the critical path. Every reel set-up and every termination saved is schedule saved.</div>
    {li}
  </div>
  {foot(n, N)}
</section>"""


QUIZ = [("Which cable type has the most miles in the power block?", ["MV / HV power", "LV power", "Instrumentation", "Fibre"], 2,
         "Instrumentation: about 200 of the 440 miles. The big cables get the attention; the small ones are most of the miles."),
        ("Who usually places the cable order?", ["The owner", "The owner's engineer", "The EPC or package builder", "The utility"], 2,
         "The EPC or package builder buys it; the owner's engineer specifies it. Be in the spec early, be ready when the EPC buys."),
        ("In a combined cycle, the steam turbine adds about how much more power, with no extra fuel?", ["5%", "One-third", "Double", "None"], 1,
         "About one-third: the HRSGs turn the gas turbines' hot exhaust into steam. Burn the gas once, use the heat twice.")]


def s_quiz(n, N, answers=False):
    html = ""
    for k, (q, opts, a, why) in enumerate(QUIZ):
        y = 186 + k * 168
        o = ""
        for i, t in enumerate(opts):
            on = answers and i == a
            o += (f'<div style="flex:1;padding:10px 14px;background:{"#b4591f" if on else "#1f2328"};border-radius:4px;font:700 17px/1.1 BC;'
                  f'color:{WHITE};text-transform:uppercase"><span style="color:{WHITE if on else COPPER};margin-right:8px">{"ABCD"[i]}</span>{t}</div>')
        html += (f'<div class="abs" style="left:64px;top:{y}px;width:1312px"><div style="display:flex;gap:14px;align-items:baseline">'
                 f'<span style="font:800 30px/1 BC;color:{COPPER}">{k + 1}</span><span style="font:800 24px/1.1 BC;color:{WHITE};text-transform:uppercase">{q}</span></div>'
                 f'<div style="display:flex;gap:12px;margin-top:14px">{o}</div>'
                 + (f'<div class="cd" style="font-size:15px;margin-top:10px;color:#e6e3dd">{why}</div>' if answers else "") + '</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Knowledge check &nbsp;&middot;&nbsp; {"the answers" if answers else "Zoom poll"}</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">{"The answers" if answers else "Three questions,"} <em>{"and why" if answers else "one minute"}</em></div>
  {html}
  {foot(n, N)}
</section>"""


def s_resources(n, N):
    res = [("The 3D plant model", "The interactive viewer you saw today, with the Nov 11 tour and the cable X-ray. Link sent with the recording."),
           ("The brochures", "Wire &amp; cable for gas power &middot; EPC solutions &middot; boiler solutions."),
           ("The recording and these slides", "Shared after the session, with a glossary of the terms used today.")]
    team = [("Stephan Hardt", "PowerGen strategy, the plant model, owners and OEMs"), ("Patrick Ritchie", "EPC accounts"),
            ("Greyson", "EPC outreach to more gas-plant builders"), ("Phil Metz &middot; Bob Benish", "OEMs and package builders: e-houses, switchgear, modular power")]
    covers = "".join(f'<div style="flex:1"><img src="{pic(p)}" style="width:100%;height:150px;object-fit:cover;object-position:{pos};border:1px solid #2c3036">'
                     f'<div style="font:700 11px/1.2 BC;letter-spacing:.1em;color:{GREY};text-transform:uppercase;margin-top:6px">{t}</div></div>'
                     for p, pos, t in [("renders/cover/viewer_campus.jpg", "50% 50%", "3D viewer"), ("renders/brochure/page_01.jpg", "50% 0%", "Wire &amp; cable brochure"),
                                       ("renders/brochure_epc/prev_01.png", "50% 0%", "EPC solutions"), ("renders/deck/boilers/SW-3X1_boilers_1.png", "0% 0%", "Boiler solutions")])
    r = "".join(f'<div style="margin-top:18px;border-left:4px solid {COPPER};padding-left:14px"><div class="ct" style="font-size:22px">{h}</div>'
                f'<div class="cd" style="font-size:15px;margin-top:5px">{t}</div></div>' for h, t in res)
    t = "".join(f'<div style="margin-top:14px;display:flex;gap:16px;align-items:baseline;border-top:1px solid #2c3036;padding-top:12px">'
                f'<div style="width:230px;font:800 19px/1.1 BC;color:{WHITE};text-transform:uppercase">{a}</div><div class="cd" style="font-size:15px">{b}</div></div>' for a, b in team)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">After today</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:56px">Resources and <em>who to call</em></div>
  <div class="abs" style="left:64px;top:180px;width:600px"><div class="cnum" style="color:{WHITE}">Resources</div>{r}</div>
  <div class="abs" style="left:64px;top:500px;width:620px;display:flex;gap:14px">{covers}</div>
  <div class="abs" style="left:730px;top:180px;width:646px"><div class="cnum" style="color:{WHITE}">Power Generation Solutions team</div>{t}
    <div style="margin-top:26px;font:700 16px/1.5 BC;letter-spacing:.06em;color:{COPPER}">{credit.EMAIL}</div></div>
  {foot(n, N)}
</section>"""


SOURCES = [("Electricity mix 2025; planned 2026 additions", "EIA, Electricity explained (2025 utility-scale generation); EIA Today in Energy, Feb 2026"),
           ("Load growth, data centres", "Grid Strategies, National Load Growth Report, 2025 (forecast)"),
           ("378 GW pipeline, 52 GW building", "Global Energy Monitor, Aug 2026; early-stage proposals will not all be built"),
           ("Turbine lead times", "S&amp;P Global Commodity Insights, May 2025"),
           ("OEM backlogs and modular orders", "OEM releases, Q2-Q3 2026; Utility Dive, Aug 2026; POWER, Oct 2025 and Feb 2026"),
           ("Capacity added per year, 1996-2026", "EIA and Southwire provisional series, to be verified"),
           ("Cable opportunity, register, states, site classes", "Southwire PowerGen planning model and register, Sep 11, 2026: assumed rates and probabilities"),
           ("Plant types, grid voltages, units", "Typical industry ranges; vary by design"),
           ("Cable counts and miles", "SW-3X1 model cable schedule: conceptual, not engineered"),
           ("Plant and yard renders", "SW-3X1 plant model: conceptual and illustrative, not engineering data")]


def s_sources_app(n, N):
    rows = "".join(f'<div style="display:flex;gap:20px;border-top:1px solid #2c3036;padding:10px 0"><div style="width:420px;font:700 15px/1.3 BC;color:{WHITE};'
                   f'text-transform:uppercase;letter-spacing:.03em">{a}</div><div class="cd" style="font-size:14px;flex:1">{b}</div></div>' for a, b in SOURCES)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Appendix</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">Sources <em>and qualifiers</em></div>
  <div class="abs" style="left:64px;top:170px;width:1312px">{rows}</div>
  <div class="abs" style="left:64px;top:720px;font:700 13px/1 BC;letter-spacing:.12em;color:{COPPER};text-transform:uppercase">Verify all figures against primary sources before external use</div>
  {foot(n, N)}
</section>"""



BUCKETS = [("1", "Inside the packages", "renders/boilers_full/RA2_pro_clean.jpg", "OEMs, e-house and package builders",
            "E-house internals (switchgear and MCC interconnections, control and panel wire, short ties), turbine skids, modular gensets",
            "Every month, across many projects, months before site", "MV-105 ties, TC-ER, control and panel wire, pre-terminated harness kits",
            "Not in our 440 miles: a separate market on top"),
           ("2", "Between the packages", "renders/training/XR_CC2_copper.jpg", "The EPC or its electrical contractor",
            "Field cable from the e-houses out to every motor, valve, instrument and transformer: the X-ray",
            "Once per plant, when detailed design fixes the cable schedule", "MV-105, TC-ER, ARMOR-X MC-HL, VFD, PLTC / ITC, thermocouple; SIMpull, cut-to-length",
            "Most of the miles: ~440 in the power block"),
           ("3", "To the grid", "renders/epic/E20_pro.png", "The EPC's HV contractor or the utility",
            "GSU to switchyard, the gen-tie to the POI, grounding",
            "Early: HV cable has the longest lead time", "HV XLPE (69-345 kV), bare copper grounding",
            "Few cables, high value")]


def s_buckets(n, N):
    html = ""
    for k, (num, h, img, who, what, when, prod, size) in enumerate(BUCKETS):
        x = 64 + k * 444
        hot = k == 1
        html += (f'<div class="abs" style="left:{x}px;top:176px;width:420px;height:470px;background:{"#2a1d14" if hot else "#181b1f"};'
                 f'border-top:4px solid {COPPER if hot else "#5d636a"}">'
                 f'<img src="{pic(img)}" style="width:420px;height:110px;object-fit:cover;display:block">'
                 f'<div style="padding:12px 18px"><div style="display:flex;gap:10px;align-items:center">{db_circ(num)}'
                 f'<div class="ct" style="font-size:24px">{h}</div></div>'
                 f'<div class="cnum" style="margin-top:12px;font-size:11px;color:{GREY}">Who buys</div>'
                 f'<div style="font:800 18px/1.15 BC;color:{COPPER};text-transform:uppercase;margin-top:3px">{who}</div>'
                 f'<div class="cd" style="font-size:13.5px;margin-top:8px;color:#e6e3dd">{what}</div>'
                 f'<div class="cnum" style="margin-top:10px;font-size:11px;color:{GREY}">When</div><div class="cd" style="font-size:13.5px;margin-top:3px">{when}</div>'
                 f'<div class="cnum" style="margin-top:10px;font-size:11px;color:{GREY}">Our products</div><div class="cd" style="font-size:13.5px;margin-top:3px">{prod}</div>'
                 f'<div style="margin-top:12px;font:800 16px/1.2 BC;color:{WHITE};text-transform:uppercase">{size}</div></div></div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Who buys &nbsp;&middot;&nbsp; follow the cable, not the building</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:54px">Three buckets of cable, <em>three different buyers</em></div>
  {html}
  <div class="abs" style="left:64px;top:662px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};padding:12px 22px;box-sizing:border-box">
    <div class="cd" style="font-size:16px"><b style="color:{WHITE}">Starting in the e-house is not the same as being bought by the e-house builder.</b> Cover both:
      EPCs for the field cable; package and e-house builders for the cable inside. The builders buy every month and shape the spec at the terminations.</div></div>
  {foot(n, N)}
</section>"""



def s_hub(n, N):
    """Where every cable starts: the switchgear room, the VFD e-house and the control room (existing renders E85, E82, E84, E86)."""
    tiles = [("renders/epic/E82_pro_clean.jpg", "Switchgear", "13.8 and 4.16 kV lineups: every MV feeder starts here"),
             ("renders/epic/E84_pro_clean.jpg", "MCCs and drives", "480 V starters and VFDs: motors, fans and pumps"),
             ("renders/epic/E86_pro_clean.jpg", "Control room", "where the instrument and control cable comes home")]
    t = "".join(f'<div class="abs" style="left:880px;top:{150 + k * 196}px;width:500px;height:182px;background:#181b1f;display:flex">'
                f'<img src="{pic(p)}" style="width:230px;height:182px;object-fit:cover;flex:none"><div style="padding:16px 18px">'
                f'<div class="ct" style="font-size:22px">{h}</div><div class="cd" style="font-size:14px;margin-top:8px">{d}</div></div></div>'
                for k, (p, h, d) in enumerate(tiles))
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/epic/E85_pro_clean.jpg')}" style="left:0;top:0;width:860px;height:765px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:860px;height:765px;background:linear-gradient(180deg,rgba(14,16,18,.88) 0%,rgba(14,16,18,0) 26%,rgba(14,16,18,0) 74%,rgba(14,16,18,.9) 100%)"></div>
  <div class="abs kicker" style="left:56px;top:40px">Inside a gas plant &nbsp;&middot;&nbsp; the hub</div>
  <div class="abs h2" style="left:54px;top:66px;font-size:50px;width:780px">Where every <em>cable starts</em></div>
  <div class="abs" style="left:56px;top:676px;width:780px;font:400 17px/1.45 B;color:#e6e3dd">The R1 switchgear room from above, roof off. <b style="color:#fff">Power leaves
    the switchgear and MCCs; signals come home to the control room.</b> Every device in between is wired.</div>
  {t}
  {foot(n, N)}
</section>"""



def s_story(n, N):
    """Why we built the 3D model: V0 and V1 concept images (March) -> V2 drawing set and first 3D (Sep) -> V3 today."""
    H = "renders/training/history/"
    cols = [("V0", "March", "First sketches", [(H + "v0_concept_electrical.jpg", "45% 35%"), (H + "v1_concept_cables.jpg", "50% 50%")],
             "Cable routes colour-coded, but generic: non-US voltages (11 kV, 138 kV), no cable counts.", "#4a4f55"),
            ("V1", "March", "A branded concept", [(H + "v0_branded.jpg", "50% 50%"), (H + "v0_ghost.jpg", "50% 50%"),
             (H + "v1_turbine_hall.jpg", "50% 50%"), (H + "v1_hrsg_trains.jpg", "50% 55%")],
             "A Southwire-branded plant, the turbine hall and HRSGs drawn in detail: good for a cover, but still invented, with nothing to measure.", "#5d636a"),
            ("V2", "September", "A real layout, then 3D", [(H + "v2_drawing_set.jpg", "20% 30%"), (H + "v2_first_3d.jpg", "50% 50%")],
             "The SK-3X1 drawing set: a 3x1 combined cycle at 230 / 13.8 / 4.16 kV and 480 V, 16 sheets. Then the first 3D model, built from it.", "#8e98a3"),
            ("V3", "October &ndash; today", "A plant you can measure", [("renders/nextgen/_src/E123_pro_clean.jpg", "50% 50%"), ("renders/training/XR_CC2_copper.jpg", "50% 50%")],
             "Every building, tray and route at LOD 3; a 6,011-run cable schedule; the X-ray; the guided tour; every render in our brochures and decks.", COPPER)]
    html = ""
    for k, (v, when, h, imgs, t, col) in enumerate(cols):
        x = 64 + k * 332
        w = (316 - 4) // 2
        ih = 200 if len(imgs) <= 2 else 98                               # four images: a 2 x 2 grid in the same space
        strip = "".join(f'<img src="{pic(p)}" style="width:{w}px;height:{ih}px;object-fit:cover;object-position:{pos};display:block;background:#fff">' for p, pos in imgs)
        html += (f'<div class="abs" style="left:{x}px;top:176px;width:316px;height:420px;background:{"#2a1d14" if k == 3 else "#181b1f"};border-top:4px solid {col}">'
                 f'<div style="display:flex;flex-wrap:wrap;gap:4px;height:200px;overflow:hidden">{strip}</div><div style="padding:14px 18px">'
                 f'<div style="display:flex;align-items:baseline;gap:10px"><span style="font:800 38px/1 BC;color:{col if k else "#8e98a3"}">{v}</span>'
                 f'<span class="cnum" style="color:{GREY}">{when}</span></div>'
                 f'<div class="ct" style="font-size:22px;margin-top:8px">{h}</div><div class="cd" style="font-size:14px;margin-top:6px">{t}</div></div></div>')
        if k < 3:
            html += f'<div class="abs" style="left:{x + 318}px;top:370px;font:800 22px/1 BC;color:{COPPER}">&rsaquo;</div>'
    why = [("See the whole plant", "end to end, not one product at a time"), ("Measure, don't guess", "cable from a real layout, not rules of thumb"),
           ("One source", "the brochures, decks, viewer, schedule and this training"), ("Speak the buyer's language", "zones, packages and e-houses, the way EPCs and OEMs think")]
    w4 = "".join(f'<div style="flex:1;border-left:3px solid {COPPER};padding-left:12px"><div style="font:800 17px/1.1 BC;color:{WHITE};text-transform:uppercase">{a}</div>'
                 f'<div class="cd" style="font-size:13.5px;margin-top:4px">{b}</div></div>' for a, b in why)
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Welcome &nbsp;&middot;&nbsp; why a 3D model</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:54px">From pictures <em>to a plant you can measure</em></div>
  {html}
  <div class="abs cnum" style="left:64px;top:614px;color:{WHITE}">Why we built it</div>
  <div class="abs" style="left:64px;top:640px;width:1312px;display:flex;gap:22px">{w4}</div>
  {foot(n, N)}
</section>"""


STORY_H = "renders/training/history/"


def story_half(x, v, when, h, hero, row, text, col, hot=False):
    """One version: a big hero picture, a row of up to three supporting pictures, then the words."""
    H = STORY_H
    rw = (648 - 8 * (len(row) - 1)) // max(len(row), 1)
    r = "".join(f'<img src="{pic(H + p if not p.startswith("renders/") else p)}" style="width:{rw}px;height:128px;object-fit:cover;object-position:{pos};'
                f'display:block;background:#fff">' for p, pos in row)
    hp, hpos = hero
    return (f'<div class="abs" style="left:{x}px;top:168px;width:648px;height:560px;background:{"#2a1d14" if hot else "#181b1f"};border-top:4px solid {col}">'
            f'<img src="{pic(H + hp if not hp.startswith("renders/") else hp)}" style="width:648px;height:268px;object-fit:cover;object-position:{hpos};display:block;background:#fff">'
            f'<div style="display:flex;gap:8px;margin-top:8px">{r}</div><div style="padding:14px 22px">'
            f'<div style="display:flex;align-items:baseline;gap:14px"><span style="font:800 44px/1 BC;color:{col}">{v}</span>'
            f'<span class="ct" style="font-size:26px">{h}</span><span class="cnum" style="color:{GREY};margin-left:auto">{when}</span></div>'
            f'<div class="cd" style="font-size:15.5px;margin-top:8px">{text}</div></div></div>')


def s_story1(n, N):
    a = story_half(64, "V0", "March", "First sketches", ("v0_concept_electrical.jpg", "50% 40%"), [("v1_concept_cables.jpg", "50% 50%")],
                   "Cable routes colour-coded to tell the story. But generic: non-US voltages (11 kV, 138 kV), invented equipment, no cable counts.", "#8e98a3")
    b = story_half(728, "V1", "March", "A branded concept", ("v0_branded.jpg", "50% 50%"),
                   [("v0_ghost.jpg", "50% 50%"), ("v1_turbine_hall.jpg", "50% 50%"), ("v1_hrsg_trains.jpg", "50% 55%")],
                   "A Southwire-branded plant, the turbine hall and HRSGs drawn in detail. Good for a cover, but still invented: nothing you can measure.", "#c4cbd2")
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Welcome &nbsp;&middot;&nbsp; why a 3D model &nbsp;&middot;&nbsp; 1 of 2</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">It started with pictures <em>that looked right</em></div>
  {a}{b}
  {foot(n, N)}
</section>"""


def s_story2(n, N):
    a = story_half(64, "V2", "Spring &ndash; summer", "3D studies", ("v2_4.jpg", "50% 45%"),
                   [("v2_1.jpg", "50% 50%"), ("v2_6.jpg", "50% 40%"), ("v2_7.jpg", "50% 55%")],
                   "Real plant elements in 3D: the hall, gas turbines, HRSGs, engines, the plant zones. Closer, but not to scale and not routed: still no cable to count.", "#c4cbd2")
    b = story_half(728, "V3", "September &ndash; today", "A plant you can measure", ("renders/cover/K1_pro.png", "50% 50%"),
                   [("v2_drawing_set.jpg", "20% 30%"), ("v2_first_3d.jpg", "50% 50%"), ("renders/training/XR_CC2_copper.jpg", "50% 50%")],
                   "Drafted first: the SK-3X1 drawing set (16 sheets, 230 / 13.8 / 4.16 kV, 480 V), then the model built from it. LOD 3, a 6,011-run cable schedule, the X-ray, the tour.", COPPER, True)
    why = " &nbsp;&middot;&nbsp; ".join(["See the whole plant", "Measure, don't guess", "One source for brochures, decks, viewer and schedule", "Speak the buyer's language"])
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Welcome &nbsp;&middot;&nbsp; why a 3D model &nbsp;&middot;&nbsp; 2 of 2</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:52px">Then a plant <em>you can measure</em></div>
  {a}{b}
  <div class="abs" style="left:64px;top:740px;width:1312px;font:700 14px/1 BC;letter-spacing:.08em;color:{COPPER};text-transform:uppercase">Why we built it: &nbsp;<span style="color:{WHITE}">{why}</span></div>
  {foot(n, N)}
</section>"""


def reused(fn, n, N, kicker):
    sec = fn()
    sec = re.sub(r"BOILERS \d+/16", f"{TITLE} {n}/{N}", sec)
    sec = sec.replace("Boiler solutions", kicker)
    return sec


def main():
    import pymupdf
    os.makedirs(OUT, exist_ok=True)
    import deck_training_candidates as cand                   # picked candidates (Oct 24): B, C, E, F, J; the combined-cycle build (c_cc1-4) replaces the cycle diagram
    cand.FOOT_LEFT = "SW-3X1 MODEL &middot; CONCEPTUAL ILLUSTRATION, NOT ENGINEERED &middot; INTERNAL TRAINING"
    N = 59                                                     # main deck 1-52, backup 53-59 (Oct 25)
    D = lambda n, *a: (lambda: s_div(n, N, *a))
    plan = [lambda: s_title(), lambda: s_agenda(2, N), lambda: s_why_you(3, N), lambda: s_story1(4, N), lambda: s_story2(5, N),
            D(6, "01", "How power", "is made", "Every plant is a black box: what goes in, what comes out, and why we zoom in on gas.", "renders/cover/K5_pro.png"),
            lambda: s_blackbox(7, N), lambda: s_sources(8, N), lambda: s_system(9, N),
            D(10, "02", "The", "market", "A boom-scale gas build, and cable is on the critical path.", "renders/cover/K11_pro.png"),
            lambda: s_glance(11, N), lambda: s_load(12, N), lambda: s_backlog(13, N), lambda: s_prize(14, N), lambda: s_where(15, N), lambda: s_map(16, N),
            D(17, "03", "Inside a", "gas plant", "The machines, the grid, and the cable that ties them together.", "renders/training/CC2_pro_clean.jpg"),
            lambda: s_box(18, N), lambda: cand.c_day(19, N),
            lambda: cand.c_xray_intro(20, N), lambda: cand.c_cc1(21, N), lambda: cand.c_cc2(22, N), lambda: cand.c_cc3(23, N), lambda: cand.c_cc4(24, N), lambda: cand.c_xray_copper(25, N), lambda: cand.c_xray(26, N),
            lambda: cand.c_grid(27, N), lambda: reused(db.slide_system, 28, N, "Fundamentals &nbsp;&middot;&nbsp; the voltage ladder"),
            lambda: cand.c_cable101(29, N),
            lambda: cand.c_stress(30, N), lambda: s_owners(31, N), lambda: s_sites(32, N), lambda: s_buy(33, N), lambda: s_buckets(34, N), lambda: s_hub(35, N), lambda: cand.c_modern(36, N),
            D(37, "04", "The", "tour", "Seven stops on the SW-3X1 campus: what it does, its electrical system, its cable.", "renders/cover/K1_pro.png", "50% 70%"),
            lambda: s_overview(38, N)]
    plan += [(lambda k=k: s_stop(k, 39 + k, N)) for k in range(7)]
    plan += [D(46, "05", "Wire and", "cable", "One supplier from the grid to the thermocouple, installed faster.", "renders/training/XR_CC2_copper.jpg"),
             lambda: s_number(47, N), lambda: s_offer(48, N), lambda: s_simpull(49, N), lambda: s_quiz(50, N),
             lambda: s_close(51, N), lambda: s_resources(52, N),
             D(53, "B", "Backup", "slides", "Extra detail if questions go there, and the sources.", "renders/epic/E66_pro.png"),
             lambda: s_quiz(54, N, answers=True), lambda: s_types(55, N), lambda: reused(db.slide_basics, 56, N, "Backup &nbsp;&middot;&nbsp; fundamentals"),
             lambda: s_follow(57, N), lambda: reused(db.slide_spec, 58, N, "Backup &nbsp;&middot;&nbsp; the HRSG spec"), lambda: s_sources_app(59, N)]
    assert len(plan) == N
    head = f"<!doctype html><html><head><meta charset='utf-8'><style>{db.CSS}</style></head><body>"
    out = pymupdf.open()
    for i, f in enumerate(plan):
        sec = f().replace('<section class="page slide">', '<section class="page slide"><div class="s">', 1).replace(
            "</section>", "</div></section>")
        hp = os.path.join(OUT, f"_s{i}.html")
        open(hp, "w").write(head + sec + "</body></html>")
        pdf = hp.replace(".html", ".pdf")
        subprocess.run([bz.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", bz.url(hp)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.insert_pdf(pymupdf.open(pdf))
        os.remove(pdf)
        os.remove(hp)
    p = os.path.join(OUT, "SW-3X1_Nov11_training.pdf")
    out.save(p, garbage=4, deflate=True)                     # garbage=4 merges the images repeated across slides
    from PIL import Image
    jd = os.path.join(OUT, "jpg")                              # JPG copies for phones (the PDF does not load fully on some)
    os.makedirs(jd, exist_ok=True)
    for f in os.listdir(OUT) + os.listdir(jd):
        if re.match(r"(training|slide)_\d+\.(png|jpg)$", f):
            os.remove(os.path.join(jd if f.endswith(".jpg") else OUT, f))
    ims = []
    for i, pg in enumerate(out):
        png = os.path.join(OUT, f"training_{i + 1:02d}.png")
        pg.get_pixmap(dpi=96).save(png)
        ims.append(Image.open(png).convert("RGB"))
        ims[-1].save(os.path.join(jd, f"slide_{i + 1:02d}.jpg"), quality=90)
    w, h = 960, 540
    for name, rng in (("opening_and_market_1-16", range(0, 16)), ("inside_a_gas_plant_17-36", range(16, 36)), ("tour_and_close_37-52", range(36, 52)), ("backup_53-59", range(52, 59)), ("all_slides", range(len(ims)))):
        rng = list(rng)
        rows = (len(rng) + 1) // 2
        sheet = Image.new("RGB", (w * 2 + 30, h * rows + 15 * (rows + 1)), (40, 40, 40))
        for k, i in enumerate(rng):
            sheet.paste(ims[i].resize((w, h)), (10 + (k % 2) * (w + 10), 15 + (k // 2) * (h + 15)))
        sheet.save(os.path.join(jd, f"{name}.jpg"), quality=88)
    print("wrote", p, len(out), "slides")


if __name__ == "__main__":
    main()
