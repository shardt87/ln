"""Detailed demonstration CCGT plant in the rev89 schema (pure stdlib).

Every one of the 47 OEM card packages gets technically recognizable geometry:
a gas turbine reads as compressor / combustor cans / turbine / exhaust
diffuser, a GSU as tank + radiator banks + HV bushings + conservator, an ACC
as A-frame streets over fan rings, a CCS island as absorber / DCC / regen
columns with platforms, and so on. Names follow the rev89 part schema so the
oemcards PKG prefixes select them exactly. Units metres, y-up, grade y=0,
identity transforms.

Usage: python3 mkplantglb.py plant.glb
"""
import json, math, struct, sys

parts = []   # (name, verts, tris)
_cur = None  # accumulating part


def part(name):
    global _cur
    _cur = (name, [], [])
    parts.append(_cur)


def _emit(v, f):
    base = len(_cur[1])
    _cur[1].extend(v)
    _cur[2].extend([(a + base, b + base, c + base) for a, b, c in f])


def _rot(p, axis, ang):
    if not ang:
        return p
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    x, y, z = p
    if axis == 'y':
        return (x * c + z * s, y, -x * s + z * c)
    if axis == 'x':
        return (x, y * c - z * s, y * s + z * c)
    return (x * c - y * s, x * s + y * c, z)


def _place(v, cx, cy, cz, rot=()):
    out = []
    for p in v:
        for axis, ang in rot:
            p = _rot(p, axis, ang)
        out.append((p[0] + cx, p[1] + cy, p[2] + cz))
    return out


def box(cx, cy, cz, sx, sy, sz, rot=()):
    x, y, z = sx / 2, sy / 2, sz / 2
    v = [(-x, -y, -z), (x, -y, -z), (x, y, -z), (-x, y, -z),
         (-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z)]
    f = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
         (3, 7, 6), (3, 6, 2), (0, 4, 7), (0, 7, 3), (1, 2, 6), (1, 6, 5)]
    _emit(_place(v, cx, cy, cz, rot), f)


def frustum(cx, cy, cz, r0, r1, h, axis='y', n=20, caps=True, rot=()):
    """r0 at -h/2, r1 at +h/2 along axis."""
    v, f = [], []
    for e, r in ((-h / 2, r0), (h / 2, r1)):
        for i in range(n):
            a = 2 * math.pi * i / n
            p, q = r * math.cos(a), r * math.sin(a)
            if axis == 'x':
                v.append((e, p, q))
            elif axis == 'y':
                v.append((p, e, q))
            else:
                v.append((p, q, e))
    for i in range(n):
        j = (i + 1) % n
        f += [(i, j, n + j), (i, n + j, n + i)]
    if caps:
        c0, c1 = len(v), len(v) + 1
        if axis == 'x':
            v += [(-h / 2, 0, 0), (h / 2, 0, 0)]
        elif axis == 'y':
            v += [(0, -h / 2, 0), (0, h / 2, 0)]
        else:
            v += [(0, 0, -h / 2), (0, 0, h / 2)]
        for i in range(n):
            j = (i + 1) % n
            f += [(c0, j, i), (c1, n + i, n + j)]
    _emit(_place(v, cx, cy, cz, rot), f)


def cyl(cx, cy, cz, r, h, axis='y', n=20, caps=True, rot=()):
    frustum(cx, cy, cz, r, r, h, axis, n, caps, rot)


def pipe(pts, r, n=12):
    """Polyline of capped cylinders (elbows read as joints)."""
    for (x0, y0, z0), (x1, y1, z1) in zip(pts, pts[1:]):
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        L = math.sqrt(dx * dx + dy * dy + dz * dz)
        if L < 1e-9:
            continue
        cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
        yaw = math.degrees(math.atan2(dx, dz))
        pitch = -math.degrees(math.asin(max(-1, min(1, dy / L))))
        cyl(cx, cy, cz, r, L, 'z', n, True, rot=(('x', pitch), ('y', yaw)))


def ladder(cx, cy, cz, h, face_dz=0.35, w=0.4):
    for s in (-w / 2, w / 2):
        box(cx + s, cy + h / 2, cz, 0.05, h, 0.05)
    steps = max(2, int(h / 0.35))
    for i in range(steps):
        box(cx, cy + (i + 0.5) * h / steps, cz, w, 0.03, 0.03)


def platform(cx, cy, cz, r):
    cyl(cx, cy, cz, r, 0.08, 'y', 24)
    for a in range(0, 360, 30):
        x = cx + r * math.sin(math.radians(a))
        z = cz + r * math.cos(math.radians(a))
        box(x, cy + 0.55, z, 0.05, 1.1, 0.05)
    cyl(cx, cy + 1.1, cz, r, 0.05, 'y', 24, caps=False)


def cabinet_row(x, y, z, n, w, h, d, axis='z', gap=0.02, detail=True):
    """Lineup of electrical cabinets on a plinth, with door panels proud of
    the face the card cameras see (az 200 looks from -x/-z)."""
    run = n * (w + gap) - gap
    if axis == 'z':
        box(x, y + 0.06, z + run / 2 - w / 2, d + 0.25, 0.12, run + 0.25)
    else:
        box(x + run / 2 - w / 2, y + 0.06, z, run + 0.25, 0.12, d + 0.25)
    y += 0.12
    for i in range(n):
        off = i * (w + gap)
        cx, cz = (x, z + off) if axis == 'z' else (x + off, z)
        box(cx, y + h / 2, cz, d if axis == 'z' else w, h, w if axis == 'z' else d)
        if detail:
            fx = cx - (d / 2 + 0.02 if axis == 'z' else 0)
            fz = cz - (0 if axis == 'z' else d / 2 + 0.02)
            box(fx, y + h * 0.68, fz, 0.04 if axis == 'z' else w * 0.6,
                h * 0.30, w * 0.6 if axis == 'z' else 0.04)
            box(fx, y + h * 0.28, fz, 0.04 if axis == 'z' else w * 0.6,
                h * 0.30, w * 0.6 if axis == 'z' else 0.04)


def fin_bank(cx, cy, cz, w, h, nfins, along='x', t=0.04, depth=0.5):
    """Radiator / cooler fin pack: array of thin plates."""
    for i in range(nfins):
        off = (i - (nfins - 1) / 2) * (w / nfins)
        if along == 'x':
            box(cx + off, cy, cz, t, h, depth)
        else:
            box(cx, cy, cz + off, depth, h, t)


def pad(name, cx, cz, sx, sz, t=0.15):
    part(name)
    box(cx, t / 2, cz, sx, t, sz)


