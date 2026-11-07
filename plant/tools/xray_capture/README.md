# Cable X-ray captures (deck slides 3 and 13, zone locators)

The X-ray pictures in the deck come from the viewer's Cable X-ray mode, captured headless with Playwright, then given
the copper glow.

```
cd plant/tools/xray_capture
npm install                                   # playwright 1.56 + three 0.147 (Chromium: /opt/pw-browsers/chromium)
python3 make_capture_page.py                  # -> capture.html from ../../viewer/index_southwire.html
# reveal / bookend (1440 x 810 at 2x):
CAMSF=cams_wide.json VW=1440 VH=810 DSF=2 SP=$PWD node covcam_w.js     # -> xw_reveal*.jpg, xw_bookend.jpg
# zone locators (960 x 600 at 2x):
CAMSF=cams_loc.json  VW=960  VH=600 DSF=2 SP=$PWD node covcam_w.js     # -> xw_loc01..06.jpg
python3 ../../blender/electrify.py xw_reveal2.jpg ../../renders/cover/xray_reveal.jpg 3
python3 ../../blender/electrify.py xw_bookend.jpg ../../renders/cover/xray_bookend.jpg 9
for k in 01 02 03 04 05 06; do python3 locglow.py xw_loc$k.jpg ../../renders/cover/xray_loc$k.jpg; done
```
Camera fields (cams_*.json): `c` / `t` camera and target (ft), `lens`, `xcol` class colours (already linearised:
the viewer renders line colours linear + ACES), `other` opacity of non-power classes, `xop` overall cable opacity,
`ids` items to light (zone locators), `idcol` / `idop` their colour and opacity, `accent` regex of items to tint.
`cams_loc01.json` is the grid-zone locator with the switchyard pad included.

Training deck slide 24 (copper X-ray of the CC2 view, the same camera as the Blender CC2 render):
```
PAGE=$PWD/capture.html CAMSF=cams_cc.json VW=1440 VH=810 DSF=2 SP=<scratch> node covcam_w.js
python3 ../../blender/electrify.py <scratch>/xw_cc2.jpg ../../renders/training/XR_CC2_copper.jpg 3
```
