# ERock RockBlock campus: public-record research

Compiled 2026-10-26 for a conceptual 3D model.

**How this was gathered:** In this session the egress proxy refused direct fetches of sec.gov, erock.com, interchange.puc.texas.gov, tceq.texas.gov, elpasomatters.org, prnewswire.com and others (CONNECT 403 / DNS failure). Only web search worked. Every quote below is the text a search engine returned for the cited URL. Treat these as **snippet-level quotes that still need checking against the full document**. Nothing here was read from a full document.

---

## 1. ERock S-1/A and 10-Q (Q2 2026)

The two filings you named (S-1/A `000119312526258942` and 10-Q `000119312526346922`) could not be opened. Search results came mostly from the original S-1 (`000119312526227199`), the earlier S-1/A (`000119312526249668`) and IR mirrors of them. The wording in your S-1/A is probably the same but has not been checked.

| Claim | Status | Quote / source |
|---|---|---|
| RockBlock scales in 0.5 MW steps from 1.5 to 3.5 MW | **Confirmed** | "At the core of our power systems is our RockBlock, a modular, distributed generator string that incorporates our proprietary natural gas engine, scales in 0.5 MW increments from 1.5 MW to 3.5 MW per RockBlock and is assembled in-house." Sources: https://www.sec.gov/Archives/edgar/data/0002110029/000119312526227199/d12401ds1.htm and https://www.sec.gov/Archives/edgar/data/2110029/000119312526249668/d12401ds1a.htm |
| Standard unit is 500 kW | **Needs qualifying** | The 500 kW product is the **ERT500**, and 500 kW is its *emergency standby (ESP)* rating. Its prime/long-term rating is **450 kW**: "With 500 kW ESP and 450 kW LTP/PRP in a compact 10' x 8' footprint, the ERT500..." https://www.prnewswire.com/news-releases/enchanted-rock-introduces-ert500-and-rockblock-advanced-onsite-power-generation-technologies-302570774.html. The El Paso (McCloud) PUC filings use **450 kW** per generator (Section 2). The S-1 wording on unit size was not found. |
| Proprietary natural-gas engine | **Confirmed** | Same S-1 sentence as above ("incorporates our proprietary natural gas engine"). |
| Assembled at the Titan facility, Houston | **Partly confirmed** | A search summary of the S-1 says ERock "began assembling its own power systems at Titan in 2025, after previously relying on a third party," and that the S-1/A says all current and future assembly facilities are in Houston. https://www.sec.gov/Archives/edgar/data/0002110029/000119312526227199/d12401ds1.htm ; https://www.sec.gov/Archives/edgar/data/2110029/000119312526249668/d12401ds1a.htm. The exact sentence was not retrieved. Titan's address and size were not found. Engine long blocks come from HD Construction Equipment (a Hyundai subsidiary) under a supply deal announced 2026-10-07: https://finance.yahoo.com/energy/articles/erock-hd-construction-equipment-sign-120000562.html |
| Hyperion targets ~1.2 GW/yr of assembly by end of 2026 | **Confirmed (summary level)** | The S-1/A "states a target of roughly 1.2 GW of annual assembly capacity by the end of 2026", and Hyperion assembly is planned for 2H 2026: https://ir.erock.com/sec-filings/all-sec-filings/content/0001193125-26-249668/0001193125-26-249668.pdf. Hyperion is probably the 407,302 sq ft leased building at 18501 Mound Rd, Cypress TX (Prologis Legacy Point), used as an "assembly, production, and testing hub": https://erock.com/newsroom/enchanted-rock-signs-lease-at-prologis-legacy-point-business-park-in-cypress-texas/ ; https://rebusinessonline.com/enchanted-rock-signs-407302-sf-industrial-lease-in-metro-houston/. That link between the name Hyperion and the Cypress building is **an inference, not stated** in any source. |
| ~1,059 MW installed as of 2026-03-31 | **Confirmed** | S-1 table: installed base 1,059 MW at 2026-03-31, against 934 MW a year earlier (+13.4%) and 1,020 MW at 2025-12-31. https://www.sec.gov/Archives/edgar/data/0002110029/000119312526227199/d12401ds1.htm. **Update from the 10-Q:** "Installed Base in Megawatts \| 1,104 \| 979 \| 126 \| 12.8%" (2026-06-30). https://www.sec.gov/Archives/edgar/data/0002110029/000119312526346922/eroc-20260630.htm |
| ~2,000 units across ~400 sites | **Confirmed** | "over 2,000 deployed units across approximately 400 operational sites". https://www.sec.gov/Archives/edgar/data/0002110029/000119312526227199/d12401ds1.htm. That works out to about 0.5 MW per unit on average. |
| Contracted backlog ~$1.28B | **Confirmed as of 2026-03-31, superseded** | About $1.276B as of 2026-03-31, per S-1 coverage: https://energycapitalhtx.com/erock-microgrid-files-ipo. **The 10-Q (2026-06-30) says:** "Contracted Power System Sales Backlog as of June 30, 2026 was approximately $1.7 billion ... driven by new contracts with data center customers". https://www.sec.gov/Archives/edgar/data/0002110029/000119312526346922/eroc-20260630.htm |
| Named customers: Microsoft, Wistron, Foxconn, Entergy, ComEd | **Confirmed** | S-1 coverage lists "Microsoft, Wistron, Foxconn, Entergy, ComEd, H-E-B, and Walmart". Microsoft is described as a 63 MW resiliency system in San Jose, and Entergy as a white-label utility partner. https://www.tradingview.com/news/tradingview:33b1b28e5f289:0-erock-vertically-integrated-provider-of-distributed-natural-gas-power-systems-and-services-files-for-nyse-600m-ipo/ ; https://www.sec.gov/Archives/edgar/data/0002110029/000119312526227199/d12401ds1.htm. The Q2 2026 results release also names a 470 MW Anthropic order: https://ir.erock.com/news-events/press-releases/detail/135/erock-reports-second-quarter-2026-results |

