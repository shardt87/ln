# Assumptions, generic content and what must be checked

Illustrative 3x1 combined-cycle plant, procedural Blender model and 27-page drawing set.
Everything below is either a published maximum design envelope (R), or an explicit generic
modelling assumption (A). Nothing here is an as-built dimension, an OEM outline, or a
vendor general-arrangement drawing. Do not label any of it "OEM-verified".

## 1. Reference basis (dimensions taken from published sources)

| Ref | Source | Used for |
|---|---|---|
| [1] | SSE / AECOM, Keadby 3 Carbon Capture Power Station, Environmental Statement Chapter 4, Table 4.1 (May 2021). Maximum design envelopes. | Turbine hall width and height, HRSG envelope, stack height and diameter, absorber and regenerator (stripper) envelopes. |
| [2] | SSE / AECOM, Keadby 3 drawing set, Document 4.7, elevation sheet 5 of 5, PDF p. 7 (May 2021). | Cross-check of the stack, absorber and regenerator heights. Written dimensions used, the picture was not scaled. |
| [3] | DESNZ, Spalding Energy Expansion, development consent order, condition (10), PDF pp. 10-11 (October 2025). Planning-limit table. | ACC overall envelope 80 x 80 x 36 m and generator transformer envelope 15 x 10 x 10 m. |
| [4] | Uploaded reference "Modular_Gas_to_Power_Yard_Views 4(4).pdf", pp. 6-7. Visual reference only, no dimensions. | Presentation of e-house cabinets, switchgear and feeders (sheet 05); two-tier tray, payout stands, cleats and bonding (sheet 13). |
| [5] | Siemens Energy, SGT-8000H gas turbine series fact sheet: SGT6-8000H 10.5 x 4.3 x 4.3 m, 289 t. | Sanity check that an H-class core fits inside the 110 x 35 x 28 ft train envelope. Not used for any drawn dimension. |
| [6] | California Energy Commission, Otay Mesa Energy Center filings (99-AFC-05): 160 ft HRSG stacks, GEA ACC 295 x 123 x 76 ft. | Cross-check only. The Keadby and Spalding envelopes are taller; the drawing set uses the taller values as instructed. |

Source qualification: [1] and [3] are maximum envelopes from planning documents. Real plants sit
inside them, often well inside. The hall clear span and framing, the ACC fan-deck height and fan
count, all internals, thermal sizing, electrical ratings and safety clearances remain project checks.

## 2. Equipment schedule as modelled (feet, L x W x H unless noted)

