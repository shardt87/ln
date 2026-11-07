# HRSG / boiler section: reference drawings, one-lines and cable specification requirements

These references are for the boiler slides. Search date: Oct 22, 2026.

The container's network policy blocks downloads from these sites, so this sheet only lists the links. To keep a copy, open
each link and save the PDF here. Use the file names suggested in brackets.

Everything here is public, and none of it is engineered for SW-3X1. The summaries come from search-result
extracts, not a full read, so check them against the documents.

## 1. One-line diagrams (real plants)

| Document | What is in it | Link |
|---|---|---|
| **Mill Creek Unit 6 NGCC (LG&E / KU), Kentucky PSC case 2025-00045, Joint Application Exhibit 2** [`millcreek6_one_line.pdf`] | **Best match.** Drawing 6MP-E1101, "Combined Cycle Generation Program, Mill Creek Unit 6, Overall One-Line Diagram". It shows **HRSG MCC 1A / 1B** next to the CT and ST essential MCCs, the common BOP MCC and the water-treatment MCCs. These are fed from **480 V switchgear** through **2,500 / 3,300 kVA 6.9 kV / 480 V** transformers. This is the same structure as our SWGR-13.8-1 → T-R2A → LC-R2A → MCC-R2A, except their MV bus is 6.9 kV (ours is 13.8 kV). | https://psc.ky.gov/pscecf/2025-00045/rick.lovekamp@lge-ku.com/02282025010202/06-Joint_Application_Exhibit_2_-_Mill_Creek_NGCC.pdf |
| Fox North Energy Center (We Energies), Wisconsin PSC engineering plan | A combined-cycle CPCN-type engineering plan. Check its exhibit list for a single-line. | https://fox11online.com/resources/pdf/b33712bc-8fe9-4d9f-8f8d-8900dfc4684d-FoxNorthEnergyCenter.PDF |
| Wisconsin "Natural Gas Engineering Plan" (2026) | Has a combined-cycle process figure, with arrangement schematics in Exhibit 2. | https://www.wpr.org/wp-content/uploads/2026/09/Natural-Gas-Engineering-Plan.pdf |
| Kondapalli 355 MW CCPP, electrical design basis report (Scribd) | An auxiliary power system description and ratings for the generators, transformers and switchgear. Indian practice (IEC). | https://www.scribd.com/document/156434967/Dbr-Elec-Ccpp |

## 2. HRSG / duct burner scope and requirements

| Document | What is in it | Link |
|---|---|---|
| E.ON Kemsley CHP, "Specification for HRSG package" (UK Environment Agency consultation) [`hrsg_package_spec.pdf`] | A real HRSG purchase specification. It covers the natural-gas supplementary firing system, fail-safe flame detection that trips the burners, the gas emergency shut-off and fuel-gas pressure control. Use it to see the HRSG vendor's scope versus the EPC's electrical / C&I scope. | https://consult.environment-agency.gov.uk/psc/me10-2td-e-on-uk-chp-limited/supporting_documents/SPECIFICATION%20FOR%20HRSG%20PACKAGE.pdf |
| NYC Buildings Bulletin 2015-011 (cogeneration with HRSG) | Fuel-gas skid and related HRSG equipment must suit a **Class I Division 2** environment (NYC Electrical Code 500.5). Duct burners must be tested to **UL 295**. | https://www.nyc.gov/assets/buildings/bldgs_bulletins/bb_2015-011.pdf |
| NYC Buildings Bulletin 2012-002 | Duct-burner field safety-trip tests: failure to light, safety shut-off valve (SSOV) failure, pilot failure. | https://www.nyc.gov/assets/buildings/bldgs_bulletins/bb_2012-002.pdf |

## 3. Cable specifications (sample owner / guide specs)

These are institutional Division 26 specs, not power-plant specs. They do carry the same MV cable requirements an EPC
writes for a combined-cycle plant.

