# Detail cycles

One zone per cycle. Each cycle:
1. **Audit:** every powered item in the zone has the right cable applications and a route reaching it; trays, pipes and supports are clash-free.
2. **Detail:** equipment, buildings, piping and cable runs to LOD 3 with realistic proportions, inside the drawn footprints and sheet-13 heights.
3. **Realism:** signage and scale figures where they fit.
4. **Checks:** verify.py, audit.py and the coastal checks clean.
5. **Renders:** 1-2 close-up epic views of the zone.
6. **Publish:** re-export the 3D models, republish the viewer, commit and push.

| # | Zone | Status | What changed |
|---|---|---|---|
| 1 | C Switchyard (230 kV breaker-and-a-half, line exits, relay house) | done | Precast control-cable trenches from the relay house down every diameter; breaker operating mechanisms, bushing CTs, ground leads; disconnect blades and motor operators; line-entrance arresters, CCVTs and line traps; lighting masts and fence with gate. The wiring check now counts routes that pass an item, not only route ends, which removed 19 redundant feeders. Camera E31. |
| 2 | Station electrical: R1-R4 e-houses, station / load-centre transformers, EDGs, duct-bank manholes | done | Auxiliary / station transformers: MV air terminal chambers with bushings, LV cable boxes and conduit, marshalling cabinets, nameplates and hazard signs, ground leads. E-houses R2A-C, R3, R4: lifting lugs, door landings and stairs, emergency lights, extinguisher cabinets, bottom cable-entry transits with cables, rooftop HVAC condensers, ground leads. EDG-1/2: weatherproof enclosures with radiator, silencer and stack, sub-base day tank, fuel fill, output breaker. Duct-bank manholes at bends and every ~300 ft, handholes at feeder ends. Cameras E32, E33. |
| 3 | B Air-cooled condenser: fans, motors and gearboxes, steam ducts, condensate tank, vacuum pumps, VFD cabling | done | Per cell: inlet bell under the deck, 9-blade fan with hub and shaft, right-angle gearbox and motor on a fan bridge, vibration switch, motor cable drop. Fan-bridge cable ladders, one per street, fed from R4 by a riser at the south-west corner and a header ladder along the south edge. Condensate drain headers along both edges of every A-frame to a north collector. Deck girders, X-bracing in end bays clear of the LV tray, fan-deck handrail. Vacuum-pump skids (liquid-ring pumps, motors, separators); aux dry-cooler fans and CCW headers. Camera E34 (south-east corner). An under-deck view was tried and dropped: the underside is in shade under any sun. |
| 4 | E Water and BOP utilities: tanks, water treatment, fire pump house, aux boiler, air compressors, aux coolers | done | New pipe routes: raw / demin water header from the tanks into water treatment, fire / service water round the tank farm to the fire pump house, insulated auxiliary steam from the aux boiler to the main rack (new route types `water` and `aux_steam`, on sleepers, sleeved under roads). Fire pump house: diesel exhaust stack and silencer, louvres, test header with hose valves, jockey-pump controller. Ammonia storage: bund walls, unloading connection, vapour scrubber, safety shower, wind sock. Aux boiler: burner front and windbox, FD fan and inlet silencer, economizer, feedwater pump skid. Air compressors: two receivers and a desiccant dryer. Oil-water separator: hatches, inlet, skimmer. Cameras E35, E36. |
| 5 | F Controls and services: control / admin, warehouse, workshop, gatehouse, parking, site lighting, fence, drainage | done | Main gate: sliding gate, barrier arms, card readers, speed table, entrance sign, with buried duct banks gatehouse-to-gate and control-building-to-gatehouse. Perimeter fence: barbed-wire arms and strands, nine CCTV poles. Drainage: catch basins along the roads, stormwater-basin inlet headwall with riprap and outlet riser. Lighting: handholes and photocells at every pole. Control building: SCADA / radio mast and dish, flagpoles, bike rack, bollards. Warehouse / workshop: paved service yard, roll-up and personnel doors, dumpsters, gas-cylinder cage, stock racks. Parking wheel stops. Wiring audit: the gatehouse, comms tower and EDGs gained cable applications (EDGs had none); gate, CCTV and site lighting carry theirs. Guard, pickup at the barrier, delivery flatbed. Cameras E37, E38. |
| 6 | G Carbon capture: absorbers, strippers, DCCs, CO2 compression, cooling tower | done | Flue-gas path closed per train: duct elbow into the DCC, DCC outlet to the booster fan, fan discharge into an overhead duct on bents to the absorber. DCC quench riser, platform, ladder. Absorber lean-amine and water-wash risers, rich-amine bottoms, sample panel. Two-tier CCS pipe rack with skid risers. Stripper overheads to a CO2 product header into compression; reboiler vapour return / feed; reflux drums; compressor fin-fan coolers and louvres. Cooling tower: fans with blades, gearboxes, motors, handrail, stair, louvres, hot-water header and risers. Wiring audit: CCS T-1/T-2, F&G, instrument air, reclaimer, solvent storage, dampers and the cooling tower had no cable applications; added, with routes T-1/T-2 to the MV building, MV building to the CT MCC, and fan cables along the tower. Cameras E39, E40. |
| 7 | H BESS: containers, PCS / MV skids, collector e-house, MPT | done | Yard surfacing, own fence with double gate, NFPA 855 signs, aisle lighting. Containers: rack doors, deflagration vents, gas-detection fan, strobe, suppression / E-stop panel, ground leads. PCS / MV skids: inverter cabinet with grilles and roof fans, LV link, DC combiner, precast DC trench to its two containers. Wiring audit: the 34.5 kV collector had no cable from the skids; added three buried feeders up the aisles to the collector e-house, and e-house to MPT; containers and skids now list their DC, MV, auxiliary, BMS, fire-alarm and grounding cables. Collector e-house / EMS stairs, HVAC, cable entries. Technicians and a pickup. Cameras E41, E42. |
| 8 | J GT inlet chilling: chillers, cooling tower, pumps, TES | done | CW loop closed (tower basin to CW pumps to chillers and back up to the tower) and CHW from the chillers to the CHW pumps and TES tank. Six chiller packages, relief vents, roof fans, louvres, roll-up door. Tower: open fan stacks with visible blades, gearboxes, shafts, motors, partitions, louvres, handrail, stair, hot-water riser and header (CCS tower stacks opened the same way). Pump blocks replaced by pump sets on plinths. E-house stairs and HVAC. Wiring audit: the chiller tower had no cable applications (skip rule); fixed, with a fan-cable route from the e-house. Cameras E43, E44. |
| 9 | K LNG satellite and green hydrogen | done | LNG tanks: heads, valve cabinets, frosted liquid lines and header, PSVs and vent header, level gauges, ID plates. Unloading arms, hose rack, ESD; trailer at bay 2. Vaporizers rebuilt as finned ambient columns with manifolds. Send-out pump pots, BOG compressor skid with knock-out drum. Impoundment foam generator, gas detectors, signs. H2: building ridge vents, louvres, detectors; twin-tower dryer; compressor doors and roof coolers; tube-bank manifolds and valves. Wiring / routes audit: the five electrolyzers and rectifiers had neither cable routes nor applications; added floor-trench MV and DC routes and their applications; H2 piping building → dryer → compressors → tube banks. Cameras E45, E46. |
| 10 | Coastal variant: LNG terminal, jetty, berth | done | Wiring audit: none of the coastal items carried cable applications; all keyed terminal items and the landfall station now do. Tank deluge / water-curtain rings and risers, roof handrail, gauges, ID band, gas detectors. HP pump suction / discharge headers, junction boxes. BOG louvres, door, roof vents; substation e-house doors, landings, HVAC; control-building canopy, HVAC, mast. Intake travelling screens. Jetty fire-water main, life rings, signs; berth ERS couplers, ESD stations, crew. Landfall station ESD actuators, CP rectifier, SCADA dish. Pickups and staff. Cameras C6, C7. |

