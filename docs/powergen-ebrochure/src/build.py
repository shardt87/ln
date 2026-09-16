#!/usr/bin/env python3
"""Build the PowerGen e-brochure package: index.html, pdf-main.html, pdf-appendix.html (paged, 1440x900)."""
import json, os, re, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'dist')
os.makedirs(OUT, exist_ok=True)
D = json.load(open(os.path.join(HERE, 'data.json')))
FONTS = open(os.path.join(HERE, '..', 'fonts', 'fonts-inline.css')).read()
FAM = {f['id']: f for f in D['families']}
CAT = {c['stock']: c for c in D['catalog']}
e = H.escape
pad = lambda n: f'{n:02d}'

# ---------------- e-brochure ----------------
tpl = open(os.path.join(HERE, 'index.template.html')).read()
data_js = json.dumps(D).replace('</', '<\\/')
index = tpl.replace('{{FONTS}}', FONTS).replace('{{DATA}}', data_js).replace('{{REVIEW_MAILTO}}', D['reviewMailto'])
open(os.path.join(OUT, 'index.html'), 'w').write(index)

# ---------------- paged PDF ----------------
CSS = FONTS + '''
:root{--bg:#0f1113;--bg2:#171a1d;--bg3:#1f2327;--line:#2c3034;--line2:#3a3f45;--ink:#f1efe9;--ink2:#c9c8c2;--ink3:#8f949a;--copper:#e0a672;--copper2:#c9803f;
--sans:"Nimbus Sans",Helvetica,Arial,sans-serif;--narrow:"Nimbus Sans Narrow","Arial Narrow",sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000}
body{font-family:var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:var(--copper);text-decoration:underline;text-decoration-color:rgba(224,166,114,.5);text-underline-offset:2px}
.page{position:relative;width:1440px;height:900px;overflow:hidden;background:var(--bg);page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.hd{position:absolute;left:60px;right:60px;top:34px;height:30px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding-bottom:12px}
.hd .wm{font-weight:700;font-size:22px;letter-spacing:.14em}
.hd .pg{font-weight:700;font-size:12px;letter-spacing:.18em;color:var(--ink3)}
.ft{position:absolute;left:60px;right:60px;bottom:30px;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:11.5px;letter-spacing:.14em;color:var(--ink3)}
.ft .n{color:var(--ink2);font-size:14px}
.ft a{color:var(--copper);text-decoration:none}
.eyebrow{position:absolute;left:60px;top:96px;font-weight:700;font-size:12.5px;letter-spacing:.18em;color:var(--copper)}
.h{position:absolute;left:60px;top:118px;width:1320px;white-space:nowrap;font-family:var(--narrow);font-weight:700;font-size:50px;line-height:1;letter-spacing:.005em}
.lede{position:absolute;left:60px;top:184px;width:980px;font-size:18px;line-height:1.45;color:var(--ink2)}
.body{position:absolute;left:60px;top:250px;width:1320px;height:570px}
.k{font-weight:700;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--copper)}
.s{font-size:12.5px;line-height:1.4;color:var(--ink3)}
.cap{position:absolute;left:60px;bottom:66px;width:1320px;font-size:12px;color:var(--ink3)}
.n{font-family:var(--narrow);font-weight:700}
img{display:block}
/* cover */
.cover .bgimg{position:absolute;left:0;top:0;width:1440px;height:900px;object-fit:cover;object-position:60% 50%}
.cover .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,9,10,.96) 0%,rgba(8,9,10,.86) 34%,rgba(8,9,10,.35) 62%,rgba(8,9,10,.15) 100%)}
.cover .shade2{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,9,10,.55) 0%,rgba(8,9,10,0) 25%,rgba(8,9,10,0) 60%,rgba(8,9,10,.92) 100%)}
.cover .hd{border-bottom-color:rgba(255,255,255,.18)}.cover .hd .pg{color:#d8d6cf}
.cover .ey{position:absolute;left:60px;top:190px;font-weight:700;font-size:14px;letter-spacing:.2em;color:var(--copper)}
.cover .title{position:absolute;left:58px;top:220px;font-family:var(--narrow);font-weight:700;font-size:126px;line-height:.92;color:#fff}
.cover .title em{font-style:normal;color:var(--copper)}
.cover .sub{position:absolute;left:60px;top:486px;width:640px;font-size:21px;line-height:1.4;color:#e8e6df}
.cover .chip{position:absolute;left:60px;top:604px;background:var(--copper2);color:#0f1113;font-weight:700;font-size:14px;letter-spacing:.1em;text-transform:uppercase;padding:13px 20px;text-decoration:none}
.cover .meta{position:absolute;left:60px;top:690px;font-size:14px;color:#c9c8c2;letter-spacing:.02em}
.cover .ft{color:#b7b9bc}
/* generic grids */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line)}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line)}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
.cell{background:var(--bg);padding:18px 20px}
.cell.alt{background:var(--bg2)}
.cell h3{font-family:var(--narrow);font-weight:700;font-size:24px;line-height:1.05;margin-bottom:8px}
.cell p{font-size:14px;line-height:1.42;color:var(--ink2)}
.cell p b{color:var(--ink);font-weight:700}
.cell .k{display:block;margin-bottom:6px}
.cell .ln{margin-top:8px;font-size:13px;display:flex;flex-wrap:wrap;gap:4px 14px}
/* map */
.map .body{display:grid;grid-template-columns:900px 380px;column-gap:40px}
.stage{position:relative;width:900px;height:506px;background:#000}
.stage img{width:900px;height:506px;object-fit:contain}
.pin{position:absolute;width:30px;height:30px;margin-left:-15px;margin-top:-15px;border-radius:50%;background:#0f1113;border:2px solid #f1efe9;color:#f1efe9;font-weight:700;font-size:13px;line-height:26px;text-align:center}
.pin.core{background:#c9803f;border-color:#fff;color:#0f1113}
.zl{display:grid;grid-template-columns:34px 1fr;align-items:center;height:31.5px;border-bottom:1px solid var(--line);font-size:14.5px;color:var(--ink2)}
.zl b{font-family:var(--narrow);font-weight:700;font-size:17px;color:var(--copper)}
/* zone packages (appendix) */
.zp{display:grid;grid-template-columns:1fr 1fr;gap:22px 40px}
.zp>div{border-top:1px solid var(--line);padding-top:12px}
.zp .t{display:flex;gap:14px;align-items:baseline;margin-bottom:6px}
.zp .t b{font-family:var(--narrow);font-weight:700;font-size:26px;color:var(--copper)}
.zp .t span{font-family:var(--narrow);font-weight:700;font-size:26px}
.zp .pk{font-weight:700;color:var(--copper);font-size:12.5px;margin-bottom:6px}
.zp p{font-size:12.5px;line-height:1.4;color:var(--ink2);margin-bottom:4px}
.zp p b{color:var(--ink)}
.zp .refs{font-size:12.5px;margin-top:4px}
.zp .refs a{margin-right:8px}
/* families page */
.fams{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line)}
.fams>div{background:var(--bg);padding:16px 18px;display:grid;grid-template-columns:8px 1fr;column-gap:12px;min-height:170px}
.fams i{display:block;width:8px;border-radius:2px}
.fams h3{font-family:var(--narrow);font-weight:700;font-size:21px;line-height:1.05;margin-bottom:6px}
.fams p{font-size:12.5px;line-height:1.4;color:var(--ink2)}
.fams .refs{margin-top:8px;font-size:12px;line-height:1.6}
.fams .refs a{margin-right:8px;white-space:nowrap}
.bounds{margin-top:18px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px 28px;font-size:12.5px;color:var(--ink2);line-height:1.4}
.bounds b{color:var(--ink)}
/* table */
table{border-collapse:collapse;width:1320px;table-layout:fixed;font-size:12.5px}
th,td{text-align:left;vertical-align:top;padding:6px 10px;border-bottom:1px solid var(--line);line-height:1.35;color:var(--ink2)}
th{font-weight:700;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;background:var(--bg3);color:var(--ink)}
td.st{color:var(--ink);font-weight:700}
td .note{display:block;font-size:11.5px;color:var(--ink3)}
td .fm{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px}
/* exec */
.exec .body{display:grid;grid-template-columns:740px 540px;column-gap:40px}
.steps>div{display:grid;grid-template-columns:120px 1fr;column-gap:14px;padding:8px 0;border-bottom:1px solid var(--line)}
.steps .ph{font-weight:700;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--copper);padding-top:5px}
.steps h4{font-family:var(--narrow);font-weight:700;font-size:19px;margin-bottom:2px}
.steps p{font-size:12px;line-height:1.38;color:var(--ink2)}
.steps .ln{font-size:12px;margin-top:3px}
.steps .ln a{margin-right:12px}
.exec img{width:540px;height:304px;object-fit:cover;border:1px solid var(--line)}
.exec .spine{margin-top:14px;padding:14px 16px;border:1px solid var(--line2);background:var(--bg2);font-size:12.5px;line-height:1.4;color:var(--ink2)}
.exec .spine b{color:var(--ink)}
.exec figcaption{font-size:12px;color:var(--ink3);margin-top:8px}
/* cases */
.cases{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line)}
.case{background:var(--bg);padding:20px 20px 22px}
.case .k{display:block;margin-bottom:12px}
.case .stat{font-family:var(--narrow);font-weight:700;font-size:56px;line-height:.95;color:var(--copper)}
.case h3{font-family:var(--narrow);font-weight:700;font-size:26px;line-height:1.05;margin:10px 0 12px}
.case dt{font-weight:700;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin-top:8px}
.case dd{font-size:13px;line-height:1.4;color:var(--ink2)}
.case dd.pg{color:var(--ink)}
.case .src{margin-top:12px;font-size:13px}
/* contact */
.contact .body{display:grid;grid-template-columns:600px 680px;column-gap:40px}
.contact .big{font-family:var(--narrow);font-weight:700;font-size:34px;line-height:1.1}
.contact .who{margin-top:30px;display:grid;gap:16px}
.contact .who b{display:block;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--copper);margin-bottom:4px}
.contact .who a{font-size:20px;text-decoration:none;color:var(--ink)}
.contact .who span{display:block;color:var(--ink3);font-size:13px}
.contact .chip{display:inline-block;margin-top:30px;background:var(--copper2);color:#0f1113;font-weight:700;font-size:14px;letter-spacing:.1em;text-transform:uppercase;padding:13px 20px;text-decoration:none}
.check>div{display:grid;grid-template-columns:44px 1fr;column-gap:12px;padding:13px 0;border-bottom:1px solid var(--line)}
.check .nn{font-family:var(--narrow);font-weight:700;font-size:28px;color:var(--copper);line-height:1}
.check h4{font-family:var(--narrow);font-weight:700;font-size:21px;margin-bottom:3px}
.check p{font-size:13px;line-height:1.4;color:var(--ink2)}
.needs{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
.chain{margin-top:22px}
.chain svg{width:1320px;height:auto;display:block}
.beyond .body{display:grid;grid-template-rows:auto auto;row-gap:20px}
.scope3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px}
.scope3>div{border-left:3px solid var(--copper2);padding:2px 0 2px 14px}
.scope3 b{display:block;font-family:var(--narrow);font-weight:700;font-size:20px;margin-bottom:4px}
.scope3 p{font-size:12.5px;line-height:1.4;color:var(--ink2)}
'''