def bushing(cx, cy, cz, h, r=0.14):
    frustum(cx, cy + h * 0.35, cz, r, r * 0.62, h * 0.7, 'y', 12)
    cyl(cx, cy + h * 0.78, cz, r * 0.5, h * 0.16, 'y', 12)
    cyl(cx, cy + h * 0.92, cz, 0.05, h * 0.16, 'y', 8)


# ============================================================== site & hall
part('site-base')
box(20, -0.1, 0, 240, 0.2, 200)
part('access-road-main')
box(20, 0.015, -32, 240, 0.03, 7)
part('access-road-east')
box(80, 0.015, 10, 7, 0.03, 130)
part('hall-apron')
box(2, 0.06, 16, 62, 0.12, 66)

# turbine hall roof (dropped on interior cards)
for i in range(4):
    part('HALL-SECTION-FIXED-ROOF-%d' % (i + 1))
    box(2, 16.2, -12 + 14.5 * i + 7.25, 58, 0.35, 14.5)
for i in range(5):
    part('HALL-FRAME-ROOF-BEAM-%d' % (i + 1))
    box(2, 15.6, -12 + 14.5 * i, 58, 0.7, 0.4)

# ======================================================== GT train 01 (GT)
part('GTG-01-skid-pad')
box(2, 0.2, 0, 26, 0.4, 6)
part('GTG-01-compressor')                      # inlet bellmouth + axial casing
box(-9.3, 2.6, 0, 1.8, 3.9, 3.9)               # inlet plenum
frustum(-6.9, 2.6, 0, 1.95, 1.5, 3.0, 'x', 24)  # compressor taper
part('GTG-01-gas-turbine')
cyl(-3.4, 2.6, 0, 1.55, 4.0, 'x', 24)           # compressor discharge / casing
cyl(0.3, 2.6, 0, 1.95, 3.0, 'x', 24)            # combustor section
for a in range(0, 360, 45):                     # can-annular combustors
    r = 1.85
    cy = 2.6 + r * math.cos(math.radians(a))
    cz = r * math.sin(math.radians(a))
    if cy > 1.1:
        cyl(0.3, cy, cz, 0.30, 1.35, 'x', 10, rot=())
frustum(3.0, 2.6, 0, 1.85, 1.45, 2.4, 'x', 24)  # turbine section
box(0.3, 0.9, 0, 8.5, 1.8, 3.4)                 # turbine deck / baseplate
part('GTG-01-exhaust')
frustum(6.2, 2.6, 0, 1.5, 2.5, 3.2, 'x', 24)    # exhaust diffuser
box(9.6, 3.4, 0, 3.6, 6.0, 5.0)                 # exhaust plenum
part('GTG-01-generator')                        # context in GT card
cyl(14.6, 2.4, 0, 1.8, 5.6, 'x', 24)
box(14.6, 4.8, 0, 4.2, 1.2, 3.0)

# ================================================= GT train 02 (GEN focus)
part('GTG-02-skid-pad')
box(2, 0.2, 18, 26, 0.4, 6)
part('GTG-02-gas-turbine')
cyl(-2, 2.6, 18, 1.8, 9.0, 'x', 24)
part('GTG-02-exhaust')
box(4.6, 3.2, 18, 3.0, 5.4, 4.6)
part('GTG-02-generator')
cyl(10.6, 2.4, 18, 1.85, 6.4, 'x', 28)          # stator body
box(10.6, 4.95, 18, 4.6, 1.5, 3.2)              # TEWAC cooler housing
frustum(7.0, 2.4, 18, 1.85, 1.1, 0.9, 'x', 28)   # end shields
frustum(14.2, 2.4, 18, 1.85, 1.1, 0.9, 'x', 28)
part('GTG-02-exciter')
cyl(15.6, 2.4, 18, 0.85, 1.9, 'x', 18)
box(15.6, 1.0, 18, 2.0, 1.4, 1.6)
part('GTG-02-terminal-box')
box(10.6, 1.5, 15.4, 2.6, 2.2, 1.0)
for i in range(3):
    bushing(9.8 + i * 0.8, 2.6, 15.4, 1.0, 0.10)

# ============================================= GT-2 auxiliaries (GTAUX)
part('GT-2-aux-skid-pad')
box(-14, 0.13, 24, 9, 0.26, 7)
part('GT-2-aux-lube-skid')
box(-16.5, 0.9, 22.5, 3.4, 1.3, 2.2)            # reservoir
cyl(-17.3, 2.0, 22.2, 0.28, 0.9, 'y', 12)        # AC pump motors
cyl(-16.3, 2.0, 22.2, 0.28, 0.9, 'y', 12)
fin_bank(-15.2, 1.9, 22.8, 1.2, 0.9, 7, 'x')     # oil cooler
cyl(-17.4, 2.2, 23.4, 0.22, 1.2, 'y', 10)        # accumulators
cyl(-16.8, 2.2, 23.4, 0.22, 1.2, 'y', 10)
part('GT-2-aux-hydraulic-skid')
box(-12.5, 0.7, 22.5, 2.2, 1.0, 1.8)
cyl(-12.9, 1.6, 22.3, 0.24, 0.8, 'y', 12)
cyl(-12.1, 1.75, 22.8, 0.20, 1.1, 'y', 10)
part('GT-2-aux-fuelgas-skid')
box(-14.5, 0.8, 26.0, 4.6, 1.2, 1.8)
pipe([(-17.0, 1.6, 26.0), (-12.0, 1.6, 26.0)], 0.16)
cyl(-15.8, 1.9, 26.0, 0.45, 1.6, 'y', 14)        # filter/separators
cyl(-14.2, 1.9, 26.0, 0.45, 1.6, 'y', 14)
box(-13.0, 2.0, 26.0, 0.5, 0.7, 0.5)             # control valve actuator

# ======================================= GT-2 controls (GTCTRL)
part('GT-2-aux-fuelgas-valve-rack')
box(-14, 0.1, 30.5, 6, 0.2, 2.4)
for i in range(4):                               # rack posts
    box(-16.5 + i * 1.66, 1.2, 30.5, 0.12, 2.4, 0.12)
box(-14, 2.35, 30.5, 5.6, 0.14, 0.6)             # rack beam
pipe([(-16.8, 1.5, 30.0), (-11.2, 1.5, 30.0)], 0.14)
pipe([(-16.8, 1.0, 31.0), (-11.2, 1.0, 31.0)], 0.10)
for i in range(3):                               # shutoff/vent valves
    x = -15.6 + i * 1.6
    box(x, 1.95, 30.0, 0.4, 0.9, 0.4)
part('TC-MARSHALLING-GT2')
cabinet_row(-11.2, 0, 32.6, 4, 0.8, 2.2, 0.8, axis='x')

