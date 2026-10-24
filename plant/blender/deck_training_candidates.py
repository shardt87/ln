"""Candidate slides for the Nov 11 training deck (the author picks which ones go in): generator basics, the grid journey,
a day on the grid, front- vs behind-the-meter, cable 101, what a plant does to a cable, future fuels, units and scale,
glossary, the modern campus (5G, EV, BTM, LNG by sea, H2, CCS). Same look and helpers as deck_training.py.

    python3 blender/deck_training_candidates.py   -> renders/deck/training/candidates/ (PDF, slide JPGs, one contact sheet)
"""
import os
import subprocess

import brochure_zones as bz
import deck_boilers as db
from deck_training import (COPPER, GREY, PLANT, SRC, WHITE, circ, foot, pic, schedule_numbers)

OUT = os.path.join(PLANT, "renders", "deck", "training", "candidates")
LI = (lambda t, fs=15: f'<div class="cd" style="font-size:{fs}px;margin-top:9px;padding-left:14px;position:relative">'
      f'<span style="position:absolute;left:0;top:{fs // 2}px;width:6px;height:6px;background:{COPPER}"></span>{t}</div>')


def band(text, top=628):
    return (f'<div class="abs" style="left:64px;top:{top}px;width:1312px;background:#181b1f;border-left:4px solid {COPPER};'
            f'padding:13px 22px;box-sizing:border-box"><div class="cd" style="font-size:17px">{text}</div></div>')


def head(kick, title, em, lede=""):
    return (f'<div class="abs kicker" style="left:64px;top:56px">{kick}</div>'
            f'<div class="abs h2" style="left:62px;top:84px;font-size:56px;width:1320px">{title} <em>{em}</em></div>'
            + (f'<div class="abs lede" style="left:64px;top:158px;width:1250px;font-size:17px">{lede}</div>' if lede else ""))


FOOT_LEFT = "CANDIDATE SLIDE &middot; INSIDE POWER GENERATION &middot; INTERNAL TRAINING"   # deck_training.py sets the deck's own


def page(n, N, body):
    return f'<section class="page slide">{body}{foot(n, N, FOOT_LEFT)}</section>'


def c_generator(n, N):
    steps = [("Spin", "Steam, hot gas, an engine, water or wind turns a shaft.", "#b4591f"),
             ("Magnet in a coil", "The shaft spins a magnet (the rotor) inside copper windings (the stator).", "#c9a227"),
             ("Current", "The moving magnetic field pushes current through the copper: alternating current, 60 times a second.", "#2f63b5")]
    html = ""
    for k, (h, t, col) in enumerate(steps):
        x = 64 + k * 444
        html += (f'<div class="abs" style="left:{x}px;top:200px;width:420px;height:250px;background:#181b1f;border-top:4px solid {col};padding:22px 24px;box-sizing:border-box">'
                 f'{circ(k + 1, 44, col, WHITE, 20)}<div class="ct" style="font-size:28px;margin-top:16px">{h}</div>'
                 f'<div class="cd" style="font-size:17px;margin-top:10px">{t}</div></div>')
        if k < 2:
            html += f'<div class="abs" style="left:{x + 424}px;top:308px;font:800 26px/1 BC;color:{COPPER}">&rsaquo;</div>'
    facts = [("60 Hz", "US grid frequency: every generator on it spins in step"), ("3,600 rpm", "a two-pole gas or steam turbine generator at 60 Hz"),
             ("21 kV", "SW-3X1's generators; the step-up transformer lifts it to 230 kV"), ("Copper", "the windings, the bus, the cable: all of it carries the current out")]
    f = "".join(f'<div class="abs" style="left:{64 + k * 334}px;top:478px;width:310px;border-top:3px solid {COPPER};padding-top:10px">'
                f'<div style="font:800 34px/1 BC;color:{COPPER}">{a}</div><div class="cd" style="font-size:14px;margin-top:6px">{b}</div></div>'
                for k, (a, b) in enumerate(facts))
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; physics in one slide", "How a generator", "makes electricity",
                           "Almost every power plant ends the same way: a spinning magnet inside a coil of copper.") + html + f
                + band("<b style='color:#f4f1ec'>Solar panels, fuel cells and batteries are the exceptions:</b> they make DC, and an inverter turns it into 60 Hz AC for the grid."))


def c_grid(n, N):
    legs = [("Generator", "13.8&ndash;25 kV", "21 kV in SW-3X1", "isolated-phase bus, MV-105"),
            ("Step-up (GSU)", "&rarr; 115&ndash;765 kV", "230 kV in SW-3X1", "HV XLPE cable, switchyard bus"),
            ("Transmission", "115&ndash;765 kV", "long distance, overhead", "overhead conductor, OPGW"),
            ("Substation", "&rarr; 4&ndash;35 kV", "steps it down for the town", "substation cable, grounding"),
            ("Distribution", "4&ndash;35 kV", "feeders along the streets", "MV URD, overhead distribution"),
            ("Customer", "480 / 240 / 120 V", "factory, office, home", "building wire, MC, service entrance")]
    html = ""
    for k, (h, v, note, cab) in enumerate(legs):
        x = 64 + k * 220
        hot = k < 2
        html += (f'<div class="abs" style="left:{x}px;top:200px;width:204px;height:330px;background:#181b1f;border-top:4px solid {COPPER if hot else "#5d636a"};'
                 f'padding:18px 16px;box-sizing:border-box">{circ(k + 1, 38, COPPER if hot else "#5d636a", "#121417" if hot else WHITE, 17)}'
                 f'<div class="ct" style="font-size:22px;margin-top:14px">{h}</div>'
                 f'<div style="font:800 24px/1.1 BC;color:{COPPER};margin-top:10px">{v}</div>'
                 f'<div class="cd" style="font-size:14px;margin-top:8px">{note}</div>'
                 f'<div class="cnum" style="margin-top:18px;font-size:11px;color:{GREY}">Cable</div><div class="cd" style="font-size:14px;color:{WHITE};margin-top:4px">{cab}</div></div>')
        if k < 5:
            html += f'<div class="abs" style="left:{x + 206}px;top:356px;font:800 18px/1 BC;color:{COPPER}">&rsaquo;</div>'
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; beyond the fence", "From the generator", "to the light switch",
                           "Power is made at medium voltage, raised to high voltage to travel, then stepped down again near the customer.")
                + html + f'<div class="abs" style="left:64px;top:548px;width:424px;font:700 14px/1.3 BC;letter-spacing:.08em;color:{COPPER};text-transform:uppercase">&larr; inside the plant: today</div>'
                + band("<b style='color:#f4f1ec'>Higher voltage, lower current, smaller losses:</b> that is why transmission runs at hundreds of kV. "
                       "Southwire has a product family at every step, from the generator to the outlet."))