## After the cycles

- **Coastal terminal moved north of the plant.** The LNG terminal, jetty, berth and carrier (A) and the landfall station and FSRU (B) were moved from east of the plant to north of it, with the coast running east-west. The sheet-15 layout is rotated 90° onto the site so every keyed shape still matches sheet 15. Links rebuilt in the site frame: a link road through a new north gate in the plant fence, the send-out pipeline to the M&R, and the 230 kV cable outside the east fence. `verify_coastal.py` gained site checks (nothing inside the compound but the links, link road clear of plant equipment, gate open, pipelines reach the M&R, cable route, shoreline north of the land, wiring on every keyed item).
- **BTM data centre added (design option, area L).** ~150 MW campus outside the east fence beside the modular yard: two data halls, BTM substation (13.8/34.5 kV step-ups from MOD-EH, 230/34.5 kV tie with a normally-open breaker to the D6 bay, 34.5 kV main-tie-main switchgear supporting islanded, islanded-with-backup and grid-parallel modes), 40 MW / 80 MWh BTM BESS, 24 × 2.5 MW backup gensets, cable routes and wiring applications on every item. Cameras E47, E48; viewer view O6.
- **Placeholder sweep.** Every remaining single-box placeholder was rebuilt as equipment (`placeholders.py`): CCS reboilers (kettles on a table with LP steam header), reclaimer, rich / lean skids (pumps, plate cross exchangers, lean cooler), quench and wash pump sets, carbon filters, instrument air, CW pumps, CO2 export compressor; LNG send-out metering and sump pump; H2 water purification and blending skid; BTM tie breaker and BESS containers; conditional items (grounding transformer, SC inlet chillers, BESS black-start) keep their tan tint but get shape.
- **BTM data-centre electrical corrected.** Review found: 8 unit substations per 60 MW hall (~7.5 MVA at 480 V, not buildable), a single feeder per hall (no redundancy), 60 MW of backup for a ~145 MW campus, the genset bus cabled into the 34.5 kV switchgear past its GSU, and a 100 MVA grid tie. Now: 2N halls (A side / B side, 20 × 3.5 MVA pad-mounts per side with bus ducts, one looped feeder per side), double-bus 34.5 kV switchgear (A / B), 36 × 3.25 MW gensets → 13.8 kV paralleling gear → two GSUs onto bus A and bus B, 180 MVA grid tie.
- **BTM electrical, second pass.** Four 34.5 kV feeder loops of six transformers per hall side (was one loop of 20, ~1.2 kA); third 90 MVA step-up for N+1 on the modular supply; 24 × 3.5 MVA per side (84 MVA, carries the whole hall in 2N); two-tier power skids for UPS, batteries and LV switchboards along both long faces of each hall (halls 260 ft deep to fit them); backup 36 × 3.6 MW (130 MW); zigzag grounding transformers on both 34.5 kV buses; LV routes from the skids into the halls.
- **Stormwater pond and wastewater treatment.** The detention basin was a solid slab flush with grade (and the surround grass plane covered it); it is now a depression: grass banks, floor at EL -8, permanent pool at EL -5, forebay rock berm, spillway, access ramp, safety fence, depth gauge, life ring, and a stormwater pump station (pump house, wet well, discharge to the outfall at the west fence). The wastewater treatment block is now a process area: equalization basin with mixers, two neutralization tanks, a circular clarifier with bridge and launder, sludge tank, press / chemical building and process piping. The viewer and Blender grass planes no longer run under the compound. Cameras E49, E50.
- **Plant-wide wiring audit.** After the turbine hall and air inlet passes, a scan of the register found items without cable applications: HRSG 1-3 + SCR, ACC, the HTP-2 / HTP-4 heat-trace panels, chemical feed, wastewater treatment, auxiliary boiler, gas-yard control enclosure, the conditional ULSD unloading / forwarding, M&R 1 pig receiver and M&R 5 meters, switchyard ground grid and lighting, aqueous ammonia, GSP-1/2, PIC, the load bank and the H2 N2 purge supply. `wiring.OVERRIDES` now gives each its applications (MV / LV / control / instrumentation / IS / thermocouple / heat trace / lighting / grounding); two had no route and got one: PIC to the load bank (portable cable) and the H2 20 e-house to the N2 purge supply. Every powered item now has applications and a route; verify, audit and coastal all pass.
- **Gas turbine and steam turbine audit.** Gaps found and fixed (`hall.gt_st_audit()`):
  - GT: no static starters. H-class units start by motoring the generator, so there is now an SFC / LCI lineup with an isolation transformer per unit in the south gallery, cabled in a floor trench to the start disconnect on the IPB.
  - GT: no generator seal-oil or H2 / CO2 gas control. There is now a skid beside each generator, with seal-oil lines to both bearings and the H2 / CO2 lines.
  - GT: no compressor bleed (anti-surge) lines. Two now run per GT with blow-off valves, from the compressor to the exhaust diffuser.
  - ST: main steam was the only steam connection. Added combined reheat stop / intercept valves fed by the hot reheat, and an LP admission line and valve onto the LP casing.
  - ST: added a turning-gear housing and motor on the coupling, junction boxes on the LP casing with conduit to a floor box, and proximity-probe housings at the bearings.
  - ST: no EHC hydraulic unit and no gland-steam condenser. Now present as `EHC-ST` (reservoir, pumps, accumulators, supply and return to the valve actuators) and `GSC-ST` (condenser shell, two exhausters, leak-off line).
  - Deck: no stairs onto the EL 20 deck. Added one from the laydown bay and one at the east end of the south gallery.
  - Wiring applications are on every new item, and verify, audit and coastal all pass. Cameras E51 (ST), E52 (GT1 generator end), E53 (static starter).
