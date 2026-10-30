"""Build the browser-tab icons from the Pool-On logo: the 'On' switch, with its knob filled white."""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')

def switch():
    im = Image.open(os.path.join(SITE, 'assets', 'logo-color.png')).convert('RGBA').crop((254, 15, 418, 106))
    W, H = im.size
    cx, cy, r = 118.5, 44.5, 32  # knob hole of the switch, in crop coordinates
    k = 8
    disc = Image.new('L', (W * k, H * k), 0)
    ImageDraw.Draw(disc).ellipse(((cx + .5 - r) * k, (cy + .5 - r) * k, (cx + .5 + r) * k, (cy + .5 + r) * k), fill=255)
    knob = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    knob.putalpha(disc.resize((W, H), Image.LANCZOS))
    return Image.alpha_composite(knob, im)

def square(img, size, pad=0.03, bg=(0, 0, 0, 0)):
    c = Image.new('RGBA', (size, size), bg)
    w = int(size * (1 - 2 * pad)); h = round(w * img.size[1] / img.size[0])
    c.alpha_composite(img.resize((w, h), Image.LANCZOS), ((size - w) // 2, (size - h) // 2))
    return c

s = switch()
square(s, 256).save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
square(s, 512).save(os.path.join(SITE, 'assets', 'icon-512.png'))
square(s, 180, pad=0.12, bg=(255, 255, 255, 255)).convert('RGB').save(os.path.join(SITE, 'apple-touch-icon.png'))
