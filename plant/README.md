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
| `wiring.py` | Wiring applications per item and buried feeders to every powered item. |
| `realism.py` | Firewater, small-bore piping, signage, people, vehicles, scaffolding and HRSG tube harps. |
| `switchyard.py` | Switchyard trenches, breaker and disconnect detail, line entrances, masts and fence (cycle 1). |
| `station.py` | Transformer, e-house and EDG detail; duct-bank manholes (cycle 2). |
| `acc.py` | ACC fans, drives, cable ladders, condensate drains, deck steel, vacuum pumps, dry coolers (cycle 3). |
| `placeholders.py` | Rebuilds the last single-box placeholders as equipment: kettle reboilers, reclaimer, amine skids with plate exchangers, pump sets, carbon filters, instrument air, CO2 export compressor, LNG metering and sump, H2 purification and blending, BTM tie breaker, conditional items (kept tan). |
| `ponds.py` | Stormwater detention pond works (pump station, fence, forebay berm, spillway, ramp) and the wastewater treatment process area (equalization, neutralization, clarifier, sludge, press building). |
| `datacenter.py` | BTM data-centre campus routes and dressing (design option, area L). |
| `coastal/coastal_detail.py` | Coastal terminal and landfall dressing and wiring applications (cycle 10). |
| `lng_h2.py` | LNG satellite and green hydrogen detail, H2 piping, electrolyzer cabling (cycle 9). |
| `inletchill.py` | GT inlet chilling: CW / CHW loops, chillers, tower fans, pump sets (cycle 8). |
| `bess.py` | BESS yard, container and PCS skid detail, DC trenches, 34.5 kV collector feeders (cycle 7). |
| `ccs.py` | Carbon capture flue-gas path, amine piping and rack, regeneration, CO2 header, cooling-tower fans (cycle 6). |
| `services.py` | Main gate, fence wire and CCTV, drainage, lighting handholes, admin / warehouse / workshop dressing (cycle 5). |
| `utilities.py` | Tank-farm water and aux-steam routes; fire pump house, ammonia, aux boiler, air compressor, OWS detail (cycle 4). |
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

`swgr_rooms.py` runs after `detail3.py` and fits out the switchgear rooms (R1, R4 VFD e-house): metal-clad
cubicle fronts with relays, meters, lamps and mimic bus, 480 V breaker cells, MCC buckets, P&C / DCS panels, VFD
and LCI doors, dry-type transformers, and the room itself (epoxy floor, mats, LED fixtures, HVAC, ground bus,
signage, arc-flash labels, lift truck). Cameras E82-E85.

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
  - TM-1/2 turbines (LOD 3, see DETAIL_CYCLES "TM2500 mobile turbines"): ladder chassis on crane mats, six axles with dual tyres, gooseneck on landing legs; turbine and generator enclosures with seams, doors, louvres and roof vent fans; filter house with weather hoods, ladder and handrail; rectangular raised stack with silencer; control trailer with HVAC and stair; fuel-gas skid and hose; generator terminal box with six 15 kV MV-105 leads in a ground tray (printed legends). Cameras E72, E73.
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

**Stacks and the HRSG-to-stack connection.**
- **Breeching:**
  - **Into the stack:** the outlet breeching now lofts into the stack shell. Before, its corners stood out beside the stack.
  - **Joint:** it carries an expansion joint and stiffener frames.
- **Stair box removed:** an unexplained full-height stair box beside each stack, the "weird stuff on the side" near the CEMS, is gone.
- **Each stack now has:**
  - a foundation plinth and access door;
  - a caged ladder with rest platforms to the CEMS platform (EL 100) and the top platform (EL 168);
  - platform handrails;
  - four CEMS probes with junction boxes;
  - a heated sample umbilical and analyzer cable on a small ladder tray down the stack, then supported to the CEMS shelter;
  - aviation-light conduit;
  - lightning air terminals and down conductors.
- **CCS diverter damper (optional layer):** a duct connection to the stack shell, support steel and an actuator.

