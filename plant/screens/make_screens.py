"""SCADA / DCS operator screens for the main control room (control_room.py), drawn with PIL.

High-performance HMI style (ISA-101): neutral grey background, grey equipment, dark values, colour kept for
alarms and state (US utility convention: red = closed / running, green = open / stopped). The numbers are a
plausible full-load operating point of the SW-3X1 3x1 plant, illustrative only.

Screens (1600 x 900 base, drawn at scale S): overview, sld, gt1, hrsg1, trend, alarm, acc, grid, cctv. The video
wall shows four of them across 2 x 2 cubes; those are also written as quarter crops (<name>_q<r><c>.png).

Run with an interpreter that has PIL (the Blender venv): bvenv/bin/python plant/screens/make_screens.py
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
FD = os.path.join(PLANT, "blender", "deck")
FONTS = {
    "r": os.path.join(FD, "Barlow-Regular.ttf"),
    "b": os.path.join(FD, "BarlowCondensed-ExtraBold.ttf"),
    "m": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "mb": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}
BG, PANEL, LINE, EQ, EQD = "#c9cccd", "#bfc3c4", "#5d6569", "#a9aeb1", "#7d858a"
TXT, VAL, HEAD = "#2a2f33", "#14325a", "#2c3338"
RED, GRN, YEL, ORG, CYN, BLU = "#c0262d", "#1f8a3c", "#e6c229", "#e07a1f", "#2b9fc4", "#3a6ea5"
CLOCK = "14:32:07"
DATE = "11-OCT-2026"


class C:
    """Canvas in 1600 x 900 base units, drawn at scale S."""

    def __init__(self, title, S=1, nav=None):
        self.S = S
        self.im = Image.new("RGB", (1600 * S, 900 * S), BG)
        self.g = ImageDraw.Draw(self.im)
        self._f = {}
        self.header(title, nav)

    def f(self, k, size):
        key = (k, size)
        if key not in self._f:
            self._f[key] = ImageFont.truetype(FONTS[k], max(6, int(size * self.S)))
        return self._f[key]

    def P(self, *xy):
        return [v * self.S for v in xy]

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=1):
        self.g.rectangle(self.P(x0, y0, x1, y1), fill=fill, outline=outline, width=max(1, int(w * self.S)))

    def line(self, pts, fill=LINE, w=2):
        self.g.line([v * self.S for p in pts for v in p], fill=fill, width=max(1, int(w * self.S)), joint="curve")

    def poly(self, pts, fill=None, outline=LINE, w=1.5):
        self.g.polygon([v * self.S for p in pts for v in p], fill=fill, outline=outline, width=max(1, int(w * self.S)))

    def ell(self, x0, y0, x1, y1, fill=None, outline=LINE, w=1.5):
        self.g.ellipse(self.P(x0, y0, x1, y1), fill=fill, outline=outline, width=max(1, int(w * self.S)))

    def text(self, x, y, t, size=14, k="r", fill=TXT, anchor="la"):
        self.g.text(self.P(x, y), t, font=self.f(k, size), fill=fill, anchor=anchor)

    def value(self, x, y, v, unit, size=15, w=None, fill=VAL, alarm=None):
        """A value box (dark value, small unit); alarm colours the border."""
        f = self.f("mb", size)
        tw = self.g.textlength(v, font=f) / self.S
        w = w or tw + 12
        if alarm:
            self.rect(x - 3, y - 3, x + w + 3, y + size + 9, outline=alarm, w=3)
        self.rect(x, y, x + w, y + size + 6, fill="#d9dcdd", outline="#9aa0a3")
        self.text(x + w - 5, y + 3, v, size, "mb", fill, "ra")
        self.text(x + w + 5, y + 4, unit, size * .8, "r", TXT)

    def bar(self, x, y, w, h, frac, lo=.2, hi=.85, label="", val=""):
        """Analog indicator: grey track, darker normal band, black pointer."""
        self.rect(x, y, x + w, y + h, fill="#d8dadb", outline="#8b9296")
        self.rect(x + w * lo, y + 2, x + w * hi, y + h - 2, fill="#b3b8bb")
        px = x + w * frac
        self.poly([(px, y - 3), (px - 5, y - 10), (px + 5, y - 10)], fill="#1d2226", outline="#1d2226")
        self.rect(px - 1.2, y, px + 1.2, y + h, fill="#1d2226")
        if label:
            self.text(x, y + h + 4, label, 12)
        if val:
            self.text(x + w, y + h + 4, val, 12, "mb", VAL, "ra")

    def header(self, title, nav):
        self.rect(0, 0, 1600, 44, fill="#3b4247")
        self.text(16, 8, "SW-3X1 CCPP", 22, "b", "#e8ecee")
        self.text(160, 12, title, 18, "r", "#e8ecee")
        x = 620
        for n in (nav or ["OVERVIEW", "ELECTRICAL", "GT1", "GT2", "GT3", "HRSG", "ST", "ACC", "BOP", "TRENDS", "ALARMS"]):
            w = len(n) * 9 + 18
            self.rect(x, 9, x + w, 35, fill="#576066" if n.lower()[:3] != title.lower()[:3] else "#8a949a",
                      outline="#6d777d")
            self.text(x + w / 2, 22, n, 12, "r", "#eef1f2", "mm")
            x += w + 5
        self.text(1590, 8, CLOCK, 18, "mb", "#e8ecee", "ra")
        self.text(1590, 28, DATE, 10, "m", "#c0c7cb", "ra")

    def footer(self, alarms=None):
        self.rect(0, 862, 1600, 900, fill="#30363a")
        alarms = alarms or [("3", "14:29:51", "ACC-C07 FAN 3 VIBRATION HIGH", YEL),
                            ("4", "14:18:22", "WT-DEMIN CONDUCTIVITY TREND HIGH", CYN)]
        for k, (p, t, s, c) in enumerate(alarms[:2]):
            y = 866 + k * 16
            self.rect(10, y + 1, 26, y + 14, fill=c)
            self.text(18, y + 1, p, 11, "mb", "#111111", "ma")
            self.text(34, y, f"{t}   {s}", 12, "m", "#e6e9ea")
        self.text(1590, 872, "ALM 3  UNACK 1  SUPPR 12", 13, "mb", "#e6e9ea", "ra")

    def save(self, name):
        self.footer()
        p = os.path.join(HERE, name + EXT.get(name, ".png"))
        self.im.save(p, quality=86) if p.endswith(".jpg") else self.im.save(p, optimize=True)
        return p


def gt_shape(c, x, y, s=1.0, fill=EQ):
    """Gas turbine profile: inlet, compressor cone, combustor, turbine, exhaust diffuser."""
    pts = [(0, -38), (30, -38), (150, -22), (175, -28), (200, -28), (255, -45), (290, -52), (290, 52), (255, 45),
           (200, 28), (175, 28), (150, 22), (30, 38), (0, 38)]
    c.poly([(x + px * s, y + py * s) for px, py in pts], fill=fill, outline=LINE, w=2)
    for k in range(9):                                                            # compressor stages
        xx = x + (34 + k * 12) * s
        hh = (36 - k * 1.6) * s
        c.line([(xx, y - hh), (xx, y + hh)], "#8d9498", 1)
    c.rect(x + 152 * s, y - 34 * s, x + 176 * s, y - 26 * s, fill="#9ba1a4", outline=LINE)
    c.rect(x + 152 * s, y + 26 * s, x + 176 * s, y + 34 * s, fill="#9ba1a4", outline=LINE)
    for k in range(4):
        xx = x + (205 + k * 13) * s
        c.line([(xx, y - (30 + k * 4) * s), (xx, y + (30 + k * 4) * s)], "#8d9498", 1)


def gen(c, x, y, r, name, run=True):
    c.ell(x - r, y - r, x + r, y + r, fill=EQ, outline=LINE, w=2)
    c.text(x, y, name, 14, "b", TXT, "mm")
    c.rect(x + r + 4, y - 6, x + r + 16, y + 6, fill=RED if run else GRN, outline="#333")


def pipe(c, pts, col="#6c757a", w=4):
    c.line(pts, col, w)


# ------------------------------------------------------------------------------------------- screens
def overview(S=2):
    c = C("PLANT OVERVIEW", S)
    MW = [372.4, 371.8, 372.9]
    for k in range(3):
        y = 150 + k * 205
        c.text(26, y - 70, f"GT{k + 1}", 22, "b", HEAD)
        gt_shape(c, 30, y, .8)
        gen(c, 30 - 0, y, 0, "") if False else None
        c.line([(22, y), (0, y)], LINE, 4)
        gen(c, 288, y, 30, f"G{k + 1}")
        c.value(330, y - 52, f"{MW[k]:.1f}", "MW", 16, 72)
        c.value(330, y - 24, "3600", "rpm", 14, 72)
        c.value(330, y + 4, f"{627 + k:.0f}", "°C EXH", 14, 72)
        c.value(330, y + 32, "2.1", "ppm NOx", 14, 72)
        # HRSG
        pipe(c, [(262, y + 40), (262, y + 62), (480, y + 62)], "#6c757a", 6)
        hx = 480
        c.poly([(hx, y + 30), (hx + 40, y - 60), (hx + 170, y - 60), (hx + 170, y + 80), (hx + 40, y + 80), (hx, y + 92)],
               fill=EQ, outline=LINE, w=2)
        for j, (lab, col) in enumerate((("HP", "#8f979b"), ("IP", "#9aa1a4"), ("LP", "#a4abae"))):
            c.rect(hx + 55 + j * 38, y - 52, hx + 85 + j * 38, y + 72, fill=col, outline="#80888c")
            c.text(hx + 70 + j * 38, y + 6, lab, 12, "b", HEAD, "mm")
        c.text(hx + 85, y - 80, f"HRSG {k + 1}", 16, "b", HEAD, "mm")
        c.rect(hx + 150, y - 140, hx + 168, y - 60, fill="#b0b5b8", outline=LINE)          # stack
        c.value(hx + 186, y - 50, f"{168.4 - k * .3:.1f}", "bar HP", 14, 64)
        c.value(hx + 186, y - 22, f"{585 - k:.0f}", "°C HP", 14, 64)
        c.value(hx + 186, y + 6, f"{38.2 + k * .1:.1f}", "bar RH", 14, 64)
        c.value(hx + 186, y + 34, f"{91.3 - k * .4:.1f}", "% DRUM", 14, 64)
        pipe(c, [(hx + 120, y - 60), (hx + 120, y - 92 + k * 4), (1010, y - 92 + k * 4)], "#4f585d", 5)
    # steam header and ST
    pipe(c, [(1010, 58), (1010, 540), ], "#4f585d", 7)
    pipe(c, [(1010, 330), (1080, 330)], "#4f585d", 7)
    sx, sy = 1080, 330
    c.poly([(sx, sy - 30), (sx + 90, sy - 50), (sx + 90, sy + 50), (sx, sy + 30)], fill=EQ, outline=LINE, w=2)
    c.poly([(sx + 95, sy - 45), (sx + 220, sy - 90), (sx + 220, sy + 90), (sx + 95, sy + 45)], fill=EQ, outline=LINE, w=2)
    c.text(sx + 45, sy, "HP/IP", 13, "b", HEAD, "mm")
    c.text(sx + 160, sy, "LP", 15, "b", HEAD, "mm")
    c.text(sx + 110, sy - 120, "STEAM TURBINE", 18, "b", HEAD, "mm")
    gen(c, sx + 280, sy, 34, "G4")
    c.value(sx + 236, sy + 50, "588.1", "MW", 16, 70)
    c.value(sx + 236, sy + 78, "3600", "rpm", 14, 70)
    # ACC
    pipe(c, [(sx + 160, sy + 90), (sx + 160, 650)], "#4f585d", 9)
    c.rect(1130, 650, 1400, 720, fill=EQ, outline=LINE, w=2)
    for k in range(10):
        c.ell(1140 + k * 26, 660, 1160 + k * 26, 680, fill="#9aa0a3", outline="#70787c", w=1)
        c.ell(1140 + k * 26, 688, 1160 + k * 26, 708, fill="#9aa0a3", outline="#70787c", w=1)
    c.text(1265, 735, "ACC  80 / 80 FANS  ·  0.083 bar a", 13, "r", TXT, "ma")
    # plant totals panel
    c.rect(1420, 60, 1590, 520, fill=PANEL, outline="#9aa0a3")
    c.text(1505, 70, "UNIT", 14, "b", HEAD, "ma")
    rows = [("GROSS", "1705.2", "MW"), ("NET", "1668.4", "MW"), ("AGC SP", "1670.0", "MW"), ("RAMP", "+0.0", "MW/m"),
            ("FREQ", "60.002", "Hz"), ("230 kV", "234.6", "kV"), ("MVAR", "+212", "Mvar"), ("HEAT RT", "6,214", "Btu/kWh")]
    for k, (a, b, u) in enumerate(rows):
        y = 100 + k * 50
        c.text(1430, y, a, 12, "r", TXT)
        c.value(1430, y + 16, b, u, 15, 92)
    c.text(1505, 512, "AGC  ON  ·  ISO REMOTE", 12, "b", GRN, "ms")
    # mini trend
    c.rect(1420, 540, 1590, 720, fill="#d4d7d8", outline="#9aa0a3")
    c.text(1430, 546, "NET MW  2 h", 12, "r")
    random.seed(4)
    pts = []
    for k in range(60):
        v = 1550 + 118 * min(1, k / 30) + random.uniform(-4, 4)
        pts.append((1425 + k * 2.75, 712 - (v - 1500) * .9))
    c.line(pts, BLU, 2)
    # ambient
    c.text(30, 800, "AMBIENT 27.4 °C   RH 54 %   BARO 1012 hPa   ·   INLET CHILLING ON   ·   CCS 92 % CAPTURE", 14, "r", TXT)
    return c


def sld(S=2):
    c = C("ELECTRICAL  ·  230 kV SWITCHYARD", S, None)
    y1, y2 = 140, 640
    c.line([(80, y1), (1520, y1)], "#2a2f33", 6)
    c.line([(80, y2), (1520, y2)], "#2a2f33", 6)
    c.text(60, y1 - 30, "BUS 1   234.6 kV", 15, "b", HEAD)
    c.text(60, y2 + 14, "BUS 2   234.5 kV", 15, "b", HEAD)
    ties = [("LINE-1", "−812 MW"), ("GSU-1", "368 MW"), ("LINE-2", "−806 MW"), ("GSU-2", "367 MW"),
            ("GSU-3", "368 MW"), ("GSU-ST", "582 MW"), ("SPARE", ""), ("FUTURE", "")]
    for d in range(4):
        x = 230 + d * 340
        c.line([(x, y1), (x, y2)], "#2a2f33", 3)
        for j, yb in enumerate((y1 + 70, (y1 + y2) / 2, y2 - 70)):
            closed = not (d == 3)
            c.rect(x - 16, yb - 16, x + 16, yb + 16, fill=RED if closed else BG, outline="#1d2226", w=2)
            c.text(x + 24, yb - 8, f"52-{d + 1}{j + 1}", 12, "m", TXT)
        for side, yb in ((-1, y1 + 160), (1, y2 - 160)):
            name, mw = ties[d * 2 + (side > 0)]
            xe = x + side * 120
            c.line([(x, yb), (xe, yb), (xe, yb + 60 * (1 if side < 0 else -1))], "#2a2f33", 3)
            yy = yb + 60 * (1 if side < 0 else -1)
            if name.startswith("GSU"):
                c.ell(xe - 22, yy - 4, xe + 22, yy + 40, outline="#1d2226", w=2)
                c.ell(xe - 22, yy + 26, xe + 22, yy + 70, outline="#1d2226", w=2)
                c.ell(xe - 20, yy + 90, xe + 20, yy + 130, fill=EQ, outline="#1d2226", w=2)
                c.text(xe, yy + 110, "G", 14, "b", TXT, "mm")
                c.line([(xe, yy + 70), (xe, yy + 90)], "#2a2f33", 3)
            else:
                c.poly([(xe - 14, yy), (xe + 14, yy), (xe, yy + 22)], fill="#5b6468", outline="#1d2226")
            c.text(xe + 30, yy + 4, name, 14, "b", HEAD)
            if mw:
                c.value(xe + 30, yy + 24, mw.split()[0], "MW", 13, 62)
    c.rect(1250, 700, 1590, 850, fill=PANEL, outline="#9aa0a3")
    for k, (a, b) in enumerate((("UAT-1/2/3", "13.8 kV  ·  38 MW"), ("SWGR-13.8-1/2/3", "CLOSED  ·  NORMAL"),
                                ("EDG-1/2", "STANDBY  ·  AUTO"), ("BLACK START", "READY"))):
        c.text(1262, 712 + k * 34, a, 13, "b", HEAD)
        c.text(1580, 712 + k * 34, b, 13, "m", VAL, "ra")
    return c


def gt1(S=1):
    c = C("GT1  ·  GAS TURBINE", S)
    gt_shape(c, 120, 360, 2.4)
    c.text(470, 120, "GT1  ·  H-CLASS  ·  BASE LOAD", 22, "b", HEAD, "ma")
    vals = [(150, 180, "84.0", "° IGV"), (330, 180, "23.4", "bar CPD"), (520, 180, "1,442", "°C FIRING*"),
            (700, 180, "627", "°C EXH"), (150, 520, "18.6", "kg/s GAS"), (330, 520, "2.1", "ppm NOx"),
            (520, 520, "3600", "rpm"), (700, 520, "372.4", "MW")]
    for (x, y, v, u) in vals:
        c.value(x, y, v, u, 16, 80)
    c.rect(960, 70, 1590, 420, fill=PANEL, outline="#9aa0a3")
    c.text(975, 80, "EXHAUST TEMPERATURE SPREAD (31 TC)", 14, "b", HEAD)
    random.seed(1)
    for k in range(31):
        v = 627 + random.uniform(-9, 9) + (14 if k == 17 else 0)
        h = (v - 560) * 3.2
        c.rect(985 + k * 19, 400 - h, 999 + k * 19, 400, fill=YEL if k == 17 else "#7d878c")
    c.line([(980, 400 - 67 * 3.2), (1580, 400 - 67 * 3.2)], "#30363a", 1)
    c.text(1580, 395 - 67 * 3.2 - 18, "AVG 627 °C", 12, "m", TXT, "ra")
    c.rect(960, 440, 1590, 840, fill=PANEL, outline="#9aa0a3")
    c.text(975, 450, "BEARINGS / VIBRATION", 14, "b", HEAD)
    for k, (b, t, v) in enumerate((("BRG 1", "96", "2.8"), ("BRG 2", "101", "3.1"), ("GEN DE", "88", "1.9"), ("GEN NDE", "86", "1.7"))):
        y = 490 + k * 80
        c.text(980, y, b, 14, "b", HEAD)
        c.bar(1090, y + 4, 200, 14, int(t) / 140, .1, .8, "", f"{t} °C")
        c.bar(1340, y + 4, 200, 14, float(v) / 12, .0, .6, "", f"{v} mm/s")
    c.rect(40, 640, 920, 840, fill=PANEL, outline="#9aa0a3")
    c.text(55, 650, "FUEL GAS  ·  DLN MODE 6", 14, "b", HEAD)
    for k, (n, p) in enumerate((("SRV", .78), ("GCV-1", .64), ("GCV-2", .41), ("GCV-3", .52), ("GCV-4", .37))):
        c.bar(60 + k * 170, 700, 140, 16, p, .1, .9, n, f"{p * 100:.0f} %")
    c.text(55, 790, "* calculated", 11, "r", "#555")
    return c


def hrsg1(S=1):
    c = C("HRSG 1  ·  3P REHEAT", S)
    for k, (n, p, t, lvl) in enumerate((("HP DRUM", "168.4 bar", "585 °C", .58), ("IP DRUM", "38.6 bar", "582 °C RH", .55),
                                         ("LP DRUM", "5.2 bar", "318 °C", .61))):
        x = 120 + k * 480
        c.ell(x, 140, x + 300, 260, fill=EQ, outline=LINE, w=2)
        c.rect(x + 20, 140 + 120 * (1 - lvl), x + 280, 250, fill="#8fa3b3")
        c.ell(x, 140, x + 300, 260, outline=LINE, w=2)
        c.text(x + 150, 120, n, 18, "b", HEAD, "mm")
        c.value(x + 40, 290, p.split()[0], p.split()[1], 16, 90)
        c.value(x + 40, 326, t.split()[0], " ".join(t.split()[1:]), 16, 90)
        c.bar(x + 20, 390, 260, 16, lvl, .4, .7, "LEVEL", f"{(lvl - .5) * 400:+.0f} mm")
        for j in range(5):
            c.rect(x + 30 + j * 50, 470, x + 60 + j * 50, 700, fill="#a2a8ab", outline="#7a8286")
        c.text(x + 150, 715, ("HP SH / RH", "IP EVAP / ECON", "LP EVAP / ECON")[k], 13, "r", TXT, "ma")
    c.rect(40, 760, 1560, 850, fill=PANEL, outline="#9aa0a3")
    for k, (n, s) in enumerate((("BFP-1A", 1), ("BFP-1B", 0), ("CEP-A", 1), ("CEP-B", 1), ("SCR NH3", 1), ("DUCT BURNER", 0))):
        x = 60 + k * 250
        c.rect(x, 785, x + 22, 807, fill=RED if s else GRN, outline="#333")
        c.text(x + 32, 786, n + ("  RUN" if s else "  STBY"), 14, "b", HEAD)
    return c


def trend(S=1):
    c = C("TRENDS  ·  8 HOURS", S)
    random.seed(7)
    charts = [("NET MW", 1300, 1750, BLU, lambda t: 1380 + 290 * min(1, max(0, (t - .25) * 2.2)) + random.uniform(-6, 6)),
              ("FREQUENCY  Hz", 59.95, 60.05, ORG, lambda t: 60 + random.uniform(-.012, .012) + (-.03 if .6 < t < .62 else 0)),
              ("GT EXHAUST  °C", 560, 660, RED, lambda t: 600 + 27 * min(1, max(0, (t - .25) * 2.2)) + random.uniform(-2, 2)),
              ("CONDENSER  bar a", .05, .12, GRN, lambda t: .07 + .013 * min(1, max(0, (t - .25) * 2.2)) + random.uniform(-.002, .002))]
    for k, (n, lo, hi, col, fn) in enumerate(charts):
        y0 = 60 + k * 198
        c.rect(70, y0, 1580, y0 + 180, fill="#d6d8d9", outline="#9aa0a3")
        for j in range(1, 8):
            c.line([(70 + j * 1510 / 8, y0), (70 + j * 1510 / 8, y0 + 180)], "#bfc3c5", 1)
        for j in range(1, 4):
            c.line([(70, y0 + j * 45), (1580, y0 + j * 45)], "#bfc3c5", 1)
        pts = [(70 + i * 1510 / 400, y0 + 180 - (fn(i / 400) - lo) / (hi - lo) * 180) for i in range(401)]
        c.line(pts, col, 2)
        c.text(80, y0 + 6, n, 14, "b", HEAD)
        c.text(64, y0, f"{hi:g}", 11, "m", TXT, "ra")
        c.text(64, y0 + 168, f"{lo:g}", 11, "m", TXT, "ra")
    for j in range(9):
        c.text(70 + j * 1510 / 8, 852, f"{6 + j:02d}:30", 11, "m", TXT, "mb")
    return c


def alarm(S=1):
    c = C("ALARM SUMMARY", S)
    c.rect(20, 56, 1580, 84, fill="#a7adb0")
    for x, h in ((30, "P"), (70, "TIME"), (190, "TAG"), (420, "DESCRIPTION"), (1180, "VALUE"), (1380, "STATE")):
        c.text(x, 62, h, 14, "b", HEAD)
    rows = [(3, "14:29:51", "ACC-C07-M3", "ACC CELL 7 FAN 3 VIBRATION HIGH", "7.4 mm/s", "UNACK"),
            (4, "14:18:22", "WT-AIT-212", "DEMIN WATER CONDUCTIVITY TREND HIGH", "0.12 µS", "ACK"),
            (3, "13:57:10", "GT1-TT-XD17", "GT1 EXHAUST TC 17 DEVIATION", "+14 °C", "ACK"),
            (4, "13:40:02", "CCS-PT-418", "ABSORBER B DIFF PRESSURE HIGH", "41 mbar", "ACK"),
            (2, "13:12:45", "BAT-1-CHG", "BATTERY CHARGER 1 AC FAIL (TRANSFERRED)", "—", "RTN"),
            (4, "12:58:30", "HRSG2-LT-HP", "HRSG 2 HP DRUM LEVEL DEVIATION", "+62 mm", "RTN"),
            (3, "12:41:16", "IC-TE-110", "INLET CHILLER 3 CHW SUPPLY TEMP HIGH", "8.9 °C", "ACK"),
            (4, "12:20:07", "FG-PT-021", "GAS YARD INLET PRESSURE LOW", "36.1 bar", "RTN"),
            (4, "11:59:44", "R4-HVAC-2", "R4 HVAC UNIT 2 FILTER DP HIGH", "260 Pa", "ACK"),
            (3, "11:31:09", "ST-VT-04", "ST BEARING 4 VIBRATION ALERT", "5.1 mm/s", "RTN"),
            (4, "11:02:55", "CW-LT-301", "RAW WATER TANK LEVEL LOW", "41 %", "RTN"),
            (4, "10:47:38", "F&G-GD-14", "GAS DETECTOR 14 FAULT", "—", "ACK"),
            (2, "10:22:19", "SWYD-52-34", "BREAKER 52-34 SF6 DENSITY LOW", "0.61 MPa", "ACK"),
            (4, "09:58:02", "BESS-B07", "BESS BLOCK 7 CELL ΔT HIGH", "6.2 °C", "RTN"),
            (4, "09:31:47", "MCC-C1-12", "MCC-C1 BUCKET 12 TRIP", "—", "RTN"),
            (3, "09:05:12", "GT3-FT-201", "GT3 FUEL GAS FILTER DP HIGH", "0.42 bar", "ACK"),
            (4, "08:44:31", "WW-LS-02", "WASTEWATER SUMP LEVEL HIGH", "—", "RTN"),
            (4, "08:13:58", "CR-UPS-B", "UPS-B ON BYPASS (MAINT)", "—", "SHLV")]
    pc = {1: RED, 2: ORG, 3: YEL, 4: CYN}
    for k, (p, t, tag, d, v, s) in enumerate(rows):
        y = 92 + k * 40
        if k % 2:
            c.rect(20, y - 4, 1580, y + 32, fill="#c2c6c8")
        c.rect(30, y, 56, y + 24, fill=pc[p])
        c.text(43, y + 3, str(p), 15, "mb", "#111", "ma")
        dim = s in ("RTN", "SHLV")
        col = "#666c70" if dim else TXT
        c.text(70, y + 3, t, 15, "m", col)
        c.text(190, y + 3, tag, 15, "m", col)
        c.text(420, y + 3, d, 15, "r", col)
        c.text(1180, y + 3, v, 15, "m", col)
        c.text(1380, y + 3, s, 15, "mb", RED if s == "UNACK" else col)
    return c


def acc(S=1):
    c = C("ACC  ·  80 CELLS", S)
    random.seed(3)
    for r in range(8):
        for k in range(10):
            x, y = 60 + k * 118, 70 + r * 92
            alarm_ = (r == 0 and k == 6)
            c.rect(x, y, x + 108, y + 82, fill="#c2c6c8", outline=YEL if alarm_ else "#8e9599", w=3 if alarm_ else 1)
            c.ell(x + 8, y + 10, x + 52, y + 54, fill=EQ, outline=LINE)
            sp = random.randint(86, 98)
            c.text(x + 30, y + 32, f"{sp}", 13, "mb", VAL, "mm")
            c.text(x + 100, y + 8, f"C{r * 10 + k + 1:02d}", 12, "m", TXT, "ra")
            c.text(x + 100, y + 60, "%", 11, "r", TXT, "ra")
            c.rect(x + 60, y + 36, x + 72, y + 48, fill=RED)
    c.rect(1250, 70, 1590, 800, fill=PANEL, outline="#9aa0a3")
    for k, (a, b, u) in enumerate((("COND PRESS", "0.083", "bar a"), ("STEAM FLOW", "412", "kg/s"), ("COND TEMP", "41.6", "°C"),
                                   ("AMBIENT", "27.4", "°C"), ("FANS RUN", "80/80", ""), ("AVG SPEED", "92", "%"),
                                   ("VAC PUMPS", "2/3", "RUN"), ("HOTWELL", "62", "%"))):
        c.text(1265, 88 + k * 86, a, 14, "b", HEAD)
        c.value(1265, 110 + k * 86, b, u, 18, 120)
    return c


def grid(S=1):
    c = C("DISPATCH  ·  ISO / AGC", S)
    c.text(60, 80, "NET OUTPUT", 22, "b", HEAD)
    c.text(60, 110, "1,668.4", 96, "b", VAL)
    c.text(520, 168, "MW", 30, "b", HEAD)
    c.text(60, 250, "ISO SETPOINT 1,670.0 MW   ·   AGC ON   ·   REG UP 40 MW   ·   SPIN 120 MW", 18, "r", TXT)
    c.rect(60, 300, 1000, 760, fill="#d6d8d9", outline="#9aa0a3")
    c.text(75, 308, "SCHEDULE vs ACTUAL  ·  TODAY", 14, "b", HEAD)
    sched = [1150, 1100, 1080, 1080, 1120, 1250, 1420, 1580, 1650, 1670, 1670, 1670, 1670, 1670, 1670, 1700, 1720, 1740, 1740,
             1700, 1600, 1450, 1300, 1200]
    pts = [(80 + h * 39, 750 - (v - 1000) * .6) for h, v in enumerate(sched)]
    stepped = []
    for (x, y), (x2, _) in zip(pts, pts[1:] + [(pts[-1][0] + 39, 0)]):
        stepped += [(x, y), (x2, y)]
    c.line(stepped, "#4a5257", 2)
    random.seed(9)
    act = [(x + random.uniform(0, 30), y + random.uniform(-5, 5)) for (x, y) in stepped[:29]]
    c.line(act, BLU, 3)
    c.line([(80 + 14.5 * 39, 300), (80 + 14.5 * 39, 760)], RED, 1)
    for k, (n, v, u, f) in enumerate((("FREQUENCY", "60.002", "Hz", .51), ("230 kV BUS", "234.6", "kV", .6), ("POWER FACTOR", "0.992", "lag", .7))):
        cx, cy = 1180 + (k % 2) * 220, 330 + (k // 2) * 230
        c.ell(cx - 90, cy - 90, cx + 90, cy + 90, fill="#d6d8d9", outline="#8b9296", w=2)
        a = math.radians(210 - 240 * f)
        c.line([(cx, cy), (cx + 70 * math.cos(a), cy - 70 * math.sin(a))], "#1d2226", 4)
        c.text(cx, cy + 40, v, 20, "mb", VAL, "mm")
        c.text(cx, cy + 62, u, 13, "r", TXT, "mm")
        c.text(cx, cy - 110, n, 13, "b", HEAD, "mm")
    c.rect(1080, 640, 1580, 840, fill=PANEL, outline="#9aa0a3")
    c.text(1095, 650, "WEATHER", 14, "b", HEAD)
    for k, (a, b) in enumerate((("AMBIENT", "27.4 °C"), ("RH", "54 %"), ("WIND", "SW 11 km/h"), ("FORECAST PEAK", "31 °C  16:00"))):
        c.text(1095, 685 + k * 36, a, 15, "r", TXT)
        c.text(1570, 685 + k * 36, b, 15, "mb", VAL, "ra")
    return c


def cctv(S=2):
    c = C("CCTV  ·  SITE CAMERAS", S, ["MOSAIC 3x3", "GT HALL", "SWYD", "GATES", "PERIMETER"])
    srcs = [("E66", "CAM 04  GT HALL  EL 0"), ("E31", "CAM 11  SWITCHYARD"), ("E37", "CAM 01  MAIN GATE"),
            ("E34", "CAM 22  ACC SOUTH"), ("E41", "CAM 31  BESS YARD"), ("E35", "CAM 17  TANK FARM"),
            ("E43", "CAM 26  INLET CHILL"), ("E32", "CAM 08  R1 / TRANSFORMERS"), ("E64", "CAM 40  MODULAR YARD")]
    ep = os.path.join(PLANT, "renders", "epic")
    for k, (src, lab) in enumerate(srcs):
        r, q = divmod(k, 3)
        x0, y0 = 10 + q * 528, 52 + r * 270
        p = os.path.join(ep, f"{src}_pro_clean.jpg")
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = ImageOps.fit(im, (int(518 * S), int(262 * S)))
            im = ImageEnhance.Color(im).enhance(.55)
            im = ImageEnhance.Contrast(im).enhance(.9)
            c.im.paste(im, (int(x0 * S), int(y0 * S)))
        else:
            c.rect(x0, y0, x0 + 518, y0 + 262, fill="#555")
        c.rect(x0, y0, x0 + 518, y0 + 22, fill="#000000")
        c.text(x0 + 6, y0 + 3, lab, 13, "m", "#f0f0f0")
        c.text(x0 + 512, y0 + 3, f"{DATE} {CLOCK}", 12, "m", "#f0f0f0", "ra")
        c.ell(x0 + 498, y0 + 240, x0 + 510, y0 + 252, fill=RED, outline=RED)
    return c


SCREENS = {"overview": overview, "sld": sld, "gt1": gt1, "hrsg1": hrsg1, "trend": trend, "alarm": alarm, "acc": acc,
           "grid": grid, "cctv": cctv}
WALL_SPLIT = ("overview", "sld", "cctv")       # shown across 2 x 2 video-wall cubes
EXT = {"cctv": ".jpg"}                         # camera mosaics are photos: JPEG


def main():
    out = []
    for n, fn in SCREENS.items():
        c = fn()
        p = c.save(n)
        out.append(p)
        if n in WALL_SPLIT:
            im = Image.open(p)
            W, H = im.size
            ext = EXT.get(n, ".png")
            for r in range(2):
                for q in range(2):
                    im.crop((q * W // 2, r * H // 2, (q + 1) * W // 2, (r + 1) * H // 2)).save(
                        os.path.join(HERE, f"{n}_q{r}{q}{ext}"), **({"quality": 86} if ext == ".jpg" else {"optimize": True}))
        # 1600 x 900 working copy for monitors (the wall screens are drawn at 2x)
        if c.S != 1:
            Image.open(p).resize((1600, 900), Image.LANCZOS).save(p, **({"quality": 86} if p.endswith(".jpg") else {"optimize": True}))
    print("screens", len(out))


if __name__ == "__main__":
    main()
