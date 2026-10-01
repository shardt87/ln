# SK-3X1 3x1 combined-cycle plant: 3D model

A 3D coordinate model of the plant in **SK-3X1 Drawing Set Rev 14**: three H-class GTs, three HRSGs, one ST, an 80-cell ACC and a 230 kV breaker-and-a-half switchyard. It also includes the optional and adjacent-market systems: carbon capture, BESS, modular and portable power, GT inlet chilling, an LNG satellite and 25 MW of green hydrogen. The model is checked back against the drawing by `verify.py`.

> Conceptual illustration. Not engineered. Not for construction.

## Verification (current build)

| Check | Result |
|---|---|
| Footprints: every filled shape on sheets 01 and 05 matched within 0.6 ft | 211 / 211 |
| Heights on sheet 13 reproduced | 21 / 21 |
| Sheet 09 coordination screen: clearances and hook margins recomputed from the model | 10 / 10 |
| Clashes between parts of different items (34,154 pairs tested) | 0 |
| Parts outside the compound or wrongly below grade | 0 |

The checks corrected the model in several places:

- **GT combustor cans** poked above the EL 38 envelope, which cut the GT hook margin to 9.7 ft instead of the 11 ft on sheet 09.
- **ACC steam riser** went up through the fans. It now runs under the deck and rises at the street ends.
- **ST exhaust duct** clashed with the ST aux skid.
- **Hoist beam** stood above the filter-house top.
- **Three shapes were misread:** the filter-house stair tower, the hoist landing with truck access, and the gallery-door forklift apron (all identified from sheet 10).

## Files

| File | What it is |
|---|---|
| `build_model.py` | Model source: 338 register items built from about 3,000 primary parts (boxes, cylinders/cones, A-frames, lofts). Writes `sk3x1_model.json`. |
| `detail.py` | Detail pass (about 9,100 parts). See "Detail layer" below. |
| `modular.py` | RICE engine hall and simple-cycle units at LOD 3. See "Modular power yard" below. |
| `yard.py` | Gensets, trailers, fuel cells, microturbines and skids in the modular yard at LOD 3. |
| `pipes.py` | Round pipes, elbows, flanges and insulation jackets generated from the process-pipe routes. |
| `hall.py` | Turbine hall machines and skids at LOD 3. |
| `trays.py` | Ladder trays with cables, supports and drops, and the IPB phase enclosures, from the routes. |
| `hrsg.py` | HRSG casing, SCR, drums, steam leads and blowdown tanks at LOD 3. |
| `fuel.py` | Fuel systems at LOD 3 (gas yard, M&R train, GT gas fuel modules, ULSD area), pipe supports and road-crossing sleeves. See "Fuel systems" below. |
| `routes_base.json`, `routes_optional.json` | Tray, bus, duct-bank, 230 kV and process-pipe centrelines from the vector geometry of sheets 01 and 02. |
| `extract_reference.py` | Pulls reference geometry from the drawing PDF into `reference/sk3x1_rev14_reference.json` (committed, so the PDF is not needed to verify). |
| `verify.py` | Runs the checks above and writes `verify_report.json`. Exits 1 on failure. |
| `palette.json` | Colour for each material key, shared by the viewer and the OBJ export. |
| `viewer/index.html` | Interactive Three.js viewer: physically based materials with procedural textures (ribbed cladding, concrete, gravel, asphalt, grass, grating, fin stripes), a sky with fog, camera-following shadows and a Detail toggle. It also has the sheet 11 views, layer toggles, a section cut by elevation, a live X / Y / EL readout, an inspector, the equipment register, a verification report, electrical rooms and the motor schedule. |
| `threejs/` | GT train 1 bay as compact JSON (`export_bay.py`) and a standalone three.js r181 scene (`gt1_bay_scene.js`, `bay.html`). |
| `site/build_site.py` | Assembles the GitHub Pages site: the viewer, the bay scene and a render gallery. |
| `render.go` | Line art using this repository's `ln` engine, one SVG + PNG per sheet 11 view in `renders/`. |
| `export_obj.py` | Wavefront OBJ + MTL for Blender, SketchUp or Rhino: one group per item, with the layer in the group name. |
| `blender/` | Blender build script (sheet 11), label annotation, contact sheets, render summary and requirements. |
| `renders/blender/` | Annotated Cycles renders and contact sheets. |

## Detail layer

`detail.py` runs after the primary model is built. It adds:

- open stair towers with switchback flights, landings and handrails, in place of solid blocks;
- guard rails on every raised platform and ring platform;
- caged ladders on the stacks, absorbers, strippers and tanks;
- sheds on every bushing and post insulator, and fans under the transformer radiators;
- lattice bracing and shield wires in the switchyard;
- process piping on the rack tiers;
- HRSG side platforms and downcomers;
- doors and louvres, light poles and fence posts.