**HRSG cabling and auxiliaries.**
- **Control / instrument trays:** a tray from the rack control tier runs down the east side of each HRSG to a ladder riser at the south-east corner, up to a roof junction box.
- **Drum level:** cables run along the drum frame to the drum-level bridles and transmitters.
- **Steam leads:** motor-operated stop valves on the leads.
- **Chemical feed:** a skid per HRSG (phosphate / amine) beside the boiler feed pumps.
- **Wiring applications:** these feed the new items, and every item still has a cable reaching it.

New epic cameras:
- E26: HRSG 1 and its stack from the north-west;
- E27: the HRSG roofs;
- E28: the stack, breeching and CEMS.

## Wiring applications

`wiring.py` gives every powered or instrumented item its cable applications (`wiring` in the model). The viewer's inspector lists them when you click the item. The selection is typical, not engineered; Southwire families are named as the requested supplier. Items the generic rules miss (HRSGs, ACC, heat-trace panels, aux boiler, M&R, temporary-power cabinets and others) get their applications from `wiring.OVERRIDES`, applied last.

| Equipment class | Applications |
|---|---|
| Transformers (GSU, UAT, station, rectifier, collector) | MV power, control / marshalling, instrumentation (temperature, gas, level), grounding |
| Switchgear, e-houses, MCCs, PCMs, control cubicles | MV and LV power, control, data / fibre, fire alarm, lighting, grounding |
| MV motors (boiler feed pumps, CO2 compression, CW pumps, fuel-gas and BOG compressors) | MV power, control, instrumentation, grounding |
| Generating units (gensets, RICE, aero units, microturbines, fuel cells, BESS) | MV power out, LV auxiliaries, control, instrumentation, type KX thermocouples, data, fire alarm, grounding |
| Analyzers, CEMS, SWAS, metering | LV power, instrumentation, data, lighting, grounding |
| Buildings and shelters | LV power, control, lighting (THHN in conduit), fire alarm, data, grounding |
| Tanks, sumps, separators | LV power, instrumentation (level), heat tracing, grounding |
| Pumps, fans, coolers, skids, heaters, valves, process vessels | LV power, control, instrumentation, grounding |

**Gas areas.** Items in Class I Div 2 areas use ARMOR-X MC-HL power cable and intrinsically safe instrumentation (Type ITC / PLTC, blue jacket). These areas are the gas yard, M&R, fuel-gas compressors, gas conditioning, LNG, H2, the gensets and the ULSD area.

**Feeders.** The check first found about 100 such items that no cable route reached, for example the CEMS shelters, gas yard skids, fire pump house, tanks, chillers, CCS pumps, BESS e-houses and gensets.
- **Buried feeders:** each now gets an L-shaped buried feeder from its nearest edge to the nearest point of the underground cable network, preferring its own system's route layer. That adds 101 feeders, averaging about 70 ft and at most 355 ft.
- **Inside R1:** items are fed through the cable basement.
- **Bridge crane:** fed from its conductor bar.

The gas / steam turbine audit (`hall.gt_st_audit()`) added the GT static starters (SFC-1..3), the generator seal-oil / H2 gas-control skids (SOS-1..3), compressor bleed lines, ST combined reheat and LP admission valves, turning gear, the EHC power unit (EHC-ST), the gland-steam condenser (GSC-ST) and two deck stairs; cameras E51-E53.

Underground systems (`underground.py`): duct banks with red-dyed caps and manhole chambers, the station ground grid, the firewater main, storm / oily-water / sanitary drains and the water mains are modelled below grade in the `UNDERGROUND` and `OPT_UNDERGROUND` layers; the viewer's "U Underground" view removes the ground to show them. Buried routes are no longer painted on grade.

`audit.py` now checks that every item with wiring applications has a cable route ending at it or passing it.

## Detail cycles

