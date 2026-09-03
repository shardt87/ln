"""Turn the light studio render of the strategy-update cover into a dark one.

usage: python3 darken2.py [input.png] [output.png]
"""
import sys
from PIL import Image
import numpy as np
from scipy import ndimage as ndi

SRC = sys.argv[1] if len(sys.argv) > 1 else 'strategy-update-cover-light.png'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'strategy-update-cover-dark.png'

img = np.array(Image.open(SRC).convert('RGB')).astype(np.float32)
H, W, _ = img.shape
R, G, B = img[..., 0], img[..., 1], img[..., 2]
mn = img.min(axis=2); mx = img.max(axis=2); sat = mx - mn
lum = img.mean(axis=2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# ---------------------------------------------------------------- regions
TX0, TX1, TY0, TY1 = 0, 900, 0, 488            # logo / title / subtitle block
text_box = np.zeros((H, W), bool); text_box[TY0:TY1, TX0:TX1] = True
bg = (mn >= 245) & ~text_box                    # white backdrop incl. enclosed sky gaps
model = ~bg & ~text_box

# floor of the model. Seeds: confident floor pixels (smooth neutral greys low in the
# frame) and confident object pixels; a watershed on the image gradient snaps the
# boundary between them onto the real contours of the objects standing on the floor.
from skimage.segmentation import watershed
from skimage.filters import sobel
br = B - R
mf = ndi.uniform_filter(lum, 5); mf2 = ndi.uniform_filter(lum ** 2, 5)
texture = np.sqrt(np.maximum(mf2 - mf * mf, 0))
neutral = (sat <= 22) & (lum >= 65) & (lum <= 228) & (B - R >= -4)
warmpad = (lum >= 150) & (lum <= 228) & (R - B >= 5) & (R - B <= 16) & (sat <= 16) & (yy > 690) & (xx >= 560)
lightground = (lum >= 195) & (lum <= 228) & (sat <= 12) & (R - B >= 2) & (R - B <= 10) & ((xx >= 560) | (yy >= 745) | (xx < 250))   # keep off the container tops
floorish = (neutral | warmpad | lightground) & (yy > 600) & model
asphalt_only = (lum >= 112) & (lum <= 145) & (br >= 6) & (br <= 20) & (sat <= 22)
cbox = np.zeros((H, W), bool); cbox[655:775, 255:565] = True   # container block: only the asphalt gaps are floor
floorish &= ~cbox | asphalt_only
floorish[:682, 1160:1430] = False      # boiler box
floorish[:715, 1385:1465] = False      # right stack base
floorish[:655, 1050:1185] = False      # big duct into the boiler
floorish[735:, 1325:] = False           # small building bottom right (roof is light)
floorish[750:, 1140:1330] &= (lum[750:, 1140:1330] <= 201)   # parked cars vs parking lot
floor_seed = floorish & (texture < 10)
floor_seed = ndi.binary_erosion(floor_seed, iterations=2)
lab, n = ndi.label(floor_seed); sizes = ndi.sum(floor_seed, lab, range(1, n + 1))
small_ok = np.zeros((H, W), bool)
small_ok[690:775, 1130:1330] = True    # ground behind the parking lot, chopped up by poles
small_ok[640:745, 1430:1536] = True    # ground right of the stack, likewise
floor_seed = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 300]) | \
             (np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 60]) & small_ok)
floor_seed[765:840, 850:970] = False   # white truck cab sides look like floor
obj_seed = ndi.binary_erosion(~floorish, iterations=1) | (sat > 30) | (lum > 228) | (lum < 60) | (yy < 600) | bg | text_box
obj_seed &= ~floor_seed
markers = np.zeros((H, W), np.int32); markers[obj_seed] = 1; markers[floor_seed] = 2
grad = sobel(lum / 255.0) + 0.5 * (sobel(R / 255.0) + sobel(G / 255.0) + sobel(B / 255.0))
labels = watershed(grad, markers)
floor = (labels == 2) & model
lab, n = ndi.label(floor); sizes = ndi.sum(floor, lab, range(1, n + 1))
in_strip = ndi.sum(small_ok, lab, range(1, n + 1)) > 0
floor = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 2000 or (s >= 300 and in_strip[i])])
floor_a = ndi.gaussian_filter(floor.astype(np.float32), 0.7)