Detail parts carry `d: 1`. None of them come from the drawing; all are typical. `verify.py` therefore checks the primary geometry against the drawing and runs only the bounds check on the detail parts. In the viewer, the Detail button toggles them.

## Site audit (connections and leftovers)

`audit.py` complements `verify.py`. It checks that:
- every route end lands on equipment or on another route (switchyard buses and future bays, the gas yard pad and the fence entry count as valid ends);
- every generating and electrical unit is connected, directly or through its own auxiliaries;
- nothing floats;
- nothing remains from removed options (SC-3/SC-4, RICE hall 2);
- tags are unique.

The first run found connections the drawing leaves open. They are now routed as typical:

- **GT fuel gas:** the drawn header stopped over HRSG 1. It now ends at the GT1 branch, and each GT gets a branch between the HRSGs to its fuel skid, clear of the feed pumps and the ST.
- **SC-1/SC-2 fuel gas:** a line from the fuel-gas compressor building to both packages.
- **CCS circulating water:** carried from the utilities road to absorber B.
- **Modular expansion:** `OPT_MODX_ROUTES` connects the gensets to the paralleling e-house and on to PAD-EH, and the trailer turbines to PAD-EH. It runs the fuel cells (a tail each) and microturbines to MOD-LV, and gas stubs from the portable-pad skid and the modular gas header.
- **LNG terminal (coastal A):**
  - a buried power cable from the plant switchyard to the terminal substation;
  - the MV trench extended to the send-out pumps and the seawater intake;
  - a relief header from the tank to the flare knock-out drum, on T-bents;
  - a seawater outfall back to the sea.

The audit now reports CLEAN and runs in CI.

## Detail layer 3 (close views)

`detail3.py` runs after `detail.py` and adds dressing for close views:

- **Buildings:** window bands, a concrete base band, rooftop HVAC units with fans, downspouts.
- **E-houses:** wall panel seams and a roof overhang.
- **Tanks:** spiral stairs with handrails, a roof rail and vent, nozzles, a manway.
- **RICE hall:** roof ventilators, a charge-air filter per engine, roll-up doors.
- **Simple-cycle and trailer turbines:** ventilation fans and filter hoods.
- **BESS containers:** HVAC units and door seams.
- **Stacks and absorbers:** aviation warning lights.
- **Buildings by use:** offices (the gatehouse and the control/admin building) get window bands and a glazed entrance with a canopy. R1 (electrical) stays closed, with louvres. Industrial buildings (warehouse, workshop, water treatment, compressor and pump houses, and so on) get ribbed metal cladding, a high translucent strip, wall louvres, roll-up doors with bollards, and skylights and ridge vents on the warehouse and workshop.
- **Site:** lane markings and cars in the parking lot, plus a solar carport over the two middle rows. It has an EV charger pedestal at every bay, green EV bay markings, and a DC fast-charger cabinet with its transformer.

Like the first detail layer, these parts carry `d: 1`, are typical rather than from the drawing, and are only bounds-checked. Windows use a tinted, glossy glazing material in the renders and the viewer. The epic set gains E9 (water tanks) and E10 (control building across the car park).

## Fuel systems (LOD 3)

`fuel.py` runs inside `build_model.py` and models the fuel train in process order. It keeps the drawn footprints and envelopes; what sits inside them is typical, not engineered.

| Area | What is modelled |
|---|---|
| Pipeline M&R (SK-3X1-14, keys 1-9) | **Pig receiver:** barrel, quick-opening closure and davit, reducer, saddles, pig signaller.<br>**ESD valve:** with its insulating joint.<br>**Horizontal filter-separator:** sump boot, relief valve, nozzles.<br>**Three water-bath line heaters:** burner ends, exhaust stacks, expansion tanks, burner panels.<br>**Two ultrasonic custody meter runs:** under a sunshade.<br>**Interconnecting piping on sleepers:** inlet and outlet heater manifolds, a liquids line to the condensate tank, a sample line to the gas quality building. |
| Plant gas yard (SK-3X1-12) | **New inlet station:** ESD valve, block valve and insulating joint.<br>**Conditional compressor tie-ins:** suction, discharge and bypass valve.<br>**Check-metering skid:** 2 x 100% ultrasonic runs, flow conditioners, block valves, flow computer, sunshade.<br>**Regulation skid:** slam-shut, monitor and active control valves on 2 runs, plus a relief vent.<br>**Shell-and-tube performance heater:** heated by IP feedwater (new insulated supply and return from HRSG 3, on T-posts).<br>**Two 100% final filter-separators.**<br>**Outlet to the GTs:** motor-operated valve and an ESD valve.<br>**Maintenance vent stack:** with its vent header.<br>**Tie-ins:** for the LNG, H2, simple-cycle and temporary-power options. |
| Conditional fuel-gas compressors | Three motor-driven packages with cylinders, suction scrubbers, relief vents and fin-fan aftercoolers. |
| GTs | **GFM-1..3:** gas fuel modules (stop/control valves, final strainer) on the turbine deck. The fuel-gas branches now rise at the hall's north wall to these modules instead of stopping under the deck. |
| Backup fuel (ULSD, conditional) | **Containment dike:** with step-overs.<br>**Truck unloading station:** canopy, curb, tanker and unloading arm.<br>**Pump skid:** unloading and forwarding pumps, duplex strainers.<br>**Fuel-oil route:** a new route type, one tier above the gas, to each GFM. |
| Modular yard | Gas-conditioning skids for the simple-cycle units and the portable pad: coalescing filters, control and slam-shut valves. |

