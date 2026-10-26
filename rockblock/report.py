"""ER-RB Rev 00 assumptions and verification report: one page, Known / Working assumption / To verify, with the source
to check for each open item. Writes out/ER-RB_Rev00_assumptions.html (then .pdf / .jpg via render_report.js)."""
import html
import os

import basis as BS
import takeoff as TO

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "sheets", "fonts")


def val(v):
    x = v[0]
    if isinstance(x, tuple):
        x = " x ".join(f"{a:g}" for a in x)
    elif isinstance(x, float) and x < 1:
        x = f"{x * 100:g} %"
    return html.escape(f"{x} {v[1]}".strip() if v[1] and not isinstance(v[0], float) or (isinstance(v[0], float) and v[0] >= 1)
                       else str(x))


def main():
    t = {mw: TO.takeoff(mw) for mw in (250, 500, 1000)}
    col = {BS.K: [], BS.WA: [], BS.TV: []}
    ALLOW = ("depth_lv", "depth_mv", "term_lv", "term_mv", "slack", "spare")
    col[BS.WA].append("<li><b>Install allowances (takeoff)</b><span class=v>trench 3 ft (600 V) / 4 ft (35 kV); terminations 3 / 6 ft "
                      "per end; slack 3 %; spare 5 %</span><i>NEC 300.5 / 300.50; ER spec</i></li>")
    for k, v in BS.B.items():
        if k in ALLOW:
            continue
        col[v[2]].append(f"<li><b>{html.escape(v[3])}</b><span class=v>{val(v)}</span><i>{html.escape(v[4])}</i></li>")
    rows = "".join(f"<tr><td>{mw:,} MW</td><td>{x['params']['n_blocks']}</td><td>{x['params']['n_groups']}</td><td>{x['params']['n_lineups']}</td>"
                   f"<td>{next(d for d in x['rollup'] if d['layer'] == 'L1')['conductor_ft']:,}</td>"
                   f"<td>{sum(d['conductor_ft'] for d in x['rollup'] if d['layer'] in ('L3', 'L4')):,}</td>"
                   f"<td>{x['totals']['MEASURED']:,}</td><td>{x['totals']['ASSUMED']:,}</td></tr>" for mw, x in t.items())
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>ER-RB Rev 00 assumptions</title><style>
@font-face{{font-family:B;src:url({FONTS}/Barlow-Regular.ttf)}}
@font-face{{font-family:BC;src:url({FONTS}/BarlowCondensed-Bold.ttf);font-weight:700}}
@font-face{{font-family:BC;src:url({FONTS}/BarlowCondensed-ExtraBold.ttf);font-weight:800}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;width:8.5in;height:11in;background:#0f1113;color:#e7e4de;font:8.8px/1.3 B,Arial,sans-serif;padding:.45in .45in .4in;position:relative;overflow:hidden}}
.k{{font:700 10px/1 BC;letter-spacing:.22em;text-transform:uppercase;color:#e8955c}}
h1{{font:800 30px/1 BC;text-transform:uppercase;margin:6px 0 4px}} h1 em{{font-style:normal;color:#d0743a}}
.sub{{color:#9aa3a8;max-width:7in;margin:0 0 8px}}
.cols{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}}
.col h2{{font:800 14px/1 BC;text-transform:uppercase;margin:0 0 5px;padding:4px 6px;border:1px solid currentColor}}
.K h2{{color:#e7e4de}} .W h2{{color:#e3a21a;border-style:dashed}} .T h2{{color:#ef6a5a;border-style:dotted;border-width:2px}}
ul{{list-style:none;margin:0;padding:0}} li{{padding:2px 0;border-bottom:1px solid #2c3238}}
li b{{display:block;font-weight:400}} li .v{{display:block;font:700 10.5px/1.2 BC;color:#f4f1ec}} li i{{display:block;font-style:normal;color:#9aa3a8;font-size:8.4px}}
.T li .v{{color:#ef6a5a}} .W li .v{{color:#e3a21a}}
table{{width:100%;border-collapse:collapse;margin-top:4px;font-size:9px}} th{{font:700 8.5px BC;letter-spacing:.1em;text-transform:uppercase;color:#9aa3a8;text-align:right;border-bottom:2px solid #d0743a;padding:3px}}
th:first-child,td:first-child{{text-align:left}} td{{text-align:right;padding:3px;border-bottom:1px solid #2c3238;font-variant-numeric:tabular-nums}}
.box{{background:#171a1d;border-left:3px solid #d0743a;padding:5px 9px;margin-top:7px}}
.box h3{{margin:0 0 3px;font:800 12px/1 BC;text-transform:uppercase}}
.foot{{position:absolute;left:.45in;right:.45in;bottom:.25in;display:flex;justify-content:space-between;color:#80868c;font-size:8px;border-top:1px solid #2c3238;padding-top:4px}}
.stamp{{font:700 8.5px BC;letter-spacing:.14em;text-transform:uppercase;color:#e8955c}}
</style></head><body>
<div class=k>{BS.DOC} · RockBlock campus module · assumptions and verification · Oct 26, 2026</div>
<h1>What the model knows, <em>assumes, and needs checked</em></h1>
<p class=sub>Every number that drives the geometry or the takeoff. Sources: the Oct 26, 2026 call and the public record only (ERock S-1/A, 10-Q Q2 2026, ERT500 release, erock.com, PUCT Docket 59076, TCEQ gas-EGU standard permit). Nothing under NDA; no stock numbers; no dollars.</p>
<div class=cols>
<div class="col K"><h2>Known</h2><ul>{''.join(col[BS.K])}</ul></div>
<div class="col W"><h2>Working assumption</h2><ul>{''.join(col[BS.WA])}</ul></div>
<div class="col T"><h2>To verify</h2><ul>{''.join(col[BS.TV])}</ul></div>
</div>
<div class=box><h3>One decision before the numbers go anywhere</h3>Are the ~75 MW feeders from the lineups to the data center ER's cable or the customer's? In this model they are about 35-40 % of the campus 35 kV conductor-ft. The takeoff carries them separately, on the ASSUMED basis, until Cliff answers.</div>
<div class=box><h3>Takeoff, measured off the model (conductor-ft; MEASURED and ASSUMED never summed)</h3>
<table><tr><th>Campus</th><th>Blocks</th><th>Groups</th><th>Lineups</th><th>L1 480 V leads</th><th>L3 + L4 35 kV</th><th>All MEASURED</th><th>ASSUMED (L5)</th></tr>{rows}</table>
<p style="margin:5px 0 0;color:#9aa3a8">cut = (routed + risers + terminations + slack) x (1 + spare); conductor-ft = cut x conductors x runs. Compact generic layout: real campuses with longer home runs will measure higher. Per-block kit: {t[250]['kit_block'] and sum(r['cft'] for r in t[250]['kit_block']):,} conductor-ft (L1, L2, L6, L7).</p></div>
<div class=box><h3>What the call adds for the Southwire story</h3>Aluminium preferred (750 / 500 kcmil at 15 or 35 kV; copper on some jobs); MV size follows system size (1/0, 250, 500); large 480 V volumes; lead time is the main concern; procurement per project, MV now ordered before detailed design. The L1 per-block kit (pre-cut, pre-terminated, labelled, tested) is the kitting value the call described.</div>
<div class=foot><span class=stamp>{BS.STAMP}</span><span>{BS.CREDIT} · {BS.DOC}</span></div>
</body></html>"""
    p = os.path.join(HERE, "out", "ER-RB_Rev00_assumptions.html")
    open(p, "w").write(doc)
    print("wrote", p)


if __name__ == "__main__":
    main()
