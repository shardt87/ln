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


def page(n, N, body):
    return f'<section class="page slide">{body}{foot(n, N, "CANDIDATE SLIDE &middot; INSIDE POWER GENERATION &middot; INTERNAL TRAINING")}</section>'


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


def main():
    import pymupdf
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    fns = [c_generator, c_grid, c_day, c_meter, c_cable101, c_stress, c_future, c_units, c_glossary, c_modern]
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
