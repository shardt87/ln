// Southwire PG x DC coverage model — working-session deck, SWR-PG-ROE Rev 00
// 12 main slides + 2 appendix, 16:9 LAYOUT_WIDE, native shapes/text only.
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Stephan Hardt";
pres.company = "Southwire";
pres.title = "Power Generation x Data Center — Coverage Model — SWR-PG-ROE Rev 00";

const WHITE = "FFFFFF";
const INK = "1A1D21";
const COPPER = "C67A43";
const MUTE = "6B7075";
const DMUTE = "A6ACB3";
const CARD = "F5F4F2";
const DCARD = "23272C";
const FONT = "Arial";
const TOTAL = 14;

function footer(slide, n, dark) {
  const c = dark ? "8C9299" : "9A9FA4";
  slide.addText("Stephan Hardt · Power Generation Solutions", {
    x: 0.6, y: 7.12, w: 5.5, h: 0.26, fontFace: FONT, fontSize: 8, color: c,
    isTextBox: true, margin: 0, align: "left", valign: "middle",
  });
  slide.addText(`SWR-PG-ROE Rev 00 · Working draft — Southwire internal · slide ${n} of ${TOTAL}`, {
    x: 6.5, y: 7.12, w: 6.23, h: 0.26, fontFace: FONT, fontSize: 8, color: c,
    isTextBox: true, margin: 0, align: "right", valign: "middle",
  });
}

function kicker(slide, text) {
  slide.addText(text, {
    x: 0.6, y: 0.48, w: 12.13, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true,
    color: COPPER, charSpacing: 2, isTextBox: true, margin: 0, align: "left", valign: "middle",
  });
}

function takeaway(slide, text, dark, opts) {
  const o = opts || {};
  slide.addText(text, {
    x: 0.6, y: o.y || 0.84, w: o.w || 12.13, h: o.h || 0.8,
    fontFace: FONT, fontSize: o.size || 30, bold: true,
    color: dark ? WHITE : INK, isTextBox: true, margin: 0, align: "left", valign: "top",
  });
}

function chip(slide, x, y, label, wOverride) {
  const w = wOverride || 0.22 + label.length * 0.078;
  slide.addText(label, {
    shape: pres.ShapeType.roundRect, rectRadius: 0.04,
    x, y, w, h: 0.26, fill: { color: COPPER }, color: WHITE,
    fontFace: FONT, fontSize: 8, bold: true, charSpacing: 1,
    align: "center", valign: "middle", isTextBox: true, margin: 0,
  });
  return w;
}

function dot(slide, x, y) {
  slide.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.09, h: 0.09, fill: { color: COPPER }, line: { type: "none" },
  });
}

