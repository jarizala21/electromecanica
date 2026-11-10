"""Transformadores de movimiento: biela-manivela (cigüeñal) y tipos de levas."""
import math, sys
from lib import Lienzo, guardar_gif, C, sombra

W, H = 800, 480
TAU = 2 * math.pi

# ======================================================================= Biela-manivela
def biela(ruta):
    base = Lienzo(W, H)
    base.titulo("Biela-manivela (cigüeñal)", "Convierte el giro del cigüeñal en el vaivén del pistón, y al revés")
    O = (250, 382); r = 58; l = 172
    pms = O[1] - (l + r); pmi = O[1] - (l - r)
    # cilindro (sección rayada)
    for x0, x1 in ((O[0] - 66, O[0] - 52), (O[0] + 52, O[0] + 66)):
        pts = [(x0, 96), (x1, 96), (x1, 318), (x0, 318)]
        base.poly(pts, fill=C["acero_l"]); base.hatch(pts, C["acero"], 6); base.poly(pts, outline=C["acero_d"], w=1.6)
    base.rect(O[0] - 66, 88, O[0] + 66, 96, fill=C["acero"], outline=C["acero_d"], w=1.4)
    # niveles PMS y PMI (cabeza del pistón)
    top_pms, top_pmi = pms - 44, pmi - 44
    for y, t in ((top_pms, "PMS"), (top_pmi, "PMI")):
        base.dash_line((O[0] - 92, y), (O[0] + 100, y), C["rojo"], 1.3, (7, 4))
        base.text(O[0] - 98, y - 9, t, "tit", 16, C["rojo"], "ra")
    base.arrow((O[0] + 90, top_pmi), (O[0] + 90, top_pms + 2), C["rojo"], 2.2, 9)
    base.arrow((O[0] + 90, top_pms), (O[0] + 90, top_pmi - 2), C["rojo"], 2.2, 9)
    base.text(O[0] + 98, (top_pms + top_pmi) / 2 - 18, "carrera", "cond", 15, C["rojo"])
    base.text(O[0] + 98, (top_pms + top_pmi) / 2, "= 2 · r", "cond", 15, C["rojo"])
    base.panel(470, 96, 780, 462, "Cómo funciona")
    fondo = base.im
    frames, dur = [], []
    N = 60
    for i in range(N):
        th = TAU * i / N            # 0 = manivela arriba (PMS); giro horario
        P = (O[0] + r * math.sin(th), O[1] - r * math.cos(th))
        yb = O[1] - (r * math.cos(th) + math.sqrt(l * l - (r * math.sin(th)) ** 2))
        B = (O[0], yb)
        L = Lienzo(W, H, base=fondo)
        # contrapeso y brazo del cigüeñal
        ca = th + math.pi
        cp = [(O[0], O[1])] + [(O[0] + 50 * math.sin(ca + d), O[1] - 50 * math.cos(ca + d)) for d in [x * 0.12 for x in range(-9, 10)]]
        L.poly(cp, fill=C["verde_d"])
        ux, uy = (P[0] - O[0]) / r, (P[1] - O[1]) / r; nx, ny = -uy, ux
        arm = [(O[0] + nx * 17, O[1] + ny * 17), (P[0] + nx * 14, P[1] + ny * 14), (P[0] - nx * 14, P[1] - ny * 14), (O[0] - nx * 17, O[1] - ny * 17)]
        L.poly(arm, fill=C["verde"], outline=C["verde_d"], w=1.6)
        L.circle(O[0], O[1], 19, fill=C["verde_l"], outline=C["verde_d"], w=2)
        L.circle(O[0], O[1], 6, fill=C["ink"])
        # biela
        bx, by = (B[0] - P[0]), (B[1] - P[1]); bl = math.hypot(bx, by); bx, by = bx / bl, by / bl; mx, my = -by, bx
        rod = [(P[0] + mx * 11, P[1] + my * 11), (B[0] + mx * 8, B[1] + my * 8), (B[0] - mx * 8, B[1] - my * 8), (P[0] - mx * 11, P[1] - my * 11)]
        L.poly(rod, fill=C["acero"], outline=C["acero_d"], w=1.6)
        L.circle(P[0], P[1], 13, fill=C["acero_l"], outline=C["acero_d"], w=1.8)
        L.circle(P[0], P[1], 5, fill=C["ink"])
        # pistón
        L.rect(O[0] - 51, yb - 44, O[0] + 51, yb + 26, fill=C["azul"], outline=C["azul_d"], w=1.8, r=3)
        for k in (0, 1, 2):
            L.line([(O[0] - 51, yb - 34 + k * 8), (O[0] + 51, yb - 34 + k * 8)], C["azul_d"], 1.6)   # segmentos
        L.circle(B[0], B[1], 10, fill=C["azul_l"], outline=C["azul_d"], w=1.6)
        L.circle(B[0], B[1], 4, fill=C["ink"])
        # flechas de giro y de vaivén
        L.arrow_arc(O[0], O[1], 84, -150, -30, 1, C["ink"], 3)
        v = -math.sin(th)          # signo de la velocidad del pistón (arriba negativo en pantalla)
        if abs(v) > 0.15:
            if v > 0: L.arrow((O[0] - 82, yb + 20), (O[0] - 82, yb - 30), C["azul_d"], 3, 11)
            else: L.arrow((O[0] - 82, yb - 30), (O[0] - 82, yb + 20), C["azul_d"], 3, 11)
        # rótulos
        L.text(O[0] - 150, O[1] - 6, "Cigüeñal", "cond", 16, C["verde_d"], "ra")
        L.text(O[0] - 150, O[1] + 12, "(manivela)", "txt", 12.5, C["muted"], "ra")
        L.leader(((P[0] + B[0]) / 2, (P[1] + B[1]) / 2), (O[0] - 104, 330), C["acero_d"])
        L.text(O[0] - 150, 322, "Biela", "cond", 16, C["acero_d"], "ra")
        L.text(O[0] - 150, 160, "Pistón", "cond", 16, C["azul_d"], "ra")
        L.leader((O[0] - 51, yb - 10), (O[0] - 146, 176), C["azul_d"])
        # panel
        grados = int(round(math.degrees(th))) % 360
        L.text(488, 128, "ÁNGULO DEL CIGÜEÑAL", "neg", 12, C["muted"])
        L.text(488, 146, f"{grados}°", "tit", 30, C["ink"])
        L.text(640, 128, "PISTÓN", "neg", 12, C["muted"])
        estado = "en el PMS" if grados in (0,) else "en el PMI" if grados == 180 else ("baja" if grados < 180 else "sube")
        L.text(640, 146, estado, "tit", 30, C["azul_d"])
        for j, t in enumerate(["El cigüeñal gira y la biela empuja",
                               "y tira del pistón: el giro se",
                               "convierte en movimiento rectilíneo",
                               "alternativo (vaivén).",
                               "",
                               "Media vuelta = una carrera.",
                               "En un motor ocurre al revés: el",
                               "pistón empuja y el cigüeñal gira."]):
            L.text(488, 206 + 26 * j, t, "txt", 15, C["ink"] if j < 4 else C["muted"])
        frames.append(L.fin()); dur.append(55)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Levas
