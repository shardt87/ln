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

All renders were extracted from the presentation's media and compressed (JPEG, progressive). No image was generated, regenerated or altered beyond cropping to frame and compression.

| Asset (package path) | Source in deck | Used for |
|---|---|---|
| `assets/hall-interior.jpg` (1600 × 900) | Slide 12, `image13.jpg`, "Inside the enclosed hall" | Hero still and video poster; PDF cover |
| `assets/plant-zones.jpg` (2000 × 1125) | Slides 8–9, `image10.png`, the numbered zone render | Interactive plant map; PDF application map. Pin positions computed from the slide's own zone-location shapes. |
| `assets/xray-plant.jpg` (1558 × 959) | Slide 10, `image11.png`, full-plant cable X-ray | Electrical-tour film poster; appendix cover |
| `assets/xray-hall.jpg` (1600 × 900) | Slide 11, `image12.png`, turbine hall X-ray | Cable X-ray film poster |
| `assets/reel-yard.jpg` (1600 × 900) | Slide 29, `image19.jpeg`, reel staging | Execution section; PDF page 6 |
| `assets/plant-scope.jpg` (1600 × 900) | Slide 4, `image7.jpeg`, plant with scope boundary | Kept in the package; not placed in the redesign |
| `assets/cover-plant.jpg` (1800 × 1012) | Slide 1, `image1.jpeg`, isometric plant on white with delivery truck | Applications section (multiplied onto the paper ground) |
| `assets/plant-aerial.jpg`, `assets/plant-core.jpg` | Slides 2 and 5 | Kept in the package for future use |

Not used: cover artwork with the race car (slide 28, off-brief for a customer piece), the state heat-map chart (slide 27, internal), the lifecycle friction infographic (slide 30, superseded by the services section and published case links), the wordmark-on-hex panel (slide 18; its baked-in tagline text conflicts with editable copy).

## Media

| Film | URL (from the email brochure, page 3) | Verified? |
|---|---|---|
| Plant flythrough, 24 s | `…/assets/motion/plant-flythrough.mp4` | **No.** Host blocked from this environment. The hero tries this file and shows the still until the file can play; if it cannot load, the still remains. |
| Cable X-ray, 5 s | `…/assets/motion/turbine-xray.mp4` | No. Linked with poster. |
| Electrical tour, 28 s | `…/assets/motion/electrical-tour.mp4` | No. Linked with poster. |

No 3D model file was supplied, so the plant map uses the original render with accurately placed clickable zones rather than a 3D interaction.

## Typography

The source documents are set in Nimbus Sans / Nimbus Sans Narrow Bold (identified from the embedded fonts of the email brochure PDF; the deck's text runs are predominantly Nimbus Sans with Arial fallback). The first e-brochure reproduced those faces; the September 16 redesign deliberately departs from them to give the piece an editorial, non-templated character while keeping the Southwire wordmark treatment and the copper accent restrained: **Bricolage Grotesque** (display, variable optical size), **Source Sans 3** (text) and **IBM Plex Mono** (reference numbers, labels). All three are open-licence Google Fonts, embedded in the package as WOFF2 (Latin subset) so the e-brochure and PDFs render identically offline. Fallback stack: Helvetica Neue, Arial. If brand governance requires the Nimbus Sans set, `src/fonts` and the two font variables in `src/template.html` and `src/build.py` are the only places to change.

## Product references

53 catalog entries: 29 core references from rev 5 pages 10–13 and 18 (identical to the earlier revision), and 24 expanded families from rev 5 pages 14–17, each transcribed and cross-checked against the page text (every stock token and spec number found). Reference types are labelled in the catalog: product family, specification number, published base code (six-digit codes reproduced as published), request stock code (size and duty selection), orderable stock number, and project-specific selection. Every "Spec · PDF" and "Product page" link is the exact URL from the source PDF's link annotation. Two references have no spec PDF in the source and are labelled as such (66131915 product page only; Genesis family page only); Royal SOOW has a product page only.

Zone decisions (rev 5 pages 8–9), lifecycle options (page 23, including the Re³ repair-kit spec 10911 and codes 67037340 / 67037640), scope boundaries (page 24) and the five-step release package (page 25) are carried verbatim in the e-brochure and the PDFs.

## Case studies

Six cases from email brochure pages 17–18 with their PDF links. Three featured in the main brochure (custom MV cable; AES Ohio rejuvenation; BJC West County installation), three in the resource library. Published results are quoted as the source states them; the "PowerGen application" lines are proposed uses and are labelled as such.

## Contacts

`powergen@southwire.com`, `stephan.hardt@southwire.com` (email brochure page 19). The review call-to-action uses the source's `mailto:` with subject "PowerGen cable package review".

## Link verification

Outbound HTTPS to southwire.com, cabletechsupport.southwire.com and the field-guide host is blocked by this environment's network policy, so **no external link was fetched from here**. Every external URL was taken verbatim from the rev 5 PDF's link annotations and checked for exact match (101 of 101). Rev 5 itself states its references were checked September 2026 by its author. Internal anchors, mailto links and the package's relative links (PDFs, register, change log) were checked in the built page. Recommended before customer distribution: one pass of the 67 links from a networked machine.
