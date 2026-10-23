# Boilers: greenfield and brownfield talking points

Notes for the boiler slides (SW-3X1_boilers.pdf, 11 slides). The equipment in the model and on the slides is generic. Company names appear only in these notes.

## Who builds what (check the latest before each meeting)

- **Vogt Power International** is a Babcock Power company. Note that Babcock Power is not Babcock & Wilcox. Vogt designs and supplies HRSGs, the heat-recovery boilers behind gas turbines. It also does HRSG retrofits and replacement parts, such as tube modules (harps), economizers and duct burners.
- **Babcock & Wilcox (B&W)** builds utility and industrial boilers, including package boilers for gas firing. It also supplies HRSGs and environmental equipment such as SCR. Its aftermarket business covers retrofits, upgrades and fuel conversions, such as coal-to-gas.
- Other HRSG names you may meet on the same projects include Nooter/Eriksen and NEM.

## How an HRSG works (slide 2)

The temperatures and pressures below are typical ranges for a three-pressure reheat HRSG behind an F-class gas turbine.

- **The idea.** The gas turbine's exhaust leaves at about 1,100 °F. The HRSG passes it over banks of finned tubes and turns that heat into steam for the steam turbine.
  - That steam makes **about a third** of the plant's output with no extra fuel.
  - This is how combined cycle reaches **60 %+ efficiency**, against about 40 % for a gas turbine alone.
- **Gas side, hot to cold:**
  - the duct burner (optional supplementary firing, up to about 1,600 °F);
  - the HP superheater and reheater;
  - the HP evaporator under the HP drum;
  - the SCR and CO catalyst, placed where the gas is in its 600-750 °F window;
  - the HP economizer and IP sections, then the LP evaporator;
  - the condensate preheater;
  - the stack, at about 180 °F.
- **Water side, the other way (counterflow).** The feed pumps push water into the cold end. It passes through the economizers into the drums, circulates through the evaporators, and leaves the superheaters as steam:
  - HP: about 1,800-2,400 psig, ~1,050 °F;
  - reheat / IP: about 400-600 psig, ~1,050 °F;
  - LP: about 50-80 psig.
- **Where cable lands, section by section** (this is the bridge to the rest of the deck):
  - MC-HL and scanner pairs at the duct burner;
  - thermocouple extension for the tube metals in the hot sections;
  - drum-level transmitters on each drum, three per drum and typically voted 2-out-of-3, plus MOVs;
  - VFD cable to the SCR blowers;
  - MV-105 to the feed pumps;
  - CEMS instrumentation and fibre at the stack.
- **Cycling is the wear story.** A modern unit hot-starts in about an hour, and every start heats and cools the thick parts (drums, headers). That's why there are so many tube-metal thermocouples: about 84 thermocouple-extension cables per train in the model.

## The whole cycle: what goes in, what comes out (slide 3)

- **In:** natural gas, air and a little makeup water. **Out:** electricity to the 230 kV grid, stack gas at about 180 °F (CO2 and water vapour, with NOx cut by the SCR), and heat rejected to the air at the condenser.
- **The path:**
  - Three gas turbines burn the gas, each spinning a generator; that's about 2/3 of the output.
  - Their exhaust, at about 1,100 °F, goes through three HRSGs, which make steam.
  - All three HRSGs feed **one** steam turbine, which spins one more generator; that's about 1/3 of the output, with no extra fuel.
- **"Is it still steam after the turbine?"** Yes, but spent. It leaves the steam turbine at about 100-150 °F (an air-cooled condenser runs warmer than a water-cooled one), below atmospheric pressure, and part of it is already water. The air-cooled condenser (80 cells, 80 fans) turns it fully back into water under vacuum.
- **The water loop is closed.** The condensate pumps return the water to the HRSGs' low-pressure end; the feed pumps (13.8 kV, MV-105) take it from the LP drum / deaerator and lift it to HP and IP pressure. HP-turbine exhaust goes back to the HRSGs' reheaters before the IP / LP turbine. Only a little makeup water replaces blowdown.
- **Cable on the loop:**
  - 21 kV isolated-phase bus from the generators to the step-up transformers;
  - MV-105 to the feed pumps;
  - VFD cable to the 80 condenser fans (four 480 V drive lineups in the R4 e-house);
  - instruments on every pump, valve and level.