def perfil_pera(f): return 34 + 22 * max(0.0, math.cos(f)) ** 2.4
def perfil_corazon(f):
    f = (f + math.pi) % TAU - math.pi
    return 26 + 30 * (1 - abs(f) / math.pi)

def levas(ruta):
    base = Lienzo(W, H)
    base.titulo("Levas: tipos", "La leva gira y el seguidor sube y baja (o va y viene) según su forma")
    paneles = [(20, 90, "Leva de disco (pera)", "seguidor de rodillo"),
               (410, 90, "Excéntrica", "seguidor plano"),
               (20, 282, "Leva de corazón", "seguidor de punta"),
               (410, 282, "Leva de tambor", "seguidor de rodillo en la ranura")]
    for x0, y0, t, s in paneles:
        base.panel(x0, y0, x0 + 370, y0 + 184)
        base.text(x0 + 14, y0 + 10, t, "tit", 17, C["ink"])
        base.text(x0 + 14, y0 + 31, s, "txt", 12.5, C["muted"])
    # gráficas (estáticas): desplazamiento del seguidor en una vuelta
    gr = []
    def lift_rodillo(prof, th, rr=10):
        best = -1e9
        for k in range(360):
            f = TAU * k / 360
            r = prof(f)
            x, y = r * math.sin(f + th), r * math.cos(f + th)
            if abs(x) <= rr:
                best = max(best, y + math.sqrt(rr * rr - x * x))
        return best
    def lift_plano(th, e=14, R=40): return R + e * math.cos(th)
    def lift_punta(th): return perfil_corazon(-th)
    def lift_tambor(th): return 26 * math.sin(th)
    funcs = [lambda th: lift_rodillo(perfil_pera, th), lift_plano, lift_punta, lift_tambor]
    curvas = []
    for (x0, y0, _, _), f in zip(paneles, funcs):
        vals = [f(TAU * k / 90) for k in range(91)]
        lo, hi = min(vals), max(vals)
        gx0, gx1, gy0, gy1 = x0 + 214, x0 + 356, y0 + 58, y0 + 160
        base.line([(gx0, gy0 - 4), (gx0, gy1), (gx1, gy1)], C["muted"], 1.2)
        def Y(v, lo=lo, hi=hi, gy0=gy0, gy1=gy1): return gy1 - 8 - (v - lo) / (hi - lo) * (gy1 - gy0 - 14)
        pts = [(gx0 + (gx1 - gx0) * k / 90, Y(v)) for k, v in enumerate(vals)]
        base.line(pts, C["azul"], 2.2)
        base.text(gx1, gy1 + 5, "1 vuelta", "txt", 11, C["muted"], "ra")
        base.text(gx0 + 4, gy0 - 12, "posición del seguidor", "txt", 11, C["muted"])
        curvas.append((f, gx0, gx1, Y))
    fondo = base.im

    def leva_radial(L, cx, cy, th, prof):
        pts = [(cx + prof(TAU * k / 120) * math.sin(TAU * k / 120 + th), cy - prof(TAU * k / 120) * math.cos(TAU * k / 120 + th)) for k in range(120)]
        L.poly(pts, fill=C["verde"], outline=C["verde_d"], w=1.6)
        L.circle(cx, cy, 8, fill=C["verde_l"], outline=C["verde_d"], w=1.5); L.circle(cx, cy, 3, fill=C["ink"])
        L.line([(cx + 10 * math.sin(th + 3.6), cy - 10 * math.cos(th + 3.6)), (cx + 24 * math.sin(th + 3.6), cy - 24 * math.cos(th + 3.6))], C["rojo"], 3)

    def guia(L, cx, ytop):
        L.rect(cx - 13, ytop, cx + 13, ytop + 14, fill=C["acero_l"], outline=C["acero_d"], w=1.4)
        L.hatch([(cx - 13, ytop), (cx + 13, ytop), (cx + 13, ytop + 14), (cx - 13, ytop + 14)], C["acero"], 5)

    frames, dur = [], []
    N = 60
    for i in range(N):
        th = TAU * i / N
        L = Lienzo(W, H, base=fondo)
        # 1) pera + rodillo
        x0, y0 = paneles[0][:2]; cx, cy = x0 + 100, y0 + 132
        h = funcs[0](th)
        leva_radial(L, cx, cy, th, perfil_pera)
        yc = cy - h
        L.rect(cx - 4, y0 + 46, cx + 4, yc, fill=C["azul_d"])
        L.circle(cx, yc, 10, fill=C["azul"], outline=C["azul_d"], w=1.6); L.circle(cx, yc, 3, fill=C["ink"])
        guia(L, cx, y0 + 50)
        # 2) excéntrica + plano
        x0, y0 = paneles[1][:2]; cx, cy = x0 + 100, y0 + 128
        e = 14
        cc = (cx + e * math.sin(th), cy - e * math.cos(th))
        L.circle(cc[0], cc[1], 40, fill=C["verde"], outline=C["verde_d"], w=1.6)
        L.circle(cx, cy, 8, fill=C["verde_l"], outline=C["verde_d"], w=1.5); L.circle(cx, cy, 3, fill=C["ink"])
        L.circle(cc[0], cc[1], 3.5, fill=C["rojo"])
        yp = cy - funcs[1](th)
        L.rect(cx - 4, y0 + 46, cx + 4, yp, fill=C["azul_d"])
        L.rect(cx - 44, yp - 7, cx + 44, yp, fill=C["azul"], outline=C["azul_d"], w=1.5)
        guia(L, cx, y0 + 50)
        # 3) corazón + punta
        x0, y0 = paneles[2][:2]; cx, cy = x0 + 100, y0 + 128
        leva_radial(L, cx, cy, th, perfil_corazon)
        yp = cy - funcs[2](th)
        L.rect(cx - 4, y0 + 46, cx + 4, yp - 9, fill=C["azul_d"])
        L.poly([(cx - 7, yp - 10), (cx + 7, yp - 10), (cx, yp)], fill=C["azul"], outline=C["azul_d"], w=1.4)
        guia(L, cx, y0 + 50)
        # 4) tambor
        x0, y0 = paneles[3][:2]; cxd, cyd, R, Lh = x0 + 100, y0 + 124, 34, 66
        L.rect(cxd - Lh, cyd - R, cxd + Lh, cyd + R, fill=C["verde"], outline=C["verde_d"], w=1.6, r=6)
        L.rect(cxd - Lh - 26, cyd - 6, cxd - Lh, cyd + 6, fill=C["verde_d"])
        L.rect(cxd + Lh, cyd - 6, cxd + Lh + 26, cyd + 6, fill=C["verde_d"])
        for sgn in (-6, 6):
            pts = []
            for k in range(41):
                a = -math.pi / 2 + math.pi * k / 40
                xx = cxd + 26 * math.sin(a + math.pi / 2 - th) + sgn
                yy = cyd + R * math.sin(a)
                pts.append((xx, yy))
            L.line(pts, C["verde_d"], 2.2)
        xs = cxd + funcs[3](th)
        L.rect(xs - 4, y0 + 62, xs + 4, cyd - R, fill=C["azul_d"])
        L.circle(xs, cyd - R + 2, 7, fill=C["azul"], outline=C["azul_d"], w=1.4)
        L.rect(cxd - Lh, y0 + 60, cxd + Lh, y0 + 66, fill=C["acero_l"], outline=C["acero_d"], w=1.2)
        L.rect(xs - 14, y0 + 56, xs + 14, y0 + 70, fill=C["azul"], outline=C["azul_d"], w=1.4)
        L.line([(cxd - Lh - 28, y0 + 168), (cxd + Lh + 28, y0 + 168)], C["muted"], 1)
        # puntos en las gráficas
        for f, gx0, gx1, Y in curvas:
            L.circle(gx0 + (gx1 - gx0) * i / N, Y(f(th)), 5.5, fill=C["rojo"])
        frames.append(L.fin()); dur.append(60)
    return guardar_gif(frames, dur, ruta)

TODOS = {"biela-manivela": biela, "levas": levas}

if __name__ == "__main__":
    salida = sys.argv[1]
    for n in sys.argv[2:] or TODOS.keys():
        print(n, TODOS[n](f"{salida}/{n}.gif"))