The model is improved zone by zone, one cycle per zone (`DETAIL_CYCLES.md` has the plan and what each cycle changed). Each cycle runs the same steps:
1. audit the zone's wiring and connections;
2. detail the equipment, buildings, piping and cable runs;
3. add realism;
4. run every check;
5. render close-ups;
6. re-export and republish.

**Cycle 10: coastal variant (`coastal/coastal_detail.py`).**
- **Wiring:** every keyed terminal item (tank, vaporizers, HP pumps, BOG, substation, control building, metering, intake, flare, jetty, berth) and the landfall valve station now carry their cable applications (MV-105, ARMOR-X MC-HL in the hazardous areas, IS instrumentation, thermocouple extension, fibre ship-shore link, fire and gas, grounding).
- **LNG tank:** water-curtain / deluge rings with risers, roof-platform handrail, level and temperature gauge housings, ID band, gas detectors round the tank.
- **HP pumps:** suction and discharge headers with drops, junction boxes, gas detectors.
- **BOG building, substation, control building:** louvres, roll-up door and roof vents; e-house doors, landings and HVAC; entrance canopy, door, rooftop HVAC and antenna mast.
- **Seawater intake:** travelling screens and trash-rake rail.
- **Jetty and berth:** fire-water main, life-ring stands, signs; emergency-release couplers on the unloading arms, ESD stations, crew on the berth.
- **Landfall valve station (B):** ESD actuators, CP rectifier, SCADA dish, a pickup and an operator.
- **Realism:** pickups on the terminal roads, staff at the control building and BOG house.
- **Cameras:** C6 and C7.

**Cycle 9: LNG satellite and green hydrogen (`lng_h2.py`).**
- **LNG tanks:** dished heads, valve / instrument cabinets with frosted fill and withdrawal lines into a liquid header, PSVs with a vent header, level gauges, ID plates.
- **Unloading:** two articulated loading arms over the truck bays with counterweights, hose rack, ESD button; an LNG trailer at bay 2.
- **Vaporizers:** rebuilt as ambient finned columns (star fins, frosted) with inlet / outlet manifolds and the glycol trim heater.
- **Send-out pumps and BOG compressor:** pump pots with heads and spools; compressor, motor and knock-out drum on a skid.
- **Impoundment:** hi-ex foam generator, gas detectors, hazard signs.
- **Hydrogen:** electrolyzer-building ridge vents, louvres, gas detectors, signs, roll-up door; twin-tower dryer with regeneration heater; compressor container doors, roof coolers and vents; tube-bank end frames, manifolds and valves.
- **Routes and wiring:** H2 piping building → dryer → compressors → tube banks; floor-trench cables from each rectifier transformer to its rectifier and DC bus to its electrolyzer (electrolyzers and rectifiers had no cable routes or applications).
- **Cameras:** E45 and E46.

**Cycle 8: GT inlet chilling (`inletchill.py`).**
- **Loops closed:** condenser water from the tower basin to the CW pumps, into the chillers and back up to the tower; chilled water from the chillers to the CHW pumps and the TES tank (new `cw` / `chw` routes, drawn as round pipe).
- **Chiller building:** six chiller packages (evaporator, condenser, compressor, motor, starter), relief vent stacks, roof exhaust fans, wall louvres, roll-up door.
- **Chiller tower (12 cells):** open fan stacks with visible blades and hubs, gearboxes, shafts and motors, partition walls, intake louvres, deck handrail, access stair, hot-water riser and header. The CCS tower's fan stacks get the same open look.
- **Pumps:** the CW and CHW pump blocks are replaced by pump sets on plinths (pump, coupling guard, motor, spools).
- **E-house:** landings, stairs, doors, HVAC.
- **Wiring:** the chiller tower had no cable applications (the name matched a skip rule); added, with a fan-cable route from the e-house round the tower.
- **Cameras:** E43 and E44.

