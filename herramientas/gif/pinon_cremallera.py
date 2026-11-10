"""GIF didáctico: piñón y cremallera.

El piñón (z = 12, módulo 2 mm, d = 24 mm) gira media vuelta en sentido antihorario
y la cremallera avanza a la derecha; pausa; gira media vuelta en sentido horario y
la cremallera vuelve a la izquierda. Avance = radio × ángulo (rodadura sin deslizar).
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "pinon-cremallera.gif"
W, H = 800, 480
SS = 3                                   # sobremuestreo para bordes suaves
# Fuentes Barlow de @fontsource (npm install @fontsource/barlow @fontsource/barlow-condensed)
# y DejaVu Sans Condensed Bold para el símbolo π. Uso: python3 pinon_cremallera.py salida.gif
F = os.environ.get("FONTSOURCE", "node_modules/@fontsource/")
def fuente(f, px): return ImageFont.truetype(F + f, px * SS)
TIT = fuente("barlow-condensed/files/barlow-condensed-latin-700-normal.woff", 34)
SUB = fuente("barlow/files/barlow-latin-500-normal.woff", 17)
ETQ = fuente("barlow-condensed/files/barlow-condensed-latin-700-normal.woff", 20)
ETQ2 = fuente("barlow/files/barlow-latin-500-normal.woff", 15)
NUM = fuente("barlow-condensed/files/barlow-condensed-latin-600-normal.woff", 26)
LAB = fuente("barlow/files/barlow-latin-600-normal.woff", 13)
PI = ImageFont.truetype(os.environ.get("DEJAVU", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"), 24 * SS)

# Colores (misma familia que la app: gris armario, verde mecánica)
BG = (240, 242, 244); INK = (22, 32, 41); MUTED = (85, 98, 108); LINE = (208, 214, 219)
PIN = (59, 135, 76); PIN_D = (31, 84, 43); PIN_HUB = (226, 238, 228)
RACK = (150, 162, 172); RACK_D = (77, 91, 102)
ROJO = (200, 62, 44); PANEL = (249, 250, 251)

# Geometría (px a escala 1)
Z = 12; M = 12.0; MODULO_MM = 2.0
R = M * Z / 2                    # radio primitivo = 72 px
RA, RF = R + M, R - 1.25 * M     # cabeza y pie
P = math.pi * M                  # paso
CX, CY = 400, 200
PITCH_Y = CY + R                 # línea primitiva de la cremallera
ALPHA = math.radians(20)

def s(v): return v * SS

def engranaje(theta):
    """Contorno del piñón; theta = giro en coordenadas de pantalla (y hacia abajo)."""
    pts = []
    half = math.pi / (2 * Z)
    w_root, w_tip = 1.32 * half, 0.56 * half
    for k in range(Z):
        a = theta + math.pi / 2 + k * 2 * math.pi / Z      # diente k=0 apunta abajo con theta=0
        for ang, rad in ((a - math.pi / Z, RF), (a - w_root, RF), (a - w_tip, RA), (a + w_tip, RA), (a + w_root, RF)):
            pts.append((s(CX + rad * math.cos(ang)), s(CY + rad * math.sin(ang))))
    return pts

def cremallera(desp):
    """Polígono de la cremallera desplazada 'desp' px (positivo = derecha)."""
    top, root = PITCH_Y - M, PITCH_Y + 1.25 * M
    base = root + 36
    hp = P / 4
    htip, hroot = hp - M * math.tan(ALPHA), hp + 1.25 * M * math.tan(ALPHA)
    x0 = CX + P / 2 + desp            # con theta = 0, hueco bajo el centro del piñón
    j0 = math.floor((-60 - x0) / P)
    j1 = math.ceil((W + 60 - x0) / P)
    pts = [(s(-80), s(base)), (s(-80), s(root))]
    for j in range(j0, j1 + 1):
        c = x0 + j * P
        pts += [(s(c - hroot), s(root)), (s(c - htip), s(top)), (s(c + htip), s(top)), (s(c + hroot), s(root))]
    pts += [(s(W + 80), s(root)), (s(W + 80), s(base))]
    return pts, base

def flecha_arco(d, sentido):
    """Flecha curva sobre el piñón; sentido = +1 horario, -1 antihorario (en pantalla)."""
    rr = RA + 20
    a0, a1 = math.radians(-125), math.radians(-55)        # arco superior
    box = [s(CX - rr), s(CY - rr), s(CX + rr), s(CY + rr)]
    d.arc(box, math.degrees(a0), math.degrees(a1), fill=INK, width=s(4))
    tip = a1 if sentido > 0 else a0
    tx, ty = CX + rr * math.cos(tip), CY + rr * math.sin(tip)
    tang = tip + sentido * math.pi / 2                    # dirección del avance en la punta
    ux, uy = math.cos(tang), math.sin(tang)
    nx, ny = -uy, ux
    L, Wd = 16, 9
    d.polygon([(s(tx + ux * 6), s(ty + uy * 6)),
               (s(tx - ux * L + nx * Wd), s(ty - uy * L + ny * Wd)),
               (s(tx - ux * L - nx * Wd), s(ty - uy * L - ny * Wd))], fill=INK)

def flecha_recta(d, x, y, sentido, largo=110):
    x0, x1 = (x - largo / 2, x + largo / 2) if sentido > 0 else (x + largo / 2, x - largo / 2)
    d.line([(s(x0), s(y)), (s(x1 - sentido * 12), s(y))], fill=INK, width=s(4))
    d.polygon([(s(x1 + sentido * 4), s(y)), (s(x1 - sentido * 14), s(y - 9)), (s(x1 - sentido * 14), s(y + 9))], fill=INK)

def texto(d, xy, t, f, fill, anchor="la"):
    d.text((s(xy[0]), s(xy[1])), t, font=f, fill=fill, anchor=anchor)

def frame(theta, desp, giro_deg, avance_mm, sentido_giro, mov):
    im = Image.new("RGB", (s(W), s(H)), BG)
    d = ImageDraw.Draw(im)

    # Cremallera con una marca roja fija en ella
    pts, base = cremallera(desp)
    d.polygon(pts, fill=RACK, outline=RACK_D, width=s(2))
    mx = CX + desp
    d.polygon([(s(mx), s(base - 10)), (s(mx - 9), s(base + 6)), (s(mx + 9), s(base + 6))], fill=ROJO)
    d.line([(s(mx), s(base - 10)), (s(mx), s(base - 34))], fill=ROJO, width=s(3))
    # línea primitiva (discontinua)

    # Piñón
    d.polygon(engranaje(theta), fill=PIN, outline=PIN_D, width=s(2))
    d.ellipse([s(CX - 30), s(CY - 30), s(CX + 30), s(CY + 30)], fill=PIN_HUB, outline=PIN_D, width=s(2))
    d.ellipse([s(CX - 10), s(CY - 10), s(CX + 10), s(CY + 10)], fill=INK)
    # radio rojo que gira con el piñón (marca de giro)
    a = theta + math.pi / 2
    d.line([(s(CX + 12 * math.cos(a)), s(CY + 12 * math.sin(a))), (s(CX + (R - 6) * math.cos(a)), s(CY + (R - 6) * math.sin(a)))], fill=ROJO, width=s(5))
    d.ellipse([s(CX + R * .82 * math.cos(a) - 7), s(CY + R * .82 * math.sin(a) - 7), s(CX + R * .82 * math.cos(a) + 7), s(CY + R * .82 * math.sin(a) + 7)], fill=ROJO)

    # Flechas de sentido
    flecha_arco(d, sentido_giro)
    flecha_recta(d, CX + 250, PITCH_Y + 1.25 * M + 58, mov)

    # Textos
    texto(d, (28, 22), "Piñón y cremallera", TIT, INK)
    texto(d, (28, 62), "Convierte el giro en desplazamiento rectilíneo", SUB, MUTED)
    texto(d, (CX + RA + 34, CY - 18), "PIÑÓN", ETQ, PIN_D)
    texto(d, (CX + RA + 34, CY + 6), "gira", ETQ2, MUTED)
    texto(d, (28, PITCH_Y + 1.25 * M + 46), "CREMALLERA", ETQ, RACK_D)
    texto(d, (150, PITCH_Y + 1.25 * M + 50), "se desplaza en línea recta", ETQ2, MUTED)

    # Panel de lectura
    py = 392
    d.rounded_rectangle([s(28), s(py), s(W - 28), s(H - 22)], radius=s(12), fill=PANEL, outline=LINE, width=s(2))
    cols = [(52, "GIRO DEL PIÑÓN", f"{giro_deg:.0f}°".replace(".", ",")),
            (300, "AVANCE DE LA CREMALLERA", f"{avance_mm:.1f} mm".replace(".", ",")),
            (575, "UNA VUELTA COMPLETA", "π × d = 75,4 mm")]
    for x, lab, val in cols:
        texto(d, (x, py + 14), lab, LAB, MUTED)
        if val.startswith("π"):
            d.text((s(x), s(py + 33)), "π", font=PI, fill=INK)
            ancho = d.textlength("π", font=PI) / SS
            texto(d, (x + ancho + 1, py + 32), val[1:], NUM, INK)
        else:
            texto(d, (x, py + 32), val, NUM, INK)
    return im.resize((W, H), Image.LANCZOS)

def suave(t): return 0.5 - 0.5 * math.cos(math.pi * t)

frames, dur = [], []
N = 44                       # fotogramas por media vuelta
MEDIA = math.pi
def tramo(sentido_giro, ida):
    for i in range(N + 1):
        t = suave(i / N)
        g = MEDIA * t
        if ida:   # antihorario: theta de +π/2 a -π/2; la cremallera va a la derecha
            theta = MEDIA / 2 - g
        else:     # horario: theta de -π/2 a +π/2; vuelve a la izquierda
            theta = -MEDIA / 2 + g
        desp = -R * theta
        frames.append(frame(theta, desp, math.degrees(g), MODULO_MM * Z / 2 * g, sentido_giro, 1 if ida else -1))
        dur.append(40)
    dur[-1] = 900            # pausa al final de cada media vuelta

tramo(-1, True)
tramo(+1, False)

# Paleta común para que no parpadee
pal = frames[0].quantize(colors=64, method=Image.Quantize.MEDIANCUT)
# Asegura que el rojo y el verde estén en la paleta: cuantiza un mosaico con fotogramas variados
mosaico = Image.new("RGB", (W, H * 3 + 120), BG)
for i, k in enumerate((0, N // 2, N)):
    mosaico.paste(frames[k], (0, H * i))
# muestras de los colores clave para que la paleta los conserve exactos
dm = ImageDraw.Draw(mosaico)
for i, c in enumerate((ROJO, PIN, PIN_D, INK, RACK, RACK_D, MUTED, PANEL)):
    dm.rectangle([i * 100, H * 3, i * 100 + 99, H * 3 + 119], fill=c)
pal = mosaico.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
q[0].save(OUT, save_all=True, append_images=q[1:], duration=dur, loop=0, optimize=True, disposal=1)
print(OUT, len(q), "fotogramas")
