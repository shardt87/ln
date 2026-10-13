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
- User review: no cable detail in the data centre (plant only), and shots that tell a story rather than isolated
  details. Removed the data-hall pad-mount cabinets, view CPM, cameras E61 / E63. Added two staged stories
  (`showcase.stories()`): the SIMpull Truck delivering feeder reels on payoffs to the modular-yard 13.8 kV cable pull,
  and a BESS crew pulling DC conductor off a reel on jack stands into the open precast trench. Views SD, SB; cameras
  E64, E65.
- Turbine hall story (`showcase.turbine_hall_pull()`): GT1 outage, a new 13.8 kV MV-105 feeder pulled from a reel on
  jacks in the laydown bay, over a sheave hung at the tray corner into the EL 48 MV ladder tray and along it to the
  GT1 drop, where a capstan puller on the deck hauls the rope; a scissor lift on the deck puts two electricians at
  tray level; reel tender, sheave watcher and supervisor on the floor. View ST; camera E66.
- 230 kV splice story (`showcase.splice_230()`): on the CCS 230 kV cable bank at x 1520, y 559-591 (clear of the
  feedwater rack further north): an open joint bay cut into the bank (bank and ground split around it, patch layer
  NOCCS_GROUND), three phases racked on the walls with staggered joints (two finished with earthing bands and bonding
  leads, the middle one in progress: XLPE pencilled back, connector crimped, joint body parked), cross-bonding link
  box, ladder, guard rail, two jointers; white jointing tent with sides rolled up and work lights, generator and spot
  air conditioner; the next 230 kV drum on a lowboy behind a red tractor; HV test van with its lead to the bay;
  supervisor, crew, barrier. View SJ; camera E67.
- User review: the 230 kV splice story (SJ / E67) was not liked; removed.
- Conditional items: the yellow flag colour is replaced by real finishes (tanks white with grey roofs, unloading pad concrete, compressors / chillers machinery grey, transformer and BESS in their own finishes); basis stays 'conditional' in the data. ULSD and TES tanks get a spiral stair, roof handrail, wind girder, top angle, vent, gauge hatch, manway and nozzles.
- Turbine-hall tray legends (`showcase.tray_legends()`, `tray_dresser()`): printed jacket legends repeated along every
  cable in the tray stack east of GT1 (x 596-724): MV-105 15 kV and ARMOR-X MC-HL in the EL 48 MV tray, Type TC-ER in
  the EL 44 LV trays, instrumentation PLTC and KX thermocouple in the EL 42 control tray; print turned 40 deg toward the
  walkway; supplier name only in the branded build. Scissor lift on the deck with two electricians dressing and
  tagging, fresh ties on the MV bundle. Tray cables in this stack drawn round (16 sides); jackets matte. Blender decals
  share one image / material per unique label. View SL; camera E67.
- Tray stack: ARMOR-X drawn with its corrugated armor ribs through the jacket (x 596-652), an ARMOR-X offcut on the lift platform stripped to the bare corrugated aluminium armor and conductors; E67 re-shot looking east inside the hall (walls shown, roof off) with the lift crew mid-frame.
- E67 re-shot with the hall roof on: interior cameras can switch the high-bay fixtures on as area lights (camera option lamps=W); frames GT1 below the tray stack. View SL shows the roof.
- E67 re-shot at the user's chosen viewer angle: just above the MV tray, looking north-east across the legends to HRSG-2 and its stack; hall cladding see-through in this render (camera option hall_alpha), high-bay lights on.
- Cover shot E68 (portrait 1545 x 2000): from the LV tray on the CCS rack (y 1133, EL 28) looking up at Absorber B with A beyond and the BF-B flue duct; legends (ARMOR-X MC-HL, Type TC-ER) printed on the rack-tray cables x 726-856; per-camera near clip (clip) for close shots.
- ARMOR-X MC-HL (cable_mc) drawn as it is: black PVC jacket (not bare metal) with the corrugated welded aluminium armor showing as fine ribs (CCS rack stretch x 708-800); cover re-rendered.
- Deck-style CCS section divider (blender/deck_divider.py): 16:9 slide matching the user's Southwire x Anixter/Wesco PowerGen deck (Barlow Condensed, charcoal / copper, logo, section number 14 = CCS zone in the deck's plant model, tag box, item rules, watermark, footer), photo E69 (1170 x 1080) under the dark diagonal. Output renders/deck/SK-3X1_divider_ccs.png / .pdf.
- 02 Gas Power divider re-shot with cable leading the frame (E71): legends and ARMOR-X ribs on the outdoor R1 -> hall MV tray (x 560, y 560-640, EL 48), looking north down the cables to HRSG 1 and its stack.

### Render quality pass
- Procedural cumulus sky (pro_look.add_clouds): a cloud deck in the world shader, view direction projected onto it so
  clouds recede in perspective, fractal noise for the shapes, second noise for lit tops / grey bellies, faded at the
  horizon; camera rays only, so lighting stays the sky + sun. (Online HDRI libraries are blocked by the network
  policy; this is full resolution and needs no image.)
