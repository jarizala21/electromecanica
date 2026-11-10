"""Dibuja la esfera del manómetro (0–10 bar) que usa render_areas.py."""
import os
from PIL import Image, ImageDraw, ImageFont
import math
S = 1024; c = S / 2
im = Image.new('RGB', (S, S), (238, 238, 236))
d = ImageDraw.Draw(im)
d.ellipse((8, 8, S - 8, S - 8), fill=(250, 250, 248))
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 74)
f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 56)
def ang(v):  # 0..10 bar sobre 270°
    return math.radians(225 - 27 * v)
for k in range(0, 51):
    v = k / 5
    a = ang(v)
    largo = 70 if k % 5 == 0 else 36
    ancho = 9 if k % 5 == 0 else 5
    r0 = 440
    x0, y0 = c + r0 * math.cos(a), c - r0 * math.sin(a)
    x1, y1 = c + (r0 - largo) * math.cos(a), c - (r0 - largo) * math.sin(a)
    d.line((x0, y0, x1, y1), fill=(20, 20, 22), width=ancho)
for v in range(0, 11, 2):
    a = ang(v)
    r = 315
    d.text((c + r * math.cos(a), c - r * math.sin(a)), str(v), font=f, fill=(20, 20, 22), anchor='mm')
# zona roja final
d.arc((c - 440, c - 440, c + 440, c + 440), start=-45 - 0, end=-45 + 0, fill=(200, 30, 30))
for k in range(0, 30):
    a = ang(9 + k / 30)
    d.line((c + 445 * math.cos(a), c - 445 * math.sin(a), c + 425 * math.cos(a), c - 425 * math.sin(a)), fill=(205, 35, 35), width=10)
d.text((c, c + 230), 'bar', font=f2, fill=(40, 40, 44), anchor='mm')
# aguja a 6,3 bar
a = ang(6.3)
tip = (c + 400 * math.cos(a), c - 400 * math.sin(a))
back = (c - 70 * math.cos(a), c + 70 * math.sin(a))
n = (-math.sin(a), -math.cos(a))
w = 13
d.polygon([tip, (c + w * n[0], c + w * n[1]), back, (c - w * n[0], c - w * n[1])], fill=(200, 28, 28))
d.ellipse((c - 34, c - 34, c + 34, c + 34), fill=(25, 25, 28))
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'esfera_manometro.png'))
