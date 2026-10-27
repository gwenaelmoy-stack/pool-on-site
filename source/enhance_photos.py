"""Photo pass used on site/assets: python3 enhance_photos.py in.webp out.webp

Bright, airy look: the projection must read as visible in daylight too, so mid-tones and
shadows are lifted rather than deepened."""
import sys, numpy as np
from PIL import Image, ImageEnhance, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.float32) / 255
W = np.array([0.299, 0.587, 0.114], np.float32)
lum = a @ W
lo, hi = np.percentile(lum, 0.3), np.percentile(lum, 99.7)
a = np.clip((a - lo) / max(hi - lo, 1e-3), 0, 1)
# Gamma chosen so the average brightness lands near 0.52, never darker than the source.
m = float(np.clip((a @ W).mean(), 0.05, 0.95))
g = float(np.clip(np.log(0.52) / np.log(m), 0.55, 1.0))
a = a ** g
# Lift the deepest shadows a little more, leave highlights alone.
a = a + 0.12 * (1 - a) ** 3 * a
a = np.clip(a, 0, 1)
out = Image.fromarray((a * 255 + .5).astype(np.uint8))
out = ImageEnhance.Color(out).enhance(1.10)
out = out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=3))
if dst.endswith('.jpg'):
    out.save(dst, 'JPEG', quality=88)
else:
    out.save(dst, 'WEBP', quality=84, method=6)