### RockBlock configuration details in public sources
- **Output voltage:** 480 V. The product page says "drop-in diesel replacement at 480 V — no electrical infrastructure changes required" (https://erock.com/rock-block/). The press release says "The system integrates with 480V infrastructure, requiring no changes to existing infrastructure." (https://www.prnewswire.com/news-releases/enchanted-rock-introduces-ert500-and-rockblock-advanced-onsite-power-generation-technologies-302570774.html)
- **Footprint:** "as little as 448 sqft for a 2.5 MW unit compared to 846 sqft for the same size diesel system" (https://erock.com/rock-block/). The S-1/A also claims a footprint about half that of comparable gas units (https://www.sec.gov/Archives/edgar/data/0002110029/000119312526249668/d12401ds1a.htm, summary level).
- **Redundancy and emissions variants:** "available from 1.5 to 3.5 MW with standard one-for-one diesel replacement capability and optional N+1 redundancy" (press release above). Units come with "Standard Low Emissions or CARB Ultra-Clean Emissions as well as an optional Reliability+" (https://enchantedrock.com/rock-block-brochures/). There is also "an advanced, CARB-compliant ultra-clean model so facilities can maximize runtime without triggering Title V air permits" (https://erock.com/rock-block/). The emissions-control hardware (catalyst or SCR) is **not described**.
- **Controls and monitoring:** a "24/7 staffed remote monitoring microgrid control center" and "Granite", proprietary software embedded in the power systems (S-1/A, summary level: https://www.sec.gov/Archives/edgar/data/0002110029/000119312526249668/d12401ds1a.htm).
- **Not found in any public source:** the step-up transformer rating, switchgear, a 13.8 kV or 34.5 kV collection voltage, grounding, enclosure dimensions or weights.

---

## 2. El Paso campus: El Paso Electric "McCloud Generation" facility for the Meta data center

- **Owner and roles:** El Paso Electric (EPE) owns the plant and the land. "Enchanted Rock LLC will build, operate, and maintain the McCloud generation facilities." Enchanted Rock became EPC under a Limited Notice to Proceed signed in September 2025. PUCT Docket **59076** (SOAH 473-26-14758): https://interchange.puc.texas.gov/Documents/59076_61_1600762.PDF ; docket index: https://interchange.puc.texas.gov/search/filings/?UtilityType=E&ControlNumber=59076&DocumentType=ALL&SortBy=ItemType&SortOrder=Ascending
- **Total capacity:** "a 366-megawatt natural gas generation facility" (Docket 59076 filings, e.g. https://interchange.puc.texas.gov/Documents/59076_41_1585189.PDF)
- **Unit count and rating:** "813 modular natural gas generators rated 450 kilowatts each, totaling 366 megawatts" (https://thefilament.news/tech/mccloud-has-813-gas-units-where-epe-promised-solar ; https://elpasomatters.org/2026/01/18/el-paso-electric-meta-data-center-new-473-million-natural-gas-power-plant/). The arithmetic checks: 813 x 0.45 MW = 365.85 MW.
- **Layout (most useful for the 3D model):** Docket 59076 describes the generators as "installed in clusters of 4 or 5 each, known as RockBlocks, then connected to a step-up transformer and circuit breaker", with roughly **168 rows** of generators. Sources: Preliminary Order of 2026-03-12 and Commission Staff filings, https://interchange.puc.texas.gov/Documents/59076_61_1600762.PDF and https://interchange.puc.texas.gov/Documents/59076_115_1649044.PDF. These are search-snippet paraphrases; the exact wording and which item says which still need checking. As a consistency check, 4–5 x 450 kW = 1.8–2.25 MW per RockBlock. 168 blocks would hold 672–840 units, which brackets 813 (for example 141 blocks of 5 plus 27 blocks of 4 = 813). That decomposition is arithmetic, **not a sourced fact**.
- **Site:** "a 31-acre site next to the Meta data center in Northeast El Paso" (https://elpasomatters.org/2026/01/18/el-paso-electric-meta-data-center-new-473-million-natural-gas-power-plant/). An unverified secondary source describes the wider campus as having "three switching stations, six substations on 1,039 acres" (https://measuredai.substack.com/p/meta-blackrock-el-paso-data-centers).
- **Interconnection:** For a bridge period of up to 5 years the plant runs as an island, connected to the data center but not to EPE's transmission system. It connects to the grid later, once the transmission build-out is done (https://elpasomatters.org/2026/03/29/meta-data-center-el-paso-10-billion-expansion-water-gas-electricity-usage/ ; https://finance.yahoo.com/news/el-paso-electric-proposes-473-203558530.html). A "McCloud Substation" is mentioned in the docket, but its kV is **not found**. 345 kV lines are mentioned only in a secondary source (measuredai substack, above).
- **Schedule:** In-service target is 2027, with construction expected to finish around May 2027 (https://microgridsnow.com/texas-enchanted-rock-meta-bridge-to-power/). Data-center groundbreaking was October 2025 (https://cleanview.co/reports/behind-the-meter-data-centers/full-report/meta-el-paso). The SOAH ALJs' proposal for decision recommends approval with conditions, and a PUCT decision was expected in December 2026 (https://insideclimatenews.org/news/24092026/el-paso-electric-only-considered-gas-to-power-meta-data-center/ ; https://kfoxtv.com/news/local/key-hearing-begins-on-el-paso-electric-gas-plant-proposal-for-meta-data-center).
- **Renderings:** not found.

---

## 3. TCEQ air permit (McCloud, El Paso)

- Inside Climate News reports EPE "has already obtained a TCEQ air permit for the McCloud facility" (https://insideclimatenews.org/news/24092026/el-paso-electric-only-considered-gas-to-power-meta-data-center/). A secondary source says it was a TCEQ standard permit obtained in October 2025 (https://measuredai.substack.com/p/meta-blackrock-el-paso-data-centers, unverified). In a PUC discovery request the City of El Paso asked EPE for the permit type, number and dates (Docket 59076, https://interchange.puc.texas.gov/Documents/59076_89_1623454.PDF).
- **Not found:** the permit or registration number, engine make and model, kW/bhp per engine, stack height and diameter, enclosure dimensions, and hour limits.
- **Regulatory context, not specific to McCloud:** TCEQ's non-rule standard permit for natural-gas spark-ignited engine EGUs (effective 2025-01-30) is reported to set a **minimum stack height of 25 ft per engine** (https://www.tceq.texas.gov/downloads/permitting/air/announcements/2024-005-oth-nr-ngegusp24-std-pmt-final-prop5.pdf/@@download/file/2024-005-oth-nr-ngegusp24-std-pmt-final-prop5.pdf). The search result flagged one version of this document as a draft.
- **Analogous ERock filings, not El Paso:**
  - An Enchanted Rock EGU standard-permit registration (Standard Permit 6005) for an H-E-B site in Manor, Travis County, calculated an effective stack height of 17.66 ft for one unit: https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&dID=8191695&Rendition=Web
  - Caprock Ranch Energy Facility, Midland County. ERock applied for permit 184626 / PSDTX1714 / GHGPSDTX277 on 2026-07-08, for "3,428 internal combustion engines capable of generating up to 1,543 megawatts". That works out to about 450 kW each. NORI: https://ukozvhzgrcnkcatjqfoo.supabase.co/storage/v1/object/public/03-00-air-construction/2026.07.14_Caprock_Ranch_Energy_Facility_184626,_PSDTX1714,_GHGPSDTX277_NORI_b1b6db8e ; news: https://news.oilandgaswatch.org/template/brief/west-texas-ranch-could-host-over-3-400-gas-fired-engines-for-power-project

---

## 4. ERock 500 kW unit (ERT500) datasheet and GCB

- **Ratings and footprint:** "500 kW ESP and 450 kW LTP/PRP in a compact 10' x 8' footprint" (https://www.prnewswire.com/news-releases/enchanted-rock-introduces-ert500-and-rockblock-advanced-onsite-power-generation-technologies-302570774.html ; https://enchantedrock.com/ert-500/)
- **Fuel:** natural gas, RNG or propane. **Performance:** ISO 8528-5 G3 step-load capability and <70 dBA (https://enchantedrock.com/ert-500/, marketing claims).
- **Output voltage:** 480 V integration is stated at the system level (press release above). No datasheet confirmation was retrieved.
- **Spec sheet:** a page exists at https://erock.com/ert500-spec-sheet/, but its contents (height, weight, voltage) were not retrieved.
- **GCB / "generator collector box":** **No public reference found.** The only public layout description is the Docket 59076 description in Section 2 (4–5 generators per RockBlock, each RockBlock to a step-up transformer and circuit breaker).

---

## Not found
- Exact quotes from S-1/A `000119312526258942` and 10-Q `000119312526346922`. Both could not be fetched; the quotes above come from search snippets of related filings.
- Titan facility address and size.
- RockBlock / ERT500 enclosure height, weight, and length and width beyond 10' x 8'.
- Step-up transformer kVA and voltage ratio, switchgear type, and collection voltage (13.8 or 34.5 kV are not stated anywhere found).
- Microgrid controller hardware, grounding design, and emissions-control hardware (catalyst or SCR).
- McCloud: substation or interconnection kV, renderings, detailed site plan.
- McCloud TCEQ permit number, engine make and model, bhp, stack height and diameter, operating-hour limits.
- Any public "GCB" or collector-box description.