**Cycle 7: battery energy storage (`bess.py`).**
- **Yard:** crushed-stone surface, its own security fence with an open double gate on the west, NFPA 855 hazard signs, aisle lighting.
- **Containers (30):** six battery-rack doors on the north face, roof deflagration vents, a gas-detection exhaust fan, strobe / horn, suppression release and E-stop panel, ground leads.
- **PCS / MV skids (15):** inverter cabinet with cooling grilles and roof fans on its own pad beside the step-up transformer, LV bus link, DC combiner, ground leads, and a precast DC trench to the two containers it serves.
- **Collector:** three buried 34.5 kV feeders, one per skid column, up the aisles to the collector e-house, and the e-house to the main power transformer.
- **Collector e-house and EMS:** landings, stairs and doors, HVAC, bottom cable entries.
- **Wiring:** containers carry 1,500 V DC, auxiliary 480 V, BMS data, fire alarm / gas detection and grounding; skids carry 34.5 kV MV-105 collector cable, DC, control and fibre.
- **Realism:** technicians and a pickup in an aisle.
- **Cameras:** E41 and E42.

**Absorber and stripper access.** Caged ladders (yellow) on each column reach the platform rings; walkways link the stripper platforms. (Stair towers with lifts were tried and taken out: they duplicated the ladders and crowded the columns.)

**Turbine hall electrical audit (`hall.py`, `hall_electrical`).** Every machine in the hall now carries its cable applications (GTs, generators, ST, ST aux, GCBs, turbine control panels, the crane and the hall itself had none; ducts, spools and the deck are passive). Inside: lighting / small-power and fire-alarm panels on the north wall with conduit to the LV tray, receptacles and welding outlets along the deck, horn / strobes, exit signs, a fused disconnect feeding the crane conductor bar, fire-stopped sleeves where the trays cross the north wall. Outside: MC-cable (ARMOR-X) ladder risers on the east and west walls from duct-bank riser boxes to the roof, roof trays both sides of the ridge feeding 24 roof exhausters, LED wall packs with conduit and pull boxes, weatherproof receptacles and beacons at the doors, air terminals on the ridge and down conductors to ground rods.

**Air inlet electrical audit (`hall.py`, `inlet_electrical`).** The filter houses carried generic building cable applications and the stair towers pump-type ones; the inlet ducts had none. Now: filter houses list hoist / heater power, pulse-jet control, stage-DP and icing instrumentation, ARMOR-X branches, lighting and frame grounding; stairs list lighting; inlet ducts list T / RH / DP and bleed-heat thermocouples. The control riser to each filter platform now lands in a riser box and a buried duct bank to the unit duct bank (it rose from bare ground). Added per filter house: pulse-jet air receiver, header and solenoid-valve manifolds, instrument-air riser, DP transmitters and the sequencer / JB panel, anti-icing manifold across the weather hoods with its supply riser and valve, platform lighting on conduit and a receptacle, the electric chain hoist with pendant, a tray under the platform, stair landing lights, frame grounding, and inlet-duct T / RH / DP instruments with conduit to the gallery control tray.

**Cycle 6: carbon capture (`ccs.py`).**
- **Flue-gas path closed:** the HRSG flue duct turns into the DCC, the DCC outlet feeds the booster fan, and the fan discharges into an overhead duct on steel bents to the absorber inlet, with an expansion joint.
- **DCC:** quench-water riser and return, platform, caged ladder.
- **Absorbers:** lean-amine riser to the upper bed, water-wash riser, rich-amine bottoms line to the pump skid, sample / analyser panel.
- **CCS pipe rack:** two tiers along y 1115-1135 carrying rich and lean amine, LP steam, condensate and cooling water, with risers from each pump skid.
- **Regeneration:** stripper overhead lines down the shell on guides to a CO2 product header into the compression building; reboiler vapour return and feed lines; a reflux drum per stripper; intercooler fin-fan banks and louvres at the compressor building.
- **Cooling tower:** 30 fans with blades, hubs, gearboxes, shafts and motors; deck handrail; access stair; intake louvres; hot-water header with a riser per cell.
- **Wiring:** CCS T-1 / T-2, F&G / control, instrument air, reclaimer, solvent storage, dampers and the cooling tower now carry cable applications; new 13.8 kV routes from the transformers into the CCS MV building, from it to the cooling-tower MCC, and fan cables along the tower.
- **Cameras:** E39 and E40.

