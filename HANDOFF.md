# Handoff: SK-3X1 power campus model, renders and the October strategy deck

Branch: `claude/3d-plant-model-generation-a3ad3u` (Oct 19: `claude/3d-plant-model-generation-a3ad3u-hdozc9`, the slim export + viewer UTF-8 fix, merged into it; continue on `-a3ad3u`). Everything lives under `plant/`. The detailed pipeline guide is
`plant/HANDOFF.md` (read it too); this file covers the whole project briefly and the Oct 17-18, 2026 session in full.

## Goal

A realistic 3D model of **SK-3X1 Rev 14**, a 3x1 H-class combined-cycle gas power campus (CCS, BESS, modular power
yard, LNG terminal, hydrogen, a behind-the-meter data centre), with every cable routed, used to show what Southwire
wire and cable does in a power plant. It feeds an interactive viewer, Blender photoreal renders and slide decks.
Owner: Stephan Hardt, Southwire Power Generation Solutions. Near-term use: the **Strategy Monthly Update, October**
deck and the **Nov 11, 2026** internal Teams training (SVP of R&D attending). Conceptual illustration, not engineered.

## Done and working

- Model build, checks and viewer pipeline (see `plant/HANDOFF.md`): `verify.py` PASS, `audit.py` CLEAN at the last
  commit.
- **Strategy deck, 14 slides**: `plant/renders/deck/SK-3X1_Strategy_Update_October_2026.pdf`
  (built by `plant/blender/deck_brochure.py`; cover by `plant/blender/deck_divider.py strategy`).
  1. Cover: photoreal power block with the cable trays energised in copper (`renders/cover/HX1_hero_cable.jpg`).
  2. One campus. Every cable. (K5 aerial)
  3. Where the cable goes: cable X-ray reveal + four model-measured numbers (`renders/cover/xray_reveal.jpg`).
  4-7. Grid zone, grid detail, power island zone, hall detail.
  8. **Inside the hall**: turbine-hall cutaway, GT1-3 and the ST side by side, labelled
     (`renders/cover/HALL7_hero_cable.jpg`, camera HALL7).
  9-12. CCS, BESS, modular power, installed faster (each zone slide has an X-ray "where in the plant" locator,
     `renders/cover/xray_loc01..06.jpg`).
  13. Bookend: "Every megawatt travels through a cable." over the campus X-ray, "10 miles" of modelled routes.
  14. Product index.