- **Tray review (user screenshots).**
  - **ACC transformers:** the short drawn tray stubs between a duct-bank end and the T-R4-1..4 transformers rode the EL +36 rack tier, so a 10 ft connection became a 36 ft "goalpost" over each transformer. These stubs are now buried, with rigid-conduit stub-ups into the transformer terminal compartment. The same rule applies to any short tray stub that leaves a duct bank.
  - **South gallery:** the excitation-transformer feed now runs at the IPB tap level (EL +24) instead of EL +36. The ET-to-excitation cable tray runs just above the cubicles (EL +10.5).
  - **ST aux:** its LV branch had a gap between the hall wall and the run from the rack, leaving a tray end hanging in the air. The gap is now closed.
- **Valve actuators (user screenshot).**
  - **Steam turbine:** the main stop / control, combined reheat and LP admission valve actuators were plain safety-yellow boxes. They are now hydraulic actuators (`hall.actuator()`) in the valve's grey finish: yoke posts and stem, spring can with flange, hydraulic cylinder, and servo / trip block with tubing.
  - **Gas turbines:** the compressor blow-off valve actuators and the VGV actuators are now grey as well.
- **Underground systems (`underground.py`, layers `UNDERGROUND` / `OPT_UNDERGROUND`, viewer view "U Underground").** Buried systems were route data painted as strips on grade; they are now real geometry below grade:
  - **Duct banks:** concrete encasement with a red-dyed top along every buried cable route (2.5 ft cover); the 230 kV banks run deeper (3.5 ft cover). Precast manhole chambers sit under the manhole covers, and handhole boxes at the feeder ends.
  - **Ground grid:** bare 4/0 Cu station ground grid at 18 in, a 40 ft mesh under the power block and electrical areas and 20 ft in the switchyard, with driven rods at the perimeter and risers to every transformer, e-house and structure.
  - **Firewater ring main:** ductile iron with thrust blocks at the bends.
  - **Storm drainage:** RCP under the road edges, catch-basin chambers with laterals, storm manholes at the junctions, and the trunk to the pond inlet headwall.
  - **Oily-water drains (HDPE):** from the transformer containment sumps, turbine-hall lube-oil areas and station transformers to the oil-water separator, then on to wastewater treatment.
  - **Sanitary sewer (green PVC):** from the buildings to a new packaged lift station (LS-1, with its LV feed), and a force main to the west boundary.
  - **Water mains (blue PVC):** potable water to the buildings and service water to the power block.
  - **Viewer:** buried routes are no longer painted on grade; each stays an invisible pick target at its depth. View U removes the ground (SITE) and shows the systems over a soil floor. Blender renders skip the buried routes and the underground layers.