// ------------------------------------------------------------- S1 (dark) Opener
{
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(s, "POWER GENERATION × DATA CENTER · WORKING SESSION · MARC HALL / STEPHAN HARDT · THURSDAY 9:00–1:00");
  takeaway(s, "One coordinated face. One owner for every dollar. Execution decides.", true, { size: 31 });
  s.addText("Coverage model, boundary rules and rules of engagement — Version 0, built to be challenged and rewritten in this room before anything goes to Jack. Nothing in it is approved.", {
    x: 0.6, y: 2.02, w: 11.6, h: 0.62, fontFace: FONT, fontSize: 13, color: DMUTE, isTextBox: true, margin: 0, valign: "top",
  });

  s.addText("THREE NON-NEGOTIABLE OUTCOMES FOR TODAY", {
    x: 0.6, y: 2.7, w: 8.0, h: 0.26, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0,
  });
  const outs = [
    ["1", "The one-page definition, signed by Marc and Stephan — asset served plus specification control."],
    ["2", "Tranche 1 — ten accounts with proposed roles, and the evidence request to Tim."],
    ["3", "The six-item ask to Jack, with a meeting date."],
  ];
  const oy = [3.1, 4.25, 5.4];
  for (let i = 0; i < 3; i++) {
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: oy[i], w: 12.13, h: 0.95, fill: { color: DCARD }, line: { type: "none" } });
    s.addText(outs[i][0], { x: 0.9, y: oy[i] + 0.18, w: 0.6, h: 0.6, fontFace: FONT, fontSize: 26, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText(outs[i][1], { x: 1.7, y: oy[i] + 0.18, w: 10.7, h: 0.62, fontFace: FONT, fontSize: 13.5, color: WHITE, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addText("How to read this deck:  [F] known fact · [A] assumption · [R] recommendation · TO SUPPLY = a fact still needed. Challenge the [A]s first — the [R]s depend on them.", {
    x: 0.6, y: 6.6, w: 12.13, h: 0.3, fontFace: FONT, fontSize: 9.5, italic: true, color: DMUTE, isTextBox: true, margin: 0,
  });
  footer(s, 1, true);
  s.addNotes(
    "Frame the session: this is Version 0 — a model to be challenged and rewritten here, then refined by Marc and Stephan before it goes to Jack. The package is built around three things, in order: the customer sees one coordinated Southwire; someone is accountable for every dollar we say we are pursuing; the assignment goes to the team that can actually execute. Session rules from Aug 17: three non-negotiable outcomes and a parking lot with owners.\n[Sources] SWR-PG-ROE Rev 00 §1, §10; Aug 17 and Aug 24 working calls."
  );
}

// ------------------------------------------------------------- S2 (light) Two axes
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "THE STRUCTURAL FIX");
  chip(s, 12.15, 0.48, "[R]", 0.58);
  takeaway(s, "Five labels, two axes. Ownership follows the asset; coverage follows the buyer.", false, { size: 28, h: 0.7 });

  const ax = [
    ["AXIS 1 — ASSET SERVED", "What does the cable physically feed?",
      "Generation asset (up to the POI) · T&D · consuming facility: data center · consuming facility: industrial process",
      "Assigns opportunity ownership"],
    ["AXIS 2 — CUSTOMER TYPE", "Who is buying, and how do they buy?",
      "OEM / packager · owner / developer · EPC / contractor · utility framework · distributor (channel)",
      "Decides coverage method, channel, and who coordinates the account"],
  ];
  const axx = [0.6, 6.75];
  for (let i = 0; i < 2; i++) {
    s.addShape(pres.ShapeType.rect, { x: axx[i], y: 1.95, w: 5.98, h: 3.0, fill: { color: CARD }, line: { type: "none" } });
    s.addText(ax[i][0], { x: axx[i] + 0.25, y: 2.15, w: 5.5, h: 0.28, fontFace: FONT, fontSize: 11, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
    s.addText(ax[i][1], { x: axx[i] + 0.25, y: 2.5, w: 5.5, h: 0.32, fontFace: FONT, fontSize: 13, bold: true, color: INK, isTextBox: true, margin: 0 });
    s.addText(ax[i][2], { x: axx[i] + 0.25, y: 2.95, w: 5.5, h: 0.95, fontFace: FONT, fontSize: 11.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
    s.addText(ax[i][3], { x: axx[i] + 0.25, y: 4.35, w: 5.5, h: 0.45, fontFace: FONT, fontSize: 11, italic: true, color: MUTE, isTextBox: true, margin: 0, valign: "top" });
  }

  s.addText(
    "PG, DC, Industrial and Utility are axis-1 values. OEM is axis-2 — a customer type, not a territory. That is why Powell splits by product line and application, never as a whole company.",
    { x: 0.6, y: 5.35, w: 12.13, h: 0.7, fontFace: FONT, fontSize: 13, color: INK, isTextBox: true, margin: 0, valign: "top" }
  );
  s.addText("Forcing five mutually exclusive boxes is exactly what produces the Powell problem.", {
    x: 0.6, y: 6.1, w: 12.13, h: 0.32, fontFace: FONT, fontSize: 11, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 2, false);
  s.addNotes(
    "The five categories requested are not one taxonomy, and the session should not try to make them one. Power Generation, Data Center, Industrial and Utility describe the asset or end market the cable serves. OEM describes a customer type — a manufacturer that designs Southwire product into its own equipment and buys to a program spec, repeatedly — and it cuts across all four. Ownership is assigned on axis 1; coverage method and the coordinator role are decided on axis 2.\n[Sources] SWR-PG-ROE Rev 00 §2–3; outside-in readout Part A (peers run product/segment structures with data center as a cross-cutting theme)."
  );
}

// ------------------------------------------------------------- S3 (light) Rule hierarchy
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "OWNERSHIP RULES — APPLIED IN ORDER");
  takeaway(s, "Two rules decide most cases. The rest are tie-breakers.", false, { size: 26, h: 0.5 });

  const rows = [
    ["1", "Asset served", "Is the cable feeding a generation asset (to the POI), a consuming facility, or T&D?", "Controls — cannot be overridden by relationship, PO issuer or preference"],
    ["2", "Specification control", "Which buying center writes or approves the spec and makes the selection?", "Controls — the EPC, GC or distributor issuing the PO is a channel, never assigned ownership"],
    ["M", "Mixed scope", "One project holds a generation scope and a facility scope", "Split by scope — one joint plan, one customer face; do not force one owner"],
    ["3", "Documented activity", "Evidence at the opportunity level (four-part standard)", "Tie-break — evidence, never a veto"],
    ["4", "Customer preference", "Written, from the buying center that controls the spec", "Tie-break — decides service model, never moves an opportunity across the Rule-1 line"],
    ["5", "Capability & capacity", "Named resource, product expertise, capacity for what is quoted", "Tie-break — capacity is allocated separately by product management after ownership"],
    ["6", "Strategy strength", "Scored on the six-criterion rubric, in writing, before the meeting", "Last resort — only when Rules 1–2 genuinely split; winner must show execution at 90 days"],
    ["—", "Corporate relationship", "“I have known this guy for ten years.”", "Not a rule — appears only as evidence inside Rules 3 and 4"],
  ];
  const tableRows = rows.map((r) => [
    { text: r[0], options: { bold: true, color: COPPER, align: "center" } },
    { text: r[1], options: { bold: true, color: INK } },
    { text: r[2], options: { color: INK } },
    { text: r[3], options: { color: MUTE } },
  ]);
  s.addTable(tableRows, {
    x: 0.6, y: 1.8, w: 12.13, colW: [0.55, 2.05, 4.55, 4.98], rowH: 0.56,
    fontFace: FONT, fontSize: 9.5, border: { type: "solid", pt: 0.5, color: "E2E2E2" },
    valign: "middle", margin: [0.04, 0.08, 0.04, 0.08],
  });
  s.addText("Settle today: the order of Rules 1–6, and whether strategy strength is a tie-breaker or nothing.", {
    x: 0.6, y: 6.55, w: 12.13, h: 0.3, fontFace: FONT, fontSize: 10.5, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 3, false);
  s.addNotes(
    "Rules 1 and 2 are applied, in order, to every opportunity and settle most cases. Rules 3–6 only exist for a genuine split. On strategy strength: as a primary rule it needs a judge and there is no neutral one below Donna, it rewards presentation over position, and it invites re-litigation every quarter. As a scored tie-breaker with a 90-day execution check it is useful because it forces both teams to write a real plan — best executed strategy keeps the opportunity. Marc's own Aug 24 question — who would be the judge inside Southwire — is the reason it cannot be the rule.\n[Sources] SWR-PG-ROE Rev 00 §4.1, §4.3."
  );
}

// ------------------------------------------------------------- S4 (light) The line
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "THE THREE BOUNDARY STATEMENTS");
  takeaway(s, "The POI is the line. A generator is a generator wherever it sits.", false);

  const bs = [
    ["PG ↔ UTILITY", "[R]",
      "Generator side of the GSU high side / plant switchyard is PG; the grid side is Utility. Transmission built to move a plant's output is Utility infrastructure even when a generation project triggered it."],
    ["PG ↔ DATA CENTER", "[F/R]",
      "Behind-the-meter generation at a data center is PG — stated as asset type, never meter position. The campus electrical from the utility interconnection inward to the rack is DC."],
    ["PG ↔ INDUSTRIAL", "[R]",
      "The test is the purpose of the electron. Produced for sale, export or as a standalone product: PG. Produced and consumed inside the fence to run a process: Industrial, with PG supporting the generation-equipment spec."],
  ];
  const by = [1.95, 3.5, 5.05];
  for (let i = 0; i < 3; i++) {
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: by[i], w: 12.13, h: 1.35, fill: { color: CARD }, line: { type: "none" } });
    s.addText(bs[i][0], { x: 0.9, y: by[i] + 0.16, w: 3.2, h: 0.28, fontFace: FONT, fontSize: 11, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
    chip(s, 11.9, by[i] + 0.14, bs[i][1], 0.62);
    s.addText(bs[i][2], { x: 0.9, y: by[i] + 0.5, w: 11.5, h: 0.75, fontFace: FONT, fontSize: 12, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addText("Say it as asset type or the DC team will read the BTM rule as a territory grab. Front-of-meter / behind-the-meter framing was rejected on Aug 20 — this wording is consistent with that.", {
    x: 0.6, y: 6.55, w: 12.13, h: 0.35, fontFace: FONT, fontSize: 10, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 4, false);
  s.addNotes(
    "These are the two boundary questions asked most, plus the industrial line. Behind-the-meter generation defaulting to PG was agreed in principle on the Aug 24 call — as generation equipment regardless of end user. Two facts settle most industrial cases: does the site export, and is the generation asset owned by a third party (if so, that owner monetizes generation and it is PG). Exception still to decide: a merchant line or a BESS-to-plant tie owned by the generator.\n[Sources] SWR-PG-ROE Rev 00 §3.7; Aug 20 and Aug 24 calls."
  );
}

// ------------------------------------------------------------- S5 (light) Hard cases
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "THE RULES APPLIED TO THE HARD CASES");
  takeaway(s, "Same account, same product — the asset decides, per scope.", false, { size: 26, h: 0.5 });

  const rows = [
    ["Powell switchgear into a gas plant", "PG — Powell engineering controls the spec; an OEM program. The PO may come from a distributor; irrelevant to ownership."],
    ["Powell switchgear inside a data-center campus", "DC — same OEM, different scope. One Powell coordinator, two opportunity leads."],
    ["Enchanted Rock / VoltaGrid generation at data centers", "PG — the asset is a generator regardless of the meter; DC keeps the campus interface. Agreed in principle Aug 24 [F]."],
    ["Hyperscaler buying packaged generators", "PG for the generation scope — their energy team controls the spec, not the facility team DC calls on. DC remains account coordinator (80/20 facility spend)."],
    ["Power-plant EPC issuing the cable PO", "PG — the PO confirms the opportunity, it does not create ownership. The EPC's corporate coordinator is a separate decision."],
    ["BESS integrator on grid and facility work", "Split by scope — grid or generation-side to PG (Renewables open), facility-side storage to DC."],
  ];
  let y = 1.85;
  for (const r of rows) {
    dot(s, 0.62, y + 0.08);
    s.addText([
      { text: r[0] + " — ", options: { bold: true, color: INK } },
      { text: r[1], options: { color: MUTE } },
    ], { x: 0.95, y, w: 11.75, h: 0.68, fontFace: FONT, fontSize: 11.5, isTextBox: true, margin: 0, valign: "top" });
    y += 0.78;
  }
  s.addText("The hyperscaler row is the highest-politics case — and the clearest reason the two-role model exists.", {
    x: 0.6, y: 6.6, w: 12.13, h: 0.3, fontFace: FONT, fontSize: 10.5, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 5, false);
  s.addNotes(
    "Walk each case through Rules 1–2 out loud; none of them needs a tie-breaker. Distributor issuing the PO on an OEM-led deal: the distributor is a channel — ownership follows the OEM product line, and the distributor is managed under Marc's direct-versus-distribution rule. Public record backs the pattern: Powell's largest-ever data-center order is itself a behind-the-meter generation asset — the two verticals converge in a single order.\n[Sources] SWR-PG-ROE Rev 00 §4.2; outside-in readout Part C (Powell 10-Q/8-K, Q3 2026 call)."
  );
}

// ------------------------------------------------------------- S6 (light) Two roles
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "ACCOUNT VERSUS OPPORTUNITY OWNERSHIP");
  takeaway(s, "Account leadership and opportunity ownership are different jobs. Separate them.", false, { size: 27, h: 0.7 });

  const roles = [
    ["ACCOUNT COORDINATOR — ONE PER CUSTOMER",
      "Owns the relationship map, joint account plan and call calendar; makes the first call; rolls up the forecast across verticals; runs the quarterly joint review.",
      "Assigned to the vertical with the majority of Southwire-relevant spend — the 80/20 test. Reviewed annually.",
      "Does not own: any opportunity outside its scope, the right to block the other vertical, or sales credit on its opportunities."],
    ["OPPORTUNITY LEAD",
      "Owns the pursuit: spec engagement, quote, channel decision, forecast line, SAP/CPQ record, close. Receives the sales credit.",
      "Assigned by Rules 1–2 — the asset and the spec, never the PO.",
      "Does not own: the customer relationship as a whole, or the right to call into the account without informing the coordinator."],
  ];
  const rx = [0.6, 6.75];
  for (let i = 0; i < 2; i++) {
    s.addShape(pres.ShapeType.rect, { x: rx[i], y: 1.85, w: 5.98, h: 3.35, fill: { color: CARD }, line: { type: "none" } });
    s.addText(roles[i][0], { x: rx[i] + 0.25, y: 2.02, w: 5.5, h: 0.28, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1, isTextBox: true, margin: 0 });
    s.addText(roles[i][1], { x: rx[i] + 0.25, y: 2.38, w: 5.5, h: 0.95, fontFace: FONT, fontSize: 10.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
    s.addText(roles[i][2], { x: rx[i] + 0.25, y: 3.4, w: 5.5, h: 0.65, fontFace: FONT, fontSize: 10.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
    s.addText(roles[i][3], { x: rx[i] + 0.25, y: 4.25, w: 5.5, h: 0.85, fontFace: FONT, fontSize: 10, italic: true, color: MUTE, isTextBox: true, margin: 0, valign: "top" });
  }

  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 5.55, w: 12.13, h: 1.15, fill: { color: COPPER }, line: { type: "none" } });
  s.addText("HOW THE CUSTOMER SEES ONE SOUTHWIRE", { x: 0.9, y: 5.68, w: 6.0, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: "F6E3D3", charSpacing: 1.5, isTextBox: true, margin: 0 });
  s.addText(
    "One written introduction naming both roles · 24-hour courtesy note before any call into a coordinated account — the coordinator can join, not refuse · one record per opportunity in SAP/CPQ, or it does not exist · quarterly joint account review.",
    { x: 0.9, y: 5.95, w: 11.5, h: 0.65, fontFace: FONT, fontSize: 11.5, color: WHITE, isTextBox: true, margin: 0, valign: "top" }
  );
  footer(s, 6, false);
  s.addNotes(
    "Putting both jobs in one person per company is what forces defensive account-holding. A coordinator whose vertical adds no value to a given opportunity may delegate the customer face for that opportunity — written and time-boxed. Sales credit goes to the opportunity lead; influence credit for the coordinator is a compensation question for Marc and finance (TO SUPPLY) — influence must trace to the PO line or attribution will be disputed (Stephan's Aug 17 concern). Published practice supports exactly this separation (ZS/SAMA account-vs-opportunity ownership; McKinsey one-face-many-specialists).\n[Sources] SWR-PG-ROE Rev 00 §5; outside-in readout Part B."
  );
}

// ------------------------------------------------------------- S7 (light) Existing accounts
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "EXISTING-ACCOUNT TREATMENT — TIM'S AND OURS, SAME WORDS");
  takeaway(s, "Evidence decides, in both directions. Lists do not.", false);

  s.addText("AN ACTIVE PURSUIT NEEDS ALL FOUR", { x: 0.6, y: 1.85, w: 6.0, h: 0.26, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  const evid = [
    "A named opportunity: project, program or product line — an SAP/CPQ ID, OEM program or part-number family.",
    "A dated interaction with the controlling buying center inside the last 90 days — not “I talk to them all the time.”",
    "A quote, sample, spec submission or approved-vendor process in motion.",
    "A dated next step with an owner — not “following up.”",
  ];
  let y = 2.2;
  for (let i = 0; i < 4; i++) {
    s.addText(String(i + 1), { x: 0.62, y, w: 0.35, h: 0.3, fontFace: FONT, fontSize: 13, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText(evid[i], { x: 1.05, y, w: 11.6, h: 0.5, fontFace: FONT, fontSize: 11.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
    y += 0.56;
  }

  const cards = [
    ["GRANDFATHERED", "Documented active opportunities · the product lines and programs actually quoted or specified · the coordinator role where the customer's 80/20 spend is in the incumbent's scope."],
    ["NOT GRANDFATHERED", "The rest of the company. An active program on one product line does not confer the others. A company name on a list is not evidence."],
    ["RELEASE", "Opportunity: 90 days without a documented interaction or next step — release is automatic, no negotiation. Coordinator: 180 days without a joint plan, reassigned at the quarterly review."],
  ];
  const cy = 4.7;
  const cx = [0.6, 4.72, 8.84];
  for (let i = 0; i < 3; i++) {
    s.addShape(pres.ShapeType.rect, { x: cx[i], y: cy, w: 3.89, h: 1.75, fill: { color: CARD }, line: { type: "none" } });
    s.addText(cards[i][0], { x: cx[i] + 0.2, y: cy + 0.14, w: 3.5, h: 0.24, fontFace: FONT, fontSize: 9.5, bold: true, color: COPPER, charSpacing: 1.2, isTextBox: true, margin: 0 });
    s.addText(cards[i][1], { x: cx[i] + 0.2, y: cy + 0.44, w: 3.5, h: 1.2, fontFace: FONT, fontSize: 9.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  chip(s, 0.6, 6.62, "[R]", 0.55);
  s.addText("Contest only where the evidence standard is not met; do not reset active pursuits. Applied honestly, the standard moves more accounts than a reset would.", {
    x: 1.3, y: 6.6, w: 11.4, h: 0.35, fontFace: FONT, fontSize: 10.5, color: INK, isTextBox: true, margin: 0, valign: "top",
  });
  footer(s, 7, false);
  s.addNotes(
    "Fairness is the only way this survives contact with Jack: the same standard, in the same words, applied to Tim's accounts and to PG's. A reset fight in the first tranche costs more political capital than the accounts are worth. Open item (TO SUPPLY): whether the same standard applies to Brian Sides' accounts and to distributor- and agent-owned accounts (Bob Bennish's organization) — if not, the DC team will ask why the rule only runs one way.\n[Sources] SWR-PG-ROE Rev 00 §6; Marc's Aug 24 question on contest-versus-reset."
  );
}

// ------------------------------------------------------------- S8 (light) Rubric
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "CONTESTED-OPPORTUNITY RUBRIC — ONLY WHEN RULES 1–2 GENUINELY SPLIT");
  takeaway(s, "Score in writing before the meeting. Decide at four points. Re-score at 90 days.", false, { size: 27, h: 0.7 });

  const crit = [
    ["1", "Application fit", "the asset served and its POI position"],
    ["2", "Access to the controlling buying center", "named contacts with dates, in the group that writes the spec"],
    ["3", "Documented activity, last 90 days", "all four evidence requirements met"],
    ["4", "Capability to execute", "named resource with bandwidth; product-management confirmation on capacity"],
    ["5", "Documented customer preference", "written, from the controlling buying center only"],
    ["6", "Plan quality", "target dollars, dated milestones, channel decision — one page, submitted before the meeting"],
  ];
  let y = 1.95;
  for (const c of crit) {
    s.addText(c[0], { x: 0.62, y, w: 0.35, h: 0.3, fontFace: FONT, fontSize: 13, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText([
      { text: c[1] + " — ", options: { bold: true, color: INK } },
      { text: c[2], options: { color: MUTE } },
    ], { x: 1.05, y, w: 11.6, h: 0.42, fontFace: FONT, fontSize: 11.5, isTextBox: true, margin: 0, valign: "top" });
    y += 0.52;
  }
  s.addText("Each 0–3, both teams score, Marc and Jack confirm. Relationship tenure is deliberately not a criterion — it shows up only through access, activity and preference.", {
    x: 0.6, y: 5.15, w: 12.13, h: 0.5, fontFace: FONT, fontSize: 10.5, italic: true, color: MUTE, isTextBox: true, margin: 0, valign: "top",
  });

  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 5.8, w: 12.13, h: 0.95, fill: { color: CARD }, line: { type: "none" } });
  s.addText(
    "Margin of 4+ leads · margin of 3 or less: shared coverage with an explicit written split — no “joint ownership” without one · milestones missed without documented reason: re-score or release. The best executed strategy keeps the opportunity.",
    { x: 0.9, y: 5.98, w: 11.5, h: 0.62, fontFace: FONT, fontSize: 11.5, color: INK, isTextBox: true, margin: 0, valign: "top" }
  );
  footer(s, 8, false);
  s.addNotes(
    "Six criteria, 0–3 each, 18 maximum. Scores and plans are filed with the opportunity record so the next contest starts from evidence, not memory. This is where strategy strength lives — as the forcing function that makes both teams write a plan with dates and dollars, with a 90-day execution test — not as a primary rule.\n[Sources] SWR-PG-ROE Rev 00 §7."
  );
}

// ------------------------------------------------------------- S9 (light) Tranche 1
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "TRANCHE 1 — THE ACCOUNTS, ON EVIDENCE");
  takeaway(s, "Ten accounts, proposed on the rules. Gaps marked, not invented.", false, { size: 24, h: 0.48 });

  const rows = [
    ["Powell Industries", "TO SUPPLY — 80/20 split", "PG gas-plant lines · DC campus lines", "Jack confirms split by project end-use; Tim's activity"],
    ["Enchanted Rock · VoltaGrid", "PG", "PG", "Ratify BTM-default-to-PG as asset type"],
    ["Hyperscalers (Google · Microsoft)", "DC — 80/20 is facility", "PG for generation scope", "First test of the two-role model"],
    ["NRG · CPV (IPPs)", "PG", "PG", "PG-vs-Brian split (2028-29 horizon); distributor rules"],
    ["Southern Company / Southern Power", "Utility for the IOUs; PG for Southern Power", "PG", "How PG operates inside a utility framework agreement"],
    ["Utility T&D / substation build", "Utility", "Utility", "Ratify the POI rule; plant-switchyard question"],
    ["Kiewit · Gemma · Burns & McDonnell", "TO SUPPLY — by primary end market", "PG for generation projects", "Corporate coordinator rule for EPCs, before Jack asks"],
    ["nVent / Trachte (eHouses)", "TO SUPPLY", "By project end-use", "First account through the rubric, with Tim"],
    ["BESS integrators (Fluence · Tesla…)", "TO SUPPLY — Renewables vs PG", "PG or Renewables grid-side · DC facility-side", "Where grid-side BESS sits; not ready for Jack"],
    ["Cooling / HVAC OEMs", "DC", "DC", "None — listed to show PG is not claiming everything"],
  ];
  const tableRows = [
    [
      { text: "Account", options: { bold: true, color: WHITE, fill: { color: COPPER } } },
      { text: "Proposed coordinator", options: { bold: true, color: WHITE, fill: { color: COPPER } } },
      { text: "Proposed opportunity lead", options: { bold: true, color: WHITE, fill: { color: COPPER } } },
      { text: "Open item / decision", options: { bold: true, color: WHITE, fill: { color: COPPER } } },
    ],
  ].concat(rows.map((r) => [
    { text: r[0], options: { bold: true, color: INK } },
    { text: r[1], options: { color: r[1].startsWith("TO SUPPLY") ? COPPER : INK } },
    { text: r[2], options: { color: INK } },
    { text: r[3], options: { color: MUTE } },
  ]));
  s.addTable(tableRows, {
    x: 0.6, y: 1.62, w: 12.13, colW: [3.1, 2.75, 3.03, 3.25], rowH: 0.42,
    fontFace: FONT, fontSize: 8.5, border: { type: "solid", pt: 0.5, color: "E2E2E2" },
    valign: "middle", margin: [0.03, 0.07, 0.03, 0.07],
  });
  s.addText("July quoting on these accounts: Powell ~$3.4M · Enchanted Rock $2.3M (~40% GM) · VoltaGrid $1M · nVent/Trachte ~$3M — quoting, not bookings [F]. Every proposed lead is conditional on Tim's documented activity — TO SUPPLY.", {
    x: 0.6, y: 6.5, w: 12.13, h: 0.5, fontFace: FONT, fontSize: 9.5, italic: true, color: MUTE, isTextBox: true, margin: 0, valign: "top",
  });
  footer(s, 9, false);
  s.addNotes(
    "The proposed leads are what the rules would give, conditional on the facts marked TO SUPPLY — without Tim's documented activity the table shows what PG would propose, not what the evidence supports. nVent/Trachte and the cooling OEMs are in the tranche because they show the model rejecting a PG claim as well as making one. Site work in motion: Texas week of Sept 21 — Enchanted Rock confirmed, VoltaGrid being scheduled, Phil Metz on Powell, Stephan on NRG / CPV / Vistra / Chevron.\n[Sources] SWR-PG-ROE Rev 00 §8, §11; July quoting figures as sent to Marc Aug 25 (17 IPP pursuits, >$200M W&C)."
  );
}

// ------------------------------------------------------------- S10 (dark) Outside-in
{
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(s, "OUTSIDE-IN — WHAT PEERS AND PUBLISHED PRACTICE ACTUALLY DO");
  takeaway(s, "No peer splits these into two account-owning teams. The buying center decides.", true, { size: 27, h: 0.7 });

  const rows = [
    "Prysmian, Eaton and Hubbell run product/segment structures and treat data center as a cross-cutting demand theme — coordinated across divisions, one face to the customer.",
    "Schneider names the vertical outright; Hubbell publicly credits sales-force alignment for its data-center share gains.",
    "Powell's largest-ever data-center order is itself a behind-the-meter generation asset — the overlap is structural, not a Southwire artifact.",
    "Hyperscaler generation purchases run through named energy / power-procurement teams (Google, Microsoft), distinct from facility construction.",
    "Published practice: separate account from opportunity ownership · written rules of engagement with CRM enforcement · 30-60-90 grandfathering · monthly re-planning · bespoke treatment only for the top overlap accounts.",
  ];
  let y = 1.9;
  for (const r of rows) {
    dot(s, 0.62, y + 0.08);
    s.addText(r, { x: 0.95, y, w: 11.7, h: 0.75, fontFace: FONT, fontSize: 12, color: WHITE, isTextBox: true, margin: 0, valign: "top" });
    y += 0.85;
  }
  s.addText("One face, many specialists — written rules, not walls.", {
    x: 0.6, y: 6.35, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: COPPER, isTextBox: true, margin: 0,
  });
  footer(s, 10, true);
  s.addNotes(
    "All public, citable sources; no internal information. The recurring public answer to overlap is cross-divisional coordination plus vertical sales alignment — not hard account walls. The most stable ownership discriminator in the public evidence is the buying center: energy/power procurement versus facility construction versus EPC versus utility. This is the outside validation for the two-axis frame and the two-role model.\n[Sources] Outside-in readout (Prysmian FY2025 results and data-center statements; Eaton FY2025 10-K; Hubbell Investor Day 2024 and Q2 2026 call; Schneider via Utility Dive 2026; Powell 10-K/10-Q and Q3 2026 call; Canary Media on Google/Microsoft energy teams; ZS/SAMA, McKinsey, HBR on coverage practice)."
  );
}

// ------------------------------------------------------------- S11 (light) The stake
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "WHAT THE BOUNDARY IS WORTH");
  chip(s, 11.55, 0.46, "PROVISIONAL", 1.18);
  takeaway(s, "$170–240M a year in gas-generation cable POs through 2030.", false, { size: 29, h: 0.7 });

  const rows = [
    "Cumulative 2026–35 base ~$1.7B (scenario range $0.8B–$5.0B). Only 46% of named MW is evidence-backed and no internal quote, BOM or PO data is loaded — the model stays provisional until it is.",
    "Roughly a quarter of near-term value sits in named buying windows open in the next 18 months — controlled mainly by EPCs (Kiewit first) and utility procurement, not plant owners.",
    "Turbine backlogs are sold out for years — GE Vernova 116 GW, Siemens Energy ~69 GW, Mitsubishi 35 GW — with ~20% explicitly data-center-tied. Cable can be contracted 3–4 years before COD; the 2028–2030 buying window is open now.",
    "The GEM 189 GW figure is a gross proposal inventory, never a market total or a control number.",
  ];
  let y = 1.9;
  for (const r of rows) {
    dot(s, 0.62, y + 0.08);
    s.addText(r, { x: 0.95, y, w: 11.7, h: 0.85, fontFace: FONT, fontSize: 12, color: INK, isTextBox: true, margin: 0, valign: "top" });
    y += 0.98;
  }
  chip(s, 0.6, 6.05, "[R]", 0.55);
  s.addText("No dollar figure goes in front of Jack until the internal data request is filled. The stake is why the boundary matters this quarter — not a forecast.", {
    x: 1.3, y: 6.03, w: 11.4, h: 0.5, fontFace: FONT, fontSize: 11, color: INK, isTextBox: true, margin: 0, valign: "top",
  });
  footer(s, 11, false);
  s.addNotes(
    "From the gas-power executive readout (research cutoff Aug 27): base-case $170–240M per year in POs through 2030, constant 2026 dollars, manufacturer net sales, generation-side cable only; shipments peak 2028–29 at ~$240M. Two things move the answer most: Southwire's own cable-per-MW history (the model carries a 5.3x multiple over the public floor) and a fuller project census (86% of TAM is unnamed residual). 2026 split: $240M full-year market, ~$73M still open after Aug 27, $89M awarded-but-unshipped backlog. Mention, do not present, unless asked.\n[Sources] Gas-Power Wire & Cable Executive Readout (model v1, 27 QA tests, 3 disclosed exceptions); NRG/GE Vernova/Kiewit 8-K; GEM reconciliation in the same readout."
  );
}

// ------------------------------------------------------------- S12 (dark) Thursday + Jack
{
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(s, "TODAY, AND THE ASK TO JACK");
  takeaway(s, "Three outcomes leave this room. Six items go to Jack, once.", true, { size: 28, h: 0.7 });

  s.addText("THIS SESSION", { x: 0.6, y: 1.8, w: 3.0, h: 0.26, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  const agenda = [
    ["9:00", "Outcomes and parking lot"],
    ["9:20", "Definitions — the one-page output"],
    ["10:10", "Rule hierarchy; strategy-strength question"],
    ["11:00", "Tranche 1 — roles and evidence request"],
    ["11:50", "Existing accounts — standard and release"],
    ["12:20", "The ask to Jack; who presents which"],
    ["12:45", "Every parked item gets an owner and a date"],
  ];
  let y = 2.15;
  for (const a of agenda) {
    s.addText(a[0], { x: 0.6, y, w: 0.85, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText(a[1], { x: 1.55, y, w: 4.6, h: 0.3, fontFace: FONT, fontSize: 10.5, color: WHITE, isTextBox: true, margin: 0, valign: "top" });
    y += 0.42;
  }
  s.addText("Not for Jack: resource transfers · every contested case · the PG-Renewables and PG-Brian lines — Marc's to settle first.", {
    x: 0.6, y: 5.3, w: 5.6, h: 0.75, fontFace: FONT, fontSize: 10, italic: true, color: DMUTE, isTextBox: true, margin: 0, valign: "top" });

  s.addText("THE SIX ITEMS JACK SIGNS", { x: 6.7, y: 1.8, w: 5.9, h: 0.26, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  const jack = [
    "The two-line definition — asset served plus specification control, POI rule, BTM stated as asset type.",
    "The rule hierarchy, with strategy strength as last resort only.",
    "The evidence standard and 90/180-day release — both verticals.",
    "The two-role model, the 24-hour courtesy rule, the single-record rule.",
    "Tranche 1 — ten accounts with roles, and the evidence request for Tim's activity.",
    "The mutual monthly reporting obligation.",
  ];
  y = 2.15;
  for (let i = 0; i < 6; i++) {
    s.addText(String(i + 1), { x: 6.7, y, w: 0.32, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText(jack[i], { x: 7.1, y, w: 5.6, h: 0.6, fontFace: FONT, fontSize: 10.5, color: WHITE, isTextBox: true, margin: 0, valign: "top" });
    y += 0.63;
  }

  s.addText("Jack approves the machine, not each output. Unresolved after two weeks goes to Donna as sponsor of the PG mandate.", {
    x: 0.6, y: 6.35, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 14, bold: true, color: COPPER, isTextBox: true, margin: 0,
  });
  footer(s, 12, true);
  s.addNotes(
    "Governance behind this slide: each vertical director proposes ownership for their own accounts in tranches of ten with evidence attached; Marc and Jack jointly approve the rules once; tranches approve within two weeks or default to the proposal — silence cannot hold an account. Contested opportunities review at 90 days; coordinator lists quarterly; whoever claims an account reports its status monthly — claiming everything means reporting on everything, which shrinks lists on its own. Escalation: Marc and Jack with the rubric; unresolved after two weeks goes to Donna (whether Jack is Marc's peer is TO SUPPLY — it determines whether Donna is the right escalation).\n[Sources] SWR-PG-ROE Rev 00 §9–10."
  );
}

// ------------------------------------------------------------- A1 — TO SUPPLY
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("APPENDIX 1 — TO SUPPLY BEFORE THE TABLE IS DEFENSIBLE", {
    x: 0.6, y: 0.5, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  const items = [
    "Tim Schmidt's documented activity at Powell, Enchanted Rock, VoltaGrid, nVent/Trachte and the hyperscalers — opportunity IDs, quote numbers, contact names, last-contact dates, next steps.",
    "Tim's scope in his own words, and Jack's org chart with reporting lines.",
    "Whether Jack and Marc are peers, and who arbitrates above them.",
    "Powell's revenue mix with Southwire — generation versus data center — to run the 80/20 test.",
    "The legacy utility and industrial teams' current activity at Southern Company, the EPCs and the substation work.",
    "Brian Sides' account list and what he considers his backbone scope.",
    "Distributor and agent ownership rules as they stand today (Bob Bennish's organization), and how influence is credited on the PO line.",
    "Product management's position on MV capacity available for PG opportunities in 2026–27, so the rubric's capability criterion can be scored honestly.",
    "The Renewables vertical's position on grid-side BESS.",
    "Any hyperscaler pursuit the DC team currently has open, so the Google introduction does not land on top of it.",
  ];
  let y = 1.3;
  for (const it of items) {
    dot(s, 0.62, y + 0.07);
    s.addText(it, { x: 0.95, y, w: 11.7, h: 0.52, fontFace: FONT, fontSize: 10.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
    y += 0.56;
  }
  footer(s, 13, false);
  s.addNotes(
    "Nothing has been invented to fill a table — every account fact not in hand is marked TO SUPPLY, and this is the full list. The first four items are the evidence request that leaves today's session addressed to Tim via Jack.\n[Sources] SWR-PG-ROE Rev 00 §11.1."
  );
}

// ------------------------------------------------------------- A2 — Prep questions
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("APPENDIX 2 — THE QUESTIONS, IN SESSION ORDER", {
    x: 0.6, y: 0.5, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  const qs = [
    "What asset does the cable feed, and who writes the spec — and is that really enough to decide most cases?",
    "Company or opportunity — which level are we assigning, and what do we lose if it is company?",
    "A generator at a data center: are we saying “asset type” or are we saying “behind the meter”?",
    "What evidence would we accept from Tim — and would we pass our own test on every account we are claiming?",
    "If the customer prefers us, is that the buying center that controls the spec, or a supportive individual?",
    "Who judges a contested case, and what happens at day 90 if the winner has not moved?",
    "What are the six things Jack signs — and which conversation are we deliberately not having with him yet?",
    "Where do BESS, the plant switchyard and captive cogeneration go — and are Marc and Stephan actually agreed?",
  ];
  let y = 1.35;
  for (let i = 0; i < qs.length; i++) {
    s.addText(String(i + 1), { x: 0.62, y, w: 0.4, h: 0.35, fontFace: FONT, fontSize: 14, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText(qs[i], { x: 1.15, y, w: 11.5, h: 0.5, fontFace: FONT, fontSize: 12, color: INK, isTextBox: true, margin: 0, valign: "top" });
    y += 0.66;
  }
  footer(s, 14, false);
  s.addNotes(
    "The eight handwritten prep questions, in the order the session hits them. Internal decisions still open behind them: plant switchyard (recommend PG), grid-side BESS (PG or Renewables — not ready for Jack), captive cogeneration (Industrial by default with PG supporting the generation spec; exporting or third-party-owned goes to PG), Brian Sides' scope against PG's 2028-29 horizon (agreed in principle Aug 20).\n[Sources] SWR-PG-ROE Rev 00 §12, §3.2, §10.1."
  );
}

pres.writeFile({ fileName: "Southwire_PG_DC_Coverage_Model_Rev00.pptx" }).then(() => {
  console.log("written: Southwire_PG_DC_Coverage_Model_Rev00.pptx");
});
