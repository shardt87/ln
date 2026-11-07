# Nov 11 training: "Inside Power Generation" run of show (draft 1)

**Session:** Wednesday, Nov 11, 2026, 1:30-2:30 PM, on Zoom. About 440 required and optional attendees, mostly internal; they need clarity, not engineering. Host: Stephan Hardt.

**Promised in the invite:** power-generation fundamentals and the market landscape, then a guided virtual tour of a 3D gas power campus (combined cycle, modular generation, BTM, LNG). The tour covers the major equipment and electrical systems, how they work together, and where wire and cable are used.

**The rule for the next 19 days:** if it doesn't serve one of the seven stops below, it goes in the parking lot (end of this file).

---

**Slides:** `renders/deck/training/SW-3X1_Nov11_training.pdf` (70 slides, built by `blender/deck_training.py`; JPG copies in `renders/deck/training/jpg/`). See the slide map below.

## Slide map (Oct 26: 70 slides; main deck 1-62, backup 63-70)

| Slides | Section |
|---|---|
| 1-14 | Title, agenda, **what you will take from this hour** (by role), **why we built it** (4), **why a 3D model** (5: V0-V1, 6: V2-V3), **how we built it** (7), **the drawings behind it** (8), **up close** (9-11), **one line of the model today** (12 simple, 13 full), **the work behind it** (14) |
| 15-18 | Divider 01 *How power is made*; every power plant is this; four families; the mix today and why gas |
| 19-25 | Divider 02 *The market*; at a glance, load growth, backlogs, the cable prize, register, state heat map |
| 26-46 | Divider 03 *Inside a gas plant*; open the box, a day on the grid, the power block snapshot (29), the combined-cycle build (30-33), the X-ray (34 copper, 35 by type, **36 the whole campus**), generator to light switch, voltage ladder, cable 101, what a plant does to a cable, owners, greenfield/brownfield, who buys, **three buckets of cable (44)**, **where every cable starts (45)**, the modern campus |
| 47-55 | Divider 04 *The tour*; campus overview; the seven stops |
| 56-62 | Divider 05 *Wire and cable*; the whole campus in one number; **the offer**; **installed faster (SIMpull)**; **knowledge check (Zoom poll)**; take-aways and Q&A; **resources and who to call** |
| 63-70 | Backup: divider, **traced to real plants (64)**, quiz answers, four ways to burn gas, how an HRSG works, follow the power, the HRSG spec, sources and qualifiers |