**Pipe supports and road crossings.** Low pipe routes (fuel gas, fuel oil, feedwater, cooling and chilled water, hydrogen, LNG) used to hang in the air. Two changes fix this:
- **Supports:** the routes now sit on concrete sleepers (up to EL 5.5) or steel T-posts every 20 ft, kept clear of equipment and roads.
- **Road crossings:** where a low route crosses a road, the 18 crossings drop into a sleeve below grade, with a headwall at each edge.

The drawing's LV trays inside the gas yard and the M&R station now run in buried conduit (hazardous area) rather than on 30 ft trays.

**New views:**
- **Viewer:** a "Fuel systems: M&R, gas yard, ULSD" view.
- **Epic set:** E11 (plant gas yard), E12 (M&R station) and E13 (the fuel systems from above).

## Modular power yard (LOD 3)

`modular.py` runs after `fuel.py`. It rebuilds the RICE engine hall and the two simple-cycle units inside their drawn footprints, keeping the sheet-13 heights (RICE stacks 90 ft, aero stacks 80 ft). The equipment is typical, not engineered.

- **RICE engine-generators (x8):**
  - **Engine:** V18 block on a common base frame, two banks of nine cylinder heads, charge-air manifold in the V, two turbochargers at the free end.
  - **Generator:** flywheel housing, generator with terminal box and feet.
  - **Hall:** an overhead crane with a runway, and eave gutters.
- **RICE exhaust trains (x8):**
  - **Path to the SCR:** turbocharger risers through the south wall, then an expansion joint, then the SCR + oxidation catalyst on a steel stand.
  - **Downstream:** silencer, then the stack with a platform, handrail, caged ladder and stiffener rings.
  - **Ancillaries:** urea dosing cabinet, SCR access platform and ladder.
- **RICE radiators:** fan shrouds and motors, bundle headers, jacket-water supply and return from the hall.
- **Simple-cycle units (x2):**
  - **Inlet:** filter house on legs, with a filter-change platform and ladder.
  - **Package:** generator and turbine enclosures on one skid, doors and CO2 cylinders.
  - **Exhaust:** collector lofted into the SCR / CO catalyst housing. The housing has casing stiffeners, an ammonia injection grid, two access platforms with a stair, an outlet duct and a stack platform.
  - **Lube oil:** fin-fan cooler with two fans.

New epic cameras: E14 (the RICE exhaust trains and stacks) and E15 (a simple-cycle unit).

`yard.py` runs after `modular.py` and details the rest of the modular yard inside the drawn footprints:

- **Containerized and enclosed gensets** (CONT-1..8, GEN-E, the black-start gensets): an enclosure on sleepers with corrugation ribs, corner castings, end and side doors, intake louvres, a roof radiator with fans, and a roof silencer and stack.
- **Trailers:**
  - MOB-1 genset and the load bank: chassis, axle sets, landing legs, gooseneck, roof fans.
  - TM-1/2 turbines: gooseneck, landing legs, walkway and stair, exhaust collector, doors.
- **Open engine skid (GEN-O):** radiator and fan, engine, generator, panel.
- **Fuel cells (FC-1..12):** four power-module cabinets each, with doors, handles and roof exhaust vents.
- **Microturbines (MT-1..6):** ribbed enclosures with roof intake hoods and exhaust outlets.
- **Conditional systems:**
  - BESS black-start alternative: two battery containers with HVAC and a PCS.
  - SC inlet chillers: chiller packages with roof fin-fans and a chilled-water line.
- **Small skids:**
  - water-injection skid: pumps, filter, sunshade;
  - aqueous-ammonia tank: on saddles, in a curbed containment.

New epic cameras: E16 (the portable power pad) and E17 (the fuel cells and microturbines).

## Round pipes (LOD 3)

`pipes.py` runs after the supports pass. It turns every above-grade process-pipe route into round pipe geometry: steam, condensate, feedwater, closed cooling water, fuel gas, fuel oil, circulating and chilled water, hydrogen and LNG.

