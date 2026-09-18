#!/usr/bin/env python3
"""Build: dist/index.html (plant-first app), dist/pdf-main.html (8 photo-led spreads), dist/pdf-appendix.html (technical)."""
import json, os, html as H, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else os.path.join(HERE, 'dist'); os.makedirs(OUT, exist_ok=True)
D = json.load(open(os.path.join(HERE, 'data.json')))
FONTS = open(os.path.join(HERE, 'fonts', 'fonts-inline.css')).read()
FAM = {f['id']: f for f in D['families']}; CAT = {c['stock']: c for c in D['catalog']}
e = H.escape; pad = lambda n: f'{n:02d}'

tpl = open(os.path.join(HERE, 'template.html')).read()
open(os.path.join(OUT, 'index.html'), 'w').write(tpl.replace('{{FONTS}}', FONTS).replace('{{DATA}}', json.dumps(D).replace('</', '<\\/')).replace('{{REVIEW_MAILTO}}', D['reviewMailto']))

CSS = FONTS + '''
:root{--ink:#1b2430;--ink2:#414b58;--ink3:#6b7480;--line:#d9d7d2;--accent:#b8723c;--sans:"Inter","Helvetica Neue",Helvetica,Arial,sans-serif;--mono:"Inter","Helvetica Neue",Arial,sans-serif}
.k,.hd .pg,.ft,th,td.st,.zp .t b,.cols .refs,.cases .k,.who .k{letter-spacing:.02em}
.hd .pg,.k{text-transform:uppercase;letter-spacing:.14em;font-weight:600;font-size:11px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
a{color:var(--accent);text-decoration:none}
.page{position:relative;width:1440px;height:900px;overflow:hidden;background:#fff;page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.hd{position:absolute;left:64px;right:64px;top:34px;display:flex;justify-content:space-between;align-items:center}
.hd .wm img{height:36px;width:auto}.hd .wm .l{display:none}.dark .hd .wm .l{display:block}.dark .hd .wm .d{display:none}
.hd .pg{font-family:var(--mono);font-size:12px;color:var(--ink3)}
.ft{position:absolute;left:64px;right:64px;bottom:32px;display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:11.5px;color:var(--ink3)}
.ft a{color:var(--accent)}
.h{position:absolute;left:64px;top:104px;width:1312px;font-weight:300;font-size:60px;letter-spacing:-.03em;line-height:1;white-space:nowrap}
.lede{position:absolute;left:64px;top:184px;width:760px;font-size:19px;line-height:1.45;color:var(--ink2);font-weight:300}
.body{position:absolute;left:64px;top:262px;width:1312px;height:560px}
.k{font-family:var(--mono);font-size:11.5px;color:var(--ink3)}
.s{font-size:12.5px;line-height:1.4;color:var(--ink3)}
.cap{position:absolute;left:64px;bottom:60px;width:820px;font-size:12px;color:var(--ink3)}
img{display:block}
.dark{background:#0b0d10;color:#fff}
.dark .hd .wm{color:#fff}.dark .hd .pg,.dark .ft{color:#aab2bd}
/* cover */
.cover .bg{position:absolute;inset:0;width:1440px;height:900px;object-fit:cover;object-position:62% 50%}
.cover .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,13,16,.05) 30%,rgba(11,13,16,.55) 70%,rgba(11,13,16,.9) 100%)}
.cover .t{position:absolute;left:64px;bottom:150px;width:1000px}
.cover .t .k{color:#aab2bd;margin-bottom:16px;display:block}
.cover h1{font-size:118px;font-weight:300;letter-spacing:-.035em;line-height:.96;color:#fff}
.cover p{margin-top:20px;font-size:21px;color:#d7dce3;max-width:46ch}
.cover .chip{position:absolute;right:64px;bottom:150px;border:1px solid rgba(255,255,255,.85);color:#fff;font-weight:400;font-size:15px;padding:14px 22px;text-decoration:none}
/* photo pages */
.photo{position:absolute;left:64px;top:262px;width:820px;height:540px;object-fit:cover}
.photo.contain{object-fit:contain;background:#0b0d10}
.side{position:absolute;left:928px;top:262px;width:448px;height:560px;display:grid;align-content:start;gap:12px}
.zl{display:grid;grid-template-columns:32px 1fr;align-items:center;font-size:13.5px;color:var(--ink2);padding:5px 0;border-bottom:1px solid var(--line)}
.zl b{font-family:var(--mono);font-weight:500;font-size:11.5px;color:var(--ink3)}
.row{display:grid;grid-template-columns:150px 1fr;gap:6px 18px;padding:12px 0;border-bottom:1px solid var(--line)}
.row .k{padding-top:3px}
.row h4{font-size:16px;font-weight:600;margin-bottom:2px}
.row p{font-size:13px;color:var(--ink2);line-height:1.4}
.row .ln{font-size:12.5px;margin-top:3px}
.row .ln a{margin-right:12px}
.pin{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:rgba(255,255,255,.94);color:var(--ink);font-family:var(--mono);font-size:11px;line-height:26px;text-align:center;box-shadow:0 0 0 1px rgba(0,0,0,.3)}
.pin.core{background:var(--accent);color:#fff}
.cols{display:grid;grid-template-columns:repeat(4,1fr);gap:0 28px}
.cols>div{border-top:2px solid var(--ink);padding-top:14px}
.cols .k{display:block;margin-bottom:8px}
.cols h4{font-size:19px;font-weight:600;margin-bottom:8px;letter-spacing:-.01em}
.cols p{font-size:13.5px;color:var(--ink2);line-height:1.42}
.cols .refs{margin-top:10px;font-family:var(--mono);font-size:11.5px;line-height:1.7;color:var(--ink2)}
.cols .refs a{margin-right:8px;white-space:nowrap}
.cases{display:grid;grid-template-columns:repeat(3,1fr);gap:0 36px}
.cases>div{border-top:2px solid var(--ink);padding-top:16px}
.cases .stat{font-size:64px;font-weight:300;letter-spacing:-.04em;line-height:1;margin:12px 0 10px}
.cases h4{font-size:19px;font-weight:600;margin-bottom:10px}
.cases p{font-size:13.5px;color:var(--ink2);line-height:1.42;margin-bottom:8px}
.cases p b{color:var(--ink);font-weight:600}
.contact .big{font-size:38px;font-weight:300;letter-spacing:-.025em;line-height:1.1;max-width:20ch}
.who{margin-top:34px;display:grid;gap:18px}
.who .k{display:block;margin-bottom:4px}
.who a{font-size:24px;font-weight:300;letter-spacing:-.02em;color:var(--ink);border-bottom:1px solid var(--line)}
.who span{display:block;color:var(--ink3);font-size:13.5px}
.chipbtn{display:inline-block;margin-top:34px;background:var(--ink);color:#fff;font-weight:500;font-size:15px;padding:15px 24px}
/* appendix */
.zp{display:grid;grid-template-columns:1fr 1fr;gap:20px 40px}
.zp>div{border-top:1px solid var(--line);padding-top:10px}
.zp .t{display:flex;gap:12px;align-items:baseline;margin-bottom:4px}
.zp .t b{font-family:var(--mono);font-weight:500;font-size:12px;color:var(--ink3)}
.zp .t span{font-size:22px;font-weight:300;letter-spacing:-.01em}
.zp .pk{font-weight:600;font-size:13px;margin-bottom:5px}
.zp p{font-size:12.5px;line-height:1.4;color:var(--ink2);margin-bottom:3px}
.zp p b{color:var(--ink);font-weight:600}
.zp .refs{font-size:12.5px;margin-top:3px}
.zp .refs a{margin-right:8px}
table{border-collapse:collapse;width:1312px;table-layout:fixed;font-size:12.5px}
th,td{text-align:left;vertical-align:top;padding:6px 10px 6px 0;border-bottom:1px solid var(--line);line-height:1.35;color:var(--ink2)}
th{font-family:var(--mono);font-weight:500;font-size:11.5px;color:var(--ink3);border-bottom:1px solid var(--ink)}
td.st{color:var(--ink);font-family:var(--mono);font-size:12px}
td .note{display:block;font-size:11.5px;color:var(--ink3);font-family:var(--sans)}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:18px 40px}
.g2>div{border-top:1px solid var(--line);padding-top:12px}
.g2 h4{font-size:19px;font-weight:600;margin-bottom:6px}
.g2 p{font-size:13px;color:var(--ink2);line-height:1.42;margin-bottom:5px}
.g2 p b{color:var(--ink);font-weight:600}
'''
def hd(dark=False): return '<div class="hd"><div class="wm"><img class="d" src="assets/logo-dark.png" alt="Southwire"><img class="l" src="assets/logo.png" alt="Southwire"></div><div class="pg">Power Generation Solutions</div></div>'
def ft(label, n): return f'<div class="ft"><span>PowerGen / {e(label)}</span><span><a href="mailto:powergen@southwire.com">powergen@southwire.com</a></span><span>{pad(n)}</span></div>'
def page(cls, label, n, inner): return f'<section class="page {cls}">{hd()}{inner}{ft(label, n)}</section>'
def A(t, u): return f'<a href="{e(u)}">{e(t)}</a>'
def reflink(r):
    c = CAT.get(r); u = c and (c.get('specUrl') or c.get('productUrl'))
    return A(r, u) if u else e(r)
