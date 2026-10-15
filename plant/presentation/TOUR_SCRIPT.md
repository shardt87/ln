# Inside Power Generation: 3D Gas Power Campus Tour

**Teams session, November 11 · 60 minutes · Southwire internal**
Draft 1 of the run of show and the tour script, for review. The tour follows the power: from the gas turbine
to the 230 kV grid, then the auxiliary system that keeps the plant running, then the controls, the hazardous
areas and the adjacent markets. Every stop answers three questions: **what is this equipment, which electrical
system is it part of, and which cable does it use and why.**

> Basis (say it on slide 2): SK-3X1 is a *typical* 3x1 H-class combined-cycle campus built from a 15-sheet
> concept drawing set (Rev 14). Equipment, ratings and cable selections are typical for the class, not
> engineered for a project. Cable quantities come from the model's cable schedule (5,701 runs), routed along
> the modelled trays and duct banks.

Numbers marked **[check]** should be confirmed by a subject-matter engineer before the session.

---

## Run of show

| Time | Segment | Medium | Source |
|---|---|---|---|
| 0:00 to 0:03 | Welcome, why this matters, the basis disclaimer | PowerPoint | New title slide + hero-shots slide |
| 0:03 to 0:15 | Power generation fundamentals and the market landscape | PowerPoint | Extracted from the Wesco deck, market numbers re-dated to 2026 |
| 0:15 to 0:20 | The campus at a glance: 16 zones, the one-line in one slide | PowerPoint | Campus aerial (E123), 16-zone slide, simplified one-line |
| 0:20 to 0:50 | **The tour: 8 stops** | Tour clips in PowerPoint, narrated live | Recorded from the viewer's tour mode |
| 0:50 to 1:00 | Live model and Q&A | Teams screen share, browser | The 3D viewer |

Backup: the full tour as one MP4 and the deck as PDF, open on the laptop before the call starts.

---

## The tour: 8 stops, about 3.5 minutes each

### Stop 1. Gas turbine to generator to the step-up transformer *(the power path)*
- **See:** GT1 on the turbine deck (E22), then the isolated-phase bus from the generator terminals through the
  generator circuit breaker to the GSU (E24).
- **Say:** an H-class GT drives a hydrogen-cooled generator at about 21 kV **[check]**. Generator current is
  tens of thousands of amps, so it leaves on isolated-phase bus, not cable. The GCB lets the unit sync and trip
  without touching the 230 kV yard. The GSU steps up to 230 kV.
- **Cable here:** none on the main path (bus duct). Cable starts at the taps: unit auxiliary transformer
  feeders and the excitation system.
- **Point for engineers:** where bus duct beats cable is decided by current and fault duty. The model's
  schedule lists 5 runs it treats as bus duct (IPB, MOD-EH ties, the ACC VFD secondaries).

### Stop 2. The 230 kV switchyard and the HV cable
- **See:** the breaker-and-a-half yard from the GSUs (E19 / E20), then the 230 kV XLPE termination (E60).
- **Say:** breaker-and-a-half: every circuit sits between two breakers, so one breaker can be maintained
  without an outage. Lines leave on overhead conductor (ACSR) to the utility.
- **Cable here:** **HV XLPE 230 kV, 1/C 2500 kcmil Cu, Cu wire shield, Al laminate sheath** (6 runs, about
  3.5 miles), on cleated risers to sealing ends with surge arresters and a bonding link box.
- **Point for engineers:** sheath bonding (single-point vs cross-bonded) and why the link box is there.

### Stop 3. Auxiliary power: 13.8 kV, 4.16 kV and 480 V
- **See:** R1 switchgear room (E82), MCCs and P&C panels (E83), the R4 VFD e-house (E84).
- **Say:** the plant consumes its own power: boiler feed pumps at 13.8 kV direct-on-line, 4.16 kV motors,
  480 V MCCs, and 80 ACC fans on VFDs. Unit auxiliary transformers feed the 13.8 kV bus; the station steps
  down from there.
- **Cable here:**
  - **MV-105 15 kV** 1/C Cu EPR 133 %, triplexed (about 55 miles), and **MV-105 5 kV**
  - **Type TC-ER 600 V** power, 3/C XHHW-2 + ground (about 170 miles)
  - **VFD cable** with 3 symmetrical grounds and overall shield (174 runs, about 19 miles) to the ACC fans