def hd(): return '<div class="hd"><div class="wm">SOUTHWIRE</div><div class="pg">POWER GENERATION SOLUTIONS</div></div>'
def ft(label, n, link=True):
    l = f'<a href="mailto:powergen@southwire.com">powergen@southwire.com</a>' if link else ''
    return f'<div class="ft"><span>POWERGEN / {e(label)}</span><span>{l}</span><span class="n">{pad(n)}</span></div>'
def page(cls, label, n, inner, links=True):
    return f'<section class="page {cls}">{hd()}{inner}{ft(label, n, links)}</section>'
def A(text, url): return f'<a href="{e(url)}">{e(text)}</a>'
def reflink(r):
    c = CAT.get(r); u = c and (c.get('specUrl') or c.get('productUrl'))
    return A(r, u) if u else e(r)

pages = []
# 1 cover
pages.append(page('cover', 'CABLE, ENGINEERING & EXECUTION · SEPTEMBER 2026', 1, f'''
<img class="bgimg" src="assets/hall-interior.jpg" alt=""><div class="shade"></div><div class="shade2"></div>
<div class="ey">POWER GENERATION SOLUTIONS</div>
<div class="title">Accelerating<br>Time to <em>Power</em><span style="font-size:36px;vertical-align:top;color:#8f949a">™</span></div>
<div class="sub">From the generation asset to the grid interface. Cable products, application support, installation planning and project execution, connected to the plant's electrical scope.</div>
<a class="chip" href="{e(D['reviewMailto'])}">Start a cable package review</a>
<div class="meta">16 application zones &nbsp;/&nbsp; 29 catalog references &nbsp;/&nbsp; 6 documented cases &nbsp;/&nbsp; interactive e-brochure and technical appendix enclosed</div>'''))

