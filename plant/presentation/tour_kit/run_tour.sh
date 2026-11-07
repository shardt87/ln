#!/bin/sh
# SW-3X1 guided tour: record every stop, add the captions, write the MP4 clips (macOS / Linux)
set -e
cd "$(dirname "$0")"
npm install
npx playwright install chromium
python3 -m pip install -r requirements.txt
node record_tour.js SW-3X1_viewer.html frames
python3 compose_tour.py frames clips
echo "Done: the clips are in ./clips (SW-3X1_tour_01.mp4 ... and SW-3X1_tour_full.mp4)."
