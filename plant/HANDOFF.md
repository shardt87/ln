# SW-3X1 3D gas power campus: handoff guide

Read this first. It lets another assistant (or a person) pick the project up with no history.
Owner: Stephan Hardt, Power Generation Solutions (Southwire). Conceptual illustration: not engineered, not for
construction.

## What this is

A 3D coordinate model of **SW-3X1 Rev 14**, a 3x1 H-class combined-cycle campus, rebuilt from a 15-sheet concept
drawing set (`reference_docs/SK-3X1_Drawing_Set_Rev14.pdf`) and checked back against it. Around the plant:
- carbon capture
- BESS
- a modular power yard (RICE engines, LM6000-class simple cycle, TM2500-class trailer turbines, containerized /
  trailer / skid gensets, fuel cells, microturbines)
- GT inlet chilling
- an LNG satellite and a marine LNG import terminal
- green hydrogen
- a ~150 MW behind-the-meter (BTM) data centre

Every powered item has its cable routed: trays, duct banks, trenches, conduit. A cable schedule (5,695 runs, about 1,120
miles) is derived from the model.

Purpose now: a **1-hour Southwire technical training on Nov 11, 2026** (Teams; SVP of R&D attending):
"Inside Power Generation: Market Fundamentals and a 3D Gas Power Campus Tour". See `presentation/TOUR_SCRIPT.md`.

## The pipeline (all Python 3.11 unless noted)

```
python3 build_model.py              # -> sw3x1_model.json  (the master model: items, parts, routes, views, decals)
python3 verify.py                   # footprints / heights / clashes / bounds vs the drawing  -> must print PASS
python3 audit.py                    # wiring audit                                            -> must print CLEAN
python3 coastal/verify_coastal.py   # coastal variant                                        -> PASS
python3 discrepancy_scan.py         # floating parts, hanging signs, open tray ends          -> zeros
python3 cable_continuity.py         # loose cable ends (37 deliberate tails)
python3 cable_schedule.py           # -> brochure/SW-3X1_Cable_Schedule_and_BOM.xlsx + brochure/cables_xray.json
python3 build_viewer.py --generic                         # -> viewer/index.html (unbranded)
python3 build_viewer.py --out viewer/index_southwire.html # Southwire-branded viewer (used for the training)
python3 export_obj.py                                     # -> sw3x1_model.obj / .mtl
```
Only the standard library plus Pillow / openpyxl / numpy are needed for these.

**Blender renders** (Blender 4.2+ Python module `bpy`, run as a script):
```
python blender/SW-3X1_Rev14_blender_build.py --views E123,E2 --style pro --set epic --samples 128 --scale 75 --out OUT
python blender/finish_pro.py OUT          # vignette, grain, caption -> *_clean.jpg / *_final.jpg
python blender/SW-3X1_Rev14_blender_build.py --style pro --set epic --no-render --out /tmp/c --blend model/SW-3X1_plant.blend
python blender/export_model.py model      # -> model/SW-3X1_plant.glb / .usdz
```
Cameras live in `blender/pro_look.py` (EPIC list: `dict(k="E123", n=..., eye=(x,y,z), target=(x,y,z), lens=mm, show=...)`).
Model coordinates: **feet, x east, y north, z up**; the compound is 2,420 x 1,920 ft.

**Slides:** `blender/slide_hero6.py` (hero-shots slide), `blender/slide_modular.py`, `blender/deck_divider.py`,
`blender/deck_zone_slides.py`. Deck fonts are in `blender/deck/` (Barlow / Barlow Condensed).

## The viewer and the guided tour

`viewer/template.html` is a single-file three.js r147 viewer, filled in by `build_viewer.py` (gzip/base64 model inlined).
- Views (SW-3X1-11)
- layers
- section cut
- Cable X-ray: every cable of the schedule on its route
- tray fill
- BTM power paths
- **▶ Tour**

The tour stops are in **`presentation/tour.json`**: 51 stops, sections Arrival → 10. Each stop has:
- `c` / `t`: camera position and target in feet
- `lens`: mm on a 36 mm sensor
- `show`: viewer view key whose layers are shown
- `add` / `hide`: extra layers
- `xray` / `paths`: overlay toggles
- `near`: near clip, for interiors
- `drift`: degrees per second of slow orbit
- caption: `sec`, `title`, `eq` (Equipment), `sys` (System), `cab` (Cable)