- **Straight runs:** cylinders. Where several drawn circuits share one line they merge into a single pipe.
- **Elbows:** a long-radius bend (1.5 D) at every change of direction, mitred in four segments.
- **Drops to grade:** elevated lines drop to grade at their free ends, with a closing flange.
- **Flanges:** weld-neck flange pairs about every 40 ft.
- **Insulated lines** (steam, condensate, feedwater, chilled water, LNG): an aluminium jacket with seam bands every 12 ft and a coloured identification band every 60 ft.
- **Bare lines:** painted in their service colour, with fuel gas in safety yellow.

The route centrelines stay in the model for the register, the legend and picking. Renderers use the round geometry and no longer draw boxes for these routes:
- **Blender:** draws only the round pipes.
- **Viewer:** keeps an invisible box so a click still selects the route.
- **OBJ:** exports the round pipes.

The epic set gains E18: fuel gas, fuel oil and feedwater crossing the east spine road.

## Complete switchyard and GSU orientation

- **Complete 230 kV yard:** Rev 14 installs 9 of the 15 breaker positions (D1-D3). The model now also shows the build-out on the `SWYD_FUTURE` layer, which appears with the optional systems and in the complete-plant view. That build-out adds 9 more breakers, for 18 in total:
  - **D4:** T-MOD-1/2 (modular yard) on the lower position and the BESS main power transformer on the upper position. The BESS connection is a new 230 kV cable to the take-off gantry.
  - **D5:** the CCS 230 kV cable.
  - **D6:** the green-H2 import and a spare. D6 sits on a 120 ft extension of both buses, with dead-ends at x 2,045 and its own gravel pad.

  Each built-out diameter carries three dead-tank SF6 breakers, disconnect stands and take-off gantries.
- **GSU orientation:** the GSUs (GSU-1..3 and GSU-ST) now face the switchyard.
  - **South (HV) side:** the 230 kV bushings stand in an east-west row along the south edge. Each has a surge arrester in front, and conductors drop to a 45 ft take-off gantry where the overhead line to the diameter leaves.
  - **North (LV) side:** the conservator and the isolated-phase bus throat sit on the north side, towards the generator and the GCB.
  - **Before the change:** the bushings stood in a north-south row on the tank centreline, so the HV side read as facing east.
- **New epic cameras:** E19 (GSUs facing the yard) and E20 (the complete switchyard).

## Turbine hall, cable trays and IPB (LOD 3)

`hall.py` rebuilds the machines on the EL 20 deck. It keeps the footprints and the envelope tops that the sheet-09 crane screen measures (GT EL 38, generator EL 36, ST EL 46), so 10/10 still reproduce. The detail inside is typical, not engineered.

- **H-class GTs (cold-end drive):**
  - **Front end:** baseplate, inlet plenum, bellmouth, and a compressor casing with horizontal-joint flanges, stiffener rings and the VGV actuator ring with its actuators.
  - **Hot section:** a combustor section with 16 can covers on a fuel-gas manifold ring with pigtails, fed from the gas fuel module. Then the turbine casing, strut flange and exhaust diffuser.
  - **Supports and services:** front and rear supports, lube-oil supply and drain lines to both bearings, and junction boxes with conduits to the LV tray drop.
- **H2-cooled generators:** stator frame with ribs, end shields, hydrogen cooler housings with cooling water, bearing pedestals, collector end, coupling guard. A line-side terminal box under the south end feeds the IPB.
- **Steam turbine (HP-IP-LP-generator):**
  - **Casings:** an LP casing with its east side-exhaust hood and a transition to the 26 ft duct, and a combined HP/IP casing.
  - **Steam path:** a crossover pipe, and main stop / control valve chests fed from the main steam line.
  - **Generator:** the STG.
- **Skids:**
  - **Lube-oil skids:** reservoir, AC/DC pumps, duplex filters, coolers, mist eliminator.
  - **CO2 fire suppression:** cylinder racks with a discharge manifold.
  - **Compressor water wash:** a tank and pumps piped to the inlet.
- **Plenum spools:** flanged ducts. The amber drawing highlight is gone.
- **Hall fit-out:** crane rails, high-bay lights, wall girts.

**Unit electrical equipment and hall cabling (typical; the drawing leaves these to the vendor):**
- **Per GT unit:**
  - **South gallery:** static excitation cubicles (EXC-n), a dry-type excitation transformer (ET-n) and a surge-protection / VT cubicle on the IPB (SPC-n).
  - **Deck:** a neutral grounding cubicle at the generator neutral (NGT-n) and turbine control and protection cabinets (TCP-n).
