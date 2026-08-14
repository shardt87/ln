// Editable PPTX version of Southwire_PowerGen_Brochure_NRG_Rev01
// Coordinates ported from build_brochure.py (pdf pts, origin bottom-left, page 810x630 incl 9pt bleed)
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.defineLayout({ name: "LETTER_LAND", width: 11, height: 8.5 });
p.layout = "LETTER_LAND";

const WARM = "F6F3EE", GRAPHITE = "17191C", INK = "1A1C22", GRAY = "6E6C66",
  GRAY_LT = "96938C", COPPER = "C67A43", COPPER_LT = "E3A06D", COPPER_DP = "9D4E24",
  TEAL = "1A272F", OFFWHITE = "ECEAE6", HAIR = "D8D2C8", HAIR_DK = "3C3F44",
  WHITE = "FFFFFF";
const A = "assets/";
const PHpt = 630, BL = 9; // pdf page height, bleed
const X = (xpt) => (xpt - BL) / 72;
const Y = (ytoppt) => (PHpt - BL - ytoppt) / 72; // pdf y (bottom-origin) of TOP edge -> inches
const W = (wpt) => wpt / 72;

// text block: yb = baseline of FIRST line (pdf pts)
function T(s, xpt, yb, wpt, lines, o = {}) {
  const size = o.size || 10, leading = o.leading || size * 1.35;
  const n = Array.isArray(lines) ? lines.length : 1;
  const text = Array.isArray(lines) ? lines.join("\n") : lines;
  const topPdf = yb + size * 1.02;
  const h = (leading * (n - 1) + size * 1.65) / 72;
  const opts = {
    x: o.align === "center" ? X(xpt) - W(wpt) / 2 : o.align === "right" ? X(xpt) - W(wpt) : X(xpt),
    y: Y(topPdf), w: W(wpt), h,
    fontFace: "Arial", fontSize: size, color: o.color || INK,
    bold: !!o.bold, italic: !!o.italic, align: o.align || "left",
    valign: "top", margin: 0, lineSpacing: leading,
  };
  if (o.track) opts.charSpacing = o.track;
  s.addText(text, opts);
}
function rect(s, xpt, ytop, wpt, hpt, color) {
  s.addShape("rect", { x: X(xpt), y: Y(ytop), w: W(wpt), h: W(hpt), fill: { color }, line: { type: "none" } });
}
function hline(s, x1, x2, ypt, color, wpx) {
  s.addShape("line", { x: X(x1), y: Y(ypt), w: W(x2 - x1), h: 0, line: { color, width: wpx } });
}
function img(s, file, xpt, ytop, wpt, hpt) {
  s.addImage({ path: A + file, x: X(xpt), y: Y(ytop), w: W(wpt), h: W(hpt) });
}
const FOOT = "Stephan Hardt   |   Power Generation Solutions";

function lightFrame(s, kicker, folio, band) {
  s.background = { color: WARM };
  rect(s, 0, PHpt, 828, 12.5, COPPER); // top copper band
  const lh = 23, lw = lh * 640 / 135;
  img(s, "lockup_light.png", 54, PHpt - 30, lw, lh);
  T(s, 810 - 54, PHpt - 43, 220, kicker, { size: 7.5, bold: true, color: COPPER, track: 1.6, align: "right" });
  if (!band) {
    T(s, 54, 30, 300, FOOT, { size: 6.5, color: GRAY_LT });
    T(s, 810 - 54, 30, 60, folio, { size: 6.5, bold: true, color: COPPER, track: 1.2, align: "right" });
  }
}
function bandFooter(s, folio) {
  T(s, 54, 14, 300, FOOT, { size: 6.5, color: "8C8A86" });
  T(s, 810 - 54, 14, 60, folio, { size: 6.5, bold: true, color: COPPER_LT, align: "right", track: 1.2 });
}

