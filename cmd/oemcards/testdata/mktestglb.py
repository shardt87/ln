"""Synthetic test GLB in the rev89 schema (pure stdlib): named parts, identity
transforms, metres, y-up. Enough geometry to exercise every rule the oemcards
tool implements: prefixes, crop box, roof drop, below-grade hide, ground
context, occlusion, cylinders (silhouette edges) and boxes (feature edges)."""
import json, math, struct, sys

parts = []  # (name, verts [(x,y,z)], tris [(a,b,c)])

def box(name, cx, cy, cz, sx, sy, sz):
    x0, x1 = cx - sx / 2, cx + sx / 2
    y0, y1 = cy - sy / 2, cy + sy / 2
    z0, z1 = cz - sz / 2, cz + sz / 2
    v = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    # CCW when viewed from outside
    f = [(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
         (3,7,6),(3,6,2),(0,4,7),(0,7,3),(1,2,6),(1,6,5)]
    parts.append((name, v, f))

def cyl(name, cx, cy, cz, r, h, axis='x', n=24):
    """Closed cylinder, length h along axis, centred at (cx,cy,cz)."""
    v, f = [], []
    for e in (-h/2, h/2):
        for i in range(n):
            a = 2*math.pi*i/n
            p, q = r*math.cos(a), r*math.sin(a)
            if axis == 'x': v.append((cx+e, cy+p, cz+q))
            elif axis == 'y': v.append((cx+p, cy+e, cz+q))
            else: v.append((cx+p, cy+q, cz+e))
    for i in range(n):
        j = (i+1) % n
        f += [(i, j, n+j), (i, n+j, n+i)]
    c0, c1 = len(v), len(v)+1
    if axis == 'x': v += [(cx-h/2, cy, cz), (cx+h/2, cy, cz)]
    elif axis == 'y': v += [(cx, cy-h/2, cz), (cx, cy+h/2, cz)]
    else: v += [(cx, cy, cz-h/2), (cx, cy, cz+h/2)]
    for i in range(n):
        j = (i+1) % n
        f += [(c0, j, i), (c1, n+i, n+j)]
    parts.append((name, v, f))

FT = 0.3048
# ground: 120x100 m slab just below grade, plus a road strip
box('site-base', 0, -0.1, 0, 120, 0.2, 100)
box('access-road-north', 0, 0.01, -30, 120, 0.02, 6)
# GT train 01: compressor box + turbine cylinder + exhaust duct
cyl('GTG-01-gas-turbine', 0, 2.2, 0, 2.0, 8, 'x')
box('GTG-01-compressor', -7, 2.0, 0, 6, 3.4, 3.4)
box('GTG-01-exhaust', 6.5, 3.0, 0, 5, 5, 4)
box('GTG-01-skid-pad', 0, 0.15, 0, 20, 0.3, 6)
# GTG-02 generator train, 25 m south
cyl('GTG-02-generator', 0, 2.0, 25, 1.8, 7, 'x')
box('GTG-02-exciter', 5.5, 1.8, 25, 2.5, 2.5, 2.5)
box('GTG-02-terminal-box', -5, 3.2, 26.5, 2, 1.5, 1)
# hall roof over both trains (must vanish on droproof shots)
box('HALL-SECTION-FIXED-ROOF-1', 0, 12.0, 12, 40, 0.4, 45)
box('HALL-FRAME-ROOF-BEAM-1', 0, 11.0, 0, 40, 0.5, 0.5)
box('HALL-FRAME-ROOF-BEAM-2', 0, 11.0, 25, 40, 0.5, 0.5)
# HRSG 40 m east: casing + stack + drums
box('HRSG-2-casing', 45, 8, 12, 12, 16, 10)
cyl('HRSG-2-stack', 53.5, 20, 12, 1.5, 24, 'y')
cyl('HRSG-2-drum-hp', 45, 17.0, 12, 0.9, 9, 'z')
# neighbours that should appear only as context, or not at all
box('WWTP-PACKAGE-TANK', -45, 2, -35, 8, 4, 8)
box('EXCAV-DUCTBANK-1', 10, -1.5, 5, 30, 1, 2)       # below grade: hidden
box('ZONE-LAYDOWN-2', -30, 0.005, 30, 20, 0.01, 20)  # zone: hidden

names = [p[0] for p in parts]
bin_parts = []
accessors, bufviews, meshes, nodes = [], [], [], []
off = 0
for i, (name, v, f) in enumerate(parts):
    pos = b''.join(struct.pack('<3f', *p) for p in v)
    idx = b''.join(struct.pack('<H', k) for t in f for k in t)
    if len(idx) % 4: idx += b'\0\0'
    xs = [p[0] for p in v]; ys = [p[1] for p in v]; zs = [p[2] for p in v]
    bufviews.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(pos)})
    accessors.append({'bufferView': len(bufviews)-1, 'componentType': 5126,
                      'count': len(v), 'type': 'VEC3',
                      'min': [min(xs), min(ys), min(zs)],
                      'max': [max(xs), max(ys), max(zs)]})
    off += len(pos)
    bufviews.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(idx)})
    accessors.append({'bufferView': len(bufviews)-1, 'componentType': 5123,
                      'count': len(f)*3, 'type': 'SCALAR'})
    off += len(idx)
    bin_parts += [pos, idx]
    meshes.append({'primitives': [{'attributes': {'POSITION': len(accessors)-2},
                                   'indices': len(accessors)-1}]})
    nodes.append({'name': name, 'mesh': i})

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
out = sys.argv[1]
with open(out, 'wb') as fh:
    fh.write(struct.pack('<III', 0x46546C67, 2, total))
    fh.write(struct.pack('<II', len(js), 0x4E4F534A)); fh.write(js)
    fh.write(struct.pack('<II', len(blob), 0x004E4942)); fh.write(blob)
print('wrote', out, total, 'bytes,', len(parts), 'parts')
