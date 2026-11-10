"""Base común para los GIF de Mecánica: estilo, primitivas de dibujo y guardado.

Coordenadas lógicas en píxeles (lienzo de 800 × 480 por defecto); se dibuja con
sobremuestreo y se reduce al final para tener bordes suaves.
Fuentes: Barlow (npm @fontsource/barlow y @fontsource/barlow-condensed) y DejaVu.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageChops

SS = 2
FS = os.environ.get("FONTSOURCE", "/tmp/fontdl/node_modules/@fontsource/")
DEJAVU = os.environ.get("DEJAVU", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf")
DEJAVU_R = os.environ.get("DEJAVU_R", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf")

_cache = {}
def fuente(nombre, px):
    rutas = {
        "tit": FS + "barlow-condensed/files/barlow-condensed-latin-700-normal.woff",
        "cond": FS + "barlow-condensed/files/barlow-condensed-latin-600-normal.woff",
        "txt": FS + "barlow/files/barlow-latin-500-normal.woff",
        "neg": FS + "barlow/files/barlow-latin-600-normal.woff",
        "sim": DEJAVU, "simr": DEJAVU_R,
    }
    k = (nombre, px)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(rutas[nombre], int(round(px * SS)))
    return _cache[k]

# Colores: verde = elemento motriz, azul = conducido, acero = partes fijas
C = dict(
    bg=(240, 242, 244), panel=(249, 250, 251), linea=(208, 214, 219), ink=(22, 32, 41), muted=(85, 98, 108),
    verde=(59, 135, 76), verde_d=(31, 84, 43), verde_l=(198, 226, 203),
    azul=(74, 128, 186), azul_d=(27, 84, 140), azul_l=(208, 224, 242),
    acero=(150, 162, 172), acero_d=(77, 91, 102), acero_l=(212, 218, 223),
    cobre=(200, 122, 62), cobre_d=(128, 70, 28),
    goma=(236, 168, 46), goma_d=(158, 104, 10),
    rojo=(200, 62, 44), blanco=(255, 255, 255), negro=(22, 32, 41),
)

def mezcla(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def sombra(c, f):
    """f > 1 aclara hacia blanco, f < 1 oscurece."""
    if f >= 1:
        return mezcla(c, (255, 255, 255), min(1, f - 1))
    return tuple(int(v * f) for v in c)


class Lienzo:
    def __init__(self, W=800, H=480, bg=C["bg"], base=None):
        self.W, self.H = W, H
        self.im = base.copy() if base is not None else Image.new("RGB", (W * SS, H * SS), bg)
        self.d = ImageDraw.Draw(self.im)

    # --- conversión ---
    @staticmethod
    def P(pts):
        return [(x * SS, y * SS) for x, y in pts]

    # --- primitivas ---
    def poly(self, pts, fill=None, outline=None, w=2):
        self.d.polygon(self.P(pts), fill=fill, outline=outline, width=int(round(w * SS)) if outline else 0)

    def line(self, pts, fill, w=2):
        self.d.line(self.P(pts), fill=fill, width=max(1, int(round(w * SS))), joint="curve")

    def circle(self, cx, cy, r, fill=None, outline=None, w=2):
        self.d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=fill, outline=outline,
                       width=int(round(w * SS)) if outline else 0)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, w=2):
        self.d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=fill, outline=outline,
                       width=int(round(w * SS)) if outline else 0)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=2, r=0):
        x0, x1 = min(x0, x1), max(x0, x1); y0, y1 = min(y0, y1), max(y0, y1)
        self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS, fill=fill, outline=outline,
                                 width=int(round(w * SS)) if outline else 0)

    def arc(self, cx, cy, r, a0, a1, fill, w=2):
        """Ángulos en grados, en sentido horario de pantalla (como PIL)."""
        self.d.arc([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], a0, a1, fill=fill, width=int(round(w * SS)))

    def text(self, x, y, t, f="txt", px=16, fill=C["ink"], anchor="la"):
        self.d.text((x * SS, y * SS), t, font=fuente(f, px), fill=fill, anchor=anchor)

    def textlen(self, t, f="txt", px=16):
        return self.d.textlength(t, font=fuente(f, px)) / SS

    # --- líneas normalizadas ---
    def dash_line(self, p0, p1, fill, w=1.4, patron=(12, 3, 2, 3)):
        """Trazo y punto (por defecto) o discontinua con patron=(6, 4)."""
        x0, y0 = p0; x1, y1 = p1
        L = math.hypot(x1 - x0, y1 - y0)
        if L == 0: return
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        s, i, on = 0.0, 0, True
        while s < L:
            seg = patron[i % len(patron)]
            e = min(L, s + seg)
            if i % 2 == 0:
                self.line([(x0 + ux * s, y0 + uy * s), (x0 + ux * e, y0 + uy * e)], fill, w)
            s = e; i += 1

    def dash_circle(self, cx, cy, r, fill, w=1.4, patron=(12, 3, 2, 3), a0=0, a1=360):
        per = 2 * math.pi * r
        if per == 0: return
        a = math.radians(a0); fin = math.radians(a1); i = 0
        while a < fin:
            seg = patron[i % len(patron)] / r
            b = min(fin, a + seg)
            if i % 2 == 0:
                self.arc(cx, cy, r, math.degrees(a), math.degrees(b), fill, w)
            a = b; i += 1

    # --- flechas ---
    def arrow(self, p0, p1, fill=C["ink"], w=3, head=12):
        x0, y0 = p0; x1, y1 = p1
        L = math.hypot(x1 - x0, y1 - y0)
        if L == 0: return
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        nx, ny = -uy, ux
        bx, by = x1 - ux * head, y1 - uy * head
        self.line([(x0, y0), (bx + ux * 2, by + uy * 2)], fill, w)
        self.poly([(x1, y1), (bx + nx * head * .6, by + ny * head * .6), (bx - nx * head * .6, by - ny * head * .6)], fill=fill)

    def arrow_arc(self, cx, cy, r, a0, a1, sentido, fill=C["ink"], w=3, head=12):
        """Arco de a0 a a1 (grados, pantalla). sentido +1: la punta está en a1 (horario); -1: en a0."""
        self.arc(cx, cy, r, a0, a1, fill, w)
        tip = math.radians(a1 if sentido > 0 else a0)
        tx, ty = cx + r * math.cos(tip), cy + r * math.sin(tip)
        t = tip + sentido * math.pi / 2
        ux, uy = math.cos(t), math.sin(t); nx, ny = -uy, ux
        self.poly([(tx + ux * head * .45, ty + uy * head * .45),
                   (tx - ux * head * .75 + nx * head * .6, ty - uy * head * .75 + ny * head * .6),
                   (tx - ux * head * .75 - nx * head * .6, ty - uy * head * .75 - ny * head * .6)], fill=fill)

    # --- rayado de corte (45°) recortado a un polígono ---
    def hatch(self, pts, fill=C["acero_d"], sep=7, w=1.1, ang=45):
        mask = Image.new("L", self.im.size, 0)
        ImageDraw.Draw(mask).polygon(self.P(pts), fill=255)
        rayas = Image.new("L", self.im.size, 0)
        dr = ImageDraw.Draw(rayas)
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)          # dirección de las rayas (pantalla, y hacia abajo)
        nx, ny = -uy, ux
        proy = [p[0] * nx + p[1] * ny for p in pts]
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        big = 2000
        c = min(proy)
        while c <= max(proy):
            d = c - (cx * nx + cy * ny)
            px, py = cx + nx * d, cy + ny * d
            dr.line([((px - ux * big) * SS, (py - uy * big) * SS), ((px + ux * big) * SS, (py + uy * big) * SS)],
                    fill=255, width=max(1, int(w * SS)))
            c += sep
        m = ImageChops.multiply(mask, rayas)
        self.im.paste(Image.new("RGB", self.im.size, fill), mask=m)

    # --- bloques de texto habituales ---
    def titulo(self, t, sub=None, x=28):
        self.text(x, 18, t, "tit", 32, C["ink"])
        if sub:
            self.text(x, 56, sub, "txt", 16, C["muted"])

    def etiqueta(self, x, y, t, color=C["ink"], sub=None, anchor="la", px=18):
        self.text(x, y, t, "tit", px, color, anchor)
        if sub:
            yy = y + px + 3
            self.text(x, yy, sub, "txt", 14, C["muted"], anchor)

    def leader(self, p_obj, p_txt, color=C["muted"]):
        """Línea de referencia fina con punto en el objeto."""
        self.line([p_obj, p_txt], color, 1.2)
        self.circle(p_obj[0], p_obj[1], 2.6, fill=color)

    def panel(self, x0, y0, x1, y1, titulo=None):
        self.rect(x0, y0, x1, y1, fill=C["panel"], outline=C["linea"], w=1.5, r=12)
        if titulo:
            self.text(x0 + 14, y0 + 10, titulo.upper(), "neg", 12, C["muted"])

    def dial(self, cx, cy, r, ang, color, etiqueta=None, rpm=None):
        """Indicador de giro: círculo con radio que gira (ang en rad, pantalla)."""
        self.circle(cx, cy, r, fill=C["panel"], outline=sombra(color, .8), w=2)
        self.line([(cx, cy), (cx + (r - 4) * math.cos(ang), cy + (r - 4) * math.sin(ang))], sombra(color, .85), 3.5)
        self.circle(cx, cy, 3.5, fill=sombra(color, .8))
        if etiqueta:
            self.text(cx, cy + r + 6, etiqueta, "cond", 14, C["muted"], "ma")
        if rpm is not None:
            self.text(cx, cy + r + 24, rpm, "tit", 16, C["ink"], "ma")

    def fin(self):
        return self.im.resize((self.W, self.H), Image.LANCZOS)


# --- geometría de engranajes (perfil simplificado trapecial) ---
def engranaje_pts(cx, cy, m, z, theta, wr=1.32, wt=0.56):
    """Contorno de un engranaje exterior. Diente k=0 apunta en la dirección theta (rad, pantalla)."""
    r = m * z / 2; ra, rf = r + m, r - 1.25 * m
    half = math.pi / (2 * z)
    pts = []
    for k in range(z):
        a = theta + k * 2 * math.pi / z
        for ang, rad in ((a - math.pi / z, rf), (a - wr * half, rf), (a - wt * half, ra), (a + wt * half, ra), (a + wr * half, rf)):
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts

def corona_pts(cx, cy, m, z, theta, wr=1.32, wt=0.56):
    """Hueco dentado de una corona de dentado interior (dientes hacia dentro). Diente k=0 en theta."""
    r = m * z / 2; rtip, rroot = r - m, r + 1.25 * m
    half = math.pi / (2 * z)
    pts = []
    for k in range(z):
        a = theta + k * 2 * math.pi / z
        for ang, rad in ((a - math.pi / z, rroot), (a - wr * half, rroot), (a - wt * half, rtip), (a + wt * half, rtip), (a + wr * half, rroot)):
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts

def dibuja_engranaje(L, cx, cy, m, z, theta, color, oscuro, cubo=None, marca=True, marca_color=C["rojo"]):
    L.poly(engranaje_pts(cx, cy, m, z, theta), fill=color, outline=oscuro, w=1.6)
    r = m * z / 2
    rc = cubo if cubo else max(8, r * 0.38)
    L.circle(cx, cy, rc, fill=mezcla(color, (255, 255, 255), .75), outline=oscuro, w=1.6)
    L.circle(cx, cy, max(3.5, rc * .32), fill=C["ink"])
    if marca:
        a = theta
        L.line([(cx + rc * .55 * math.cos(a), cy + rc * .55 * math.sin(a)), (cx + (r - m * .9) * math.cos(a), cy + (r - m * .9) * math.sin(a))], marca_color, 3.5)
        L.circle(cx + (r - m * 1.2) * math.cos(a), cy + (r - m * 1.2) * math.sin(a), 4.2, fill=marca_color)


# --- sólidos extruidos en perspectiva caballera (para guías) ---
class Caballera:
    """Proyección: x a la derecha, y hacia arriba, z hacia el fondo (sube y va a la derecha)."""
    def __init__(self, ox, oy, kx=0.62, ky=0.36):
        self.ox, self.oy, self.kx, self.ky = ox, oy, kx, ky
    def p(self, x, y, z):
        return (self.ox + x + z * self.kx, self.oy - y - z * self.ky)

def extrusion(L, cab, perfiles, paso=2.0, luz=(-0.45, 0.89)):
    """Dibuja varios sólidos extruidos con orden de pintor por rebanadas.
    perfiles: lista de dicts {pts:[(x,y)...] en sección, z0, z1, color, borde}.
    Las caras laterales se sombrean según la normal del borde."""
    rebanadas = []
    for i, s in enumerate(perfiles):
        z = s["z1"]
        while z > s["z0"]:
            rebanadas.append((z, i, False))
            z -= paso
        rebanadas.append((s["z0"], i, True))
    rebanadas.sort(key=lambda t: (-t[0], t[1]))
    for s in perfiles:
        pts = s["pts"]; n = len(pts)
        area = sum(pts[k][0] * pts[(k + 1) % n][1] - pts[(k + 1) % n][0] * pts[k][1] for k in range(n))
        sg = 1 if area > 0 else -1                   # antihorario (y arriba) → normal exterior (ey, -ex)
        s["_tonos"] = []
        for k in range(n):
            (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % n]
            ex, ey = x1 - x0, y1 - y0
            le = math.hypot(ex, ey) or 1
            nx, ny = sg * ey / le, -sg * ex / le
            f = 0.70 + 0.42 * max(0.0, nx * luz[0] + ny * luz[1])
            s["_tonos"].append(sombra(s["color"], f))
    for z, i, frente in rebanadas:
        s = perfiles[i]; pts = s["pts"]; n = len(pts)
        sp = [cab.p(x, y, z) for x, y in pts]
        if frente:
            L.poly(sp, fill=s["color"], outline=s["borde"], w=1.6)
        else:
            L.poly(sp, fill=sombra(s["color"], .74))
            for k in range(n):
                L.line([sp[k], sp[(k + 1) % n]], s["_tonos"][k], paso * 1.5)


# --- guardado ---
def guardar_gif(frames, duraciones, ruta, colores=80, extra=()):
    """Paleta común (con muestras de colores clave) y sin tramado: archivo ligero y sin parpadeo."""
    W, H = frames[0].size
    idx = sorted(set([0, len(frames) // 3, 2 * len(frames) // 3, len(frames) - 1]))
    mos = Image.new("RGB", (W, H * len(idx) + 60), C["bg"])
    for i, k in enumerate(idx):
        mos.paste(frames[k], (0, H * i))
    dm = ImageDraw.Draw(mos)
    clave = [C[k] for k in ("rojo", "verde", "verde_d", "azul", "azul_d", "ink", "acero", "acero_d", "goma", "cobre", "panel")] + list(extra)
    paso = W // len(clave)
    for i, c in enumerate(clave):
        dm.rectangle([i * paso, H * len(idx), i * paso + paso - 1, H * len(idx) + 59], fill=c)
    pal = mos.quantize(colors=colores, method=Image.Quantize.MEDIANCUT)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    q[0].save(ruta, save_all=True, append_images=q[1:], duration=duraciones, loop=0, optimize=True, disposal=1)
    return os.path.getsize(ruta)

def suave(t):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