def doc(title, pages_html): return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(title)}</title><style>{CSS}</style></head><body>{"".join(pages_html)}</body></html>'

P = []
# 1 cover
P.append(page('cover dark', 'Cable, engineering and execution · September 2026', 1, f'''<img class="bg" src="assets/hero-hall.jpg" alt=""><div class="veil"></div>
<div class="t"><span class="k">Power Generation Solutions · the plant model</span><h1>Accelerating<br>Time to Power.</h1><p>Cable, application engineering and project execution, from the generation asset to the grid interface.</p></div>
<a class="chip" href="{e(D['reviewMailto'])}">Start a cable package review</a>'''))
# 2 the plant
pins = ''.join(f'<div class="pin{" core" if z.get("core") else ""}" style="left:{64+820*z["x"]/100:.0f}px;top:{262+540*z["y"]/100:.0f}px">{pad(z["n"])}</div>' for z in D['zones'])
zl = ''.join(f'<div class="zl"><b>{pad(z["n"])}</b><span>{e(z["name"])}</span></div>' for z in D['zones'])
P.append(page('', 'The plant', 2, f'''<div class="h">One plant. Sixteen application zones.</div><div class="lede">Every zone is an equipment package, a cable scope and a buyer. The interactive e-brochure opens each one from the model.</div>
<img class="photo contain" src="assets/plant-zones.jpg" alt="">{pins}<div class="side">{zl}</div>
<div class="cap">Original engineering model. Illustrative; not a validated engineering design or a digital twin. Cable design and quantities follow the approved project scope.</div>'''))
# 3 before release
rows = ''.join(f'<div class="row"><div class="k">Zones {" · ".join(pad(z) for z in d["zones"])}</div><div><h4>{e(d["title"])}</h4><p>{e(d["release"])}</p></div></div>' for d in D['zoneDecisions'])
P.append(page('', 'Before release', 3, f'''<div class="h">What has to be settled before the cable is released.</div><div class="lede">Eight decisions, drawn from the zone framework. Zone numbers follow the model.</div>
<div class="body" style="top:250px;height:580px;columns:2;column-gap:40px">{rows}</div>'''))
# 4 families
def fam(f):
    core = [c for c in D['catalog'] if c['family']==f['id'] and c['tier']=='core']; nx = sum(1 for c in D['catalog'] if c['family']==f['id'] and c['tier']=='expanded')
    return f'<div><span class="k">{len(core)} core · {nx} expanded</span><h4>{e(f["name"])}</h4><p>{e(f["desc"])}</p><div class="refs">{" ".join(reflink(c["stock"]) for c in core)}</div></div>'