| Zone | Package | Modelled envelope | Basis |
|---|---|---|---|
| 1 | Switchyard | 360 x 240 yard, two 230 kV main buses at el. 40, four breaker bays, gen-tie dead-end and grid-exit gantries 60 ft, lightning masts 95 ft, control house, station-service transformer | A (NESC/IEEE 230 kV spacings are generic; breaker-and-a-half not modelled) |
| 1 | GSU transformers x4 | 49.21 x 32.81 x 32.81 each, radiators both sides, HV bushings on top, LV bushings facing the hall, 38 ft fire walls, oil-containment curb | R[3] envelope; internals A |
| 1 | Gen-tie | Take-off gantry 70 ft along the GSU row, one double-circuit lattice line (92 ft towers, 22 ft base) west then north to the switchyard, shield wire | A. Two GSUs share each circuit on the gantry strain buses: an illustrative simplification, not a protection design |
| 1 | Underground HV option | Sealing-end structures at both ends, link boxes, 6 x 4 ft duct bank at -5 to -9 ft, three splice manholes | A. Shown only in the X-ray portion of sheet 04 |
| 2 | BESS | 8 containers 40 x 8 x 9.5 in two rows, each paired with a 24 x 10 x 10 PCS / transformer skid, collector trays, MV switchgear container, one feeder to the e-house | A (ISO 668 container size) |
| 3 | Reels / laydown / prefab | 180 x 110 gravel area, 6 reels dia 8-9 x 6 wide on A-frame payout stands, 40 ft two-tier prefab spine on trestles, cleats at 3 ft, copper bonding jumpers and end caps, crates, site office, spare drums | A, detail per [4] |
| 4 | Admin / control | 100 x 60 x 24, two storeys, glazed strips, raised control-room roof block, canopy, parking, cable entry | A |
| 5 | E-house | 120 x 32 x 14 enclosure on steel with floor at +8, under-floor trays, MV lineup (8 x 3 ft), LV lineup (12 x 2.5 ft), relay panels, UPS and battery rack, DC panel, overhead control tray, roof HVAC, stair | A, detail per [4] |
| 6 | HRSG x3 | 92 transverse x 164 along the gas path x 184 high (150 ft casing, drums and roof-deck frame to 184), inlet and outlet transitions, external columns, three drums, downcomers, stair tower | R[1] envelope. Orientation of the 92 x 164 footprint along the gas path is an assumption; typical horizontal F-class HRSGs are 90-110 ft high |
| 6 | Stacks x3 | dia 26.25 x 278.87, four platform rings, ladder cage, flue take-off damper at el. 50 | R[1,2] |
| 7 | Turbine hall | 600 x 164.04 x 114.83 eave, gable ridge +8, crane rail at 65, columns at 30 ft, roof and south long wall are separate named parts (HALL-ROOF, HALL-WALL-S) with openings built from panels, never booleans | Hall W / H R[1]; length, crane and framing A |
| 7 | GT trains x3 | 110 x 35 x 28 envelope: 15 ft exhaust diffuser, 48 ft enclosure with roof vents, coupling, 42 ft generator, exciter, terminal box, neutral cubicle; GT axes N-S at 130 ft pitch, exhaust north, generator south | A; [5] confirms an H-class core fits |
| 7 | ST train | 140 x 45 x 35: HP, IP, LP casings and generator on a 30 ft tabletop; LP exhaust duct east through the wall | A |
| 7 | Generator connection | Generator leads (flexible links with copper connectors) into three 2.5 ft isophase bus tubes at el. 18 through the south wall to the GSU LV bushings; IPB tap to a unit auxiliary transformer per GT | A; sized for 300 MW class |
| 8 | Inlet filter houses x3 | 60 x 40 x 25 on a support deck at +25, weather hoods both faces, stair tower, plenum and silencer, 14 x 14 duct through the south wall to the compressor inlet | A |
| 9 | MCC / VFD / UPS | 80 x 40 x 16 with two fire-rated partitions (MCC, VFD, UPS/DC rooms), overhead tray, cable entry pit, roof HVAC | A |
| 10 | Modular power yard | 180 x 120: 2 standby + 1 black-start containerised gensets 40 x 12 x 14, 4 fuel-cell modules 20 x 8 x 10 with inverter skids, paralleling switchgear container, fuel-gas skid | A |
| 11 | ACC | 262.47 x 262.47 x 118.11 overall, 8 x 8 fan cells, fan dia 28, fan deck +82, wind wall to 118, A-frame bundles per column row, ridge steam manifolds, main steam duct dia 12 from the ST, condensate tank and pumps, ACC MCC with riser and deck trays and one feeder drop per fan motor | Envelope R[3]; fan count, deck height and internals A |
| 12 | Chillers / towers | 3 chillers 30 x 10 x 12, 4 auxiliary wet-tower cells 24 x 24 x 30, pumps and piping | A. Auxiliary duty only; the ACC is the main condenser |
| 13 | Water treatment | 80 x 50 x 20 building, 2 tanks dia 40 x 30, lined wastewater pond 140 x 90 drawn as a diked basin (the 8 ft depth is a parameter, not drawn, so nothing is below grade), pumps | A |
| 14 | CCS block | DCC dia 35 x 90 (A); absorber 52.49 x 141.08 x 324.80 with outlet to 344.49; regenerator dia 49.21 x 173.88 with reboiler; CO2 compression building 80 x 40 x 24; solvent tank; heat-exchanger skid; flue-gas collector duct dia 14 at el. 50 with booster fan; CO2 export pipe | R[1,2] except DCC and ducting. One representative train; not a proven three-GT capture design |
| 15 | Gas metering | 40 x 25 x 16 house, 2 process-water tanks dia 22 x 28 (non-fuel), pipeline crossing on a pipe bridge over the perimeter road, ESD valve, pig receiver, filter/separators, three meter runs with orifice flanges, pressure-reduction skid, performance heater, fuel-gas header on sleepers to the hall | A |
| - | Outside-fence fuel context | 250 ft strip: pipeline with block-valve station and marker post, LNG vessel dia 18 x 50 on saddles with ambient vaporiser, hydrogen tube module 40 x 8 x 9.5 with compressor, blending skid at the tie-in | A. Alternatives, not a qualified blending system |
| 16 | Cable corridor | 24 ft corridor along the spine road: power tray at +4 (3 ft wide), controls tray at +6 (2 ft), 6 x 3 ft concrete duct bank at -4 with eight conduits and manholes at 200 ft, trays broken at every road crossing where cables dive into the duct bank, MV ring-main kiosks and pad-mount transformers at four laterals, grounding grid at -1.5 ft on a 25 ft pitch with copper risers | A, detail per [4]; grid pitch generic (IEEE 80 design not performed) |

