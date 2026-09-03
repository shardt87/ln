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

# floor of the model: light ground, asphalt yard, roads, parking, concrete pad
br = B - R
ground  = (lum >= 195) & (lum <= 232) & (sat <= 12) & (R - B >= 2)
asphalt = (lum >= 112) & (lum <= 145) & (br >= 6) & (br <= 20) & (sat <= 22)
road    = (lum >= 70) & (lum <= 104) & (br >= 4) & (br <= 14) & (sat <= 16)
parking = (lum >= 180) & (lum <= 222) & (br >= 3) & (br <= 14) & (sat <= 16)
pad     = ((lum >= 140) & (lum <= 172) & (sat <= 6)) | \
          ((lum >= 150) & (lum <= 215) & (R - B >= 8) & (R - B <= 15) & (sat <= 15) & (yy > 690))
mf = ndi.uniform_filter(lum, 5); mf2 = ndi.uniform_filter(lum ** 2, 5)
texture = np.sqrt(np.maximum(mf2 - mf * mf, 0))
cand = (ground | asphalt | road | parking | pad) & (yy > 600) & model & (texture < 25)
cand[:700, 1160:1430] = False                   # boiler box panels share the asphalt colour
cand = ndi.binary_opening(cand, iterations=2)
lab, n = ndi.label(cand); sizes = ndi.sum(cand, lab, range(1, n + 1))
keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 3000])
keep = ndi.binary_dilation(keep, iterations=2)
holes = ndi.binary_fill_holes(keep) & ~keep
hl, hn = ndi.label(holes); hs = ndi.sum(holes, hl, range(1, hn + 1))
floor = (keep | np.isin(hl, [i + 1 for i, s in enumerate(hs) if s <= 600])) & model
floor_a = ndi.gaussian_filter(floor.astype(np.float32), 1.5)

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
