"""Guías de deslizamiento: redonda, plana, prismática y cola de milano.
Izquierda: carro deslizando sobre la guía (perspectiva caballera). Derecha: sección con sus partes."""
import math, sys
from lib import Lienzo, Caballera, extrusion, guardar_gif, suave, C, sombra

W, H = 800, 480

def arco(cx, cy, r, a0, a1, n=24):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

# ---------------- perfiles (x a la derecha, y hacia arriba; origen en la base de la guía) ----------------
def perfiles_redonda():
    eje = [(24 * math.cos(2 * math.pi * k / 40), 70 + 24 * math.sin(2 * math.pi * k / 40)) for k in range(40)]
    soporte = [(-36, 0), (36, 0), (36, 10), (11, 26), (11, 52), (-11, 52), (-11, 26), (-36, 10)]
    carro = [(-62, 46), (-62, 132), (62, 132), (62, 46), (14, 46)] + arco(0, 70, 28, -59, 239)[1:-1] + [(-14, 46)]
    casq = arco(0, 70, 28, -59, 239) + arco(0, 70, 24.6, 239, -59)
    guia = [dict(pts=soporte, color=C["acero"], borde=C["acero_d"]), dict(pts=eje, color=C["acero_l"], borde=C["acero_d"])]
    movil = [dict(pts=carro, color=C["azul"], borde=C["azul_d"]), dict(pts=casq, color=C["cobre"], borde=C["cobre_d"])]
    contacto = [arco(0, 70, 24.6, -55, 235, 30)]
    etiquetas = [("CARRO", "se desliza", (40, 118), "der", C["azul_d"]),
                 ("CASQUILLO", "de bolas o de bronce", (-20, 96), "izq", C["cobre_d"]),
                 ("EJE", "barra redonda rectificada", (17, 62), "der2", C["acero_d"]),
                 ("SOPORTE", "apoya el eje en toda su longitud", (-30, 6), "izq2", C["acero_d"])]
    return guia, movil, contacto, etiquetas

def perfiles_plana():
    guia_p = [(-50, 0), (50, 0), (50, 30), (70, 30), (70, 50), (-70, 50), (-70, 30), (-50, 30)]
    carro = [(-86, 92), (86, 92), (86, 16), (72, 16), (72, 52), (-72, 52), (-72, 16), (-86, 16)]
    reg_d = [(58, 16), (72, 16), (72, 28), (58, 28)]
    reg_i = [(-72, 16), (-58, 16), (-58, 28), (-72, 28)]
    guia = [dict(pts=guia_p, color=C["acero"], borde=C["acero_d"])]
    movil = [dict(pts=carro, color=C["azul"], borde=C["azul_d"]),
             dict(pts=reg_d, color=C["cobre"], borde=C["cobre_d"]), dict(pts=reg_i, color=C["cobre"], borde=C["cobre_d"])]
    contacto = [[(-70, 50), (70, 50)], [(70, 31), (70, 49)], [(-70, 31), (-70, 49)], [(58, 29.5), (70, 29.5)], [(-70, 29.5), (-58, 29.5)]]
    etiquetas = [("CARRO", "apoya en superficies planas", (60, 80), "der", C["azul_d"]),
                 ("REGLETAS", "evitan que el carro se levante", (-64, 22), "izq", C["cobre_d"]),
                 ("GUÍA PLANA", "bancada", (30, 10), "der2", C["acero_d"])]
    return guia, movil, contacto, etiquetas

def perfiles_prismatica():
    guia_p = [(-62, 0), (62, 0), (62, 40), (30, 40), (0, 70), (-30, 40), (-62, 40)]
    carro = [(-72, 104), (72, 104), (72, 42), (32, 42), (0, 74), (-32, 42), (-72, 42)]
    guia = [dict(pts=guia_p, color=C["acero"], borde=C["acero_d"])]
    movil = [dict(pts=carro, color=C["azul"], borde=C["azul_d"])]
    contacto = [[(-29, 41), (-1, 69)], [(1, 69), (29, 41)]]
    etiquetas = [("CARRO", "con ranura en V", (54, 90), "der", C["azul_d"]),
                 ("PRISMA", "en V invertida: centra el carro", (-16, 56), "izq", C["rojo"]),
                 ("GUÍA", "bancada", (40, 14), "der2", C["acero_d"])]
    return guia, movil, contacto, etiquetas

def perfiles_cola():
    guia_p = [(-70, 0), (70, 0), (70, 30), (30, 30), (50, 62), (-50, 62), (-30, 30), (-70, 30)]
    carro = [(-82, 98), (82, 98), (82, 32), (40, 32), (60, 64), (-51.25, 64), (-31.25, 32), (-82, 32)]
    reg = [(31.8, 32), (39.4, 32), (59.2, 63.2), (51.2, 63.2)]
    guia = [dict(pts=guia_p, color=C["acero"], borde=C["acero_d"])]
    movil = [dict(pts=carro, color=C["azul"], borde=C["azul_d"]), dict(pts=reg, color=C["cobre"], borde=C["cobre_d"])]
    contacto = [[(-31, 31.5), (-50.5, 62.5)], [(-50, 63), (50, 63)], [(31.6, 32), (50.4, 62.2)]]
    etiquetas = [("CARRO", "abraza la cola de milano", (-60, 86), "izq", C["azul_d"]),
                 ("REGLETA CÓNICA", "con tornillos, ajusta el juego", (52, 50), "der", C["cobre_d"]),
                 ("COLA DE MILANO", "no deja que el carro se levante", (-40, 14), "izq2", C["acero_d"])]
    return guia, movil, contacto, etiquetas

