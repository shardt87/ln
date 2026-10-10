"""Brochure v2, cable zones: the zones spread (17 x 11 in) and one page per zone (8.5 x 11 in), as vector HTML printed
to PDF by headless Chromium, in the 'Path of Power' style of brochure_v2.py.

- brochure/zones.json holds the seven zones: name, intro, hero camera, model areas, and the top five products with
  a one-line description and the model location (ft) where each runs.
- Pins on the hero renders are projected from those locations with the same pinhole camera Blender uses
  (eye, target, lens, 36 mm sensor), so each number sits on the equipment it names.
- The campus map is drawn in SVG from the item footprints of sk3x1_model.json, zones tinted by model area.

    python blender/brochure_zones.py        # -> renders/brochure_v2/SW_PathOfPower_zones.pdf + previews
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DECK = os.path.join(HERE, "deck")
OUT = os.path.join(PLANT, "renders", "brochure_v2")
EPIC = os.path.join(PLANT, "renders", "epic")
CHROME = "/opt/pw-browsers/chromium"
url = lambda p: "file://" + os.path.abspath(p)
PX = 96
SW, SH, CW = 17 * PX, 11 * PX, int(8.5 * PX)
COPPER, COPPER_L, INK, WHITE, GREY = "#e39a5f", "#f2b98a", "#0e1012", "#f5f3ef", "#b9bec4"
HALO = 'stroke="#0e1012" stroke-width="3" stroke-opacity=".75" paint-order="stroke" stroke-linejoin="round"'
MODEL = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))
ZONES = json.load(open(os.path.join(PLANT, "brochure", "zones.json")))["zones"]


def cameras():
    """Hero camera definitions from pro_look (read with Blender's Python, which can import it)."""
    cache = os.path.join(OUT, "_cams.json")
    if not os.path.exists(cache) or os.path.getmtime(cache) < os.path.getmtime(os.path.join(HERE, "pro_look.py")):
        py = ("import sys,json;sys.path.insert(0,%r);import pro_look as pl;c={}\n"
              "for L in ('EPIC','HEROES','COASTAL_A'):\n"
              "  for h in getattr(pl,L,[]): c[h['k']]=dict(eye=h['eye'],target=h['target'],lens=h['lens'],"
              "res=h.get('res',(1920,1080)))\n"
              "json.dump(c,open(%r,'w'))") % (HERE, cache)
        bpy_py = os.environ.get("BPY_PYTHON", sys.executable)
        subprocess.run([bpy_py, "-c", py], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return json.load(open(cache))


def project(cam, p):
    sub = lambda a, b: [a[i] - b[i] for i in range(3)]
    dot = lambda a, b: sum(a[i] * b[i] for i in range(3))
    cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    nrm = lambda a: [x / math.sqrt(dot(a, a)) for x in a]
    f = nrm(sub(cam["target"], cam["eye"]))
    r = nrm(cross(f, [0, 0, 1]))
    u = cross(r, f)
    d = sub(p, cam["eye"])
    z = dot(d, f)
    W, H = cam["res"]
    fpx = cam["lens"] / 36.0 * max(W, H)
    return W / 2 + dot(d, r) / z * fpx, H / 2 - dot(d, u) / z * fpx


CSS = f"""
@font-face {{ font-family: BC; src: url({url(os.path.join(DECK, 'BarlowCondensed-Bold.ttf'))}); font-weight: 700; }}
@font-face {{ font-family: BC; src: url({url(os.path.join(DECK, 'BarlowCondensed-ExtraBold.ttf'))}); font-weight: 800; }}
@font-face {{ font-family: B; src: url({url(os.path.join(DECK, 'Barlow-Regular.ttf'))}); font-weight: 400; }}
@page single {{ size: 8.5in 11in; margin: 0; }}
@page spread {{ size: 17in 11in; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ position: relative; overflow: hidden; background: {INK}; break-after: page; }}
.single {{ page: single; width: 8.5in; height: 11in; }}
.spread {{ page: spread; width: 17in; height: 11in; }}
.abs {{ position: absolute; }}
.kicker {{ font: 700 14px/1 BC; letter-spacing: .3em; color: {COPPER}; text-transform: uppercase; }}
.h1 {{ font: 800 84px/.9 BC; color: {WHITE}; text-transform: uppercase; }}
.h1 em {{ font-style: normal; color: {COPPER}; }}
.body {{ font: 400 13.5px/1.55 B; color: {GREY}; }}
.small {{ font: 400 9px/1.4 B; color: #80868c; }}
.zrow {{ break-inside: avoid; display: grid; grid-template-columns: 34px 1fr; column-gap: 8px; padding: 9px 0 10px; border-top: 1px solid #2c3036; }}
.zn {{ font: 800 22px/1 BC; color: {COPPER}; }}
.zt {{ font: 800 17px/1 BC; letter-spacing: .06em; color: {WHITE}; text-transform: uppercase; }}
.zp {{ font: 400 10.5px/1.45 B; color: {GREY}; margin-top: 5px; }}
.zp b {{ font: 700 10.5px/1.45 BC; letter-spacing: .08em; color: {COPPER_L}; margin-right: 5px; }}
.card {{ display: grid; grid-template-columns: 38px 1fr; column-gap: 10px; padding: 11px 0 12px; border-top: 1px solid #2c3036; }}
.cn {{ width: 26px; height: 26px; border-radius: 13px; background: {COPPER}; color: {INK}; font: 800 15px/26px BC;
      text-align: center; }}
.ct {{ font: 800 18px/1.05 BC; letter-spacing: .03em; color: {WHITE}; text-transform: uppercase; }}
.cd {{ font: 400 11.5px/1.45 B; color: {GREY}; margin-top: 4px; }}
"""


def zone_geometry():
    """Per zone: item footprints (for tinting) and a label point (median of item centres)."""
    out = {}
    for z in ZONES:
        fps = [it["fp"] for it in MODEL["items"] if it.get("area") in z["areas"] and it.get("fp") and len(it["fp"]) == 4
               and (it["fp"][1] - it["fp"][0]) < 400 and (it["fp"][3] - it["fp"][2]) < 400 and it["z"][1] > .6]
        xs = sorted((f[0] + f[1]) / 2 for f in fps)
        ys = sorted((f[2] + f[3]) / 2 for f in fps)
        out[z["n"]] = dict(fps=fps, c=(xs[len(xs) // 2], ys[len(ys) // 2]))
    return out


GEO = zone_geometry()
ZCOL = {}


def plan_svg(w, h, hi=None, labels=True, numbers=True):
    """Vector campus plan: compound, roads, every item footprint; zones tinted copper (one zone lit when hi)."""
    x0, x1, y0, y1 = -30, 2450, -40, 1960
    s = min(w / (x1 - x0), h / (y1 - y0))
    ox, oy = (w - (x1 - x0) * s) / 2, (h - (y1 - y0) * s) / 2
    P = lambda x, y: (ox + (x - x0) * s, oy + (y1 - y) * s)
    g = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    a, b = P(0, 1920), P(2420, 0)
    g.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#15181b" '
             f'stroke="#3a3f45" stroke-width="1"/>')
    for it in MODEL["items"]:
        if it["layer"] == "SITE" and "road" in it["name"].lower():
            f = it["fp"]
            a, b = P(f[0], f[3]), P(f[1], f[2])
            g.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#24282c"/>')
    zone_of = {ar: z["n"] for z in ZONES for ar in z["areas"]}
    for it in MODEL["items"]:
        f = it.get("fp")
        if not f or len(f) != 4 or it["layer"] in ("SITE", "UNDERGROUND", "OPT_UNDERGROUND") or "ROUTES" in it["layer"]:
            continue
        if (f[1] - f[0]) > 700 or (f[3] - f[2]) > 700 or it["z"][1] < .6 or f[0] > 2440:
            continue
        zn = zone_of.get(it.get("area"))
        if zn and (hi is None or zn == hi):
            col, op = COPPER, (.85 if hi else .55)
        else:
            col, op = "#5b6168", (.55 if hi else .7)
        a, b = P(f[0], f[3]), P(f[1], f[2])
        g.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{max(.6, b[0] - a[0]):.1f}" height="{max(.6, b[1] - a[1]):.1f}" '
                 f'fill="{col}" fill-opacity="{op}"/>')
    if numbers:
        for z in ZONES:
            if hi and z["n"] != hi:
                continue
            cx, cy = P(*GEO[z["n"]]["c"])
            r = 15 if not hi else 11
            g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{INK}" stroke="{COPPER_L}" stroke-width="2"/>')
            g.append(f'<text x="{cx:.1f}" y="{cy + r * .42:.1f}" text-anchor="middle" font-family="BC" font-weight="800" '
                     f'font-size="{r * 1.15:.0f}" fill="{WHITE}">{z["n"]}</text>')
            if labels:
                right = cx > w * .68
                g.append(f'<text x="{cx - r - 7 if right else cx + r + 7:.1f}" y="{cy + 4:.1f}" '
                         f'text-anchor="{"end" if right else "start"}" font-family="BC" font-weight="700" font-size="12" '
                         f'letter-spacing="1.6" fill="{WHITE}" {HALO}>{z["name"].upper()}</text>')
    n = P(2380, 1880)
    g.append(f'<text x="{n[0]:.1f}" y="{n[1]:.1f}" text-anchor="end" font-family="BC" font-weight="700" font-size="10" '
             f'letter-spacing="2" fill="#80868c">N &#8593;</text>')
    g.append("</svg>")
    return "".join(g)


def short(p):
    return p.replace(", red PVC", "").replace(", black PVC", "")


def zones_spread():
    rows = []
    for z in ZONES:
        prods = "".join(f"<b>{i + 1}</b>{short(p[0])}<br>" for i, p in enumerate(z["products"]))
        rows.append(f'<div class="zrow"><div class="zn">{z["n"]}</div><div><div class="zt">{z["name"]}</div>'
                    f'<div class="zp">{prods}</div></div></div>')
    mw, mh = 960, 780
    return f"""
<section class="page spread">
  <div class="abs kicker" style="left:64px;top:64px">03 &mdash; The cable zones</div>
  <div class="abs h1" style="left:60px;top:92px;font-size:66px">Seven zones.<br><em>One cable partner.</em></div>
  <div class="abs body" style="left:64px;top:236px;width:470px;color:{WHITE}">From the 230 kV switchyard to the
    portable power pad, each part of the campus asks something different of its cable. Here are the seven zones of
    the SK-3X1 campus and the five products that carry each one.</div>
  <div class="abs" style="left:64px;top:336px;width:500px;column-count:2;column-gap:26px">{''.join(rows)}</div>
  <div class="abs" style="left:{SW - 64 - mw}px;top:120px">{plan_svg(mw, mh)}</div>
  <div class="abs small" style="left:{SW - 64 - mw}px;top:{120 + mh + 10}px;width:{mw}px">Campus plan drawn from
    the SK-3X1 3D model: every footprint at true position, zones tinted by model area. Data-centre campus and the
    marine terminal not shown. Products are typical for each application; confirm against current Southwire
    specifications.</div>
  <div class="abs" style="left:64px;right:64px;bottom:40px;border-top:1px solid #3a3f45;padding-top:10px;display:flex;
       justify-content:space-between"><span class="small">SOUTHWIRE &middot; POWER GENERATION SOLUTIONS</span>
       <span class="small">THE PATH OF POWER</span></div>
</section>"""


def zone_page(z, cams, page_no):
    cam = cams[z["cam"]]
    img = os.path.join(EPIC, f"{z['cam']}_pro.png")
    jpg = os.path.join(OUT, "_img", f"{z['cam']}.jpg")
    os.makedirs(os.path.dirname(jpg), exist_ok=True)
    if not os.path.exists(jpg) or os.path.getmtime(jpg) < os.path.getmtime(img):
        from PIL import Image
        Image.open(img).convert("RGB").save(jpg, quality=90, subsampling=0)
    W, H = cam["res"]
    ih = round(CW * H / W)                                   # hero height at full page width
    pins = []
    for i, (name, desc, pt) in enumerate(z["products"]):
        x, y = project(cam, pt)
        x, y = x / W * CW, y / H * ih
        pins.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{COPPER}" stroke="{WHITE}" stroke-width="1.8"/>'
                    f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" font-family="BC" font-weight="800" '
                    f'font-size="14" fill="{INK}">{i + 1}</text>')
    cards = "".join(f'<div class="card"><div class="cn">{i + 1}</div><div><div class="ct">{p[0]}</div>'
                    f'<div class="cd">{p[1]}</div></div></div>' for i, p in enumerate(z["products"]))
    dots = "".join(f'<span style="display:inline-block;width:{22 if q["n"] == z["n"] else 7}px;height:4px;margin-right:5px;'
                   f'background:{COPPER if q["n"] == z["n"] else "#3a3f45"};border-radius:2px"></span>' for q in ZONES)
    return f"""
<section class="page single">
  <img class="abs" src="{url(jpg)}" style="left:0;top:0;width:{CW}px;height:{ih}px;object-fit:cover">
  <div class="abs" style="left:0;top:0;width:{CW}px;height:{ih}px;background:linear-gradient(180deg,rgba(14,16,18,.55) 0%,
       rgba(14,16,18,0) 22%,rgba(14,16,18,0) 70%,rgba(14,16,18,1) 100%)"></div>
  <svg class="abs" style="left:0;top:0" width="{CW}" height="{ih}">{''.join(pins)}</svg>
  <div class="abs kicker" style="left:48px;top:40px;color:{WHITE}">Zone {z["n"]} of 07</div>
  <div class="abs" style="left:48px;top:{ih - 18}px;width:{CW - 96}px">
    <div class="kicker">{z["sub"]}</div>
    <div class="h1" style="font-size:{58 if len(z["name"]) < 20 else 44}px;margin-top:8px">{z["n"]} &nbsp;{z["name"]}</div>
  </div>
  <div class="abs body" style="left:48px;top:{ih + 92}px;width:{CW - 330}px">{z["intro"]}</div>
  <div class="abs" style="left:{CW - 250}px;top:{ih + 86}px;width:202px">{plan_svg(202, 165, hi=z["n"], labels=False)}
    <div class="small" style="margin-top:4px;letter-spacing:.14em">WHERE IN THE CAMPUS</div></div>
  <div class="abs" style="left:48px;top:{ih + 200}px;width:{CW - 330}px">{cards}</div>
  <div class="abs" style="left:48px;right:48px;bottom:36px;display:flex;justify-content:space-between;align-items:center;
       border-top:1px solid #3a3f45;padding-top:10px"><span>{dots}</span>
       <span class="small">TYPICAL PRODUCTS; CONFIRM AGAINST CURRENT SOUTHWIRE SPECIFICATIONS &nbsp;&middot;&nbsp; {page_no:02d}</span></div>
</section>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    cams = cameras()
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + zones_spread() + \
        "".join(zone_page(z, cams, 8 + k) for k, z in enumerate(ZONES)) + "</body></html>"
    hp = os.path.join(OUT, "zones.html")
    open(hp, "w").write(html)
    pdf = os.path.join(OUT, "SW_PathOfPower_zones.pdf")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}", url(hp)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", pdf)


if __name__ == "__main__":
    main()