# ---------------------------------------------------------------- backdrop
cx, cy = 0.68 * W, 0.60 * H
r = np.sqrt(((xx - cx) / (0.55 * W)) ** 2 + ((yy - cy) / (0.55 * H)) ** 2)
glow = np.clip(1.0 - r, 0, 1) ** 1.6
base = 17 + 26 * glow
base = base * (1 - 0.35 * np.clip((yy / H - 0.72) / 0.28, 0, 1))
rng = np.random.default_rng(7)
noise = rng.normal(0, 1.2, (H, W)).astype(np.float32)
bgcol = np.clip(np.stack([base + noise, base + noise, base + noise + 1.0], axis=2), 0, 255)

out = img.copy()

# ---------------------------------------------------------------- model grading
# darker, punchier, slightly warm in the highlights - like a lit model in a dark studio
m = out
m = (m - 128.0) * 1.14 + 128.0                 # contrast
m = m * 0.80                                    # overall darker
hi = np.clip((m.mean(axis=2) - 120.0) / 100.0, 0, 1)[..., None]
m = m + hi * np.array([14, 6, -6], np.float32)  # warm highlights
# richer copper / orange
warm = (R > B + 40) & (R > G + 10)
m = np.where(warm[..., None], (m - m.mean(axis=2, keepdims=True)) * 1.25 + m.mean(axis=2, keepdims=True) * 1.05, m)
out = np.where(model[..., None], np.clip(m, 0, 255), out)

# floor -> dark charcoal, keeping the road markings and shading as faint texture
fl = out.mean(axis=2)
target = 24.0 + fl * 0.14
scale = target / np.maximum(fl, 1.0)
floor_col = out * scale[..., None]
# fade the floor into the backdrop toward the bottom and the side edges
edge = np.clip((yy / H - 0.86) / 0.14, 0, 1) ** 1.5
edge = np.maximum(edge, np.clip((0.06 - xx / W) / 0.06, 0, 1))
floor_col = floor_col * (1 - 0.6 * edge[..., None]) + bgcol * (0.6 * edge[..., None])
out = out * (1 - floor_a[..., None]) + floor_col * floor_a[..., None]

# ---------------------------------------------------------------- silhouette edge un-mixing
edge_band = ndi.binary_dilation(bg, iterations=2) & ~bg & ~text_box
interior = ~bg & ~edge_band
_, idx = ndi.distance_transform_edt(~interior, return_indices=True)
mi = img[idx[0], idx[1]]
t = np.clip(((img - mi) / np.maximum(255.0 - mi, 1.0)).mean(axis=2), 0, 1)
t = np.where(edge_band, t, 0.0)
model_part = np.clip(out - t[..., None] * 255.0 * 0.8, 0, 255)
out = np.where(edge_band[..., None], model_part * (1 - t[..., None]) + bgcol * t[..., None], out)
out = np.where(bg[..., None], bgcol, out)

# ---------------------------------------------------------------- text
ORANGE = np.array([181, 101, 57], np.float32)
gray = text_box & (sat < 30); orng = text_box & ~gray
cov_gray = np.clip((255.0 - lum) / (255.0 - 27.0), 0, 1)
cov_orng = np.clip((255.0 - B) / (255.0 - 57.0), 0, 1)
out = np.where(gray[..., None], bgcol + (255.0 - bgcol) * cov_gray[..., None], out)
out = np.where(orng[..., None], bgcol + (ORANGE - bgcol) * cov_orng[..., None], out)

Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT)
print('floor fraction', round(float(floor.mean()), 3))