## The three boiler stories in the model

1. **Greenfield heat-recovery boiler (HRSG 1–3).** A three-pressure HRSG with SCR and a duct burner.
   - One HRSG train in the model's cable schedule is **705 cables, about 156,000 ft**.
   - That train includes its feed pumps, SCR blowers, chemical feed, CEMS and the duct burner.
   - The cable runs:
     - **MV-105 15 kV** to the 13.8 kV feed-pump motors;
     - **TC-ER 600 V** power and VFD cable;
     - **ARMOR-X MC-HL** for the duct-burner gas skid (a Class I Div 2 area);
     - **control TC-ER**;
     - **instrumentation PLTC / TC-ER** and **thermocouple extension**, for drum level, pressures and temperatures.
2. **Gas-fired package boiler (auxiliary boiler AB-1).** This is the plant's start-up and sealing-steam boiler, and the same kind of package sold to industrial sites. It is **83 cables, about 42,000 ft**:
   - TC-ER power and VFD cable for the combustion-air fan motor;
   - burner-management control and flame-scanner cable;
   - ARMOR-X MC-HL to the gas train's valves;
   - instrumentation and fire alarm.
3. **Brownfield module replacement (HRSG 3 outage).** An HP evaporator module is lifted out through the opened roof, and the new module waits on a lowboy. The cable work happens in the same window: SIMpull reels, pre-terminated harnesses landing on the marshalling box, and old cable cut back into recycling.

## Inside the e-house and the full wiring (slides 4 and 5)

- **Slide 4** lifts the roof off R2A, the HRSG 1 e-house. It traces every leg from the transformer to the drops into each section:
  - the 13.8 kV primary (MV-105, 3 cables, 660 ft) into T-R2A;
  - the 480 V secondary (10 sets of 4 x 1/C 500 kcmil XHHW-2, 40 cables, 4,800 ft) over the room to the LC-R2A main breaker;
  - the feeders to the MCCs and VFDs, the drops into every bucket, the marshalling home runs, and the UPS / DC panels;
  - the exits to the field: power through the north-wall transit frame, instruments, thermocouple, fire alarm and fibre through the roof glands.
- **Slide 5** is the one-line. Every number comes from a schedule row:
  - the HRSG 1 train is **705 cables, about 156,000 ft**;
  - feeding the room adds **86 cables, about 12,400 ft**: the T-R2A primary and secondary, the transformer fans, controls and monitoring, the DCS fibre, and the room's own lighting, receptacles and fire-alarm wiring.
  - R2A also serves the GT1 unit, so the feed is shown but not counted in the train.
- The 480 V secondary was missing from the schedule until this pass. It is now in for every unit and load-centre transformer (T-R2A/B/C, T-R3, LCT-A/B). At 10 to 12 parallel sets, it is also a bus-duct candidate; ask the EPC which they carry.

## The electrical system: levels and ratings (slide 6)

All ratings are the model's typical values, not engineered.