## 3. Site and arrangement decisions

- Site 2000 x 1400 ft inside the fence (the approval plan said 1800 x 1400; it was widened by 200 ft
  so the CCS and gas-metering column fits east of the ACC column without overlaps). Fuel context
  strip 250 ft east of the fence. Roads 24 ft: perimeter, E-W spine at y = 312, four N-S roads,
  gate road at the south-west with a gatehouse.
- Zone order is preserved: west to east, column-major (north to south within a column):
  1-5 west column; 6 HRSG (north), 7 hall, 8 inlets (south) in the power block; 9-10; 11-13; 14-15; 16 is the corridor along the spine road.
- Because the zone order puts the CCS block at the east end, the flue-gas collector runs from the
  stacks north of the ACC along the north road. On a real plant the capture block would sit next
  to the stacks.
- GT axis N-S with the exhaust to the north: HRSGs north of the hall, inlet houses and GSUs south
  of the hall, GSUs directly opposite their generators, IPB straight through the wall. This is a
  common cold-end-drive layout; the actual OEM train orientation must be checked.
- Three HRSGs feed one ST through common HP and hot-reheat headers running between the hall and
  the HRSGs. Cold reheat, LP steam, feedwater and bypass systems are not modelled.
- The ACC is the main condenser. Wet towers and chillers serve auxiliaries (or the CCS block).
- The e-house collects auxiliaries and MV (13.8 kV); it does not carry generator output.
- Voltages: generator 18 kV, MV 13.8 kV, LV 480 V, HV 230 kV. No MW rating and no OEM identity.
- Elevations: pads at +0.2 ft, gravel at 0, roads at +0.1. Pads are 1.5 ft slabs. All equipment
  sits on a pad or on the ground plane; the preflight checks that compact solids do not collide.
- Below-grade items (duct banks, conduits, manhole shafts, cable pits, earth grid, pond liner) are
  flagged `below_grade` and hidden in every view except the X-ray portions of sheets 04 and 12.
- No brand names, logos or model numbers appear anywhere in the model or on the sheets.

## 4. Look, camera and sheet conventions

- +X east, +Y north. Camera azimuth is measured eastward from south (45 deg = from the south-east),
  elevation above the horizon. Overview at 85 mm, details at 55-65 mm; all perspective.
