# SK-3X1 guided tour kit

Everything needed to present the SK-3X1 3D campus tour and to record it as MP4 clips on your own computer.
Conceptual illustration, not engineered.

## What is in the kit

| File | What it is |
|---|---|
| `SK-3X1_viewer.html` | The 3D viewer with the guided tour (Southwire build). Opens in Chrome or Edge. |
| `tour.json` | The tour stops: camera, section, title and the Equipment / System / Cable captions. |
| `record_tour.js` | Records each stop frame by frame (flight in, then the dwell). |
| `compose_tour.py` | Adds the deck-style captions and writes the H.264 MP4 clips. |
| `fonts/` | Barlow / Barlow Condensed for the captions. |
| `run_tour.bat` / `run_tour.sh` | One-click: install, record, caption, encode. |

## Present it live (no install)

1. Double-click `SK-3X1_viewer.html` (Chrome or Edge, internet on: it loads three.js and the fonts).
2. Click **▶ Tour** (top left of the 3D view). The view goes full screen.
3. **→ / Space / PageDown** next stop, **← / PageUp** back, **Esc** exit. A presentation clicker works.
4. In Teams, share the browser **window**.

## Record the clips

Needs: **Node.js 18+** (nodejs.org) and **Python 3.9+** (python.org, tick "Add to PATH"). A graphics card makes it fast.

- **Windows:** double-click `run_tour.bat`.
- **Mac / Linux:** `./run_tour.sh`

A Chromium window opens and steps through the tour by itself; leave it alone until it closes. With a normal laptop
GPU the 51 stops take roughly 30 to 60 minutes. Output: `clips/SK-3X1_tour_01.mp4` ... `SK-3X1_tour_51.mp4` (one per
stop, 1080p, 24 fps, PowerPoint-ready) and `clips/SK-3X1_tour_full.mp4`.

Options:
- Only some stops: `node record_tour.js SK-3X1_viewer.html frames 0,1,2` (stop numbers start at 0), then
  `python compose_tour.py frames clips`.
- Smoother / longer: `node record_tour.js SK-3X1_viewer.html frames "" 30 6000` (30 fps, 6 s dwell per stop).
- Interrupted? Run it again: finished stops and frames are kept.
- Re-make one clip (e.g. after changing a caption in `tour.json`): delete it from `clips/` and run `compose_tour.py` again.
- No graphics card: set `SOFTWARE_GL=1` first (much slower).

## Change the tour

Edit `tour.json`: `c` = camera position, `t` = target (plant feet: x east, y north, z up), `lens` in mm, `sec` /
`title` / `eq` / `sys` / `cab` = caption. The viewer in this kit has the tour built in; caption edits affect the
recorded clips (compose step). To change the live viewer's tour, ask for a rebuilt `SK-3X1_viewer.html`.