def c_day(n, N):
    import math
    W, H, X0, Y0 = 900, 340, 120, 230
    hrs = [h / 2 for h in range(49)]
    def load(h):
        return 0.62 + 0.13 * math.exp(-((h - 8.5) / 2.2) ** 2) + 0.30 * math.exp(-((h - 18.5) / 2.8) ** 2) - 0.05 * math.exp(-((h - 3.5) / 2.5) ** 2)
    def solar(h):
        return max(0, 0.30 * math.cos((h - 13) / 6.5 * math.pi / 2)) if 6.5 < h < 19.5 else 0
    base = lambda h: 0.42
    layers = [("Baseload: nuclear, coal, combined cycle", "#5d636a", lambda h: base(h)),
              ("Solar", "#c9a227", lambda h: base(h) + min(solar(h), load(h) - base(h))),
              ("Mid-merit: combined cycle", "#b4591f", lambda h: base(h) + min(solar(h), load(h) - base(h)) + max(0, min(0.20, load(h) - base(h) - solar(h)))),
              ("Peaking: simple cycle, engines, batteries", "#e8a874", load)]
    X = lambda h: X0 + h / 24 * W
    Y = lambda v: Y0 + H - v * H
    svg, prev = "", lambda h: 0
    for lab, col, top in layers:
        pts = [f"{X(h):.1f},{Y(top(h)):.1f}" for h in hrs] + [f"{X(h):.1f},{Y(prev(h)):.1f}" for h in reversed(hrs)]
        svg += f'<polygon points="{" ".join(pts)}" fill="{col}" stroke="#0e1012" stroke-width="2"/>'
        prev = top
    ax = "".join(f'<text x="{X(h):.0f}" y="{Y0 + H + 24}" fill="#80868c" font-size="13" text-anchor="middle" font-family="Barlow">{t}</text>'
                 for h, t in [(0, "midnight"), (6, "6 am"), (12, "noon"), (18, "6 pm"), (24, "midnight")])
    key = "".join(f'<div style="margin-top:14px;display:flex;gap:10px;align-items:flex-start"><span style="flex:none;width:16px;height:16px;background:{col};margin-top:2px"></span>'
                  f'<span class="cd" style="font-size:15px;color:#f4f1ec">{lab}</span></div>' for lab, col, _ in reversed(layers))
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; how plants run", "A day on the grid:", "who runs when",
                           "Demand rises in the morning and peaks in the evening. Each kind of plant takes a layer.")
                + f'<svg class="abs" style="left:0;top:0" width="1440" height="810">{svg}{ax}</svg>'
                + f'<div class="abs" style="left:1070px;top:236px;width:310px">{key}'
                f'<div class="cd" style="font-size:14px;margin-top:22px">The evening peak arrives as the sun sets: that is when gas and batteries earn their keep.</div></div>'
                + f'<div class="abs" style="left:64px;top:600px;{SRC}">Illustrative summer weekday, not a real grid&rsquo;s data.</div>'
                + band("<b style='color:#f4f1ec'>Every start and stop cycles the plant</b>, and its cable: heat, vibration and terminations that move. Peakers may start every day.", 640))


def c_meter(n, N):
    lanes = [("Front of the meter", "The utility-scale plant", ["Sells power into the grid through a switchyard and the POI",
              "Utilities and IPPs; the ISO dispatches it", "HV gen-tie, switchyard, GSUs: the big cables", "Most of SW-3X1's power block"], COPPER),
             ("Behind the meter", "Power at the customer's site", ["Feeds a load directly: data centre, factory, campus",
              "Often modular engines, turbines, fuel cells and batteries", "MV collection and LV distribution on site; little or no grid tie",
              "SW-3X1's data-centre campus and modular yard"], "#8e98a3")]
    html = ""
    for k, (h, sub, items, col) in enumerate(lanes):
        x = 64 + k * 664
        html += (f'<div class="abs" style="left:{x}px;top:200px;width:648px;height:400px;background:#181b1f;border-top:4px solid {col};padding:24px 28px;box-sizing:border-box">'
                 f'<div class="ct" style="font-size:32px">{h}</div><div class="cnum" style="margin-top:8px;color:{GREY}">{sub}</div>'
                 + "".join(LI(t, 17) for t in items) + "</div>")
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; where the power goes", "Front of the meter,", "behind the meter",
                           "The same machines, two business models. The meter is the line between the utility and the customer.") + html
                + band("<b style='color:#f4f1ec'>Behind-the-meter is the fastest-growing lane</b>: data centres that cannot wait years for a grid connection build their own power.", 620))