fs = D['families']
P.append(page('', 'The cable offering', 4, f'''<div class="h">Seven families. One electrical scope.</div><div class="lede">Published constructions with specification numbers. Stock numbers do not indicate inventory; the technical appendix carries every reference and its manufacturer document.</div>
<div class="body" style="top:292px"><div class="cols">{''.join(fam(f) for f in fs[:4])}</div><div class="cols" style="margin-top:26px;grid-template-columns:repeat(3,1fr)">{''.join(fam(f) for f in fs[4:])}</div></div>'''))
# 5 execution
svc = ''.join(f'<div class="row" style="grid-template-columns:110px 1fr;padding:9px 0"><div class="k">{e(s["phase"])}</div><div><h4 style="font-size:15px">{e(s["name"])}</h4><p style="font-size:12.5px">{e(s["desc"])}</p><div class="ln">{" ".join(A(l[0],l[1]) for l in s["links"])}</div></div></div>' for s in D['services'])
P.append(page('', 'From specification to installation', 5, f'''<div class="h">Make the schedule work in the field.</div><div class="lede">Package the delivery around the installation sequence: reel lengths, circuit identification, staged issue.</div>
<img class="photo" src="assets/reel-yard.jpg" alt="" style="width:600px"><div class="side" style="left:708px;width:668px;gap:0">{svc}</div>
<div class="cap">Reel staging and prefab, zone 03. Staging adds no circuit footage; it changes when and how the footage is issued.</div>'''))
# 6 applications
apps = ''.join(f'<div class="row" style="grid-template-columns:120px 1fr;padding:7px 0;gap:4px 14px"><div class="k">{e(a["k"])}</div><div><h4 style="font-size:14px">{e(a["name"])}</h4><p style="font-size:12px;line-height:1.35">{e(a["desc"])}</p></div></div>' for a in D['applications'])
hv = [c for c in D['cases'] if c['id'] in ('vineyard','atlantic')]
gridcols = ''.join(f'<div><h4 style="font-size:15px;font-weight:600;margin-bottom:5px">{e(g["name"])}</h4><p style="font-size:12.5px;line-height:1.4;color:var(--ink2)">{e(g["desc"])}</p><div class="ln" style="font-size:12.5px;margin-top:6px">{" &nbsp;·&nbsp; ".join(A(l[0],l[1]) for l in g["links"])}</div></div>' for g in D['grid'])
hvcol = '<div>' + ''.join(f'<div style="display:grid;grid-template-columns:132px 1fr;gap:10px;align-items:baseline;margin-bottom:8px"><span style="font-size:26px;font-weight:300;letter-spacing:-.03em">{e(c["stat"])}</span><span style="font-size:12px;color:var(--ink2);line-height:1.35">{e(c["title"])} {A("Case study · PDF", c["url"])}</span></div>' for c in hv) + '</div>'
P.append(page('', 'Beyond one plant configuration · plant to grid', 6, f'''<div class="h">Build the package around the application.</div><div class="lede">The combined-cycle model is a starting point. Adapt scope to the generation technology, site and operating duty.</div>
<img class="photo" src="assets/plant-white.jpg" alt="" style="width:600px;height:330px;object-fit:cover;background:#fff;border:1px solid var(--line)"><div class="side" style="left:708px;width:668px;height:330px;gap:0">{apps}</div>
<div style="position:absolute;left:64px;top:622px;width:1312px;border-top:2px solid var(--ink);padding-top:14px"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:24px"><div><span class="k" style="display:block;margin-bottom:6px">Zone 01 · Plant to grid</span><h4 style="font-size:24px;font-weight:300;letter-spacing:-.02em">{e(D["gridIntro"]["title"])}</h4></div><p style="font-size:12.5px;color:var(--ink2);max-width:560px;line-height:1.4">{e(D["gridIntro"]["desc"])}</p></div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0 36px;margin-top:14px">{gridcols}{hvcol}</div></div>'''))
# 7 cases
cs = ''.join(f'<div><span class="k">{e(c["tag"])}</span><div class="stat">{e(c["stat"])}</div><h4>{e(c["title"])}</h4><p><b>Result.</b> {e(c["result"])}</p><p><b>PowerGen use, proposed.</b> {e(c["powergen"])}</p><p>{A("Case study · PDF", c["url"])}</p></div>' for c in D['cases'] if c['featured'])
more = [c for c in D['cases'] if not c['featured']]
P.append(page('', 'Documented experience', 7, f'''<div class="h">Results with a reference.</div><div class="lede">Historical Southwire projects with their published sources. The PowerGen use is proposed, not an outcome from the illustrated plant.</div>
<div class="body" style="top:250px"><div class="cases">{cs}</div><p class="s" style="margin-top:28px">More: {" · ".join(A(c["tag"]+" ("+c["stat"]+")", c["url"]) for c in more)}.</p></div>'''))
# 8 contact
who = ''.join(f'<div><span class="k">{e(c.get("org") or c["name"])}</span><a href="mailto:{c["email"]}">{e(c["email"])}</a>{"<span>"+e(c["role"])+"</span>" if c.get("role") else ""}</div>' for c in D['contacts'])
chk = ''.join(f'<div class="row"><div class="k">{pad(i+1)}</div><div><h4>{e(t)}</h4><p>{e(d)}</p></div></div>' for i,(t,d) in enumerate(D['checklist']))
P.append(page('contact', 'Project review and contact', 8, f'''<div class="h">Connect your next power project.</div>
<div class="body" style="top:200px"><div style="display:grid;grid-template-columns:600px 640px;column-gap:72px"><div><div class="big">Start with the one-line diagram, the cable schedule, the equipment interfaces and the target energization date.</div><div class="who">{who}</div><a class="chipbtn" href="{e(D['reviewMailto'])}">Start a cable package review</a></div><div>{chk}</div></div></div>
<div class="cap">{e(D['sourceNote'])}</div>'''))
open(os.path.join(OUT, 'pdf-main.html'), 'w').write(doc('Accelerating Time to Power', P))