- **The levels, top down:**
  - **230 kV:** GSU-1.
  - **21 kV:** the generator and isolated-phase bus. UAT-1 (21 / 13.8 kV, 40 MVA) feeds SWGR-13.8-1 at 1,674 A over 4 sets of 750 kcmil MV-105.
  - **13.8 kV:** SWGR-13.8-1 (1,200 A, 40 kA, arc-resistant) feeds the two 5,000 kW direct-on-line feed pumps (232 A each, 250 kcmil MV-105) and T-R2A (105 A, #2).
  - **480 V:** T-R2A (2,500 kVA, 3,007 A secondary, 40 x 500 kcmil) feeds LC-R2A (4,000 A main, 65 kA), then MCC-R2A-1 / -2 (800 A, 65 kA) and the VFDs.
  - **120 V AC / 125 V DC:** a 10 kVA UPS and a 60-cell battery for the DCS, F&G and breaker control.
  - **Signals:** 4-20 mA, thermocouple millivolts and 24 V DC discretes.
- **Numbers to remember:**
  - **About 750 kW is connected at 480 V on one HRSG train (77 circuits).** The SCR blowers are the big ones, 2 x 110 kW.
  - **About 74 % of the train's cables are instrument or thermocouple pairs.** HRSG cable is mostly signal cable by count, so instrumentation is where the volume is.
  - **Arc flash is 8.4 cal/cm² at 13.8 kV and 24.6 at 480 V** (model labels). The 480 V gear is the higher hazard: a lower voltage, but more current and longer clearing.
- **Real plants vary.** Many plants put the feed pumps on a 4.16 or 6.9 kV bus; Mill Creek 6 uses 6.9 kV. The cable logic is the same.

## What the spec calls for (slide 7)

Public sources are listed in `references/boilers/README.md`. Have the standard numbers ready; boiler and EPC engineers
write their specifications around them.

- **The one-line is real.**
  - The Mill Creek Unit 6 NGCC filing (LG&E / KU, Kentucky PSC case 2025-00045, Exhibit 2, drawing 6MP-E1101) shows dedicated HRSG MCCs 1A / 1B.
  - They are fed from 480 V switchgear through 2,500 / 3,300 kVA 6.9 kV / 480 V transformers. This is the same structure as SW-3X1, which uses 13.8 kV.
  - On the slide this is "a recent US utility filing"; give the name verbally if asked.
- **MV, 15 kV (feed pumps, transformer primaries).**
  - The specification: EPR at 133 % insulation level, tape shield, ICEA S-93-639, UL 1072 MV-105, IEEE 48 terminations, VLF acceptance testing (IEEE 400.2 / NETA).
  - Southwire: MV-105 15 kV, 220 mil NL-EPR 133 %, on SIMpull reels (SPEC 46302).
- **480 V.**
  - The specification: XHHW-2, sized at 125 %, voltage drop of 3 % or less.
  - T-R2A's secondary is 10 parallel sets. Ask whether the EPC carries cable or bus duct; parallel 1/C on SIMpull reels pulls in one pass.
- **TC-ER is the default tray cable.** The "ER" (exposed run) rating lets the cable leave the tray and run to the motor or valve without conduit (NEC 336.10). The specification also calls for the IEEE 1202 / UL 1685 70,000 Btu/h tray flame test.
- **Duct burners bring gas into the HRSG.**
  - The burner skid and valve area is typically Class I Div 2.
  - ARMOR-X MC-HL (UL 1569 + UL 2225) meets Div 2 and also qualifies for Div 1, so one cable covers any classification change.
  - Burner management falls under NFPA 85, the boiler and combustion systems hazards code.
- **VFDs** (SCR blowers, FD fans): a symmetrical three-ground construction plus a shield or continuous armor controls common-mode current and bearing damage. ARMOR-X MC-HL VFD covers this.
- **Instruments.** Individually shielded twisted pairs, 300 V PLTC (UL 13), ICEA S-73-532, kept apart from power in tray.
- **Thermocouple extension.** The alloy must match the thermocouple (type K means KX extension), colour-coded to ANSI MC96.1. It is never copper. An HRSG can carry about 80 of these runs per train.
- **Design guides to name:**
  - IEEE 422 (cable raceway in generating stations);
  - IEEE 80 / 665 (grounding);
  - API RP 500 / NEC 500 (area classification);
  - NETA ATS (field acceptance).

## The message for boiler companies

- **"The outage clock is the cost."** On a replacement or a conversion, cable is on the critical path unless it's staged and pre-terminated before the unit comes down.
- **Stage before the trip.** Cut-to-length reels on SIMpull Cradles and reel rollers, labelled per pull.
- **Pre-terminate.** Factory-made harnesses with QR tags turn terminating into testing during the outage.
- **Pull clean.** SIMpull reels with a sheave at the wall: one crew, no reel jacks, and the pull tension recorded.
- **Conversions** to gas, or new duct burners, add burner management and gas trains in Class I Div 2. That's an ARMOR-X MC-HL scope.
- **One supplier** across greenfield HRSG and package boiler projects and brownfield outages: the same product families, staged and pulled the same way.

## Caveats

- The model is a conceptual illustration, not engineered. Cable counts and footage are typical quantities from the model's cable schedule (see the workbook's Audit sheet).
- Duct-burner and package-boiler device counts are typical for the equipment class, not a specific vendor's design.