def c_cable101(n, N):
    runs, cables, total, groups = schedule_numbers()
    fam = [("HV", "69&ndash;345 kV", "XLPE: switchyard and gen-tie"), ("MV", "5&ndash;35 kV", "MV-105: big motors, transformers, feeders"),
           ("LV power", "600 V", "TC-ER, MC, ARMOR-X: motors, panels, lighting"), ("VFD", "600 V&ndash;2 kV", "drive-rated: fans and pumps on drives"),
           ("Control", "600 V", "TC-ER multi-conductor: breakers, valves, interlocks"), ("Instrumentation", "300 V", "PLTC / ITC shielded pairs, thermocouple extension"),
           ("Fibre", "&mdash;", "controls network, protection"), ("Grounding", "bare Cu", "the ground grid under everything")]
    html = ""
    for k, (h, v, t) in enumerate(fam):
        x, y = 64 + (k % 4) * 334, 196 + (k // 4) * 170
        html += (f'<div class="abs" style="left:{x}px;top:{y}px;width:310px;height:150px;background:#181b1f;border-top:4px solid {COPPER if k < 2 else "#5d636a"};padding:16px 18px;box-sizing:border-box">'
                 f'<div style="display:flex;justify-content:space-between;align-items:baseline"><div class="ct" style="font-size:26px">{h}</div>'
                 f'<div style="font:800 18px/1 BC;color:{COPPER}">{v}</div></div><div class="cd" style="font-size:15px;margin-top:10px">{t}</div></div>')
    g = sorted(groups.items(), key=lambda kv: -kv[1])
    share = " &middot; ".join(f"{k} {100 * v / total:.0f}%" for k, v in g)
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; cable 101", "The cable families", "in a power plant",
                           f"From the biggest to the smallest. In SW-3X1's schedule: {cables:,} cables, {total / 5280:,.0f} miles.") + html
                + band(f"<b style='color:#f4f1ec'>By length:</b> {share}. The big cables get the attention; the small ones make up most of the miles.", 548)
                + f'<div class="abs" style="left:64px;top:640px;{SRC}">Shares by footage from the SW-3X1 model cable schedule; voltage ratings typical.</div>')


def c_stress(n, N):
    rows = [("Heat", "beside turbines, HRSGs and steam lines", "high-temperature ratings, route away from hot surfaces"),
            ("Cycling", "daily starts: heat, vibration, moving terminations", "flexible strands, good terminations, support"),
            ("Electrical noise", "variable-frequency drives on fans and pumps", "VFD-rated, shielded cable"),
            ("Hazardous areas", "gas skids and fuel yards (Class I, Div 2)", "ARMOR-X MC-HL, no conduit"),
            ("Fire and smoke", "halls, control rooms, cable spreading rooms", "flame-retardant, low-smoke, circuit integrity"),
            ("Outdoors", "sun, oil, water, burial", "sunlight- and oil-resistant jackets, direct-burial ratings"),
            ("Schedule", "long pulls on the critical path", "SIMpull reels, cut-to-length, pre-terminated")]
    html = (f'<div class="abs cnum" style="left:64px;top:192px;width:240px;color:{GREY}">Stress</div>'
            f'<div class="abs cnum" style="left:320px;top:192px;color:{GREY}">Where</div><div class="abs cnum" style="left:820px;top:192px;color:{GREY}">The answer</div>')
    for k, (a, b, c) in enumerate(rows):
        y = 220 + k * 54
        html += (f'<div class="abs" style="left:64px;top:{y}px;width:1312px;height:1px;background:#2c3036"></div>'
                 f'<div class="abs" style="left:64px;top:{y + 14}px;font:800 22px/1 BC;color:{WHITE};text-transform:uppercase">{a}</div>'
                 f'<div class="abs cd" style="left:320px;top:{y + 14}px;width:480px;font-size:16px">{b}</div>'
                 f'<div class="abs" style="left:820px;top:{y + 14}px;width:556px;font:400 16px/1.3 B;color:{COPPER}">{c}</div>')
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; why the spec matters", "What a power plant", "does to a cable") + html
                + band("<b style='color:#f4f1ec'>The wrong cable fails early, and a cable failure can trip a unit.</b> That is why the spec is strict, and why it is written for each area of the plant.", 618))


def c_future(n, N):
    cards = [("Hydrogen", "renders/epic/E108_pro_clean.jpg", ["Gas turbines can burn a blend of hydrogen with natural gas; OEMs are working toward 100%",
              "Our model has an H2 receiving station, trailer bay and an electrolyzer building", "More gas-detection, hazardous-area and DC cable"]),
             ("Carbon capture", "renders/epic/E68_pro.png", ["Captures CO2 from the stack: absorber, stripper, compressors",
              "A second plant's worth of motors, drives and instruments beside the first", "In SW-3X1: the CCS zone, about 142 miles of cable"]),
             ("Batteries beside gas", "renders/epic/E65_pro.png", ["Batteries take the fast swings; gas runs for days",
              "PCS skids, MV collection, DC cable in trenches", "In SW-3X1: the battery yard, about 50 miles of cable"])]
    html = ""
    for k, (h, im, items) in enumerate(cards):
        x = 64 + k * 444
        html += (f'<div class="abs" style="left:{x}px;top:190px;width:420px;height:420px;background:#181b1f;border-top:4px solid {COPPER}">'
                 f'<img src="{pic(im)}" style="width:420px;height:150px;object-fit:cover;display:block"><div style="padding:16px 20px">'
                 f'<div class="ct" style="font-size:26px">{h}</div>' + "".join(LI(t, 15) for t in items) + '</div></div>')
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; what is next", "Gas plants are getting", "cleaner, and more cable-dense") + html
                + band("<b style='color:#f4f1ec'>Every add-on is more cable:</b> hydrogen, carbon capture and storage each bring their own motors, drives, sensors and controls.", 628))