# 2 challenge
needs = [('Time to power','Reach the specification before it is frozen, with the plant model, the one-line and the cable schedule in the same conversation.','CableTechSupport application review; Construction Planning Services takeoffs and pull calculations.'),
 ('Installation labor and constructability','Reel lengths, pull sections, circuit identification and staged issue planned around the installation sequence.','Contractor Solutions and SIMpull equipment planning; qualified prefabrication to an agreed engineered scope.'),
 ('Material availability, coordination and traceability','Published constructions with specification numbers, kitting and labels by circuit, reel tracking and staged delivery.','SPEED Services, Project Services, Southwire Reel Tracking System.'),
 ('Reliable operation and lifecycle support','Constructions rated for the duty, and assessment or rejuvenation of existing feeders where a brownfield expansion depends on them.','Field Assessment Services and cable rejuvenation, with published utility results.')]
chain = '''<svg viewBox="0 0 1320 150" xmlns="http://www.w3.org/2000/svg" font-family="Nimbus Sans, Helvetica, Arial, sans-serif">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#8f949a"/></marker></defs>
<g fill="#1f2327" stroke="#3a3f45"><rect x="0" y="20" width="300" height="64"/><rect x="340" y="20" width="300" height="64"/><rect x="680" y="20" width="300" height="64"/><rect x="1020" y="20" width="300" height="64" fill="#2a1f16" stroke="#c9803f"/></g>
<g stroke="#8f949a" stroke-width="2" marker-end="url(#ar)"><path d="M300 52H334"/><path d="M640 52H674"/><path d="M980 52H1014"/></g>
<g font-family="Nimbus Sans Narrow, Arial Narrow, sans-serif" font-weight="700" font-size="23" fill="#f1efe9" text-anchor="middle"><text x="150" y="60">Specification</text><text x="490" y="60">Equipment interfaces</text><text x="830" y="60">Construction sequence</text><text x="1170" y="60">Energization</text></g>
<g font-size="13" fill="#8f949a" text-anchor="middle"><text x="150" y="112">one-line · cable schedule · voltage class</text><text x="490" y="112">OEM terminal boundaries · package scope</text><text x="830" y="112">pull sections · reel plan · kitting</text><text x="1170" y="112">test records · outage and COD dates</text></g>
<g font-size="12" fill="#e0a672" text-anchor="middle" font-weight="700"><text x="150" y="138">CABLETECHSUPPORT</text><text x="490" y="138">APPLICATION REVIEW</text><text x="830" y="138">PLANNING · PROJECT SERVICES</text><text x="1170" y="138">FIELD ASSESSMENT</text></g></svg>'''
pages.append(page('', 'THE ELECTRICAL EXECUTION CHALLENGE', 2, f'''
<div class="eyebrow">01 / THE ELECTRICAL EXECUTION CHALLENGE</div>
<div class="h">Cable is last on every branch and first on the schedule.</div>
<div class="lede">Cable selection, equipment interfaces, construction sequencing and energization are one chain. A spec frozen before the interfaces are agreed, a reel out of sequence, or a drive output on the wrong cable each costs time to power.</div>
<div class="body"><div class="needs">{''.join(f'<div class="cell"><h3>{e(a)}</h3><p>{e(b)}</p><p style="margin-top:8px"><b>Capability:</b> {e(c)}</p></div>' for a,b,c in needs)}</div>
<div class="chain">{chain}</div></div>
<div class="cap">Audience: EPC engineers and procurement teams; generation owners, utilities and independent power producers; OEMs, modular-power companies and equipment packagers.</div>'''))

