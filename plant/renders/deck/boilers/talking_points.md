# Boilers: greenfield and brownfield talking points

Notes for the boiler slides (SW-3X1_boilers.pdf). The equipment in the model and on the slides is generic. Company names appear only in these notes.

## Who builds what (check the latest before each meeting)

- **Vogt Power International** is a Babcock Power company. Note that Babcock Power is not Babcock & Wilcox. Vogt designs and supplies HRSGs, the heat-recovery boilers behind gas turbines. It also does HRSG retrofits and replacement parts, such as tube modules (harps), economizers and duct burners.
- **Babcock & Wilcox (B&W)** builds utility and industrial boilers, including package boilers for gas firing. It also supplies HRSGs and environmental equipment such as SCR. Its aftermarket business covers retrofits, upgrades and fuel conversions, such as coal-to-gas.
- Other HRSG names you may meet on the same projects include Nooter/Eriksen and NEM.

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
