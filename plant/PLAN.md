# Combined-cycle 3x1 drawing set — Step 1 plan

Deliverables will live in `plant/`: build_plant.py, render_views.py, make_sheets.py, views.json, assumptions.md. Renders go to `plant/out/renders/`, sheets to `plant/out/sheets/`. Feet throughout; `TRUE_SCALE = 0.3048` converts to Blender metres.

## 1. Equipment list (ft: L x W x H) with sources

| # | Zone / item | Dimensions (ft) | Basis |
|---|---|---|---|
| 7 | Gas turbine core (H-class), x3 | 34 x 14 x 14; packaged enclosure 48 x 18 x 18 | Siemens SGT-8000H fact sheet: 10.5 x 4.3 x 4.3 m, 289 t |
| 7 | GT generator (H2-cooled), x3 | 42 x 15 x 15 on 8 ft pedestal | Scaled from GT core; check OEM outline |
| 7 | GT train pitch | 110 ft bay spacing, axis E-W | Assumption (hall crane + laydown between trains) |
| 7 | Steam turbine + generator | ST 60 x 20 x 18, gen 45 x 15 x 15 on 40 ft tabletop | Assumption from typical ST pedestal elevation |
| 7 | Turbine hall | 520 x 150, eave 90, crane rail 65; roof + south wall separate parts | Assumption; CEC AFCs list turbine buildings 80-100 ft; verify span |
| 6 | HRSG casing, x3 | 210 x 45 x 85 (inlet duct + modules + outlet) | US 6,230,480 (501G HRSG: 200 L x 40 W x 70 H), uprated for H-class |
| 6 | HRSG stack, x3 | 22 dia x 160 above grade | Otay Mesa Energy Center (CEC 99-AFC-05): 160 ft stacks |
| 8 | Air-inlet filter house, x3 | 45 x 30 x 25, floor at el. 30, on braced legs, duct to GT | Assumption (elevated inlets 30-60 ft common); verify |
| 11 | Air-cooled condenser | 400 x 200, fan deck 70, windwall top 95, 40 cells (8x5) | Otay Mesa GEA ACC 295 x 123 x 76 (2x1) scaled to 3x1 |
| 1 | GSU transformers, x4 (3 GT + 1 ST) | 40 x 30 x 32 with 14 ft firewalls; 230 kV bushings el. 40 | Assumption (400 MVA class); custom per OEM |
| 1 | 230 kV switchyard | 500 x 700, bus el. 40, dead-end towers 70, breaker-and-a-half | NESC/IEEE 230 kV clearances; layout generic |
| 1 | Gen-tie | 3 A-frame structures 80 ft + 2 lattice towers 110 ft; underground getaway shown as X-ray duct bank | Assumption |
| 7/1 | Isophase bus | 3 x 2.5 ft dia tubes, el. 18, generator to GSU | Typical IPB for 300 MW class |
| 5 | Elevated modular e-house | 2 modules 60 x 20 x 12 on 6 ft steel, cable vault below, MV/LV switchgear, relay panels inside | Assumption (modular e-house practice) |
| 9 | MCC / VFD / UPS building | 120 x 60 x 20, three rooms | Assumption |
| 4 | Admin + control room | 160 x 80 x 28, two storeys | Assumption |
| 2 | BESS yard | 24 x 20 ft ISO containers (20 x 8 x 8.5) each with PCS/transformer skid 12 x 8 x 8; MV collector to e-house | ISO 668 container; PCS skid generic |
| 15 | Gas metering house + 2 process tanks | 40 x 20 x 14; tanks 40 dia x 40 (demin / raw water) | Assumption |
| 15+ | Fuel-gas context, outside fence | 24 in pipeline + pig launcher; 2 LNG bullets 120 x 16 dia + vaporizer skids; H2 tube storage 12 x (40 x 4 dia) + blending skid | Assumption; context only |
| 13 | Water treatment | building 120 x 60 x 24, 4 tanks 40 dia x 40, pond 200 x 120 x 8 deep | Assumption |
| 12 | Chillers + cooling towers | 6 chiller skids 40 x 12 x 12; 4-cell tower 200 x 50 x 45 | Assumption |
| 14 | CCS block | DCC 30 dia x 100; absorber 45 dia x 220; regenerator 25 dia x 140; CO2 compressor building 100 x 50 x 30; 30 ft dia flue-gas duct from stacks | Petra Nova absorber 380 ft (POWER, 2017) scaled down for page fit; flagged |
| 10 | Modular power yard | 6 genset containers 40 x 8 x 9.5; 8 fuel-cell modules 30 x 10 x 10; black-start aero GT 60 x 14 x 14 | Assumption |
| 3 | Reel staging / laydown / prefab | 30 reels 8-12 ft dia on payout stands; prefab spine tent 200 x 60 x 25; laydown 500 x 400 | Assumption |
| 16 | Cable corridor | duct bank 8 ft wide (2 x 6 conduits), 2-tier tray rack (power el. 12, controls el. 15), MV loop switchgear 8 x 4 x 8, grounding grid 50 ft mesh | IEEE 80 grid pitch generic |
| site | Site | 3000 x 2000 (about 140 acres), fence, perimeter road, E-W spine road | Typical 1,100 MW CC site 100-200 acres |