- **ST:** EXC-ST, NGT-ST and TCP-ST.
- **Control / instrument backbone:** runs from R1 along the hall north wall at EL +42.
  - **Control drops per unit:** to the TCP, the GT junction boxes, the NGT and GCB, and the excitation / IPB cubicles.
  - **LV feeders:** to the CO2 skid, water wash, gas fuel module, TCP UPS and generator auxiliaries.
  - **Excitation connections:** the ET tap from the IPB, the ET to EXC link, and the DC field cables to the generator collector end.
  - **GSU and UAT marshalling cabinets:** tied into the duct bank.
- **Hall services:** a crane conductor bar, lighting circuits, grounding risers on the columns, and a ladder-tray riser to each filter-house platform for the pulse-jet and anti-icing controls.

`trays.py` generates the cable trays and the isolated-phase bus from the routes, and the renderers draw these in place of the old boxes.
- **Ladder trays:** MV at EL +36, LV at +30 and control at +42. Each has galvanised rails and rungs with cables laid in, and collinear runs merge.
- **Tray supports:**
  - carried by the pipe racks where one runs under the tray;
  - wall brackets with knee braces near the hall walls;
  - trapeze stanchions from the deck or grade elsewhere.
- **Tray drops:** vertical drops at the free ends down to the equipment they feed.
- **IPB:** three round phase enclosures with joint bands on steel frames, running from the generator terminals through the GCB to the GSU, with the UAT tap.

**Cutaways and cameras:**
- **Cutaway renders:** pro cameras can hide named items for one render (`hide`, `hide_layers`). The four new turbine-hall cameras render with the hall walls and roofs removed.
- **New cameras:**
  - E21: the hall from the laydown bay;
  - E22: a GT1 close-up;
  - E23: the north-wall trays;
  - E24: the IPB, GCB and GSU;
  - E25: the south gallery with its excitation and IPB cubicles and the cable drops.
- **Viewer:** the "X-ray hall" toggle shows the same detail.

## HRSGs (LOD 3)

**Proportions (typical large horizontal HRSG, as on GE Vernova-class units).**
- **Casing:** about 78 ft tall. The sheet-13 note gives ~70 ft for a 501G HRSG and 85 ft for the largest.
- **Drums:** HP, IP and LP stand on an open steel frame from EL 79 to 89, with walkways, so the risers show between the casing roof and the drums. The overall top stays at the drawn EL 100.
- **Casing face:** shows its insulated panel modules in two tones between the buckstays and wale bands.
- **Ducts:** the inlet transition and the outlet breeching follow the lower casing.
- **East-face platforms:** sit at EL 25, 50 and 74.

`hrsg.py` details the three HRSGs: three-pressure reheat, horizontal gas flow, with SCR. They stay inside the drawn 70 x 160 ft envelope and the sheet-13 top of EL 100, so 21/21 heights still reproduce. The detail is typical, not engineered.

- **Casing:**
  - external buckstays every 8 ft and wale bands;
  - module seams at the coil-section breaks (HP SH / RH, HP evaporator, SCR + CO catalyst, HP economizer / IP SH, IP evaporator, LP evaporator / IP economizer, LP economizer);
  - access doors per section.
- **SCR:**
  - catalyst-loading doors on three levels and a CO catalyst door;
  - an ammonia injection grid (riser, lances and balancing valves);
  - an ammonia vaporization / dilution-air skid at grade;
  - a catalyst-handling monorail with a hoist, cantilevered over the west wall.
- **Drums (HP, IP, LP):**
  - dished heads with manways, two rows of risers from the roof headers, and downcomers at both ends down the west wall;
  - two spring safety valves per drum, with vent pipes and silencers to about EL 109;
  - level gauges and a roof handrail.
- **Steam and water:**
  - main steam, hot reheat and LP steam leads run over the east roof edge and down the north face beside the breeching to the pipe rack;
  - feedwater runs from the boiler feed pumps up the east face to the economizer.
- **Other:** the GT exhaust expansion joint, inlet-duct stiffener frames, stack stiffener rings and CEMS sampling ports, and a blowdown tank per HRSG.

New epic cameras: E26 (HRSG 1 and its stack from the north-west) and E27 (the HRSG roofs).

## Cable schedule and tray coordination

**Cable schedule.** Every tray class carries a typical cable schedule.
- **Where it shows:** in the model data, and in the viewer's inspector when you click a tray. The cables lie in the trays in schedule order and colour, packed in layers inside the side rails.
- **Basis:** this is a selection, not an engineered schedule. Southwire product families are named as the requested supplier; confirm part numbers and sizes with the supplier.

