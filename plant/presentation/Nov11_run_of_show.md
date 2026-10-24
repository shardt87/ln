# Nov 11 training: "Inside Power Generation" run of show (draft 1)

**Session:** Wednesday, Nov 11, 2026, 1:30-2:30 PM, on Zoom. About 440 required and optional attendees, mostly internal; they need clarity, not engineering. Host: Stephan Hardt.

**Promised in the invite:** power-generation fundamentals and the market landscape, then a guided virtual tour of a 3D gas power campus (combined cycle, modular generation, BTM, LNG). The tour covers the major equipment and electrical systems, how they work together, and where wire and cable are used.

**The rule for the next 19 days:** if it doesn't serve one of the seven stops below, it goes in the parking lot (end of this file).

---

**Slides:** `renders/deck/training/SW-3X1_Nov11_training.pdf` (17 slides, built by `blender/deck_training.py`): title, agenda, why gas now (3 market placeholders to fill), simple vs combined cycle, how an HRSG works, the 16-zone campus, 7 tour-stop backup slides, the whole plant in one number, what the spec calls for, pain points and the answer, three things to remember + Q&A.

## Rundown (60 min)

| Time | Segment | On screen | Mins |
|---|---|---|---|
| 1:30 | 0. Welcome and why this matters | 1 title slide | 3 |
| 1:33 | 1. Fundamentals and market | 4 slides | 10 |
| 1:43 | 2. The 3D tour: seven stops | Live viewer, plus one slide per stop if needed | 30 |
| 2:13 | 3. Wire and cable takeaways | 3 slides | 9 |
| 2:22 | 4. Q&A | Viewer on the overview | 8 |

Keep 2 minutes of slack inside the tour. If you run long, shorten stop 7 (LNG) to one minute.

---

## 0. Welcome (3 min)

**Say:**
- "Every power plant runs on cable. Today we walk through a complete gas power campus, built as a 3D model with a full cable schedule, and look at what each part does and where our products go."
- "No engineering background needed. At each stop you'll get three things: what it does, its electrical system, and the cable."

**Housekeeping:** questions in the chat, answered at the end. The recording will be shared.

---

## 1. Fundamentals and market (10 min, 4 slides)

**Slide 1: Why gas, why now (3 min)**
- Demand is growing again: data centres, manufacturing and electrification.
- Gas plants are firm, dispatchable power that complements wind and solar.
- Message: new gas build, modular and behind-the-meter (BTM) generation, and upgrades to the existing fleet all need cable.
- **Check the market numbers you quote against current Southwire market intelligence.**

**Slide 2: Simple cycle vs combined cycle (3 min).** Reuse boilers slide 6, "What goes in, what comes out".
- In: gas, air, a little water. Out: power, stack gas, heat.
- The gas turbines make about 2/3 of the power; the steam from their exhaust makes about 1/3 more with no extra fuel.

**Slide 3: How an HRSG works (2 min).** Reuse boilers slide 5: the "What it is" and "Fun facts" box.

**Slide 4: The campus at a glance (2 min).** Use the 16-zone overview slide.
- "This is SW-3X1, a 3x1 combined-cycle plant: three gas turbines, three HRSGs and one steam turbine, with a modular generation yard, a battery yard, a behind-the-meter data centre, LNG supply, and options for carbon capture and hydrogen."
- "Conceptual and not engineered, but sized like real plants."

---

## 2. The 3D tour: seven stops (30 min, about 4 min each)

**How to run it:** open the viewer and press **▶ Nov 11** (top left of the 3D window). It goes full screen with captions (Equipment / System / Cable). Use **→ / space** for the next view, **←** to go back, keys **1-7** (or the chapter bar at the top) to jump to a stop, and **Esc** to leave. The tour has 22 views: an opening, 20 across the seven stops, and a closing cable X-ray. Use the same three beats at every stop:

1. **What it does** (1 min)
2. **Electrical system** (1 min)
3. **Where the cable goes** (1-2 min, show the cable X-ray)