Keys in the tour: → / Space / PageDown next, ← back, Esc exit. Published viewer:
https://claude.ai/artifact/9bfQJUnJ6GCH35zmjBq7cP (Claude-hosted; the HTML files in `viewer/` are the same page,
open them locally in Chrome or Edge).

**Recording the tour as MP4** (`presentation/tour_kit/README.md`):
- `record_tour.js` (Node + Playwright) renders every frame on a fixed clock.
- `compose_tour.py` adds the deck-style captions and encodes H.264 clips plus the full tour.
- On a PC with a graphics card it takes 30 to 60 minutes. Without a GPU (cloud) it takes most of a day.

## Rules the owner has set (keep them)

- **Realism first:** cables visible and connected end to end, nothing floating or disconnected, no empty areas.
- **Fix it properly, not with a band-aid.** Example: the LNG cable runs on one rack level and drops into the e-house
  roof, with no step-ups.
- **The HRSGs and stacks are the visual hero.** HRSG casings slate grey (#6b757c) with black buckstays / wale bands,
  light-grey stacks (#cfd3d5) with burnished-copper bands, black platforms / rails / ladders, copper "HRSG k"
  lettering (no black crown: tried and rejected). See the root `HANDOFF.md` for the Oct 17-18 session. Carbon capture stays secondary: muted sage (#9dbba5) with four "CCS" letterings per absorber.
- **One gravel colour** everywhere except the switchyard.
- **Every view shows the whole campus** (modular yard, BTM, the marine terminal); views remove only cutaway roofs and walls.
- **Commits:** checks must be clean (verify PASS, audit CLEAN, scans at zero) before a commit.
- **Docs:** each change gets an entry in `DETAIL_CYCLES.md`.
- **Language:** plain English in captions and docs. Product names are Southwire families: ARMOR-X MC-HL, MV-105,
  Type TC-ER, PLTC / ITC, FPLR, Type W, SHD-GC, SIMpull. The `--generic` build strips the brand names.

## Where things stand (Oct 16, 2026)

- Model, checks, viewer and tour: done and current.
- Hero-shots slide (7 renders): `renders/deck/SW-3X1_hero_shots.*`.
- Tour clips: 11 of 51 recorded in the cloud; the rest are best recorded on a PC (tour kit) or by screen recording the
  live Tour.
- Deck plan, i.e. which Wesco-deck slides to keep, change or add: `presentation/TOUR_SCRIPT.md`.
- **Open items:**
  - New slides: combined-cycle fundamentals, the gas-generation family, a simplified one-line, and the closer
    "What the plant asks of cable" (R&D hook).
  - SME review of the items marked [check] in the script.
  - Two dry runs on Teams.

## File map (short)

| Path | What |
|---|---|
| `build_model.py`, `fuel.py` | Master build and the part / item helpers |
| `*_lod3.py`, `hall*.py`, `hrsg.py`, `modular*.py`, `yard.py`, `ccs*.py`, `lng_h2.py`, `datacenter.py`, ... | Detail passes per area (see README "Files") |
| `trays.py`, `wiring.py`, `cables.py`, `cable_*.py`, `surface_cable.py`, `underground.py`, `network.py` | Cable routing, drops, risers, duct banks; `network.py` is the route graph shared by the build and the schedule |
| `verify.py`, `audit.py`, `discrepancy_scan.py`, `cable_continuity.py` | Checks |
| `sw3x1_model.json` | The built model (also regenerable) |
| `viewer/` | Viewer template and built viewers |
| `presentation/` | Tour stops, script, recorder, compositor, tour kit |
| `blender/` | Render look, cameras, render and export scripts, slide scripts |
| `brochure/` | Cable schedule workbook, X-ray data |
| `coastal/`, `reference/`, `screens/`, `site/`, `threejs/` | Coastal variant, drawing reference data, control-room screen images, site data, three.js helpers |
| `README.md`, `DETAIL_CYCLES.md` | Full documentation and the change log |

## Next-generation power brochure section (Oct 21)
- `blender/brochure_nextgen.py` builds `renders/nextgen/SW_NextGenPower.pdf` (6 pp, email credit on pp 2+), previews prev_01..06.png.
- Pages: opener / then and now (8-row table) / the modern campus / decarbonisation (CCS, 25 MW PEM H2, H2-ready GTs) /
  built faster (SC-4 plug-and-play pad, SIMpull + Maxis fit-out) / sustainability + Formula E.
- Formula E photo and logo: dashed placeholder until brand approval. Formula E facts as published; the series' own
  sustainability claims are attributed to it. Check all of these before printing.

## SC-1 / SC-2 simple-cycle detail pass (Oct 21, viewer v56)
- New `sc_detail.py`, called from `modular.build()` (drawn coordinates; SC-2's set is turned end for end by
  `sc2_mirror.build()` with the rest of the unit, since every item is named "SC-k ...").
- Inlet: tapered transition out of the filter house, silencer duct with bands and expansion joint, plenum into the
  turbine enclosure (replaces the plain plenum box in modular.py). Generator vent fan moved off the duct (modular_lod3).
- Enclosures: generator panel joints, vent louvres, turbine vent-exhaust silencer, door steps, CO2 rack and signs,
  generator terminal box over the MV tray, NGR.
- New items: SC-k auxiliary skids (fuel-gas module on the gas drop, water-wash skid), tempering-air fans (2 x 100 %,
  ducted over the fuel-gas header into the collector), ammonia flow-control unit, CEMS shelter with heated sample
  line to the stack platform. SCR access doors; stack foundation ring, breeching expansion joint.
- SCR stair turned to run along the platform: it used to straddle the y 1182 fuel-gas header (pre-existing clash).
- Conduit stub-ups and whips into every new motor / skid.
- Cameras SC9-SC12 (pro_look.py); previews in renders/sc_detail/.
- Oct 21 tidy (owner: the auxiliaries looked bulky on the camera face): ammonia flow-control unit and the NH3 riser to
  the injection grid moved to the north (back) face of each SCR; fuel-gas module made low (6 ft) and set tight
  against the enclosure; CO2 cylinders stand on the skid against the wall with a strap (rack removed). Tempering-air
  fans kept as they were. Viewer v57.
- Oct 21 tempering-air fans remodelled (owner: model them better): two centrifugal fans (shaft along x, scroll housing,
  top-horizontal outlet) on a steel platform at EL 7.6 over the fuel-gas header, motors inboard on a common base with
  coupling guards and terminal boxes, inlet bells and silencers with weather hoods outboard, isolation dampers with
  actuators and expansion joints, short ducts straight into the collector; handrail, ladder, local control station,
  conduit up the column to each motor, sign under the deck edge. Bracing in the column rows (clear of the header).
  Viewer v58.
- Oct 21 stack / SCR check (owner): SC stacks get an exhaust silencer section (EL 31-47, cones and flanges), a
  heat-stained band at the outlet, a caged ladder, sampling ports above the platform, a base manway. SCR: caged
  ladders EL 14 -> 27 and 27 -> roof, roof guardrail, expansion joints at both ends of the exhaust collector.
  Cameras SC13 (from above) and SC14 (from grade). Viewer v59.
- Oct 21 SC branding (owner: "the same branding of the combined cycle"): campus_brand.py gives SC-1 / SC-2 the hall's
  set on the turbine enclosure: 1.6 ft copper band (EL 17.2-18.8), black coping, black corner pilasters, metallic
  copper chevrons (screens/sc_chevrons_e/_w.png from blender/hall_sign.py) at the exhaust end pointing at the paired
  stacks, and SC1 / SC2 painted in the hall's Barlow face (screens/unit_SC*.png) where the white nameplate was
  (removed in modular_lod3). South compartment louvre dropped for the livery (north one stays). Viewer v60.
- Oct 21 SC stack / SCR branding (owner): the HRSG stacks' finish on the SC stacks (3.7 ft copper band under the
  sampling platform, 1.2 ft band below the silencer, platform / rails / ladder / cage black; the dark outlet band
  taken off, as the CC black-crown trial was) and the HRSG casing finish on the SCRs (slate "hrsg" casing, black
  ribs, "SCR 1 / SCR 2" in copper between the platforms on the south face, the ribs broken behind it; upper catalyst
  doors moved to the ends). Viewer v61.
- Oct 21 SC-4 plug-and-play pad remodelled (owner: the three-tier spine modules looked generic and clunky; how is such
  a pad really wired?): reserved_pad.demo() now shows it as an LM6000-class pad is built: a factory cable bus (two
  bolted aluminium sections on portal supports, capped flanges, "AWAITING GENERATOR") for the 13.8 kV generator leads
  to the PCM; a precast surface cable trough on grade (2 ft, lids, two stretches open with the lids stacked beside)
  carrying control / instrument / fibre to branches at each skid landing and the PCM pad; pre-terminated harnesses
  with plug connectors and dust caps coiled at each landing (moved clear of the PCM MV stub-ups); ground-grid copper
  pigtails at the foundation and PCM pad corners. Painted outlines, PCM landing frame and PLUG & PLAY sign kept.
  Camera SC15 (close). Viewer v62. NB: the nextgen brochure page 5 hero (SC7) still shows the old modules; re-render
  SC7 and rebuild brochure_nextgen.py when that brochure is next touched.
- Oct 21 SC-4 pad "show the wire" (owner): cable bus second section opened (west panel off, laid on the slab):
  3 phases x 4 x 500 kcmil MV-105 in two rows, spacer blocks, phase tape; label on the closed section. Testing in
  progress at the TCP landing: test cart (IR / VLF set showing PASS, laptop), leads to the harness connector,
  technician. Every harness tag carries a QR (screens/qr_cable.png, blender/qr_tags.py, placeholder record ID; needs
  `pip install qrcode` to regenerate); a SCAN ANY CABLE TAG digital-model sign with its QR; a cable ID placard on the
  open trough stretch. Cameras SC16 (cable bus cutaway), SC17 (testing / QR / placard). Viewer v63.
- Oct 21 SC-1 / SC-2 cable audit (owner):
  * fixed: every SC load (package motors, lube cooler, SCR, stack lighting, inlet chiller, new skids) was fed from the
    RICE plant's PCM-1 (nearest by distance); cable_schedule.sc_pcm() now takes each unit's 480 V, control and I/O
    from its own SC-k PCM;
  * fixed: the second-pass equipment had no cables: tempering-air fans 2 x 185 kW (500 kcmil), ammonia flow-control
    (2 x 7.5 kW blowers, 45 kW vaporiser heater, I/O, solenoids), fuel-gas module + water-wash (ARMOR-X / ITC, Class I
    Div 2), CEMS shelter (panel, HVAC, analyser I/O, fibre, fire alarm), generator neutral to the NGR (MV-105 #2),
    generator CT / VT secondaries; the SCR's two phantom 30 kW motors removed (the fans are their own item);
  * fixed: model vs schedule: the generator tray showed 6 MV cables, the schedule sizes 5 x 3 x 750 kcmil MV-105
    for ~2,100 A: tray now 36 in with 15 cables; the SC-4 cable bus cutaway shows the same 5 x 750 kcmil per phase,
    one row per phase (red / amber / blue tape); terminal-box drops lifted clear of the tray;
  * pre-existing, not SC: the admin building's 800 A service fails the 125 % ampacity check (2 sets).
  Camera SC18 (generator tray). Viewer v64.
- Oct 21 SC audit, part 2 (owner: "did you check these ones too"): every item round the SC units checked.
  Fixed: water-injection skid (now 2 x 75 kW HP pumps + I/O), demin tank, aqueous ammonia (2 pumps + I/O) and the
  fuel-gas compressors' control / home runs moved from the RICE PCM to the nearer SC PCM (sc_pcm(); their MV stays
  from MOD-EH); the SC PCMs get their own building services (lighting / HVAC from their 480 V board, DCS fibre and
  F&G to the control building). Unchanged and correct: RICE hall, reagent storage, RICE PCM on the RICE PCM; trays,
  pipes, signage, people, fence and site lighting carry no load of their own (lighting counted under Site lighting).