# ---------- appendix ----------
def zone_block(z):
    refs = ' '.join(reflink(r) for r in z['refs']) or '<span class="s">Services and staging scope</span>'
    return f'<div><div class="t"><b>{pad(z["n"])}</b><span>{e(z["name"])}</span></div><div class="pk">{e(z["package"])}</div><p>{e(z["cable"])}</p><p><b>Package focus:</b> {e(z["focus"])}</p><p><b>Specifies &amp; buys:</b> {e(z["buys"])}</p><div class="refs"><span class="k" style="margin-right:6px">References</span>{refs}</div></div>'
AP = []; n = 1
AP.append(page('cover dark', 'Technical appendix', n, f'''<img class="bg" src="assets/xray-plant.jpg" alt="" style="object-position:50% 50%"><div class="veil"></div>
<div class="t"><span class="k">Power Generation Solutions · September 2026</span><h1 style="font-size:100px">Technical<br>appendix.</h1><p>Sixteen zone cable packages, zone decisions and the full catalog of published references with manufacturer documents. Stock numbers do not indicate inventory.</p></div>'''))
for i in range(0, 16, 4):
    n += 1
    AP.append(page('', f'Zone packages {pad(i+1)}–{pad(i+4)}', n, f'<div class="h">Applications {pad(i+1)}–{pad(i+4)}. From equipment to scope.</div><div class="body" style="top:190px;height:630px"><div class="zp">{"".join(zone_block(z) for z in D["zones"][i:i+4])}</div></div><div class="cap">Click a stock reference for its technical document. Shared routes and staging do not add circuit footage.</div>'))
