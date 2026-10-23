# Render queue: full-quality renders to run at the end

Owner (Oct 22): work at preview quality for now (14 samples, scale 50, ~1-2 min a view). Do the full-quality pass
for everything on this list in one batch once the content is settled.

Full-quality command (from `plant/`, absolute paths; ~3-5 min a view at 32 samples):

    SP=<scratchpad>; $SP/bvenv/bin/python /home/user/ln/plant/blender/SW-3X1_Rev14_blender_build.py \
        --views <K1,K2,...> --style pro --set epic --samples 32 --scale 100 --out $SP/full
    $SP/bvenv/bin/python /home/user/ln/plant/blender/finish_pro.py $SP/full
    cp $SP/full/*_pro_clean.jpg renders/boilers_full/   # deck_boilers.py prefers these over renders/boilers
    python3 blender/deck_boilers.py

Shot rule: hide the plant cable-tray / IPB item (`hide=("Cable trays and isolated",)`) when it clutters a close-up. Keep
it where tray congestion is the point of the shot. Process piping stays visible.

| View | Used on | Status | Note |
|---|---|---|---|
| RA1 | Boilers slide 6 (main), slide 8 (R2A node) | preview only | plant rack hidden, R2A interconnection trays shown (Oct 23) |
| RA2 | Boilers slide 6 (inset) | full done Oct 22 | re-render only if the R2A interior changes |
| ELV1 | Boilers slide 5 | preview only | HRSG 2/3, all stacks and the outage crane kept in colour, Oct 22; the stale full render was deleted |
| CM1 / CM2 / CM3 / CM4 | Boilers slide 7 (CEMS: cutaway main; exterior, stack-platform and stack-top insets) | preview only | new Oct 23 |
| RA3 | Boilers slide 6 (interconnection inset) | preview only | new Oct 23: MV tray to T-R2A, EL 42 control tray into the roof riser; process piping hidden |
