"""Nov 11 internal training "Inside Power Generation" (presentation/Nov11_run_of_show.md): 26 slides at 1440 x 810,
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
    if path.endswith(".png") and os.path.getsize(path) > 1e6:            # raw renders: embed as JPEG to keep the PDF small
        import tempfile
        from PIL import Image
        jpg = os.path.join(tempfile.gettempdir(), "deck_training_" + os.path.basename(path)[:-4] + ".jpg")
        if not os.path.exists(jpg) or os.path.getmtime(jpg) < os.path.getmtime(path):
            Image.open(path).convert("RGB").save(jpg, quality=90)
        path = jpg
    return bz.url(path)


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


AGENDA = [("1:30", "Welcome", "why this matters", "3"),
          ("1:33", "Market and fundamentals", "the gas build and the cable prize; the black box, owners, the POI corridor", "18"),
          ("1:51", "The 3D tour", "seven stops: what it does, its electrical system, its cable", "22"),
          ("2:13", "Wire and cable takeaways", "the whole plant in one number, products, pain points", "9"),
          ("2:22", "Q&amp;A", "questions from the chat", "8")]


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
    def node(x, big, lab, sub, bg):
        return (f'<div class="abs" style="left:{x}px;top:250px;width:260px;text-align:center">'
                f'<div style="margin:0 auto;width:200px;height:200px;border-radius:50%;background:{bg};display:flex;align-items:center;'
                f'justify-content:center;font:800 34px/1 BC;color:{WHITE};text-transform:uppercase">{big}</div>'
                f'<div style="font:800 26px/1 BC;color:{WHITE};text-transform:uppercase;margin-top:26px">{lab}</div>'
                f'<div class="cd" style="font-size:16px;margin-top:8px">{sub}</div></div>')
    arrow = lambda x: f'<div class="abs" style="left:{x}px;top:342px;width:120px;height:3px;background:{COPPER}"></div><div class="abs" style="left:{x + 112}px;top:334px;width:0;height:0;border-left:16px solid {COPPER};border-top:9px solid transparent;border-bottom:9px solid transparent"></div>'
    box = (f'<div class="abs" style="left:590px;top:250px;width:260px;height:200px;background:#0b0c0e;border:3px solid {COPPER};'
           f'border-radius:6px;display:flex;align-items:center;justify-content:center;font:800 44px/1 BC;color:{WHITE};text-align:center">BLACK<br>BOX</div>'
           f'<div class="abs cd" style="left:590px;top:476px;width:260px;text-align:center;font-size:16px">Thermal conversion</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Every thermal project <em>is this</em></div>
  <div class="abs lede" style="left:64px;top:160px;width:1100px">Input &rarr; conversion &rarr; output. The complexity is what's inside the box, and what's around it.</div>
  {node(230, "Fuel", "Input", "fuel / energy source", "#3b7a4a")}{arrow(465)}{box}{arrow(865)}{node(950, "Power", "Output", "dispatchable power", "#2f63b5")}
  <div class="abs lede" style="left:64px;top:620px;width:1300px;font-size:18px">Gas turbine, combined cycle or engines: <b style="color:{WHITE}">the same physics on every project.</b>
    Today we open the box and follow the power out of it.</div>
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
    eq = [("ProjectCo", "SPV / LLC"), ("Asset", "conversion plant"), ("Contract", "PPA / off-take"), ("Customer", "off-taker / load"),
          ("Capital", "PE / tax equity"), ("Market", "ERCOT, PJM, MISO")]
    e = "".join(f'<div style="display:inline-block;vertical-align:top;width:150px;text-align:center">'
                f'<div style="font:800 24px/1 BC;color:{WHITE};text-transform:uppercase">{a}</div><div class="cd" style="font-size:14px;margin-top:6px">{b}</div></div>'
                + (f'<div style="display:inline-block;vertical-align:top;width:22px;font:800 24px/1 BC;color:{COPPER}">+</div>' if k < 5 else "")
                for k, (a, b) in enumerate(eq))
    arch = [("IOUs / co-ops", "Regulated", ["Utility-led, rate-based ownership", "Own and operate generation", "Buy like utilities: standards, cycles"]),
            ("Hybrid IPPs", "Mixed model", ["Utility-affiliated IPP subsidiaries", "Bridge regulated and competitive", "Two buying behaviours"]),
            ("Pure IPPs", "Competitive", ["Privately owned, PE-backed projects", "A direct fit with the project equation", "Speed and cost drive decisions"])]
    cards = ""
    for k, (h, tag, items) in enumerate(arch):
        hot = k == 2
        li = "".join(f'<div class="cd" style="font-size:16px;margin-top:10px;padding-left:14px;position:relative">'
                     f'<span style="position:absolute;left:0;top:8px;width:6px;height:6px;background:{COPPER}"></span>{t}</div>' for t in items)
        cards += (f'<div class="abs" style="left:{64 + k * 444}px;top:420px;width:420px;height:220px;background:{"#2a1d14" if hot else "#181b1f"};'
                  f'border-top:4px solid {COPPER if hot else "#5d636a"};{"border:1px solid #b4591f;border-top:4px solid " + COPPER + ";" if hot else ""}padding:22px 26px;box-sizing:border-box">'
                  f'<div class="ct" style="font-size:28px">{h} <span style="font:700 14px/1 BC;letter-spacing:.14em;color:{COPPER};margin-left:10px">{tag}</span></div>{li}</div>')
    return f"""
