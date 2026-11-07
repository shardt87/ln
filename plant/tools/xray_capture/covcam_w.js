// X-ray captures at any viewport (VW x VH): cam.xcol class colours, cam.other opacity for non-power classes,
// cam.xop overall cable opacity, cam.ids items to light in an accent colour (zone locators).
const { chromium } = require('playwright');
const SP = process.env.SP, cams = JSON.parse(require('fs').readFileSync(process.env.CAMSF,'utf8')), sc = +(process.env.DSF||1);
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium', args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const ctx = await b.newContext({viewport:{width:+process.env.VW,height:+process.env.VH}, deviceScaleFactor:sc, colorScheme:'dark'});
  const p = await ctx.newPage();
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r=>r.abort());
  await p.goto('file://'+(process.env.PAGE||SP+'/capture.html'),{waitUntil:'commit',timeout:180000});
  await p.waitForFunction(()=>window.tourAPI && document.getElementById('loading').hidden, null, {timeout:600000});
  for (const cam of cams) {
    const d = await p.evaluate(cam=>{
      if(cam.xcol){ Object.assign(window.__vw.XCOL, cam.xcol); }
      const s=tourAPI.stop(50); Object.assign(s,cam); s.drift=0; window.__rec=true; window.__clock=0; tourAPI.start(50); tourAPI.advance(30000);
      if(cam.ghost){ window.__vw.ghostMat.opacity=cam.ghost; }
      const {itemMeshes,MODEL}=window.__vw;
      if(window.__accMeshes){ window.__accMeshes.forEach(([m,mat])=>m.material=mat); }
      window.__accMeshes=[];
      const hide=(re,mat)=>{ for(const id in itemMeshes){ const it=MODEL.items.find(q=>q.id===id); if(it && re(it)) (itemMeshes[id]||[]).forEach(m=>{ if(m.userData.xmat){ window.__accMeshes.push([m,m.material]); m.material=mat; } }); } };
      if(cam.accent){ const acc=new THREE.MeshBasicMaterial({color:0xe0a070, transparent:true, opacity:.30, depthWrite:false});
        const re=new RegExp(cam.accent,'i'); hide(it=>re.test(it.name),acc); }
      if(cam.ids){ const ids=new Set(cam.ids); const acc=new THREE.MeshBasicMaterial({color:cam.idcol||0xf0a060, transparent:true, opacity:cam.idop||.5, depthWrite:false});
        hide(it=>ids.has(it.id),acc); }
      if(cam.xcol){ for(const g of window.__vw.XR.groups){ const pw=/^(HV|MV|LV|Portable)/.test(g.userData.cls);
          g.material.opacity = (pw ? 1.0 : (cam.other ?? .35)) * (cam.xop ?? 1); } }
      tourAPI.advance(30000); return tourAPI.frame(30001,.93); }, cam);
    require('fs').writeFileSync(`${SP}/xw_${cam.tag}.jpg`, Buffer.from(d.split(',')[1],'base64'));
    console.log('wrote', cam.tag);
  }
  await b.close();
})();