- Overcast look: uniform grey world (#D9D8D5, the page colour), one large-angle sun (25 deg) at low
  strength, ambient-occlusion pass multiplied in the compositor, mist fade of the far ground to
  the page colour, Standard view transform so the page and backdrop match exactly. Cycles,
  384 samples, OpenImageDenoise. No sky, no hard speculars.
- Materials: enclosures #E6E4DF, galvanised steel #9A9C9E, concrete #C9C6BF with a 20 ft
  scored joint grid (procedural brick texture in world metres), asphalt #5A5A58 with a modelled
  centre crack, cable #141414, copper #C8722E only on end caps, connectors, bonding jumpers and
  ground-riser connectors. Insulated pipe #D2D0CB, porcelain #B9BDBE.
- Renders are 5000 x 3550 px. Sheets are 6000 x 4500 px (20 x 15 in at 300 dpi). The render is
  never stretched: a declared band is cropped from the top (`crop_top`, 8-14 %), the camera
  shift keeps the framed subject centred in the remaining band, and the image is scaled to the
  sheet width. The credit line is a camera-parented text object in the render pixels at the
  bottom-left of the full frame, so every crop keeps it.
- Callouts: every ANCHOR-* empty is projected through each camera into callouts.json with
  in-frame and ray-cast visibility flags. The sheet composer places only the callouts listed per
  view, offsets bubbles automatically (or by `dx`, `dy` per callout in views.json), and warns about
  any callout outside the cropped image or occluded.
- Type sizes are given in points at 300 dpi (title 24 pt bold, subtitle 14 pt, legend 11 pt,
  footnote 10 pt). Fonts: DejaVu Sans if present, otherwise Liberation, Arial or Pillow's default.

## 5. What must be checked against real drawings before any reuse beyond illustration

1. GT and generator outlines, train length, inlet and exhaust geometry (OEM GA drawings).
2. HRSG height and length for the selected OEM and pressure levels; stack height from the air
   permit (dispersion modelling), not from another site's envelope.
3. Turbine hall clear span, crane capacity and hook height, laydown bays, roof framing.
4. ACC fan count, fan-deck elevation, street layout and wind-wall height for the site climate.
5. GSU size, fire-wall height and spacing, oil containment, IPB rating and routing, UAT location.
6. Switchyard scheme (breaker-and-a-half vs ring), bus heights, clearances, line-entry angles.
7. Gen-tie circuit count and structure type; the modelled two-GSUs-per-circuit strain bus is a
   drawing simplification.
8. Underground HV option: cable count per phase, duct-bank depth, thermal backfill, sealing-end
   structure size and clearances.
9. E-house, MCC and UPS room sizes, cubicle counts, cable-vault depth and tray fill.
10. BESS container count, PCS pairing, fire separation distances and MV collection scheme.
11. Corridor tray widths, tiers, separation between power and control, duct-bank conduit count,
    manhole spacing and road-crossing details; grounding grid per IEEE 80 study.
12. CCS train sizing for gas-turbine flue gas (low CO2 concentration): absorber, DCC and booster
    fan sizes, solvent inventory, CO2 export route.
13. Fuel-gas supply pressure, metering class, heater duty, and whether LNG or hydrogen supply is
    actually foreseen; blending limits are not represented.
14. Water balance: tank sizes, pond sizing and lining, discharge route.
15. Every clearance, road width, turning radius and fire-access requirement.

## 6. Known limitations of the scripts

- The model has not been executed in Blender in this environment (no Blender available). The
  geometry path was executed in dry-run mode and through a minimal bpy shim
  (`tools/mock_bpy.py`), which exercised every builder, the material and object-creation calls,
  camera framing, credit placement and anchor projection, and produced wireframe previews for
  all 13 camera views plus all 27 composed sheets. Cycles-specific behaviour (lighting balance,
  denoiser, compositor node names) is written to the Blender 4.x API but was not rendered here;
  the first real run may need small exposure or sun-strength adjustments in views.json.
- Occlusion flags in callouts.json come from a single ray cast per anchor and are advisory.
- Curves use POLY splines with a round bevel; cables are straight or gently sagged polylines,
  not physically draped.
- The bpy shim's occlusion test is bounding-box based and reports far more occlusion than a
  real render will; ignore those lines when running the mock.

## 7. How to run

```
cd plant
blender -b -P build_plant.py -- --out out/plant.blend            # build the model, writes out/preflight.json
blender -b out/plant.blend -P render_views.py -- --scale 0.25 --samples 64     # quick test at 1250 x 888
blender -b out/plant.blend -P render_views.py -- --views views.json --out out/renders     # full 5000 x 3550
python3 make_sheets.py --renders out/renders --out out/sheets     # needs: pip install reportlab pillow
```

Options: `--only 01,04` renders a subset; `--no-render` only places cameras and writes callouts.json;
`--device cpu` forces the CPU. Without Blender, `python3 build_plant.py --dry-run` runs the preflight and
`python3 tools/mock_bpy.py --out out/mock` produces wireframe previews for layout checks
(`python3 make_sheets.py --renders out/mock --out out/mock_sheets --placeholders`).
Hide any package in Blender by prefix, for example `GT-`, `HRSG-2-`, `ACC-`, `ELEC-EHOUSE-`.
