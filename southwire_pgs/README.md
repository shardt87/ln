# Southwire Power Generation Solutions — reusable 3D model and leave-behinds

Discussion material for conversations with generator manufacturers, switchgear builders, integrators,
assembly partners, testing companies and distributors. Everything here is a **discussion concept**:
the illustrated kits, cable packages and assemblies are applications to evaluate, not qualified Southwire
products, and nothing implies that any named company has agreed to a partnership, pilot or purchase.

## Folder contents

| Path | What it is |
|---|---|
| `blender/Southwire_PGS_Master.blend` | Editable master scene (Blender 4.2+ / 5.x). All modules, materials, 23 saved views, cameras, callout anchors, control panel. No external textures — every material is procedural/flat, so nothing needs packing. |
| `blender/scripts/build_master.py` | Rebuilds the `.blend` from scratch (reproducible). |
| `blender/scripts/mod_*.py` | One file per module (geometry + routing). |
| `blender/scripts/views.py` | Saved views: camera, visible collections, hidden/exploded objects, callout anchors. |
| `blender/scripts/sw_controls.py` | View/configuration switcher (also embedded in the `.blend` as a text block). |
| `blender/scripts/render_views.py` | Batch renderer (clean PNG + transparent PNG + callout pixel positions). |
| `blender/scripts/content.py` | All page copy (headlines, callouts, statements, next steps, contact). |
| `blender/scripts/pages.py` | Builds PDF, PPTX and annotated PNGs from one layout spec. |
| `blender/scripts/qa.py` | Delivery checks: callouts in frame, text fit, banned claims (%, savings, certification…), every file opens. |
| `renders/clean/` | 2400 × 1664 px renders (7.5 × 5.2 in at 320 dpi), no annotations. `_alpha` = transparent background. |
| `renders/annotated/` | Same renders with the three numbered callouts burned in (for email/screens). |
| `pages/pdf/` | Print-ready US Letter one-pagers (one per company + `All_one_pagers.pdf`). |
| `pages/pptx/` | Editable one-pagers (one per company + `All_one_pagers.pptx`). Text, callouts, leaders, legend and boxes are native PowerPoint shapes. |
| `pages/png/` | Page previews (150 dpi) for quick review. |

## Modules and collections

Top-level collections (as requested): `Generator`, `Switchgear`, `Control_Wiring`, `Power_Cables`,
`Grounding`, `Ehouse`, `Cable_Tray`, `Transformer`, `Temporary_Power`, `Assembly_Kit`, `Annotations`,
`Cameras`, `Lighting`. Each holds named sub-collections per assembly (e.g. `Control_Wiring/CW_WireKit`,
`Power_Cables/PC_CfgA_NormalSource`), so any assembly can be hidden, removed or exported on its own.

| Module | Zone (world origin) | Key content |
|---|---|---|
| 1 Switchgear + control cabinet | `(0, 40, 0)` | 3-section LV lineup; section 3 open (door swung, right side panel removable) with backplate, DIN rails, slotted wire duct, CPT, fuses, MCBs, PLC, relays, PSU, two terminal-block rows, ~130 individually routed control conductors (one curve per wire, custom props `from`/`to`), door harness with hinge loop, field control cables through glands, main bus + risers (rigid copper — not replaced by cable), incoming power cables to lugs, ground bus and bonding. Prepared wire kit on a cart (`KIT_Root`, movable/explodable): 3-compartment tray (STEP 1–3), folded bundles with ferrules and markers at both ends, four exploded conductors, kit label, wiring-schedule clipboard with blank check boxes. |
| 2 Generator package | root `(-6.6, 0, 0)` | Sub-base, simplified engine/radiator/alternator, removable side and roof panels (exploded offsets), LV **and** MV terminal-box variants, output cables to an end-wall gland plate and riser tray (external interface), local control cabinet, engine harness, AVR sensing cable, remote-start cable in its own conduit, batteries/starter cables, ground pad. `GEN_Kits`: power-lead kit and control-wire kit on pallets. |
| 3 E-house / skid | `(40, 0, 0)` | Two shipping sections (removable roof + front wall per section), LV lineup re-using the Module 1 bay mesh, dry-type transformer, MCC/control lineup, ladder tray with separate control channel, split splice kit, field-completed feeders and control interconnect (amber), external entry transit + lateral tray, ground pads, split bonding jumper, interconnect cable package for the exploded view, staged reels and deliveries. |
| 4 Transformer interface | plant zone | Simplified unit transformer: tank, radiator banks, LV and HV air-terminal chambers (top entry), LV spade terminals with lugs, HV bushings with cable terminations, aux/control box with conduit to the MV switchgear, ground pad, translucent site-installed boundary planes. Not an engineered design. |
| 5 Temporary power + testing | `(0, -40, 0)` | Trailer generator with cam-lock output panel, docking station (generator-input port, load-bank port, internal bus and prepared internal connections, facility feed to conduits below the pad), single-conductor portable lead sets, load bank as a configurable test load, lead-set storage cart. |
| 6 Cable assembly workbench | `(40, 40, 0)` | Exploded axis: cable → prepared end → ID sleeve → compression lug → support cleat; finished coiled assembly, carton, generic inspection/test-record card (blank fields only). |

## Configurations (only one shown per render)

| View | Topology |
|---|---|
| `CFG_A` | LV generator → open-transition ATS (separate **normal**, **generator** and **load** lugs, labeled; solid neutral) → load distribution. Normal source from a utility service section on its own tray; generator feeders on a separate tray; engine-start cable in a separate conduit. No source paralleling is shown. |
| `CFG_B` | LV generator → LV chamber of step-up transformer; HV chamber → MV tray → MV switchgear incoming section. Transformer alarm wiring in its own conduit. |
| `CFG_C` | MV generator (MV terminal-box variant, stress-cone terminations, shield grounds) → MV tray → MV switchgear. |
| `CFG_D` | Temporary generator → portable leads → docking station generator input; docking station load-bank port → portable leads → load bank. The facility feed is shown only as an interface; no permanent loads are connected to the test arrangement. |

