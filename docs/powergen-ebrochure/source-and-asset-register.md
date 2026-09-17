# Source and asset register

PowerGen e-brochure, "Accelerating Time to Power". September 2026.

## Inputs supplied in this session

| # | File | Type | Role | Status |
|---|------|------|------|--------|
| 1 | `PowerGen_101_Accelerating_Time_to_Power_FINAL_EDITED_MSH_5.pptx` (30 slides, 30 MB) | Strategy update presentation, Sept 14 2026 | Authority for positioning, terminology, visual identity and the 16-zone plant model. Source of all plant renders. | **Latest approved presentation.** Slides 3–30 are the internal leadership narrative (market sizing, buyers, path to market, asks); that content is internal and was deliberately **not** carried into the customer e-brochure. |
| 2 | `PowerGen_Email_Brochure.pdf` (19 pages, 960 × 600 pt) | Customer-facing email brochure, earlier revision | Superseded by rev 5 below. Pages 1–7, 10–13 and 18–27 of rev 5 are identical to it. | Superseded; kept for comparison. |
| 2b | `PowerGen_Email_Brochure_5.pdf` (28 pages, 960 × 600 pt) | Customer-facing email brochure, **rev 5** | Authority for the customer narrative, the 16 zone cable packages, zone decisions, the core and expanded cable catalog, lifecycle options, scope boundaries, release package, services, case studies, contacts and every outbound link. Its closing note states it was expanded from the supplied NGCC offering, zone framework, M22 schedule, backbone deck and RFQ, and that linked manufacturer references were checked September 2026 (the author's statement, not verified here). | **Latest approved customer document and most complete technical product reference.** 109 distinct link targets extracted; 101 URLs reused verbatim in this package. |
| 3 | Reference site `powergen-cable-field-guide.shardt87.chatgpt.site` (`#model-studio`) | Online field guide with three model films | Named in the brief and linked from the email brochure. | **Not reachable from this environment** (network policy). Films are linked, not embedded; see Media below. |

Not supplied: cable schedules, drawings, a 3D model file, video files, HTML source of the online guide, manufacturer spec PDFs themselves. The brief lists these as possible inputs; none were attached.

## Assets used

All renders were extracted from the presentation's media and compressed (JPEG, progressive). No image was generated, regenerated or altered beyond cropping to frame and compression. Every image in the package is placed at least once; nothing is a placeholder.

| Asset (package path) | Source in deck | Used for |
|---|---|---|
| `assets/plant-zones.jpg` (2000 × 1125) | Slides 8–9, `image10.png`, the numbered zone render | **The opening view and the plant map.** Sixteen clickable pins; positions computed from the slide's own zone-location shapes (python-pptx), not placed by eye. PDF page 2. |
| `assets/plant-aerial.jpg` (2400 × 1350) | Slide 2 | "Aerial" view of the stage |
| `assets/plant-core.jpg` (2400 × 1350) | Slide 5 | "Power block" view |
| `assets/xray-plant.jpg` (1558 × 959) | Slide 10, `image11.png`, full-plant cable X-ray | "Cable routes" view; electrical-tour film poster; appendix cover |
| `assets/xray-hall.jpg` (1600 × 900) | Slide 11, `image12.png`, turbine hall X-ray | "Turbine hall" view; cable X-ray film poster |
| `assets/hall-interior.jpg` (2000 × 1125) | Slide 12, `image13.jpg`, "Inside the enclosed hall" | "Inside the hall" view; flythrough film poster; email PDF cover |
| `assets/reel-yard.jpg` (1600 × 900) | Slide 29, `image19.jpeg`, reel staging | Execution drawer; PDF page 5 |
| `assets/cover-plant.jpg` (1800 × 1012) | Slide 1, `image1.jpeg`, isometric plant on white with delivery truck | Applications drawer; PDF page 6 |

Not used: cover artwork with the race car (slide 28, off-brief for a customer piece), the state heat-map chart (slide 27, internal), the lifecycle friction infographic (slide 30, superseded by the services section and published case links), the wordmark-on-hex panel (slide 18; its baked-in tagline text conflicts with editable copy), the scope-boundary render (slide 4) and the dark plant render (slide 3), both dropped from this build because each view on the stage must carry something the previous one does not.

## Media

| Film | URL (from the email brochure, page 3) | Verified? |
|---|---|---|
| Plant flythrough, 24 s | `…/assets/motion/plant-flythrough.mp4` | **No.** Host blocked from this environment. Linked from the "Inside the hall" caption and the Applications drawer with its poster; not embedded, so nothing in the page can fail to play. |
| Cable X-ray, 5 s | `…/assets/motion/turbine-xray.mp4` | No. Linked with poster. |
| Electrical tour, 28 s | `…/assets/motion/electrical-tour.mp4` | No. Linked with poster. |

**3D.** No 3D model file was supplied. The stage is therefore built from the original renders with true pan and zoom (pointer drag, wheel, pinch, double-click, HUD buttons) and accurately placed zone pins, not a fake 3D interaction assembled from unrelated stills. The page contains an opt-in model viewer (three.js, GLTF) that activates only if a file named `assets/plant.glb` is present next to the page; with no file, no control, placeholder or message is shown. Export the engineering model to glTF binary and drop it in to get a rotatable model view without any code change.

## Typography

The source documents are set in Nimbus Sans / Nimbus Sans Narrow Bold (identified from the embedded fonts of the email brochure PDF; the deck's text runs are predominantly Nimbus Sans with Arial fallback). This build follows the register of Siemens Energy and GE Vernova product pages, which the reviewer named as the reference: one neutral grotesk in sentence case, large and tightly set for headlines, small and calm for data. **Instrument Sans** (400/500/600/700 and italic) is used for all text and **Geist Mono** (400/500) for stock numbers, spec numbers, zone numbers and labels. Both are open-licence Google Fonts, embedded in the page and PDFs as WOFF2 (Latin subset, 242 KB inlined) so they render identically offline. Fallback stack: Helvetica Neue, Arial. If brand governance requires the Nimbus Sans set, `src/fonts/fonts-inline.css` and the two font variables at the top of `src/template.html` and `src/build.py` are the only places to change.

## Product references

53 catalog entries: 29 core references from rev 5 pages 10–13 and 18 (identical to the earlier revision), and 24 expanded families from rev 5 pages 14–17, each transcribed and cross-checked against the page text (every stock token and spec number found). Reference types are labelled in the catalog: product family, specification number, published base code (six-digit codes reproduced as published), request stock code (size and duty selection), orderable stock number, and project-specific selection. Every "Spec · PDF" and "Product page" link is the exact URL from the source PDF's link annotation. Two references have no spec PDF in the source and are labelled as such (66131915 product page only; Genesis family page only); Royal SOOW has a product page only.

Zone decisions (rev 5 pages 8–9), lifecycle options (page 23, including the Re³ repair-kit spec 10911 and codes 67037340 / 67037640), scope boundaries (page 24) and the five-step release package (page 25) are carried verbatim in the e-brochure and the PDFs.

## Case studies

Six cases from email brochure pages 17–18 with their PDF links. Three featured on email PDF page 7 (custom MV cable; AES Ohio rejuvenation; BJC West County installation), all six in the Cases drawer and the appendix. Published results are quoted as the source states them; the "PowerGen application" lines are proposed uses and are labelled as such.

## Contacts

`powergen@southwire.com`, `stephan.hardt@southwire.com` (email brochure page 19). The review call-to-action uses the source's `mailto:` with subject "PowerGen cable package review".

## Link verification

Outbound HTTPS to southwire.com, cabletechsupport.southwire.com and the field-guide host is blocked by this environment's network policy, so **no external link was fetched from here**. Every external URL was taken verbatim from the rev 5 PDF's link annotations and checked for exact match (101 of 101). Rev 5 itself states its references were checked September 2026 by its author. Internal anchors, mailto links and the package's relative links (PDFs, register, change log) were checked in the built page. Recommended before customer distribution: one pass of the 67 links from a networked machine.