# 3 plant map
pins = ''.join(f'<div class="pin{" core" if z.get("core") else ""}" style="left:{z["x"]}%;top:{z["y"]}%">{pad(z["n"])}</div>' for z in D['zones'])
zl = ''.join(f'<div class="zl"><b>{pad(z["n"])}</b><span>{e(z["name"])}</span></div>' for z in D['zones'])
pages.append(page('map', 'PLANT APPLICATION MAP', 3, f'''
<div class="eyebrow">02 / EXPLORE THE PLANT</div>
<div class="h">One plant. Sixteen application zones.</div>
<div class="lede">Every zone is an equipment package, a cable scope and a buyer. The interactive e-brochure opens each one with its cable families, products, services and specification links. Copper pins mark the zones most conversations start in.</div>
<div class="body" style="top:250px;height:520px"><div class="stage"><img src="assets/plant-zones.jpg" alt="">{pins}</div><div>{zl}</div></div>
<div class="cap">Concept application map from the original engineering model. Optional systems are shown. Illustrative, not a validated engineering design or digital twin; cable design and quantities follow the approved project scope.</div>'''))

# 4 six key zones
key = [1, 5, 7, 9, 10, 16]
def zone_block(z, short=False):
    refs = ' '.join(reflink(r) for r in z['refs']) or '<span class="s">Services and staging scope</span>'
    fam = ' · '.join(FAM[k]['short'] for k in z['families'])
    return f'''<div><div class="t"><b>{pad(z['n'])}</b><span>{e(z['name'])}</span></div><div class="pk">{e(z['package'])}</div>
<p>{e(z['cable'])}</p><p><b>Package focus:</b> {e(z['focus'])}</p><p><b>Specifies &amp; buys:</b> {e(z['buys'])}</p>
<div class="refs"><span class="k" style="margin-right:6px">References</span>{refs}</div></div>'''
pages.append(page('', 'ZONE PACKAGES · KEY ZONES', 4, f'''
<div class="eyebrow">02 / EXPLORE THE PLANT</div>
<div class="h">From equipment to scope: the six zones that set the package.</div>
<div class="lede">The handoff, the primary distribution, the core, the drives, the modular yard and the corridor that connects them. The other ten zones are in the technical appendix and the e-brochure.</div>
<div class="body" style="top:236px"><div class="zp">{''.join(zone_block(D['zones'][n-1]) for n in key)}</div></div>
<div class="cap">Click a stock reference for its technical document. Shared routes and staging do not add circuit footage.</div>'''))