**Cycle 5: controls and services (`services.py`).**
- **Main gate:** sliding gate parked open, inbound and outbound barrier arms, card readers, speed table, entrance sign; a buried duct bank from the gatehouse feeds the gate, and another feeds the gatehouse from the control / admin building.
- **Perimeter security:** barbed-wire arms with three strands on every fence post, and nine CCTV poles (corners, gate, access road).
- **Drainage:** catch basins along every road about every 150 ft, and the stormwater basin's inlet headwall with riprap and its outlet riser.
- **Site lighting:** a handhole and a photocell box at every pole; wiring for the pole circuits, CCTV and access control.
- **Buildings:** a SCADA / radio mast with antennas and a dish on the control room, flagpoles, bike rack, bollards; a paved service yard round the warehouse and workshop, with roll-up and personnel doors, dumpsters, a gas-cylinder cage and stock racks; wheel stops in the parking bays.
- **Wiring:** the gatehouse, the comms tower and the EDGs now carry their cable applications.
- **Realism:** a guard at the gate, a pickup at the barrier, a delivery flatbed at the warehouse, workers in the workshop yard.
- **Cameras:** E37 and E38.

**Cycle 4: water and BOP utilities (`utilities.py`).**
- **Pipe routes:** water headers from the tank farm to water treatment and the fire pump house, and insulated auxiliary steam to the rack.
- **Fire pump house:** diesel stack, test header with hose valves, jockey-pump controller.
- **Ammonia storage:** bund, scrubber, safety shower, wind sock.
- **Aux boiler:** burner, FD fan, economizer, feed pumps.
- **Air compressors:** receivers and a dryer.
- **Oil-water separator:** detail.
- **Cameras:** E35 and E36.

**Cycle 3: air-cooled condenser (`acc.py`).**
- **Each of the 80 cells:** inlet bell, 9-blade fan, gearbox and motor on a fan bridge, vibration switch, cable drop.
- **Cabling and drains:** fan-bridge cable ladders per street fed from R4, and condensate drain headers along every A-frame.
- **Structure:** deck girders, X-bracing and a deck handrail.
- **Auxiliaries:** vacuum-pump skids, and aux dry-cooler fans with their headers.
- **Camera:** E34.

**Cycle 2: station electrical (`station.py`).**
- **Auxiliary and station transformers:** MV air terminal chambers, LV cable boxes, marshalling cabinets, nameplates and hazard signs, ground leads.
- **E-houses:** door landings and stairs, emergency lights, extinguisher cabinets, bottom cable-entry transits, rooftop HVAC.
- **EDGs:** weatherproof enclosures with radiator, silencer and stack, day tank and output breaker.
- **Duct-bank network:** manholes at bends and every ~300 ft, and handholes at feeder ends.
- **Cameras:** E32 and E33.

**Cycle 1: switchyard (`switchyard.py`).**
- **Cable trenches:** precast trenches with covers run from the relay house along the yard and down every diameter; the breakers' control cabling runs in them.
- **Breakers:** operating-mechanism cabinets, bushing CTs and ground leads.
- **Disconnect switches:** centre-break blades and motor operators.
- **Line entrances:** arresters, CCVTs and line traps.
- **Yard:** lighting masts, and a fence with a gate at the relay house.
- **Camera:** E31.

## Realism pass

`realism.py` runs last, so every placement is tested against the finished geometry. Anything that would pass through something is skipped. Everything here is typical, not engineered.

- **Firewater:**
  - **Mains:** a buried ring main round the power block, with branches to the BOP / gas / modular areas and the switchyard side, and a feed from the fire pump house.
  - **Hydrants:** 44, about every 200 ft.
  - **Valves and stations:** post-indicator valves at the loop corners, a GSU water-spray deluge valve station by each GSU, and fixed monitors at the GSUs and the gas yard.