- **HRSGs / stacks (the hero)**: slate casings (`pro_look.py` COLOUR_SYSTEM `hrsg` #6b757c), black buckstays, light
  stacks with copper bands, black platforms / handrails / caged ladder / CEMS ladder tray (`hero.py`), photoreal
  finishes (`pro_look.py` `hero_finish`: panel joints, weld seams, soot at the exit, drip stains, brushed copper).
- **HRSG stair towers**: full top deck with guard rails so the roof bridge no longer starts in mid-air (`hrsg.py access`).
- **Turbine hall** (`hall_finish.py`, `hall_wiring.py`, `st_detail.py`):
  - dark epoxy deck with yellow walkway lines, generators and LP casing in the unit blue, GT casings in sections
    (dark compressor, combustor, quilted insulation blankets on the hot end);
  - Southwire black structural steel, a copper band round the walls at EL 64, black rings / ribs, one copper band per
    machine;
  - end wall: US flag + printed graphic "3x1 CCGT / WIRE & CABLE PARTNER / Southwire logo"
    (`blender/hall_sign.py` -> `screens/hall_wall_sign.png`, a `print` image decal; the generic build keeps plain
    "3x1 CCGT"). Oct 19 (user: "too faded"): logo mark one solid deep copper #a65a2c with fully opaque edges,
    wordmark and labels solid black #111214, "WIRE & CABLE PARTNER" ExtraBold 165 px; in Blender every `print`
    decal is flat matte (roughness 1, specular 0) so the hall lights no longer wash it out;
  - interior electrical item: lighting panel + transformer, MC-HL under the crane girders and along the purlins to
    every high bay, column drops to welding / duplex receptacles and fire-alarm devices (red FPLR), crane conductor
    bar, exit lights;
  - steam turbine brought to the GTs' level: lube oil to three bearings, casing thermocouples (KX), probes, EHC servo
    cable, junction boxes in conduit to the EL 42 control tray, STG box, turning-gear MC feed;
  - south wall + roof split into "Turbine hall south cladding and roof (lifted off in the cutaway views)" for cutaways.
  - exterior (Oct 19, user: "the elevations look too plain"; `hall_exterior.py`, run last in `build_model.py`): brand
    once, design the rest. One exterior sign, 100 x 50 ft over the west equipment door (same `hall_wall_sign.png`;
    generic build plain "3x1 CCGT"); unit numbers GT 1-3 on the west sides of the inlet filter houses (their south
    faces are weather hoods, the hall's south wall is behind them) and ST on the south wall; the EL 64 copper band
    outside on all walls (stops at the sign's edges); black pilasters on the 44 ft column lines and corners;
    clerestory strip under both eaves; black gallery fascia; intake louvres per GT bay; west door surround + lights.
    Every strip is cut back round anything standing at the wall, so verify stays at 0 clashes. South pieces are a
    separate "Turbine hall south cladding exterior ..." item (lifts off with the cladding). Camera HX2 = the
    south-west exterior view (renders/cover/HX2_exterior.jpg).
- Renders this session (all in `plant/renders/cover/`): `HX1_hero_cable.jpg`, `HX1_photoreal.jpg`,
  `HALL7_hero_cable.jpg`, `ST1_steam_turbine.jpg`, `HALL4_hero_cable.jpg` (down-the-row alternative),
  comparison sheets (`hrsg_grey_test.jpg`, `hrsg_slate_stacks_test.jpg`, `stack_*_test.jpg`, `hall_options.jpg`).

## In progress / not yet done

- **Viewer: published.** The branded viewer (`plant/viewer/index_southwire.html`) is live at
  https://claude.ai/artifact/QtsCN1A1zmrgNTyMrqJbTL: version 3 (Oct 19) carries the UTF-8 / mobile-viewport fix
  (commit 41836bb), the solid wall sign and the hall exterior branding. To update: rebuild with `build_viewer.py --out viewer/index_southwire.html`
  and publish that file to the same url. The older artifact https://claude.ai/artifact/9bfQJUnJ6GCH35zmjBq7cP
  (generic viewer) was not updated and is superseded.
- **HALL7 / slide 8 with the solid sign:** the HALL7 128-sample re-render was running at the Oct 19 hand-off
  (first try hit the 30 min background limit); then `hero_cable.py` -> `renders/cover/HALL7_hero_cable.jpg`,
  `deck_brochure.py`, commit. If lost: rerun the mask pass (`SK_CABLE_MASK=power ... --samples 8`) and the full pass
  (`--samples 128`, run in the background with a 2 h limit).
- **GLB / USDZ / .blend predate the solid sign and the hall exterior** (exported Oct 18): they embed the old faded sign texture and lack the exterior finish. Re-export
  (`blender/export_model.py`, slim) when the 3D files are next used.
- **Older deck pictures** (slides 4-7, 9-12 heroes, K5 aerial on slide 2) predate the slate HRSG / black-copper look
  and the photoreal finishes. Re-render the cameras they use (`brochure.py` ZONES heroes E60/E70/E68/E65/E77/E64,
  details E20/E4/E66/E67/E23, K5) and rebuild the deck: about 3-4 h of Blender time.
- `plant/renders/epic/HX1_pro.png` etc. are git-ignored (`*.png`); the slide pictures that matter are committed as
  JPG in `renders/cover/`.
- ST close-up: the thermocouple leads over the LP hood top hang in the air (`st_detail.py`, exhaust-hood leads at
  EL 45.4); route them flush on the casing if ST1 is used in the deck.
- `DETAIL_CYCLES.md` / `README.md` have no entries yet for the Oct 17-18 work (the commit messages describe it).

## 3D assets (files, format, size, what uses them)

All under `plant/`. Units: the model JSON and OBJ are in feet; GLB / USDZ / .blend are in metres (Blender units).

| File | Format | Size | Built | Used by |
|---|---|---|---|---|
| `sk3x1_model.json` | master model (items, parts, routes, decals) | 22.8 MB | Oct 18 | everything: viewer build, Blender, exports, checks, cable schedule |
| `sk3x1_model.obj` + `sk3x1_model.mtl` | Wavefront OBJ, colour-only materials (no textures), Y-up, feet | 87.1 MB + 9 KB | Oct 18 | SketchUp / Rhino / Revit / 3ds Max hand-off |
| `model/sk3x1_model.obj` + `.mtl` | same files, beside the other exports | 87.1 MB + 9 KB | Oct 18 | model download folder |
| `model/SK-3X1_plant.blend` | Blender 4.2, images packed, every camera | 47.5 MB | Oct 18 | renders, re-export source |
| `model/SK-3X1_coastal_A.blend` | Blender 4.2 (plant + LNG terminal, jetty, carrier) | 47.7 MB | Oct 18 | renders, re-export source |
| `model/SK-3X1_plant_datacenter.blend` | Blender 4.2 (plant + BTM data centre) | 47.5 MB | Oct 18 | re-export source |
| `model/SK-3X1_everything_datacenter.blend` | Blender 4.2 (everything) | 47.7 MB | Oct 18 | re-export source |
| `model/SK-3X1_*.glb` (4) | GLB, glTF 2.0 binary, self-contained, every decal / screen embedded (227 images) | 94.8-101.1 MB (90.4-96.5 MiB) | Oct 18 (slim export) | PowerPoint 3D, web, Windows 3D Viewer |
| `model/SK-3X1_*.usdz` (4) | USDZ with the decal textures | 88.9-93.4 MB | Oct 18 (slim export) | iPhone / iPad AR Quick Look |
| `viewer/index.html`, `viewer/index_southwire.html` | single-file three.js viewer, model inlined (gzip) | 2.7 / 2.8 MB | Oct 19 | the interactive viewer and the tour (branded one published, QtsCN1A1zmrgNTyMrqJbTL) |
| `renders/epic/*_pro.png` (19 committed), `renders/cover/*.png`, `*.jpg` | Blender renders | ~70 MB + | Oct 2-18 | deck slides and cover |
| `screens/*.png`, `screens/hall_wall_sign.png` | images placed on the model (control-room screens, hall sign) | 2 MB | Oct 19 (solid sign) | viewer + Blender decals |

GLB / USDZ size (Oct 18, investigated and fixed): the first Oct 18 exports were 140-147 MB (GLB) / 115-120 MB
(USDZ), over GitHub's 100 MiB file limit, so they went up as zips. Why they grew from the Oct 5 files (80-87 MB):
- geometry: 2.65 M -> 4.12 M exported vertices (+56%) from the Oct 6-18 detail (tray stacks and cables +360 k,
  R1 panels +200 k, modular yard, reel yard, people, duct banks, interiors); ~2.85 M of the 3.47 M mesh vertices are
  round rods, and rod_geo gives every rod two separate flat cap rings (half its vertices);
- 1,795 decal quads, each its own object / mesh (646 -> 2,522 meshes), plus 232 embedded images (14 MB; the Oct 5
  files had no decals at all). The decals were never the size problem (7 k vertices, 14 MB of images).
Fix, in the export only (`blender/export_slim.py`, called by `export_model.py`; the .blend and renders untouched):
caps of thin rods (< 3 in radius) and of straight rod joints dropped (-25 MB), faces buried under the ground
dropped (-7 MB), decal quads merged per item and image (2,522 -> 1,268 meshes), images recompressed and
de-duplicated by `tools/glb_images.py` (14 -> 4 MB). Result: GLB 94.8-101.1 MB, USDZ 88.9-93.4 MB (now with the
decal textures), all four raw files committed again, `model/current/` zips removed (in commit c3e0529 if needed).
Checked: glTF validator 0 errors (same as before); three.js renders of old vs new files at four tour cameras
differ in <= 0.02% of pixels. No glTF extensions added. Headroom is ~3.5 MiB on the "everything" GLB: if the model
grows, the next lever is KHR_mesh_quantization (`gltfpack -kn -km -ke`, 140 -> 65 MB, lossless to the eye; fine
for three.js / web, untested in PowerPoint) or Git LFS.
No committed file is over 100 MiB; the largest is the 101.1 MB (96.5 MiB) everything GLB (GitHub warns above 50 MiB).

## Key decisions and why

- **Colours**: one colour system in `pro_look.py` COLOUR_SYSTEM (neutral greys, slate hero, Southwire black #1c1d1f /
  burnished copper accents only on the hero and the hall). The user rejected: black stack crowns, white/gloss stacks,
  golden hour, dark ground, busy rooftop equipment. Liked: slate HRSG, light stacks, black platforms, copper bands,
  copper X-ray, energised-copper glow.
- **Cable as hero** in photoreal shots: render the same camera twice, second pass with `SK_CABLE_MASK=1|mv|power`
  (cables pure red), then `blender/hero_cable.py PHOTO MASK OUT` adds copper tint, core, bloom and pulses only on the
  cable pixels (occlusion correct). `power` = 15 kV + 480 V MC; `mv` = 15 kV only. The 15 kV tray correctly stops at
  GT3: the ST has no MV loads (fed at 480 V from the EL 30 tray and R3).
- **Plumes off** in the close shots: thin white vapour still rendered as grey smoke against bright sky.
  (`PLUME_DENSITY`, `volume_bounces = 3` and white absorption are in `pro_look.py` for later.)
- **Cutaway for the hall**: from inside the hall (150 ft wide, 460 ft long) the machines always overlap; HALL7 lifts the
  south cladding / roof, the hall exterior electrical item and the filter houses / inlet ducts.
- **Branding on the wall** as an owner-style credit ("WIRE & CABLE PARTNER"), not an advert; generic build unbranded.
- Units: model in **feet, x east, y north, z up**; Blender in metres (`FT = 0.3048`).
- `verify.py` TOUCH pairs and `audit.py` allowed list were extended for the hall south cladding (its own wall panels).

## How to run / build / preview

```
cd plant
python3 build_model.py && python3 verify.py && python3 audit.py          # model + checks (PASS / CLEAN)
python3 build_viewer.py --generic && python3 build_viewer.py --out viewer/index_southwire.html
# Blender (Python 3.11 venv with pip install bpy==4.2.0 pillow numpy):
python blender/SK-3X1_Rev14_blender_build.py --views HALL7 --style pro --set epic --samples 128 --scale 100 --out OUT
SK_CABLE_MASK=power python blender/SK-3X1_Rev14_blender_build.py --views HALL7 --style pro --set epic --samples 8 --scale 100 --out MASK
python blender/hero_cable.py OUT/HALL7_pro.png MASK/HALL7_pro.png renders/cover/HALL7_hero_cable.jpg
python blender/deck_divider.py strategy      # cover (COVER_PHOTO env picks the picture, default HX1_hero_cable.jpg)
python blender/deck_brochure.py              # slides 2-14 + the full PDF
python blender/hall_sign.py                  # end-wall graphic
```
Hall cameras in `blender/pro_look.py` EPIC: HX1 (cover), HALL2-HALL8, ST1, E1, K5, SC1. X-ray captures:
`plant/tools/xray_capture/README.md`.

## Next steps (priority) and the plan proposed Oct 18 evening (awaiting the owner's go)

1. **Viewer republish: done Oct 19** (branded viewer, https://claude.ai/artifact/QtsCN1A1zmrgNTyMrqJbTL). Still
   worth a look on desktop and phone width: hall views, tour stops 4-7 and 14-15. Finish the HALL7 / slide 8
   re-render (see In progress).
2. **Deck re-render** (old renders predate the slate HRSG / light stacks / black-copper hall / photoreal finish).
   Slide -> cameras (`blender/deck_brochure.py`, `brochure.py` ZONES):
   2 K5 · 4 E60 (+ inset E19) · 5 E20, E4, E31 · 6 E70 · 7 E66, E67, E23 · 9 E68 (+E57) · 10 E65 (+E62) ·
   11 E77 (+E78) · 12 E64 (+E58) · 14 K1 (product index, also shows the plant).
   - Tier 1, the hero or the hall is in frame (must): K5, E20, E70, E66, E67, E23, E68, E64 (8 cameras).
   - Tier 2, no HRSG / stack in frame (consistency of light and finish only): E60, E19, E4, E31, E57, E65, E62,
     E77, E78, E58, and optionally K1.
   - Run as background batches under the 2 h job limit (4 CPUs, ~15-20 min per camera at 128 samples, scale 100):
     batch A K5, E20, E70, E66; batch B E67, E23, E68, E64; then tier 2 if wanted. Each: render, `finish_pro.py`,
     look at a contact sheet against the HX1 / HALL7 look, re-render any miss, then `deck_brochure.py` and commit the
     PNG sources (force-add, `*.png` is ignored) plus the PDF. K5_pro.png / K1_pro.png are not in the repo (ignored,
     lost with the container), so K5 and K1 must be rendered before `deck_brochure.py` can rebuild slides 2 / 14.
3. Log the Oct 17-18 work in `plant/README.md` (DETAIL_CYCLES.md has the slim-export entry).
4. ST close-up polish (flush thermocouple leads) if ST1 goes in the deck.
5. Training prep from `plant/HANDOFF.md`: fundamentals slides, SME review, two Teams dry runs.

## Only in the conversation (not in files until now)

- The user's taste and review history above (what was rejected and liked); keep "not too busy, not too dark",
  realism first, power block as hero, copper accents, ship and BTM visible in campus views.
- A reviewer's note adopted for the cover: one subject, sky above, no smoke, label unobstructed.
- Environment: the Blender venv lives in the session scratchpad and dies with the container. Recreate it:
  `python3.11 -m venv bvenv && bvenv/bin/pip install bpy==4.2.0 pillow numpy openpyxl` (Oct 18 evening: bpy 4.2.0,
  numpy 2.4.6, Pillow 13.0.0; installs in ~1 min). Blender segfaults on exit after an export; the files are complete. Background jobs max 2 h. **Never `pkill -f` / `pgrep -f`
  with a pattern that also appears in the same command line** (it kills the shell); run the kill as its own command.
- Root `.gitignore` ignores `*.png`; force-add PNGs that the build needs (e.g. `screens/hall_wall_sign.png`).
- No file in the repo is over 100 MiB (largest: the everything GLB, 96.5 MiB). Current GLB / USDZ are raw in
  `plant/model/` again (slim export, Oct 18 evening).