# 5 families
def fam_cell(f):
    refs = ' '.join(reflink(c['stock']) for c in D['catalog'] if c['family']==f['id'])
    return f'<div><i style="background:{f["color"]}"></i><div><h3>{e(f["name"])}</h3><p>{e(f["desc"])}</p><div class="refs">{refs}</div></div></div>'
bounds = [('OEM internal wiring vs. field interconnection.','The OEM wires inside the package to terminal boxes or local panels; the EPC or installer connects between packages.'),
 ('Fixed wiring vs. portable cable.','DLO and other flexible constructions are portable-cable applications, not substitutes for fixed tray-rated wiring.'),
 ('MV insulation level.','Voltage class, 100% or 133% insulation level and shield type are project selections from the one-line.'),
 ('VFD duty.','Drive-output cable is matched to the drive system; qualify the drive before selecting the cable.'),
 ('Hazardous locations.','ARMOR-X MC-HL constructions, glands and seals follow the area classification and the complete installation.'),
 ('BESS DC vs. solar PV.','RenewaFLEX is approved internal BESS wiring, not a photovoltaic application. Immersion and circuit integrity are separate qualifications.')]
fams7 = D['families']
pages.append(page('', 'THE CABLE OFFERING', 5, f'''
<div class="eyebrow">03 / THE CABLE OFFERING</div>
<div class="h">Seven families cover the plant's electrical scope.</div>
<div class="lede">Published references connect circuit requirements to specific constructions. Stock numbers do not indicate inventory. The full catalog with specifications and documents is in the technical appendix.</div>
<div class="body" style="top:236px"><div class="fams">{''.join(fam_cell(f) for f in fams7[:4])}</div>
<div class="fams" style="border-top:0;grid-template-columns:1fr 1fr 1fr">{''.join(fam_cell(f) for f in fams7[4:])}</div>
<div class="bounds">{''.join(f'<div><b>{e(a)}</b> {e(b)}</div>' for a,b in bounds)}</div></div>'''))