Zone map, west to east (x 0-3000), north row / south row: 1 switchyard (N) + 2 BESS (S) at x 0-500; 4 admin (N), 5 e-house (mid), 3 laydown (S) at x 500-900; 6 HRSG at x 900-1150; 7 hall at x 1150-1300; 8 inlets at x 1300-1400; 10 modular power (N) + 9 MCC (S) at x 1400-1700; 11 ACC (N) + 12 chillers (S) at x 1750-2150; 14 CCS (N) + 13 water (S) at x 2150-2600; 15 gas metering at x 2600-2900; 16 cable corridor along the spine road y = 500, x 200-2900. Fuel-gas context at x 3050-3600 outside the fence.

## 2. View list (15 sheets, each issued clean + tagged, numbered "NN / 15")

| Sheet | Subject | Az / El / mm | Hidden | Callouts |
|---|---|---|---|---|
| 01 | Whole site, zones 1-16 | 45 / 38 / 85 | below-grade | 1-16 |
| 02 | Turbine hall cutaway: GT train, generator, IPB, leads | 40 / 30 / 60 | hall roof, south wall, below-grade | A-J |
| 03 | HRSG and stack | 50 / 32 / 65 | below-grade | A-H |
| 04 | Switchyard / GSU: overhead gen-tie + underground HV getaway | 45 / 35 / 65 | none (X-ray: ground plane 40% alpha over duct bank) | A-J |
| 05 | E-house cutaway | 35 / 30 / 55 | e-house roof + south wall | A-I |
| 06 | MCC / VFD / UPS room cutaway | 35 / 30 / 55 | building roof + south wall | A-H |
| 07 | BESS yard | 45 / 35 / 65 | below-grade | A-G |
| 08 | ACC | 50 / 33 / 65 | below-grade | A-G |
| 09 | Fuel gas + metering with pipeline / LNG / H2 | 45 / 35 / 60 | below-grade | A-I |
| 10 | CCS block | 45 / 32 / 60 | below-grade | A-H |
| 11 | Modular power yard | 45 / 35 / 65 | below-grade | A-G |
| 12 | Cable corridor: duct bank, tray, MV distribution | 40 / 28 / 55 | none (X-ray) | A-J |
| 13 | Reel staging + prefab electrical spine | 45 / 33 / 60 | below-grade | A-H |
| 14 | Site MV distribution and grounding (X-ray, whole site) | 45 / 38 / 85 | all buildings 30% alpha | A-J |
| 15 | How the plant connects (text-only, three columns, abbreviations) | - | - | - |

