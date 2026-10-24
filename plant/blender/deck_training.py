"""Nov 11 internal training "Inside Power Generation" (presentation/Nov11_run_of_show.md): 17 slides at 1440 x 810,
same look as the boiler deck. Reuses the boiler-deck slides for the fundamentals and the cable takeaways (their footers
re-numbered), the 16-zone overview, and the model renders for the seven tour stops; new: title, agenda, why gas now
(market figures left as marked placeholders for Southwire market intelligence), one slide per tour stop, the whole
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


def pic(rel):
    full = os.path.join(PLANT, "renders", "boilers_full", os.path.basename(rel))
    path = full if os.path.exists(full) else os.path.join(PLANT, rel)
    if not os.path.exists(path):
        raise FileNotFoundError(rel)
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
  <img class="abs" src="{pic('renders/nextgen/_src/E123_pro_clean.jpg')}" style="left:0;top:0;width:1440px;height:810px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:1440px;height:810px;background:linear-gradient(90deg,rgba(14,16,18,.94) 0%,
       rgba(14,16,18,.78) 38%,rgba(14,16,18,0) 70%)"></div>
  <div class="abs kicker" style="left:72px;top:150px;font-size:14px">Southwire internal training &nbsp;&middot;&nbsp; November 11, 2026</div>
  <div class="abs h2" style="left:70px;top:186px;font-size:92px;width:760px">Inside power <em>generation</em></div>
  <div class="abs lede" style="left:72px;top:396px;width:560px;font-size:21px">A guided tour of a gas power campus: how it works,
    the equipment and electrical systems, and where wire and cable go.</div>
  <div class="abs" style="left:72px;top:540px;font:700 15px/1.5 BC;letter-spacing:.14em;color:{WHITE};text-transform:uppercase">
    1:30 &ndash; 2:30 PM &nbsp;&middot;&nbsp; Zoom<br><span style="color:{GREY}">Hosted by Stephan Hardt</span></div>
</section>"""


AGENDA = [("1:30", "Welcome", "why this matters", "3"),
          ("1:33", "Fundamentals and market", "why gas, how a combined cycle works, the campus", "10"),
          ("1:43", "The 3D tour", "seven stops: what it does, its electrical system, its cable", "30"),
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


def s_overview(n, N):
    return f"""
<section class="page slide">
  <img class="abs" src="{pic('renders/deck/slide19_zones.png')}" style="left:0;top:0;width:1440px;height:765px;object-fit:contain;background:#0e1012">
  {foot(n, N)}
</section>"""


STOPS = [
    ("Grid connection and switchyard", "renders/epic/E19_pro_clean.jpg",
     "Sends the plant's power to the 230 kV grid.",
     ["Generator step-up transformers: 21 kV up to 230 kV", "Breakers, disconnects, and a control house with protection relays"],
     ["HV conductor and 230 kV cable", "Control and relay cable from every breaker to the control house", "Fibre; the buried bare-copper ground grid"],
     "Every breaker out here has a bundle of control cable running back to the control house."),
    ("Turbine hall", "renders/epic/E21_pro_clean.jpg",
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
    ("Modular generation", "renders/modular/MP1_pro_clean.jpg",
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
    N = 17
    plan = [lambda: s_title(), lambda: s_agenda(2, N), lambda: s_why(3, N),
            lambda: reused(db.slide_cycle, 4, N, "Fundamentals"), lambda: reused(db.slide_basics, 5, N, "Fundamentals"),
            lambda: s_overview(6, N)]
    plan += [(lambda k=k: s_stop(k, 7 + k, N)) for k in range(7)]
    plan += [lambda: s_number(14, N), lambda: reused(db.slide_spec, 15, N, "Wire and cable takeaways"),
             lambda: reused(db.slide_value, 16, N, "Wire and cable takeaways"), lambda: s_close(17, N)]
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
    for i, pg in enumerate(out):
        pg.get_pixmap(dpi=96).save(os.path.join(OUT, f"training_{i + 1:02d}.png"))
    print("wrote", p, len(out), "slides")


if __name__ == "__main__":
    main()