# 6 execution
steps = ''.join(f'<div><div class="ph">{e(s["phase"])}</div><div><h4>{e(s["name"])}</h4><p>{e(s["desc"])}</p><div class="ln">{" ".join(A(l[0],l[1]) for l in s["links"])}</div></div></div>' for s in D['services'])
pages.append(page('exec', 'FROM SPECIFICATION TO INSTALLATION', 6, f'''
<div class="eyebrow">04 / FROM SPECIFICATION TO INSTALLATION</div>
<div class="h">Make the schedule work in the field.</div>
<div class="lede">Coordinate cable, equipment interfaces and the installation sequence before material reaches the jobsite. Package the delivery around the pull sequence: reel lengths, circuit identification, staging.</div>
<div class="body" style="top:240px"><div class="steps">{steps}</div>
<div><img src="assets/reel-yard.jpg" alt=""><div class="s" style="margin-top:8px">Reel staging and prefab, zone 03. Staging adds no circuit footage; it changes when and how the footage is issued.</div>
<div class="spine"><b>Prefabricated cable spine, project development.</b> A factory-built spine needs defined interfaces, a qualified assembly provider and an agreed test plan. Evaluate a pilot using factory labor, field labor, logistics, schedule and total installed cost. Availability and performance are project-specific.</div></div></div>'''))

# 7 beyond + grid
apps = ''.join(f'<div class="cell"><span class="k">{e(a["k"])}</span><h3>{e(a["name"])}</h3><p>{e(a["desc"])}</p><p style="margin-top:8px;font-size:12.5px;color:var(--copper)">Review zone {pad(a["zone"])} · {e(D["zones"][a["zone"]-1]["name"])}</p></div>' for a in D['applications'])
grid = ''.join(f'<div class="cell alt"><h3>{e(g["name"])}</h3><p>{e(g["desc"])}</p><div class="ln">{" ".join(A(l[0],l[1]) for l in g["links"])}</div></div>' for g in D['grid'])
pages.append(page('beyond', 'GENERATION APPLICATIONS · PLANT TO GRID', 7, f'''
<div class="eyebrow">05 / BEYOND ONE PLANT CONFIGURATION</div>
<div class="h">Build the package around the application.</div>
<div class="lede">The combined-cycle model is a starting point. Adapt scope to the generation technology, site and operating duty. Do not combine plant configurations or carry the model's preliminary quantities into procurement.</div>
<div class="body" style="top:236px"><div class="g4">{apps}</div>
<div class="scope3" style="margin-top:22px"><div><b>Generation scope</b><p>Generation assets and the electrical balance of plant, up to the generator step-up transformer. Includes behind-the-meter generation packages wherever they sit.</p></div><div><b>Downstream facility scope</b><p>Campus distribution, UPS, PDU and the consuming infrastructure belong to the facility. Confirm the generation-to-campus handoff at the equipment boundary.</p></div><div><b>Grid interface</b><p>Agree the GSU, point of interconnection, asset owner and route before selecting the connection cable. Underground and overhead need different engineering packages.</p></div></div>
<div class="g2" style="margin-top:22px">{grid}</div></div>'''))

