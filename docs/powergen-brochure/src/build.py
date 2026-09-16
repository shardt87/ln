#!/usr/bin/env python3
"""Build the PowerGen strategy brochure: index.html (assets relative), express.html (self-contained)."""
import base64, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')

# ---------- fonts ----------
fontcss = open(os.path.join(HERE, 'gfonts-latin.css')).read()
fmap = {}
for line in open(os.path.join(HERE, 'fontmap.txt')):
    url, fn, _ = line.split()
    fmap[url] = fn
def inline_fonts(css):
    for url, fn in fmap.items():
        b = base64.b64encode(open(os.path.join(HERE, fn), 'rb').read()).decode()
        css = css.replace(url, 'data:font/woff2;base64,' + b)
    return css
FONTS_INLINE = inline_fonts(fontcss)

# ---------- chart (PO year) ----------
yrs = ['2026','2027','2028','2029','2030','2031','2032','2033','2034','2035']
gw = [13.2,17.0,20.7,21.2,14.7,9.5,11.1,13.2,14.3,14.9]
named = [97.7,132.6,164.7,156.4,82.5,21.1,11.1,6.2,1.0,0.0]
allow = [0.0,0.0,2.9,13.1,31.3,53.7,76.9,97.1,110.3,115.7]
def chart_svg():
    W,H,L,R,T,B = 820,440,58,10,30,60
    pw,ph,mx = W-L-R, H-T-B, 200
    y = lambda v: T+ph-(v/mx)*ph
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" font-family="Barlow, sans-serif">']
    for v in (0,50,100,150,200):
        col = '#8a8f95' if v==0 else '#2c3034'
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{col}" stroke-width="{1.5 if v==0 else 1}"/>')
        out.append(f'<text x="{L-8}" y="{y(v)+4:.1f}" font-size="12" fill="#9aa0a6" text-anchor="end">${v}M</text>')
    bw = pw/len(yrs); barw = bw*0.6
    for i,yr in enumerate(yrs):
        x = L+bw*i+(bw-barw)/2; tot = named[i]+allow[i]
        if named[i]>0:
            out.append(f'<rect x="{x:.1f}" y="{y(named[i]):.1f}" width="{barw:.1f}" height="{y(0)-y(named[i]):.1f}" fill="#c9803f"/>')
        if allow[i]>0:
            gap = 2 if named[i]>0 else 0
            out.append(f'<rect x="{x:.1f}" y="{y(tot):.1f}" width="{barw:.1f}" height="{y(named[i])-y(tot)-gap:.1f}" fill="#4f93d8"/>')
        out.append(f'<text x="{x+barw/2:.1f}" y="{y(tot)-8:.1f}" font-size="13" font-weight="600" fill="#f1efe9" text-anchor="middle">${round(tot)}M</text>')
        out.append(f'<text x="{x+barw/2:.1f}" y="{H-B+22}" font-size="13" fill="#d8d6cf" text-anchor="middle">{yr}</text>')
        out.append(f'<text x="{x+barw/2:.1f}" y="{H-B+40}" font-size="12" fill="#9aa0a6" text-anchor="middle">{gw[i]} GW</text>')
    out.append(f'<text x="{L}" y="16" font-size="12" fill="#9aa0a6">$M, constant 2026 dollars · GW = PO-year equivalent</text>')
    out.append('</svg>')
    return '\n'.join(out)

# ---------- zones ----------
ZONES = [
 (1,"Switchyard / GSU / grid tie",49.9,87.2),(2,"Battery energy storage",63.6,81.1),(3,"Reel staging / prefab",71.3,68.8),
 (4,"Admin / control room",82.6,54.9),(5,"E-house",70.0,48.1),(6,"HRSG trains & stacks",68.0,38.9),(7,"Turbine hall",57.9,50.3),
 (8,"GT air inlets",43.4,48.9),(9,"MCC / VFD / UPS",43.6,34.3),(10,"Modular power yard",51.9,13.9),(11,"Air-cooled condenser",45.2,76.4),
 (12,"Chillers / cooling towers",23.1,65.6),(13,"Water / wastewater",12.7,49.2),(14,"Carbon capture",37.1,32.0),(15,"Gas metering",37.5,24.6),
 (16,"Shared cable corridor",30.6,57.6)]
CORE = {1,7,9,10,16}
def pins():
    return ''.join(f'<div class="pin{" core" if n in CORE else ""}" style="left:{x}%;top:{y}%">{n:02d}</div>' for n,_,x,y in ZONES)
def zonelist():
    return ''.join(f'<div class="zl"><b>{n:02d}</b><span>{t}</span></div>' for n,t,_,_ in ZONES)

tpl = open(os.path.join(HERE, 'template.html')).read()
html = tpl.replace('{{CHART}}', chart_svg()).replace('{{PINS}}', pins()).replace('{{ZONELIST}}', zonelist())

# index.html: google font link + local fonts fallback (inline @font-face), assets relative
index = html.replace('{{FONTS}}', FONTS_INLINE)
open(os.path.join(HERE, 'index.html'), 'w').write(index)

# express.html: everything inline
def inline_images(h):
    def rep(m):
        p = os.path.join(ASSETS, m.group(1))
        b = base64.b64encode(open(p,'rb').read()).decode()
        return f'data:image/jpeg;base64,{b}'
    return re.sub(r'assets/([a-z0-9\-]+\.jpg)', rep, h)
express = inline_images(index)
express = express[:express.index('<script>')] + '</body>\n</html>\n'
open(os.path.join(HERE, 'express.html'), 'w').write(express)
print('index', len(index)//1024, 'KB; express', len(express)//1024, 'KB')
