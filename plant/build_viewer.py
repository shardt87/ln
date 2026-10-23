#!/usr/bin/env python3
"""Inject the model, palette and verification report into
viewer/template.html -> viewer/index.html.

The coastal variant A (sheet SW-3X1-15: onshore LNG import terminal, jetty,
berth and carrier) is merged in as its own layer group with a sea layer and a
'Coastal: LNG terminal' view; it is off in the other views."""
import json
import os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "viewer", "template.html")).read()
import sys
GENERIC = "--generic" in sys.argv     # unbranded build: supplier wordmarks and livery left off
model = json.load(open(os.path.join(HERE, "sw3x1_model.json")))
if not GENERIC:
    model["decals"] = [d for d in model.get("decals", []) if not d.get("nobrand")]
if GENERIC:
    dd = []
    for d in model.get("decals", []):
        if d.get("brand"):
            continue
        d["lines"] = [l for l in d["lines"] if not l.get("brand")]
        if d["lines"] or d.get("img"):
            dd.append(d)
    model["decals"] = dd
COASTAL = "--no-coastal" not in sys.argv   # the sheet-15 marine LNG import terminal (on unless --no-coastal)
ov = {"items": []}
full = next(v for v in model["views"] if v["k"] == "ALL")
if COASTAL:
    ov = json.load(open(os.path.join(HERE, "coastal", "sw3x1_coastal_A.json")))
    meta = ov["coastal"]
    model["layers"].update(ov["layers"])
    model["layers"]["COASTAL_SEA"] = dict(label="A Sea and shoreline", group="Coastal (sheet 15)")
    model["items"] += ov["items"]
    model["parts"] += ov["parts"]
    model["coastal"] = meta
    coast = [l for l, v in model["layers"].items() if v["group"].startswith("Coastal")]
    model["views"].append(dict(k="COAST", n="Coastal: LNG terminal",
                               show=[l for l in full["show"] if not l.startswith("OPT_LNG")] + coast,
                               t=[1450, 2900, 20], c=[3900, 100, 3100]))
model["views"].append(dict(k="EVERY", n="Everything: plant + all LNG + BTM data centre" if COASTAL else "Everything: plant, all options and the BTM data centre",
                           show=[l for l in model["layers"] if l not in ("R1_INTERIOR", "R4_INTERIOR", "CR_INTERIOR", "UNDERGROUND",
                                                                         "OPT_UNDERGROUND", "OPT_H2P", "OPT_H2P_ROUTES")],
                           t=[1700, 1800, 20] if COASTAL else [1700, 900, 30],
                           c=[-900, -2600, 4300] if COASTAL else [500, -1700, 2100]))
model["views"].append(dict(k="FUEL", n="Fuel systems: M&R, gas yard, ULSD", show=list(full["show"]),
                           t=[1640, 1660, 4], c=[1330, 1330, 330]))
# every view shows the whole campus (options, BTM campus, coastal terminal), so equipment never drops out when the
# view changes; a view still leaves out the roofs / walls it cuts away, and the underground views keep their own set
ROOFS = {"HALL_ROOF", "R1_ROOF", "R2A_ROOF", "CEMS_ROOF", "BOILER_ROW_ROOF", "R1_WALL_E", "R4_ROOF", "R4_WALL_E", "CR_ROOF", "H2_ROOF"}
FULL = [l for l in model["layers"] if l not in ("R1_INTERIOR", "R4_INTERIOR", "CR_INTERIOR", "UNDERGROUND", "OPT_UNDERGROUND",
                                                "OPT_H2P", "OPT_H2P_ROUTES", "NOBESS_GROUND", "NOMOD_GROUND")]
for v in model["views"]:
    if v["k"] in ("U", "U2"):
        continue
    keep = set(v["show"])
    v["show"] = list(dict.fromkeys(v["show"] + [l for l in FULL if l not in ROOFS or l in keep]))
# screen decals (control-room SCADA / CCTV displays): small JPEG data URIs, one per image
import io, base64 as _b64
try:
    from PIL import Image as _Image
except ImportError:
    _Image = None
model["screens"] = {}
for d in model.get("decals", []):
    n = d.get("img")
    if n and n not in model["screens"]:
        p = os.path.join(HERE, "screens", n)
        fmt = "jpeg"
        if _Image and d.get("print"):                       # printed wall graphic: keep its transparency
            im = _Image.open(p).convert("RGBA")
            im.thumbnail((1024, 1024))
            buf = io.BytesIO()
            im.save(buf, "PNG", optimize=True)
            raw, fmt = buf.getvalue(), "png"
        elif _Image:
            im = _Image.open(p).convert("RGB")
            im.thumbnail((720 if d["w"] > 3 else 480, 405))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=78)
            raw = buf.getvalue()
        else:
            raw = open(p, "rb").read()
            fmt = "png" if p.endswith(".png") else "jpeg"
        model["screens"][n] = "data:image/%s;base64," % fmt + _b64.b64encode(raw).decode()
# the model travels gzip-compressed (base64) and is inflated in the browser with DecompressionStream:
# the page drops from ~12 MB to ~2-3 MB, which mobile viewers load reliably
import base64, gzip
mz = base64.b64encode(gzip.compress(json.dumps(model, separators=(",", ":")).encode(), 9)).decode()
tpl = tpl.replace("const MODEL = /*MODEL_JSON*/null;",
                  "const MODEL = await (async () => { const b = Uint8Array.from(atob(document.getElementById('mz').textContent), c => c.charCodeAt(0));\n"
                  "  const r = new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip')));\n"
                  "  return JSON.parse(await r.text()); })();")
tpl = tpl.replace("<script>\nconst MODEL = await", '<script id="mz" type="text/plain">' + mz + '</script>\n<script>\n(async () => {\nconst MODEL = await', 1)
i = tpl.rindex("</script>")
tpl = tpl[:i] + "\nObject.assign(window, {MODEL, goView});\n})().catch(e => { const el = document.getElementById('loading'); if (el) { el.hidden = false; el.textContent = 'Could not load the model: ' + e.message; } });\n" + tpl[i:]
cz = base64.b64encode(gzip.compress(open(os.path.join(HERE, "brochure", "cables_xray.json"), "rb").read(), 9)).decode()
tpl = tpl.replace("const CAB = /*CABLES_JSON*/null;",
                  "const CAB = await (async () => { const b = Uint8Array.from(atob(document.getElementById('cz').textContent), c => c.charCodeAt(0));\n"
                  "  return JSON.parse(await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text()); })();")
tpl = tpl.replace('<script id="mz" type="text/plain">', '<script id="cz" type="text/plain">' + cz + '</script>\n<script id="mz" type="text/plain">', 1)
tour = open(os.path.join(HERE, "presentation", "tour.json")).read()
if GENERIC:                                           # unbranded build: generic cable names in the tour captions
    tour = tour.replace("ARMOR-X MC-HL", "MC-HL").replace("ARMOR-X ", "")
tour2 = open(os.path.join(HERE, "presentation", "tour_nov11.json")).read()
if GENERIC:
    tour2 = tour2.replace("ARMOR-X MC-HL", "MC-HL").replace("ARMOR-X ", "")
for key, data in (("TOUR", tour), ("TOUR2", tour2), ("PALETTE", open(os.path.join(HERE, "palette.json")).read()),
                  ("REPORT", open(os.path.join(HERE, "verify_report.json")).read())):
    tpl = tpl.replace(f"/*{key}_JSON*/null", data)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "viewer", "index.html")
open(OUT, "w").write(tpl)
print("wrote", OUT, len(tpl), "bytes;", len(ov["items"]), "coastal items merged")