<section class="page slide">
  <div class="abs kicker" style="left:64px;top:56px">Fundamentals &nbsp;&middot;&nbsp; who buys</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Same physics, <em>different owners</em></div>
  <div class="abs lede" style="left:64px;top:156px;width:1200px;font-size:17px">The owner decides how the project is structured, and how it gets bought.</div>
  <div class="abs" style="left:64px;top:206px;width:1312px;height:160px;background:#181b1f;border-top:4px solid {COPPER};padding:22px 26px;box-sizing:border-box">
    <div class="cnum">The structural equation</div>
    <div style="margin-top:26px;white-space:nowrap"><div style="display:inline-block;vertical-align:top;width:170px;font:800 28px/1 BC;color:{COPPER};text-transform:uppercase">Thermal IPP =</div>{e}</div></div>
  <div class="abs cnum" style="left:64px;top:392px;color:{WHITE}">Power owner archetypes</div>
  {cards}
  <div class="abs" style="left:952px;top:652px;font:700 14px/1 BC;letter-spacing:.1em;color:{COPPER};text-transform:uppercase">Primary focus for competitive thermal power</div>
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
  <div class="abs kicker" style="left:64px;top:56px">Wire and cable takeaways</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">The whole plant in <em>one number</em></div>
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
  <div class="abs kicker" style="left:64px;top:56px">Three things to remember</div>
  <div class="abs h2" style="left:62px;top:84px;font-size:58px">Take <em>away</em></div>
  <div class="abs" style="left:64px;top:176px;width:860px">{html}</div>
  <div class="abs" style="left:990px;top:190px;width:390px;height:440px;background:#181b1f;border-top:3px solid {COPPER};padding:30px;box-sizing:border-box">
    <img src="{LOGO}" style="width:300px;margin-bottom:26px">
    <div class="h2" style="font-size:72px">Q&amp;A</div>
    <div class="lede" style="font-size:16px;margin-top:18px">Questions from the chat. The recording and the 3D viewer link will be
      shared after the session.</div>
    <div style="font:700 15px/1.6 BC;letter-spacing:.06em;color:{WHITE};margin-top:34px">Stephan Hardt<br>
      <span style="color:{COPPER}">{credit.EMAIL}</span></div></div>
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
    N = 26                                                     # s_q3 (Q3 progress) taken out on Oct 24; kept for later use
    plan = [lambda: s_title(), lambda: s_agenda(2, N), lambda: s_glance(3, N), lambda: s_load(4, N), lambda: s_backlog(5, N),
            lambda: s_prize(6, N), lambda: s_where(7, N), lambda: s_map(8, N),
            lambda: s_blackbox(9, N), lambda: s_anatomy(10, N),
            lambda: reused(db.slide_cycle, 11, N, "Fundamentals"), lambda: reused(db.slide_basics, 12, N, "Fundamentals"),
            lambda: s_owners(13, N), lambda: s_corridor(14, N), lambda: s_overview(15, N)]
    plan += [(lambda k=k: s_stop(k, 16 + k, N)) for k in range(7)]
    plan += [lambda: s_number(23, N), lambda: reused(db.slide_spec, 24, N, "Wire and cable takeaways"),
             lambda: reused(db.slide_value, 25, N, "Wire and cable takeaways"), lambda: s_close(26, N)]
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
    out.save(p, garbage=3, deflate=True)
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
    for name, rng in (("market_slides_3-8", range(2, 8)), ("fundamentals_9-14", range(8, 14)), ("all_slides", range(len(ims)))):
        rng = list(rng)
        rows = (len(rng) + 1) // 2
        sheet = Image.new("RGB", (w * 2 + 30, h * rows + 15 * (rows + 1)), (40, 40, 40))
        for k, i in enumerate(rng):
            sheet.paste(ims[i].resize((w, h)), (10 + (k % 2) * (w + 10), 15 + (k // 2) * (h + 15)))
        sheet.save(os.path.join(jd, f"{name}.jpg"), quality=88)
    print("wrote", p, len(out), "slides")


if __name__ == "__main__":
    main()