Camera targets are named anchor empties (VIEW-nn-target); crops are per-view render regions in views.json; every crop includes ground, pad and road. Renders 5000 x 3550, Cycles 384 samples, OpenImageDenoise; credit line burned into the pixels via the compositor.

## 3. PARAMS block (top of build_plant.py)

```python
PARAMS = dict(
    TRUE_SCALE = 0.3048,          # ft -> m
    SITE = (3000, 2000),          # ft, x east, y north
    FENCE_SETBACK = 40,
    ROAD_W = 24, SPINE_Y = 500, PERIM_INSET = 60,
    EXP_JOINT = 20,               # paving score grid, ft
    N_GT = 3, GT_PITCH = 110, GT_AXIS = "EW",
    HALL = dict(L=520, W=150, EAVE=90, CRANE=65, ORIGIN=(1150, 700)),
    GT = dict(CORE=(34,14,14), PKG=(48,18,18), GEN=(42,15,15), PED=8),
    ST = dict(BODY=(60,20,18), GEN=(45,15,15), TABLETOP=40),
    HRSG = dict(L=210, W=45, H=85, STACK_H=160, STACK_D=22, GAP_TO_HALL=40),
    INLET = dict(L=45, W=30, H=25, FLOOR_EL=30),
    ACC = dict(L=400, W=200, DECK=70, WALL=95, CELLS=(8,5), ORIGIN=(1750, 1100)),
    GSU = dict(N=4, SIZE=(40,30,32), WALL_H=14, BUSHING_EL=40),
    SWYD = dict(L=500, W=700, BUS_EL=40, DEADEND_H=70, ORIGIN=(0, 1200)),
    GENTIE = dict(AFRAME_H=80, TOWER_H=110, DUCTBANK_DEPTH=6),
    IPB = dict(D=2.5, EL=18, SPACING=5),
    EHOUSE = dict(MODULES=2, SIZE=(60,20,12), STEEL_H=6, ORIGIN=(700, 900)),
    MCC = dict(SIZE=(120,60,20), ORIGIN=(1450, 250)),
    ADMIN = dict(SIZE=(160,80,28), ORIGIN=(550, 1500)),
    BESS = dict(N=24, ROWS=2, CONT=(20,8,8.5), PCS=(12,8,8), PITCH=30, ORIGIN=(60, 150)),
    GASMET = dict(HOUSE=(40,20,14), TANK_D=40, TANK_H=40, ORIGIN=(2650, 900)),
    FUELGAS = dict(ORIGIN=(3050, 600), LNG=(120,16), N_LNG=2, H2=(40,4), N_H2=12, PIPE_D=2),
    WATER = dict(BLDG=(120,60,24), TANK_D=40, TANK_H=40, N_TANK=4, POND=(200,120,8), ORIGIN=(2200, 150)),
    CHILL = dict(N=6, SKID=(40,12,12), TOWER=(200,50,45), CELLS=4, ORIGIN=(1800, 150)),
    CCS = dict(DCC=(30,100), ABS=(45,220), REGEN=(25,140), COMP=(100,50,30), DUCT_D=30, ORIGIN=(2200, 1100)),
    MODPWR = dict(GENSETS=6, FUELCELLS=8, BLACKSTART=(60,14,14), ORIGIN=(1450, 1200)),
    LAYDOWN = dict(AREA=(500,400), REELS=30, REEL_D=(8,12), TENT=(200,60,25), ORIGIN=(500, 60)),
    CORRIDOR = dict(Y=470, X0=200, X1=2900, DUCT_W=8, DUCT_DEPTH=5, TRAY_EL=(12,15), MV_SWGR=(8,4,8), GRID_PITCH=50),
    COLORS = dict(ENCL="#E6E4DF", STEEL="#9A9C9E", CONC="#C9C6BF", ASPH="#5A5A58", CABLE="#141414", COPPER="#C8722E", BACKDROP="#D9D8D5"),
)
```

Confirm, or edit numbers in the table / PARAMS, and I produce all five files in one pass.
