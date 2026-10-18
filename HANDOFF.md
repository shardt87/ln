# Handoff: SK-3X1 power campus model, renders and the October strategy deck

Branch: `claude/3d-plant-model-generation-a3ad3u`. Everything lives under `plant/`. The detailed pipeline guide is
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
    "3x1 CCGT");
  - interior electrical item: lighting panel + transformer, MC-HL under the crane girders and along the purlins to
    every high bay, column drops to welding / duplex receptacles and fire-alarm devices (red FPLR), crane conductor
    bar, exit lights;
  - steam turbine brought to the GTs' level: lube oil to three bearings, casing thermocouples (KX), probes, EHC servo
    cable, junction boxes in conduit to the EL 42 control tray, STG box, turning-gear MC feed;
  - south wall + roof split into "Turbine hall south cladding and roof (lifted off in the cutaway views)" for cutaways.
- Renders this session (all in `plant/renders/cover/`): `HX1_hero_cable.jpg`, `HX1_photoreal.jpg`,
  `HALL7_hero_cable.jpg`, `ST1_steam_turbine.jpg`, `HALL4_hero_cable.jpg` (down-the-row alternative),
  comparison sheets (`hrsg_grey_test.jpg`, `hrsg_slate_stacks_test.jpg`, `stack_*_test.jpg`, `hall_options.jpg`).

## In progress / not yet done

- **Viewer not republished** since the hall / ST / branding changes. Rebuild `plant/viewer/index.html` and
  `index_southwire.html` (`build_viewer.py`) and republish the artifact https://claude.ai/artifact/9bfQJUnJ6GCH35zmjBq7cP
  (publish `plant/viewer/index.html` with that url). The new `print` image decal (wall sign) is supported in
  `viewer/template.html` but untested in the browser.
- **Older deck pictures** (slides 4-7, 9-12 heroes, K5 aerial on slide 2) predate the slate HRSG / black-copper look
  and the photoreal finishes. Re-render the cameras they use (`brochure.py` ZONES heroes E60/E70/E68/E65/E77/E64,
  details E20/E4/E66/E67/E23, K5) and rebuild the deck: about 3-4 h of Blender time.
- `plant/renders/epic/HX1_pro.png` etc. are git-ignored (`*.png`); the slide pictures that matter are committed as
  JPG in `renders/cover/`.
- ST close-up: the thermocouple leads over the LP hood top hang in the air (`st_detail.py`, exhaust-hood leads at
  EL 45.4); route them flush on the casing if ST1 is used in the deck.
- `DETAIL_CYCLES.md` / `README.md` have no entries yet for the Oct 17-18 work (the commit messages describe it).

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

## Next steps (priority)

1. Rebuild and republish the viewer with the hall / ST / branding work; check the wall sign renders in the browser.
2. Re-render the older deck pictures with the current look; rebuild the deck PDF.
3. Log the Oct 17-18 work in `plant/DETAIL_CYCLES.md` and `plant/README.md`.
4. ST close-up polish (flush thermocouple leads) if ST1 goes in the deck.
5. Training prep from `plant/HANDOFF.md`: fundamentals slides, SME review, two Teams dry runs.

## Only in the conversation (not in files until now)

- The user's taste and review history above (what was rejected and liked); keep "not too busy, not too dark",
  realism first, power block as hero, copper accents, ship and BTM visible in campus views.
- A reviewer's note adopted for the cover: one subject, sky above, no smoke, label unobstructed.
- Environment: the Blender venv lived in the session scratchpad (`bvenv`, Python 3.11.15, bpy 4.2.0, numpy 2.4.6,
  Pillow 12.3.0) and is gone with the container; recreate it. Background jobs max 2 h. **Never `pkill -f` / `pgrep -f`
  with a pattern that also appears in the same command line** (it kills the shell); run the kill as its own command.
- Root `.gitignore` ignores `*.png`; force-add PNGs that the build needs (e.g. `screens/hall_wall_sign.png`).
- No file in the repo is over 100 MB (largest: `plant/model/*.glb` and `plant/sk3x1_model.obj`, ~80-87 MB).
