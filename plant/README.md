# SK-3X1 3x1 combined-cycle plant: 3D model

A 3D coordinate model of the plant in **SK-3X1 Drawing Set Rev 14** (3 x H-class GT, 3 x HRSG, 1 x ST, 80-cell ACC, 230 kV breaker-and-a-half switchyard), including the optional and adjacent-market systems (carbon capture, BESS, modular / portable power, GT inlet chilling, LNG satellite, 25 MW green hydrogen).

> Conceptual illustration. Not engineered. Not for construction.

## Files

| File | What it is |
|---|---|
| `build_model.py` | The model source. Every item, with plan coordinates, elevation, basis and drawing reference. Writes `sk3x1_model.json`. |
| `routes_base.json`, `routes_optional.json` | Cable tray, bus, duct bank, 230 kV and process-pipe centrelines taken from the vector geometry of sheets 01 and 02. |
| `sk3x1_model.json` | The generated model: 840 objects and 293 route polylines, in 23 layers. |
| `viewer/index.html` | Interactive Three.js viewer with layer toggles, the SK-3X1-11 camera views, an inspector, an equipment register, electrical rooms, the motor schedule and the height comparison. |
| `render.go` | Line-art renderer using this repository's `ln` engine. Writes SVG and PNG to `renders/`. |
| `export_obj.py` | Wavefront OBJ + MTL export for Blender, SketchUp, Rhino and similar tools. |
| `renders/*.png` | Line-art views: overview, power block, ACC / pumps, carbon capture. |

## Coordinates

X east, Y north, Z up, in feet. The origin is the SW corner of the 2,420 x 1,920 ft compound. In sheet 01, the drawing frame maps exactly to the compound at 3.115 ft per PDF point, so every footprint lands on the round-foot coordinates of the original model. For example, the turbine hall is x 480–1100, y 370–560, the ACC is x 1130–1450, y 380–780, and R1 is x 410–474, y 600–780.

Elevations come from SK-3X1-09 (hall section), SK-3X1-12 (dimension review) and SK-3X1-13 (height comparison): the turbine deck is EL 20, the hall roof EL 101, filter houses EL 100–135, HRSGs EL 100, HRSG stacks 180 ft, the ACC fan deck EL 90 with its top at 125 ft, and the CCS absorbers 262 ft with stacks to 313 ft. Items with no published height are tagged `typical`.

## Rebuild

```sh
python3 plant/build_model.py      # model JSON
python3 plant/build_viewer.py     # viewer/index.html (inlines the JSON)
python3 plant/export_obj.py       # OBJ, Y-up (add --zup or --base as needed)
go run ./plant                    # ln line art -> plant/renders/
go run ./plant -view powerblock -opt
```

## Layers

`SITE`, `BASE_POWER_BLOCK`, `BASE_INLET_AIR`, `BASE_ACC`, `BASE_ELECTRICAL`, `BASE_UTILITIES`, `BASE_SWITCHYARD`, `BASE_SERVICES`, `BASE_WATER`, `BASE_FUEL`, `ADJ_MR`, `ROUTES_BASE`, `PROCESS_PIPING`, and the optional layers `OPT_CCS`, `OPT_CCSU`, `OPT_BESS`, `OPT_MOD`, `OPT_TMP`, `OPT_IC`, `OPT_LNG`, `OPT_H2`, `OPT_D6`, `OPT_ROUTES`. These follow the collection names on sheet SK-3X1-11.

## Simplifications

- Equipment is modelled as boxes, cylinders and A-frame prisms.
- HRSG internals, the bridge crane, IPB phases, pipe sizes and conductor bundles are not modelled.
- Rack bents, ACC columns, filter-house frames and stair towers are representative.
- Some small items on sheets 01 and 02 are not labelled on the drawing. Their names were inferred from the equipment keys on sheets 03 and 14 and are marked "(as drawn)" where the drawing gives no label.
