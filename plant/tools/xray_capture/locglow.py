import sys
import numpy as np
from PIL import Image, ImageChops, ImageFilter
im = Image.open(sys.argv[1]).convert("RGB"); a = np.asarray(im).astype(float)
m = np.clip((a[..., 0] - a[..., 2] - 40) / 60, 0, 1)
g = np.zeros_like(a); g[..., 0], g[..., 1], g[..., 2] = m * 255, m * 140, m * 60
gl = Image.fromarray(g.astype("uint8"))
out = ImageChops.screen(im, ImageChops.multiply(gl.filter(ImageFilter.GaussianBlur(3)), Image.new("RGB", im.size, (170,) * 3)))
out = ImageChops.screen(out, ImageChops.multiply(gl.filter(ImageFilter.GaussianBlur(10)), Image.new("RGB", im.size, (110,) * 3)))
out.save(sys.argv[2], quality=92)