# ========================================= GT-2 fire suppression (GTFIRE)
part('FIRE-GT-2-bottlerack')
box(-18.5, 0.1, 18, 2.8, 0.2, 1.4)
for i in range(7):
    cyl(-19.6 + i * 0.36, 0.95, 18, 0.14, 1.5, 'y', 10)
box(-18.5, 1.85, 18, 2.8, 0.12, 0.3)             # top restraint
pipe([(-19.6, 1.9, 18), (-17.4, 1.9, 18), (-17.4, 2.6, 18)], 0.06)
part('FIRE-GT-2-panel')
box(-18.5, 1.5, 16.6, 0.9, 1.1, 0.3)

# ============================================== inlet filter house (INLET)
part('air-inlet-2-filterhouse')
for lx, lz in ((-35, 12), (-29, 12), (-35, 20), (-29, 20)):
    box(lx, 2.5, lz, 0.5, 5.0, 0.5)              # support legs
box(-32, 7.6, 16, 8.5, 5.2, 9.5)                 # filter house body
for i in range(4):                               # weather hoods
    box(-36.5, 6.0 + i * 1.1, 16, 0.5, 0.55, 8.6, rot=(('z', -22),))
box(-32, 10.6, 16, 8.9, 0.3, 9.9)                # roof
part('air-inlet-2-duct')
box(-27.0, 6.8, 16, 2.2, 4.2, 4.6)               # transition
box(-25.2, 5.2, 16, 2.4, 3.4, 3.8, rot=(('z', -35),))
part('air-inlet-2-silencer')
box(-30, 4.2, 16, 3.2, 1.6, 6.8)

# ======================================================== HRSG-2 (HRSG)
part('HRSG-2-pad')
box(48, 0.13, 18, 26, 0.26, 12)
part('HRSG-2-inletduct')
box(38.5, 3.4, 18, 4.0, 5.6, 4.8, rot=(('z', 14),))
part('HRSG-2-casing')
box(48, 6.5, 18, 14, 13, 9)
for i in range(6):                               # module ribs
    box(42.2 + i * 2.3, 6.5, 22.6, 0.35, 12.6, 0.25)
    box(42.2 + i * 2.3, 6.5, 13.4, 0.35, 12.6, 0.25)
box(48, 13.4, 18, 14.4, 0.35, 9.4)               # casing roof
part('HRSG-2-drum-hp')
cyl(43, 14.6, 18, 1.05, 8.2, 'z', 20)
cyl(43, 14.6, 22.4, 0.5, 0.5, 'z', 12)           # manway
part('HRSG-2-drum-ip')
cyl(47, 14.35, 18, 0.85, 7.4, 'z', 18)
part('HRSG-2-drum-lp')
cyl(51, 14.15, 18, 0.7, 6.8, 'z', 16)
part('HRSG-2-risers')
for x, r in ((43, 1.05), (47, 0.85), (51, 0.7)):
    pipe([(x, 13.1, 15.2), (x, 14.6 - r, 15.2)], 0.14)
    pipe([(x, 13.1, 20.8), (x, 14.6 - r, 20.8)], 0.14)
part('HRSG-2-stack')
cyl(60.5, 12.5, 18, 1.9, 25, 'y', 28)
for yy in (6, 12, 18, 24):                        # stiffener rings
    cyl(60.5, yy, 18, 2.02, 0.3, 'y', 28, caps=False)
platform(60.5, 20.0, 18, 2.6)
ladder(62.6, 1, 18, 19)
part('HRSG-2-blowdown-tank')
cyl(55.5, 1.6, 24.5, 0.9, 3.0, 'y', 16)

# ======================================================== CEMS (CEMS)
part('CEMS-HRSG-2-shelter')
box(64.5, 1.3, 21.5, 2.4, 2.4, 2.0)
box(64.5, 2.62, 21.5, 2.7, 0.24, 2.3)            # shelter roof
part('CEMS-HRSG-2-probe')
box(62.6, 20.3, 19.6, 0.5, 0.5, 1.4)             # probe box on stack
part('CEMS-HRSG-2-umbilical')
pipe([(64.5, 2.4, 21.0), (63.2, 3.0, 19.4), (63.0, 20.0, 19.2)], 0.07, 8)

# ================================================== BFP trains (BFP)
part('BFP-2-pad')
box(40, 0.13, 30, 9, 0.26, 5)
part('BFP-2-motor')
cyl(37.6, 1.35, 30, 0.75, 2.6, 'x', 18)
box(37.6, 0.55, 30, 2.2, 0.7, 1.6)
part('BFP-2-coupling')
cyl(39.4, 1.35, 30, 0.35, 1.0, 'x', 12)
part('BFP-2-pump')
cyl(41.6, 1.35, 30, 0.62, 3.2, 'x', 18)          # barrel
cyl(40.6, 1.35, 30, 0.75, 0.5, 'x', 18)          # suction head
pipe([(42.8, 1.35, 30), (43.4, 1.35, 30), (43.4, 3.2, 30), (44.6, 3.2, 30)], 0.22)
part('BFP-2-lube')
box(39.5, 0.75, 32.0, 1.8, 0.9, 1.2)

# ============================================== steam turbine (STG)
part('STG-pedestal')
box(10, 1.0, 36, 17, 2.0, 6.5)
part('STG-hp-ip-casing')
box(4.0, 2.55, 36, 4.8, 1.1, 3.2)                # casing base
frustum(2.6, 3.4, 36, 1.15, 1.35, 2.2, 'x', 22)  # HP
frustum(5.2, 3.4, 36, 1.45, 1.25, 2.6, 'x', 22)  # IP
cyl(4.0, 3.4, 36, 1.05, 5.2, 'x', 22)
part('STG-lp-casing')
box(9.9, 3.4, 36, 4.6, 2.8, 5.8)                 # LP hood
frustum(9.9, 5.15, 36, 2.4, 1.9, 0.7, 'y', 4,
        rot=(('y', 45),))                        # hood taper (square)
pipe([(5.0, 4.4, 36), (5.0, 6.4, 36), (9.9, 6.4, 36),
      (9.9, 5.4, 36)], 0.45, 14)                 # crossover pipe
part('STG-generator')
cyl(14.6, 3.4, 36, 1.55, 4.8, 'x', 24)
box(14.6, 5.35, 36, 3.4, 1.1, 2.7)               # cooler housing
frustum(11.9, 3.4, 36, 1.55, 0.95, 0.7, 'x', 24)
frustum(17.3, 3.4, 36, 1.55, 0.95, 0.7, 'x', 24)
part('STG-exciter-end')
cyl(18.3, 3.4, 36, 0.7, 1.4, 'x', 14)
box(18.3, 2.2, 36, 1.4, 1.0, 1.4)

