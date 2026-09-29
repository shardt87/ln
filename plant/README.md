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
| `build_model.py` | Model source: 338 register items built from about 3,000 primary parts (boxes, cylinders/cones, A-frames, lofts). Writes `sk3x1_model.json`. |
| `detail.py` | Detail pass (about 9,100 parts). See "Detail layer" below. |
| `routes_base.json`, `routes_optional.json` | Tray, bus, duct-bank, 230 kV and process-pipe centrelines from the vector geometry of sheets 01 and 02. |
| `extract_reference.py` | Pulls reference geometry from the drawing PDF into `reference/sk3x1_rev14_reference.json` (committed, so the PDF is not needed to verify). |
| `verify.py` | Runs the checks above and writes `verify_report.json`. Exits 1 on failure. |
| `palette.json` | Colour for each material key, shared by the viewer and the OBJ export. |
| `viewer/index.html` | Interactive Three.js viewer: physically based materials with procedural textures (ribbed cladding, concrete, gravel, asphalt, grass, grating, fin stripes), a sky with fog, camera-following shadows and a Detail toggle. It also has the sheet 11 views, layer toggles, a section cut by elevation, a live X / Y / EL readout, an inspector, the equipment register, a verification report, electrical rooms and the motor schedule. |
| `threejs/` | GT train 1 bay as compact JSON (`export_bay.py`) and a standalone three.js r181 scene (`gt1_bay_scene.js`, `bay.html`). |
| `site/build_site.py` | Assembles the GitHub Pages site: the viewer, the bay scene and a render gallery. |
| `render.go` | Line art using this repository's `ln` engine, one SVG + PNG per sheet 11 view in `renders/`. |
| `export_obj.py` | Wavefront OBJ + MTL for Blender, SketchUp or Rhino: one group per item, with the layer in the group name. |
| `blender/` | Blender build script (sheet 11), label annotation, contact sheets, render summary and requirements. |
| `renders/blender/` | Annotated Cycles renders and contact sheets. |

## Detail layer

`detail.py` runs after the primary model is built. It adds:

- open stair towers with switchback flights, landings and handrails, in place of solid blocks;
- guard rails on every raised platform and ring platform;
- caged ladders on the stacks, absorbers, strippers and tanks;
- sheds on every bushing and post insulator, and fans under the transformer radiators;
- lattice bracing and shield wires in the switchyard;
- process piping on the rack tiers;
- HRSG side platforms and downcomers;
- doors and louvres, light poles and fence posts.

Detail parts carry `d: 1`. None of them come from the drawing; all are typical. `verify.py` therefore checks the primary geometry against the drawing and runs only the bounds check on the detail parts. In the viewer, the Detail button toggles them.

## GitHub Pages

`.github/workflows/sk3x1-pages.yml` rebuilds and verifies the model, then assembles the site with `plant/site/build_site.py`. The site has the viewer as `index.html`, the GT1 bay close-up as `bay.html`, and a render gallery as `renders.html`.

The workflow always uploads the site as the **sk3x1-site** artifact. It also deploys to GitHub Pages once the repository owner has turned Pages on (Settings → Pages → Build and deployment → Source: GitHub Actions). A workflow token cannot turn Pages on by itself.

## Blender renders (local or GitHub Actions)

`blender/SK-3X1_Rev14_blender_build.py` is the build script named on sheet SK-3X1-11. It:

- builds the model into Blender collections named as on that sheet;
- fits the orthographic 1920 x 1080 cameras to each view with the 3% margin;
- renders with Cycles.

There are two styles:

- **drawing** (the sheet 11 look): white world, neutral grey equipment, copper only on cables, trays and bus, and dark Freestyle outlines.
- **photo:** a Nishita sky, sun shadows and darker real-world albedos.

`blender/annotate.py` then burns in the equipment labels and the credit block, and `blender/contact_sheet.py` tiles the views onto one page.

```sh
pip install -r plant/blender/requirements.txt          # bpy 4.2 (Blender as a Python module) + Pillow
python plant/blender/SK-3X1_Rev14_blender_build.py --views A,B --style drawing --samples 64
python plant/blender/annotate.py plant/renders/blender
# or inside a Blender install:
blender -b -P plant/blender/SK-3X1_Rev14_blender_build.py -- --views A --style photo --blend sk3x1.blend
```

The GitHub workflow `.github/workflows/sk3x1-blender-render.yml` runs in three stages:

1. It runs `verify.py` and fails if the model JSON is stale.
2. It renders all views in five parallel jobs.
3. It publishes an **sk3x1-renders** artifact. That artifact holds the annotated PNGs, contact sheets, `SK-3X1_Rev14.blend` and the OBJ, and each run has a job summary.

It runs on every push that touches `plant/`, and you can also run it by hand. The manual run (Actions → SK-3X1 Blender renders → Run workflow) lets you choose the views, samples and resolution.

Sheet 11 lists ten views, and the render loop was adjusted over several review passes:

| Issue | Fix |
|---|---|
| Framing too wide (view A was 2,108 ft) | Clip the fit set to D1–D3. It is now 1,325 ft; sheet 11 gives 1,438 ft. |
| Coplanar road crossings rendered as black squares | Stagger the road heights. |
| Hidden collections blocked the label visibility rays | Exclude hidden collections instead of hiding them. |
| Freestyle strokes below 1 px vanished | Set strokes to 1.8 px. |
| Collinear tray runs overlapped and rendered black | Merge the runs per tier. |
| Stormwater basin appeared black | Build the ground slab around the basin and recalculate normals. |
| Photo style overexposed | Lower the sky and exposure and use real-world albedos. |

## Professional renders and presentation board

`--style pro` switches the Blender build to a presentation look:

- **Materials** (`blender/pro_look.py`): procedural and physically based, with bevelled edges. They include ribbed metal cladding, broken-up concrete, galvanised steel with varied roughness, gravel, asphalt, porcelain insulators, safety-yellow rails and a see-through chain-link fence.
- **Landscape:** grass, about 550 trees in clusters and windbreak rows, and the public road to the main gate.
- **Light:** a late-afternoon Nishita sky with the sun at 24° altitude, azimuth 258°.
- **Cameras:** six perspective hero cameras (P1–P6) with real lens lengths and subtle depth of field, plus four complete-plant angles (P7 from the north-east, P8 from the south-east, P9 overhead, P10 from the south gate road).
- **Compositor:** haze from the mist pass, fog glow, slight lens dispersion and a warm grade.

`blender/finish_pro.py` adds a smooth vignette, fine grain and the burned-in credit caption. `blender/board.py` composes the presentation board: one sheet, 4800 x 3200 px plus a PDF, with a hairline key plan drawn from the verified model, the view cone of every plate, a sun-angle diagram, scale and north. The board follows the design philosophy in `renders/pro/design-philosophy.md` ("Measured Light"). Fonts are in `blender/fonts` (SIL Open Font License).

```sh
python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --samples 128 --out plant/renders/pro
python plant/blender/finish_pro.py plant/renders/pro
python plant/blender/board.py plant/renders/pro
```

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
