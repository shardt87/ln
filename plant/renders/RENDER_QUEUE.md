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
| RA1 | Boilers slide 9 (main), slide 11 (R2A node) | preview only | plant rack hidden, R2A interconnection trays shown (Oct 23) |
| RA2 | Boilers slide 9 (inset) | full done Oct 22 | re-render only if the R2A interior changes |
| ELV1 | Boilers slide 8 | preview only | HRSG 2/3, all stacks and the outage crane kept in colour, Oct 22; the stale full render was deleted |
| CM1 / CM2 / CM3 / CM4 | Boilers slide 10 (CEMS: cutaway main; exterior, stack-platform and stack-top insets) | preview only | new Oct 23; Steam Street layout (spine rack, control room, steam storage, bay plates) |
| RA3 | Boilers slide 9 (interconnection inset) | preview only | new Oct 23: MV tray to T-R2A, EL 42 control tray into the roof riser; process piping hidden |
| BR1 / BR2 / BR3 (BR1, BR2 re-shot Oct 23 with the heater bay) | Boilers slide 4 (Boiler Row: aerial main; BR3 electric-boiler cutaway inset; BR2 spine close-up for marketing); Nov 11 tour | preview only | new Oct 23; Steam Street layout (spine rack, control room, steam storage, bay plates) |
| BR4 / BR5 | BR5: Boilers slide 4 inset (burner front close-up); BR4: back bay (talking points, marketing) | preview only | new Oct 23: UB-1 13.8 kV switchgear + SST-A/B, gas metering; burner hardware |
| BR6 / BX1 / BX2 | BR6: UB-1 cells on the shared CCS cooling tower + CW pumps (marketing); BX1: boilers slide 1 (package boiler, back on its drawn spot); BX2 | preview only | Oct 23: AB-1 moved and moved back; full render needed (the old one was deleted) |
| BR7 | Burner front, wide (stair tower, braces, scanner cooling air, lights, operators): marketing / MC-HL story | preview only | new Oct 23 |
| BR8 | Boiler Row west: package boiler AB-1, condensate storage, EDG | preview only | new Oct 23 |
| BR9 | UB-1 CEMS shelter at the stack (north side, by the road) | preview only | new Oct 23 |
| E95 / E96 | EPC brochure (skid pre-wire workstation) | full render stale | Oct 23: workstation moved beside the inlet chillers; renders/epic E95 / E96 still show the old spot; re-render at full quality, then rebuild the EPC brochure |
| MP1 / MP2 | Nov 11 stop 5 (modular yard), marketing: AX-1 + IG-1 packages; AX-1 module joint with plug-in interconnects | preview only | new Oct 24 |
| E43 / E89 | Zone slides 12 (chillers) and 3 (reel staging & prefab) | check + full render | Oct 24: the skid pre-wire workstation now sits between the reel yard and the chillers and may be in both shots |

## Oct 24: training deck, combined cycle
- **CC1** (blender/pro_look.py): the power block from above with the hall roof off. It is the base of the training deck's combined-cycle slide (slide 15, `c_combined`; the markers are placed for this framing, so do not move the camera). The deck uses the preview at renders/training/CC1_pro_clean.jpg; replace it with the full render.
- **CC2** replaces CC1 as the deck's base: the same view pulled back, used by the four-slide combined-cycle build (slides 15-18, `c_cc`). The overlays come from projecting model coordinates with CC2's eye, target and lens, so keep the camera exactly as it is. Preview at renders/training/CC2_pro_clean.jpg. CC1 is no longer used.

## Oct 25: training deck picture pass (re-render at full quality so the deck is sharp)
Views now on training slides that only exist as Oct 8-13 previews: E10, E16, E41, E47, E82, E83, E84, E85, E86, E88, E89, E92, E108, E109, E110, E123 (nextgen). E19-E24, E26, E31, E48 and E7 already have Oct 17 full renders.

## Oct 25: K1 re-render (current plant)
- **K1** (cover/K1_pro.png, Oct 17) is out of date: it predates Boiler Row, AX-1 / IG-1, the CEMS shelters and the latest power-block detail. Re-render it at full quality on the same camera; it is the V3 hero on training slide 5 (crop 50% 50%), the campus overview, the brochure cover and the deck dividers. Check the crop still shows the LNG carrier, jetty and terminal.

## Oct 26: contractor area on the laydown pad
- **E126 / E127 / E129** (contractor_yard.py) and **E128 / E130** (fitout_products.py, admin fit-out): preview only (16 spp, 60 %); render at full quality in the batch.
- **E132 / E133** (skid_prewire.kits): standardized kits on the pre-wire pad; preview only.
- **E134 / E135** (standard_kits.py): kits 4 and 5; preview only.
- **E136** (skid_prewire.kit_fitup): kit 1 fit-up on LOS-2; preview only. E95 / E96 now show LOS-2 bare with the kit going on.
- **E137** (skid_prewire ready row: CFS-2 + LOS-2 kit 1): preview only.
- **E138** (pre-wire pad east: power skid, IA skid, CEMS shelter): preview only.
- **E139** (bfp_kit: BFP-1B terminal box with kit 2): preview only; fill lights in the camera.
- **E140 / E141 / E142** (prefab_electrical: lineups, panel shop, open enclosure): preview only.
- **E143 / E144** (modular gas genset blocks; genset_blocks block 1 trench): preview only. E144 is a tight corridor shot between GBS-1 / GBT-1 and the gensets.
- **E145** (genset row, photo angle): preview only.
- **E143 / E144 / E145** re-aimed Oct 26 for the reworked modular gas blocks (5 x 500 kW per block, 35 kV loop to SWG-MY): previews only.
- **E146** (golden hour from the south-east over the modular gas blocks; Oct 26): preview at 24 spp, scale 70.
- **E147 / E148** (technology row, Oct 27): preview only.
- **E149 / E150** (AX-1 / IG-1 rebuilt, Oct 27): preview only.