- **Cables and conductors that bend and sag (user feedback: "cables are stiff").**
  - **Tray bends:** every L-corner of a tray run now has a radius bend fitting (curved side rails and radial rungs). The cables sweep round it, inner cables on the inside, and the straight runs stop at the tangent points (51 bends).
  - **Tray drops:** each drop is a "waterfall". The cables leave the tray, curve down over a 1.2 ft radius and hang against the rungs of a ladder drop to a cable gland at the equipment.
  - **Strung conductors (`cables.py`):**
    - **Strain buses:** the 230 kV strain buses sag between the dead-end structures, and the bay droppers meet the bus at its sagged height.
    - **Shield wires:** sag between the dead-end peaks.
    - **GSU-to-switchyard lines:** these overhead routes, previously flat bars, are now three ACSR phases with sag, carried on steel monopole angle structures where the routes turn.
    - **H-MOD tie:** hangs on suspension strings at its monopoles.
    - **Jumpers and droppers:** short ones get a slight curve.
  - Rigid tubular bus on post insulators stays straight, as it is in reality. The viewer and Blender no longer draw the overhead routes as bars; the conductors are geometry.
- **Tray supports and fences (user screenshots).**
  - **Tray supports:**
    - **Cause of the floating spans:** supports were skipped wherever the floor was inside an equipment envelope. The trays crossing the turbine hall over the machines, and the run under the ACC, had spans of up to 411 ft with no support.
    - **New support logic:** supports now check the actual steel and parts. Options are tried in order:
      - a trapeze from the floor, widened to a portal where a pipe runs on the same line;
      - a single-post T-support beside equipment;
      - posts on a flat e-house roof;
      - threaded-rod hangers from steel above (in the hall only below EL 80, never into the crane path);
      - a cantilever bracket off nearby structural steel (not off HRSG casings or pipes);
      - finally, a beam shared with a parallel tray's posts.
    - **Spacing and result:** 12 ft spacing (NEMA 12 class); the longest unsupported span is now 29 ft.
    - The ST-aux branch "fix" from the tray review was undone: R3 sits between the two ends, and the tray end over R3 now drops to a roof entry instead of crossing its roof.
  - **Fences:** fences drew as solid 8 ft grey slabs. The north gate in the screenshot looked like walls: the link road to the LNG terminal through the perimeter fence, with the two gate leaves parked open. Fence panels are now see-through chain-link mesh in the viewer (the Blender look was already a haze). Every fence gets line posts every 10 ft and a top rail, and posts and gate posts are galvanised steel.
