// SK-3X1 Rev 14 - GT train 1 bay: GT1 + generator, HRSG 1 + stack, FH-1, GSU-1 / UAT-1 bay, R2A, BFP/SCR blowers.
// Coordinates in feet from the verified model (X east, Y north, Z up).
// D: the bay data (plant/threejs/gt1_bay.json), provided by the caller

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, width / height, 2, 20000);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(width, height); renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
const CX = 630, CY = 560;
const P = (x, y, z) => [x - CX, z, -(y - CY)];
// sky
{ const c = document.createElement('canvas'); c.width = 4; c.height = 256; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#6f9cc9'); gr.addColorStop(.6, '#c8dbeb'); gr.addColorStop(1, '#eef2f3');
  g.fillStyle = gr; g.fillRect(0, 0, 4, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; scene.background = t; }
scene.fog = new THREE.Fog(0xdfe8ee, 900, 2600);
scene.add(new THREE.HemisphereLight(0xe6eef8, 0x7a7f6c, 1.6));
const sun = new THREE.DirectionalLight(0xfff2dc, 2.4); sun.position.set(-260, 420, 240); sun.castShadow = true;
sun.shadow.mapSize.set(4096, 4096); Object.assign(sun.shadow.camera, { left: -420, right: 420, top: 420, bottom: -420, near: 50, far: 1500 });
sun.shadow.bias = -0.0003; sun.shadow.normalBias = .3; scene.add(sun);
// procedural textures
function tex(size, draw) { const c = document.createElement('canvas'); c.width = c.height = size; draw(c.getContext('2d'), size);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; t.colorSpace = THREE.SRGBColorSpace; return t; }
let sd = 7; const rnd = () => ((sd = Math.imul(sd ^ sd >>> 15, 0x2c1b3c6d) + 0x297a2d39 | 0) >>> 0) / 4294967296;
const T = {
  clad: tex(256, (g, s) => { for (let i = 0; i < 16; i++) { const x = i * s / 16, gr = g.createLinearGradient(x, 0, x + s / 16, 0);
    gr.addColorStop(0, '#e2e6e8'); gr.addColorStop(.2, '#fff'); gr.addColorStop(.6, '#f0f2f3'); gr.addColorStop(.85, '#cfd5d8'); gr.addColorStop(1, '#e2e6e8');
    g.fillStyle = gr; g.fillRect(x, 0, s / 16, s); } }),
  concrete: tex(256, (g, s) => { g.fillStyle = '#f1f1ef'; g.fillRect(0, 0, s, s); for (let i = 0; i < 6000; i++) { const v = 255 - rnd() * 40 | 0; g.fillStyle = `rgb(${v},${v},${v})`; g.fillRect(rnd() * s, rnd() * s, 2, 2); }
    g.strokeStyle = 'rgba(0,0,0,.1)'; g.strokeRect(1, 1, s - 2, s - 2); }),
  gravel: tex(256, (g, s) => { g.fillStyle = '#ebeae6'; g.fillRect(0, 0, s, s); for (let i = 0; i < 14000; i++) { const v = 255 - rnd() * 95 | 0; g.fillStyle = `rgb(${v},${v},${v})`; g.fillRect(rnd() * s, rnd() * s, 2, 2); } }),
  grating: tex(128, (g, s) => { g.fillStyle = '#f4f4f4'; g.fillRect(0, 0, s, s); g.strokeStyle = '#8d959a'; g.lineWidth = 2; for (let i = 0; i <= s; i += 8) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, s); g.stroke(); } }),
  fins: tex(128, (g, s) => { g.fillStyle = '#fff'; g.fillRect(0, 0, s, s); for (let i = 0; i < s; i += 4) { g.fillStyle = i % 8 ? '#d4dad8' : '#b3bcb9'; g.fillRect(i, 0, 1.5, s); } }),
};
const SURF = { clad: [T.clad, 24, .6, .1], concrete: [T.concrete, 30, .92, 0], gravel: [T.gravel, 18, 1, 0], grating: [T.grating, 6, .6, .4], fins: [T.fins, 6, .55, .3],
  metal: [null, 0, .45, .18], paint: [null, 0, .6, .05], ceramic: [null, 0, .28, 0], copper: [null, 0, .42, .35], glass: [null, 0, .3, .1] };
const CLASS = { hall: 'glass', ehouse: 'clad', filter: 'clad', hrsg: 'clad', roof: 'clad', building: 'clad', concrete: 'concrete', pad: 'concrete', road: 'gravel', gravel: 'gravel',
  grating: 'grating', bundle: 'fins', radiator: 'fins', insulator: 'ceramic', copper: 'copper', copper_dark: 'copper', steel: 'metal', pipe: 'metal', stack: 'metal',
  duct: 'metal', machine: 'metal', fan: 'metal', conductor: 'metal', fence: 'metal' };
const buf = {};
function B(cls) { return buf[cls] || (buf[cls] = { p: [], c: [], uv: [] }); }
function tri(b, a, bb, c, col, tile) { for (const v of [a, bb, c]) { b.p.push(...P(...v)); b.c.push(col.r, col.g, col.b); }
  if (tile) { const n = [(bb[1] - a[1]) * (c[2] - a[2]) - (bb[2] - a[2]) * (c[1] - a[1]), (bb[2] - a[2]) * (c[0] - a[0]) - (bb[0] - a[0]) * (c[2] - a[2]), (bb[0] - a[0]) * (c[1] - a[1]) - (bb[1] - a[1]) * (c[0] - a[0])].map(Math.abs);
    for (const v of [a, bb, c]) { let u, w; if (n[2] >= n[0] && n[2] >= n[1]) { u = v[0]; w = v[1]; } else if (n[0] >= n[1]) { u = v[1]; w = v[2]; } else { u = v[0]; w = v[2]; } b.uv.push(u / tile, w / tile); } }
  else b.uv.push(0, 0, 0, 0, 0, 0); }
