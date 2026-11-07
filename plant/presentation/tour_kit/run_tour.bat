@echo off
REM SW-3X1 guided tour: record every stop, add the captions, write the MP4 clips (Windows)
cd /d "%~dp0"
call npm install || goto :err
call npx playwright install chromium || goto :err
python -m pip install -r requirements.txt || goto :err
node record_tour.js SW-3X1_viewer.html frames || goto :err
python compose_tour.py frames clips || goto :err
echo.
echo Done: the clips are in the "clips" folder (SW-3X1_tour_01.mp4 ... and SW-3X1_tour_full.mp4).
pause
exit /b 0
:err
echo Something failed - see the message above.
pause
exit /b 1