def c_units(n, N):
    t = [("1 kW", "a microwave oven running", "kilowatt = 1,000 watts"), ("1 MW", "a large store or a small factory", "megawatt = 1,000 kW"),
         ("1 GW", "the average use of roughly 800,000 US homes", "gigawatt = 1,000 MW"), ("300&ndash;550 MW", "one large modern gas turbine", "the machines in our turbine hall")]
    html = "".join(f'<div class="abs" style="left:{64 + k * 334}px;top:200px;width:310px;height:230px;background:#181b1f;border-top:4px solid {COPPER};padding:20px 22px;box-sizing:border-box">'
                   f'<div style="font:800 52px/1 BC;color:{COPPER}">{a}</div><div class="cd" style="font-size:17px;color:{WHITE};margin-top:14px">{b}</div>'
                   f'<div class="cd" style="font-size:14px;margin-top:10px">{c}</div></div>' for k, (a, b, c) in enumerate(t))
    two = [("MW is power", "how hard something runs right now: the speedometer"), ("MWh is energy", "power &times; time: the odometer. 1 MW for 1 hour = 1 MWh"),
           ("Capacity factor", "how much a plant actually makes vs. running flat out all year")]
    html += "".join(f'<div class="abs" style="left:{64 + k * 444}px;top:462px;width:420px;border-top:3px solid #5d636a;padding-top:12px">'
                    f'<div class="ct" style="font-size:24px">{a}</div><div class="cd" style="font-size:15px;margin-top:6px">{b}</div></div>' for k, (a, b) in enumerate(two))
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; units", "Units that stick:", "kW, MW, GW")
                + html + band("<b style='color:#f4f1ec'>A 1 GW data-centre campus uses as much power as a city.</b> That is why data centres are pulling new gas plants forward.", 600)
                + f'<div class="abs" style="left:64px;top:690px;{SRC}">Homes: EIA average US residential use, about 10,800 kWh a year (about 1.2 kW on average). Turbine size: typical large-frame H/J-class range.</div>')


GLOSS = [("BESS", "battery energy storage system"), ("BOP", "balance of plant: everything that is not the main machines"),
         ("BTM", "behind the meter: power at the customer's site"), ("COD", "commercial operation date: when the plant goes live"),
         ("EPC", "engineering, procurement and construction contractor: builds the plant, buys the cable"),
         ("FID", "final investment decision: the money is committed"), ("GSU", "generator step-up transformer"),
         ("HRSG", "heat recovery steam generator: the boiler behind each gas turbine"), ("IPP", "independent power producer"),
         ("ISO / RTO", "the grid operator that runs a power market (ERCOT, PJM, MISO)"), ("MCC", "motor control centre"),
         ("POI", "point of interconnection: where the plant meets the grid"), ("PPA", "power purchase agreement"),
         ("RICE", "reciprocating internal combustion engine: a big gas engine"), ("SCR", "selective catalytic reduction: cuts NOx in the HRSG"),
         ("VFD", "variable-frequency drive: controls motor speed")]


def c_glossary(n, N):
    html = ""
    for k, (a, b) in enumerate(GLOSS):
        x, y = 64 + (k // 8) * 664, 186 + (k % 8) * 60
        html += (f'<div class="abs" style="left:{x}px;top:{y}px;width:648px;height:1px;background:#2c3036"></div>'
                 f'<div class="abs" style="left:{x}px;top:{y + 14}px;width:130px;font:800 24px/1 BC;color:{COPPER}">{a}</div>'
                 f'<div class="abs cd" style="left:{x + 140}px;top:{y + 15}px;width:500px;font-size:16px;color:#f4f1ec">{b}</div>')
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; glossary", "The words", "you will hear today") + html
                + f'<div class="abs" style="left:64px;top:690px;{SRC}">A handout version can go out with the recording.</div>')


MODERN = [("Private 5G / LTE", "renders/nextgen/_src/T5G1_pro_clean.jpg", "A monopole with massive-MIMO antennas: the plant's own wireless network.",
           "fibre backhaul, tower power, grounding"),
          ("EV charging + solar carport", "renders/epic/E10_pro_clean.jpg", "Chargers at every bay, a DC fast charger, PV on the carport roof.",
           "LV feeders, PV wire, a pad-mount transformer"),
          ("Behind-the-meter data centre", "renders/epic/E47_pro_clean.jpg", "A ~150 MW campus fed straight from the plant and the modular yard.",
           "34.5 kV collection, cable bus, UPS feeders"),
          ("LNG by sea", "renders/coastal/C2_pro_clean.jpg", "A marine terminal: the carrier at the berth, unloading arms, the tank onshore.",
           "hazardous-area cable, long runs to the jetty, MV pumps"),
          ("Hydrogen", "renders/epic/E108_pro_clean.jpg", "Tube-trailer bay and receiving station; an electrolyzer building beside it.",
           "Class I Div 2 runs, gas detection, DC cable"),
          ("Carbon capture", "renders/epic/E68_pro.png", "Absorber, stripper and compressors on the stack exhaust.",
           "a second plant's motors, drives and instruments")]