- **Point for engineers:** why VFD cable (common-mode current, reflected wave), why 133 % insulation level on
  MV (ungrounded / high-resistance grounded systems) **[check]**.

### Stop 4. The cable trays: turbine hall and the R1 tray
- **See:** E71 (ARMOR-X and MV-105 in the R1 tray, HRSG 1 ahead), E67 / E70 (the legends on every jacket).
- **Say:** this is where cable lives most of its life. Ladder tray, separated by voltage class, with drops to
  every skid.
- **Cable here:** **ARMOR-X MC-HL** (continuous corrugated aluminium armor) and **MV-105**, with the print
  legend readable on the jacket.
- **Point for engineers:** tray fill, segregation of power from instrumentation, and why the jacket legend
  matters for inspection.

### Stop 5. HRSG, controls and the control room
- **See:** HRSG 1 west side tray to the marshalling box (E100), then the control room (E86 / E87).
- **Say:** hundreds of transmitters, valves and thermocouples per HRSG, marshalled locally and home-run to
  the DCS.
- **Cable here** (the largest quantities on the campus):
  - **Instrumentation PLTC / TC-ER**, #18 twisted shielded pairs: about **375 miles**, the single largest family
  - **Control TC-ER #14**: about 160 miles
  - **Thermocouple extension (KX)**, **RTD triads**, **single-mode armored fibre**
  - **FPLR fire alarm** (red jacket, NEC 760)
- **Point for engineers:** by length, a combined-cycle plant is mostly an instrumentation-cable job.

### Stop 6. Hazardous areas: fuel gas and LNG
- **See:** the gas yard conduit rack and exposed MC-HL on strut (E110 / P110), the LNG cable pull with the
  roof entry into the e-house (E112 / E122).
- **Say:** fuel gas makes these Class I Div 1 and Div 2 areas. The choice is rigid conduit with seals, or
  MC-HL listed for exposed runs.
- **Cable here:** **ARMOR-X MC-HL** power and control (about 60 miles together), **ITC / PLTC intrinsically safe**
  (blue jacket), Class I glands and EYS seals at every entry.
- **Live install moment:** the ARMOR-X reel on a reel roller, over the sheave, to the capstan (E112).

### Stop 7. Modular power, BESS and behind-the-meter
- **See:** the modular yard (E117), the RICE hall and SCR stacks (E14), the BESS aisle and PCS skid (E41 / E62),
  the BTM data-centre campus.
- **Say:** fast-start engines, aeroderivatives and fuel cells sit beside the combined cycle. A 40 MW / 80 MWh
  BESS rides through load steps from AI training loads at the data centre.
- **Cable here:** **MV-105 35 kV Al** collector circuits (BESS), **2 kV DC** (PV / RHW-2), **Type W** and
  **SHD-GC** portable cable with cam-locks on the portable pad, and the SIMpull reel logistics (E58 / E64).
- **Point for engineers:** collector cable sizing and the 2 kV DC rating.

### Stop 8. Carbon capture and hydrogen: where demand is heading
- **See:** the absorbers (E118), CCS T-1 / T-2 230 kV terminations (E57), the electrolyzer hall DC trays (E106).
- **Say:** carbon capture adds a large electrical load (16 MW class booster fans per train, CO2 compression);
  green hydrogen adds DC bus work at the electrolyzers.
- **Cable here:** MV-105 to large drives, HV cable to the CCS transformers, DC conductors in tray to the
  PEM stacks.
- **Close:** about **1,100+ miles of cable** on one campus **[check: exact total from the workbook]**, and
  most of it is instrumentation and control.

---

## The live 10 minutes (Teams screen share)

1. Open the viewer **before** the call, in Chrome or Edge, on the laptop on wired network. Share the browser
   window, not the whole screen.
2. Orbit the campus once, then "Cable X-ray" to show every tray route at once.
3. Take questions as "show me": click a piece of equipment to show its tag and description.
4. If the share stutters: switch back to the MP4, no apology needed.

## Open items

- [ ] Wesco deck .pptx (Stephan to upload): fundamentals and market slides to extract and re-date.
- [ ] SME reviewer named; review pass on the **[check]** items and the cable family per application.
- [ ] Tour mode in the viewer (Next / Back through the 8 stops, captions, cable highlight); recorded to MP4.
- [ ] Simplified one-line slide (generator to grid, plus the auxiliary system).
- [ ] Two dry runs on Teams, one with a remote viewer.
