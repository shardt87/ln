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
- Oct 21 SC electrical system review (owner): one-line generator 13.8 kV -> 5 x 3 x 750 kcmil tray -> PCM 15 kV GCB ->
  5 x 3 x 750 kcmil duct bank -> MOD-EH -> bus duct -> T-MOD-1 / -2 13.8/230 kV -> gantry -> H-MOD tie checks out.
  Added: PCM aux transformer 2 MVA (MV primary row), 125 V DC battery cables, emergency DC lube-oil pump feed, 120 V
  UPS to the unit control, hydraulic starter pump motor 225 kW (verify with the OEM), 2 welding receptacles per unit,
  lighting on the SCR platforms (10), enclosure exterior (8) and fan platform (4); CT / VT secondaries now on the
  #10 CTCT product. Capacity: the yard exports ~255 MW (~283 MVA); T-MOD bus duct raised to 6,300 A and T-MOD-1 / -2
  noted ~150 MVA ONAN/ONAF in the model (5,000 A / ~120 MVA each was short). Viewer v65.
- Oct 21 SC package interiors (owner: "inside the enclosures"): new sc_interior.py. walls() (called from
  sc_detail.build before the detail) makes the generator / turbine compartments hollow in their own item "SC-k package
  enclosure (walls and roof)" with openings for the shaft, the roof inlet duct and the exhaust diffuser; enclosure
  doors, joints, louvres, vent silencer, roof fans (modular_lod3), CO2 strap and wall signs moved onto it; campus_brand
  skips it as wall; detail3 no longer adds SC roof fans. interior(): generator (stator, end shields, exciter, bearings,
  cooler, line-side terminal box with the 13.8 kV leads to the wall, neutral cubicle, lube lines), shaft and coupling
  guards, inlet plenum, bellmouth, LM6000-class engine stages, mounts, fuel-gas manifold with 15 nozzles, water-
  injection ring, fuel / water lines from the south wall, harnesses to JB-1/2/3 on the north wall, interior ladder tray
  and wall transit, CO2 header and nozzles, gas / heat detectors, lights, walkways, monorail with hoist.
  Fuel-gas drops now rise into each unit's fuel-gas module (build_model routes x 1950 / 2218.5) instead of at the
  enclosure door. Cameras SC19 / SC20 hide "SC-1 package enclosure" and the exterior finish. Viewer v66 (use the
  section cut at ~EL 16 to look inside in the viewer).
- Oct 21 SC interiors, second pass + x-ray (owner): sc_interior.refine(): accessory gearbox with radial drive and
  hydraulic starter (+ hydraulic lines out south), lube supply / scavenge to the sumps and out north to the cooler,
  ignition exciter and igniter leads, UV flame detectors, VSV unison ring and actuators with LVDT leads, speed and
  vibration pickups with cables down the base to JB-3, generator stator RTDs and bearing probes to an RTD box, space
  heaters, ceiling lighting conduit and lighting panel, fire-and-gas loop to an F&G panel. SC-2's enclosure walls and
  roof are x-rayed: new palette colour "xray" (#9fc4d8, opacity .22; Blender pro_look alpha .14, viewer 'glass'
  class); band, joints, doors and roof gear stay solid. SC-1 keeps its solid enclosure (cutaways SC19 / SC20).
  Camera SC21 (SC-2 x-ray from above). Viewer v67.
- Oct 21 turbine hall GT wiring audit (owner: "I feel that we are missing"): GT1-3 had only the TC harness, two JBs
  with conduit, the fuel manifold and lube lines; GTG-1..3 had no cable at all. New gt_wiring.py (after st_detail):
  bearing proximity probes with extension cable to the JBs, IGV actuator servo / LVDT cable, four UV flame detectors
  with leads to JB-2, ignition exciter and igniter leads; on each GTG an RTD / vibration box with rigid conduit along
  the GT conduit run, bearing probes, stator RTD leads, space-heater MC feed, DC field leads from the collector end
  through a deck plate (west of the IPB phases). The cable schedule already counted these devices (DEV GT / GTG);
  the model now shows them. Cameras GTW1 / GTW2 (hall wall and roof lifted). Viewer v68.
- Oct 21 turbine hall power-cable audit (owner): 480 V to every GT / GTG / skid was already scheduled from MCC-GTn and
  the generator output rides the IPB. Missing and now scheduled per GT: ET-n secondary to EXC-n (5 x 3 x 750 kcmil
  5 kV, ~2,200 A AC), EXC-n DC field leads to the GTG collector (8 x 2 x 1000 kcmil 2 kV, ~4,500 A DC), TX-LCI-n
  secondary to LCI-n and LCI-n output to the GTG terminals (3 x 3 x 750 kcmil 5 kV each), GTG-n neutral to NGT-n
  (25 kV 4/0); STG field leads from EXC-ST and neutral to NGT-ST. Model: MC-HL from the tray drop to both pump
  motors on each GT aux skid, with local disconnects (gt_wiring.py). Viewer v69.