for i in range(0, 8, 4):
    n += 1
    cells = ''.join(f'<div><span class="k">Zones {" / ".join(pad(z) for z in d["zones"])} · {e(d["group"])}</span><h4>{e(d["title"])}</h4><p><b>Cables:</b> {e(d["cables"])}</p><p><b>Before release:</b> {e(d["release"])}</p></div>' for d in D['zoneDecisions'][i:i+4])
    AP.append(page('', f'Zone decisions {i//4+1}', n, f'<div class="h">{"Specify the duty. Protect the interface." if i==0 else "Close the gaps between packages."}</div><div class="body" style="top:200px"><div class="g2">{cells}</div></div><div class="cap">Select constructions against actual routes and approved OEM data. The equipment shown does not establish cable size, quantity or a product guarantee.</div>'))
def row(c):
    f = FAM[c['family']]; docs = []
    if c.get('specUrl'): docs.append(A(f'Spec {c["spec"]} · PDF', c['specUrl']))
    elif c.get('spec'): docs.append(f'<span class="note">Spec {e(c["spec"])} · no PDF in source</span>')
    if c.get('productUrl'): docs.append(A('Product page', c['productUrl']))
    for x in c.get('extraUrls', []): docs.append(A(f'Spec {x[0]} · PDF', x[1]))
    if not docs: docs.append('<span class="note">Not published in source</span>')
    CTL = {'base':'Published base code','request':'Request stock code','family':'Product family'}
    extra = (f'<span class="note">{e(c["size"])}</span>' if c.get('size') else '') + (f'<span class="note" style="color:var(--accent)">{CTL[c["codeType"]]}</span>' if c.get('codeType') in CTL else '') + (f'<span class="note">{e(c["note"])}</span>' if c.get('note') else '')
    return f'<tr><td class="st">{e(c["stock"])}{extra}</td><td>{e(f["short"])}{"<span class=note>MC-HL · hazardous location</span>" if c.get("hazloc") else ""}</td><td>{e(c["duty"])}</td><td>{e(c["construction"])}</td><td>{e(c.get("spec") or "—")}</td><td>{"<br>".join(docs)}</td><td>{", ".join(pad(z) for z in c["zones"]) or "—"}</td></tr>'