# ======================================= ST auxiliaries (STAUX)
part('ST-aux-pad')
box(-2, 0.13, 41, 8, 0.26, 5)
part('ST-aux-lubeoil-tank')
cyl(-4.5, 1.7, 41, 1.1, 3.2, 'y', 18)
cyl(-4.5, 3.5, 41, 0.3, 0.5, 'y', 10)            # vent
part('ST-aux-oil-coolers')
cyl(-2.4, 1.1, 40.0, 0.45, 2.6, 'z', 14)
cyl(-2.4, 1.1, 42.0, 0.45, 2.6, 'z', 14)
part('ST-aux-vacuum-skid')
box(0.6, 0.7, 40.2, 2.4, 1.0, 1.6)
cyl(0.0, 1.6, 40.2, 0.3, 0.8, 'y', 12)
cyl(1.2, 1.6, 40.2, 0.3, 0.8, 'y', 12)
part('ST-aux-gland-condenser')
cyl(0.8, 1.2, 42.6, 0.55, 2.4, 'x', 14)

# ================================================ condensate pumps (CEP)
part('CEP-pad')
box(18, 0.13, 41, 5, 0.26, 4)
for i, x in enumerate((16.8, 19.2)):
    part('CEP-%d' % (i + 1))
    box(x, 0.5, 41, 1.4, 0.6, 1.4)               # sole plate over can
    cyl(x, 2.2, 41, 0.42, 2.8, 'y', 14)          # vertical motor
    box(x, 0.95, 41.8, 0.8, 0.7, 0.9)            # discharge head
    pipe([(x, 0.95, 42.2), (x, 0.95, 43.0), (x, 2.6, 43.0)], 0.18)

# ============================================ ACC island (ACC / ACCFAN)
part('acc-steam-duct')                           # lowercase: context, not a
pipe([(12, 9.5, -20), (12, 9.5, -48), (-2, 9.5, -52),   # crop target
      (-2, 12.5, -55)], 1.3, 18)
part('ACC-support-structure')
for gx in range(3):
    for gz in range(3):
        box(-14 + gx * 12, 3.75, -72 + gz * 11, 0.55, 7.5, 0.55)
        box(-8 + gx * 12, 3.75, -72 + gz * 11, 0.55, 7.5, 0.55)