- Oct 21 turbine hall "all cables" audit (owner): every cable class checked per item for GT1-3 / GTG / skids / EXC /
  NGT / SFC / GCB / GSU / UAT and the ST train. Added: TCP-1..3 and EHC-ST redundant DCS fibre and 120 V UPS feeds;
  lube-oil skid fire detection (GT aux, ST aux); GSU / UAT transformer fire detection + deluge release; GCB 125 V DC
  close / trip / spring charge and heater feeds; FS-GTn fire detection and CO2 release; GFM-n gas detection.
  Admin building 800 A service now 3 sets 500 kcmil (was 2; the workbook's last ampacity FAIL). Workbook audit: all
  PASS; the voltage-drop CHECK (EDG-1 / -2 3.1-3.3 %, fuel-cell AC 5.6 %) remains for review.
- Oct 22 MV connections at the generators (owner: "how MV connects to the turbine", both views): new
  mv_terminations.py (late, after admin_wiring). SC-1 TB-G1 opened (closed box and token drops removed from the SC-1
  item; SC-2 keeps its closed box): wall bushings, copper phase bars, 15 x 750 kcmil MV-105 up from the tray through
  the gland plate, each with phase tape, cold-shrink termination with three sheds, compression lug and bolt, shield
  drain to a ground bus bonded to the grid; cover on the slab with the TB-G1 legend; DANGER 13,800 V sign. North-face
  generator vent louvre moved clear of the box (sc_detail). GT1: SDS-1 starting disconnect in the electrical gallery
  beside the IPB (stand, switch housing with viewing window and handle, open cable chamber with a light, 9
  terminations on three bars, tap enclosure to the bus), LCI-1 output 3 x 3 x 750 kcmil on a ladder tray from SFC-1
  at y 388 (north of the EL 42 tray posts). Cameras MVT1, MVT2 (cutaway). Viewer v70.
- Oct 22 cable moment at SC-1 (owner: "make a wire cable moment"): mv_terminations.moment(): two electricians on a
  scissor lift at the opened TB-G1 with cold-shrink kits and a tool bag; the last set of 750 kcmil MV-105 off a reel
  on an RR-SW30 reel roller (simpull.reel_roller) over a sheave into the generator tray (tray cables carry their
  printed jacket legends from modular_lod3); reel tender; VLF test cart ready; story sign (generator leads 13.8 kV,
  15 x 750 kcmil MV-105, terminate / VLF test / energize). TB-G1 cover moved north (y 1224.4-1227.2) and its ground
  bond moved to the east end, clear of the lift. Camera CM-SC1. Viewer v71.
- Oct 22 RICE branding, the last branding step (owner: "RICE branding and that's it"; the rest of the modular yard
  stays as is): metallic copper chevrons on the RICE hall's east end wall north of the roll-up door, pointing at it,
  full wall height through the band (screens/rice_chevrons.png from blender/hall_sign.py; decal in campus_brand.py).
  Camera RICE1. Viewer v72.
- Oct 22 RICE branding revised (owner: the chevrons crossing the band read odd; "missing the stacks and the rest of the
  composition"): chevrons now under the band only (EL .8-22.3, 10 ft wide, rice_chevrons.png); campus_brand
  rice_exhaust(): the eight 90 ft stacks get the HRSG stacks' copper bands (under the EL 62 platform and a thin one
  at EL 38) with platforms / rails / ladders black, and the SCR housings and silencers the HRSG casing finish (slate
  "hrsg", black ribs). Camera RICE2 (south-east overview). Viewer v73.
- Oct 22 RICE hall tidy (owner: two name signs; black corner post and copper band not mixing): the white "RICE ENGINE
  HALL / 8 x 18 MW" panel above the band removed (modular_lod3), the black door sign stays at each end; RICE corner
  pilasters off (campus_brand corners=False), the band wraps the corners clean. Camera RICE3. Viewer v74.
- Oct 22 electrical audit, RICE hall + turbine hall gallery (owner: "too rough"):
  * RICE (new rice_electrical.py, before mv_terminations): MV leads from every generator terminal box (6 cables) to
    an EL 20 MV ladder tray over the generator line, east-end drop to EL 12 and through a wall sleeve onto the PCM
    bridge; parallel control tray; trapeze hangers to the roof steel (clear of the parked crane); per engine an
    engine control panel (HMI, lamps, E-stop) with a conduit pair to the control tray, three engine JBs and the
    harness along the base frame; LED high-bays in three rows on MC from LP-RE; welding receptacles on the north
    columns; horn-strobes; ridge methane detectors on their loop. Camera RICEIN (roof / wall lifted).
  * Gallery (new gallery_electrical.py): EXC / SPC / NGT / ET / SFC / GCB rebuilt with swgr_rooms fronts (drive,
    pc_panel, dry_xfmr), nameplates, GCB mechanism cabinets and bus flanges; DC field cables rising from each
    exciter to the existing EL 30 field tray; LED high-bays at EL 30 where clear. The tray model already carried
    ET -> EXC (EL 10.5) and EXC -> GTG (EL 30): no duplicates. gt_wiring field leads now rise from the collector to
    that tray end (no deck penetration). Cameras E25 / E53 lit and cut away. Viewer v75.

## Oct 22 — every reel and the SIMpull Truck in the Southwire livery (viewer v76)
Owner: "correct the reels and SIMpull truck with the Southwire logo on flange and trucks that are still the old model".
- `simpull.meatball()` / `simpull.logo_flange()`: black steel flange (spoked) filled by the copper `sw_meatball.png`
  image decal, the same treatment as the hall_exterior tractor-trailer reels.
- Applied to every older reel builder: `showcase.reel` (timber flanges and stencils gone; reel yard, modular_lod3,
  jack_reel, cable moments), `simpull.sp_reel`, `flange_reel` (meatball on the SIMpull Flange), `stack_reel`,
  `reel_roller` (all reel-roller scenes incl. the SC-1 moment and the GT1 outage pull), `maintenance.reel_trailer`
  (meatball placed in site coordinates in `scene()`, the local parts are transformed by `_place`),
  `admin_wiring.reel_stand`. 133 meatball decals in the model.
- `showcase.simpull_truck` (reel yard and modular-yard pull): white cab with the red stripe, exhaust stacks, the
  solid logo on the doors, red skirts with the white logo and SIMpull SOLUTIONS, tyres; same 34 ft footprint.
- Cameras RL1 (truck close-up) and RL2 (reel rows) added. Previews: renders/reels_livery/.
- verify PASS, audit CLEAN.

## Oct 22 — SIMpull trucks: copper instead of red (viewer v77)
Owner: "instead of red on the trucks change it to copper". The cab stripe and flatbed skirts of `showcase.simpull_truck`
and the skirts and cab stripe of the hall_exterior tractor-trailer are now `hero_accent` (the copper of the stack
bands and chevrons). Logos unchanged. Previews: renders/truck_copper/ (RL1, HX3). verify PASS, audit CLEAN.

## Oct 22 — ladder-tray elbows: the cables bend (viewer v78)
Owner (tour stop 32, RICE generator cables to the PCM): "why are the cables not curving or bending, it looks cut out".
The ladder-tray builder (`gas_lod3.tray`, style "tray") drew each leg's cables as straight rods that stopped square at
the corner and overlapped the next leg. Now `_rounded()` replaces each corner with a radius-max(2 ft, w) elbow: every
cable follows the centre line at its own offset (concentric arcs), the elbow has curved side rails and radial rungs,
and the straight rails / rungs stop at the elbow. Used by the RICE MV bridge (MY-T1) and the SC generator trays.
Camera RB1 added; previews renders/tray_bend/ (E115, RB1). verify PASS, audit CLEAN.

## Oct 22 — sustainability leaf on the CCS absorber bands (viewer v79)
Owner: "add a leaf for sustainability on the spaces in between CCS". `blender/leaf_icon.py` draws screens/ccs_leaf.png
(a single leaf in the lettering's dark sage #3d5c47, veins in the band's light green, transparent). `ccs_lod3.
absorber_identity()` prints it in every gap between the four CCS letterings on absorbers A-C: one 12.5 ft leaf at 45,
135 and -45 deg; the south-west gap carries the caged ladder (-135 deg), so two 8 ft leaves flank it (-121, -149).
Cameras CL1 (absorbers from the south-west) and CL2 (absorber B close); previews renders/ccs_leaf/. verify PASS, audit
CLEAN.

## Oct 22 — CCS leaf redrawn, one big leaf per gap (viewer v80)
Owner: "didn't like the shape of this leaf, and I also don't want two side by side, just one big one in between those
CCS". `blender/leaf_icon.py` redrawn from cubic Beziers: a smooth pointed blade tilted up to the right, curved midrib
with four sweeping veins per side, curled stem; same dark sage on transparent. `ccs_lod3.absorber_identity()`: one
17 x 17 ft leaf centred in each of the four gaps (45, 135, -45, -135 deg) on absorbers A-C; at -135 the caged ladder
runs in front of it. Camera CL3 (absorber A from the south-west); previews renders/ccs_leaf/. verify PASS, audit CLEAN.

## Oct 22 — CCS leaf made legible at distance (viewer v81)
Owner: "from the distance ... looks like just a blob; make sure it looks like a leaf from distance as well". The thin
veins vanished at distance and the outline alone was near-oval. `blender/leaf_icon.py` redrawn as a signage icon: a
pointed blade with a drawn-out tip, a thick stem continuing the axis, a wide midrib gap splitting it into two greens
(#34543e / #5c8562), three thick vein cuts per side (cuts are transparent, so the band shows through). Checked at 120,
48 and 24 px. Decal enlarged 17 -> 20 ft. Previews renders/ccs_leaf/ (CL1 distance, CL3 close). verify PASS, audit
CLEAN.

## Oct 22 — CCS mark: a Growing Green style sprig, one colour (viewer v82)
Owner supplied the Southwire "Growing Green" mark as the reference: "use this ... but all same colour, not just one leaf
green". `blender/leaf_icon.py` now draws a sprig in that manner (drawn, not traced; no wordmark): a gently curving
stem, a top leaf and three left / right pairs growing larger toward the foot, wide pointed leaves curling up at the tip,
each with a curved vein cut to the band colour; all one green (61, 100, 72). Same file (screens/ccs_leaf.png), same 20 ft
decal in each of the four gaps on absorbers A-C. Previews renders/ccs_leaf/ (CL1, CL3). verify PASS, audit CLEAN.

## Oct 22 — CCS mark: the Southwire Growing Green sprig itself (viewer v83)
Owner: "use the same model, you can use it since it's Southwire". The owner-supplied mark is kept at
blender/ref/southwire_growing_green.jpg; `blender/leaf_icon.py` now lifts the sprig off it (any non-white pixel is
leaf, so the grey and green leaves become one solid shape; JPEG specks median-filtered; upscaled 6x, blurred and
re-thresholded for a smooth edge), leaves out the "Growing Green" wordmark, and fills it with one green
(61, 100, 72); the white vein cuts stay transparent. Same screens/ccs_leaf.png, same 20 ft decals in the four gaps on
absorbers A-C. Previews renders/ccs_leaf/ (CL1, CL3). verify PASS, audit CLEAN.

## Oct 22 — CCS absorbers numbered 1-3 (viewer v84)
Owner: "add 1 on the side of absorber A and 2 and 3 for the others". `ccs_lod3.absorber_identity()`: a 24 ft numeral
(1 / 2 / 3 for A / B / C) in the CCS sage on the grey shell under each of the four CCS letterings, centred EL 172
between the EL 130 and EL 200 platforms (checked clear of the risers, piping and the fire-alarm device at EL 156).
The small "ABSORBER A-C" line and the viewer tags keep their letters. Camera CL4 (the three from the south); previews
renders/ccs_numbers/. verify PASS, audit CLEAN.

## Oct 22 — CCS 1 / CCS 2 / CCS 3 on the band (viewer v85)
Owner: "I meant by the side of the CCS on the band, so CCS 1, CCS 2, CCS 3; no need for another number below". The v84
shell numerals are removed. `ccs_lod3.absorber_identity()` now letters each of the four faces "CCS n" (n = 1-3 for
absorbers A-C): the word and the digit are two panels, each tangent to the shell at its own angle so the pair follows
the curve; 9.2 ft DejaVu Bold (the size "CCS" already rendered at), .22 em space, the 28.7 ft pair centred on the face.
The Growing Green sprigs trimmed 20 -> 16.5 ft to keep clear of the wider lettering. Previews renders/ccs_numbers/
(CL1, CL3, CL4). verify PASS, audit CLEAN.

## Oct 22 — CCS over the unit number, framed to the sprig (viewer v86)
Owner: "didn't like that you made it smaller; put the numbers below CCS, same size as before ... CCS 1 in the middle,
the height and bottom the same as the sprig (enquadrado)". `ccs_lod3.absorber_identity()`: on each face "CCS" at its
original 10 ft type (DejaVu Bold, caps 7.5 ft) over the unit digit (1-3 for A-C) in the same type, both centred on
the face; the two lines span exactly the sprig's visible height (ZS = 0.935 x 20 = 18.7 ft, measured from the alpha
of screens/ccs_leaf.png), 3.7 ft line gap, block and sprig both centred at EL 226.5. Line panels 24.5 x 15 ft so the
renderer neither shrinks nor offsets the line; .17 ft corrects the "mm" anchor to the glyph centre. Sprig back to 20 ft.
Previews renders/ccs_numbers/ (CL1, CL3, CL4). verify PASS, audit CLEAN.

## Oct 22 — back to the shell numbers, south and north faces only (viewer v87)
Owner preferred the v84 look ("cleaner; too cluttered with numbers" in the band versions) and agreed to trimming it.
`ccs_lod3.py` restored to v84 (band: CCS + Growing Green sprig at 20 ft, unchanged), with the 24 ft unit numbers on
the grey shell (EL 172) only under the south (-90) and north (90) CCS: on the east / west faces they showed as slivers
at the absorber edges. The band-lettering experiments of v85-v86 are dropped. Previews renders/ccs_numbers/ (CL4, CL1).
verify PASS, audit CLEAN.

## Oct 22 — boiler section: greenfield HRSG, package boiler, brownfield outage + deck slides (viewer v88)
Owner: boilers for gas power, greenfield and brownfield, to talk with the boiler OEMs (Vogt Power, B&W). Kept the
auxiliary boiler's combined-cycle role. All typical, not engineered.
- `aux_boiler.py` (new): AB-1 gas-fired package boiler at LOD 3 in the drawn envelope (x 935-995, y 1450-1540, EL 70):
  D-type casing on its skid, windbox / burner with igniter and two flame scanners, drum heads, water column and level
  transmitters, roof platform with safety valves and the main-steam MOV, FD fan + 200 hp motor + inlet silencer,
  natural-gas train (manual, regulator, SSOV-vent-SSOV, vent line, gas detector), outlet box, economizer, breeching,
  70 ft stack with CEMS platform and caged ladder, deaerator, two feedwater pumps, chemical feed, blowdown tank,
  AB-MCC e-house, EL 17.5 ladder tray to the BMS panel, VFD cable to the fan, scanner cables, MC-HL on strut to the
  gas train, drum-level cable, area lights, signs. Steam line ties into the aux-steam route at (993.4, 1495, EL 12).
  The placeholder block / stack in build_model.py and the old dressing in utilities.py were removed.
- `hrsg_electrical.py` (new): per HRSG a duct burner (gas header up the east-wall slot at y 636, 8 runners with
  flex hose, igniter, scanner, a cable ladder to the DB JB; fuel skid with SSOV-vent-SSOV and FCV at x 676-690,
  y 690-701 between the tray posts; BMS panel; MC-HL on strut; scanner multicable at EL 4.6) and the BFP 13.8 kV
  terminations (tray under the drop's end glands at EL 10.3, 3 x 1/C into an MV terminal box per motor, ground bond).
- `brownfield.py` (new): HRSG 3 outage. build_model.py splits HRSG 3's roof (opening x 943-957, y 674-686) and the
  centre drum-frame stringer. Old HP evaporator module (12 ft wide, 70 ft, weathered) on a spreader bar over the roof,
  tag lines to two crew on the drum walkway; crawler crane (tracks on mats, house, counterweight, 215 ft lattice
  boom, mast, pendants, load lines) at x 1040-1088, y 639-679; new module on a heavy-haul lowboy on the ring road
  (y 907-919); cable work by R2C (two SIMpull Reels on Cradles, sheave, cable up to the HRSG marshalling JB,
  pre-terminated harness crates with QR, cable-recycling bin, cone-and-chain barricade, two-sided outage sign, crew).
- cable_schedule.py / wiring.py: AB-1 devices (FD fan 150 kW, 2 BFP 75 kW, chem 2 x 4 kW, ai 30, di 30, sol 6; LV
  330 kW) and the duct burners (ai 8, di 24, sol 6; 15 kW). brochure/boiler_numbers.json: one HRSG train 705 cables /
  156,200 ft; AB-1 83 cables / 42,430 ft.
- Cameras BX1/BX2 (aux boiler), BH1/BH2 (duct burner, BFP), BB1-BB4 (outage); previews renders/boilers/.
- Deck: `blender/deck_boilers.py` -> renders/deck/boilers/SW-3X1_boilers.pdf (2 slides, 1440 x 810, deck style,
  credit in each footer) + PNGs; talking points renders/deck/boilers/talking_points.md (OEM names only there).
- verify PASS, audit CLEAN; workbook audit unchanged (the known voltage-drop CHECK only).

## Oct 22 — boiler slide 3: the offering, cable circled at every spot
Owner: "one slide at the end with all the offering, circling the cable on each spot, and the cable specs, links, stock
number reference". `blender/deck_boilers.py` slide3(): four scene tiles (BX1 package boiler, BH2 duct-burner skid,
new camera BF1 = BFP 13.8 kV terminations, BB3 outage cable work) with numbered copper circles projected from the
cable's 3D position in the model (bz.project, clamped inside the tile), and a table of 8 products: MV-105 15 kV
(SPEC 46302, #95604599, 500 kcmil), TC-ER power (45252, #95305999, 12 AWG 3/C), ARMOR-X MC-HL (45352, #89052799,
8 AWG 4/C), ARMOR-X MC-HL VFD (45352, #89051899, 3/0 3/C), control TC-ER (45053, #89067701, 14 AWG 5/C),
instrumentation PLTC/ITC SPOS (43303), thermocouple extension (42345), SIMpull Cradle (SPR-CRDL, #67606001); each with
a clickable link to its Southwire page. Stock numbers come from Southwire's catalogue listings found by web search
(southwire.com itself was not reachable from the container to open the pages); one representative size each, noted on
the slide. The deck is now 3 slides (BOILERS n/3); talking_points.md has the same product list.

## Oct 22 — boiler deck: HRSG hero + elevation slides, full-quality renders (5 slides)
Owner: pictures "too dark, not clean, details not there"; then "focus on the HRSG isometric as the hero and details, and
a separate 3D view at an elevation angle", the rest of the plant faded.
- Render script (`blender/SW-3X1_Rev14_blender_build.py`), two new per-camera options in pro_look: `fill` = point
  lights (x, y, z, W, radius ft) for shaded close-ups; `ghost` = dict(keep=item prefixes, glow, alpha): every item not
  kept goes to pale clay (ground to a grey clay), cable / bus / conductor materials glow (HV / MV copper, LV / control /
  instrument amber), the tray / duct-bank items' steel goes mid grey, decals of faded items hidden; restored after
  the render.
- Cameras: ISO1 = HRSG 1 train isometric from the SE (HRSG 2 train, turbine-hall shell and filter houses hidden),
  ELV1 = HRSG 1 from the west at ~6 deg elevation (R1 and the hall shell hidden); both ghosted with the HRSG 1 train,
  BFP-1, SCRB-1, CEMS-1, R2A and the GT1 exhaust duct kept. Framings solved from the projection (see deck_boilers).
  BH2 / BF1 / BB3 got exposure / fill tuning, BX1 / BB1 / BB2 a light exposure lift.
- Full-quality renders (1920 x 1080, 20-64 spp, denoised) in renders/boilers_full/ (deck_boilers prefers them).
- `blender/deck_boilers.py`: 5 slides: 1 overview, 2 "The HRSG, every cable" (ISO1, 8 numbered details placed from
  model coordinates, each with the offering-slide product numbers, 705 cables / 156,000 ft per train), 3 "The train in
  elevation" (ELV1, elevation scale grade / EL 42 / EL 86 / EL 180, 7 callouts), 4 brownfield, 5 the offering.
  The earlier plant-wide iso with the cable-route overlay was replaced at the owner's direction (the overlay code is
  gone; the routed-path data remains in brochure/cables_xray.json).

## Oct 22 — boiler deck slide 4: switchgear room to the HRSG (wiring diagram), 6 slides
Owner: "you're missing the switchgear room ... what are the cable applications there ... a diagram, the breakdown".
`blender/deck_boilers.py` slide_diagram(): a one-line / riser of one HRSG train: GSU-1 / UAT-1 -> switchgear room R1
(SWGR-13.8-1, E82 render inset) -> BFP-1A/B (MV-105 15 kV, 6 cables, 8,400 ft) and the MV feeder to T-R2A -> HRSG
e-house R2A (480 V MCC, DCS I/O, E32 render inset) -> five field legs coloured by application (TC-ER power / VFD,
control TC-ER / ARMOR-X MC-HL, instrumentation PLTC / ITC / RTD, thermocouple extension, fibre / fire alarm from the
control room), each with offering-slide product numbers, cable count and footage summed from the Cable Schedule for
HRSG 1 + BFP-1 + SCRB-1 + CEMS-1 + duct burner / chemical feed / blowdown; an exploded bar of the ~156,000 ft by
application. Gap noted on the slide: the 13.8 kV SWGR-13.8-1 -> T-R2A feeder is not in the cable schedule (only its
control / instrument cables are), so it is drawn but not counted. Deck: 1 overview, 2 HRSG hero, 3 elevation,
4 wiring diagram, 5 brownfield, 6 offering.

## Oct 22: boiler slide 4/5: the wires inside the room, every leg (7 slides)
- Schedule gap fixed (cable_schedule.py): the 480 V secondaries were missing for every unit and load-centre transformer.
  - Added: T-R2A/B/C → R2A/B/C at 10 sets of 4 x 1/C 500 kcmil; T-R3 → R3 and LCT-A/B → LC-480-A/B at 12 sets.
  - Sizing: 125 % of full-load current, so the Audit sheet lists them as bus-duct candidates.
- Correction to the previous entry: the SWGR-13.8-1 → T-R2A primary WAS in the schedule (A-MV-0015, 3 cables, 660 ft); the slide footnote saying otherwise is gone.
- r2a_interior.py (new; runs after hrsg_electrical): R2A is now a shell instead of a solid block.
  - Lifting layer: the roof, west wall and south wall sit on the new layer R2A_ROOF so a cutaway can lift them. The layer is in BASE_SHOW, view A and the viewer ROOFS; viewer view B3 is the R2A cutaway.
  - Lineups: LC-R2A 480 V switchgear (main at the north end), MCC-R2A-1 / -2, VFDs, DCS / marshalling, UPS, 125 V DC battery, panels and FACP.
  - Trays and drops: ladder trays EL 11.4 / 11.9 / 12.4, with drops into every section.
  - T-R2A: the secondary leaves the LV box, crosses to the north-wall sleeve and runs over the room into the main breaker; the MV-105 primary drops off the EL 36 tray into the air terminal chamber.
  - Field exits tie into the existing route risers: the north-wall transit frame at EL 8.9 and the roof glands at (575.75, 644).
  - Also: building wire, the FA loop and detectors, ground bus and a technician.
  - Checks: verify PASS, audit CLEAN.
- Cameras RA1 (cutaway from the SW, R2A_ROOF hidden) and RA2 (inside, east aisle at tray height), both with `fill` lights. Full renders are in renders/boilers_full.
- deck_boilers.py now reads every leg from the Cable Schedule sheet (legs(); the run formula as in the workbook), and asserts the train equals boiler_numbers.json (705).
  - New slide 4 "Inside the room": RA1 with 9 numbered legs and the RA2 inset.
  - Slide 5, the diagram, lists every leg:
    - primary 3 / 660 ft and secondary 40 / 4,800 ft;
    - T-R2A auxiliaries 38 / 3,600;
    - DCS fibre 730;
    - room THHN 2,280 plus 330;
    - CEMS fibre / FA / THHN added to the train rows.
  - Bar: the train (~156,000 ft), then "feeding the room" (86 cables, 12,400 ft), not counted in the train because R2A also serves GT1.
  - Footers now read n/7.
- Follow-up (owner): preview quality only for now. Full renders are listed in renders/RENDER_QUEUE.md and run in one batch at the end.
  - RA1 now hides the plant tray / IPB item (`hide=("Cable trays and isolated",)`); the big pipe over R2A is process piping and stays.
  - Rule going forward: hide that item on close-ups unless tray congestion is the point of the shot.
  - The full RA1 render with trays was deleted; the deck uses the preview.
- ELV1 (slide 3): the ghost keep now also holds HRSG 2, HRSG 3 (stacks, ducts and skids) and the brownfield outage crane, all in real colour. Preview image only; queued in RENDER_QUEUE.md.
- Spot lists (slides 2-4) now name the cable application on every circle (APPNAME in deck_boilers.py; small superscript = product number on the offering slide). Slide 2 stats moved onto the image; slide 4 inset moved to the image's lower left.
- references/boilers/README.md: public one-lines (Mill Creek 6 KY PSC 2025-00045, HRSG MCC 1A/1B), HRSG package spec, duct-burner bulletins, MV/TC cable sample specs, standards list. Downloads blocked by the container network policy: links only.
- Boiler deck slide 6 'What the spec calls for' (SPEC list in deck_boilers.py): 8 applications -> spec requirements and standards -> Southwire product / SPEC; real-plant check (Mill Creek 6 one-line, unnamed on the slide) and design / install standards. Deck is now 8 slides; talking points have a matching section.
- Boiler deck slide 6 'Levels, ratings and the cable they drive' (LEVELS in deck_boilers.py: 230 kV to the signals, the rating per level and the cable each drives; key-fact tiles: 750 kW at 480 V, 2 x 5 MW pumps, 3,007 A, 74 % instrument cables, arc flash). The spec slide is now 7; the deck has 9 slides.
- Boiler deck slide 2 'How an HRSG works' (slide_basics / SECTIONS in deck_boilers.py): vector gas-path schematic with 7 tube sections and the stack, typical gas temperatures, HP / IP / LP drums, the counterflow water / steam loop with typical pressures, the cable at each section, and 4 fact tiles. The deck is now 10 slides; RENDER_QUEUE slide numbers updated.
- Boiler deck slide 3 'What goes in, what comes out' (slide_cycle in deck_boilers.py): 3 x 1 cycle flow (gas and air in, GTs -> HRSGs -> ST -> ACC -> condensate / feed pumps back, generators -> GSUs -> grid; outputs stack gas and heat to air; makeup water), plus 4 Q&A tiles (spent steam, closed loop, power split, cable on the loop). The deck is now 11 slides.
- Slide 3 / 2 accuracy pass: spent steam 100-150 °F (ACC), condensate pumps to the HRSG LP end and feed pumps from the LP drum / DA to HP / IP, reheat loop shown, GT exhaust 1,500-2,000 lb/s per GT.
- Slide 2: 'Why it's there' panel (the HRSG's purpose: ~1/3 more power from the same fuel, ~40 % -> 60 %+, SCR housing, duct firing, the bridge between the two halves). Footnote changed to H-class. Talking points updated.
- Slide 2 panel restyled as a quick review (owner liked the chat format): 'What it is' (without it / with it / the payoff) and 'Fun facts' bullets (.qr list style).
- Boiler deck slide 10 'Pain points and the answer' (PAINS / VALUES in deck_boilers.py): 9 technical pain points, 7 value points, closing line. The deck is now 12 slides (brownfield 11, offering 12).
- cems_lod3.py (new, after r2a_interior): CEMS shelters 1-3 at LOD 3 (skid, insulated shell, door, HVAC, XP boxes and conduit, strobe / horn, cal-gas rack, sample-line bulkhead, conduit stub-ups to an entry JB; inside: 3 analyzer racks, sample conditioning, DAHS / PLC, transformer / panel, heated-line controller, ladder tray with drops). Roof, east and south walls on the new layer CEMS_ROOF (BASE_SHOW, view A, viewer ROOFS). Cameras CM1 (exterior), CM2 (cutaway), CM3 (stack platform), show=base. Deck slide 7 'The stack and the CEMS shelter' (CEMS_SPOTS; cables per shelter from the schedule, 31 / 7,200 ft). The deck is now 13 slides. Previews only; queued.
- Stack top (owner, Oct 23): the schedule gains per-stack aviation obstruction-light feeds (TC-ER) and light-failure alarms to the DCS (CT 7/C); tools/boiler_numbers.py (new) recomputes the HRSG train in boiler_numbers.json: now 707 cables / 157,380 ft (texts updated: 707, ~157,000, ~472,000, 78 circuits). cems_lod3.stack_top: lighting JB + photocell at the top platform, leads to the lights, open flue, test clamps on the down conductors. Camera CM4; slide 7 third inset. Previews; queued.
- R2A interconnection trays (owner, Oct 23): r2a_interior.split_plant_trays moves the plant tray / riser parts in x 562-640, y 640-760 into the item 'R2A interconnection trays ...' (boxes and axis-aligned rods cut at the edge), so RA1 can hide the overhead rack yet show the risers and drops (the audit allows the new item). New camera RA3 (wide interconnection view, process piping hidden) as a second inset on slide 6; callout 8 is on the roof riser.
- presentation/Nov11_run_of_show.md: the Nov 11 training (60 min, ~440 attendees) run of show: fundamentals 10, 7-stop 3D tour 30, cable takeaways 9, Q&A 8; talk track per stop, backup plan, checklist to Nov 11 (dry run Nov 4), parking lot. Scope freeze: only work that serves a tour stop.
- Viewer: second guided tour 'Nov 11' (presentation/tour_nov11.json, 21 views in 7 chapters: grid, turbine hall, HRSG + e-house (incl. new e-house, CEMS, stack-top cameras), cooling, modular, BTM, fuel; opening + cable X-ray close). Template: TOUR2, chapter bar (#tchap), keys 1-9 jump to a chapter; the original 51-stop tour unchanged. Verified in headless Chromium (navigation, chapters, Esc, no page errors); screenshots too slow with software GL.
- Boiler deck slide 2 'Every boiler, the cable behind it' (BOILER_TYPES in deck_boilers.py): 7 boiler types (HRSG and package in the model; utility / conversions, FBC / biomass / WtE, once-through, electric (newest market, MV-fed), waste-heat) with the cable story and products, plus a pattern tile. The deck is now 14 slides; talking points, run of show and render queue renumbered.
- Slide 2: drawn example along the bottom, a utility boiler converted to gas (gas train, burners, furnace + drum, backpass, SCR, air heater, ESP / baghouse, FD / ID fans, stack) with 5 cable callouts; cards shortened to make room. Talking points updated.
- Boiler deck slide 3 'The electric boiler: a straight MV cable sale' (slide_eboiler in deck_boilers.py): drawn one-line from grid / renewables to the 13.8 kV switchgear, MV-105 parallel sets, electrode boiler (3 electrodes, water conducts), steam out, pump, PLC, ground; 5 cable callouts; 4 fact tiles; typical-values caveat. The deck is now 15 slides; talking points, run of show and render queue renumbered.
- Slide 2 (owner, Oct 23, after the B&W / Base Electron news): the utility card is retitled 'new gas-fired or converted' with AI and data-centre power; the example gets a caption ('the same layout is being built new for AI campuses: 300 MW per unit'). The B&W / Base Electron / Applied Digital facts (Mar 4, 2026 full NTP: $2.4 B, 4 x 300 MW gas boilers + STGs, 1.2 GW option) are in the talking points only.
- Boiler Row (owner, Oct 23: "an important message in visual ... utility boilers, gas boilers and electric boilers"): boiler_row.py (new, after cems_lod3) on the new layer OPT_BOILERS (+ BOILER_ROW_ROOF for the electric-boiler cutaway; viewer ROOFS). East of AB-1, south of the CCS road: UB-1 300 MW-class gas-fired utility boiler (representative: 170 ft clad house, 12-burner front with platforms, gas train + BMS in MC-HL, FD fans on 13.8 kV, backpass / SCR / air heater, 230 ft stack), its STG hall with GSU, EB-1 30 MW electrode boiler (vessel, 3 bushings, pumps, PLC; its 13.8 kV e-house; MV-105 3 parallel sets on a ladder tray through the wall and up to the bushings), BOILER ROW sign. Showcase only: the SW-3X1 cable schedule is unchanged (6,003 runs). tools/boiler_row_numbers.py (new) writes typical take-offs to boiler_numbers.json: UB ~1,843 cables / 972,360 ft (66 % instrument), EB 97 / 27,230 ft (18 x 750 kcmil MV-105, 1,255 A). Cameras BR1 (aerial from the south), BR2 (burner front), BR3 (EB-1 cutaway). Boiler deck slide 4 'Three boilers, three cable stories' (ROW_SPOTS; aerial with 7 named spots, two insets, three cards). The deck is now 16 slides; talking points, run of show (+ Boiler Row line closing stop 3, PDF rebuilt), render queue renumbered. Nov 11 tour: 22 views (Boiler Row added at the end of chapter 3). verify PASS, audit CLEAN. Previews only; BR1-3 queued.
- Boiler Row relayout, "Steam Street" (owner, Oct 23: "not fluid ... should this look like a factory?"; layout sketch approved with "Go"): boiler_row.py adds a copper-coloured spine rack along the fronts (y 1516, EL 22 trays with control / instrument / MV cable, EL 31 steam header, condensate and fuel gas; west end ties into AB-1's aux steam; drops to UB-1 gas train, the STG and the EB-1 e-house), a shared 'Boiler Row control room and MCC' (cable hub; its cable rises into the spine tray), EB-1 steam storage (accumulator) fed from the boiler and tied to the spine, the 13.8 kV feeder marker strip with red posts, bay pads and painted bay plates (1 Package / 2 Utility / 3 Electric). UB-1 moved 8 ft north, stair tower to the NW corner, BMS beside the gas skid. BR1 re-aimed (higher, from the south); slide 4 spots now 1 AB-1, 2 burner front, 3 FD fans, 4 spine, 5 control room, 6 EB-1, 7 steam storage; tour stop camera and text updated; talking points explain the layout and the 'factory' question. verify PASS, audit CLEAN; previews, queued.
- Boiler Row realism pass (owner, Oct 23: "what are these circles ... make this look like a boiler power plant ... the back?"): UB-1 burner front at LOD 3 (12 burners with quarl, register housing, gas gun, burner gas valve, flame scanner, igniter + transformer, air-register drive; per-level gas header, platform tray, level JB A/B/C; MC-HL flex runs; BMS riser; one main gas riser); exposed steel columns, roof safety-valve vents with silencers, hot-air duct air heater -> windbox, elevator; main steam + hot / cold reheat to the STG. Back bay (new items): UB-1 SST-A/B (13.8 kV, firewall, containment) and the UB-1 13.8 kV switchgear e-house, MV-105 on a ladder tray behind the boiler to the FD fan motors; gas metering and pressure-reducing station (filter-separator, two regulator runs, meter, RTU, MC-HL on strut) feeding the gas train. Cameras BR4 (back bay) and BR5 (burner close-up). Slide 4: spot 8 (switchgear + transformers), BR5 inset replaces the spine close-up. verify PASS, audit CLEAN; previews, queued.
- AB-1 moved to the modular yard (owner, Oct 23: "move the auxiliary boiler ... so it looks like a real boiler utility plant"): aux_boiler.build draws it as before and turns it 90 deg anticlockwise into x 1534-1624, y 1300-1360 (_mv: x' = 3074 - y, y' = x + 365; parts, decals and the operator; item fp updated). New routes in utilities.routes: aux steam from AB-1 up the pipe corridor (x 1527) to the x 1040 header at y 881; fuel gas from the gas yard (x 1612.5); duct bank off the x 1500 bank to the AB-MCC. The old aux-steam header now starts at the Boiler Row spine (x 998). verify: owner-approved relocation list MOVED (reported as RELOCATED, not matched; 210/210). Cameras BX1 / BX2 and the BX1 deck spots transformed the same way; the stale BX1 full render deleted. Boiler Row: UB-1 cooling tower (3 cells, fan stacks with open throats and blades), CW pumps CWP-A/B on 4.16 kV (MV-105 stub-ups), discharge below grade, CT MCC on the x 915 duct bank; bay plates now UTILITY / ELECTRIC (+ PACKAGE at AB-1). Camera BR6; slide 4 spot 1 = cooling tower; card 1 says 'in the modular yard'; tour text, talking points, render queue. Schedule still 6,003 runs. verify PASS, audit CLEAN.
- UB-1 cooling tower restyled to match the CCS cooling tower (owner, Oct 23: "needs to be consistent"): same build as ccs.cooling_tower (water basin, 'tower' casing EL 3-40, grating deck EL 40-42, concrete cell walls, flared 'tower' fan stacks to EL 50 with 8 'fan' blades, 'fanhub' throat, gearbox, shaft and motor outside the stack, intake louvres, deck rail, north-end stair, teal 'waterline' hot-water header with a riser into each of the 3 cells). BR6 re-aimed to show both towers and the burner front. verify PASS, audit CLEAN.
- UB-1 burner front completed (owner, Oct 23: "is there anything missing?"): stair tower to burner levels A-C (west end, switchback flights, landings, sign), platform knee braces and end rails, platform lights with their circuit, windbox stiffeners, flame-scanner cooling air (2 blowers on 480 V motors with TC-ER power, riser, level headers, a hose to each scanner), three operators. Camera BR7 (wide burner front). verify PASS, audit CLEAN; preview, queued.
- Boiler Row support yard (owner, Oct 23: "still some space ... anything else?"): boiler_row.support_yard on the free land x 782-878, y 1502-1645 and at the stack: UB-1 condensate storage tank (30 ft dia) + 2 transfer pumps (480 V); UB-1 emergency diesel generator (480 V, ~2 MW; sub-base tank, silencer) with a ladder tray of 1/C 500 kcmil into the 13.8 kV e-house; Boiler Row cable laydown (16 SIMpull reels by circuit: MV-105, MC-HL, TC-ER, PLTC; SIMpull Truck; sign; operator); UB-1 CEMS shelter beside the stack with the heated sample line to EL 120 and cables to the MV tray. Camera BR8. verify PASS, audit CLEAN; preview, queued.
- Owner, Oct 23: "didn't like" the reel laydown; AB-1 brought back next to Boiler Row instead. aux_boiler now shifts AB-1 by (-151, +105) without rotation into x 784-844, y 1555-1645 (where the laydown was); its steam runs to the Boiler Row aux-steam header (route 844,1600 -> 852,1552 -> 994,1552 -> 998,1510), the AB-MCC feeder is a duct bank off (915, 1450) via x 778; the modular-yard routes were removed. Reels, truck and sign deleted; the PACKAGE BOILER plate is in front of AB-1. verify MOVED text, BX1 / BX2 cameras and BX1 deck spots updated; slide 4 card 1 text; tour, talking points, render queue. verify PASS, audit CLEAN.
- UB-1 joined power-station block (owner approved the sketch, Oct 23): boiler_row.heater_bay (x 1110-1160, y 1530-1598, EL 105; same cladding and copper coping as the turbine hall; control-room window band, spreading-room vents and sign, roller door, deaerator and storage tank on the roof, cable from the spine tray through a wall sleeve into the spreading room). Turbine hall raised to EL 80, 1632 deep, copper coping, south-face ribs and sign; roof trimmed on the bay side. CEMS shelter moved behind the bay (y 1600-1614). Slide 4 spot 5 = heater bay / unit control room (cable spreading room); spot 4 moved east on the spine. verify PASS, audit CLEAN.
- Boiler Row ground name plates (UTILITY / ELECTRIC / PACKAGE BOILER) removed (owner, Oct 23); the bay pads stay. BR1 re-shot, deck rebuilt. verify PASS, audit CLEAN.
- Boiler Row cable / equipment / pipe audit (owner, Oct 23): tools/boiler_row_audit.py (new; dangling cable and pipe ends, equipment with no cable or conduit, floating part groups, cables / pipes through solid bodies; reviewed exceptions listed in ACCEPT with reasons). First run: 24 / 10 / 27 / 13. Fixed: UB-1 gas line ran through SST-A/B (now via 929,1584 -> 929,1600 -> 998,1600); main gas riser moved downstream of the safety shut-offs (east end, x 1067), level gas headers capped; MC-HL drops land on the valve actuators (UB-1 gas train, metering station); metering-station filter outlet connected; scanner cooling-air riser reaches the top header, header ends capped; spine drops go below grade, east-end blind flanges; EB-1 pump suctions reach the vessel; AB-1 steam outlet meets the aux-steam route (842.4,1600), AB-1 MOV actuator cabled, chemical-feed panel fed, feedwater discharge starts at the pump; SST-A/B now 13.8 / 4.16 kV with cable-box terminations (open bushings removed) and a duct-bank incomer into the UB-1 switchgear (route from 915,1450); GSU 230 kV take-off gantry with cable terminations and HV cable down; burner stair tower gets west landings and stringers. Result: CLEAN (13 reviewed and accepted). cable_schedule.py now excludes OPT_BOILERS (the condensate tank had matched a 'tank' rule: +4 runs); plant schedule 6,003 runs, 21,189 cables, 6.43 M ft. verify PASS, audit CLEAN.
- Shared cooling (owner, Oct 23: "use the CCS cooling ... add more cooling towers at the CCS"; AB-1 stays where it is): the Boiler Row 3-cell tower, its CW pumps and CT MCC removed. boiler_row.shared_cooling adds 8 cells (4 x 2, x 240-440, y 1740-1860) at the west end of the CCS cooling tower in the same build (basin, casing, deck, stacks with fans, gearbox, shaft, motor, louvres, rails with posts, the hot-water header continued with risers and an end cap), CWP-A/B on 4.16 kV motors (MV-105) at the west end, the UB-1 cells' MCC (duct bank off the CCS feeder route at y 1868), and the buried CW supply / return to the UB-1 turbine hall as a marker strip with posts (y 1700, then x 1150 across the road). CCS tower info notes the sharing. BR6 re-aimed at the new cells; slide 4 spot 1 = shared cooling tower; tour, talking points, render queue; boiler_row_audit region widened. verify PASS, audit CLEAN, Boiler Row audit CLEAN, schedule 6,003 runs.
- AB-1 back on its drawn place (owner, Oct 23: "so it fits in the shot"): aux_boiler DX = DY = 0 (relocation kept as a hook); routes back to the drawn aux-steam start (993.4, 1495) plus the spine tie-in (998, 1510 -> 998, 1495); the AB-1 west routes removed; verify MOVED empty, footprints 211/211 again; BX1 / BX2 cameras and BX1 deck spots back to the original coordinates; slide 4 spot 1 = package boiler AB-1; Boiler Row audit ACCEPT patterns updated. The west land keeps the condensate tank, EDG and gas metering. verify PASS, audit CLEAN, Boiler Row audit CLEAN, schedule 6,003 runs.
- AB-1 CEMS shelter (owner, Oct 23: "is there a CEMS shelter missing?"): every other stack had one. aux_boiler.cems_shelter: walk-in shelter north of the AB-1 stack (x 949-961, y 1541.5-1552), HVAC, door, sign, probe box on the EL 50 platform, heated sample line down the stack, power / signal / fibre conduits up. Its 8 schedule rows (CEMS rule) are plant scope and kept: schedule now 6,011 runs, 21,217 cables, 6.44 M ft (run of show + PDF updated); boiler_numbers.json aux block now includes the shelter: 111 cables, 56,530 ft (slides 1 and 4, talking points). Boiler Row audit covers the shelter. verify PASS, audit CLEAN, Boiler Row audit CLEAN.
- UB-1 CEMS shelter moved from the dark gap behind the heater bay (under the MV tray) to the open north side of the stack by the road (x 1121-1137, y 1633-1646): sign, door and cal-gas rack facing the road, heated sample line straight up the stack to EL 120, conduits up from grade. Camera BR9 (north side, sun from 330, exposure +.3). verify PASS, audit CLEAN, Boiler Row audit CLEAN.
- Skid pre-wire workstation moved (owner, Oct 23: crowded by the shared cooling-tower cells): skid_prewire DX, DY = -1931, 8 puts it on the open strip between the cable reel yard and the inlet chillers (parts x 70-206, y 922-1026; fp 66-206 x 918-1030); the area sign and lowboy follow (+10, -790); cameras E95 / E96 moved the same; item name / info, docstring and the EPC brochure caption updated. The renders/epic E95 / E96 full renders are stale (queued). verify PASS, audit CLEAN.
- Modular GT packages (owner, Oct 24: "other gas power plants on the modular yard ... different modular ones"): modular_packages.py (new, after skid_prewire; layer OPT_MODX, not in the register): AX-1 factory-modular aeroderivative package (LM2500XPRESS class, ~35 MW; enclosure, inlet filter house module on top, exhaust and 60 ft stack, control module, fin-fan lube cooler, fuel-gas module with MC-HL; module joints marked in copper with plug-in MV / control / instrument interconnects) at x 2015-2115, y 1008-1054, and IG-1 industrial GT package (Titan 250 class, ~23 MW; single skid, inlet on top, 50 ft stack, same auxiliaries) at x 2152-2240. Generator leads MV-105 down into new OPT_MODX_ROUTES duct banks to MOD-EH. Cameras MP1 (aerial), MP2 (module joint). Run of show stop 5 + parking lot, Nov 11 tour text, render queue. Boiler Row audit extended to AX-1 / IG-1 (CLEAN). verify PASS, audit CLEAN, schedule unchanged (6,011 runs).
- IG-2 larger industrial GT (owner, Oct 24: "larger unit, this side"): modular_packages.large_unit on the open corner east of the 230 kV switchyard (pad x 2088-2345, y 140-222): SGT-800 class ~60 MW simple cycle; 120 ft enclosure (generator west), filter house on top, exhaust diffuser, SCR + CO catalyst with ammonia skid, 100 ft stack with test-port platform and CEMS shelter, control module, fin-fan lube cooler, fuel-gas module (MC-HL); generator on isolated-phase bus to GSU-IG2 13.8 / 230 kV, take-off gantry at x 2075 and 230 kV conductors onto the D6 breaker 2 bushings (SWYD_FUTURE bay). Layer OPT_MODX, not in the register; schedule unchanged. Camera MP3. Run of show (stop 5, parking lot) + PDF, tour text, render queue; Boiler Row audit region now the whole east side (CLEAN). verify PASS, audit CLEAN.
- IG-2 removed (owner, Oct 24: it repeated the SC-1 / SC-2 simple-cycle story): large_unit() deleted from modular_packages.py, camera MP3 and its preview removed, run of show (stop 5; parking-lot note says it was tried and removed) + PDF, tour text, render queue and the audit name list updated. The corner east of the switchyard is open again; bay D6 stays a future build-out. verify PASS, audit CLEAN, Boiler Row audit CLEAN, schedule 6,011 runs.
- AX-1 / IG-1 made a mirrored pair like SC-1 / SC-2 (owner, Oct 24): stacks face each other on the SC stack lines (x 2052 and 2116.5). AX-1 enclosure shortened to 46 ft (pad x 1984-2072, clear of the cable spine at x <= 1980); IG-1 built then mirrored by modular_packages.mirror_x about x = 2142.25 (pad 2096-2184). Generator-lead routes moved (AX-1 x 1987.5 straight to MOD-EH; IG-1 from x 2180.5). MP1 / MP2 re-aimed and re-rendered. verify PASS, audit CLEAN, Boiler Row audit CLEAN.
- Oct 24: Boiler Row and the modular yard closed for Nov 11 (owner agreed; fixes only). Render queue gains E43 / E89 (zone slides 12 and 3 may now show the moved skid pre-wire workstation). Run of show parking lot: CHP / cogeneration and linear generators as possible later plant types.
- Nov 11 training deck v1 (owner, Oct 24): blender/deck_training.py (new) -> renders/deck/training/SW-3X1_Nov11_training.pdf + training_NN.png, 17 slides in the boiler-deck style: title (E123, no email on the cover), agenda, why gas now (three dashed placeholders for Southwire market figures), boiler slides cycle / basics / spec / value reused with re-numbered footers and kickers, the 16-zone overview, seven tour-stop slides (render + does / electrical system / where the cable goes + one-line quote, from the run of show), the whole plant in one number (computed from the cable schedule: 6.4 M ft, 6,011 runs, 21,217 cables, footage by type as a single-series bar), three things to remember + Q&A. Run of show points to it. Images: stop 5 uses the MP1 preview (full render queued).

## Oct 24: training deck v2 (images and logo)
- Title: K15 "Path of Power" brochure picture (switchyard and 230 kV towers in front, turbine hall, ACC, LNG carrier at the terminal), plus the Southwire Power Generation Solutions logo (blender/deck/southwire_pgs_logo.png).
- Overview (slide 6): K1 campus aerial with the marine terminal and the 7 tour stops listed beside it (replaces slide19_zones).
- Stop 1 (switchyard): E20, an eye-level view of the switchyard with the ACC and turbine hall behind.
- Q&A card: logo added.

## Oct 24: training deck, latest renders
- `pic()` in deck_training.py now picks the newest render of each view: the boilers_full copy, the raw `*_pro.png` (the Oct 17 full renders the strategy deck and brochure use) or `*_pro_clean.jpg`. The Oct 8 preview JPGs were being used before. Large PNGs are embedded as JPEG q90 (the PDF is about 9.5 MB).
- Stop 2: HALL9_hero_cable (the strategy deck's "Three turbines, one tray stack"). Stop 5: E77 (the "Power that moves" page). Stop 1 now gets E20 at full quality.

## Oct 24: training deck, market section (22 slides)
- The "why gas now" placeholder is replaced by six market slides rebuilt from the Oct 6 PowerGen channel deck (pages 3, 5-10, 14) in the training-deck style: at a glance; load growth plus US gas capacity added 1996-2026 (bar values read from the PDF geometry); turbine backlogs (OEMs anonymised as OEM 1-3); the ~$1.2B cable prize by PO year (named vs allowance split from the PDF geometry); the project register by status and top states; Q3 progress.
- Names (OEMs, owners, EPCs, the channel partner) are kept in the run of show, not on the slides. Agenda: market and fundamentals 15 min, tour 25 min. The run of show and its PDF are updated.

## Oct 24: training deck, state heat map (23 slides) and JPG export
- New slide 8, `s_map`: the state tile heat map from page 10 of the Oct 6 deck (values and grid read from the PDF text layer), plus owner × site bars and site classes. The register slide's top states are corrected: AZ is 6.1 GW, not 8.1.
- JPG copies for phones: renders/deck/training/jpg/slide_NN.jpg, plus contact sheets market_slides_3-9.jpg and all_slides.jpg (written by hand this time, not by deck_training.py).

## Oct 24: training deck, Q3 progress slide out (22 slides)
- The "From discovery to execution" slide was removed at the author's request. `s_q3` is kept in deck_training.py, unused. The deck now writes the JPG copies itself: jpg/slide_NN.jpg, market_slides_3-8.jpg and all_slides.jpg. The run of show is renumbered.

## Oct 24: training deck, fundamentals from the thermal narrative (26 slides)
- Four new slides from the PowerGen thermal narrative (pages 1-4), restyled: s_blackbox (9), s_anatomy (10), s_owners (13) and s_corridor (14). They sit around the cycle and HRSG slides (11, 12), and the corridor leads into the campus overview (15). Page 5's pipeline figures ($470M, 17 projects) are a different basis from the market slides' $1.2B and 386, so they are left out.
- Agenda: market and fundamentals 18 min, tour 22 min. The run of show is updated. A fundamentals_9-14.jpg contact sheet is added.

## Oct 24: training deck, fundamentals rework (28 slides)
- Slides 9 and 10 merged into `s_box` (the black box, opened). The POI corridor slide is replaced by `s_follow`: cable by plant area from the cable schedule (zones A-K grouped along the flow; the black box holds 44% of 1,212 mi) plus a plain definition of the POI. It no longer calls upstream "not our fight".
- New: `s_types` (simple cycle, combined cycle, engines, aeroderivative, plus a units strip), the voltage ladder (`db.slide_system`, reused) and `s_buy` (who buys, and when). Owners slide: plain-English IPP gloss, "our sales focus".
- Order: market 3-8; fundamentals 9-17; tour stops 18-24; takeaways 25-27; close 28. Agenda: 22 / 20 / 8 / 7 min. The run of show is rewritten for 9-17.
- s_q3, s_blackbox, s_anatomy and s_corridor are kept in the script, unused.

## Oct 24: training deck, greenfield and brownfield (29 slides)
- New slide 16, `s_sites`: the register's five site classes (greenfield grid-connected 77.0 GW, data-centre / BTM 54.5, coal-site repower 41.3, expansion 21.4, industrial captive 11.6), each with a model render and its cable implications, plus a band on running-plant work (outages, HRSG module replacement). Who buys moves to 17, the campus to 18, tour stops to 19-25, close to 29. The run of show is updated.

## Oct 24: training deck, step-back slide (30 slides)
- New slide 3, `s_system`: every way we make electricity (EIA 2025 shares: gas 41, nuclear 18, coal 17, wind 11, solar ~7, hydro 6; firm vs variable tags) and the 2026 planned additions (86 GW: solar 43.4, batteries 24, wind 11.8, gas 6.3; the 6.3 matches the 2026 bar on the capacity chart). Three "why gas" points; "Southwire cables every one of these; today we focus on gas". Everything after it shifts by one (market 4-9, fundamentals 10-19, stops 20-26, close 30). The run of show is renumbered.

## Oct 24: training deck, black-box intro back (31 slides)
- `s_blackbox` (the input / black box / output circles) is back as slide 10 and opens the fundamentals; `s_box` is retitled "Open the box: the physical anatomy" (slide 11). Later slides shift by one (stops 21-27, close 31). The run of show is renumbered.

## Oct 24: training deck, "four families" opener (32 slides)
- New slide 3, `s_sources`: how electricity is made, in four families (thermal with gas highlighted, water and wind, direct, storage), firm/variable tags and what is in SW-3X1. The EIA mix slide is retitled "The mix today, and why we zoom in on gas" (slide 4). Later slides shift by one (market 5-10, fundamentals 11-21, stops 22-28, close 32). Agenda: market and fundamentals 23 min, tour 19 min.

## Oct 24: training deck, definitions slide first (32 slides)
- `s_blackbox` is generalised to "Every power plant is this" (source / input → black box / conversion → power / output, with definitions) and moved to slide 3, ahead of the four families (4) and the mix (5). Market 6-11; "Open the box" (12) picks the black box back up for gas. The run of show is updated.

## Oct 24: training deck candidate slides (A-I), for the author to pick
- `blender/deck_training_candidates.py` writes renders/deck/training/candidates/: A how a generator works, B the grid journey (generator to light switch), C a day on the grid (illustrative load curve), D front vs behind the meter, E cable 101 (families plus footage shares from the schedule), F what a plant does to a cable, G future fuels (H2, CCS, batteries), H units and scale, I glossary. They are not in the main deck yet; move the picked ones into deck_training.py's plan.
- Candidate J, "A modern gas plant is more than the power block": six model renders with their cable (private 5G monopole with massive-MIMO, T5G1; EV charging + solar carport, E10; BTM data centre, E47; LNG carrier at the berth, C2; hydrogen tube-trailer bay, E108; carbon capture, E68).

## Oct 24: training deck, picked candidates in (37 slides)
- B, C, E, F and J are in the main deck, built from deck_training_candidates.py (the footer is switched to the deck's own): C day on the grid (14), B generator to light switch (17), E cable 101 (19), F what a plant does to a cable (20), J the modern campus (25). Agenda: welcome 2 / market and fundamentals 28 / tour 18 / takeaways 6 / Q&A 6. The run of show is updated.

## Oct 24: combined cycle on the model (slide 15)
- New camera CC1 (power block from above, hall roof off; preview at renders/training/CC1_pro_clean.jpg, queued for the full batch). New candidate K, `c_combined`: seven numbered steps on the render with gas, steam, water and power arrows, a step list with the cable for each step, and "burn the gas once, use the heat twice". It replaces the boiler-deck flow diagram as slide 15 (the diagram is the backup). The run of show is updated.

## Oct 24: combined cycle, take 2 (40 slides)
- The single annotated slide was rejected. It is replaced by a four-slide build, `c_cc(step)` in deck_training_candidates.py (slides 15-18): the CC2 render is darkened; each step lights its equipment (model footprints projected through the CC2 camera, convex hulls, the clip shows the photo inside) and draws glowing flows along the real routes (air, exhaust, stack, steam, water, power). Steps: gas turbine, HRSG, steam turbine, then all with the payoff numbers. There is a step tracker under the title. The run of show and render queue are updated.

## Oct 24: cable X-ray slide (41 slides)
- `c_xray` (candidate P, deck slide 23 after Cable 101): the CC2 aerial, near-black, with every cable route from brochure/cables_xray.json projected through the CC2 camera and glowing by type. Each path takes the colour of the group with the most cables on it; width scales with the log of the count; it is clipped to the image area. The side panel describes the five types with whole-plant counts and miles (21,138 cables). The run of show is updated.

## Oct 24: one scope per number
- Cable X-ray (slide 23) now counts and draws only what the picture shows: the power block plus the ACC (zones A and B, `XR_ZONES`): 8,234 cables, about 440 mi. The combined-cycle payoff (slide 18) uses the same 8,234. The whole-campus totals (~21,000 cables, ~1,200 mi) appear only on slides labelled "whole campus" (Cable 101, Follow the power, The whole campus in one number). The run of show has the method answer for Q&A.

## Oct 24: X-ray "before" slide (42 slides)
- New `c_xray_intro` (deck slide 23): the CC2 aerial in full colour with six projected leader-line tags (gas turbines, HRSGs, stacks, steam turbine, ACC, step-up transformers) and the line "Next: take all of it away". The X-ray reveal follows as slide 24. The run of show is renumbered.

## Oct 24: copper X-ray of the CC2 view (43 slides)
- tools/xray_capture/cams_cc.json captures the CC2 camera in the viewer's copper X-ray, then electrify.py: renders/training/XR_CC2_copper.jpg (the README has the commands). New `c_xray_copper` (slide 24) is the reveal; the coloured X-ray (slide 25) is retitled "Now sort it by job: five kinds of cable". Three clicks on one view: 23 normal → 24 copper → 25 by type. The run of show is updated.

## Oct 25: training deck framing (55 slides: main 1-48, backup 49-55)
- New in deck_training.py: `s_why_you` (3), section dividers `s_div` (4, 8, 15, 33, 42; backup 49), `s_offer` (44, the whole-plant offer replacing the HRSG spec slide), `s_simpull` (45), `s_quiz` (46; the answers in backup 50), `s_resources` (48, with the PGS team), `s_sources_app` (55).
- Moved to backup: four ways to burn gas (51), how an HRSG works (52), follow the power (53), the HRSG spec (54). Boilers slide_value (pain points) is out.
- The JPG export writes section sheets (opening_and_market, inside_a_gas_plant, tour_and_close, backup) plus all_slides. The run of show has a slide map and talking points for the new slides; presentation/customer_story_form.md is for the one customer-story slide still to come.

## Oct 25: power-block snapshot moved
- The labelled full-colour power block (`c_xray_intro`) now opens the combined-cycle build as slide 18 (kicker "Combined cycle · the power block", caption "Next: how it makes power, one stage at a time"); the build is 19-22. The X-ray now runs Cable 101 (25) → copper (26) → by type (27). Still 55 slides.
- Then the X-ray pair moved up to follow the build on the same view: 18 snapshot → 19-22 cycle → 23 copper X-ray → 24 by type → 25 generator to light switch → 26 voltage ladder → 27 Cable 101.

## Oct 25: three buckets of cable (56 slides)
- New `s_buckets` (slide 32, after Who buys): 1 inside the packages (OEMs, e-house and package builders; not in the 440 mi), 2 between the packages (EPC or electrical contractor; most of the miles), 3 to the grid (HV contractor or utility). "Starting in the e-house is not the same as being bought by the e-house builder. Cover both." Main deck 1-49, backup 50-56; the run of show slide map is rewritten.

## Oct 25: training deck picture pass (57 slides)
- Pictures from the existing library on: four families (6: photo circles plus the solar carport and battery yard), open the box (16: one render per step), generator to light switch (25), Cable 101 (27: the cable cross-section icons), what a plant does to a cable (28: a thumbnail per row), who buys (31: one render per phase), the offer (46: icons per row), the whole campus in one number (45: campus behind), take-aways (49: E7 hero), resources (50: viewer and brochure covers).
- New `s_hub` "Where every cable starts" (33): the R1 cutaway (E85) plus switchgear (E82), MCC/VFD (E84) and control room (E86). Main deck 1-50, backup 51-57. The render queue lists the preview-only views to re-render.
- PDF size: `pic()` now embeds every image over 250 KB at slide resolution (JPEG q84, max 1920 px; icons as 360 px PNG), and the merge saves with garbage=4, which de-duplicates images repeated across slides: 66 MB down to about 29 MB. Do not use pymupdf rewrite_images: it breaks the CSS-gradient patterns.
- Small pictures were unreadable (author, Oct 25): the stress-table thumbnails (slide 28) and the four-families photo circles (6) are out; slides 16, 25 and 31 (now 17, 26, 32) use `capimg()` (taller image with its name on it, for example "M&R station", "Step-up transformers", "The reel yard").

## Oct 25: why a 3D model (58 slides)
- New `s_story` (slide 4): V0-V1 March concept images (the author's three AI-style illustrations, stored in renders/training/history/v0_*, v1_*: unmeasurable, 11/138 kV), then V2 September (SK-3X1 drawing set sheet 01 and the Sep 26 first 3D render, blender/A_photo), then V3 today (E123 and the copper X-ray), plus four "why we built it" points. Main deck 1-51, backup 52-58; the run of show is renumbered.
- Then four steps: V0 March (the author's Southwire-branded concept pair, history/v0_branded.jpg, v0_ghost.jpg), V1 March (the colour-coded cable concepts), V2 September, V3 today.
- V1 now shows four images as a 2 x 2 grid (adds history/v1_turbine_hall.jpg and v1_hrsg_trains.jpg).
- Corrected (author): V0 = the four colour sketches, V1 = the Southwire-branded pair (file names in history/ are historical).
- V1 also takes the turbine-hall and HRSG-trains images (2 x 2); V0 is the two colour sketches.
- Split into two slides (author: "find a better way than cramming"): `s_story1` (4: V0 first sketches + V1 branded concept) and `s_story2` (5: V2 3D studies, the author's spring-summer renders in history/v2_1..8; V3 drawing set + first 3D + today). Each version is a hero image, a row of three, then one line. 59 slides: main 1-52, backup 53-59.
- V3 hero is now K1 (the cover render: whole campus, LNG carrier and terminal, CCS, modular yard, data centre) instead of E123; a fresh V3A aerial was tried and dropped as weaker.

## Oct 25: how we built it (60 slides)
- New `s_how` (slide 6): research (700+ pages of real combined-cycle drawings, per the author; source not yet stated) → the 16-sheet drawing set (sheet 03 image in history/) → the model (items, parts and routes from verify_report.json) → checks (footprints, heights, clash pairs) → the cable schedule → one model behind everything. Main deck 1-53, backup 54-60. The run of show flags: confirm what the 700+ pages were and whether to name them.
- New `s_rigor` (slide 7, "Iterated, audited, reworked"): iteration counts read live from git (commits since Sep 1, working days, fix/audit/rework commits), the clash-pair count from verify_report.json, five check layers, and eight real findings that were fixed. 61 slides: main 1-54, backup 55-61.
- New `s_refs` (slide 7, "Drawn first, now at Rev 14"): the 16 SK-3X1 sheet thumbnails (history/sheets/skNN.jpg, from the Rev 14 PDF) with numbers and titles, plus Rev 14 / 700+ reference pages / beyond-Rev-14 design changes tagged. 62 slides: main 1-55, backup 56-62.
- New `s_zoom` (slide 8, "Real engineering detail, sheet by sheet"): high-resolution crops of SK-3X1-04 (single-line, GT1 start-up path), -05 (R1 plan; Rev 04 too small, Rev 05 64 x 180 ft) and -03 (motor and load schedule), in history/sheets/z*.jpg. 63 slides: main 1-56, backup 57-63.
- New `s_zoom2` (slide 9): SK-3X1-03 power-block plan large plus its electrical-facilities list (history/sheets/z03_power_block.jpg, z03_facilities.jpg). 64 slides: main 1-57, backup 58-64.
