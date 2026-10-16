# SK-3X1 3D gas power campus: handoff guide

Read this first. It lets another assistant (or a person) pick the project up with no history.
Owner: Stephan Hardt, Power Generation Solutions (Southwire). Conceptual illustration: not engineered, not for
construction.

## What this is

A 3D coordinate model of **SK-3X1 Rev 14**, a 3x1 H-class combined-cycle campus, rebuilt from a 15-sheet concept
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
python3 build_model.py              # -> sk3x1_model.json  (the master model: items, parts, routes, views, decals)
python3 verify.py                   # footprints / heights / clashes / bounds vs the drawing  -> must print PASS
python3 audit.py                    # wiring audit                                            -> must print CLEAN
python3 coastal/verify_coastal.py   # coastal variant                                        -> PASS
python3 discrepancy_scan.py         # floating parts, hanging signs, open tray ends          -> zeros
python3 cable_continuity.py         # loose cable ends (37 deliberate tails)
python3 cable_schedule.py           # -> brochure/SK-3X1_Cable_Schedule_and_BOM.xlsx + brochure/cables_xray.json
python3 build_viewer.py --generic                         # -> viewer/index.html (unbranded)
python3 build_viewer.py --out viewer/index_southwire.html # Southwire-branded viewer (used for the training)
python3 export_obj.py                                     # -> sk3x1_model.obj / .mtl
```
Only the standard library plus Pillow / openpyxl / numpy are needed for these.

**Blender renders** (Blender 4.2+ Python module `bpy`, run as a script):
```
python blender/SK-3X1_Rev14_blender_build.py --views E123,E2 --style pro --set epic --samples 128 --scale 75 --out OUT
python blender/finish_pro.py OUT          # vignette, grain, caption -> *_clean.jpg / *_final.jpg
python blender/SK-3X1_Rev14_blender_build.py --style pro --set epic --no-render --out /tmp/c --blend model/SK-3X1_plant.blend
python blender/export_model.py model      # -> model/SK-3X1_plant.glb / .usdz
```
Cameras live in `blender/pro_look.py` (EPIC list: `dict(k="E123", n=..., eye=(x,y,z), target=(x,y,z), lens=mm, show=...)`).
Model coordinates: **feet, x east, y north, z up**; the compound is 2,420 x 1,920 ft.

**Slides:** `blender/slide_hero6.py` (hero-shots slide), `blender/slide_modular.py`, `blender/deck_divider.py`,
`blender/deck_zone_slides.py`. Deck fonts are in `blender/deck/` (Barlow / Barlow Condensed).

## The viewer and the guided tour

`viewer/template.html` is a single-file three.js r147 viewer, filled in by `build_viewer.py` (gzip/base64 model inlined).
- Views (SK-3X1-11)
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
- **The HRSGs and stacks are the visual hero.** They are darker grey, with a black crown, burnished-copper accent bands framed in black, black access steel and copper "HRSG k"
  lettering. Carbon capture stays secondary: muted sage (#9dbba5) with four "CCS" letterings per absorber.
- **One gravel colour** everywhere except the switchyard.
- **Every view shows the whole campus** (modular yard, BTM, the marine terminal); views remove only cutaway roofs and walls.
- **Commits:** checks must be clean (verify PASS, audit CLEAN, scans at zero) before a commit.
- **Docs:** each change gets an entry in `DETAIL_CYCLES.md`.
- **Language:** plain English in captions and docs. Product names are Southwire families: ARMOR-X MC-HL, MV-105,
  Type TC-ER, PLTC / ITC, FPLR, Type W, SHD-GC, SIMpull. The `--generic` build strips the brand names.

## Where things stand (Oct 16, 2026)

- Model, checks, viewer and tour: done and current.
- Hero-shots slide (7 renders): `renders/deck/SK-3X1_hero_shots.*`.
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
| `sk3x1_model.json` | The built model (also regenerable) |
| `viewer/` | Viewer template and built viewers |
| `presentation/` | Tour stops, script, recorder, compositor, tour kit |
| `blender/` | Render look, cameras, render and export scripts, slide scripts |
| `brochure/` | Cable schedule workbook, X-ray data |
| `coastal/`, `reference/`, `screens/`, `site/`, `threejs/` | Coastal variant, drawing reference data, control-room screen images, site data, three.js helpers |
| `README.md`, `DETAIL_CYCLES.md` | Full documentation and the change log |