// ---------------- 1 · cover
{
  const s = p.addSlide();
  s.background = { color: GRAPHITE };
  const bh = 810 * 785 / 4752;
  img(s, "hex_top_fade.png", 0, PHpt, 828, bh);
  img(s, "hex_bottom_fade.png", 0, bh, 828, bh);
  const lw = 200, lh = lw * 202 / 943;
  img(s, "lockup_dark_keyed.png", 405 - lw / 2, 472 + lh, lw, lh);
  T(s, 405, 352, 700, "ACCELERATING", { size: 40, bold: true, color: WHITE, track: 6, align: "center" });
  T(s, 405, 300, 700, "TIME TO POWER", { size: 40, bold: true, italic: true, color: COPPER_LT, track: 6, align: "center" });
  hline(s, 405 - 62, 405 + 62, 274, COPPER, 1.2);
  T(s, 405, 236, 700, "Accelerating & protecting power readiness across NRG's gas power generation buildout.", { size: 11, color: OFFWHITE, align: "center" });
  T(s, 405, 210, 760, "COMBINED CYCLE  ·  SIMPLE CYCLE & PEAKERS  ·  MODULAR POWER  ·  BLACK START  ·  COAL/GAS REPOWER  ·  GREENFIELD & BROWNFIELD", { size: 6.8, color: "969490", track: 1.1, align: "center" });
  T(s, 405, 158, 700, "PRESERVE SCHEDULE CERTAINTY THROUGH ENERGIZATION.", { size: 8.5, bold: true, color: COPPER_LT, track: 2.2, align: "center" });
  T(s, 405, 84, 700, "Stephan Hardt   |   Director, Power Generation Solutions   |   www.southwire.com", { size: 7.5, color: "9E9C98", align: "center" });
}

