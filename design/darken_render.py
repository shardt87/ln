"""Dark-studio version of the raw plant render (gradient sky, cream slab).

usage: python3 darken3.py render-light.png render-dark.png
"""
import sys, time
from PIL import Image
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.filters import sobel

SRC, OUT = sys.argv[1], sys.argv[2]
t0 = time.time()
img = np.array(Image.open(SRC).convert('RGB')).astype(np.float32)
H, W, _ = img.shape
R, G, B = img[..., 0], img[..., 1], img[..., 2]
lum = img.mean(axis=2); sat = img.max(axis=2) - img.min(axis=2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
S = W / 2000.0                                   # preview-pixel scale
mf = ndi.uniform_filter(lum, 7); mf2 = ndi.uniform_filter(lum ** 2, 7)
texture = np.sqrt(np.maximum(mf2 - mf * mf, 0))

# ---------------------------------------------------------------- sky
# the sky is a smooth 2-D gradient: fit a quadratic to the sky connected to the top
# edge, then anything within a few levels of that fit (and smooth) is sky - this also
# catches the sky patches enclosed by the power lines.
sky_like = (R - B <= -1) & (R - B >= -16) & (lum >= 210) & (sat <= 14) & (texture < 4)
lab, n = ndi.label(sky_like)
top = np.unique(lab[0]); top = top[top != 0]
sky_top = np.isin(lab, top)
step = 24
ys, xs = np.nonzero(sky_top[::step, ::step]); ys = ys * step; xs = xs * step
A = np.stack([np.ones_like(xs), xs, ys, xs * xs, xs * ys, ys * ys], axis=1).astype(np.float64) / np.array([1, W, H, W * W, W * H, H * H])
coef = [np.linalg.lstsq(A, img[ys, xs, c].astype(np.float64), rcond=None)[0] for c in range(3)]
Afull = np.stack([np.ones_like(xx), xx, yy, xx * xx, xx * yy, yy * yy], axis=-1).astype(np.float64) / np.array([1, W, H, W * W, W * H, H * H])
fit = np.stack([Afull @ coef[c] for c in range(3)], axis=-1).astype(np.float32)
resid = np.abs(img - fit).max(axis=2)
print('sky fit residual on top-connected sky: p50/p99', np.percentile(resid[sky_top], [50, 99]))
sky_like2 = (resid < 4) & (texture < 4) & (yy < int(1000 * S))
sky_seed = ndi.binary_erosion(sky_like2, iterations=4)
lab, n = ndi.label(sky_seed); sizes = ndi.sum(sky_seed, lab, range(1, n + 1))
sky_seed = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 100 * S])
sky_like = sky_like2

# ---------------------------------------------------------------- floor
y0 = int(820 * S)
slab   = (R - B >= 3) & (lum >= 225) & (sat <= 12)
slab_side = (yy > int(1030 * S)) | ((xx < int(260 * S)) & (yy > int(880 * S)))   # blown-out slab faces
white  = (lum >= 250) & (sat <= 3) & slab_side
lot    = (sat <= 9) & (lum >= 100) & (lum <= 150)
dark   = (sat <= 8) & (lum >= 35) & (lum <= 75)
padw   = (R - B >= 9) & (R - B <= 16) & (sat <= 16) & (lum >= 170) & (lum <= 200)
apron  = (R - B >= -14) & (R - B <= -5) & (sat <= 14) & (lum >= 170) & (lum <= 215) & (xx > int(1350 * S))
pad_box = np.zeros((H, W), bool); pad_box[int(850 * S):int(1035 * S), int(700 * S):int(1310 * S)] = True
padall = pad_box & (R - B >= 3) & (R - B <= 18) & (sat <= 20) & (lum >= 100) & (lum <= 235)
floor_like = (slab | white | lot | dark | padw | apron | padall) & ((yy > y0) | ((xx > int(1700 * S)) & (yy > int(700 * S))))
floor_like[int(1000 * S):, int(1690 * S):] = False           # small building bottom right
floor_seed = floor_like & ((texture < 6) | pad_box)
floor_seed = ndi.binary_erosion(floor_seed, iterations=3)
bridged = ndi.binary_dilation(floor_seed, iterations=int(6 * S))   # bridge thin poles for the size test
lab, n = ndi.label(bridged); sizes = ndi.sum(bridged, lab, range(1, n + 1))
floor_seed &= np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 4000 * S])