groups = [('Medium-voltage power', ['mv']), ('Low-voltage, VFD and flexible / DC', ['lv','vfd','dc']), ('Control, instrumentation and protection', ['ci']), ('Grounding, networks, building systems and specialty', ['gnd','sp'])]
for title, fams in groups:
    for tier, tl in (('core','core references'),('expanded','expanded families')):
        rows = [c for c in D['catalog'] if c['family'] in fams and c['tier']==tier]
        if not rows: continue
        chunks = [rows[i:i+10] for i in range(0, len(rows), 10)]
        for ci, ch in enumerate(chunks):
            n += 1; suffix = f' ({ci+1}/{len(chunks)})' if len(chunks)>1 else ''
            AP.append(page('', f'Catalog · {title} · {tl}', n, f'''<div class="h">{e(title)}{suffix}</div><div class="lede">{tl.capitalize()}. Published references connect circuit requirements to specific constructions.</div>
<div class="body" style="top:250px"><table><colgroup><col style="width:190px"><col style="width:120px"><col style="width:190px"><col style="width:380px"><col style="width:90px"><col style="width:200px"><col style="width:142px"></colgroup><thead><tr><th>Stock / reference</th><th>Family</th><th>Duty</th><th>Construction / size</th><th>Spec</th><th>Documents</th><th>Zones</th></tr></thead><tbody>{"".join(row(c) for c in ch)}</tbody></table></div>
<div class="cap">Product family: selected by size and listing · specification number: a construction · published base code: not a complete orderable stock number · stock number: orderable, not inventory · request stock code: size and duty selected with the project.</div>'''))
n += 1
cs2 = ''.join(f'<div><span class="k">{e(c["tag"])}</span><div class="stat">{e(c["stat"])}</div><h4>{e(c["title"])}</h4><p><b>Problem.</b> {e(c["problem"])}</p><p><b>Contribution.</b> {e(c["contribution"])}</p><p><b>Result.</b> {e(c["result"])}</p><p><b>PowerGen use, proposed.</b> {e(c["powergen"])}</p><p>{A("Case study · PDF", c["url"])}</p></div>' for c in more)
AP.append(page('', 'More documented experience', n, f'<div class="h">Additional cases with a reference.</div><div class="body" style="top:200px"><div class="cases">{cs2}</div></div>'))
open(os.path.join(OUT, 'pdf-appendix.html'), 'w').write(doc('PowerGen technical appendix', AP))
print('main', len(P), 'appendix', len(AP))
