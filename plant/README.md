# SK-3X1 3x1 combined-cycle plant: 3D model

A 3D coordinate model of the plant in **SK-3X1 Drawing Set Rev 14**: three H-class GTs, three HRSGs, one ST, an 80-cell ACC and a 230 kV breaker-and-a-half switchyard. It also includes the optional and adjacent-market systems: carbon capture, BESS, modular and portable power, GT inlet chilling, an LNG satellite and 25 MW of green hydrogen. The model is checked back against the drawing by `verify.py`.

> Conceptual illustration. Not engineered. Not for construction.

## Verification (current build)

| Check | Result |
|---|---|
| Footprints: every filled shape on sheets 01 and 05 matched within 0.6 ft | 211 / 211 |
| Heights on sheet 13 reproduced | 21 / 21 |
| Sheet 09 coordination screen: clearances and hook margins recomputed from the model | 10 / 10 |
| Clashes between parts of different items (34,154 pairs tested) | 0 |
| Parts outside the compound or wrongly below grade | 0 |

The checks corrected the model in several places:

- **GT combustor cans** poked above the EL 38 envelope, which cut the GT hook margin to 9.7 ft instead of the 11 ft on sheet 09.
- **ACC steam riser** went up through the fans. It now runs under the deck and rises at the street ends.
- **ST exhaust duct** clashed with the ST aux skid.
- **Hoist beam** stood above the filter-house top.
- **Three shapes were misread:** the filter-house stair tower, the hoist landing with truck access, and the gallery-door forklift apron (all identified from sheet 10).

## Files

| File | What it is |
|---|---|
| `build_model.py` | Model source: 338 register items built from about 3,000 parts (boxes, cylinders/cones, A-frames, lofts). Writes `sk3x1_model.json`. |
| `routes_base.json`, `routes_optional.json` | Tray, bus, duct-bank, 230 kV and process-pipe centrelines from the vector geometry of sheets 01 and 02. |
| `extract_reference.py` | Pulls reference geometry from the drawing PDF into `reference/sk3x1_rev14_reference.json` (committed, so the PDF is not needed to verify). |
| `verify.py` | Runs the checks above and writes `verify_report.json`. Exits 1 on failure. |
| `palette.json` | Colour for each material key, shared by the viewer and the OBJ export. |
| `viewer/index.html` | Interactive Three.js viewer: the sheet 11 views, layer toggles, a section cut by elevation, a live X / Y / EL readout, an inspector, the equipment register, a verification report, electrical rooms and the motor schedule. |
| `render.go` | Line art using this repository's `ln` engine, one SVG + PNG per sheet 11 view in `renders/`. |
| `export_obj.py` | Wavefront OBJ + MTL for Blender, SketchUp or Rhino: one group per item, with the layer in the group name. |

## Coordinates and sources

X east, Y north, Z up, in feet. The origin is the SW corner of the 2,420 x 1,920 ft compound.

- **Sheet 01:** the plan frame maps exactly to the compound (3.115 ft per PDF point).
- **Sheet 05:** the R1 plan is rotated, with plant north to the right (4.08 pt per ft). Its switchgear, MCC, P&C, LCI and room layout are modelled as `R1_INTERIOR`.
- **Elevations:** from sheets 09, 12 and 13. Values with no published source (cabinet heights, drum sizes, radiators, gantries, structural steel) are tagged `typical`.

## Layers

Layers follow the collections on sheet SK-3X1-11, so its view definitions map directly. For example, view B hides `R1_ROOF` and `R1_WALL_E` to show `R1_INTERIOR`.

Other collections include `BASE_POWER_BLOCK`, `HALL_ROOF`, `BASE_INLET_AIR`, `BASE_ELECTRICAL`, `R4_INTERIOR`, `BASE_SWITCHYARD`, `SWYD_FUTURE` and `HV_CORRIDOR`. Each optional system has its own layer and route layer: `OPT_CCS`, `OPT_CCSU`, `OPT_BESS`, `OPT_MOD`, `OPT_TMP`, `OPT_IC`, `OPT_LNG` and `OPT_H2`, plus the matching `*_ROUTES` layers.

## Rebuild

```sh
python3 plant/build_model.py        # model JSON
python3 plant/verify.py             # checks -> verify_report.json
python3 plant/build_viewer.py       # viewer/index.html (inlines model, palette, report)
python3 plant/export_obj.py         # OBJ (add --zup or --base as needed)
go run ./plant                      # ln line art for every view -> plant/renders/
go run ./plant -view B              # one view; -list shows the keys
# optional, needs PyMuPDF and the PDF:
python3 plant/extract_reference.py SK-3X1_Drawing_Set_Rev14.pdf
```