# ---------------------------------------------------------------- objects + watershed
# only confident object colours seed objects: saturated, bluish steel/containers,
# beige walls, near-black, and neutral whites above the slab's blown-out band.
# Ground in soft shadow is left unseeded so the watershed can give it to the floor.
broad_floor = (sat <= 14) & (lum >= 60) & (((R - B >= -3) & (yy > y0)) | ((R - B >= -10) & (xx > int(1700 * S)) & (yy > int(700 * S))))
veh_box = np.zeros((H, W), bool)
veh_box[int(925 * S):int(1020 * S), int(1075 * S):int(1235 * S)] = True   # white truck
veh_box[int(885 * S):int(1065 * S), int(1435 * S):int(1615 * S)] = True   # parked cars
white_obj = (lum >= 205) & (sat <= 4) & (R - B <= 2) & (R - B >= -1) & veh_box
obj_seed = ndi.binary_erosion(~(sky_like | broad_floor | floor_like), iterations=3) | (sat > 30) | white_obj \
           | ndi.binary_erosion(lum < 30, iterations=2)
obj_seed &= ~(sky_seed | floor_seed)
markers = np.zeros((H, W), np.int32)
markers[obj_seed] = 1; markers[sky_seed] = 2; markers[floor_seed] = 3
grad = sobel(lum / 255.0) + 0.5 * (sobel(R / 255.0) + sobel(G / 255.0) + sobel(B / 255.0))
labels = watershed(grad, markers)
import os
if os.environ.get('PROBE'):
    for (py, px) in [(777, 1905), (790, 1959), (799, 1991), (811, 1917), (819, 1974), (837, 1992)]:
        Y, X = int(py * S), int(px * S)
        print('probe', (py, px), img[Y, X], 'floor_like', bool(floor_like[Y, X]), 'fseed', bool(floor_seed[Y, X]), 'obj', bool(obj_seed[Y, X]), 'skyseed', bool(sky_seed[Y, X]), 'sky_like', bool(sky_like[Y, X]), 'tex', round(float(texture[Y, X]), 1), 'label', int(labels[Y, X]))
sky = labels == 2
floor = labels == 3
lab, n = ndi.label(floor); sizes = ndi.sum(floor, lab, range(1, n + 1))
floor = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 4000 * S])
model = ~sky
print('masks done', round(time.time() - t0), 's  sky', round(float(sky.mean()), 3), 'floor', round(float(floor.mean()), 3))
np.save('masks3.npy', np.stack([sky, floor]))

# ---------------------------------------------------------------- backdrop
cx, cy = 0.62 * W, 0.66 * H
r = np.sqrt(((xx - cx) / (0.6 * W)) ** 2 + ((yy - cy) / (0.6 * H)) ** 2)
glow = np.clip(1.0 - r, 0, 1) ** 1.6
base = 17 + 26 * glow
base = base * (1 - 0.35 * np.clip((yy / H - 0.78) / 0.22, 0, 1))
rng = np.random.default_rng(7)
noise = rng.normal(0, 1.0, (H, W)).astype(np.float32)
bgcol = np.clip(np.stack([base + noise, base + noise, base + noise + 1.0], axis=2), 0, 255)

# ---------------------------------------------------------------- model grading
m = (img - 128.0) * 1.14 + 128.0
m = m * 0.82
hi = np.clip((m.mean(axis=2) - 120.0) / 100.0, 0, 1)[..., None]
m = m + hi * np.array([14, 6, -6], np.float32)
warm = (R > B + 40) & (R > G + 10)
mm = m.mean(axis=2, keepdims=True)
m = np.where(warm[..., None], (m - mm) * 1.25 + mm * 1.05, m)
out = np.clip(m, 0, 255)

# ---------------------------------------------------------------- floor -> dark charcoal
floor_a = ndi.gaussian_filter(floor.astype(np.float32), 1.0 * S)
fl = out.mean(axis=2)
target = 22.0 + fl * 0.15
floor_col = out * (target / np.maximum(fl, 1.0))[..., None]
edge = np.clip((yy / H - 0.84) / 0.16, 0, 1) ** 1.5
edge = np.maximum(edge, np.clip((0.05 - xx / W) / 0.05, 0, 1))
floor_col = floor_col * (1 - 0.7 * edge[..., None]) + bgcol * (0.7 * edge[..., None])
out = out * (1 - floor_a[..., None]) + floor_col * floor_a[..., None]

# ---------------------------------------------------------------- sky -> backdrop, soft edge
sky_a = ndi.gaussian_filter(sky.astype(np.float32), 0.7 * S)
out = out * (1 - sky_a[..., None]) + bgcol * sky_a[..., None]

Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT)
print('done', round(time.time() - t0), 's')