# 8 cases
def case_card(c):
    return f'''<div class="case"><span class="k">{e(c['tag'])}</span><div class="stat">{e(c['stat'])}</div><h3>{e(c['title'])}</h3>
<dt>Customer problem</dt><dd>{e(c['problem'])}</dd><dt>Southwire contribution</dt><dd>{e(c['contribution'])}</dd><dt>Published result</dt><dd>{e(c['result'])}</dd><dt>PowerGen application · proposed</dt><dd class="pg">{e(c['powergen'])}</dd>
<p class="src">{A('Read the case study · PDF', c['url'])}</p></div>'''
feat = [c for c in D['cases'] if c['featured']]
more = [c for c in D['cases'] if not c['featured']]
pages.append(page('', 'DOCUMENTED EXPERIENCE', 8, f'''
<div class="eyebrow">06 / DOCUMENTED EXPERIENCE</div>
<div class="h">Results with a reference.</div>
<div class="lede">Historical Southwire project examples with their published sources. The PowerGen application under each case is a proposed use, not an outcome from the illustrated plant.</div>
<div class="body" style="top:236px"><div class="cases">{''.join(case_card(c) for c in feat)}</div>
<div class="s" style="margin-top:14px">More in the resource library: {' · '.join(A(c["tag"]+" ("+c["stat"]+")", c["url"]) for c in more)}.</div></div>'''))

# 9 contact
who = ''.join(f'<div><b>{e(c.get("org") or c["name"])}</b><a href="mailto:{c["email"]}">{e(c["email"])}</a>{"<span>"+e(c["role"])+"</span>" if c.get("role") else ""}</div>' for c in D['contacts'])
check = ''.join(f'<div><div class="nn">{pad(i+1)}</div><div><h4>{e(t)}</h4><p>{e(d)}</p></div></div>' for i,(t,d) in enumerate(D['checklist']))
pages.append(page('contact', 'PROJECT REVIEW & CONTACT', 9, f'''
<div class="eyebrow">07 / PROJECT CONVERSATION</div>
<div class="h">Connect your next power project.</div>
<div class="body" style="top:200px"><div><div class="big">Start with the one-line diagram, the cable schedule, the equipment interfaces and the target energization date.</div>
<div class="who">{who}</div><a class="chip" href="{e(D['reviewMailto'])}">Start a cable package review</a>
<div class="s" style="margin-top:26px">Interactive e-brochure: explore the plant, the films and the searchable catalog online. Technical appendix: all sixteen zone packages and the full catalog with specification links.</div></div>
<div class="check">{check}</div></div>
<div class="cap">Based on the September 2026 PowerGen strategy update, the PowerGen email brochure and linked Southwire references. Final engineering and commercial terms are project-specific.</div>''', links=False))

def doc(title, pages_html):
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(title)}</title><style>{CSS}</style></head><body>{"".join(pages_html)}</body></html>'
open(os.path.join(OUT, 'pdf-main.html'), 'w').write(doc('Accelerating Time to Power — PowerGen e-brochure', pages))