### Stop 1: Grid connection and switchyard
- **Does:** sends the plant's power to the 230 kV grid.
- **Electrical:** generator step-up transformers (GSUs) take 21 kV up to 230 kV; then breakers, disconnects, and a control house with protection relays.
- **Cable:**
  - HV conductor and 230 kV cable;
  - control and relay cable from every breaker to the control house;
  - fibre;
  - a buried ground grid (bare copper).
- **Line:** "Every breaker out here has a bundle of control cable running back to the control house."

### Stop 2: Turbine hall: gas turbines, generators, steam turbine
- **Does:** three H-class gas turbines and one steam turbine turn generators.
- **Electrical:**
  - isolated-phase bus from the generators to the GSUs;
  - unit auxiliary transformers feed the 13.8 kV switchgear in R1;
  - static starters spin the gas turbines up.
- **Cable:**
  - MV-105 to big motors and transformers;
  - TC-ER power and control to the lube-oil and hydraulic skids;
  - thousands of instrument pairs (vibration, temperatures).
- **Show:** the R1 switchgear room interior (13.8 kV lineups, MCCs).

### Stop 3: HRSG and its e-house (the boiler story; your best material)
- **Does:** turns exhaust heat into steam; the SCR inside cuts NOx.
- **Electrical:**
  - the 13.8 kV feed pumps (two of 5 MW each);
  - the T-R2A transformer feeds the e-house (480 V switchgear, MCCs, drives, DCS);
  - CEMS shelter at the stack.
- **Cable:**
  - one HRSG train is **707 cables, about 157,000 ft**, and **about 74 % of them are instrument and thermocouple pairs**;
  - ARMOR-X MC-HL at the duct-burner gas skid.
- **Show:**
  - the HRSG close-up;
  - the e-house cutaway with its 9 callouts;
  - the CEMS shelter (boilers slides 7, 9 and 10). Pick **one** of the three if time is short.
- **Close the stop on Boiler Row** (the last view of stop 3; boilers slide 4): the package, utility and electric boilers side by side.
  - **Line:** "Three boilers, three cable stories. The package boiler is control cable, the utility boiler is instrument cable, and the electric boiler is MV cable."

### Stop 4: Cooling and water: air-cooled condenser and water treatment
- **Does:** the ACC turns spent steam back into water. 80 fans, no cooling-tower water.
- **Electrical:** the R4 e-house holds four VFD lineups that drive the 80 fan motors.
- **Cable:** VFD-rated cable (ARMOR-X MC-HL VFD / TC-ER VFD) to every fan; water-treatment MCCs.
- **Line:** "Variable-frequency drives mean VFD-rated cable; ordinary cable fails early here."

### Stop 5: Modular generation yard
- **Does:** fast-start, flexible power.
- **What's there:**
  - reciprocating engine gensets in halls;
  - aeroderivative simple-cycle units;
  - two package types side by side: a factory-modular aeroderivative (AX-1, LM2500XPRESS class, ~35 MW, shipped as pre-built modules with plug-in interconnects) and an industrial gas-turbine package (IG-1, Titan 250 class, ~23 MW, one skid);
  - fuel-cell and microturbine modules;
  - the battery storage yard next door.
- **Electrical:** each unit has its own generator step-up and MV e-house; inverters and power-conversion skids for the battery and fuel cells.
- **Cable:**
  - MV collection cable;
  - DC cable at the battery and fuel cells;
  - prefabricated cable spines installed as modules;
  - skid pre-wire.
- **Line:** "Modular means factory pre-wiring, which is our opportunity to sell pre-terminated and cut-to-length cable."

### Stop 6: Behind-the-meter data centre
- **Does:** a ~120 MW data-centre campus powered directly by the plant's modular gensets, with the grid only as backup.
- **Electrical:**
  - 13.8 kV to 34.5 kV step-up transformers (3 x 90 MVA);
  - double-bus 34.5 kV switchgear;
  - a 40 MW / 80 MWh battery to absorb load steps;
  - two data halls, each fed 2N through 48 pad-mount transformers and UPS skids.
- **Cable:**
  - 35 kV MV cable;
  - large LV feeders to the UPS skids;
  - fibre everywhere.