box(-5, 7.7, -61, 26, 0.5, 23.5)                 # fan deck
for i in range(6):
    part('ACC-street-%d' % (i + 1))              # A-frame condenser cells
    cx = -11 + (i % 3) * 12
    cz = -66.5 + (i // 3) * 11
    box(cx - 1.75, 10.6, cz, 0.4, 5.6, 9.6, rot=(('z', -28),))
    box(cx + 1.75, 10.6, cz, 0.4, 5.6, 9.6, rot=(('z', 28),))
    cyl(cx, 13.2, cz, 0.5, 9.6, 'z', 12)         # ridge steam header
for i in range(6):
    nm = i + 1
    part('ACC-fan-%d' % nm)
    cx = -11 + (i % 3) * 12
    cz = -66.5 + (i // 3) * 11
    cyl(cx, 8.5, cz, 4.4, 1.5, 'y', 30, caps=False)   # fan ring
    cyl(cx, 8.4, cz, 0.55, 0.9, 'y', 12)              # hub
    for a in range(0, 360, 60):
        box(cx + 2.2 * math.sin(math.radians(a)), 8.45,
            cz + 2.2 * math.cos(math.radians(a)),
            0.5, 0.09, 3.4, rot=(('y', a), ('x', 8)))
    part('ACC-fan-motor-%d' % nm)
    cyl(cx, 6.9, cz, 0.4, 1.3, 'y', 14)               # motor below deck
    box(cx, 7.5, cz, 0.75, 0.55, 0.75)                # gearbox

# ================================================ ACC VFDs (ACCVFD)
part('ELEC-ACC-VFD-house')
box(-30, 1.7, -46, 6.5, 3.2, 3.0)
box(-30, 3.5, -46, 6.9, 0.3, 3.4)
box(-27.4, 2.2, -44.3, 0.9, 1.2, 0.5)            # HVAC pods
box(-32.6, 2.2, -44.3, 0.9, 1.2, 0.5)
part('ELEC-ACC-VFD-xfmr')
box(-36, 1.1, -46, 1.9, 1.8, 1.6)
fin_bank(-36, 1.1, -44.9, 1.6, 1.3, 6, 'x', depth=0.4)
bushing(-36.4, 2.1, -46.4, 0.7, 0.08)
bushing(-35.6, 2.1, -46.4, 0.7, 0.08)

# ============================================ cooling tower (COOLTWR)
part('cooling-tower-basin')
box(70, 0.6, -30, 30, 1.2, 12)
for i in range(3):
    part('cooling-tower-cell-%d' % (i + 1))
    cx = 61 + i * 9
    box(cx, 4.6, -30, 8.6, 6.8, 11)
    for k in range(6):                            # inlet louvers
        box(cx, 1.6 + k * 0.55, -24.4, 8.2, 0.4, 0.5, rot=(('x', 40),))
        box(cx, 1.6 + k * 0.55, -35.6, 8.2, 0.4, 0.5, rot=(('x', -40),))
    frustum(cx, 8.9, -30, 3.4, 2.6, 2.2, 'y', 22, caps=False)  # fan stack
    cyl(cx, 8.6, -30, 0.45, 0.7, 'y', 10)
    for a in range(0, 360, 90):
        box(cx + 1.5 * math.sin(math.radians(a)), 8.55,
            -30 + 1.5 * math.cos(math.radians(a)),
            0.4, 0.07, 2.3, rot=(('y', a),))

# ======================================== CW / raw water pumps (CWPUMP)
part('pump-house')
box(70, 2.4, -12, 14, 4.8, 8)
box(70, 4.95, -12, 14.6, 0.35, 8.6)
for i in range(3):
    x = 66 + i * 4
    part('pump-motor-%d' % (i + 1))
    cyl(x, 3.1, -10.5, 0.5, 2.2, 'y', 16)
    part('pump-casing-%d' % (i + 1))
    cyl(x, 1.2, -10.5, 0.85, 1.4, 'y', 18)       # volute
    pipe([(x, 1.2, -9.6), (x, 1.2, -7.6), (x, 2.6, -7.6)], 0.35)

# ================================================== chillers (CHILLER)
part('chiller-pad')
box(56, 0.13, -12, 9, 0.26, 5)
for i, z in enumerate((-13.3, -10.7)):
    part('chiller-%d' % (i + 1))
    cyl(56, 0.95, z, 0.62, 6.5, 'x', 18)         # evaporator shell
    cyl(56, 2.05, z, 0.55, 6.0, 'x', 18)         # condenser shell
    cyl(54.5, 2.75, z, 0.4, 1.6, 'x', 14)        # compressor
    box(58.8, 1.4, z, 0.7, 1.6, 0.9)             # panel

# =============================================== GSU transformers (GSU)
for i in range(3):
    x = 0 + i * 14
    part('transformer-%d-pad' % i)
    box(x, 0.16, -22, 9.5, 0.32, 8)
    part('transformer-%d' % i)
    box(x, 2.5, -22, 5.2, 4.4, 3.6)              # tank
    box(x, 4.85, -22, 5.5, 0.35, 3.9)            # cover
    cyl(x - 1.0, 6.1, -22, 0.5, 3.6, 'z', 14)    # conservator
    box(x - 1.0, 5.35, -22, 0.3, 1.2, 0.3)
    for k in range(3):                           # HV bushings
        bushing(x - 1.6 + k * 1.6, 5.1, -22.9, 2.6, 0.17)
    for k in range(3):                           # LV bushings
        bushing(x - 1.2 + k * 1.2, 5.1, -21.0, 1.1, 0.11)
    for sgn in (-1, 1):                          # radiator banks + fans
        fin_bank(x + sgn * 3.6, 2.3, -22, 2.6, 3.2, 8, 'x', depth=1.1)
        pipe([(x + sgn * 2.7, 4.2, -22), (x + sgn * 4.6, 4.2, -22)], 0.14)
        pipe([(x + sgn * 2.7, 0.8, -22), (x + sgn * 4.6, 0.8, -22)], 0.14)
        cyl(x + sgn * 3.6, 0.35, -20.6, 0.5, 0.4, 'y', 14, caps=False)
part('GSU-firewall-1')
box(7, 3.2, -22, 0.5, 6.4, 9)
part('GSU-firewall-2')
box(21, 3.2, -22, 0.5, 6.4, 9)

# ===================================== generator breaker + IPB (GCB)
part('GCB-2-housing')
box(20.5, 2.6, 18, 3.2, 2.6, 2.4)
box(19.6, 2.9, 16.7, 0.9, 1.1, 0.1)              # access panels
box(21.4, 2.9, 16.7, 0.9, 1.1, 0.1)
part('GCB-2-ipb')
pipe([(17.0, 2.6, 18), (25.5, 2.6, 18)], 0.55, 16)
for x in (18.4, 23.8):
    box(x, 1.1, 18, 0.4, 2.2, 0.4)               # duct supports

# ================================================ NGR (NGR)
part('NGR-2-cubicle')
box(24.5, 1.3, 22.5, 1.6, 2.2, 1.4)
part('NGR-2-resistor-frame')
for k in range(5):
    box(24.5, 0.6 + k * 0.35, 24.4, 1.3, 0.06, 0.9)
box(23.9, 1.2, 24.4, 0.1, 1.9, 1.0)
box(25.1, 1.2, 24.4, 0.1, 1.9, 1.0)
bushing(24.5, 2.35, 22.5, 0.8, 0.1)

# ============================================== HV switchyard (SWYARD)
part('substation-gravel-pad')
box(14, 0.05, -52, 44, 0.1, 22)
for b in range(2):                               # gantry
    part('substation-gantry-%d' % (b + 1))
    for x in (-2 + b * 32,):
        box(x, 5.5, -44, 0.7, 11, 0.7)
        box(x, 5.5, -60, 0.7, 11, 0.7)
        box(x, 10.7, -52, 0.6, 0.6, 17)
for i in range(3):                               # dead tank breakers
    part('substation-breaker-%d' % (i + 1))
    x = 4 + i * 10
    box(x, 1.0, -50, 3.2, 0.9, 1.4)              # frame
    for lx in (-1.3, 1.3):
        for lz in (-0.5, 0.5):
            box(x + lx, 0.35, -50 + lz, 0.18, 0.7, 0.18)
    cyl(x, 2.2, -50, 0.55, 3.0, 'x', 14)         # tank
    for k in range(3):
        bushing(x - 1.0 + k * 1.0, 2.8, -50, 2.0, 0.13)
    box(x + 1.9, 1.6, -50.9, 0.7, 1.1, 0.5)      # mechanism cabinet
for i in range(3):
    part('substation-disconnect-%d' % (i + 1))
    x = 4 + i * 10
    for dz in (-1.1, 1.1):
        box(x + dz * 0, 2.0, -45 + dz, 0.25, 2.6, 0.25)
        frustum(x, 3.6, -45 + dz, 0.14, 0.09, 0.9, 'y', 8)
    box(x, 4.15, -45, 0.12, 0.1, 2.4)            # switch arm
for i in range(3):
    part('substation-ct-%d' % (i + 1))
    x = 4 + i * 10
    box(x, 0.8, -55.5, 0.8, 1.6, 0.8)
    frustum(x, 2.5, -55.5, 0.4, 0.3, 1.8, 'y', 12)
    cyl(x, 3.6, -55.5, 0.5, 0.6, 'y', 12)        # head
part('substation-cvt-1')
box(20, 0.7, -58.5, 0.7, 1.4, 0.7)
frustum(20, 2.6, -58.5, 0.24, 0.16, 2.6, 'y', 10)
cyl(20, 4.05, -58.5, 0.3, 0.3, 'y', 10)
part('substation-arrester-1')
box(9, 0.55, -58.5, 0.6, 1.1, 0.6)
frustum(9, 2.1, -58.5, 0.17, 0.12, 2.0, 'y', 8)
part('substation-bus-runs')                      # tubular bus, 3 phases
for i in range(3):
    x = 4 + i * 10
    pipe([(x - 1.0, 4.4, -45), (x - 1.0, 4.4, -55.5)], 0.06, 8)
    pipe([(x, 4.4, -45), (x, 4.4, -55.5)], 0.06, 8)
    pipe([(x + 1.0, 4.4, -45), (x + 1.0, 4.4, -55.5)], 0.06, 8)
    pipe([(x - 1.0, 4.8, -50), (x - 1.0, 2.8 + 2.0, -50)], 0.04, 6)

# ===================================== substation control (SUBCTRL)
part('substation-control-house')
box(40, 1.9, -52, 7.5, 3.4, 4.5)
box(40, 3.75, -52, 7.9, 0.3, 4.9)
box(37.2, 1.55, -49.6, 1.1, 2.3, 0.15)           # door
cyl(43.2, 5.0, -53.8, 0.05, 3.0, 'y', 6)         # antenna mast
part('TRENCH-SUB-run')
box(30, 0.25, -52, 13, 0.5, 1.1)

# =============================== MV switchgear lineups (MVSWGR)
part('SWGR-MV-13800-lineup')
cabinet_row(-22.5, 0, -6, 6, 1.0, 2.4, 1.5)
box(-22.5, 2.75, -3.5 + 0.55, 1.2, 0.7, 6.2)     # top bus enclosure
part('SWGR-MV-4160-lineup')
cabinet_row(-22.5, 0, 3, 5, 0.9, 2.3, 1.4)
box(-22.5, 2.6, 5.28, 1.1, 0.6, 4.7)

# =============================== LV switchgear (LVSWGR)
part('SWGR-LV-480-lineup')
cabinet_row(-22.5, 0, 11, 5, 0.8, 2.2, 1.0)
part('lv-panelboard-wall')
for i in range(3):
    box(-24.6, 1.5, 11 + i * 1.1, 0.25, 1.1, 0.8)

# ======================================================= MCC room (MCC)
part('MCC-hall-bay-floor')
box(-21.5, 0.08, 24, 8, 0.16, 10)
part('MCC-A-lineup')
cabinet_row(-23.5, 0, 20.5, 6, 0.65, 2.3, 0.55)
part('MCC-B-lineup')
cabinet_row(-19.5, 0, 20.5, 6, 0.65, 2.3, 0.55)
part('MCC-overhead-tray')
box(-21.5, 3.1, 22.5, 3.6, 0.12, 0.6)
for i in range(6):
    box(-21.5, 3.1, 20.9 + i * 0.7, 3.6, 0.16, 0.08)

# ==================================================== e-house (EHOUSE)
part('ehouse-piers')
for px in (-44, -36):
    for pz in (-23, -17):
        box(px, 0.45, pz, 0.8, 0.9, 0.8)
part('ehouse')
box(-40, 2.7, -20, 11, 3.6, 7)
box(-40, 4.65, -20, 11.4, 0.3, 7.4)
box(-40.0, 5.25, -21.5, 2.2, 0.9, 1.6)           # roof HVAC
cyl(-40.0, 5.85, -21.5, 0.55, 0.3, 'y', 14, caps=False)
box(-36.5, 5.25, -18.5, 2.2, 0.9, 1.6)
box(-34.4, 2.0, -18.2, 0.15, 2.2, 1.1)           # door
box(-40, 1.1, -16.2, 7, 0.5, 0.7)                # cable bustle

# ======================================================== VFDs (VFD)
part('VFD-lineup')
cabinet_row(-22.5, 0, 32, 5, 0.9, 2.35, 1.1)
box(-22.5, 2.8, 34.2, 1.0, 0.5, 3.8)             # cooling duct

# ========================================================= UPS (UPS)
part('UPS-A')
cabinet_row(-16.5, 0, 39.5, 3, 0.8, 2.0, 0.9, axis='x')
part('UPS-B')
cabinet_row(-16.5, 0, 42.0, 3, 0.8, 2.0, 0.9, axis='x')

# =========================================== station battery / DC (DC)
part('battery-rack-A')
for tier in range(2):
    box(-23.5, 0.55 + tier * 0.75, 41.5, 0.75, 0.12, 4.4)
    for i in range(8):
        box(-23.5, 0.85 + tier * 0.75, 39.6 + i * 0.52, 0.55, 0.45, 0.4)
box(-23.9, 1.0, 41.5, 0.08, 2.0, 4.6)            # rack frame
part('battery-rack-B')
for tier in range(2):
    box(-21.8, 0.55 + tier * 0.75, 41.5, 0.75, 0.12, 4.4)
    for i in range(8):
        box(-21.8, 0.85 + tier * 0.75, 39.6 + i * 0.52, 0.55, 0.45, 0.4)
part('DC-CHARGER-panels')
cabinet_row(-19.8, 0, 40.2, 2, 0.8, 2.0, 0.6, axis='x')

# ================================================= DCS / control (DCS)
part('admin-dcs-cabinet-row')
cabinet_row(27.5, 0, 27, 5, 0.8, 2.0, 0.9)
part('admin-console-1')
box(24.0, 0.75, 29.5, 2.6, 0.08, 1.1)            # desk
box(24.0, 0.4, 29.5, 2.2, 0.7, 0.9)
box(24.0, 1.35, 30.1, 2.2, 0.75, 0.08, rot=(('x', -12),))  # monitor bank
part('admin-console-2')
box(24.0, 0.75, 32.0, 2.6, 0.08, 1.1)
box(24.0, 0.4, 32.0, 2.2, 0.7, 0.9)
box(24.0, 1.35, 32.6, 2.2, 0.75, 0.08, rot=(('x', -12),))
part('admin-mimic-panel')
box(21.5, 1.6, 31.0, 0.15, 2.2, 4.5)

# ================================================== BESS (BESSCONT etc)
part('BESS-container-0-1')
box(-30, 1.5, 60, 12.2, 2.9, 2.5)
box(-30, 3.05, 60, 12.5, 0.2, 2.7)
for i in range(5):                               # side HVAC pods
    box(-34.8 + i * 2.4, 1.6, 61.5, 1.0, 2.0, 0.45)
box(-24.2, 1.5, 58.9, 0.1, 2.4, 1.8)             # door end
part('ELEC-BESS-PCS-2')
box(-17.5, 1.4, 60, 5.5, 2.6, 2.2)
box(-17.5, 2.85, 60, 5.8, 0.2, 2.4)
box(-15.0, 1.5, 61.3, 1.6, 1.8, 0.4)             # inverter vents
box(-19.9, 1.5, 61.3, 1.6, 1.8, 0.4)
part('ELEC-BESS-XFMR-2')
box(-8.5, 1.35, 60, 2.6, 2.3, 2.0)
fin_bank(-8.5, 1.3, 61.4, 2.2, 1.6, 7, 'x', depth=0.5)
bushing(-9.1, 2.55, 59.4, 0.8, 0.1)
bushing(-7.9, 2.55, 59.4, 0.8, 0.1)
part('ELEC-BESS-COLLECTOR')
box(-4.8, 1.25, 60, 1.8, 2.2, 1.4)

# ============================================ RICE / gas engines (RICE)
part('modular-unit-2-pad')
box(10, 0.16, 62, 14, 0.32, 7)
part('modular-unit-2-engine')
box(8.0, 1.9, 62, 6.0, 2.4, 2.2)                 # block
for i in range(6):                               # cylinder heads
    box(5.8 + i * 0.85, 3.25, 62, 0.6, 0.35, 1.0)
cyl(10.6, 3.6, 62.6, 0.5, 1.2, 'x', 14)          # turbocharger
box(10.9, 3.6, 61.4, 1.2, 0.9, 0.9)              # charge air cooler
part('modular-unit-2-generator')
cyl(13.2, 1.8, 62, 1.05, 3.0, 'x', 20)
part('modular-unit-2-radiator')
fin_bank(3.0, 2.3, 62, 3.2, 2.6, 9, 'z', depth=1.5)
part('modular-unit-2-exhaust')
cyl(9.0, 4.9, 62.8, 0.55, 3.6, 'x', 14)          # silencer
pipe([(10.8, 4.9, 62.8), (11.6, 4.9, 62.8), (11.6, 8.6, 62.8)], 0.3)
part('modular-unit-2-scr')
box(6.2, 5.0, 62.8, 2.4, 1.3, 1.3)               # SCR housing

# =========================================== black start (BLACKST)
part('blackstart-2-container')
box(24, 1.75, 62, 9, 2.7, 2.5)
box(24, 3.2, 62, 9.3, 0.2, 2.7)
part('blackstart-2-radiator')
box(28.8, 1.75, 62, 0.6, 2.3, 2.3)
fin_bank(29.3, 1.75, 62, 2.0, 2.0, 6, 'z', depth=0.3)
part('blackstart-2-exhaust')
cyl(21.5, 3.9, 62.8, 0.28, 1.4, 'x', 10)
pipe([(22.2, 3.9, 62.8), (22.8, 3.9, 62.8), (22.8, 6.2, 62.8)], 0.16)
part('blackstart-2-fueltank')
box(24, 0.5, 62, 9, 0.9, 2.5)                    # belly tank

# ================================================ fuel cells (FUELCELL)
part('fuelcell-skid')
box(38, 0.25, 62, 9, 0.5, 4)
for i in range(4):
    part('fuelcell-module-%d' % (i + 1))
    x = 34.8 + i * 2.15
    box(x, 1.75, 62, 1.8, 2.5, 3.2)
    box(x, 3.1, 62, 1.9, 0.2, 3.3)
    box(x, 1.75, 63.7, 1.4, 1.8, 0.15)           # front louvre
part('fuelcell-manifold')
pipe([(34.0, 0.9, 59.8), (42.0, 0.9, 59.8)], 0.12)

# ============================================ fuel cell PCS (FCPCS)
part('fuelcell-inverter')
box(47, 1.3, 62, 3.4, 2.4, 1.8)
box(47, 1.5, 63.05, 2.6, 1.6, 0.2)
part('fuelcell-transformer')
box(51, 1.2, 62, 2.2, 2.0, 1.8)
fin_bank(51, 1.15, 63.15, 1.8, 1.4, 6, 'x', depth=0.45)
part('ELEC-FUELCELL-swgr')
box(54, 1.25, 62, 1.6, 2.2, 1.5)

# ================================================= CCS island (CCS)
part('ccs-pad')
box(88, 0.16, 32, 26, 0.32, 34)
part('ccs-dcc-column')
cyl(79, 9, 16, 2.0, 18, 'y', 26)
platform(79, 13, 16, 2.7)
ladder(81.1, 1, 16, 12)
part('ccs-absorber')
cyl(90, 15, 20, 2.6, 30, 'y', 30)
platform(90, 12, 20, 3.3)
platform(90, 22, 20, 3.3)
ladder(92.7, 1, 20, 21)
cyl(90, 30.6, 20, 1.0, 1.6, 'y', 16)             # top outlet
part('ccs-regen-column')
cyl(99, 12.5, 34, 1.75, 25, 'y', 24)
platform(99, 17, 34, 2.4)
ladder(100.8, 1, 34, 16)
part('ccs-reboiler')
cyl(96, 1.6, 42, 1.1, 6.5, 'x', 18)
frustum(99.4, 1.6, 42, 1.1, 0.7, 0.8, 'x', 18)   # channel head
part('ccs-reflux-drum')
cyl(90, 2.2, 42, 0.8, 3.6, 'x', 14)
part('ccs-interconnect-rack')
for x in (82, 86, 90, 94):
    box(x, 2.6, 28, 0.35, 5.2, 0.35)
box(88, 5.0, 28, 13, 0.3, 0.3)
pipe([(79, 5.4, 18.2), (79, 5.4, 28), (90, 5.4, 28), (90, 5.4, 22.8)], 0.3)
pipe([(90, 4.6, 22.8), (90, 4.6, 28.4), (99, 4.6, 28.4), (99, 4.6, 31.8)], 0.24)

# =================================== CCS fan / pumps (CCSFAN)
part('ccs-flue-fan')
cyl(77, 2.4, 40, 1.9, 1.6, 'z', 24)              # scroll
box(77, 4.6, 40, 1.4, 2.6, 1.5)                  # discharge
frustum(77, 2.4, 38.6, 1.0, 1.3, 1.2, 'z', 18)   # inlet cone
cyl(77, 2.4, 42.1, 0.55, 2.4, 'z', 14)           # motor
box(77, 0.8, 40.8, 4.2, 0.9, 3.2)                # foundation block
part('ccs-pump-1')
cyl(73.5, 0.85, 36.5, 0.32, 1.1, 'x', 12)
cyl(74.6, 0.85, 36.5, 0.42, 0.7, 'x', 12)
box(74.0, 0.35, 36.5, 2.2, 0.35, 0.9)
part('ccs-pump-2')
cyl(73.5, 0.85, 38.3, 0.32, 1.1, 'x', 12)
cyl(74.6, 0.85, 38.3, 0.42, 0.7, 'x', 12)
box(74.0, 0.35, 38.3, 2.2, 0.35, 0.9)
part('ccs-cw-exchanger')
cyl(73.8, 1.5, 41.5, 0.55, 4.2, 'z', 14)

# ================================================ LNG vaporisers (LNGVAP)
part('lng-vaporiser-1')
box(84, 0.25, -18, 6, 0.5, 4)
for gx in range(6):
    for gz in range(3):
        cyl(81.8 + gx * 0.9, 3.2, -19.2 + gz * 1.2, 0.22, 5.6, 'y', 10)
box(84, 6.1, -18, 6.2, 0.25, 4.2)                # top header frame
pipe([(81.2, 6.0, -18), (86.8, 6.0, -18)], 0.14)
pipe([(81.2, 0.7, -18), (86.8, 0.7, -18)], 0.14)

# ============================================ LNG pumps / BOG (LNGPUMP)
part('lng-pump-sump')
box(84, 0.8, -30, 4.5, 1.4, 2.6)
part('lng-pump-1')
cyl(83.0, 2.7, -30, 0.35, 2.2, 'y', 12)
part('lng-pump-2')
cyl(85.0, 2.7, -30, 0.35, 2.2, 'y', 12)
part('lng-bog-compressor')
box(84, 0.9, -34.5, 4.0, 1.0, 2.0)
cyl(82.9, 1.9, -34.5, 0.5, 1.6, 'x', 14)         # compressor
cyl(85.2, 1.9, -34.5, 0.55, 1.8, 'x', 16)        # motor
cyl(84, 2.2, -33.4, 0.45, 1.3, 'y', 12)          # suction drum

# ============================================ H2 compression (H2COMP)
part('h2-compressor-skid')
box(72, 0.4, -45, 7, 0.8, 4)
part('h2-compressor')
box(71.2, 1.6, -45, 2.6, 1.6, 1.8)               # crankcase
cyl(69.2, 1.6, -44.2, 0.4, 1.6, 'x', 12)         # cylinder throw 1
cyl(69.2, 1.6, -45.8, 0.4, 1.6, 'x', 12)         # cylinder throw 2
cyl(69.0, 2.6, -44.2, 0.3, 1.0, 'y', 10)         # pulsation bottles
cyl(69.0, 2.6, -45.8, 0.3, 1.0, 'y', 10)
cyl(74.0, 1.6, -45, 0.65, 2.2, 'x', 16)          # drive motor
part('h2-compressor-cooler')
fin_bank(72, 2.9, -43.2, 2.4, 1.0, 7, 'x', depth=0.8)

# ==================================== gas metering station (METERING)
part('GMS-pad')
box(60, 0.13, 55, 16, 0.26, 10)
for i, z in enumerate((52.5, 55.0)):
    part('GMS-RUN-%d' % (i + 1))
    pipe([(53, 1.1, z), (67, 1.1, z)], 0.24)
    cyl(56.5, 1.1, z, 0.5, 1.6, 'x', 14)         # filter separator
    cyl(60.5, 1.1, z, 0.38, 1.2, 'x', 14)        # meter body
    box(63.5, 1.75, z, 0.5, 1.3, 0.45)           # regulator + actuator
    cyl(63.5, 2.6, z, 0.3, 0.4, 'y', 10)
part('GMS-heater')
cyl(58, 1.3, 58.8, 0.8, 5.0, 'x', 18)            # bath heater shell
box(55.0, 1.3, 58.8, 1.1, 1.1, 1.1)              # burner box
cyl(60.2, 3.4, 58.8, 0.22, 2.6, 'y', 10)         # heater stack

# ===================================== fire & gas detection (FIREGAS)
for i in range(3):
    part('GMS-LEL-post-%d' % (i + 1))
    x = 54 + i * 6
    cyl(x, 1.5, 61.5, 0.05, 3.0, 'y', 8)
    box(x, 2.9, 61.5, 0.28, 0.35, 0.22)          # detector head
part('GMS-GAS-DETECTION-PANEL')
box(66, 1.4, 61.5, 0.9, 1.2, 0.35)
box(66, 0.6, 61.5, 0.15, 1.2, 0.15)              # stand

# ================================================ WWTP (WWTP)
part('WWTP-PACKAGE-plant')
box(-45, 1.25, 42, 9, 2.5, 4)                    # package basins
box(-47.5, 2.55, 42, 3.5, 0.2, 4.2)              # covered section
box(-41.5, 1.35, 40.2, 1.6, 1.8, 0.4)            # blower / panel
part('WWTP-CLARIFIER')
cyl(-45, 0.9, 51, 4.2, 1.8, 'y', 30)             # clarifier wall
cyl(-45, 1.9, 51, 0.25, 2.2, 'y', 10)            # centre column
box(-45, 2.35, 53.1, 0.8, 0.1, 4.4)              # walkway bridge
box(-45, 2.6, 55.1, 0.9, 0.5, 0.6)               # drive

# =========================================== service air (AIR)
part('AIR-package')
box(26.5, 1.1, 7, 2.8, 1.8, 1.8)                 # screw compressor enclosure
box(26.5, 2.1, 7, 2.9, 0.15, 1.9)
part('AIR-receiver')
cyl(29.2, 1.9, 7, 0.6, 3.2, 'y', 16)
frustum(29.2, 3.6, 7, 0.6, 0.2, 0.5, 'y', 16)
part('AIR-dryers')
cyl(31.0, 1.5, 6.4, 0.32, 2.4, 'y', 12)          # desiccant towers
cyl(31.0, 1.5, 7.6, 0.32, 2.4, 'y', 12)
pipe([(31.0, 2.8, 6.4), (31.0, 3.1, 7.0), (31.0, 2.8, 7.6)], 0.08)

# ================================================================= write GLB
bin_parts = []
accessors, bufviews, meshes, nodes = [], [], [], []
off = 0
tris = 0
for i, (name, v, f) in enumerate(parts):
    pos = b''.join(struct.pack('<3f', *p) for p in v)
    idx = b''.join(struct.pack('<I', k) for t in f for k in t)
    xs = [p[0] for p in v]; ys = [p[1] for p in v]; zs = [p[2] for p in v]
    bufviews.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(pos)})
    accessors.append({'bufferView': len(bufviews) - 1, 'componentType': 5126,
                      'count': len(v), 'type': 'VEC3',
                      'min': [min(xs), min(ys), min(zs)],
                      'max': [max(xs), max(ys), max(zs)]})
    off += len(pos)
    bufviews.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(idx)})
    accessors.append({'bufferView': len(bufviews) - 1, 'componentType': 5125,
                      'count': len(f) * 3, 'type': 'SCALAR'})
    off += len(idx)
    bin_parts += [pos, idx]
    meshes.append({'primitives': [{'attributes': {'POSITION': len(accessors) - 2},
                                   'indices': len(accessors) - 1}]})
    nodes.append({'name': name, 'mesh': i})
    tris += len(f)

blob = b''.join(bin_parts)
doc = {'asset': {'version': '2.0'}, 'scene': 0,
       'scenes': [{'nodes': list(range(len(nodes)))}],
       'nodes': nodes, 'meshes': meshes,
       'accessors': accessors, 'bufferViews': bufviews,
       'buffers': [{'byteLength': len(blob)}]}
js = json.dumps(doc).encode()
js += b' ' * ((4 - len(js) % 4) % 4)
blob += b'\0' * ((4 - len(blob) % 4) % 4)
total = 12 + 8 + len(js) + 8 + len(blob)
out = sys.argv[1] if len(sys.argv) > 1 else 'plant.glb'
with open(out, 'wb') as fh:
    fh.write(struct.pack('<III', 0x46546C67, 2, total))
    fh.write(struct.pack('<II', len(js), 0x4E4F534A)); fh.write(js)
    fh.write(struct.pack('<II', len(blob), 0x004E4942)); fh.write(blob)
print('wrote %s: %d bytes, %d parts, %d triangles' % (out, total, len(parts), tris))