**New slides, talking points**
- **Slides 5-6, why a 3D model (1.5 min):** 5: V0 (March) the first sketches, cable colour-coded but generic (11 kV / 138 kV, no counts); V1 (March) a Southwire-branded concept, hall and HRSGs in detail, still invented. 6: V2 (spring-summer) 3D studies, real elements but not to scale or routed; V3 (September-today) drafted as the SK-3X1 drawing set, then the model built from it: LOD 3, the cable schedule, the X-ray, the tour. Why: see the whole plant, measure instead of guess, one source, speak the buyer's language.
- **Slide 7, how we built it (1 min):** research (700+ pages of real combined-cycle drawings: layouts, one-lines, equipment and load lists, to confirm equipment, voltages and electrical systems) → the 16-sheet SK-3X1 drawing set → the 3D model (1,023 items, 156,247 parts, 719 routes) → checks (211/211 footprints, 21 heights, 1.5 M clash pairs, none) → the cable schedule (21,217 cables, 6,011 runs) → one model behind everything. "Conceptual, not engineered, but not invented." CONFIRM before Nov 11: what the 700+ pages were and whether to name the source.
- **Slide 8, the drawings behind it (45 s):** the 16 SK-3X1 sheets at Rev 14 (site, optional systems, power block electrical, single-line, R1, CCS, modular, turbine-hall maintenance, dimensions, heights, fuel supply, LNG terminal, hydrogen); 700+ pages of real reference drawings; everything beyond Rev 14 tagged as a design change.
- **Slide 9, up close (45 s):** three zooms: SK-3X1-04 single-line with GT1's start-up path traced (230 kV to 13.8 kV); SK-3X1-05 R1 building (Rev 04 could not hold the switchgear, Rev 05 grew it to 64 x 180 ft: the revisions were real); SK-3X1-03 motor and load schedule.
- **Slide 10, the power block up close (30 s):** SK-3X1-03 large: rooms R1 to R4, every motor at its equipment, every MV and LV route named, plus the seven electrical rooms and what each feeds.
- **Slide 11, planned before it was modelled (30 s):** SK-3X1-02 optional systems with reserved space (the hero); SK-3X1-13 height comparison to scale (each height checked against a named real drawing, permit or vendor reference: the orange dots); SK-3X1-11 the 3D view plan. The model must match these on every build.
- **Slide 12, one line, the whole campus (1 min):** the model's single-line as it stands today: 230 kV breaker-and-a-half yard D1-D6; GTG-1..3 and the STG through GSUs; UATs to the 13.8 kV buses in R1 and on to BFPs, LCIs, 4.16 kV, R2A-C, R3, R4 (92 VFDs) and R-WT; Rev 14 options on D4 (modular yard, BESS), D5 (CCS), D6 (H2); design changes beyond Rev 14 in green (data-centre campus via BTM-T1..3 and the N.O. BTM-TIE, AX-1 / IG-1, Boiler Row with UB-1's GSU). Simplified, typical ratings.
- **Slide 13, the full single-line (show, don't read; 30 s):** drawing-sheet style: every bus (230 kV, three 13.8 kV with N.O. ties, 4.16 kV A/B, 480 V rooms, EMCC, DC/UPS), every generator, transformer and motor group, plus the modular collector, BESS feeders, CCS, H2 rectifiers, the BTM 34.5 kV double bus and Boiler Row. "This is what is behind the cable schedule." Slide 11 is the version to explain.
- **Slide 14, the work behind it (1 min):** Rev 14 of the drawing set; ~620 saved iterations since the first 3D model, about 85 of them fixes, audits and rework; five layers of checks on every change (drawings, geometry, electrical, cable schedule, real-plant logic); what the audits caught and fixed (gas line through two transformers, gas riser upstream of its shut-offs, unwired equipment, tray through the boiler house, floating stairs, a duplicate package, mixed cable totals). "Design, build, audit, review, rework, every day." (Counts update from the project history at each build.)
- **Slide 64 (backup), traced to real plants:** for "is this real?" questions. Seven systems (grid connection, generator leads, plant MV buses, 480 V and MCCs, big motors, HRSG and burners, cable), what real plants show, the kind of public document that shows it, and where it is in SW-3X1. The documents and links are in presentation/reference_linkage.md (say plant names from there if useful; they stay off the slide). CONFIRM: add the page counts of the author's own set so the 700+ adds up.
- **Slide 4, why we built it (1 min):** four reasons. 1 nothing like it existed: no competitor material and no public reference shows a whole gas plant with its cable (OEM brochures stop at the turbine; EPC drawings are confidential). 2 a way to talk with customers: one picture sales, an EPC and an owner can all point at. 3 a seat at the IPP table: IPPs and developers plan whole campuses (power block, BESS, data centre, behind-the-meter), so the model gets us into the conversation before the EPC buys. 4 cable is the story, the plant is the backdrop: every render shows our products applied where they go. Close: "Not engineered for one customer: built so we can talk about theirs."
- **Slide 3, what you will take (1 min):** one line per audience: sales, customer service, supply chain and plants, marketing and leadership. "No engineering background needed."
- **Dividers 14, 18, 25, 45, 54 (5 s each):** say the section name and move on.
- **Slide 44, three buckets of cable (1.5 min):** follow the cable, not the building. 1 inside the packages: OEMs, e-house and package builders buy it, every month, not in our 440 miles. 2 between the packages: the EPC or its electrical contractor, once per plant, most of the miles. 3 to the grid: the HV contractor or utility, early, few cables, high value. "Starting in the e-house is not the same as being bought by the e-house builder. Cover both."
- **Slide 45, where every cable starts (1 min):** the R1 switchgear room from above, with the switchgear, MCCs and drives, and the control room. "Power leaves the switchgear and MCCs; signals come home to the control room. Every device in between is wired." Ties the three buckets to a real room.
- **Slide 58, the offer (1.5 min):** our families by plant area, grid to thermocouple, plus the services (spec support, cut-to-length, harness kits, logistics, field support). It replaces the HRSG-only spec slide (now backup 69).
- **Slide 59, installed faster (1 min):** SIMpull reels (one pull per feeder), SIMpull truck, cut-to-length, pre-terminated. "Every set-up and termination saved is schedule saved."
- **Slide 60, knowledge check (2 min):** launch the Zoom poll with the three questions, show results, give the answers by voice (backup 65 has them with the why). Answers: C instrumentation; C the EPC or package builder; B about one-third.
- **Slide 62, resources (30 s, leave it up during Q&A):** the viewer link, the brochures, the recording; the team: Stephan Hardt, Patrick Ritchie (EPC accounts), Greyson (EPC outreach), Phil Metz and Bob Benish (OEMs and package builders).
- **Slide 70, sources:** for questions on any number.

## Rundown (60 min)

| Time | Segment | On screen | Mins |
|---|---|---|---|
| 1:30 | 0. Welcome and why this matters | 14 slides (title, agenda, why you, why we built it, why a 3D model x2, how we built it, the drawings, up close x3, one line x2, the work behind it) | 2 |
| 1:32 | 1. Market and fundamentals | 31 slides | 28 |
| 2:00 | 2. The 3D tour: seven stops | Live viewer, plus one slide per stop if needed | 18 |
| 2:18 | 3. Wire and cable takeaways | 3 slides | 6 |
| 2:24 | 4. Q&A | Viewer on the overview | 6 |

Keep 2 minutes of slack inside the tour. If you run long, shorten stop 7 (LNG) to one minute.

---

## 0. Welcome (2 min)

**Say:**
- "Every power plant runs on cable. Today we walk through a complete gas power campus, built as a 3D model with a full cable schedule, and look at what each part does and where our products go."
- "No engineering background needed. At each stop you'll get three things: what it does, its electrical system, and the cable."

**Housekeeping:** questions in the chat, answered at the end. The recording will be shared.

---

## 1. Market and fundamentals (28 min, 31 slides)

Market slides 6-11 come from the Oct 6 PowerGen channel deck. **OEM, owner and EPC names are not on the slides; say them here if useful.** Verify the figures against the primary sources (appendix of the Oct 6 deck) before Nov 11.

**Slide 16: Every power plant is this (1.5 min).** The definitions: source (input: fuel or nature) → conversion (the black box: turbine and generator, engine, panel, fuel cell) → power (output: to the grid through a switchyard, or behind the meter). "Every plant fits this picture; what changes is the source and the machine in the box."

**Slide 17: How electricity is made: four families (1.5 min).** Thermal (heat spins a turbine: gas, coal, nuclear, biomass, geothermal, oil), water and wind (hydro, wind), direct (solar PV, fuel cells: no turbine, DC) and storage (batteries, pumped hydro: shifts power, does not make it). Firm vs variable. "Almost all of them spin a generator; every one of them ends in cable. Today: gas, inside the thermal family." Our campus has gas, engines, aeros and package boilers, the fuel-cell bank and the battery yard.

**Slide 18: The mix today, and why gas (2 min).** US electricity 2025 (EIA): gas 41%, nuclear 18%, coal 17%, wind 11%, solar ~7%, hydro 6%. Planned 2026 additions: 86 GW, mostly solar (43.4) and batteries (24), wind 11.8, gas 6.3. "Southwire cables every one of these. Today we zoom in on gas: it is firm, it is the backbone, and the next wave of data-centre load needs it."

**Slide 20: At a glance (1.5 min).** 378 GW in development (52 GW under construction), ~$1.2B core cable 2026-2035, 386 projects tracked, $50M+ booked in Q3. "Today's goal: know the plant, so you can follow the cable through it."

**Slide 21: Load growth (2 min).** 166 GW peak-load growth by 2030 (about 90 GW data centres); 378 GW gas in development (189 GW tied to data centres); 52 GW under construction; turbine lead times up to 7 years. The chart: the 2000-04 merchant boom built 188 GW (peak 57 GW in 2002); 2015-25 averaged 8.1 GW a year. "Today's pipeline needs a boom-scale build again."

**Slide 22: Turbine backlogs (1 min).** Turbine OEM 1 = GE Vernova (116 GW, firm backlog plus slot reservations, Q2 2026); OEM 2 = Siemens Energy (~69 GW gas-turbine backlog, Q3 FY26); OEM 3 = Mitsubishi Power (35 GW large-frame, Aug 2026). Tiles: +72% Caterpillar power-generation sales Q2 2026; 2.3 GW VoltaGrid modular fleet for Oracle's Texas AI data centres plus 1 GW for Vantage; 500 MW standard modular SGT-800 plant from Siemens Energy and Eaton.

**Slide 23: The cable prize (2 min).** 378 GW to 93.7 GW modeled additions to ~$180B of plant investment to $0.75-1.2B of wire and cable: under 1% of capex, on the critical path. By PO year: $673M named projects, $501M future allowance; peak 2028-29.

**Slide 24: The register (1 min).** 205.8 GW eligible; 68% only announced. Top states TX 55.5, LA 16.3, WV 13.4 GW (AZ is 6.1). Example owners if asked: NRG, CPV, Entergy, Homer City Redevelopment. Named EPCs: Kiewit/TIC, Zachry, Gemma, PCL, Burns & McDonnell; 87% of gross capacity has no confirmed constructor yet.

**Slide 25: Where the build is (1 min).** The state heat map: TX 55.5 GW leads, then LA, WV, IN, OH, PA. Owners: IPPs and behind-the-meter developers mostly build new; utilities reuse old sites (coal-site repowers 41.3 GW).

**Slide 27: Open the box: the physical anatomy (1.5 min).** Back to the black box, now for gas: the six steps from fuel infrastructure to end use, grouped under input, black box and output. "Same physics on every project; what changes is the machine in the box, and who owns it."

**Slide 66: Four ways to burn gas for power (2 min).** Simple cycle (the peaker), combined cycle (the workhorse, our power block), engines (the sprinter) and aeroderivatives (the jet): size, efficiency, start time, how they run. Units: GW, MW, kW; MW is power, MWh is energy.

**Slide 28: A day on the grid (1.5 min).** Illustrative 24-hour demand: baseload all day, solar at midday, combined cycle in the middle, peakers and batteries on the evening peak. "Every start cycles the plant and its cable."

**Slide 29: The power block, as you would see it (30 s).** The aerial in full colour, labelled: gas turbines in the hall, HRSGs, stacks, steam turbine, air-cooled condenser, step-up transformers. "This is the power block. Now watch how it makes power, one stage at a time." Click.

**Slides 30-33: Combined cycle, a four-click build (2.5 min).** The same aerial of our power block, darkened; each click lights one stage on the real equipment, and the flows follow the real routes. 15: the gas turbine (air in, power out to the step-up transformers, about 2/3 of the power). 16: the HRSG catches the ~1,100 °F exhaust and makes steam, no extra fuel. 17: the steam turbine makes about 1/3 more; the condenser returns the water. 18: all lit: "Burn the gas once, use the heat twice": ~60% vs ~40%, 3 + 1, 8,234 cables in the power block and its condenser. (The old flow diagram, boilers slide 6, is the backup.)

**Slide 67: How an HRSG works (1.5 min).** Reuse boilers slide 5: the "What it is" and "Fun facts" box.

**Slide 34: Copper X-ray (30 s).** Same view, one more click after the cycle with the steel made glass and every cable glowing copper. "Take the plant away: the cable stays. About 8,200 cables and 440 miles in the power block and its condenser." Let it land; say nothing for a beat.

**Slide 35: X-ray by type (1.5 min).** "Now sort it by job: five kinds of cable." Only what is in the picture: the power block and its air-cooled condenser, 8,234 cables, about 440 miles. Every route glows by type (each route takes the colour of the type with the most cables on it): green instrumentation dominates. MV/HV 232 cables (28 mi), LV power 1,160 (95 mi), control 1,255 (94 mi), instrumentation 5,484 (202 mi), fibre and fire alarm 103 (21 mi). "The big cables get the attention; the small ones are most of the miles." If asked how: every device in the model gets its own cable, routed on the modelled trays: (route + drops + 20 ft) x 1.1. A conceptual estimate, not an engineered take-off. The whole campus (modular yard, BESS, CCS, LNG) is about 21,000 cables and 1,200 miles: that is the next slide (36).

**Slide 36: Now pull back, the whole campus (1 min).** One level up from slide 35, same idea as the two one-lines (11 simple, 12 full). The campus X-ray with cable by area: power block 7,353 and ACC 881 (the 8,234 of the last slide, in copper), then the modular yard 5,001, carbon capture 2,753, fuel supply 1,275, grid 1,215, BESS 1,155 and the rest: 21,138 cables, ~1,143 miles (building wire, grounding and overhead not counted; the schedule total with those is 21,217 and 1,212 mi). "The power block is the densest piece; the campus is 2.6 times as much." Instrumentation is 73% of the cable count but most of it is small.

**Slide 37: From the generator to the light switch (1.5 min).** Generator 13.8-25 kV → step-up to 115-765 kV → transmission → substation → 4-35 kV distribution → 480/240/120 V at the customer, with the cable family at each step. "Southwire has a product at every step."

**Slide 38: The voltage ladder (2 min).** Reused from the boiler deck (slide 9, "Levels, ratings and the cable they drive"): 230 kV to the grid, 21 kV at the generator, 13.8 kV to the big motors, 480 V to the small ones, 120 V AC / 125 V DC for controls, then signals. "Every rung has its own cable family."

**Slide 39: Cable 101 (1.5 min).** The eight families: HV, MV, LV power, VFD, control, instrumentation, fibre, grounding. By length in SW-3X1: instrumentation 44%, LV power 20%, control 18%, MV/HV 7%.

**Slide 40: What a power plant does to a cable (1.5 min).** Heat, cycling, electrical noise, hazardous areas, fire and smoke, outdoors, schedule, each with the answer (VFD-rated cable, ARMOR-X MC-HL, SIMpull, pre-terminated). "The wrong cable fails early, and a cable failure can trip a unit."

**Slide 68: Follow the power (1.5 min).** SW-3X1 cable by plant area, from the model's schedule: the black box (turbine hall, HRSGs, cooling, water) holds 44% of the campus's 1,212 miles. The POI is where the plant meets the grid: plant side is owner and EPC scope, past it the utility's. "The grid connection carries the biggest cables; the power block carries the most."

**Slide 41: Same physics, different owners (1.5 min).** IPP = one company per plant + asset + power purchase agreement + customer + investors + market (ERCOT, PJM, MISO). Utilities and co-ops buy like utilities; hybrid IPPs both ways; pure IPPs are our sales focus for competitive thermal power.

**Slide 42: Greenfield and brownfield (1.5 min).** Five kinds of site from the register: greenfield grid-connected 77.0 GW, data-centre / behind-the-meter campus 54.5, coal-site repower 41.3, expansion at an operating plant 21.4, industrial captive and site reuse 11.6. New sites take the whole cable scope; existing sites mean tie-ins, live equipment and outage windows. Plus work on running plants (HRSG module replacement: the boiler deck's outage story). Utilities mostly reuse old sites; IPPs and BTM developers mostly build new.

**Slide 43: Who buys, and when (1.5 min).** Develop → finance → engineer (the owner's engineer specifies the cable) → procure (the EPC or package builder buys it) → build (cable pulls on the critical path) → operate. "Be in the spec early; be ready when the EPC buys."

**Slide 46: A modern gas plant (1 min).** Six things beyond the power block, all in the model: private 5G monopole (massive-MIMO), EV charging and solar carport, the BTM data centre, LNG by sea, hydrogen, carbon capture, each with its own cable.

**Slide 48: The campus at a glance (2 min).** The campus aerial with the LNG terminal and the seven stops.
- "This is SW-3X1, a 3x1 combined-cycle plant: three gas turbines, three HRSGs and one steam turbine, with a modular generation yard, a battery yard, a behind-the-meter data centre, LNG supply, and options for carbon capture and hydrogen."
- "Conceptual and not engineered, but sized like real plants."

---

## 2. The 3D tour: seven stops (18 min, about 3 min each; stop 7 is 1 min)

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

## 3. Wire and cable takeaways (6 min, 3 slides)

**Slide A: The whole campus in one number (3 min)**
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

## 4. Q&A (6 min)

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