function quad(b, a, bb, c, d, col, t) { tri(b, a, bb, c, col, t); tri(b, a, c, d, col, t); }
const COL = D.c.map(h => new THREE.Color(h));
function classOf(ci, kind) { let k = CLASS[D.k[ci]] || 'paint'; if (kind === 1 && ['clad', 'concrete', 'fins', 'grating'].includes(k)) k = 'paint'; return k; }
function box(x0, y0, z0, x1, y1, z1, ci) { const k = classOf(ci, 0), b = B(k), col = COL[ci], t = SURF[k][1];
  const v = (i) => [i & 1 ? x1 : x0, i & 2 ? y1 : y0, i & 4 ? z1 : z0];
  for (const f of [[0, 2, 3, 1], [4, 5, 7, 6], [0, 1, 5, 4], [2, 6, 7, 3], [0, 4, 6, 2], [1, 3, 7, 5]]) quad(b, v(f[0]), v(f[1]), v(f[2]), v(f[3]), col, t); }
function rod(ax, ay, az, bx, by, bz, r1, r2, ci, n) { const k = classOf(ci, 1), b = B(k), col = COL[ci];
  const A = new THREE.Vector3(ax, ay, az), Bv = new THREE.Vector3(bx, by, bz), d = Bv.clone().sub(A).normalize();
  const ref = Math.abs(d.x) < .9 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0), u = d.clone().cross(ref).normalize(), w = d.clone().cross(u);
  const ring = (C, r) => [...Array(n).keys()].map(i => { const a = 2 * Math.PI * i / n; return C.clone().addScaledVector(u, r * Math.cos(a)).addScaledVector(w, r * Math.sin(a)).toArray(); });
  const s0 = ring(A, r1), s1 = ring(Bv, r2);
  for (let i = 0; i < n; i++) { const j = (i + 1) % n; quad(b, s0[i], s0[j], s1[j], s1[i], col, 0); tri(b, A.toArray(), s0[j], s0[i], col, 0); tri(b, Bv.toArray(), s1[i], s1[j], col, 0); } }
function hexa(v, ci) { const k = classOf(ci, 2), b = B(k), col = COL[ci], t = SURF[k][1]; const q = i => v.slice(i * 3, i * 3 + 3);
  for (const f of [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]) quad(b, q(f[0]), q(f[1]), q(f[2]), q(f[3]), col, t); }
function prism(x0, y0, z0, x1, y1, z1, ci, rx) { const k = classOf(ci, 3), b = B(k), col = COL[ci], t = SURF[k][1]; let v;
  if (rx) { const ym = (y0 + y1) / 2; v = [[x0, y0, z0], [x0, y1, z0], [x0, ym, z1], [x1, y0, z0], [x1, y1, z0], [x1, ym, z1]]; }
  else { const xm = (x0 + x1) / 2; v = [[x0, y0, z0], [x1, y0, z0], [xm, y0, z1], [x0, y1, z0], [x1, y1, z0], [xm, y1, z1]]; }
  tri(b, v[0], v[2], v[1], col, t); tri(b, v[3], v[4], v[5], col, t); quad(b, v[0], v[3], v[5], v[2], col, t); quad(b, v[1], v[2], v[5], v[4], col, t); quad(b, v[0], v[1], v[4], v[3], col, t); }
for (const e of D.p) { if (e[0] === 0) box(...e.slice(1, 7), e[7]); else if (e[0] === 1) rod(...e.slice(1, 9), e[9], e[10] || 16);
  else if (e[0] === 2) hexa(e.slice(1, 25), e[25]); else prism(...e.slice(1, 7), e[7], e[8]); }
for (const [z, w, h, ci, pts] of D.r) for (let i = 0; i < pts.length - 1; i++) { const [ax, ay] = pts[i], [bx, by] = pts[i + 1];
  box(Math.min(ax, bx) - w / 2, Math.min(ay, by) - w / 2, z - h / 2, Math.max(ax, bx) + w / 2, Math.max(ay, by) + w / 2, z + h / 2, ci); }
for (const [k, b] of Object.entries(buf)) { const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(b.p, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(b.c, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(b.uv, 2)); g.computeVertexNormals();
  const s = SURF[k]; const m = new THREE.MeshStandardMaterial({ vertexColors: true, map: s[0], roughness: s[2], metalness: s[3] });
  if (k === 'glass') Object.assign(m, { transparent: true, opacity: .22, depthWrite: false, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(g, m); mesh.castShadow = k !== 'glass'; mesh.receiveShadow = true; scene.add(mesh);
  if (k !== 'glass' && b.p.length < 900000) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(g, 35), new THREE.LineBasicMaterial({ color: 0x27313a, transparent: true, opacity: .18 })); scene.add(e); } }
{ const g = new THREE.PlaneGeometry(4000, 4000); g.rotateX(-Math.PI / 2); const t = T.gravel.clone(); t.repeat.set(160, 160); t.needsUpdate = true;
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: 0xcfd2c8, map: t, roughness: 1 })); m.position.y = -.4; m.receiveShadow = true; scene.add(m); }
const controls = new OrbitControls(camera, renderer.domElement); controls.enableDamping = true; controls.maxPolarAngle = Math.PI * .495;
controls.target.set(0, 45, 60); camera.position.set(-330, 230, 330);
function animate() { requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
animate();