- **Small-bore piping:**
  - **Rack lines:** instrument-air, service-water and nitrogen headers on the rack tiers, broken where a tray drop crosses the tier.
  - **HRSG drains:** drain headers to the blowdown tanks.
- **Pipe markers:** in the ASME A13.1 style, a white legend band between two service-colour bands every 60 ft on every round pipe.
- **Signage:** equipment ID signs on buildings and e-houses, and hazard signs on transformers (48).
- **Weathering:** every painted, clad, galvanised and concrete surface gets grime in the splash zone near grade, faint vertical rain streaks, and light rust bloom on bare and galvanised steel. It is all done in the shaders, by world position, so it changes nothing in the model.
- **Scale:**
  - **People:** 33 people in hard hats and hi-vis, at work positions at grade, on the turbine deck, on the HRSG platforms, on the CEMS platform, in the gas yard and in the switchyard.
  - **Vehicles:** pickups, a flatbed at the laydown bay, a forklift and a mobile crane.
  - **Scaffolding:** on an HRSG wall.
- **HRSG 3 tube harps:** finned-tube harps with upper and lower headers and hanger rods, in gas-flow order, plus the SCR / CO catalyst blocks, for the cutaway camera E29.
- **New cameras:** E29 (the cutaway, with a per-camera sun override, since HRSG 2 shades it at golden hour) and E30 (the access road by the hall: crews, pickups, hydrants, the deluge stations).

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

**Epic set (`--set epic`, E1–E50):** golden hour, with the sun at 11°. The shots are:
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
- E26 to E28: HRSG 1 from the north-west, the HRSG roofs, and the stack with its breeching and CEMS;
- E29 and E30: the HRSG 3 tube-harp cutaway, and the access road by the hall;
- E31: switchyard bay D2;
- E32 and E33: an R2 e-house, and the emergency diesels;
- E34: the ACC's south-east corner;
- E35 and E36: the tank farm, and the ammonia storage with the aux boiler.
- E37 and E38: the main gate with the gatehouse and control building, and the warehouse / workshop yard.
- E39 and E40: carbon-capture train A (DCC, booster fan, duct, absorber, rack), and the regenerators.
- E41 and E42: a BESS aisle, and the collector e-house with the main power transformer.
- E43 and E44: the GT inlet-chilling plant, and its cooling tower.
- E45 and E46: the LNG satellite, and the green-hydrogen plant.
- E47 and E48: the BTM data-centre campus, and its BTM substation.
- E49 and E50: the stormwater detention pond, and the wastewater treatment area.

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

## BTM data centre (design option, area L)

A ~150 MW data-centre campus outside the east fence, beside the modular yard, supplied behind the meter (`datacenter.py`, layers `OPT_DC` / `OPT_DC_ROUTES`). It is a design option beyond Rev 14, typical and not engineered, and it is an **add-on**: the plant views, renders and exports show the plant alone, and the campus appears only when it is added:
- **Viewer:** "Complete plant" and every other view leave it off; the view **"Add-on: plant + BTM data centre"** (O6) turns it on, or tick its layers.
- **Blender:** the plant cameras leave it out; the cameras E47 and E48 (`show="dc"`) include it.
- **Everything:** the viewer view "Everything: plant + all LNG + BTM data centre", the camera C8 (`show="everything"`) and the export `SK-3X1_everything_datacenter` show the plant with the LNG satellite, the coastal LNG terminal and the data centre together.
- **Exports:** `SK-3X1_plant` and `SK-3X1_coastal_A` are plant only; `SK-3X1_plant_datacenter.glb / .usdz / .blend` is the plant plus the campus (`export_model.py plant/model SK-3X1_plant_datacenter SK-3X1_plant`).