- **Shared cable-tray racks (user screenshot east of R1).** Parallel trays at different tiers (EL 30-48) in one corridor each had their own pair of thin posts, so they stood on a forest of loose sticks. Runs that share a corridor (same direction, within 14 ft, overlapping by more than 10 ft) now ride on one cable-tray rack: portal frames about every 20 ft, each with two wide-flange columns on concrete piers, a beam at every tray level and knee braces, plus longitudinal ties where clear. Single trays keep their own supports. HRSG length kept as drawn (Rev 14: 160 ft casing, 240 ft gas path), at the user's decision.
- **Cable trays read as cable systems (user screenshots by R2A / HRSG 1).**
  - **MV cable colour:** MV-105 cables are now black (their real jacket colour) and MV trays carry six triplexed circuits plus one red ARMOR-X cable. Before, a single colour made each MV tray read as one flat red strip.
  - **Building risers:** where a tray ends just outside a building wall above the roof (R1's east wall, R3, R4, the R2 e-houses), the cables now leave the building through a multi-cable transit frame below the roof line with a rain hood, climb a vertical ladder riser on the wall and bend out onto each tray level. Before, the trays simply began in mid-air beside R1 and the drawn exit stubs at EL 18-20 connected to nothing.
  - **Ends at equipment:** tray ends at equipment faces (HRSG casings, skids) end in a terminal junction box on the face, never through the casing.
  - **Hall conduit:** the GT junction-box conduits now stop at the tray drop instead of crossing it.
- **Viewer size (artifact failed to open on mobile at v59, 12.2 MB).** The model data is now embedded gzip-compressed (base64) and inflated in the browser with `DecompressionStream`; the page is about 1 MB. The "Everything" view no longer switches on the underground layers.
- **Duct banks rebuilt and underground cable audit (user review).**
  - **Duct banks as built:**
    - **Conduits:** PVC conduits inside a cast concrete encasement (drawn see-through in the underground view) with a red-dyed top. Sizing follows the circuits sharing each stretch: one 5 in conduit per feeder plus ~50 % spares, from 2 x 2 up to 6 x 4, never more than two rows deep. 230 kV banks carry one 8 in conduit per phase plus a fibre / ground duct.
    - **Joints and ends:** long-radius sweeps at every corner; a red warning tape 12 in above; stub-ups at the feeder ends (90° sweeps rising to grade with bell ends) into the equipment.
    - **Depths:** 30 in cover for MV / LV. The 230 kV banks run 1 ft below the deepest MV bank, where they used to collide.
  - **Separation:** the buried pipes sit deeper: water 6.8 ft, firewater 7.3 ft, sanitary 7.8 ft, oily water 8.3 ft, storm 9.5 ft. Any pipe that would still pass within 1 ft of a bank dives under it.
  - **Cable route ends:** the three 230 kV cable routes that ended in mid-air in the switchyard (BESS and CCS at the D4 / D5 bays, BTM tie at D6) now rise on cable termination structures with outdoor potheads. The site service duct bank ends in a boundary handhole with a marker post.
  - **Underground audit** (in `audit.py`):
    - **Coverage:** all 255 buried cable routes (42,266 ft) are drawn, with every end at equipment, a termination or another bank.
    - **Conflicts:** no bank-to-bank conflicts, and no bank within 1 ft of a buried pipe.
    - **Fixes:** one diagonal stub (R1) is now an L.
  - **Viewer:** view U also lifts away surface pads (switchyard gravel, yard slabs).
- **Underground coverage across every zone (user question).**
  - **Missed runs:** the underground model now also draws the buried runs that the drawing labels as trays: 10 routes at the pipeline M&R, the gas yard and the LNG side, previously left out. That brings the total to 265 buried cable routes (42,554 ft), each listed per zone by `audit.py`.
  - **Coastal links:** the terminal's buried 230 kV feed (D6 extension to the terminal substation, outside the east fence) is now a real cable bank with sweeps, plus a cable termination structure in the D6 yard. The send-out pipeline (variant A) and landfall pipeline (variant B) are now real buried pipes, not just right-of-way strips.
  - **Viewer:** new view "U2 Underground: all zones" shows the option banks (BESS, modular, portable pad, gas / LNG / H2, CCS, inlet chilling, BTM data centre) with their equipment. Both underground views lift away flat yard surfacing (BESS yard, pads, gravel) so the banks under them show.
- **Cable-pull maintenance scene (`maintenance.py`, viewer view "M", cameras E54 / E55).** A crew is replacing a feeder in the R1 -> water-treatment duct bank (x 355), beside the cable reel yard.
  - **MH-A (355, 887):** the manhole is open, with its cover laid aside, a guard rail with chain, cones, a davit tripod with lifeline, a gas monitor, and a ventilation blower with its duct down the shaft. A reel trailer behind a pickup pays a new cable over a feeder sheave into the shaft. In the chamber a worker feeds it into a duct.
  - **MH-B (355, 1153):** the cable-puller truck stands with its capstan, and its boom and sheave sit over the open manhole, with the pulling rope down the shaft and a dynamometer stand.
  - **Trench between them:** an open excavation with a steel trench box, the encasement broken out to expose the conduits, a ladder, a spoil pile, a mini excavator and an orange barrier fence.
  - **Crew:** ten workers in PPE.
  - **Ground cut:** the compound ground is cut at the openings so the shafts and the trench read from above.
  - **Manhole chambers:** all chambers are now hollow (see-through walls, roof slab with the access opening, cable racks), so the worker and the cable read in the underground view.
- **Maintenance scene moved (user screenshot: clipping with the pipes).** At y 880-1180 the R1 duct bank shares its corridor with the inlet-chilling chilled-water pipes (x 340 / 346), so the reel trailer, guard rails and trench box ran through them. The scene now sits on the same bank further north (y 1150-1370), the only stretch of base-plant duct bank with a 50 ft clear band beside it (searched against every item, above-grade route and road):
  - **MH-A:** station manhole (355, 1153), with the reel trailer north-west of it.
  - **MH-B:** a new pulling manhole (355, 1340) with its own chamber.
  - **Trench:** at y 1236-1260.
  - **Checks:** a direct part-by-part check finds nothing above grade intersecting the scene. Viewer view M and cameras E54 / E55 follow it.
- **Carbon capture audit (`ccs_detail.py`).**
  - **Absorber dimensions:** 62 ft dia x 262 ft with a stack to 313 ft, as Keadby 3's DCO (19 m x 80 m, stack 95.5 m); the size is kept. It was a plain shell with ring platforms and one caged ladder. Added:
    - bed manways at every packed bed and the wash section;
    - an open stair tower to EL 250 with bridges to each platform;
    - an intercooler skid (pumps, plate exchanger) with draw-off and return lines;
    - an instrument / lighting tray riser up the shell with junction boxes and platform lights;
    - a stack platform with CEMS ports;
    - aviation obstruction lights at the top and mid-height (structures above 200 ft);
    - lightning air terminals and a down conductor.
  - **Strippers:** added manways, an overhead condenser over the reflux drum, a tray riser with junction boxes, obstruction lights and lightning protection.
  - **Electrical supply:** the D5 bay feeds two 230 kV circuits, but only one cable (to T-2) was drawn. The second now shares the bank and branches to T-1. Both transformers got 230 kV cable termination structures with jumpers to the bushing tops, and a firewall was added between them (10 ft apart).
  - **Electrical distribution:** the CCS loads were fed by automatic buried feeders chained from one item to the next. They are now fed radially from the MV / VFD building:
    - a wall riser, a tray along the CCS pipe rack (EL 30) with drops to every train's DCC, DCC pumps, rich / lean skid, water-wash pumps, intercooler and absorber;
    - a control tray along y 1100 to the reboilers, strippers, reclaimer, storage, carbon filter, export compressor and dehydration;
    - a buried 13.8 kV bank to the 3 x ~19 MW CO2 compressors.
    - No automatic feeders remain in the CCS.
  - **Equipment and buildings:**
    - booster fans: MV terminal box, cable riser, lube-oil console and motor air intake;
    - MV building: rooftop HVAC, doors and landings;
    - compression building: roof ventilators and doors, plus a new dehydration skid (two molecular-sieve towers and a regeneration heater).
  - **Cameras:** E56 (absorber), E57 (transformers).
  - **Underground:** pipes now dive 1.15 ft under the banks, clearing the deeper two-circuit 230 kV bank.
- **Absorber stair towers removed (user):** the caged ladder with its rest platforms already serves each absorber, so the added stair towers and bridges were duplicates and are gone. Same call as for the filter houses.
- **CCS storage, flue ducts and cable routing (user screenshots).**
  - **Regeneration-area cables:** these ran in a control tray at EL 42 on rows of tall thin posts. They are now buried duct banks with stub-ups into each reboiler, stripper, the reclaimer, storage, compression, the export compressor and dehydration.
  - **Train tray:** the train LV / control tray now rides on top of the CCS pipe rack (EL 27.3), which is its own item, so no posts are needed along it.
  - **Solvent / NaOH storage:** the tanks stood plain on a slab. The farm now has:
    - a 4 ft containment bund with a sump and step-over stairs;
    - cone roofs with vents, wind girders, roof handrails, caged ladders, manways, outlet nozzles and valves, level gauges and transmitters;
    - a transfer-pump pad with a local control station;
    - a truck unloading station with hose connections and a safety shower;
    - pump discharge lines on sleepers to the CCS rack.
  - **HRSG-to-DCC flue ducts:** each was a bare box on two thin posts. Each now has:
    - stiffener frames every 8 ft and cladding seams;
    - fabric expansion joints at both ends;
    - access doors and low-point drains;
    - a test-port platform with a caged ladder;
    - braced portal bents with sliding shoes on pier caps.
- **Flue-duct test platforms moved (user):** the test-port platform and caged ladder sat mid-span over the ring road (y 900-930), so the ladder landed in the road. They now sit near the DCC end (y 948-964), with the ladder on clear grade beside the duct.
- **Absorber lights and amine pipe ends (user screenshots).**
  - **Lights:** an older pass (detail3) placed the absorbers' obstruction lights at the shell radius (31 ft) all the way up, so the top set hung in the air round the 9 ft stack. The absorbers are now skipped there; their lights are on the stack top and at mid-shell (ccs_detail).
  - **Pipe ends:** at each rich / lean skid, every line now meets the equipment it serves:
    - the rich-amine bottoms line from the absorber now runs to the rich-pump suction header;
    - the lean-amine riser now starts at the lean cooler outlet;
    - the rack risers come up off the skid headers;
    - the rich and lean pump discharges join those headers.
- **Plant-wide quality / realism sweep (`qa.py`, `terminate.py`).**
  - **New check:** `qa.py` is a geometry check that complements verify / audit. It flags floating parts, open pipe ends, anything at grade in a road and headroom under 18 ft over roads, and writes `qa_report.json`.
  - **First run found:** 469 floating parts, 412 open pipe ends and 24 road intrusions (after correcting its own handling of large parts).
  - **Open pipe ends (`terminate.build`, runs after all geometry):** every end above grade that touches nothing now gets a realistic ending:
    - 198 drop to grade or to their pad, through a UG sleeve block;
    - 73 upward nozzles (mostly pump discharges) get an isolation valve with a handwheel;
    - 120 with no clear path get a blind flange.
  - **Floating parts (`terminate.support_floating`):** 251 parts above grade that touched nothing now get steel legs down to the surface below. These include transformer conservators over their tanks, pump casings over baseplates, equipment over skids, and headers over roofs.
  - **Roads:**
    - flue-duct bents moved from the ring-road edge (y 930) to y 937;
    - ACC stair towers pulled 2 ft west, clear of the east spine road;
    - the 230 kV angle poles stand 6 ft clear of any road.
  - **Cooling-tower stairs:** the CCS and inlet-chilling tower access stairs get stringers, handrails and intermediate supports.
  - **Result:** open pipe ends 412 -> 21 (only parking bollards and two dry-cooler nozzles, which are fine). Floating parts 469 -> 117 (small wall devices and internal fittings within the check's tolerance). Road intrusions 24 -> 2 (the reserved-corridor marking, which legitimately crosses the road). Verify, audit and coastal all pass.
- **Option-zone detail pass (`zone_detail.py`).**
  - **BESS yard:** surfaced with crushed rock, and the containers sit on concrete plinth beams.
  - **Modular yard:** T-MOD-1 / -2 had their 230 kV bushings ending in the air, with the H-MOD tie starting at its first pole 55 ft away. Now:
    - jumpers rise from the bushings to a take-off gantry (strain strings, arresters on stands);
    - the leads continue to the first H-MOD monopole;
    - a firewall stands between the two transformers.
  - **LNG / H2 / RICE zones:** reviewed and already detailed; no change.
- **R1 east-wall riser (user screenshots).** The "R1 east-wall tray exits / tray riser to rack" was drawn as two solid copper-coloured blocks, 4 ft square, EL 0.6-36. The rack trays starting beside the wall (x 478, y 736 / 746) didn't see R1, because they run parallel to the wall rather than pointing at it, so each got a cable drop that landed on the block.
  - **Risers:** `trays.building_beside` now also recognises trays that start within 5 ft alongside a wall. These trays now leave R1 through wall entries below the roof and climb ladder risers to their tiers, like the other building risers.
  - **Copper blocks:** removed.
  - **Interior and wall-sleeve trays:** R1's interior overhead trays and wall sleeves were orange copper bars. They are now galvanised ladder trays carrying their cables.

### Maintenance scene relocated to the modular yard
- The cable-pull scene (open manholes, davit, blower, reel trailer, puller truck, trench box, excavator, 11 crew) moved off the
  cramped R1 -> water-treatment bank by the inlet-chilling plant onto the modular power yard's 13.8 kV collector duct bank
  (y 960, x 1712-1900), open ground south of the RICE / SC units: an MV feeder replacement with room for the vehicles.
  MH-B reuses the existing bend manhole at (1900, 960); MH-A is a new chamber on the bank.
- The scene is part of the modular-yard option (layer OPT_MOD); a NOMOD_GROUND patch closes the ground openings in views
  without the yard (viewer and Blender switch it automatically). View M and cameras E54 / E55 updated.
- Fix: the ground cut now subtracts every opening from each compound tile in one pass (the old split left overlapping
  duplicate tiles along the bank, which rendered as a black band); E54 / E55 re-rendered with shorter captions.

### Cable product showcase (Southwire, the requested cable supplier)
- New `showcase.py`: printed decals (placards, reel stencils, truck livery) as a model-level `decals` list, drawn by
  the viewer (canvas textures) and Blender (PIL image textures); brand lines are flagged so `build_viewer.py --generic`
  and the Blender `--generic` flag leave the wordmarks off (`viewer/index.html` = generic, `viewer/index_southwire.html`
  = branded).
- Cutaway display stands (2:1 samples, layers stepped back from the cut: conductor, insulation, shields, sheath /
  armor, jacket; spec placard and sign panel) for 230 kV XLPE, MV-105, ARMOR-X MC-HL, Type TC-ER, instrumentation,
  SIMpull THHN, overhead conductor (ACSR / ACSS / C7), bare copper grounding, Armorlite MC / MV-105 35 kV.
- At the point of use: R1 tray riser (TC-ER), switchyard (overhead conductor, bare Cu), plant gas yard (ARMOR-X MC-HL,
  Class I Div 2), BESS 230 kV cable termination (HV XLPE), BESS collection and modular-yard collector (MV-105),
  data hall A gallery (MV-105 35 kV, Armorlite MC).
- The drawn cable reel yard / outage laydown is now a stocked reel yard: three rows of stencilled reels (230 kV on a
  steel reel, MV-105, ARMOR-X, TC-ER, instrumentation), the SIMpull Truck (flatbed with three SIMpull Reels on
  payoffs, livery on the skirts and doors) unloading, two reels on payoffs with a crew, the full product row and a
  yard sign. The modular-yard pull scene's reel now carries MV-105 with stencilled flanges.
- Viewer views CY, CHV, CTC, CSY, CDC; Blender cameras E58 (reel yard + SIMpull Truck), E59 (product row),
  E60 (230 kV cutaway at the BESS termination); E54 re-rendered with the branded reel.
- Removed again (user review: a showcase is not wanted, the cable should be shown installed where it is used): the
  cutaway display stands, sign panels, product row and yard sign, views CHV / CTC / CSY / CDC and cameras E59 / E60.
  Kept: the stocked reel yard, the SIMpull Truck and the decal system.

### Installed cable at the point of use
- New `cable_install.py`. 230 kV cable termination structures (BESS bay, CCS T-1 / T-2) rebuilt as installed: braced
  steel structure on a foundation, the three 1/C XLPE cables up out of sealed duct mouths through steel cable guards,
  cleated to beams every 3 ft, through entry glands into outdoor sealing ends (stress-cone body, shedded insulator,
  top terminal); surge arresters behind, jumpered to the terminals, with ground leads and a surge counter;
  sheath-bonding leads to a link box on the front column with a copper lead to the grid. The cable jacket carries
  its printed legend (supplier name only in the branded build). CCS jumpers to the T-1 / T-2 bushings start at the
  new terminals.
- MOD-EH: the solid plinth is now piers and a steel skid base; at each duct-bank stub-up the cables leave the end
  bell (MV-105 triplex from the grey conduits, fibre from the orange) and rise under the skid beam into gland plates
  under the bottom-entry switchgear.
- Decals can be generic-only twins (`nobrand`) of branded ones. Views CHV, CEH; camera E60.
- Pad-mount termination cabinets (`padmount_cabinet`) on all 96 data-hall 34.5/0.48 kV pad-mounts (feeder side) and the
  15 BESS PCS / MV skid transformers (collector side): loop feed of six 200 A load-break elbows on the HV bushings,
  test-point caps, concentric-neutral leads to the ground bus, parking-stand bracket, cables down through the pad to
  the feeder bank; LV compartment shut. Doors shut and labelled on most; open on one per area (printed legend on a
  cable). The tank face stops at the cabinet back sheet.
- BESS DC trench (`bess_dc_trench`): the flat slabs are now precast U-sections with lids; at one skid a run of lids is
  lifted and stacked on timber and the compound ground and yard gravel are opened (patch layer NOBESS_GROUND for
  views without the BESS), showing the paired 1,500 V DC conductors from the container DC entry boxes along the
  trench floor and up into the inverter gland plate.
- Blender: patch layers are no longer part of "all"; set_visibility decides them. Views CPM, CBE; cameras E61-E63.