## The offering (slide 3): product, SPEC, stock number, link

Stock numbers are one representative catalogue size per product, taken from Southwire's product listings. Every size and construction is on the same SPEC. Confirm current stock with Southwire customer service before quoting.

1. **MV-105 15 kV**: 1/C Cu, 220 mil NL-EPR 133 %, tape shield, SIMpull PVC. Used for Feed-pump motors, 13.8 kV. SPEC 46302, stock # 95604599 (500 kcmil). [Product page](https://southwire.com/wire-cable/medium-voltage-power-cable/1-c-cu-15kv-220-nlepr-133-simpull-pvc-mv-105/p/95604599)
2. **Type TC-ER power**: 3/C Cu XHHW-2 + ground, PVC, 600 V. Used for Fans, pumps, MCC feeders. SPEC 45252, stock # 95305999 (12 AWG 3/C). [Product page](https://www.southwire.com/wire-cable/power-control/cu-600-1000v-xlpe-insulation-pvc-jacket-xhhw-2-ct-rated-sunlight-resistant-for-direct-burial-silicone-free/p/95305999)
3. **ARMOR-X MC-HL**: Cu XLPE XHHW-2, welded armor, PVC, 600 V, Class I Div 2. Used for Gas trains, burner skids. SPEC 45352, stock # 89052799 (8 AWG 4/C). [Product page](https://www.southwire.com/wire-cable/armored-power-cable/4-c-cu-600v-xlpe-xhhw-2-armor-x-pvc-power-cable-with-ground/p/89052799)
4. **ARMOR-X MC-HL VFD**: 3/C Cu XLPE XHHW-2 + ground, VFD rated. Used for FD fan on its drive. SPEC 45352, stock # 89051899 (3/0 3/C). [Product page](https://www.southwire.com/wire-cable/armored-power-cable/3-c-cu-600v-xlpe-xhhw-2-armor-x-pvc-power-cable-with-ground-vfd/p/89051899)
5. **Control TC-ER**: Cu XLPE XHHW-2, 600 V. Used for BMS panels, valves, MOVs. SPEC 45053, stock # 89067701 (14 AWG 5/C). [Product page](https://southwire.com/wire-cable/power-control/spec45053-cu-600v-xlpe-insulation-thermoplastic-cpe-tp-jacket-xhhw-2-ct-rated-sunlight-resistant-for-direct-burial-silicone-free/p/89067701)
6. **Instrumentation PLTC / ITC**: 300 V, shielded pairs + overall shield (SPOS). Used for Flame scanners, drum level, transmitters. SPEC 43303, stock # per pair count. [Product page](https://www.southwire.com/wire-cable/instrumentation/300v-cu-pvc-pairs-pvc-spos-instrumentation/p/SPEC43303)
7. **Thermocouple extension**: PVC, PLTC multi-pair (KX on request), 105 °C. Used for HRSG gas-path and tube temperatures. SPEC 42345, stock # per construction. [Product page](https://cabletechsupport.southwire.com/en/cablespec/download_spec/?spec=42345)
8. **SIMpull Cradle**: for 51 / 61 in SIMpull Reels, one-person payoff. Used for Outage staging and pulls. SPEC SPR-CRDL, stock # 67606001. [Product page](https://www.southwire.com/tools-equipment/material-handling-storage/spr-crdl-simpull-cradle/p/67606001)