## Switching configurations and views

**In Blender (interactive):** open the `.blend`, allow the embedded script when prompted (or open the
Text Editor, select `sw_controls.py`, *Run Script*). A sidebar tab **View3D ▸ N ▸ Southwire PGS** lists every
view grouped as *Company pages*, *Configurations* and *Modules*, plus **Explode all / Assemble all**.
Clicking a view sets collection visibility, hides the panels it removes, applies exploded positions and
activates its camera (`CAM_<view>`).

**From a script / Python console:**

```python
import sw_controls
sw_controls.apply_view("CFG_B")            # any key in scene["sw_views"]
sw_controls.set_explode(["EH_S1_Roof"])    # explode only listed objects
```

Removable panels carry the custom property `removable_panel`; explodable objects carry `explode_offset`
(metres, world axes). Every view's definition is stored as JSON in the scene property `sw_views`.

## Rendering variants

```bash
cd blender/scripts
python3 build_master.py                      # rebuild the .blend (needs the 'bpy' module, or: blender -b -P build_master.py)
python3 render_views.py --samples 96         # all views at full size  -> renders/clean/
python3 render_views.py --preview CFG_A      # quick low-res check      -> renders/preview/
python3 pages.py                             # PDF + PPTX + annotated PNGs for every company
python3 pages.py IEM                         # one page only
python3 qa.py                                # delivery checks
```

To add a company variant: add a view in `views.py` (camera, collections, callout anchors), add its copy
in `content.py`, rebuild, render that view, run `pages.py`.

Renders used Cycles with OpenImageDenoise: the IEM main render at 96 samples, all other views at 48.
Per-page callout marker positions and legend corner are set in `content.py` (`labels`, `legend_pos`) so they
can be moved without re-rendering; in the PPTX every marker, leader and label is a separate editable shape.

## Cameras

`CAM_IEM_ControlKit` (main IEM render), `CAM_EPD_ControlCabinet`, `CAM_PATRIOT_Terminations`,
`CAM_MAVERICK_Lineup`, `CAM_CAT_GenInterface`, `CAM_TAYLOR_GenKits`, `CAM_ASCO_TransferInterface`,
`CAM_RESA_TestBoundaries`, `CAM_POWELL_EhouseExploded`, `CAM_SIEMENS_SkidBoundaries`,
`CAM_NVENT_EnclosureRouting`, `CAM_WESCO_StagedSupply`, `CAM_INPOWER_Docking`, `CAM_MOSEBACH_LoadBankTest`,
`CAM_WINAR_AssemblyBench`, `CAM_CFG_A`–`CAM_CFG_D`, `CAM_MOD_Generator_Exploded`, `CAM_MOD_Transformer`,
`CAM_MOD_Ehouse_Exploded`, `CAM_MOD_Switchgear_Overview`. Lighting rigs `LGT_*` are switched with the view.

## Presentation color key (on every page legend)

* Presentation blue — control wiring / kit conductors
* Charcoal — power conductors
* Green / bare copper / braid — grounding and bonding
* Presentation amber — connections completed after placement onsite (e-house, site boundary)

These are **presentation highlights, not conductor identification**. Cam-lock connector colors in
Module 5 are equipment colors.

## Page design

US Letter portrait. Top ~15 %: logo placeholder, business unit, headline, “Discussion with …”. Middle
~50 %: supporting sentence + 7.43 × 5.15 in render with three numbered callouts and the color legend.
Lower ~25 %: three numbered opportunity statements, then a separated *Established* line and a *For
evaluation* line, plus the engineering disclaimer. Bottom ~10 %: proposed next step and contact. No QR
code (no approved destination supplied). No target-company logos are used.

## Placeholders and items to confirm before use

* **Southwire logo** — placeholder box on every page; insert approved artwork (PPTX shape
  `Logo_Placeholder`).
* **Phone / email** — `[Phone]` `[Email]` placeholders (`content.py` → `COMMON`).
* **Accent red** (`#B5121B`) is a neutral stand-in; align with the approved Southwire palette.
* **Established-capability line** (“Southwire wire and cable manufacturing and supply.”) is generic
  because no capability material was supplied; replace with approved wording.

## Engineering assumptions (illustrative only)

* Dimensions are representative (LV section 762 × 1524 × 2286 mm; generator enclosure 5.4 × 2.0 m;
  e-house 12 × 3.6 m in two 6 m sections). Not derived from any manufacturer's drawings.
* Conductor counts, sizes (e.g. ~14 AWG control, ~500 kcmil-class LV feeders shown as two per phase,
  single-core MV), lug types, bend radii and clearances are visual approximations chosen to look
  plausible; they are **not** ratings or selections.
* Transfer equipment is drawn as a two-position open-transition switch with a solid neutral.
* The transformer, MV switchgear, docking station and load bank are generic shapes; no engineered design,
  rating or certification is implied. No code compliance or engineering approval is claimed.
* Inspection/test record cards and schedules show blank fields only; no results, ratings or customer data.

## Asset sources

All geometry, materials and lighting were generated procedurally by the scripts in `blender/scripts/`
(Blender 5.0 Python API, Cycles). Fonts: Liberation Sans (SIL OFL) for PDF/PNG; PowerPoint uses Arial.
No third-party models, textures, logos or certification marks are included.