// ---------------- 2 · why now
{
  const s = p.addSlide();
  lightFrame(s, "WHY NOW", "02", true);
  T(s, 54, 508, 660, ["NRG's growth agenda creates three distinct", "electrical-delivery environments & power demand."], { size: 27, bold: true, leading: 33 });
  const cols = [
    ["1.5 GW", "TEF PORTFOLIO", "One project operating; two targeting mid-2028. Not the entire portfolio under construction."],
    ["5.4 GW", "NEWBUILD DEVELOPMENT", "Turbine and EPC access supports a development runway through 2032."],
    ["25.8 GW", "OPERATING FLEET", "Reported after the LS Power acquisition; ~1–2 GW of upgrades under evaluation."],
  ];
  const colw = (810 - 108 - 72) / 3;
  cols.forEach((c0, i) => {
    const x = 54 + i * (colw + 36);
    T(s, x, 356, colw, c0[0], { size: 34, bold: true });
    hline(s, x + 1, x + 27, 338, COPPER, 1.4);
    T(s, x, 316, colw, c0[1], { size: 8, bold: true, color: COPPER_DP, track: 1.5 });
    T(s, x, 294, colw - 12, c0[2], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  const ph = 196, pw = ph * 1672 / 941;
  img(s, "peaker_warm.png", 810 - pw, 280, pw, ph);
  T(s, 54, 204, 400, ["Specifications, capacity, metals hedging, releases, reels, package interfaces and field", "readiness still have to converge on COD.  Do not sum the figures — asset states overlap."], { size: 10, color: GRAY, leading: 14 });
  T(s, 54, 100, 300, "Source: NRG 2Q26, Aug. 4, 2026", { size: 6, color: GRAY_LT });
  rect(s, 0, 84, 828, 84, GRAPHITE);
  T(s, 54, 56, 500, "DIFFERENT ASSET STATES. ONE REQUIREMENT.", { size: 8, bold: true, color: COPPER_LT, track: 1.8 });
  T(s, 54, 34, 500, "Preserve schedule certainty through energization.", { size: 13.5, bold: true, color: WHITE });
  bandFooter(s, "02");
}

// ---------------- 3 · thesis
{
  const s = p.addSlide();
  s.addImage({ path: A + "hero_sky.jpg", x: 0, y: 0, w: 11, h: 8.5 });
  T(s, 54, 568, 300, "THE THESIS", { size: 7.5, bold: true, color: COPPER_DP, track: 1.6 });
  T(s, 54, 536, 620, ["Time to power is an electrical execution problem", "before it is a cable-buying problem."], { size: 23, bold: true, leading: 29 });
  const bullets = [
    "Interfaces cross packages, zones, POI, contractors and turnover paths.",
    "Late material decisions return as handling, rework and commissioning exposure.",
    "Managing the workstream as a system protects schedule better than isolated purchase-order optimization.",
  ];
  bullets.forEach((b, i) => {
    const yb = 474 - i * 18;
    hline(s, 55, 67, yb + 3, COPPER_DP, 1.4);
    T(s, 76, yb, 620, b, { size: 9.5 });
  });
  rect(s, 0, 44, 828, 44, GRAPHITE);
  T(s, 54, 18, 700, "The plant-wide electrical-delivery partner — cable scope ready for the workface, not merely available at the warehouse.", { size: 9.5, bold: true, italic: true, color: WHITE });
  T(s, 810 - 54, 568, 300, FOOT + "   ·   03", { size: 6.5, color: GRAY, align: "right" });
}

// ---------------- 4 · risks
{
  const s = p.addSlide();
  lightFrame(s, "THE THREE RISKS", "04", true);
  T(s, 54, 508, 660, ["Three execution risks can erode certainty", "between design and energization."], { size: 27, bold: true, leading: 33 });
  const cols = [
    ["01", "LABOR & DEMAND PRESSURE", "Long pulls, dense terminations and compressed turnover windows concentrate labor when flexibility is lowest."],
    ["02", "MATERIAL + INSTALLATION FIT", "Ratings, routes, reel lengths, accessories and releases must match the workface, not only the BOM — or material arrives right and installs wrong."],
    ["03", "FRAGMENTED COORDINATION", "Civil, electrical, OEM and contractor decisions can converge after routing and procurement choices are already locked, turning gaps into rework."],
  ];
  const colw = (810 - 108 - 72) / 3;
  cols.forEach((c0, i) => {
    const x = 54 + i * (colw + 36);
    T(s, x, 326, colw, c0[0], { size: 21, bold: true, color: COPPER, track: 2 });
    hline(s, x + 1, x + 27, 310, COPPER, 1.4);
    T(s, x, 288, colw, c0[1], { size: 8.5, bold: true, track: 1.2 });
    T(s, x, 266, colw - 12, c0[2], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  rect(s, 0, 84, 828, 84, GRAPHITE);
  T(s, 54, 48, 600, "Late handoffs become schedule and commissioning exposure.", { size: 12.5, bold: true, color: WHITE });
  T(s, 54, 28, 600, "LABOR AVAILABILITY   |   MATERIAL READINESS   |   DECISION TIMING", { size: 7, color: "969490", track: 1.6 });
  bandFooter(s, "04");
}

// ---------------- 5 · system
{
  const s = p.addSlide();
  s.addImage({ path: A + "interior_full.jpg", x: 0, y: 0, w: 11, h: 8.5 });
  T(s, 54, 574, 300, "THE SYSTEM", { size: 7.5, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, 54, 542, 620, ["One coordinated flow aligns decisions", "from planning through turnover."], { size: 24, bold: true, color: WHITE, leading: 29 });
  T(s, 54, 489, 620, ["Southwire connects application support, material planning, sequenced logistics", "and field readiness — without changing project accountability."], { size: 9.5, bold: true, color: OFFWHITE, leading: 15 });
  rect(s, 0, 140, 828, 140, GRAPHITE);
  const steps = ["PLAN + FORECAST", "APPLICATION ALIGNMENT", "MATERIAL + REEL STRATEGY", "RELEASE + LOGISTICS", "INSTALLATION READINESS", "FIELD SUPPORT + TURNOVER"];
  const x0 = 90, x1 = 720, ny = 100, r = 11.5;
  hline(s, x0, x1, ny, COPPER, 1);
  steps.forEach((name, i) => {
    const x = x0 + i * (x1 - x0) / 5;
    s.addShape("ellipse", { x: X(x - r), y: Y(ny + r), w: W(2 * r), h: W(2 * r), fill: { color: i < 5 ? "32353A" : COPPER_DP }, line: { type: "none" } });
    T(s, x, ny - 3.2, 30, String(i + 1), { size: 9.5, bold: true, color: WHITE, align: "center" });
    const parts = name.length > 17 ? name.split(" + ").map((t, j) => (j === 0 ? t + " +" : t)) : [name];
    T(s, x, ny - 28, 110, parts, { size: 7, bold: true, color: OFFWHITE, track: 0.8, align: "center", leading: 10 });
  });
  T(s, 405, 30, 700, "FIELD-ENGINEER WHAT IS UNIQUE. PREFABRICATE WHAT REPEATS.", { size: 8.5, bold: true, color: COPPER_LT, track: 1.6, align: "center" });
  T(s, 54, 12, 300, FOOT, { size: 6, color: "8C8A86" });
  T(s, 810 - 54, 12, 60, "05", { size: 6, bold: true, color: COPPER_LT, align: "right", track: 1.2 });
}

// ---------------- 6 · value proposition
{
  const s = p.addSlide();
  lightFrame(s, "THE VALUE PROPOSITION", "06", false);
  T(s, 54, 452, 660, "Southwire helps IPPs", { size: 34, bold: true });
  T(s, 54, 408, 660, "accelerate time to power.", { size: 34, bold: true, color: COPPER_DP });
  hline(s, 56, 180, 378, COPPER, 1.2);
  T(s, 54, 330, 640, ["By transforming fragmented plant-wide cable procurement into a coordinated,", "workface-ready electrical delivery system — reducing schedule risk, installed effort,", "and commissioning exposure from planning through energization."], { size: 13, color: "4A4C50", leading: 22 });
}

// ---------------- 7 · adjacent evidence
{
  const s = p.addSlide();
  s.background = { color: TEAL };
  T(s, 54, 566, 300, "ADJACENT EVIDENCE", { size: 7.5, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, 54, 534, 620, ["Adjacent experience indicates where", "to test — not what NRG will save."], { size: 23, bold: true, color: WHITE, leading: 29 });
  T(s, 54, 388, 240, "4,400", { size: 42, bold: true, color: WHITE });
  s.addShape("line", { x: X(236), y: Y(402), w: W(42), h: 0, line: { color: COPPER, width: 1.6, endArrowType: "arrow" } });
  T(s, 298, 388, 240, "~880", { size: 42, bold: true, color: COPPER_LT });
  T(s, 54, 366, 220, ["OBSERVED FIELD HOURS", "SITE-BUILT BASELINE"], { size: 6.8, bold: true, color: "B2B6B8", track: 1, leading: 11 });
  T(s, 298, 366, 220, ["MODELED FIELD HOURS", "FACTORY-BUILT ASSEMBLY"], { size: 6.8, bold: true, color: COPPER_LT, track: 1, leading: 11 });
  T(s, 54, 326, 380, ["Field hours per electrical spine in one repetitive modular-generation scope.", "Illustrative adjacent-market benchmark — not an NRG result."], { size: 8.5, color: "969EA2", leading: 13 });
  T(s, 54, 268, 300, "WHAT IT SUGGESTS", { size: 7.5, bold: true, color: COPPER_LT, track: 1.4 });
  T(s, 54, 248, 330, ["Stable, repeatable interfaces may be candidates", "for offsite work."], { size: 9.5, color: OFFWHITE, leading: 14 });
  T(s, 54, 196, 300, "WHAT IT DOES NOT PROVE", { size: 7.5, bold: true, color: COPPER_LT, track: 1.4 });
  T(s, 54, 176, 330, ["Net NRG savings, schedule reduction or", "critical-path removal."], { size: 9.5, color: OFFWHITE, leading: 14 });
  const iw = 384, ih = iw * 730 / 1600, ix = 810 - iw - 9;
  img(s, "xray_feather.png", ix, 244 + ih, iw, ih);
  T(s, ix + 14, 212, 366, "THE ROUTED MODEL — WHAT MAKES THE FACTORY-BUILT NUMBER POSSIBLE", { size: 6.8, bold: true, color: COPPER_LT, track: 1 });
  T(s, ix + 14, 191, 370, ["One electrical system — trays, routes and cable planned", "plant-wide, so repeatable runs can be built offsite."], { size: 8.5, color: OFFWHITE, leading: 13 });
  T(s, ix + 14, 156, 370, "CCGT tray & cable x-ray · conceptual — not for construction", { size: 6, color: "8C989E" });
  T(s, 54, 100, 700, "REBUILD THE CASE WITH NRG SCOPE, LABOR RATES, SCHEDULE LOGIC AND ACCEPTANCE CRITERIA.", { size: 7.5, bold: true, color: COPPER_LT, track: 1.2 });
  T(s, 54, 84, 700, "NO PRESUMPTION THAT THE ANSWER IS PREFAB — OR THAT SOUTHWIRE BELONGS IN THE SOLUTION.", { size: 7.5, bold: true, color: "969EA2", track: 1.2 });
  T(s, 54, 24, 300, FOOT, { size: 6.5, color: "969B9E" });
  T(s, 810 - 54, 24, 60, "07", { size: 6.5, bold: true, color: COPPER_LT, align: "right", track: 1.2 });
}

// ---------------- 8 · owner economics
{
  const s = p.addSlide();
  lightFrame(s, "OWNER ECONOMICS", "08", true);
  T(s, 54, 508, 660, ["Cable is a small cost category with", "outsized execution consequences."], { size: 26, bold: true, leading: 32 });
  T(s, 54, 446, 640, ["The owner lens is how electrical decisions influence COD readiness, installed effort, capital", "certainty and lifecycle continuity — not unit price alone."], { size: 10.5, color: GRAY, leading: 15 });
  const quads = [
    ["01", "COD / REVENUE START & ENERGY DELIVERED", "Capacity visibility, delivered power, release timing and installation readiness can influence energization milestones."],
    ["02", "INSTALLED COST", "Routes, reels, cuts, pulls, congestion and rework often matter more than purchase price alone."],
    ["03", "CAPITAL CERTAINTY", "Earlier scope visibility supports commodity planning, material allocation and contingency discipline."],
    ["04", "AVAILABILITY / LIFECYCLE", "Turnover records, spares, condition screens and replacement planning support long-term continuity."],
  ];
  const colw = (810 - 108 - 44) / 2;
  quads.forEach((q, i) => {
    const x = 54 + (i % 2) * (colw + 44);
    const yy = 372 - Math.floor(i / 2) * 128;
    T(s, x, yy, 100, q[0], { size: 17, bold: true, color: COPPER, track: 1.5 });
    hline(s, x + 1, x + 27, yy - 13, COPPER, 1.4);
    T(s, x, yy - 32, colw, q[1], { size: 8.5, bold: true, track: 1 });
    T(s, x, yy - 50, colw - 16, q[2], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  rect(s, 0, 76, 828, 76, GRAPHITE);
  T(s, 54, 44, 640, "LOW CAPEX SHARE. HIGH SCHEDULE AND COMMISSIONING LEVERAGE.", { size: 10, bold: true, color: COPPER_LT, track: 1.8 });
  bandFooter(s, "08");
}

// ---------------- 9 · plant-wide coverage
{
  const s = p.addSlide();
  lightFrame(s, "PLANT-WIDE COVERAGE", "09", true);
  T(s, 54, 514, 660, ["Six clusters map a routed 3×1 electrical", "reference model."], { size: 26, bold: true, leading: 32 });
  const clusters = [
    ["GRID + SITE BACKBONE", "Switchyard, GSU/grid tie and MV corridors", "HV/EHV · MV · protection/control · fiber · grounding"],
    ["GENERATION ISLAND + BOP", "HRSG, turbine hall and GT inlet", "MV/LV/VFD · I&C · F&G/ESD · CEMS · heat trace"],
    ["MODULAR + PACKAGED SYSTEMS", "BESS, reel staging, prefab/skids and modular power", "DC/MV/LV · controls · fiber · engineered sets"],
    ["HEAT REJECTION + WATER + BOP", "ACC, cooling and water/wastewater", "Repeated fan/pump power · VFD · controls · wet runs"],
    ["BUILDINGS + DISTRIBUTION + BOP", "Control building, e-house and MCC/VFD/UPS", "MV/LV/VFD · essential AC/DC · life safety · BAS/data"],
    ["OPTIONAL + AUXILIARY + BOP", "Carbon capture and gas metering", "Classified power/control · instrumentation · F&G · fiber"],
  ];
  const colw = (810 - 108 - 68) / 3;
  clusters.forEach((c0, i) => {
    const x = 54 + (i % 3) * (colw + 34);
    const yy = 408 - Math.floor(i / 3) * 138;
    hline(s, x + 1, x + 27, yy + 14, COPPER, 1.4);
    T(s, x, yy, colw - 10, c0[0], { size: 8.5, bold: true, leading: 12 });
    T(s, x, yy - 26, colw - 12, c0[1], { size: 9, color: GRAY, leading: 12.5 });
    T(s, x, yy - 62, colw - 12, c0[2], { size: 7.5, color: COPPER_DP, leading: 10.5 });
  });
  rect(s, 0, 84, 828, 84, GRAPHITE);
  T(s, 54, 56, 720, "CABLE CLASSES — HV/EHV · MV 5–35 kV · LV 600 V · VFD · ESSENTIAL AC/DC · I&C · FIBER/NETWORK · LIFE SAFETY · GROUNDING", { size: 7.5, bold: true, color: COPPER_LT, track: 1.4 });
  T(s, 54, 36, 700, "Illustrative — not NRG/IFC. Excludes generator-output bus, OEM wiring and contractor methods.", { size: 7, color: "969490" });
  bandFooter(s, "09");
}

// ---------------- 10 · governance
{
  const s = p.addSlide();
  lightFrame(s, "GOVERNANCE", "10", true);
  T(s, 54, 514, 660, ["Clear decision rights preserve existing", "project accountability."], { size: 26, bold: true, leading: 32 });
  const rows = [
    ["NRG + UTILITY INTERFACE", "Owner priorities, portfolio standards, risk tolerances, acceptance criteria and investment decisions.", false],
    ["EPC & OE/EOR", "Design authority, calculations, specifications, routing basis and approved technical design.", false],
    ["OEM & INTEGRATORS / PACKAGERS", "Equipment-package interfaces, internal wiring, approved terminations and warranty boundaries.", false],
    ["ELECTRICAL CONTRACTOR · CHANNEL", "Installation means and methods, pull planning, workface execution, testing support and field feedback.", false],
    ["SOUTHWIRE", "Application support, material and capacity visibility, engineered cable and reel strategy, sequenced delivery and selected field support.", true],
  ];
  let ry = 436;
  rows.forEach(([label, desc, hl]) => {
    if (hl) rect(s, 44, ry + 16, 742, 46, "F0E4D6");
    T(s, 54, ry, 220, label, { size: 8, bold: true, color: hl ? COPPER_DP : INK, track: 1 });
    T(s, 284, ry, 470, desc, { size: 9.5, color: hl ? "3A3C42" : GRAY, leading: 13 });
    hline(s, 54, 756, ry - 32, HAIR, 0.6);
    ry -= 52;
  });
  rect(s, 0, 76, 828, 76, GRAPHITE);
  T(s, 54, 44, 660, ["Southwire connects selected decisions — it does not replace owner, EPC, OEM, Contractor", "or Channel accountability or preference."], { size: 11, bold: true, color: WHITE, leading: 15 });
  bandFooter(s, "10");
}

// ---------------- 11 · who we are
{
  const s = p.addSlide();
  lightFrame(s, "WHO WE ARE", "11", true);
  T(s, 54, 518, 660, ["A family-held American manufacturer —", "from copper rod to finished cable since 1950."], { size: 25, bold: true, leading: 31 });
  T(s, 54, 458, 660, ["Roy Richards founded Southwire after the poles his crews built stood wireless for months after World War II.", "From 12 employees and three secondhand machines in Carrollton, Georgia, Southwire remains family-held", "and vertically integrated — from copper rod through finished cable."], { size: 10, color: GRAY, leading: 15 });
  hline(s, 54, 756, 384, HAIR, 0.75);
  const stats = [["1950", "FOUNDED", INK], ["9,000+", "EMPLOYEES WORLDWIDE", INK], ["$9.7B", "2025 REVENUE · FORBES", COPPER_DP], ["12", "INDUSTRIES SERVED", INK], ["7", "COPPER MARK SITES", INK]];
  const colw = (810 - 108) / 5;
  stats.forEach((st, i) => {
    const x = 54 + i * colw;
    T(s, x, 338, colw, st[0], { size: 26, bold: true, color: st[2] });
    T(s, x, 316, colw, st[1], { size: 6.5, bold: true, color: GRAY, track: 1.1 });
  });
  const proofs = [
    ["COPPER TECHNOLOGY", "Half of the world’s copper rod passes through a Southwire SCR® system."],
    ["U.S. POWER GRID", "We produce half of the wire and cable that moves U.S. electricity."],
    ["AMERICAN HOMES", "Half of American homes contain wiring produced by Southwire."],
  ];
  const colw3 = (810 - 108 - 72) / 3;
  proofs.forEach((pr, i) => {
    const x = 54 + i * (colw3 + 36);
    hline(s, x + 1, x + 27, 276, COPPER, 1.4);
    T(s, x, 256, colw3, pr[0], { size: 8, bold: true, color: COPPER_DP, track: 1.5 });
    T(s, x, 234, colw3 - 12, pr[1], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  const sh = 810 * 670 / 3840;
  img(s, "yard_strip.png", 0, 42 + sh, 828, sh);
  T(s, 54, 20, 300, FOOT, { size: 6.5, color: GRAY_LT });
  T(s, 810 - 54, 20, 60, "11", { size: 6.5, bold: true, color: COPPER, align: "right", track: 1.2 });
}

// ---------------- 12 · the ask
{
  const s = p.addSlide();
  s.background = { color: GRAPHITE };
  const sw = 630 * 548 / 2640;
  img(s, "hex_side_fade.png", 0, PHpt, sw, PHpt + 18);
  s.addShape("line", { x: X(sw + 4), y: 0, w: 0, h: 8.5, line: { color: COPPER, width: 1.4 } });
  const lw = 168, lh = lw * 202 / 943;
  img(s, "lockup_dark_keyed.png", 810 - 54 - lw, PHpt - 48, lw, lh);
  const x0 = sw + 56;
  T(s, x0, 534, 300, "THE ASK", { size: 7.5, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, x0, 490, 560, "ONE SITE WALK.  ONE HOUR.", { size: 29, bold: true, color: WHITE });
  T(s, x0, 450, 560, "NO SALES PRESENTATION.", { size: 29, bold: true, color: WHITE });
  hline(s, x0, x0 + 64, 440, COPPER, 1.2);
  T(s, x0, 414, 580, ["NRG selects the starting scope — one live package, conversion/uprate screen or planned-", "outage replacement — and brings the people closest to execution."], { size: 10.5, color: OFFWHITE, leading: 15 });
  const walk = ["SELECT SCOPE", "WALK THE WORK", "MAP THE RISK", "DECIDE"];
  const wx0 = x0 + 12, wx1 = 810 - 54 - 30, wy = 344, r = 10.5;
  hline(s, wx0, wx1, wy, COPPER, 0.9);
  walk.forEach((wl, i) => {
    const x = wx0 + i * (wx1 - wx0) / 3;
    s.addShape("ellipse", { x: X(x - r), y: Y(wy + r), w: W(2 * r), h: W(2 * r), fill: { color: i === 3 ? COPPER_DP : "32353A" }, line: { type: "none" } });
    T(s, x, wy - 3, 30, String(i + 1), { size: 8.5, bold: true, color: WHITE, align: "center" });
    T(s, x, wy - 26, 130, wl, { size: 6.8, bold: true, color: OFFWHITE, track: 1, align: "center" });
  });
  const rows = [["INPUT", "One live scope"], ["OUTPUT", "Written execution-risk read-back — milestone exposure, route, reel + release constraints"], ["DECISION", "Stop, standardize or define a bounded pilot"]];
  let ry = 268;
  rows.forEach(([label, val]) => {
    T(s, x0, ry, 90, label, { size: 8, bold: true, color: COPPER_LT, track: 1.6 });
    T(s, x0 + 92, ry - 1, 470, val, { size: 10.5, bold: true, color: WHITE });
    hline(s, x0, 756, ry - 13, HAIR_DK, 0.6);
    ry -= 40;
  });
  T(s, x0, 122, 560, "NO PRICING EXERCISE. NO BROAD COMMERCIAL COMMITMENT.", { size: 9, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, x0, 82, 560, "Stephan Hardt   |   Director, Power Generation Solutions", { size: 8.5, bold: true, color: WHITE });
  T(s, x0, 66, 560, "stephan.hardt@southwire.com   |   +1 470-439-8488", { size: 8.5, color: "A8A6A2" });
}

p.author = "Stephan Hardt";
p.title = "Accelerating Time to Power — NRG | Southwire Power Generation Solutions";
p.subject = "SWR-PG-BROCHURE-NRG Rev 01";
p.writeFile({ fileName: "Southwire_PowerGen_Brochure_NRG_Rev01.pptx" }).then(() => console.log("written"));