GUIAS = {
    "guia-redonda": ("Guía redonda", "Un casquillo desliza sobre un eje cilíndrico", perfiles_redonda),
    "guia-plana": ("Guía plana", "El carro apoya sobre superficies planas de la bancada", perfiles_plana),
    "guia-prismatica": ("Guía prismática", "La forma en V centra el carro mientras se desliza", perfiles_prismatica),
    "guia-cola-de-milano": ("Guía de cola de milano", "El carro encaja en un perfil trapecial y no puede levantarse", perfiles_cola),
}

def seccion(L, guia, movil, contacto, etiquetas, cola=False):
    L.panel(486, 96, 780, 462, "Sección")
    k = 1.2
    sx, sy = 633, 352
    T = lambda p: (sx + p[0] * k, sy - p[1] * k)
    for s in guia:
        pts = [T(p) for p in s["pts"]]
        L.poly(pts, fill=C["acero_l"])
        L.hatch(pts, C["acero"], sep=7, ang=45)
        L.poly(pts, outline=C["acero_d"], w=1.8)
    for i, s in enumerate(movil):
        pts = [T(p) for p in s["pts"]]
        base = sombra(s["color"], 1.55)
        L.poly(pts, fill=base)
        L.hatch(pts, s["color"], sep=7 if i == 0 else 4, ang=135 if i == 0 else 45)
        L.poly(pts, outline=s["borde"], w=1.8)
    if cola:   # tornillos de ajuste de la regleta
        for yy in (42, 54):
            xf = 40 + (yy - 32) / 32 * 20
            L.line([T((94, yy)), T((xf, yy))], C["ink"], 2.4)
            p0, p1 = T((92, yy + 5)), T((100, yy - 5))
            L.rect(p0[0], p0[1], p1[0], p1[1], fill=C["acero_d"])
    for seg in contacto:
        L.line([T(p) for p in seg], C["rojo"], 3.2)
    # etiquetas: dos columnas arriba y dos abajo, con línea de referencia
    sitios = {"izq": (500, 126), "der": (640, 126), "izq2": (500, 372), "der2": (640, 372)}
    for tit, sub, ancla, lado, col in etiquetas:
        ax, ay = T(ancla)
        tx, ty = sitios[lado]
        lineas = partir(sub, 24)
        if lado in ("izq", "der"):
            fin = (tx + 6, ty + 20 + 14 * len(lineas) + 4)
        else:
            fin = (tx + 6, ty - 4)
        L.leader((ax, ay), fin, C["muted"])
        L.text(tx, ty, tit, "tit", 15, col)
        for j, ln in enumerate(lineas):
            L.text(tx, ty + 19 + 14 * j, ln, "txt", 12, C["muted"])
    L.line([(500, 449), (522, 449)], C["rojo"], 3.2)
    L.text(528, 442, "superficies de contacto (deslizamiento)", "txt", 12.5, C["muted"])

def partir(t, n):
    out, act = [], ""
    for w in t.split():
        if len(act) + len(w) + 1 > n and act:
            out.append(act); act = w
        else:
            act = (act + " " + w).strip()
    if act: out.append(act)
    return out

def hacer(nombre, ruta):
    titulo, sub, fperf = GUIAS[nombre]
    guia, movil, contacto, etiquetas = fperf()
    base = Lienzo(W, H)
    base.titulo(titulo, sub)
    seccion(base, guia, movil, contacto, etiquetas, cola=(nombre == "guia-cola-de-milano"))
    base.text(28, 448, "El carro se desliza a lo largo de la guía", "txt", 14, C["muted"])
    fondo = base.im
    cab = Caballera(120, 410, kx=0.6, ky=0.34)
    LG, LC = 340, 104
    frames, dur = [], []
    N = 30
    def pinta(c, direc):
        L = Lienzo(W, H, base=fondo)
        objs = [dict(s, z0=0, z1=LG) for s in guia] + [dict(s, z0=c, z1=c + LC) for s in movil]
        extrusion(L, cab, objs, paso=2.2)
        # flecha de movimiento junto a la guía
        x0, y0 = cab.p(110, 6, 50); x1, y1 = cab.p(110, 6, 250)
        if direc > 0: L.arrow((x0, y0), (x1, y1), C["ink"], 3, 13)
        else: L.arrow((x1, y1), (x0, y0), C["ink"], 3, 13)
        return L.fin()
    for ida in (True, False):
        for i in range(N + 1):
            t = suave(i / N)
            c = 18 + (190 * t if ida else 190 * (1 - t))
            frames.append(pinta(c, 1 if ida else -1)); dur.append(50)
        dur[-1] = 600
    return guardar_gif(frames, dur, ruta)

if __name__ == "__main__":
    salida = sys.argv[1]
    for n in sys.argv[2:] or GUIAS.keys():
        print(n, hacer(n, f"{salida}/{n}.gif"))
