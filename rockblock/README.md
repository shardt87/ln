# ER-RB Rev 00 — RockBlock campus module

A generic 2.5 MW RockBlock campus module in the SW-3X1 viewer convention. It does two jobs:

1. A leave-behind for the engineering meeting at Enchanted Rock: "we modeled a block from what you showed us, tell us where it's wrong".
2. The instrument for the per-block cable takeoff: units × cable per unit, by voltage layer, rolled up to a campus.

This is a new, separate model. It does not modify SW-3X1, Kilby or WCEC.

Basis: only the Oct 26, 2026 call and the public record. Nothing under NDA, no stock numbers, no dollars. Every number that drives geometry or the takeoff carries a status in `basis.py`: KNOWN, WORKING ASSUMPTION or TO VERIFY.

| File | What it is |
|---|---|
| `basis.py` | Basis register: value, status, statement and source to check for every driving number; layer and key definitions |
| `model.py` | Parametric generator. `layout(mw, n_blocks, blocks_per_group, groups_per_lineup)` builds Unit → Block → Group → Lineup → Campus; `circuits()` routes L1–L7 |
| `takeoff.py` | Per-block kit and campus roll-up. `cut = (routed + risers + terminations + slack) x (1 + spare)`. Writes `out/takeoff_{250,500,1000}MW.csv/.json`. MEASURED and ASSUMED totals are never summed |
| `build_viewer.py` + `viewer/template.html` | Writes `viewer/index.html`: tags, tour, compass, X/Y/EL readout, stamp, K / WA / TV legend, L1–L7 toggles (off by default), X-ray, credit-burned snapshot, takeoff with a basis switch, register |
| `sheets/sheets.py` | SK-2300 set, `out/ER-RB_Rev00_SK-2300.pdf` (+ JPGs): letter landscape, 300 dpi, stated scale plus a graphic bar that agrees |
| `report.py` | One-page assumptions and verification report, `out/ER-RB_Rev00_assumptions.{html,pdf,jpg}` |
| `research/public_record.md` | Public-record notes with source URLs |
| `internal/` | **Internal only.** The 1.2M ft sanity line. Not attached to any named project; not part of the deliverables |

Rebuild:
```
python takeoff.py && python build_viewer.py && python sheets/sheets.py && python report.py
```
