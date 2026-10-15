// Record the viewer's guided tour frame by frame (deterministic clock, frames read from the canvas).
//   node record_tour.js PAGE.html OUTDIR [stops e.g. 0,1,2] [fps] [dwell_ms]
// Each stop is one clip: the flight in from the previous stop, then the dwell with its slow drift.
// Captions are composited afterwards by compose_tour.py (frames here are the 3D view only).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [page, out, stopsArg, fpsArg, dwellArg] = process.argv.slice(2);
const FPS = +(fpsArg || 24), DWELL = +(dwellArg || 6000);
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport: {width: 1920, height: 1080}});
  await p.goto('file://' + path.resolve(page), {waitUntil: 'commit', timeout: 180000});
  await p.waitForFunction(() => window.tourAPI && document.getElementById('loading').hidden, null, {timeout: 600000});
  await p.addStyleTag({content: '#tour{display:none!important} .stamp{display:none!important}'});
  await p.evaluate(() => { window.__clock = 0; tourAPI.start(0); });
  await p.waitForTimeout(800);
  const n = await p.evaluate(() => tourAPI.n());
  const stops = stopsArg ? stopsArg.split(',').map(Number) : [...Array(n).keys()];
  for (const i of stops) {
    const dir = path.join(out, 'stop_' + String(i).padStart(2, '0'));
    if (fs.existsSync(path.join(dir, 'meta.json'))) { console.log('skip', i); continue; }
    fs.mkdirSync(dir, {recursive: true});
    let t = 100000 * (i + 1);
    if (i > 0) {                                    // arrive at the previous stop and let it drift for the dwell
      const d0 = await p.evaluate(([j, t]) => { window.__rec = true; window.__clock = t; return tourAPI.go(j); }, [i - 1, t]);
      t += d0 + DWELL; await p.evaluate(t => tourAPI.advance(t), t);
      await p.evaluate(t => tourAPI.advance(t), t + 1);
      t += 2;
    } else {
      await p.evaluate(t => { window.__rec = true; window.__clock = t; }, t);
    }
    const dur = await p.evaluate(([i, t]) => { window.__clock = t; return tourAPI.go(i); }, [i, t]);
    const nf = Math.ceil((dur + DWELL) * FPS / 1000);
    const t0 = Date.now();
    for (let f = 0; f < nf; f++) {
      const fn = path.join(dir, 'f_' + String(f).padStart(4, '0') + '.jpg');
      const d = await p.evaluate(([tt]) => tourAPI.frame(tt, .93), [t + f * 1000 / FPS]);
      fs.writeFileSync(fn, Buffer.from(d.split(',')[1], 'base64'));
      if (f % 24 === 0) console.log('stop', i, 'frame', f, '/', nf, ((Date.now() - t0) / (f + 1) / 1000).toFixed(1), 's/frame');
    }
    fs.writeFileSync(path.join(dir, 'meta.json'), JSON.stringify({i, fps: FPS, fly_ms: dur, dwell_ms: DWELL, frames: nf}));
    console.log('done stop', i);
  }
  await b.close();
})();