# ---------------- appendix ----------------
ap = []
n = 1
ap.append(page('cover', 'TECHNICAL APPENDIX', n, f'''
<img class="bgimg" src="assets/xray-plant.jpg" alt="" style="object-position:50% 50%"><div class="shade"></div><div class="shade2"></div>
<div class="ey">POWER GENERATION SOLUTIONS</div>
<div class="title" style="font-size:96px">Technical<br><em>appendix</em></div>
<div class="sub" style="top:440px">Sixteen zone cable packages and the full catalog of published references, with specification numbers and manufacturer documents. Companion to the Accelerating Time to Power e-brochure.</div>
<div class="meta" style="top:560px">Stock numbers do not indicate inventory. Confirm voltage, insulation level, conductor size, installation rating, reel length, listing, pricing and lead time against the project design.</div>'''))
for i in range(0, 16, 4):
    n += 1
    zs = D['zones'][i:i+4]
    ap.append(page('', f'ZONE PACKAGES {pad(i+1)}–{pad(i+4)}', n, f'''
<div class="eyebrow">A / ZONE CABLE PACKAGES</div>
<div class="h">Applications {pad(i+1)}–{pad(i+4)}. From equipment to scope.</div>
<div class="body" style="top:196px;height:620px"><div class="zp">{''.join(zone_block(z) for z in zs)}</div></div>
<div class="cap">Click a stock reference for its technical document. Shared routes and staging do not add circuit footage. Illustrative model; cable design and quantities follow the approved project scope.</div>'''))
# catalog pages by family groups
groups = [('Medium-voltage power', ['mv']), ('Low-voltage, VFD and flexible / DC', ['lv','vfd','dc']), ('Control, instrumentation and protection', ['ci']), ('Grounding, networks, building systems and specialty', ['gnd','sp'])]
def row(c):
    f = FAM[c['family']]
    docs = []
    if c.get('specUrl'): docs.append(A(f'Spec {c["spec"]} · PDF', c['specUrl']))
    elif c.get('spec'): docs.append(f'<span class="note">Spec {e(c["spec"])} · no PDF in source</span>')
    if c.get('productUrl'): docs.append(A('Product page', c['productUrl']))
    for x in c.get('extraUrls', []): docs.append(A(f'Spec {x[0]} · PDF', x[1]))
    if not docs: docs.append('<span class="note">Not published in source</span>')
    note = f'<span class="note">{e(c["note"])}</span>' if c.get('note') else ''
    hz = '<span class="note">MC-HL · hazardous location</span>' if c.get('hazloc') else ''
    zones = ', '.join(pad(z) for z in c['zones']) or '—'
    return f'<tr><td class="st">{e(c["stock"])}{note}</td><td><span class="fm" style="background:{f["color"]}"></span>{e(f["short"])}{hz}</td><td>{e(c["duty"])}</td><td>{e(c["construction"])}</td><td>{e(c.get("spec") or "—")}</td><td>{"<br>".join(docs)}</td><td>{zones}</td></tr>'
for title, fams in groups:
    n += 1
    rows = [c for c in D['catalog'] if c['family'] in fams]
    ap.append(page('', f'CATALOG · {title.upper()}', n, f'''
<div class="eyebrow">B / CABLE CATALOG</div>
<div class="h">{e(title)}</div>
<div class="lede">Published references connect circuit requirements to specific constructions. Stock numbers do not indicate inventory.</div>
<div class="body" style="top:236px"><table><colgroup><col style="width:190px"><col style="width:130px"><col style="width:190px"><col style="width:380px"><col style="width:90px"><col style="width:190px"><col style="width:150px"></colgroup>
<thead><tr><th>Stock # / reference</th><th>Family</th><th>Duty</th><th>Construction / size</th><th>Spec</th><th>Documents</th><th>Zones</th></tr></thead><tbody>{''.join(row(c) for c in rows)}</tbody></table></div>
<div class="cap">Reference types: product family (selected by size and listing) · specification number (a construction) · published base code (not a complete orderable stock number) · stock number (orderable; not inventory) · project-specific engineered selection. Type TC and TC-ER are distinct ratings.</div>'''))
n += 1
ap.append(page('', 'MORE DOCUMENTED EXPERIENCE', n, f'''
<div class="eyebrow">C / DOCUMENTED EXPERIENCE · RESOURCE LIBRARY</div>
<div class="h">Additional cases with a reference.</div>
<div class="lede">Historical Southwire examples. The PowerGen application is a proposed use, not an outcome from the illustrated plant.</div>
<div class="body" style="top:236px"><div class="cases">{''.join(case_card(c) for c in more)}</div></div>''', ))
open(os.path.join(OUT, 'pdf-appendix.html'), 'w').write(doc('PowerGen technical appendix', ap))
print('index', len(index)//1024, 'KB; main pages', len(pages), '; appendix pages', len(ap))