| Tray | Cable types | Jacket in the model |
|---|---|---|
| MV (EL +36, +48 in the hall) | 15 kV MV-105 1/C Cu, 133% EPR, copper-tape shield, triplexed (ICEA S-93-639 / UL 1072); 15 kV ARMOR-X MC-HL / MV-105 3/C (continuous corrugated welded armor) | red |
| LV (EL +30, +44 in the hall) | 600 V power, Cu XHHW-2, Type TC-ER (UL 1277); 600 V ARMOR-X MC-HL power / VFD cable for Class I Div 2 areas (UL 2225); 600 V control, Type TC-ER | black; grey (armored) |
| Control / instrument (EL +42) | 600 V control, 14 AWG Type TC-ER (ICEA S-73-532); instrumentation shielded pairs / triads, Type TC-ER / PLTC (blue for intrinsically safe circuits); thermocouple extension, type KX (ANSI MC96.1 yellow); fire alarm FPLR; fibre optic | black; blue; yellow; red; orange |
| Lighting and small power | Cu THHN/THWN-2 building wire in conduit (UL 83) | in conduit |

**GT thermocouples.** Each GT carries 16 exhaust thermocouples around the diffuser and 8 wheel-space thermocouples on the turbine casing. Rings of yellow type KX extension cable run from them to the junction box.

**Tray coordination fixes.** These come from a clash review of the generated trays.
- **Seating:** trays sit on their rack tier (the route elevation is the tray bottom) instead of passing through the tier beams.
- **Turbine hall:** the MV and LV runs ride above the GT exhaust ducts, LV at EL +44 and MV at +48. Each connected chain from R1 is raised together, and the tail to the ST aux skid stays at +30 under the ST exhaust duct.
- **Legs shifted off structure:** drawn tray legs that sat on column lines move a few feet clear: the HRSG stair towers, the ACC column line, the main-steam duct supports and the rack bents.
- **Other runs re-routed:**
  - the ST control run goes down the west side of the ST;
  - the rack tier-30 pipes moved to the north half of the rack;
  - a crossing rack stops its pipes at the junction.
- **Drops:** junction ends of split drawing runs no longer drop to grade. Drops land on whatever is below them and are omitted over pipes.
- **Supports:** every support, bracket and IPB frame checks the surrounding geometry, and shifts up to 5 ft or is left out.
- **Drawing conflict found:** sheet 01 puts the middle filter-house columns (x 630 / 790 / 950, y 366-369 and 400-403) on the GT centreline, where the IPB and the GCB also sit.
  - The columns stay as drawn.
  - The IPB jogs 7 ft east past each column line and returns to the centreline through the GCB.
  - The UAT tap leaves the GSU-side leg, and the GSU LV throat is offset to meet it.
- **New audit check:** `audit.py` now checks that no tray, cable, support, drop or IPB part passes through structures or equipment. The allowed exceptions are the IPB entering its GCB and generator terminals, and trays through the R1 wall sleeves.

## GitHub Pages

`.github/workflows/sk3x1-pages.yml` rebuilds and verifies the model, then assembles the site with `plant/site/build_site.py`. The site has the viewer as `index.html`, the GT1 bay close-up as `bay.html`, and a render gallery as `renders.html`.

The workflow always uploads the site as the **sk3x1-site** artifact. It also deploys to GitHub Pages once the repository owner has turned Pages on (Settings → Pages → Build and deployment → Source: GitHub Actions). A workflow token cannot turn Pages on by itself.

## Blender renders (local or GitHub Actions)

`blender/SK-3X1_Rev14_blender_build.py` is the build script named on sheet SK-3X1-11. It:

- builds the model into Blender collections named as on that sheet;
- fits the orthographic 1920 x 1080 cameras to each view with the 3% margin;
- renders with Cycles.

There are two styles:

- **drawing** (the sheet 11 look): white world, neutral grey equipment, copper only on cables, trays and bus, and dark Freestyle outlines.
- **photo:** a Nishita sky, sun shadows and darker real-world albedos.

`blender/annotate.py` then burns in the equipment labels and the credit block, and `blender/contact_sheet.py` tiles the views onto one page.

```sh
pip install -r plant/blender/requirements.txt          # bpy 4.2 (Blender as a Python module) + Pillow
python plant/blender/SK-3X1_Rev14_blender_build.py --views A,B --style drawing --samples 64
python plant/blender/annotate.py plant/renders/blender
# or inside a Blender install:
blender -b -P plant/blender/SK-3X1_Rev14_blender_build.py -- --views A --style photo --blend sk3x1.blend
```

The GitHub workflow `.github/workflows/sk3x1-blender-render.yml` runs in three stages:

1. It runs `verify.py` and fails if the model JSON is stale.
2. It renders all views in five parallel jobs.
3. It publishes an **sk3x1-renders** artifact. That artifact holds the annotated PNGs, contact sheets, `SK-3X1_Rev14.blend` and the OBJ, and each run has a job summary.

It runs on every push that touches `plant/`, and you can also run it by hand. The manual run (Actions → SK-3X1 Blender renders → Run workflow) lets you choose the views, samples and resolution.

Sheet 11 lists ten views, and the render loop was adjusted over several review passes:

| Issue | Fix |
|---|---|
| Framing too wide (view A was 2,108 ft) | Clip the fit set to D1–D3. It is now 1,325 ft; sheet 11 gives 1,438 ft. |
| Coplanar road crossings rendered as black squares | Stagger the road heights. |
| Hidden collections blocked the label visibility rays | Exclude hidden collections instead of hiding them. |
| Freestyle strokes below 1 px vanished | Set strokes to 1.8 px. |
| Collinear tray runs overlapped and rendered black | Merge the runs per tier. |
| Stormwater basin appeared black | Build the ground slab around the basin and recalculate normals. |
| Photo style overexposed | Lower the sky and exposure and use real-world albedos. |

## Professional renders and presentation board

`--style pro` switches the Blender build to a presentation look:

- **Materials** (`blender/pro_look.py`): procedural and physically based, with bevelled edges. They include ribbed metal cladding, broken-up concrete, galvanised steel with varied roughness, gravel, asphalt, porcelain insulators, safety-yellow rails and a see-through chain-link fence.
- **Landscape:** grass, about 550 trees in clusters and windbreak rows, and the public road to the main gate.
- **Light:** a late-afternoon Nishita sky with the sun at 24° altitude, azimuth 258°.
- **Cameras:** six perspective hero cameras (P1–P6) with real lens lengths and subtle depth of field, plus four complete-plant angles (P7 from the north-east, P8 from the south-east, P9 overhead, P10 from the south gate road) and P11, the modular power yard.
- **Compositor:** haze from the mist pass, fog glow, slight lens dispersion and a warm grade.

**Epic set (`--set epic`, E1–E27):** golden hour, with the sun at 11°. The shots are:
- E1: the three stacks from beside the absorbers;
- E2: a long-lens compression from the west road;
- E3: a low pass over the ACC;
- E4: along the switchyard at eye level;
- E5: looking up beneath the absorbers;
- E6: a drone dive over the power block;
- E7: into the sun, with the plant in silhouette;
- E8: the RICE hall stacks;
- E9 and E10: the water tanks and the EV carport;
- E11 to E13: the plant gas yard, the M&R station and the fuel systems from above;
- E14 and E15: the RICE exhaust trains and a simple-cycle unit;
- E16 and E17: the portable power pad, and the fuel cells and microturbines;
- E18: the process pipes crossing the east spine road;
- E19 and E20: the GSUs facing the yard, and the complete switchyard;
- E21 to E25: turbine-hall cutaways (the GTs, a GT1 close-up, the cable trays, the IPB, the gallery);
- E26 and E27: HRSG 1 from the north-west, and the HRSG roofs.

Output goes to `renders/epic/`.

`blender/finish_pro.py` adds a smooth vignette, fine grain and the burned-in credit caption. `blender/board.py` composes the presentation board: one sheet, 4800 x 3200 px plus a PDF, with a hairline key plan drawn from the verified model, the view cone of every plate, a sun-angle diagram, scale and north. The board follows the design philosophy in `renders/pro/design-philosophy.md` ("Measured Light"). Fonts are in `blender/fonts` (SIL Open Font License).

```sh
python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --samples 128 --out plant/renders/pro
python plant/blender/finish_pro.py plant/renders/pro
python plant/blender/board.py plant/renders/pro
```

## Modular expansion (design change beyond Rev 14)

Layer `OPT_MODX` adds some of the smaller modular technologies from sheets 07 and 08 beside the Rev 14 modular yard. It is a design change: none of it is on the drawing, every item is tagged `basis: design change`, and the layer can be switched off. The simple-cycle units (SC-1, SC-2) and the RICE engine hall (8 engines) stay exactly as drawn.

| Technology | Rev 14 | Added | Total |
|---|---|---|---|
| Trailer-mounted aeroderivatives (TM2500 class, ~35 MW each) | – | TM-1, TM-2 | 2 |
| Containerized gas gensets (~2 MW each) | 2 | CONT-3 to CONT-8, plus a paralleling e-house | 8 |
| Fuel-cell modules (SOFC, 200–300 kW) | 4 | FC-5 to FC-12 | 12 |
| Microturbines (1 MW) | 3 | MT-4 to MT-6 | 6 |

The north-west corner is kept open as a maintenance laydown. The plots were picked from an occupancy map of the verified model, keeping 10 ft clear of every part and route. `verify.py` still passes: 211/211 footprints, 21/21 heights, 10/10 sheet 09 clearances, 0 clashes. In the presentation renders, items the drawing marks conditional get a normal equipment finish instead of the drawing's tan tint.

## Coastal variant: LNG marine terminal (sheet 15)

Sheet SK-3X1-15 shows where a coastal plant gets its gas when there is no pipeline. The inland model stays as it is (its trucked LNG satellite from sheet 14 is unchanged). The coastal variant is a separate scene, built as an overlay on the same verified plant and rendered on its own:

| Variant | What is modelled |
|---|---|
| **A: onshore import terminal** beside the plant (EcoElectrica / AES Andres class) | 160,000 m³ full-containment tank (270 ft × 160 ft), 4 open-rack vaporizers, HP send-out pumps, BOG compressors, terminal substation, control building and fire water, send-out metering and ESD, seawater intake, flare, 1,740 ft jetty trestle on piles, berth with 4 unloading arms (3 LNG + 1 vapour), breasting and mooring dolphins, a 294 m Moss-type carrier and two tugs. LNG lines run from the tank to the jetty and the send-out pumps as drawn. The buried send-out pipeline runs to the plant's pipeline M&R. |
| **B: FSRU moored offshore** (Porto de Sergipe class) | Landfall valve station (ESD, pig receiver, metering), buried pipeline to the M&R, a soft-yoke mooring tower with its gas riser, a 170,000 m³ FSRU with a regas module on the fore deck, and an LNG carrier alongside for ship-to-ship transfer with fenders and hoses. |

- `coastal/extract_sheet15.py` reads sheet 15 (both panels draw the compound to scale, 7.61 ft per point). It matches every numbered key item to its drawn shape and writes `reference/sk3x1_rev14_sheet15.json`, which is committed.
- `coastal/build_coastal.py` writes the overlays `coastal/sk3x1_coastal_A.json` and `_B.json`. Sheet 15 draws the FSRU closer than it is ("distance NOT to scale"), so the model places it at the stated ~21,000 ft (6.4 km) pipeline length.
- `coastal/verify_coastal.py` checks the overlays. It currently passes:
  - all 15 keyed footprints are within 0.6 ft of sheet 15;
  - no clashes;
  - nothing new inside the compound;
  - vessels and all piles are in the water;
  - the carrier is 294 m LOA, with a 15 ft gap to the berth face;
  - the jetty is 1,740 ft;
  - the ship-to-ship fender gap is 50 ft;
  - the landfall to yoke run is 6.4 km.
- Renders use `--overlay` and a morning sun from the south-east, so the sea-side views are front lit. There are five views for A (C1–C5) and three for B (F1–F3). `board.py … coastal` composes the sheet 15 board.

```sh
python plant/coastal/build_coastal.py && python plant/coastal/verify_coastal.py
python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --overlay plant/coastal/sk3x1_coastal_A.json --samples 128 --out plant/renders/coastal
python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --overlay plant/coastal/sk3x1_coastal_B.json --samples 128 --out plant/renders/coastal
python plant/blender/finish_pro.py plant/renders/coastal && python plant/blender/board.py plant/renders/coastal coastal
```

Heights, pile spacing, vessel superstructure and everything marked `typical` are assumptions. Marine, siting and permitting are not addressed.

## Coordinates and sources

X east, Y north, Z up, in feet. The origin is the SW corner of the 2,420 x 1,920 ft compound.

- **Sheet 01:** the plan frame maps exactly to the compound (3.115 ft per PDF point).
- **Sheet 05:** the R1 plan is rotated, with plant north to the right (4.08 pt per ft). Its switchgear, MCC, P&C, LCI and room layout are modelled as `R1_INTERIOR`.
- **Elevations:** from sheets 09, 12 and 13. Values with no published source (cabinet heights, drum sizes, radiators, gantries, structural steel) are tagged `typical`.

## Layers

Layers follow the collections on sheet SK-3X1-11, so its view definitions map directly. For example, view B hides `R1_ROOF` and `R1_WALL_E` to show `R1_INTERIOR`.

Other collections include `BASE_POWER_BLOCK`, `HALL_ROOF`, `BASE_INLET_AIR`, `BASE_ELECTRICAL`, `R4_INTERIOR`, `BASE_SWITCHYARD`, `SWYD_FUTURE` and `HV_CORRIDOR`. Each optional system has its own layer and route layer: `OPT_CCS`, `OPT_CCSU`, `OPT_BESS`, `OPT_MOD`, `OPT_TMP`, `OPT_IC`, `OPT_LNG` and `OPT_H2`, plus the matching `*_ROUTES` layers.

## Rebuild

```sh
python3 plant/build_model.py        # model JSON
python3 plant/verify.py             # checks -> verify_report.json
python3 plant/build_viewer.py       # viewer/index.html (inlines model, palette, report)
python3 plant/export_obj.py         # OBJ (add --zup or --base as needed)
go run ./plant                      # ln line art for every view -> plant/renders/
go run ./plant -view B              # one view; -list shows the keys
# optional, needs PyMuPDF and the PDF:
python3 plant/extract_reference.py SK-3X1_Drawing_Set_Rev14.pdf
```