def c_modern(n, N):
    html = ""
    for k, (h, im, what, cab) in enumerate(MODERN):
        x, y = 64 + (k % 3) * 444, 168 + (k // 3) * 226
        html += (f'<div class="abs" style="left:{x}px;top:{y}px;width:420px;height:212px;background:#181b1f;border-top:4px solid {COPPER};display:flex">'
                 f'<img src="{pic(im)}" style="width:170px;height:208px;object-fit:cover;display:block;flex:none">'
                 f'<div style="padding:14px 16px"><div class="ct" style="font-size:21px">{h}</div>'
                 f'<div class="cd" style="font-size:14px;color:#f4f1ec;margin-top:8px">{what}</div>'
                 f'<div class="cnum" style="margin-top:12px;font-size:11px;color:{GREY}">Cable</div>'
                 f'<div class="cd" style="font-size:14px;color:{COPPER};margin-top:4px">{cab}</div></div></div>')
    return page(n, N, head("Fundamentals &nbsp;&middot;&nbsp; the modern campus", "A modern gas plant is", "more than the power block") + html
                + band("<b style='color:#f4f1ec'>All six are in the SW-3X1 model.</b> Each one adds its own network of cable on top of the power block: "
                       "the campus is the customer, not just the turbines.", 630))


CC_STEPS = [("Air and gas in", "Filters pull in air; gas comes from the gas yard.", "instrumentation, fan and heater power"),
            ("Gas turbine", "Burns the gas in compressed air; the hot gas spins the turbine and its generator.", "MV-105, iso-phase bus, TC-ER to the skids"),
            ("HRSG", "The ~1,100 &deg;F exhaust boils water into steam: no extra fuel.", "thermocouples, MOVs, feed-pump MV"),
            ("Steam turbine", "Steam from all three HRSGs spins a fourth generator.", "MV-105, lube-oil and control cable"),
            ("Condenser", "80 fans cool the spent steam back into water; pumps send it back to the HRSGs.", "VFD cable to every fan"),
            ("Step-up to the grid", "Each generator's 21 kV goes up to 230 kV in its GSU, then out through the switchyard.", "HV XLPE, control and relay cable"),
            ("Stack", "What is left of the exhaust leaves, cleaned by the SCR.", "CEMS instrument cable")]
# marker positions on the slide (the CC1 render, 1360 px wide, shown left-aligned at 765 px high)
CC_PTS = [(425, 566), (462, 450), (470, 250), (800, 470), (955, 330), (452, 655), (470, 72)]


def c_combined(n, N):
    img = (f'<img class="abs" src="{pic("renders/training/CC1_pro_clean.jpg")}" style="left:0;top:0;width:1000px;height:765px;object-fit:cover;object-position:0 0">'
           f'<div class="abs" style="left:880px;top:0;width:130px;height:765px;background:linear-gradient(90deg,rgba(14,16,18,0),#0e1012)"></div>')
    P = CC_PTS
    def arrow(pts, col, dash=""):
        d = " ".join(f"{x},{y}" for x, y in pts)
        return (f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="5" stroke-linejoin="round" {dash} marker-end="url(#h{col[1:]})"/>')
    cols = {"#e8a874": "gas", "#e04b3c": "steam", "#3a8fd9": "water", "#b06ae0": "power"}
    defs = "".join(f'<marker id="h{c[1:]}" markerWidth="4" markerHeight="4" refX="2.2" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4 z" fill="{c}"/></marker>' for c in cols)
    svg = (f'<svg class="abs" style="left:0;top:0" width="1000" height="765"><defs>{defs}</defs>'
           + arrow([(P[0][0], P[0][1] - 22), (P[1][0] - 4, P[1][1] + 24)], "#e8a874")
           + arrow([(P[1][0] + 2, P[1][1] - 24), (P[2][0], P[2][1] + 26)], "#e8a874")
           + arrow([(P[2][0], P[2][1] - 26), (P[6][0], P[6][1] + 26)], "#e8a874")
           + arrow([(P[2][0] + 24, P[2][1]), (760, P[2][1]), (P[3][0], P[3][1] - 26)], "#e04b3c")
           + arrow([(P[3][0] + 24, P[3][1] - 10), (P[4][0] - 18, P[4][1] + 20)], "#e04b3c")
           + arrow([(P[4][0] - 8, P[4][1] - 26), (P[4][0] - 8, 190), (P[2][0] + 30, 190), (P[2][0] + 30, P[2][1] - 30)], "#3a8fd9", 'stroke-dasharray="12 8"')
           + arrow([(P[1][0] - 2, P[1][1] + 26), (P[5][0] + 2, P[5][1] - 26)], "#b06ae0")
           + arrow([(P[3][0], P[3][1] + 26), (P[3][0], P[5][1]), (P[5][0] + 28, P[5][1])], "#b06ae0")
           + '</svg>')
    marks = "".join(f'<div class="abs" style="left:{x - 22}px;top:{y - 22}px;width:44px;height:44px;border-radius:50%;background:{COPPER};'
                    f'border:3px solid #121417;box-sizing:border-box;font:800 21px/38px BC;color:#121417;text-align:center">{k + 1}</div>'
                    for k, (x, y) in enumerate(P))
    key = "".join(f'<span style="display:inline-block;width:22px;height:5px;background:{c};margin:0 6px 3px {0 if i == 0 else 14}px;vertical-align:middle"></span>{t}'
                  for i, (c, t) in enumerate(cols.items()))
    steps = "".join(f'<div style="display:flex;gap:12px;margin-top:11px">{circ(k + 1, 28, COPPER, "#121417", 14)}'
                    f'<div><div style="font:800 17px/1.05 BC;color:{WHITE};text-transform:uppercase">{h}</div>'
                    f'<div class="cd" style="font-size:13px;margin-top:3px">{t}</div>'
                    f'<div style="font:400 12px/1.3 B;color:{COPPER};margin-top:2px">{c}</div></div></div>' for k, (h, t, c) in enumerate(CC_STEPS))
    return page(n, N, img + svg + marks
                + f'<div class="abs" style="left:24px;top:722px;font:700 12px/1 BC;letter-spacing:.08em;color:#d6d9dc;text-transform:uppercase;'
                  f'background:rgba(14,16,18,.75);padding:7px 10px;border-radius:3px">{key}</div>'
                + f'<div class="abs" style="left:1010px;top:40px;width:400px">'
                  f'<div class="kicker">Fundamentals &nbsp;&middot;&nbsp; combined cycle</div>'
                  f'<div class="h2" style="font-size:40px;margin-top:8px">Burn the gas once, <em>use the heat twice</em></div>'
                  f'{steps}'
                  f'<div style="margin-top:14px;border-top:3px solid {COPPER};padding-top:8px;font:800 19px/1.15 BC;color:{WHITE};text-transform:uppercase">'
                  f'~2/3 of the power from the gas turbines, ~1/3 from the steam: <span style="color:{COPPER}">same fuel</span></div></div>')


# Combined cycle as a four-step build on the CC1 render: model coordinates are projected into the image, so the highlights
# sit on the real equipment and the flows follow the real routes.
CC_CAM = dict(eye=(965, -60, 1250), target=(965, 585, 0), lens=30)   # camera CC2
TRAINS = (630, 790, 950)


def cc_project(p, W=1440, H=810):
    import numpy as np
    eye, tgt = np.array(CC_CAM["eye"], float), np.array(CC_CAM["target"], float)
    f = (tgt - eye) / np.linalg.norm(tgt - eye)
    r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    d = np.array(p, float) - eye
    z = d @ f
    k = CC_CAM["lens"] / 36 * W
    return W / 2 + (d @ r) / z * k, H / 2 - (d @ u) / z * k


def cc_hull(x0, x1, y0, y1, z0, z1):
    pts = sorted(cc_project((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1))
    def half(ps):
        h = []
        for q in ps:
            while len(h) > 1 and (h[-1][0] - h[-2][0]) * (q[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (q[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(q)
        return h
    lo, hi = half(pts), half(pts[::-1])
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in lo[:-1] + hi[:-1])


CC_BOXES = {"gt": [(x - 13, x + 13, 455, 540, 20, 38) for x in TRAINS], "gsu": [(x - 20, x + 20, 325, 365, 0, 45) for x in TRAINS],
            "hrsg": [(x - 35, x + 35, 600, 760, 0, 100) for x in TRAINS], "stk": [(x - 11, x + 11, 779, 801, 0, 180) for x in TRAINS],
            "st": [(1020, 1080, 460, 552, 20, 46)], "gsust": [(1030, 1072, 320, 370, 0, 45)], "acc": [(1130, 1450, 380, 780, 0, 125)]}
CC_FLOWS = {"air": [[(x - 7, 385, 60), (x - 7, 452, 34)] for x in TRAINS],
            "gtpow": [[(x + 7, 452, 30), (x + 7, 368, 30)] for x in TRAINS],
            "exhaust": [[(x, 545, 30), (x, 600, 45), (x, 760, 60), (x, 790, 80)] for x in TRAINS],
            "stack": [[(x, 790, 110), (x, 790, 190)] for x in TRAINS],
            "steam": [[(x, 680, 100), (x, 575, 72)] for x in TRAINS] + [[(TRAINS[0], 575, 72), (1050, 575, 72), (1050, 555, 48)]],
            "toacc": [[(1082, 506, 40), (1160, 506, 60)]],
            "water": [[(1150, 640, 8), (1000, 640, 8), (985, 700, 30)]],
            "stpow": [[(1051, 458, 30), (1051, 372, 30)]]}
CC_COL = {"air": "#7fe0d0", "gtpow": "#c58cff", "stpow": "#c58cff", "exhaust": "#ff8a3d", "stack": "#9aa3ab", "steam": "#ff5a4a",
          "toacc": "#ff5a4a", "water": "#4aa8ff"}
CC_STAGE = [("gt", "gsu"), ("hrsg", "stk"), ("st", "gsust", "acc")]
CC_STAGE_FLOWS = [("air", "gtpow"), ("exhaust", "stack"), ("steam", "toacc", "water", "stpow")]
CC_TEXT = [("1", "The gas turbine", "a jet engine on the ground",
            "It burns gas in compressed air; the hot gas spins the turbine and its generator. That makes <b>about two-thirds</b> of the plant's power, "
            "and leaves exhaust at about 1,100 &deg;F."),
           ("2", "The HRSG", "catch the heat",
            "Instead of going up the stack, the hot exhaust runs through a heat-recovery steam generator and boils water into steam. <b>No extra fuel.</b>"),
           ("3", "The steam turbine", "power from the leftovers",
            "Steam from all three HRSGs spins one more turbine and generator: <b>about one-third more power.</b> The air-cooled condenser turns it back "
            "into water, and round it goes.")]


def c_cc(step, n, N):
    """step 0, 1, 2: one stage lit; step 3: the whole cycle."""
    img = pic("renders/training/CC2_pro_clean.jpg")
    lit = range(3) if step == 3 else [step]
    boxes = [b for i in lit for key in CC_STAGE[i] for b in CC_BOXES[key]]
    flows = [(key, pts) for i in lit for key in CC_STAGE_FLOWS[i] for pts in CC_FLOWS[key]]
    clip = "".join(f'<polygon points="{cc_hull(*b)}"/>' for b in boxes)
    outl = "".join(f'<polygon points="{cc_hull(*b)}" fill="none" stroke="{COPPER}" stroke-width="2.5" opacity=".95"/>' for b in boxes)
    def path(pts):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in (cc_project(p) for p in pts))
    fl = ""
    for key, pts in flows:
        c = CC_COL[key]
        dash = 'stroke-dasharray="14 10"' if key == "water" else ""
        fl += (f'<polyline points="{path(pts)}" fill="none" stroke="{c}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" opacity=".35" filter="url(#glow)"/>'
               f'<polyline points="{path(pts)}" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" {dash} marker-end="url(#a{key})"/>')
    marks = "".join(f'<marker id="a{k}" markerWidth="4" markerHeight="4" refX="2" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4 z" fill="{c}"/></marker>'
                    for k, c in CC_COL.items())
    svg = (f'<svg class="abs" style="left:0;top:0" width="1440" height="810"><defs><clipPath id="lit">{clip}</clipPath>'
           f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>{marks}</defs>'
           f'<image href="{img}" x="0" y="0" width="1440" height="810" clip-path="url(#lit)" style="filter:brightness(1.12) saturate(1.1)"/>'
           f'{outl}{fl}</svg>')
    base = (f'<img class="abs" src="{img}" style="left:0;top:0;width:1440px;height:810px;filter:brightness(.38) saturate(.35)">'
            f'<div class="abs" style="left:0;top:0;width:1440px;height:810px;background:linear-gradient(180deg,rgba(14,16,18,.85) 0%,rgba(14,16,18,0) 22%,'
            f'rgba(14,16,18,0) 70%,rgba(14,16,18,.92) 100%)"></div>')
    prog = ""
    labels = ["Gas turbine", "Heat recovery", "Steam turbine", "Combined cycle"]
    for k, t in enumerate(labels):
        on = k == step or (step == 3)
        prog += (f'<div style="display:flex;align-items:center;gap:10px;opacity:{1 if on else .4}">'
                 f'{circ("=" if k == 3 else k + 1, 30, COPPER if on else "#3a3f45", "#121417" if on else WHITE, 15)}'
                 f'<span style="font:700 15px/1 BC;letter-spacing:.1em;color:{WHITE};text-transform:uppercase">{t}</span></div>')
        if k < 3:
            prog += f'<div style="width:40px;height:2px;background:{"#b4591f" if step == 3 or k < step else "#3a3f45"}"></div>'
    if step < 3:
        num, h, em, body = CC_TEXT[step]
        text = (f'<div class="abs kicker" style="left:56px;top:40px">Combined cycle &nbsp;&middot;&nbsp; step {num} of 3</div>'
                f'<div class="abs h2" style="left:54px;top:66px;font-size:54px">{h}: <em>{em}</em></div>'
                f'<div class="abs" style="left:56px;top:664px;width:900px;font:400 19px/1.45 B;color:#e6e3dd">{body.replace("<b>", "<b style=color:#fff>")}</div>')
    else:
        text = (f'<div class="abs kicker" style="left:56px;top:40px">Combined cycle</div>'
                f'<div class="abs h2" style="left:54px;top:66px;font-size:54px">Burn the gas once, <em>use the heat twice</em></div>'
                f'<div class="abs" style="left:56px;top:650px;display:flex;gap:46px;align-items:flex-end">'
                f'<div><div style="font:800 56px/1 BC;color:{COPPER}">~60%</div><div class="cd" style="font-size:15px;margin-top:4px">of the fuel becomes power, vs ~40% for a gas turbine alone</div></div>'
                f'<div><div style="font:800 56px/1 BC;color:{WHITE}">3 + 1</div><div class="cd" style="font-size:15px;margin-top:4px">three gas turbines, three HRSGs, one steam turbine: a "3x1"</div></div>'
                f'<div><div style="font:800 56px/1 BC;color:{WHITE}">9,266</div><div class="cd" style="font-size:15px;margin-top:4px">cables in this power block, in our model</div></div></div>')
    keys = {"0": [("air", "air"), ("gtpow", "power")], "1": [("exhaust", "hot exhaust"), ("stack", "to the stack")],
            "2": [("steam", "steam"), ("water", "water"), ("stpow", "power")],
            "3": [("exhaust", "exhaust"), ("steam", "steam"), ("water", "water"), ("gtpow", "power")]}[str(step)]
    key = "".join(f'<span style="display:inline-block;width:22px;height:5px;background:{CC_COL[k]};margin:0 7px 3px 16px;vertical-align:middle"></span>{t}' for k, t in keys)
    return page(n, N, base + svg + text
                + f'<div class="abs" style="left:56px;top:136px;display:flex;align-items:center;gap:10px">{prog}</div>'
                + f'<div class="abs" style="right:56px;top:46px;font:700 12px/1 BC;letter-spacing:.1em;color:#cfd3d6;text-transform:uppercase">{key}</div>')


def c_cc1(n, N): return c_cc(0, n, N)
def c_cc2(n, N): return c_cc(1, n, N)
def c_cc3(n, N): return c_cc(2, n, N)
def c_cc4(n, N): return c_cc(3, n, N)


XR_GROUPS = [("MV / HV power", "#f05a28", ("HV 230 kV", "MV 35 kV", "MV 25 kV", "MV 15 kV", "MV 5 kV", "Portable MV"),
              "The big feeders: generators, transformers, the largest motors. MV-105, HV XLPE."),
             ("LV power", "#f2c613", ("LV 600 V", "DC 2 kV", "Portable LV"),
              "600 V to motors, valves, drives, lighting. TC-ER, ARMOR-X MC-HL, VFD cable."),
             ("Control", "#3a8fd9", ("Control",), "Starts, stops and trips: breakers, interlocks, MCC starters. Multi-conductor TC-ER."),
             ("Instrumentation", "#3ac46a", ("Instrumentation",), "The plant's nerves: pressure, flow, temperature. Shielded pairs, thermocouple extension."),
             ("Fibre and fire alarm", "#c58cff", ("Fibre / data", "Fire alarm"), "The control network, protection and life safety.")]


def c_xray(n, N):
    import json, math
    d = json.load(open(os.path.join(PLANT, "brochure", "cables_xray.json")))
    cls = d["classes"]
    gi = {c: k for k, g in enumerate(XR_GROUPS) for c in g[2]}
    tot = [[0, 0] for _ in XR_GROUPS]
    per = {}
    for r in d["cables"]:
        g = gi.get(cls[r[1]])
        if g is None:
            continue
        tot[g][0] += r[5]
        tot[g][1] += r[5] * r[6]
        if r[12] >= 0:
            a = per.setdefault(r[12], [0] * len(XR_GROUPS))
            a[g] += r[5]
    img = pic("renders/training/CC2_pro_clean.jpg")
    lines = {k: "" for k in range(len(XR_GROUPS))}
    for pi, cnts in per.items():
        g = max(range(len(cnts)), key=lambda k: cnts[k])          # the type with the most cables on the route
        cnt = sum(cnts)
        q = d["paths"][pi]
        pts = [(q[i], q[i + 1], max(q[i + 2], 0)) for i in range(0, len(q), 3)]
        if not any(470 < x < 1470 and 290 < y < 840 for x, y, z in pts):
            continue
        xy = [cc_project(p) for p in pts]
        if not any(-50 < x < 1490 and -50 < y < 860 for x, y in xy):
            continue
        w = min(1.0 + 0.9 * math.log(1 + cnt), 6.5)
        lines[g] += f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in xy)}" stroke-width="{w:.1f}"/>'
    svg = (f'<svg class="abs" style="left:0;top:0" width="1440" height="810"><defs>'
           f'<filter id="xg" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
           f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
           f'<clipPath id="xc"><rect x="0" y="168" width="1030" height="500"/></clipPath></defs><g clip-path="url(#xc)">'
           + "".join(f'<g fill="none" stroke="{XR_GROUPS[k][1]}" stroke-linecap="round" stroke-linejoin="round" opacity=".9" filter="url(#xg)">{lines[k]}</g>'
                     for k in (1, 2, 0, 4, 3)) + '</g></svg>')
    base = (f'<img class="abs" src="{img}" style="left:0;top:0;width:1440px;height:810px;filter:brightness(.26) saturate(.2)">'
            f'<div class="abs" style="left:0;top:0;width:1440px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,0) 60%,rgba(14,16,18,.96) 75%),'
            f'linear-gradient(180deg,rgba(14,16,18,.85) 0%,rgba(14,16,18,0) 20%,rgba(14,16,18,0) 82%,rgba(14,16,18,.9) 100%)"></div>')
    rows = ""
    for k, (h, col, _, t) in enumerate(XR_GROUPS):
        c, ft = tot[k]
        rows += (f'<div style="margin-top:16px;border-left:4px solid {col};padding-left:12px">'
                 f'<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font:800 19px/1 BC;color:{WHITE};text-transform:uppercase">{h}</span>'
                 f'<span style="font:800 17px/1 BC;color:{col}">{c:,} &middot; {ft / 5280:,.0f} mi</span></div>'
                 f'<div class="cd" style="font-size:13px;margin-top:5px">{t}</div></div>')
    allc = sum(c for c, _ in tot)
    return page(n, N, base + svg
                + f'<div class="abs kicker" style="left:56px;top:40px">Wire and cable &nbsp;&middot;&nbsp; X-ray</div>'
                + f'<div class="abs h2" style="left:54px;top:66px;font-size:52px">Take the plant away: <em>the cable stays</em></div>'
                + f'<div class="abs" style="left:56px;top:690px;width:820px;font:400 18px/1.45 B;color:#e6e3dd">Every line is a route from the model\'s cable schedule, '
                  f'in trays, conduit and duct banks; thicker lines carry more cables. <b style="color:#fff">The power block is a web of copper.</b></div>'
                + f'<div class="abs" style="left:1060px;top:70px;width:330px"><div class="cnum" style="color:{WHITE}">The cable types &middot; whole plant</div>'
                  f'<div style="font:800 40px/1 BC;color:{COPPER};margin-top:10px">{allc:,} <span style="font-size:18px;color:{GREY}">cables</span></div>{rows}'
                  f'<div class="cd" style="font-size:12px;margin-top:14px">Counts and miles from the SW-3X1 model cable schedule (trays, conduit, duct banks; '
                  f'building wire, grounding and overhead not shown).</div></div>')


def main():
    import pymupdf
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    fns = [c_generator, c_grid, c_day, c_meter, c_cable101, c_stress, c_future, c_units, c_glossary, c_modern, c_combined, c_cc1, c_cc2, c_cc3, c_cc4, c_xray]
    N = len(fns)
    head_ = f"<!doctype html><html><head><meta charset='utf-8'><style>{db.CSS}</style></head><body>"
    out = pymupdf.open()
    for i, f in enumerate(fns):
        sec = f(i + 1, N).replace('<section class="page slide">', '<section class="page slide"><div class="s">', 1).replace("</section>", "</div></section>")
        hp = os.path.join(OUT, f"_c{i}.html")
        open(hp, "w").write(head_ + sec + "</body></html>")
        pdf = hp.replace(".html", ".pdf")
        subprocess.run([bz.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", bz.url(hp)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.insert_pdf(pymupdf.open(pdf))
        os.remove(pdf)
        os.remove(hp)
    out.save(os.path.join(OUT, "SW-3X1_Nov11_candidates.pdf"), garbage=3, deflate=True)
    ims = []
    for i, pg in enumerate(out):
        p = os.path.join(OUT, f"candidate_{chr(65 + i)}.jpg")
        pix = pg.get_pixmap(dpi=96)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.save(p, quality=90)
        ims.append(im)
    w, h = 960, 540
    rows = (len(ims) + 1) // 2
    sheet = Image.new("RGB", (w * 2 + 30, h * rows + 15 * (rows + 1)), (40, 40, 40))
    for k, im in enumerate(ims):
        x, y = 10 + (k % 2) * (w + 10), 15 + (k // 2) * (h + 15)
        sheet.paste(im.resize((w, h)), (x, y))
    sheet.save(os.path.join(OUT, "candidates_sheet.jpg"), quality=88)
    print("wrote", len(ims), "candidates to", OUT)


if __name__ == "__main__":
    main()
