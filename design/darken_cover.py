from PIL import Image
import numpy as np
from scipy import ndimage as ndi

import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'strategy-update-cover-light.png'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'strategy-update-cover-dark.png'
img = np.array(Image.open(SRC).convert('RGB')).astype(np.float32)
H, W, _ = img.shape
mn = img.min(axis=2); mx = img.max(axis=2); sat = mx - mn
lum = img.mean(axis=2)

# ---- text region (logo + title + subtitle + date), verified free of the model
TX0, TX1, TY0, TY1 = 0, 900, 0, 488
text_box = np.zeros((H, W), bool); text_box[TY0:TY1, TX0:TX1] = True
sub = img[TY0:TY1, TX0:TX1]
nonwhite = (sub.min(axis=2) < 245)
ys, xs = np.nonzero(nonwhite)
print('text box non-white extent: x', xs.min(), xs.max(), 'y', ys.min(), ys.max())
# anything non-white in the far right / bottom strip of the box would be model leakage
print('leak check x>=850:', nonwhite[:, 850:].sum(), ' y>=470:', nonwhite[470:, :].sum())

# ---- background mask outside the text box: near-white connected to the image border
white = mn >= 245
# every near-white region outside the text box is sky/backdrop (gaps between the
# power lines and between the pipe and roof line are enclosed, so no flood fill)
bg = white & ~text_box
lab, n = ndi.label(bg)
sizes = ndi.sum(bg, lab, range(1, n + 1))
small = [(int(s), o) for s, o in zip(sizes, ndi.find_objects(lab)) if s < 20 and o[0].start > 640]
print('small near-white specks in model body:', len(small), small[:10])

# ---- new backdrop: charcoal with a soft glow behind the model (like pic 2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = 0.68 * W, 0.62 * H
r = np.sqrt(((xx - cx) / (0.55 * W)) ** 2 + ((yy - cy) / (0.55 * H)) ** 2)
glow = np.clip(1.0 - r, 0, 1) ** 1.6
base = 19 + 24 * glow                      # 19 in the corners, ~43 near the model
# faint vertical falloff toward the bottom edge (pic 2's floor goes almost black)
base = base * (1 - 0.25 * np.clip((yy / H - 0.78) / 0.22, 0, 1))
rng = np.random.default_rng(7)
noise = rng.normal(0, 1.2, (H, W)).astype(np.float32)
bgcol = np.stack([base + noise, base + noise, base + noise + 1.0], axis=2)
bgcol = np.clip(bgcol, 0, 255)

out = img.copy()

# ---- soft silhouette edge: un-mix the white contribution in edge pixels
edge_band = ndi.binary_dilation(bg, iterations=2) & ~bg & ~text_box
interior = ~bg & ~edge_band
_, idx = ndi.distance_transform_edt(~interior, return_indices=True)
m = img[idx[0], idx[1]]                      # nearest interior model colour
p = img
t = (p - m) / np.maximum(255.0 - m, 1.0)     # per-channel white coverage estimate
t = np.clip(t.mean(axis=2), 0, 1)
t = np.where(edge_band, t, 0.0)
model_part = np.clip(p - t[..., None] * 255.0, 0, 255)
out = np.where(edge_band[..., None], model_part + t[..., None] * bgcol, out)
out = np.where(bg[..., None], bgcol, out)

# ---- text: rebuild on the dark backdrop (dark text -> white, orange stays orange)
ORANGE = np.array([181, 101, 57], np.float32)
tb = text_box
gray = tb & (sat < 30)
orng = tb & ~gray
cov_gray = np.clip((255.0 - lum) / (255.0 - 27.0), 0, 1)
cov_orng = np.clip((255.0 - img[..., 2]) / (255.0 - 57.0), 0, 1)
white_col = np.array([255, 255, 255], np.float32)
tg = bgcol + (white_col - bgcol) * cov_gray[..., None]
to = bgcol + (ORANGE - bgcol) * cov_orng[..., None]
out = np.where(gray[..., None], tg, out)
out = np.where(orng[..., None], to, out)

# ---- gentle darkening of the model so it sits in the dark studio like pic 2
model = ~bg & ~tb
tone = np.clip(out * 0.9, 0, 255)
out = np.where(model[..., None], tone, out)

Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT)
print('bg fraction', bg.mean(), 'edge px', edge_band.sum())