- New shared scale figure (figure.py) for every person in the model: boots, jointed legs, pelvis, tapered torso in a
  hi-vis vest with reflective bands, shoulders, jointed arms with gloves, neck, head, hard hat with brim; relaxed or
  working pose.
- Deck divider photos rendered at 160 % and 160 samples; photographic finish (vignette, fine grain) in
  deck_divider.finish_photo.
- Whole-facility cover photo K5 (coastal variant A overlay: plant, BTM data centre, LNG tank, jetty and carrier) from the south-west, 1170 x 1080 at 160 % / 160 spp with the cloud sky; deck title slide (make_title, the deck's cover layout) and an alternative 02 divider on it.
- Cover photo K6: from the cable reel yard (230 kV steel drum stencilled SOUTHWIRE, reel row receding) across to the HRSG stacks and turbine hall; title slide and alternative 02 divider rebuilt on it (K5 aerial kept).
- Backdrop (pro_look.backdrop): rolling hills beyond ~5,000 ft, rectangular farmland parcels with rows and hedge lines (also on the flat surround), a four-lane highway with traffic, and the two 230 kV lines leaving the switchyard on 38 double-circuit lattice towers with catenary conductors and shield wires. Cover camera K7: golden hour between the lines, conductors leading to the plant.
- Cover look pass: per-camera grade (apply_look: haze, saturation, exposure, sun colour / strength, sky dust, volume bounces; LOOK_GOLDEN for K11) and white vapour plumes above the three HRSG stacks and the three absorbers (add_plumes: chains of soft volumetric puffs drifting downwind), enabled per camera.
- Material pass: colour hierarchy (dark roofs, blue-grey HRSG casings, darker steel stacks and ducts against the white absorbers), panel-to-panel tone variation on cladding, grey crushed-stone ground; plume wind direction per scene (cover: drifting west, clear of the LNG terminal); cover camera reframed.

### TM2500 mobile turbines (TM-1, TM-2) at LOD 3
- The two trailer-mounted aeroderivatives were still block models. Rebuilt in `yard.tm2500()` inside the same
  78 x 55 ft envelope and 42 ft height:
  - **GT trailer:** ladder chassis with cross members, a four-axle rear bogie and a two-axle mid bogie (dual tyres,
    rims, hubs, fenders) on timber crane mats, gooseneck and kingpin plate on landing legs with sand shoes.
  - **Enclosures:** turbine and generator enclosures with panel seams, doors with handles, wall intake louvres, and
    a roof vent silencer with two fans.
  - **Filter house:** combustion-air filter house on a frame over the generator end, with three rows of weather
    hoods, a roof ladder and handrail, and a plenum down to the inlet.
  - **Exhaust:** rectangular exhaust collector and raised stack with silencer section, flange bands and stays (it
    was a round chimney).
  - **Control / auxiliary trailer:** rear HVAC unit, wall units, door, landing and stair; interconnect cables to
    the GT trailer under a yellow cable protector.
  - **Fuel-gas / water-wash skid:** moved off the gooseneck to the east end; flexible gas hose to the trailer.
  - **Cable moment:** the generator terminal box on the north face drops six 15 kV MV-105 1000 kcmil leads (two per
    phase) into an open ground tray on sleepers. The tray runs north to the yard duct bank, and printed jacket
    legends are staggered on the run. The TM-1/TM-2 cable routes now start at the tray (x + 50).
- New palette colour `tyre`. verify, audit and coastal checks: PASS / CLEAN.
- The generic e-house door-and-stair dressing in `detail.py` now skips TM items (it had dropped a loose stair beside each trailer).
- Cameras **E72** (TM-2 from the south-east) and **E73** (generator leads and legend close-up). Viewer v93.

### Modular yard: cable on the surface where the power is temporary, last plain units detailed
- **Buried vs surface.** The permanent modular plant (RICE, LM6000-class units, MOD-EH, T-MOD) keeps its buried
  duct banks. The portable pad and the bridge-power units are now cabled on grade, the way rental power is
  installed (`surface_cable.py`; routes inside the pad area are tagged `surface`, so the underground pass skips them
  and the renderers draw the cable parts instead of a strip):
  - **Portable pad (OPT_TMP):** 15 kV Type SHD-GC portable power cable (yellow jacket, two per feeder) laid loose
    on the gravel; 480 V links as two Type W sets of four single conductors (black) ending in colour-coded cam-lock
    plugs at PAD-LV, GEN-E, GEN-O and the input cabinet; MV ends rise to gland plates.
  - The C-L01 drive-over ramp from sheet 08 is now a modular cable protector (black base with sloped edges,
    yellow hinged lids in 3 ft modules). The MOB-1 -> PIC feeder runs through it (it used to cross the lane with no
    ramp).
  - **Bridge power (OPT_MODX):** CONT-3..8, the CONT paralleling e-house and TM-1 / TM-2 feeders run in open
    ground trays on timber sleepers. The trays sit high enough for the loose 480 V sets to pass under them, and no
    sleeper lands on a cable. The TM-1 feeder no longer passes under PAD-LV.
  - Cable ends that started inside a unit (CONT-6, GSP-2) now stop at the unit's face.
  - Printed jacket legends on the longest straight run of each feeder (SHD-GC and Type W).
- **Last plain units at LOD 3** (`yard.small_units()`):
  - GSP-1 / -2 breaker cabinets: doors, louvres, gland plate, sign.
  - PIC input cabinet: cam-lock receptacle panels with rain hoods on both faces.
  - GEN-O open engine-generator skid: base rails, radiator with guards, V engine, generator, terminal box,
    silencer, control panel, batteries.
  - Portable-pad gas-conditioning skid: two filter-separators, line heater, two regulator runs with control
    valves, panel.
  - RICE CEMS shelter: door, HVAC, calibration-gas cylinder rack, sample-line entry.
  - SC-1 / -2 lube-oil fin-fan coolers: legs, coil bundle, fan rings, drives, headers.
- The RICE engines were already at LOD 3 (V18 block, heads, turbochargers, generator) inside the see-through hall.
- New colours: `cable_shd`, cam-lock red / blue / white / green, `hdpe` in the render look.
- Cameras: E74 (portable pad overview), E75 / E76 (modular yard reviews), E77 (SHD-GC through the C-L01 ramp),
  E78 (Type W and cam-locks at PAD-LV), E79 (GEN-O and GEN-E). verify PASS, audit CLEAN, coastal PASS. Viewer v94.

### Switchgear rooms at LOD 3: R1 and the R4 VFD e-house (`swgr_rooms.py`)
User review: the switchgear rooms were plain boxes. The lineups keep their drawn footprints and heights
(SK-3X1-05, -03, -11 view B2); the room around them is now fitted out as a real electrical room.
- **15 kV / 5 kV metal-clad (SWGR-13.8-1/2/3, SWGR-4.16-A/B):** 36 in two-high cubicles: breaker door with viewing
  window, racking port and handle; relay door with a numerical protection relay (LCD, target LEDs, keys), power
  meter, open / closed / charged lamps and control switch; mimic bus with drops; cubicle nameplates; base channel;
  arc-resistant relief flaps and roof plenum, with the 13.8 kV plenum exhaust taken to the east wall.
- **480 V (LC-480-A/B, R4-LC):** four-high draw-out breaker cells with trip units. **MCCs (MCC-GT1..3, C1/C2,
  EMCC, R4 vacuum-pump MCC):** 20 in sections, buckets with disconnects and pilot lights, wireways; conduit drops
  from the overhead tray into the MCC tops.
- **P&C panels:** flush relays, test switches, lamps. **DCS / telecom:** perforated doors, status LEDs.
  **LP / HT:** panelboards.
- **LCI-1..3 and the 92 ACC VFDs:** louvred doors, keypads, lamps, roof fan hoods; dry-type TX-LCI transformers
  in louvred enclosures. R4: VFD output trays over each lineup to the cable exit, bus-duct entries from T-R4-1..4.
- **Room:** epoxy floor, yellow aisle lines, dielectric mats in front of every lineup, LED high-bays on hangers,
  ducted HVAC with diffusers (R1) and four wall-mounted units (R4), copper ground bus, extinguishers, exit signs,
  lineup nameplates and NFPA 70E arc-flash labels, an MV breaker lift truck with a spare breaker, technicians at
  SWGR-13.8-2 and VFD lineup 1.
- Interior colours (`swgr_in`, `cab_in`, `panel_in`, `epoxy`, `mat`, `led_*`, `hmi`, `lamp_in`, ...) stay clean in
  Blender; the LEDs, displays and fixtures glow. Room cameras take `add_layers` (interior layers) and
  `lamp_z` / `lamp_box` (which fixtures light the shot).
- Cameras E82 (R1 MV aisle), E83 (R1 MCC / P&C aisle), E84 (R4 VFD aisle), E85 (R1 roof-off cutaway). verify PASS,
  audit CLEAN, coastal PASS. Viewer v96 (views B and B2 show the rooms).

### Control / admin building: main control room and offices (`control_room.py`, `screens/make_screens.py`)
User request: a real control room with SCADA and screens. The building keeps its SK-3X1-12 footprint and height;
the solid box is now walls, a roof slab and a suspended ceiling (layer `CR_ROOF`), with the rooms on `CR_INTERIOR`
(off in the plant views like the R1 / R4 interiors; view **B3 Control room** and camera E88 lift the roof).
- **Main control room** (east end, 43 x 49 ft): a 16-cube video wall (8 x 2, ~70 in cubes) shows the plant overview,
  the 230 kV one-line and a CCTV mosaic across 2 x 2 cubes, plus dispatch / AGC, trends, ACC and the alarm
  summary. A six-position operator console on an arc faces it, each position with 2 x 3 monitors (27 in) on posts,
  two keyboards, mice and a phone. Hard-wired GT / ST trip and plant ESD buttons sit under guards at the two centre
  positions. The shift supervisor's desk is on a raised platform behind, with five monitors. There's also a halo
  light, carpet tiles, a 2 x 2 ft ceiling grid with troffers, acoustic wall panels, a GPS clock with frequency and
  MW tickers, the fire-alarm panel, binder shelving, a printer and plants. Three operators sit at the console and
  the supervisor stands at the platform.
- **Screens** are real images (`plant/screens`, drawn by `make_screens.py` in a high-performance HMI style):
  - overview, 230 kV one-line, GT1, HRSG 1, 8-hour trends, alarm summary, ACC 80 cells, ISO dispatch;
  - a CCTV mosaic cut from the plant renders.
  Decals take an `img` (Blender: an emissive image texture; viewer: an embedded JPEG, self-lit).
- **Rest of the building:** shift-supervisor office behind a glass wall, operations meeting room, DCS engineering /
  server room (two rack rows, workstations), lobby with reception, plant sign and safety board at the entrance,
  conference room with a wall display, break room, open office (24 desks), north strip with lockers, restrooms,
  permit / work control, print, training, telecom / UPS, kitchen, relief room; door signs on every room.
- Operators and office staff have no hard hats indoors (seated and standing figures in `control_room.py`).
- Cameras E86 (MCR hero), E87 (over the console), E88 (roof-off cutaway). verify PASS, audit CLEAN, coastal PASS.

### SIMpull / Maxis installation equipment (`simpull.py`)
User request: add the SIMpull Solutions equipment (brochure and NECA 2026 booth photos) to the reel yard and wherever
it makes sense on the plant. Sizes are from the brochure; the geometry is typical.
- **Reel yard staging** (east end of the reel pad):
  - six SIMpull Reels (61 x 32 in, black spoked flanges, magnetic chocks) on SIMpull Cradles, holding paralleled
    colour-coded feeders with reel labels;
  - an RR-SW45 Reel Roller with a 35 kV MV-105 steel reel, a second RR-SW45 with 15 kV, and an RR-SW30 with
    ARMOR-X. Each has its welded frame, driven rollers, fork tubes, motor / VFD box and pendant;
  - three wooden reels fitted with SIMpull Flanges, and two SIMpull Stack paralleled reels on Maxis JAX reel stands;
  - a CoilPAK cart, a wire wagon, two SIMpull BARREL drums on hand trucks, the Maxis Feeder and the Maxis XD10
    puller, and a Southwire tools & equipment container;
  - temporary power: a 150 kW towable generator, cam-lock cords, a 480 V 3-phase cart and power distribution
    boxes, plus extension cords, tripod LED work lights and an area light.
- **Active feeder pull at the maintenance building:** a new 400 A welding-shop feeder (SIMpull THHN 4 x 500 kcmil
  + ground) comes off a SIMpull Reel. Its factory SIMpull Heads go into the wall wireway and conduit riser.
  Branch circuits feed from a BARREL drum and a wire wagon. The pull has a tension monitor, a Triggers wireless
  safety switch, a distribution box, a work light and a three-person crew.
- **Existing pulls:**
  - Turbine-hall GT1 outage pull: the MV reel now sits on an RR-SW45 Reel Roller, with a tension monitor and a
    Triggers switch at the capstan.
  - BESS DC trench pull: the red reel jacks are now black Maxis JAX stands.
  - SIMpull Truck: its reels now use the real SIMpull Reel look.
- Cameras E89 (yard staging), E90 (workshop feeder pull), E91 (reels and reel roller close-up). verify PASS,
  audit CLEAN, coastal PASS.

### Prefabricated cable systems: staging bay and the modular-yard cable spine (`prefab.py`)
User question: should prefabs and cable-spine prefabs go in the reel yard? They go on the same drawn pad ("cable reel
yard / outage laydown"), but in their own bay, and the model also shows where they go.
- **Prefab staging bay** (south strip of the pad, beside the truck / crane lane):
  - spine modules 6-8 on timber dunnage, with shrink-wrapped coiled tails and sequence tags; module 9 arrives on a
    flatbed with ratchet straps;
  - pre-terminated 15 kV MV assemblies in open crates: factory terminations, tested and capped, tagged for T-MOD-1
    feeder B;
  - two prefab multi-conduit racks, three pre-wired junction-box skids, and a "Prefab staging" sign.
- **Cable spine going in** (modular-yard expansion, OPT_MODX): an elevated LV power / control / fibre spine from
  MOD-EH north toward the aeroderivative units.
  - Built from 40 ft modules: a welded frame with three ladder-tray tiers (EL 12 power, EL 14.5 control, EL 17
    fibre) and the cable laid in. The modules sit on bents every 20 ft on pier footings.
  - Modules 1-4 are set, with splice plates between them. Tray risers drop into a wall entry on MOD-EH.
  - Module 5 hangs from a truck crane on a spreader bar, held by two riggers on tag lines. Two electricians on a
    boom lift at the module 4 / 5 splice take the coiled tails. The bents for module 6 stand ready, and a lift
    supervisor watches.
- Labels are generic (prefabricated cable spine, pre-terminated assemblies); geometry typical.
- Cameras E92 (crane lift), E93 (staging bay), E94 (splice). verify PASS, audit CLEAN, coastal PASS.

### Skid pre-assembly / pre-wire workstation (`skid_prewire.py`)
User question: should skid equipment be pre-wired at a prefab workstation? Yes for small and mid skids; no for
transformers (set directly, wired in place) or large e-houses (factory-integrated; only their shipping-split
interconnects are a site job). Placed in the drawn maintenance laydown (north-west corner, OPT_MODX). It was first placed beside the cable spine at the work front; moved on review because a dedicated laydown keeps pre-assembly away from energised plant, gives contractor access from the west spine road, and leaves the east half clear for engine / turbine exchanges. Finished skids go out on a lowboy (waiting at the laydown) to the modular yard.
- **Workstation:** a fabric shelter (arched frame, open south end, east side rolled up) on a slab.
  - A fuel-gas conditioning skid and a CW pump skid sit on cribbing being pre-wired: JBs on stanchions,
    skid-edge ladder tray, conduit drops, field tails coiled and tagged, a PRE-WIRE IN PROGRESS / DO NOT LIFT
    tag.
  - Around them: workbenches with a megger, JB and tray-fitting kits on pallets, a wire wagon, a distribution
    box, two tripod lights, and four electricians.
- **Ready-to-set row:** a lube-oil skid and a second fuel-gas skid, wrapped tails, TESTED / READY TO SET tags
  (IR > 1 GΩ, continuity OK), crane pick order sign.
- **PDC e-house in two shipping splits** on cribbing: split faces wrapped, and pre-terminated interconnects
  coiled at the split and tagged for reconnection.
- Cameras E95 (overview), E96 (inside the shelter). verify PASS, audit CLEAN, coastal PASS.

### Turbine hall access: how people cross between the units (`hall_access.py`)
User question: how do people cross the turbine hall? The machine trains fill the EL 20 deck from the south gallery
to the HRSG wall. Cable trays run at EL 41-49 over them (GT top EL 38, generator EL 36), which leaves no headroom
for a crossover bridge over the machines. As in a real table-top turbine hall, people cross underneath:
- **Structure:** the solid EL 0-20 block is now an operating-floor slab (EL 18.5-20) on a 20 ft steel column grid
  with beams. Each GT and the ST stands on its own table-top pedestal (top slab on concrete legs). The ground floor
  is open, with LED fixtures under the slab and yellow walkway lines. The inlet-chilling chilled-water headers
  (EL 3), which used to be buried in the block, now run visibly under the deck.
- **Stairs:** stairs rise from the ground floor through guarded slab openings (toe board, mid and top rails)
  between GT1 / GT2 and GT2 / GT3. With the existing laydown-bay and south-gallery stairs, the route is: deck - down
  - across at grade - up - next unit.
- **Crossover stiles:** where the north-south walk to each stair meets the chilled-water headers, a stile (steps
  up, a grated platform with handrails, steps down) carries people over them.
- Operators are shown on the ground floor, on a stile, on a stair and arriving on the deck.
- Cameras E97 (ground floor), E98 (deck opening). verify PASS (0 clashes), audit CLEAN, coastal PASS.

### HRSG shape review (`hrsg.py`, `build_model.py`)
User question: does the HRSG look right? The type and arrangement are right: horizontal gas flow, three-pressure
reheat with SCR, drums on the roof, diverging inlet transition from the GT exhaust, stack at the outlet. Three things
made it read wrong against photos:
- **Casing height:** raised from 78 to 85 ft, the upper value in the sheet-13 note; H-class units sit at the top of
  that range. The drums keep their elevation on a shorter frame, so the top stays at EL 100. The roof, risers,
  handrail, steam leads, downcomers, AIG riser and cable riser all follow the new roof.
- **Stair tower:** was a solid grey block. It's now an open switchback stair tower at the south end of the east
  wall: four columns on footings, 10 flights to the casing roof, landings and yellow guard rails. The tower was
  first placed at the north-east corner, but the EL 30 cable tray (x 670-672.5) runs through that spot, so it
  moved to the only spot clear of trays on all three units.
- **Access platforms:** new grated platforms with yellow handrails along the east wall at every second landing
  (about EL 17, 34, 52, 69), running north from the tower on brackets from the buckstays, plus a step-over from
  the top landing onto the casing roof.
- Camera E99 (south-east view); E26 and E28 re-rendered. verify PASS (0 clashes), audit CLEAN, coastal PASS.

### HRSG control tray fix (`routes_base.json`, `build_model.py`, `hrsg.py`)
User question: a tray rising from the R2 e-house roof ended in mid-air at the HRSG. The drawing has the EL 42
control / instrument tray from each R2 e-house to its HRSG as a diagonal line. The tray generator only builds
straight runs, so it dropped the run and kept only the riser and elbow at the e-house end.
- The route now runs as a real tray would: riser from the e-house roof, north along the EL 30 LV tray line
  (sharing its supports), east to the HRSG west wall, ending over a new marshalling junction box there.
- Any other diagonal tray segment on the drawings now becomes an L (along x, then y) when the routes load.
- Camera E100 (west side close-up); E26 and E28 re-rendered. verify PASS (0 clashes), audit CLEAN, coastal PASS.

### HRSG proportions (`build_model.py`, `hrsg.py`, `realism.py`)
User question: does the HRSG read as one giant block, should the tail be shorter? Yes: built H-class
three-pressure HRSGs have a casing of about 120-130 ft behind a long (about 70 ft) inlet diffuser, with the stack
tight at the outlet. The model had a 158 ft casing behind an abrupt 40 ft inlet duct.
- The drawn envelope (70 x 160 ft, sheet 01) and the stack position (sheet 01) are kept. The casing now starts at
  y 629: 130 ft long, with the first coil section (HP superheater / reheater) shortened.
- The inlet transition is a 69 ft diffuser from the GT exhaust to the casing face, with four stiffener frames.
- The stair tower stays at the south-east corner beside the diffuser and bridges onto the roof. The east-wall
  platforms, the cable riser, the roof junction box and the steam leads follow the new south end.
- Camera E101 (aerial from the west); E99 and E26 re-rendered. verify PASS (0 clashes), audit CLEAN, coastal PASS.

### HRSG outlet hood (`build_model.py`, `hrsg.py`, `routes_base.json`)
User question: is the connector between the HRSG and the stack realistic? No: a 50 x 30 ft box joined the middle
of the 64 x 81 ft casing outlet to the stack. Built units take the whole casing outlet through a converging
outlet hood into a tall rectangular inlet on the side of the stack.
- A 3 ft flanged section at the full casing outlet with the expansion joint. Then a 17 ft hood converging to
  18 x 62 ft, and a straight end that pierces the stack shell. Three stiffener frames on the hood.
- The steam leads now come down north of the hood (y 777). The steam route starts there, and the condensate
  line now enters the casing on its west wall instead of running under the hood.
- Camera E102 (outlet hood from the north-east); E28 re-rendered. verify PASS (0 clashes), audit CLEAN, coastal PASS.

### Turbine hall ground floor: crossover stiles removed (`hall_access.py`, `build_model.py`)
User question: what is the up-and-down stair under the deck? It was a crossover stile over the inlet-chilling
chilled-water headers at EL 3. Those headers are an optional system, so in most views the stile crossed nothing.
Even with them shown, running the headers overhead under the slab is the realistic layout.
- The CHW headers run at EL 10, between the pedestal legs and the column lines (9 ft clear below). The run from
  the inlet-chilling plant is at the same level, except where it dips under the road.
- The two stiles are removed. The ground-floor walk to each deck stair is clear, and the operator who stood on
  the stile now walks at grade.
- verify PASS (0 clashes), audit CLEAN, coastal PASS.

### Hydrogen-ready zone K (`h2_ready.py`, `build_model.py`, `verify.py`)
User question: does the hydrogen area mean the GTs are hydrogen-ready, and does a plant need on-site
production? The turbines are hydrogen-capable H-class units, which burn blends of roughly 30-50 % by volume. A
plant does not need its own production: the usual supply is a pipeline from a hub (e.g. ACES Delta at
Intermountain). The base case for the zone is now:
- **H2R receiving station** (fenced, Group B):
  - pipeline riser with an insulating joint and ESD valve, a pig receiver, twin filter / coalescers;
  - a two-run ultrasonic metering skid with a purity analyser shelter;
  - two pressure-reduction trains (slam-shut, monitor, active regulator; no preheater, since hydrogen warms on
    expansion), with relief to the existing vent stack;
  - an N2 purge skid, and an e-house (480 V, UPS, fire & gas / ESD);
  - gas and UV / IR flame detection, lighting and Group B signs.
- **H2T tube-trailer bay**: two trailers, unloading posts with earthing reels, a canopy. Used to commission
  and test the blend before the pipeline is in.
- **H2X reserve pad** for a Phase 2 on-site plant: graded, fenced, with conduit stub-ups and a sign.
  **H2F** is the future T-H2 foundation, where the 230 kV cable from D6 comes up (capped).
- The station feeds the blending skid in the gas yard, which now serves all three GT fuel branches.
- The 25 MW electrolysis complex (sheet 14) and its routes move to the alternative layers OPT_H2E /
  OPT_H2E_ROUTES. These are excluded from the "all" views. View O5H shows them, and verify skips clashes
  between the two alternatives.
- Cameras E103 (receiving station) and E104 (zone overview). verify PASS (0 clashes), audit CLEAN, coastal PASS.
- **Revised the same day:** shown as the default, the receiving station left the zone looking empty. The 25 MW
  on-site electrolysis complex (sheet 14) is the base case again. This is a real precedent: FPL Cavendish is
  built at the Okeechobee plant, and it is the stronger cable showcase (rectifier DC cables, the 230 kV feed,
  Group B areas). Pipeline supply (receiving station, tube-trailer bay, reserve pad, future T-H2 foundation)
  is the alternative layer OPT_H2P / OPT_H2P_ROUTES, with view O5P. The alternative is excluded from the "all"
  views, and its cameras E103 / E104 add it and hide the electrolysis layers. Both arrangements share the vent
  stack and the blending skid, which serves all three GTs.

### H2 30 blending station (`h2_ready.py`)
User question (screenshot of the gas yard): is this right? The routing was right: hydrogen from the electrolysis
area blends into the plant fuel header. But the blending skid was a placeholder (a frame with two valves) alone in
an empty corner of the gas-yard pad. It is now a fenced Group B blending station in that corner (x 1782-1906,
y 1440-1500):
- **Hydrogen train:** ESD valve, cartridge filter, Coriolis meter, ratio-control valve, check valve.
- **Gas slipstream:** from the fuel header, buried tie and riser, with an ESD valve and an ultrasonic meter.
- **Static mixer:** the blend returns to the header through an MOV, upstream of the GT ESD, with a sample point.
- **Around them:** an H2-concentration / Wobbe analyser shelter, a hydrogen buffer vessel with relief to a local
  30 ft vent stack, an N2 purge rack, a remote-I/O / fire & gas panel, gas and UV / IR flame detectors, a
  light pole and Group B signs.
- The hydrogen supply now ends at the station's east fence. Camera E105. verify PASS (0 clashes), audit CLEAN,
  coastal PASS.

### Electrolyzer hall H2 22 at LOD 3 (`h2_hall.py`)
The building was a solid block. It is now an open hall, with its roof and ridge vents on layer H2_ROOF.
- **Building:** portal frames every 20 ft, insulated walls with a liner, an epoxy floor, LED high-bays, ceiling
  hydrogen detectors at the ridge, and exhaust fans.
- **Five PEM skids:** four stack modules each with end plates, tie rods and DC terminals; H2 and O2 separators,
  a circulation pump and a control cabinet. H2 goes to an overhead header out of the east wall; the O2 vents
  rise through the roof.
- **Five rectifiers** with doors, roof vents and a status strip.
- **DC bus, per unit:** a ladder tray at EL 14 from the rectifier over the aisle to the stack bus bar, carrying
  eight parallel 1/C DC cables (red +, black -) on trapeze hangers.
- **13.8 kV supply:** from the rectifier transformers in covered floor trenches, with conduits up into each
  cabinet.
- **Also inside:** an LV / control room with an MCC lineup and PLC / UPS cabinets, cooling-water headers with
  drops to each skid, and technicians.
- **Outside:** a pipe track under the dry coolers (N2, instrument air, cooling water) and a covered cable trench
  to the dryer and compressors.
- New viewer view O5E (roof off). Cameras E106 (roof off) and E107 (aisle). verify PASS (0 clashes), audit
  CLEAN, coastal PASS.

### Gas yard and pipeline M&R station at LOD 3 (`gas_lod3.py`)
User question: what happened to the gas yard, it looks dull and lost stuff? Nothing was lost: the gas-yard and
M&R equipment has been unchanged for about 100 versions. It was simply the least detailed zone left. This pass:
- **New gas-yard equipment:**
  - final coalescers (2 x 100 %) tied into the GT header;
  - E-202 electric start-up / dew-point heater skid with its SCR power panel;
  - a gas-chromatograph / Wobbe analyser shelter fed by a sample line from the meters;
  - a drains / condensate tank in a bund;
  - the yard's 480 V pad-mount transformer and LV panel.
- **Surface:** crushed-stone gravel (new colour gravel_yard) with a concrete drive from the north gate, a
  turning apron and walkways.
- **Yard furniture, both pads (Class I Div 2 Group D):**
  - chain-link fences, opened wherever pipes cross, with vehicle gates and hazard signs;
  - explosion-proof LED flood poles, fixed gas detectors, wheeled dry-chemical extinguishers and windsocks;
  - instrument JB stands with sealed rigid conduit rising from the buried duct bank (ARMOR-X MC-HL / TC-ER
    in conduit inside the hazardous area).
- **Building dressing:** the gas-yard control enclosure (door, HVAC, conduit bank, sign), the M&R gas-quality
  building (calibration cylinders), the M&R service panel (doors, sunshade), the SCADA antenna mast and the CP
  test station.
- Insulation bands and nameplates on the heater and the filter-separators. Operators and a pickup in each area.
- Everything is placed by a clearance test against the existing parts. Cameras E108 (gas yard) and E109 (M&R).
  verify PASS (0 clashes), audit CLEAN, coastal PASS.
- **Follow-up, visible cable:** the user asked where the cable is in the gas areas. It was all in buried conduit,
  so only the stub-ups showed. Both areas now carry it the other code-compliant way, in tray, per NEC 501.10(B):
  ARMOR-X MC-HL power, TC-ER control, instrument and fire-alarm cable in ladder tray on T-stanchions (EL 9,
  raised where pipes cross).
  - **Gas yard:** the trunk rises at the control enclosure, runs along the south side and up the east side to
    the inlet ESD, with branches to the meters and the compressors.
  - **M&R station:** the trunk runs from the service panel to the heaters and the pig receiver.
  - **Spurs and drops:** spur trays carry drops down to each explosion-proof JB stand and to the start-up heater
    panel, the analyser shelter and the yard transformer.
  - Lighting circuits run in conduit up each flood pole.
  - Camera E110 (cable close-up).
- **Follow-up, tray routing:** the gas-yard trunk followed the pad edge, away from the equipment, and the drops
  weren't visible. Trunk GY-T1 now rises at the control enclosure and runs north between the coalescers and the
  filter-separators. It then runs east down the corridor between the two equipment rows (filter-separators /
  heater and meters / regulation), and north past the start-up heater to the inlet ESD. GY-T2 branches to the
  compressors.
  - Short spurs drop into each JB stand: drop ladders with rungs, armored cable and sealing glands at the JB.
  - Yellow tray ID tags (GY-T1, GY-T2, MR-T1, MR-T2) every 30 ft.
  - E110 is re-aimed down the corridor.

### Cable hero moments for the growth markets (`cable_moments.py`)
User request: a wire-and-cable hero moment for green hydrogen, LNG and the gas meter house yard, like the
turbine-hall and BESS pulls.
- **Green hydrogen (electrolyzer hall):**
  - 2 kV DC 1/C 1000 kcmil (RHW-2 / USE-2) is pulled from a reel on Maxis JAX stands, over a sheave into the
    DC tray of electrolyzer 5.
  - Two electricians on a scissor lift feed it; a reel tender, a supervisor and a gang box are on the floor.
  - Printed legends (POSITIVE / NEGATIVE) on all the DC conductors in the five trays.
  - Viewer story SH2 (roof off); camera E111.
- **LNG:**
  - New visible ladder tray LNG-T1 from the LNG 17 e-house to the send-out pumps, with a riser and a drop to a
    pump JB stand.
  - ARMOR-X MC-HL is paid off an RR-SW45 reel roller over a sheave into the tray; a rope runs to a capstan puller
    with tension monitor and Triggers box at the pump end, with crew.
  - Printed legends on the tray cables. Viewer story SLN; camera E112.
- **Gas meter house (M&R):**
  - An instrument technician terminates PLTC-ER into an open explosion-proof JB at the custody-transfer meter
    run (cover hinged down, terminal rail, fanned conductors).
  - A SIMpull wire wagon feeds the pull from the tray drop.
  - Printed legends on the MR and GY tray cables. Viewer story SMR; camera E113.
- verify PASS (0 clashes), audit CLEAN, coastal PASS.
- **Realism review of the gas-area cable:** the user checked photos of real stations and asked whether the cable trays
  are realistic. They aren't at this scale. Gas yards and M&R stations run control and instrument cable in rigid
  galvanized conduit on Unistrut racks, and ARMOR-X MC-HL power cable exposed on strut; ladder tray belongs to large
  compressor stations, refineries and LNG plants on the main pipe rack.
  - **Gas yard and M&R:** the trays are now conduit banks (2 in rigid conduit with couplings) plus exposed MC-HL on
    strut T-stanchions every 8 ft. Tags read GY-C / MR-C. Each drop to an explosion-proof JB is a rigid conduit
    with an EYS seal, plus an MC-HL drop with a Class I gland, clamped to a strut riser.
  - **LNG:** tray LNG-T1 only along the e-house; MC-HL on strut (LNG-C1) to the send-out pumps.
  - **Electrolyzer DC conductors:** black jackets with red / black polarity tape at both ends (they were bright
    red). The pull reel is black too.
- **Fix, floating conduit racks:** the user found racks floating with dangling ends in the eye-level render. A
  clearance-test bug made every strut post collide with the rack it was meant to hold, so all posts were skipped.
  - Fixed: supports now slide along each span to the nearest clear spot, no more than ~9 ft apart. A run whose
    spans can't all be supported isn't built.
  - A spur is built only if its JB drop also fits.
  - Spurs raised above the trunk to clear pipes now get a vertical step (conduits and MC-HL bent up, with a strut
    bracket).
  - A check script confirms 0 spans over 14 ft unsupported in the gas yard, the M&R and LNG.
  - Rack posts are 4 in galvanized pipe with cap plates on concrete footings, about 10 ft apart; thin strut posts
    read as a forest of wires from eye level.