| Part | What is modelled |
|---|---|
| Campus | 920 × 1,080 ft (x 2,460–3,380, y 300–1,380): crushed stone, internal 30 ft roads, security fence, entrance from the south with gatehouse, admin / security / NOC building with diverse fibre entries |
| Data halls A and B | 560 × 260 ft, 45 ft, ~60 MW IT each, liquid-cooled racks on a closed loop; rooftop dry-cooler banks with fans and headers; west gallery for MV/LV distribution, controls and cooling pumps; east loading docks |
| Hall power, 2N | Each hall has an A side (north face, bus A) and a B side (south face, bus B). Per side: 24 two-tier power skids against the wall (UPS modules, Li-ion battery, LV switchboard; ~22,000 sq ft per side), then 24 × 3.5 MVA 34.5/0.48 kV pad-mount transformers (84 MVA, so one side carries the whole hall), each bus-ducted into its skid; the 24 transformers hang on four 34.5 kV feeder loops of six, in one duct bank along the row |
| BTM substation | BTM-T1 / T2 / T3 13.8/34.5 kV step-ups (3 × 90 MVA, N+1 on the ~150 MW campus) fed from the modular yard's 13.8 kV collector (MOD-EH) by cable bus; BTM-TIE 230/34.5 kV (180 MVA, carries the full campus) with a normally-open 230 kV tie breaker; 34.5 kV double-bus switchgear (bus A: T1 + GSU-1; bus B: T2 + GSU-2; T3, the tie and the BESS on the bus-tie section) with the transfer scheme and sync check; a zigzag grounding transformer on each bus |
| BTM BESS | 40 MW / 80 MWh, 15 containers and 5 PCS / MV skids: absorbs AI training load steps so the engines follow slowly, bridges genset starts and mode transfers |
| Backup generation | 36 × 3.6 MW diesel gensets at 13.8 kV (130 MW: the IT load plus the critical cooling pumps), 48 h belly tanks, in three rows; collectors to the 13.8 kV paralleling switchgear, then two 75 MVA GSUs onto bus A and bus B |

**Simplification to know:** the 13.8 kV link from MOD-EH to the step-ups (about 550 ft, ~150 MW) would in practice be a cable bus with many parallel sets per phase, or the step-ups would sit in the modular yard.

**Supply paths.** The equipment keeps its real finishes (grey transformers, white battery containers, genset enclosures). The paths are shown on demand instead: the viewer's **BTM power paths** button tints the three paths and labels them, and the data-centre renders carry numbered callouts. The paths are tagged in the model (`path` on items and routes):
1. **Islanded BTM power:** campus gensets with their paralleling switchgear and step-up, the BTM battery, the 34.5 kV switchgear and the hall feeders.
2. **Supply from the modular yard:** BTM-T1 / T2 and the 13.8 kV cables from the modular collector (MOD-EH).
3. **230 kV grid tie:** BTM-TIE, the normally-open tie breaker and the 230 kV cable from D6.

**Three operating modes, selected by breakers at the BTM switchgear:**
1. **Islanded:** T1 / T2 mains closed, 230 kV tie open. The modular yard supplies the campus: eight RICE engines, two aeroderivative SC units, fuel cells and microturbines, with the portable pad as a temporary source. The BTM BESS takes the load steps.
2. **Islanded with backup:** the 230 kV tie from the plant switchyard (D6 bay) closes on loss of the modular supply (open transition) or for maintenance.
3. **Grid-parallel co-location:** the tie is closed with sync check; the modular yard and the BESS firm the load. This mode carries the most regulatory exposure (co-location at grid-connected plants is under scrutiny), which the islanded modes avoid.

**Routes (buried):** MOD-EH to T1 / T2; the 230 kV tie from D6, outside the east fence, to BTM-TIE; step-ups and tie to the switchgear; switchgear to a 34.5 kV ring through each hall gallery; BESS, genset bus and genset collectors to the switchgear; LV to the admin building and gate. Every campus item carries its cable applications (wiring audit clean, no new feeders needed), and `verify.py` allows the campus east of the compound.
**Cameras:** E47 (campus) and E48 (BTM substation).

## Coastal variant: LNG marine terminal (sheet 15)