| Document | Key requirements | Link |
|---|---|---|
| University of Michigan DG 26 05 13, MV cable | 1/C stranded Cu, **EPR 15 kV, 90 °C, 133 % insulation level**, tape shield, PVC jacket. | https://umaec.umich.edu/desguide/tech/26/DG260513.pdf |
| Northwestern Univ. 26 05 13, MV cables | The same family of requirements. | https://northwestern.edu/facilities/docs/construction/design_guidelines/26_electrical/NU_26%200513%20-%20MED-VOLT%20CABLES.pdf |
| Univ. of Kentucky, MV cable standard | 1/C Cu 15 kV shielded EPR, jacketed. | https://uky.edu/cpmd/download/file/fid/80672 |
| Wisconsin DOA master spec 26 05 13 (.docx) | **NETA ATS** acceptance testing, test voltages for 5 kV / 15 kV cable, and UL MV-105 labelling. | https://doa.wi.gov/DFDM_Documents/MasterSpecs/Electrical/260513.docx |
| LAWA (Los Angeles airports) guide spec | 5, 8, 15 and 35 kV ratings; EPR at 133 %; compact-stranded Cu; metal-tape shield. | https://www.lawa.org/media/12505 |
| Southwire SPEC 42350, thermocouple extension cable | Multi-pair PVC, conductors to **ANSI MC96.1 / ASTM E230**, Al/Mylar overall shield with drain, **UL PLTC**. | https://cabletechsupport.southwire.com/cablespec/download_spec/?spec=42350 |
| Southwire SPEC 42345, thermocouple extension (on the offering slide) | | https://cabletechsupport.southwire.com/en/cablespec/download_spec/?spec=42345 |

The other Southwire product pages are on the offering slide (renders/deck/boilers/talking_points.md).

## 4. Standards an HRSG cable specification calls up

Standard industry references; buy them from IEEE / ICEA / NFPA / UL.

| Cable / topic | Standards |
|---|---|
| Raceway and cable design for generating stations | **IEEE 422** (the 1986 guide covered generating-station cable systems; the 2012 edition covers raceway design; a revision is under way), IEEE 525 for substations |
| MV power (MV-105, 5-35 kV) | ICEA S-93-639 / NEMA WC 74, UL 1072, IEEE 48 (terminations), IEEE 404 (splices), IEEE 400 / 400.2 (VLF field testing), NETA ATS |
| 600 V power, control (TC-ER) | ICEA S-73-532 / NEMA WC 57 (control, thermocouple extension and instrumentation), ICEA S-95-658 / NEMA WC 70 (power), UL 1277 (Type TC, TC-ER), UL 44 (XHHW-2) |
| Armored (ARMOR-X MC-HL) | UL 1569 (MC), UL 2225 (hazardous locations), NEC Art. 330, NEC 501.10 for Class I Div 2 wiring methods |
| Instrumentation / thermocouple extension | ICEA S-73-532, UL 13 (PLTC), NEC Art. 725; ANSI MC96.1 / ASTM E230 for thermocouple alloy and colour code; individually shielded twisted pairs for 4-20 mA, RTD and thermocouple signals |
| Flame propagation (cable tray) | **IEEE 1202** (70,000 Btu/h tray flame test) or IEEE 383; UL 1685 (vertical-tray fire test) |
| Fire alarm | NEC Art. 760 (FPLR / FPLP), NFPA 72 |
| Duct burner / boiler BMS | **NFPA 85** (Boiler and Combustion Systems Hazards Code; HRSG and duct burners are covered in its HRSG chapter), UL 295, NFPA 54 / 56 for fuel gas |
| Hazardous areas | NEC Art. 500 / 501, API RP 500, NFPA 497 (area classification) |
| Station grounding | IEEE 80, IEEE 665 (generating-station grounding) |

## 5. How SW-3X1 lines up with the Mill Creek one-line

| Level | Mill Creek Unit 6 (filing) | SW-3X1 model |
|---|---|---|
| MV auxiliary bus | 6.9 kV | 13.8 kV (SWGR-13.8-1, fed by UAT-1) |
| 480 V source | 2,500 / 3,300 kVA 6.9 kV / 480 V transformers → 480 V switchgear | T-R2A 2,500 kVA 13.8 / 0.48 kV → LC-R2A |
| HRSG MCCs | HRSG MCC 1A / 1B | MCC-R2A-1 / -2 in e-house R2A |

Talking point: the model's structure matches a real utility combined-cycle one-line. Most plants with a 6.9 or 4.16 kV
auxiliary bus put the boiler-feed-pump motors on it, so check the voltage for each project.