- **Line:** "Data centres are why gas is growing again, and they're cable-dense on both A and B sides."

### Stop 7: Fuel: gas yard and LNG
- **Does:** brings fuel in and conditions it: the gas metering and regulating (M&R) station, plus an LNG satellite of 8 tanks holding about 414,000 gal (about 3 hours of the whole plant) for backup.
- **Electrical:** an LNG e-house (13.8 kV / 480 V); pumps, vaporizers and the boil-off compressor.
- **Cable:** this is hazardous-area territory, so ARMOR-X MC-HL (Class I Div 1 and 2) and TC-ER control, PLTC instrumentation and fire alarm on one strut rack.
- **Line:** "Wherever there's gas, the cable has to be rated for it."

---

## 3. Wire and cable takeaways (9 min, 3 slides)

**Slide A: The whole plant in one number (3 min)**
- The model's cable schedule: **6,011 runs, 21,217 cables, about 6.4 million ft (~1,200 miles).**
- By footage:
  - instrumentation, 2.8 M ft;
  - 600 V power, 1.3 M ft;
  - control, 1.1 M ft;
  - MV, about 0.4 M ft.
- Message: "Most of the footage is small cable: instrument and control. MV is the high-value part, but it isn't the volume."

**Slide B: Product map (3 min).** Reuse boilers slide 13, "What the spec calls for", or the brochure product map:
- MV-105;
- TC-ER;
- ARMOR-X MC-HL;
- instrumentation and thermocouple extension;
- SIMpull THHN;
- fibre and fire alarm.

**Slide C: Pain points and our answer (3 min).** Reuse boilers slide 14.

**Close with three things to remember:**
1. Gas plants are growing again, driven by data centres and firm power.
2. Most of a plant's cable is instrument and control; the big MV and power cable is the smaller share.
3. Southwire covers the whole plant: one supplier, staged on SIMpull reels, spec-compliant from MV down to the thermocouple.

---

## 4. Q&A (8 min)

**Questions to prepare for:**
- "How long does a plant take to build?" 3-4 years for a combined-cycle plant; modular units are much faster.
- "Who are the customers?" Utilities, independent power producers, EPCs, boiler and turbine OEMs, and data-centre developers.
- "Is the model a real plant?" Conceptual, sized from public filings of real plants, and not engineered.
- "What about hydrogen and carbon capture?" Both are in the model as options; show them if asked (layers on).

---

## Backup plan

- **Recorded video of the tour:** screen-record the viewer stop by stop by Nov 3. If the viewer lags on Zoom, play the video and narrate over it.
- **PDF of all slides,** in case screen sharing fails.
- **Second laptop or phone** logged in as co-host.

## Checklist

| Date | Task |
|---|---|
| Oct 24-27 | React to this draft; mark what to cut or keep. Tour mode done (▶ Nov 11 in the viewer); walk it once and note any view to change. |
| Oct 28-31 | One slide per stop (reuse zone and boiler slides). Optional: modular turbine packages, **only if done in one day**. |
| Nov 2-3 | Full-quality render batch overnight (renders/RENDER_QUEUE.md); record the backup video. |
| **Nov 4** | **Dry run with one colleague, timed.** |
| Nov 5-9 | Fixes only. |
| Nov 10 | Zoom tech check; freeze. |

## Parking lot (after Nov 11)

- Modular yard and Boiler Row are **closed for Nov 11** (Oct 24): no more equipment, fixes only.
- Possible later plant types: a CHP / cogeneration unit (gas turbine + HRSG selling steam to an industrial host), linear generators.

- Wastewater-treatment and cooling-tower refinements.
- Turbine close-ups at HRSG depth.
- More switchgear-room detail.
- Blender fly-through animation.
- Zone 07 parts 3-4 (construction compound, deck slide).
- Modular gas-turbine packages: done Oct 24 (AX-1 LM2500XPRESS class, IG-1 Titan 250 class). A larger SGT-800-class unit was tried and removed: it repeated the SC-1 / SC-2 simple-cycle story.
