"""INTERNAL ONLY. Not part of the ER-RB deliverables, not attached to any named project or bid.
Sanity line: for a given campus size, what 35 kV loop length does 1.2M conductor-ft of 750 kcmil Al imply, and does it
reconcile with the loop length measured off the generic model?"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import takeoff as TO

FT = 1_200_000
lines = ["INTERNAL ONLY - sanity line (generic; not attached to any named project)", ""]
for mw in (250, 500, 1000):
    t = TO.takeoff(mw)
    r = {d["layer"]: d for d in t["rollup"]}
    loops, ties, fdr = r["L3"]["conductor_ft"], r["L4"]["conductor_ft"], r["L5"]["conductor_ft"]
    g = t["params"]["n_groups"]
    implied_trench = FT / 3                     # 3 x 1/C per loop circuit
    model_trench = loops / 3
    lines.append(f"{mw:5d} MW: model loops {loops:,} cond-ft (+ ties {ties:,}, + feeders {fdr:,} ASSUMED) = "
                 f"{(loops + ties + fdr):,}; per group {model_trench / g:,.0f} ft of loop route.")
    lines.append(f"         1.2M cond-ft = {implied_trench:,.0f} ft of 3-conductor loop route = "
                 f"{implied_trench / g:,.0f} ft per group at this group count; ratio to model "
                 f"{FT / (loops + ties + fdr):.1f}x (loops+ties+feeders) -> "
                 f"{'RECONCILES' if 0.7 < FT / (loops + ties + fdr) < 1.4 else 'DOES NOT RECONCILE'}")
lines += ["", "Reading: at the generic module's density, 1.2M conductor-ft of 750 Al does not reconcile with loops + ties +",
          "feeders for a 250-500 MW campus. Either the routes are much longer than this compact layout (home runs to a remote",
          "switchyard, wider block spacing), runs are paralleled, the quantity covers more than the loops (feeders, other",
          "sites), or it includes margin. Ask ER engineering for loop route length per group; do not quote this line."]
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sanity_check.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
