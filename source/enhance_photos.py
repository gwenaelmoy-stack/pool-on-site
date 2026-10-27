"""Photo pass used on site/assets: python3 enhance_photos.py in.webp out.webp"""
import sys, os, numpy as np
from PIL import Image, ImageEnhance, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.float32) / 255
lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
lo, hi = np.percentile(lum, 0.5), np.percentile(lum, 99.6)
# Stretch levels on luminance only (keeps the colour mood of night shots), blended to stay natural.
st = np.clip((a - lo) / max(hi - lo, 1e-3), 0, 1)
a = 0.65 * st + 0.35 * a
# Gentle S-curve for contrast.
a = a + 0.10 * (a - a**2) * (2 * a - 1)
a = np.clip(a, 0, 1)
out = Image.fromarray((a * 255 + .5).astype(np.uint8))
out = ImageEnhance.Contrast(out).enhance(1.06)
out = ImageEnhance.Color(out).enhance(1.12)
out = out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=3))
out.save(dst, 'WEBP', quality=84, method=6)