Sheet SK-3X1-15 shows where a coastal plant gets its gas when there is no pipeline. The inland model stays as it is (its trucked LNG satellite from sheet 14 is unchanged). The coastal variant is a separate scene, built as an overlay on the same verified plant and rendered on its own:

| Variant | What is modelled |
|---|---|
| **A: onshore import terminal** beside the plant (EcoElectrica / AES Andres class) | 160,000 m³ full-containment tank (270 ft × 160 ft), 4 open-rack vaporizers, HP send-out pumps, BOG compressors, terminal substation, control building and fire water, send-out metering and ESD, seawater intake, flare, 1,740 ft jetty trestle on piles, berth with 4 unloading arms (3 LNG + 1 vapour), breasting and mooring dolphins, a 294 m Moss-type carrier and two tugs. LNG lines run from the tank to the jetty and the send-out pumps as drawn. The buried send-out pipeline runs to the plant's pipeline M&R. |
| **B: FSRU moored offshore** (Porto de Sergipe class) | Landfall valve station (ESD, pig receiver, metering), buried pipeline to the M&R, a soft-yoke mooring tower with its gas riser, a 170,000 m³ FSRU with a regas module on the fore deck, and an LNG carrier alongside for ship-to-ship transfer with fenders and hoses. |

**Placement: north of the plant.** Sheet 15 draws the terminal east of the plant with the sea further east. The model places it north of the plant instead: the coast runs east-west about 1,180 ft north of the north fence, and the jetty runs north to the berth. Every sheet-15 shape is built in the sheet frame and rotated 90° counter-clockwise onto the site (x' = 2,470 − y, y' = x − 500). The terminal plot sits at x 790–2,210, y 1,980–3,060, centred on the north fence. The links into the plant are built directly in the site frame:
- **Access road:** from the plant's fuel road (y 1,650–1,675) north along x 1,470–1,500, through a new 40 ft north gate in the perimeter fence, to the terminal's south road.
- **Send-out pipeline:** buried, from the send-out metering south to the pig-receiver end of the plant's pipeline M&R station.
- **Terminal power:** the buried 230 kV cable from the east end of the switchyard runs outside the east fence and north to the terminal substation.
- **Variant B:** the landfall valve station sits north of the plant, the buried pipeline runs to the same M&R end, and the FSRU and carrier lie about 21,000 ft (6.4 km) offshore to the north.

- `coastal/extract_sheet15.py` reads sheet 15 (both panels draw the compound to scale, 7.61 ft per point). It matches every numbered key item to its drawn shape and writes `reference/sk3x1_rev14_sheet15.json`, which is committed.
- `coastal/build_coastal.py` writes the overlays `coastal/sk3x1_coastal_A.json` and `_B.json`. Sheet 15 draws the FSRU closer than it is ("distance NOT to scale"), so the model places it at the stated ~21,000 ft (6.4 km) pipeline length.
- `coastal/verify_coastal.py` checks the overlays. It currently passes:
  - all 15 keyed footprints are within 0.6 ft of sheet 15;
  - no clashes;
  - nothing new inside the compound except the three links, which are buried rights of way or the link road;
  - the link road clears every plant item above grade, and the fence is open at the north gate;
  - the send-out pipeline (and B's pipeline) reach the M&R station; the 230 kV cable leaves the switchyard and runs outside the east fence;
  - the shoreline is north of every land item;
  - every keyed terminal item has its cable applications;
  - vessels and all piles are in the water;
  - the carrier is 294 m LOA, with a 15 ft gap to the berth face;
  - the jetty is 1,740 ft;
  - the ship-to-ship fender gap is 50 ft;
  - the landfall to yoke run is 6.4 km.
- Renders use `--overlay` and a morning sun from the south-east. The sheet-15 cameras are rotated onto the site with the layout; C4 is framed north-up in the site frame. There are eight views for A (C1–C8; C8 shows everything, with the data centre) and three for B (F1–F3). `board.py … coastal` composes the sheet 15 board.

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
