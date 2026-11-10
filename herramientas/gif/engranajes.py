"""Engranajes: animación a la izquierda y representación normalizada (UNE-EN ISO 2203) a la derecha.
Convenios usados en el dibujo normalizado:
  - circunferencia / línea de cabeza: línea continua gruesa
  - circunferencia / línea primitiva: línea fina de trazo y punto
  - circunferencia de pie: no se dibuja en vista; en corte, línea continua gruesa
  - en corte axial los dientes no se rayan; en la zona de engrane, los dientes de una rueda se suponen ocultos
  - helicoidales: tres líneas finas indican la dirección del dentado
"""
import math, sys
from lib import Lienzo, guardar_gif, C, sombra, mezcla, engranaje_pts, corona_pts, dibuja_engranaje

W, H = 800, 480
TAU = 2 * math.pi
K = C["ink"]          # color del dibujo técnico
G, F = 2.6, 1.2       # grosor de línea gruesa y fina
HAT = (120, 128, 136)

# ---------------------------------------------------------------- utilidades del dibujo normalizado
def panel_norma(L, leyenda):
    L.rect(436, 92, 782, 466, fill=(255, 255, 255), outline=C["linea"], w=1.5, r=12)
    L.text(452, 102, "REPRESENTACIÓN NORMALIZADA", "neg", 12, C["muted"])
    L.text(452, 118, "UNE-EN ISO 2203", "txt", 11.5, C["muted"])
    y = 466 - 18 * len(leyenda) - 8
    L.line([(446, y - 8), (772, y - 8)], C["linea"], 1)
    for i, (tipo, txt) in enumerate(leyenda):
        yy = y + 18 * i + 6
        if tipo == "gruesa": L.line([(452, yy), (486, yy)], K, G)
        elif tipo == "punto": L.dash_line((452, yy), (486, yy), K, F, (12, 3, 2, 3))
        elif tipo == "oculta": L.dash_line((452, yy), (486, yy), K, F, (5, 3))
        elif tipo == "fina": L.line([(452, yy), (486, yy)], K, F)
        elif tipo == "nota": L.text(469, yy - 8, "•", "txt", 13, C["muted"], "ma")
        L.text(494, yy - 8, txt, "txt", 12, C["ink"] if tipo != "nota" else C["muted"])

def ejes_cruz(L, cx, cy, r):
    L.dash_line((cx - r, cy), (cx + r, cy), K, F)
    L.dash_line((cx, cy - r), (cx, cy + r), K, F)

def circ_gruesa(L, cx, cy, r): L.circle(cx, cy, r, outline=K, w=G)
def circ_punto(L, cx, cy, r): L.dash_circle(cx, cy, r, K, F, (12, 3, 2, 3))

def chavetero(L, cx, cy, rb):
    L.circle(cx, cy, rb, outline=K, w=G)
    L.rect(cx - rb * .3, cy - rb - rb * .35, cx + rb * .3, cy - rb + 2, fill=(255, 255, 255), outline=K, w=1.6)

def rayar(L, pts, ang=45):
    L.hatch(pts, HAT, sep=5.5, w=1.0, ang=ang)
    L.poly(pts, outline=K, w=G)

def corte_rueda(L, x0, x1, cy, ra, rp, rf, rb, ang=45, oculto_arriba=False, oculto_abajo=False):
    """Corte axial de una rueda cilíndrica (eje horizontal en pantalla). Dientes sin rayar."""
    for s in (-1, 1):
        cuerpo = [(x0, cy + s * rb), (x1, cy + s * rb), (x1, cy + s * rf), (x0, cy + s * rf)]
        rayar(L, cuerpo, ang)
        # zona de dientes: contorno grueso, sin rayado
        oc = (s < 0 and oculto_arriba) or (s > 0 and oculto_abajo)
        L.line([(x0, cy + s * rf), (x0, cy + s * ra)], K, G)
        L.line([(x1, cy + s * rf), (x1, cy + s * ra)], K, G)
        if oc: L.dash_line((x0, cy + s * ra), (x1, cy + s * ra), K, F, (5, 3))
        else: L.line([(x0, cy + s * ra), (x1, cy + s * ra)], K, G)
        L.dash_line((x0 - 8, cy + s * rp), (x1 + 8, cy + s * rp), K, F)

def base_gif(titulo, sub, leyenda):
    b = Lienzo(W, H)
    b.titulo(titulo, sub)
    b.text(28, 96, "FUNCIONAMIENTO", "neg", 12, C["muted"])
    panel_norma(b, leyenda)
    return b

# ======================================================================= Dientes rectos
def rectos(ruta):
    b = base_gif("Engranajes de dientes rectos", "Transmiten el giro entre ejes paralelos; las ruedas giran en sentidos contrarios",
                 [("gruesa", "circunferencia de cabeza"), ("punto", "circunferencia primitiva y ejes"),
                  ("oculta", "dientes ocultos en la zona de engrane"), ("nota", "en corte, los dientes no se rayan")])
    # vista frontal normalizada
    m, z1, z2 = 5, 10, 20
    r1, r2 = m * z1 / 2, m * z2 / 2
    cx, c1, c2 = 520, 186, 186 + r1 + r2
    for cy, r, rb in ((c1, r1, 7), (c2, r2, 11)):
        circ_gruesa(b, cx, cy, r + m); circ_punto(b, cx, cy, r); chavetero(b, cx, cy, rb)
        b.dash_line((cx - r - m - 10, cy), (cx + r + m + 10, cy), K, F)
    b.dash_line((cx, c1 - r1 - m - 10), (cx, c2 + r2 + m + 10), K, F)
    b.text(cx, 342, "Vista frontal", "cond", 13, C["muted"], "ma")
    # corte axial
    xa, xb = 660, 704
    corte_rueda(b, xa, xb, c1, r1 + m, r1, r1 - 1.25 * m, 7, 45, oculto_abajo=False)
    corte_rueda(b, xa, xb, c2, r2 + m, r2, r2 - 1.25 * m, 11, 135, oculto_arriba=True)
    b.dash_line((xa - 14, c1), (xb + 14, c1), K, F); b.dash_line((xa - 14, c2), (xb + 14, c2), K, F)
    b.text((xa + xb) / 2, 342, "Corte axial", "cond", 13, C["muted"], "ma")
    b.text(590, c1 - 22, "piñón", "txt", 11, C["muted"])
    b.text(590, c2 - 22, "rueda", "txt", 11, C["muted"])
    # rótulos fijos de la animación
    M, Z1, Z2 = 9, 10, 20
    R1, R2 = M * Z1 / 2, M * Z2 / 2
    A = (122, 288); B = (A[0] + R1 + R2, 288)
    b.text(A[0], 404, "Piñón (motriz)", "cond", 16, C["verde_d"], "ma")
    b.text(A[0], 422, "z = 10", "txt", 13, C["muted"], "ma")
    b.text(B[0], 404, "Rueda (conducida)", "cond", 16, C["azul_d"], "ma")
    b.text(B[0], 422, "z = 20", "txt", 13, C["muted"], "ma")
    b.text(28, 446, "Relación i = 20 / 10 = 2: la rueda gira a la mitad de velocidad", "txt", 14, C["ink"])
    fondo = b.im
    frames, dur = [], []
    N = 48
    for i in range(N):
        t1 = 2 * TAU * i / N
        t2 = math.pi + math.pi / Z2 - t1 * Z1 / Z2
        L = Lienzo(W, H, base=fondo)
        dibuja_engranaje(L, *B, M, Z2, t2, C["azul"], C["azul_d"])
        dibuja_engranaje(L, *A, M, Z1, t1, C["verde"], C["verde_d"])
        L.arrow_arc(A[0], A[1], R1 + M + 16, -150, -70, 1, C["verde_d"], 3)
        L.arrow_arc(B[0], B[1], R2 + M + 16, -110, -30, -1, C["azul_d"], 3)
        frames.append(L.fin()); dur.append(75)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Helicoidales
def helicoidales(ruta):
    b = base_gif("Engranajes helicoidales", "Dientes inclinados: engranan poco a poco, son más silenciosos y soportan más carga",
                 [("gruesa", "contorno de cabeza"), ("punto", "línea primitiva y ejes"),
                  ("fina", "3 líneas finas: dirección del dentado"), ("nota", "las dos ruedas tienen hélices opuestas")])
    # normalizada: vista frontal y vista lateral (sin cortar) con las tres líneas
    m, z1, z2 = 5, 10, 20
    r1, r2 = m * z1 / 2, m * z2 / 2
    cx, c1, c2 = 520, 186, 186 + r1 + r2
    for cy, r, rb in ((c1, r1, 7), (c2, r2, 11)):
        circ_gruesa(b, cx, cy, r + m); circ_punto(b, cx, cy, r); chavetero(b, cx, cy, rb)
        b.dash_line((cx - r - m - 10, cy), (cx + r + m + 10, cy), K, F)
    b.dash_line((cx, c1 - r1 - m - 10), (cx, c2 + r2 + m + 10), K, F)
    b.text(cx, 342, "Vista frontal", "cond", 13, C["muted"], "ma")
    xa, xb = 652, 712
    beta = math.radians(22)
    for cy, ra, rp, sgn in ((c1, r1 + m, r1, 1), (c2, r2 + m, r2, -1)):
        b.rect(xa, cy - ra, xb, cy + ra, outline=K, w=G)
        b.dash_line((xa - 8, cy - rp), (xb + 8, cy - rp), K, F)
        b.dash_line((xa - 8, cy + rp), (xb + 8, cy + rp), K, F)
        b.dash_line((xa - 14, cy), (xb + 14, cy), K, F)
        # tres líneas finas inclinadas (ángulo de hélice), opuestas en cada rueda
        dx = (xb - xa - 16) / 2
        for k in (-1, 0, 1):
            yc = cy + k * ra * 0.42
            ddy = sgn * dx * math.tan(beta)
            b.line([((xa + xb) / 2 - dx, yc + ddy), ((xa + xb) / 2 + dx, yc - ddy)], K, F)
    b.text((xa + xb) / 2, 342, "Vista lateral", "cond", 13, C["muted"], "ma")
    # animación: arriba vista frontal pequeña, abajo vista lateral con dientes inclinados
    M, Z1, Z2 = 6, 10, 20
    R1, R2 = M * Z1 / 2, M * Z2 / 2
    A = (110, 170); B = (A[0] + R1 + R2, 170)
    b.text(300, 112, "Vista frontal", "cond", 14, C["muted"])
    b.text(300, 250, "Vista lateral", "cond", 14, C["muted"])
    b.text(28, 446, "Al girar, los dientes inclinados entran en contacto de forma gradual", "txt", 14, C["ink"])
    fondo = b.im
    frames, dur = [], []
    N = 48
    # vista lateral: cilindros con dientes como bandas inclinadas
    ancho = 74
    ytop = 280
    def cilindro(L, cx, R, z, ang, sgn, col, osc):
        L.rect(cx - R - 1, ytop, cx + R + 1, ytop + ancho, fill=sombra(col, .78), outline=osc, w=1.6)
        delta = sgn * ancho * math.tan(math.radians(24)) / R
        for k in range(z):
            a = ang + k * TAU / z
            for w0, w1, f in ((a - .5 * math.pi / z, a + .5 * math.pi / z, 1.0),):
                xs = []
                ok = True
                for (aa, yy) in ((w0, ytop), (w1, ytop), (w1 + delta, ytop + ancho), (w0 + delta, ytop + ancho)):
                    if math.cos(aa) < -0.05: ok = False
                    xs.append((cx + R * math.sin(aa), yy))
                if not ok: continue
                luz = 0.82 + 0.4 * max(0, math.cos(a + delta / 2))
                L.poly(xs, fill=sombra(col, luz), outline=osc, w=1.0)
        L.rect(cx - R - 1, ytop, cx + R + 1, ytop + ancho, outline=osc, w=1.8)
    for i in range(N):
        t1 = 2 * TAU * i / N
        t2 = math.pi + math.pi / Z2 - t1 * Z1 / Z2
        L = Lienzo(W, H, base=fondo)
        dibuja_engranaje(L, *B, M, Z2, t2, C["azul"], C["azul_d"])
        dibuja_engranaje(L, *A, M, Z1, t1, C["verde"], C["verde_d"])
        # ejes en la vista lateral
        L.rect(A[0] - 6, ytop - 26, A[0] + 6, ytop + ancho + 26, fill=C["verde_d"])
        L.rect(B[0] - 9, ytop - 26, B[0] + 9, ytop + ancho + 26, fill=C["azul_d"])
        cilindro(L, B[0], R2 + M * .5, Z2, -t2 + math.pi / 2, -1, C["azul"], C["azul_d"])
        cilindro(L, A[0], R1 + M * .5, Z1, -t1 - math.pi / 2, 1, C["verde"], C["verde_d"])
        frames.append(L.fin()); dur.append(75)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Cónicos
def conicos(ruta):
    b = base_gif("Engranajes cónicos", "Transmiten el giro entre ejes que se cortan, normalmente a 90°",
                 [("gruesa", "contorno de cabeza y del cuerpo"), ("punto", "conos primitivos y ejes"),
                  ("oculta", "dientes ocultos en la zona de engrane"), ("nota", "los conos primitivos se cortan en el vértice")])
    z1, z2 = 12, 18
    d1 = math.atan(z1 / z2); d2 = math.pi / 2 - d1
    # ---------- corte axial normalizado
    O = (648, 206)
    Re, Ri, m = 100, 64, 7
    def gear_corte(axis, u, delta, ang, oculto_lado=None):
        a_, d_ = m, 1.25 * m
        def S(t, r, s): return (O[0] + axis[0] * t + u[0] * s * r, O[1] + axis[1] * t + u[1] * s * r)
        n = (-math.sin(delta), math.cos(delta))           # normal al cono primitivo en el plano (t, r)
        def P(sl, off): return (sl * math.cos(delta) + off * n[0], sl * math.sin(delta) + off * n[1])
        for s in (-1, 1):
            A1 = P(Ri, -d_); A2 = P(Re, -d_)
            rh = max(16.0, A1[1] * 0.55)
            cuerpo = [S(*q, s) for q in (A1, A2, (A2[0], rh), (A2[0] + 18, rh), (A2[0] + 18, 7), (A1[0], 7))]
            rayar(b, cuerpo, ang)
            T1, T2, T3, T4 = P(Ri, a_), P(Re, a_), P(Re, -d_), P(Ri, -d_)
            pts = [S(*q, s) for q in (T1, T2, T3, T4)]
            b.line([pts[1], pts[2]], K, G); b.line([pts[3], pts[0]], K, G)
            if oculto_lado == s: b.dash_line(pts[0], pts[1], K, F, (5, 3))
            else: b.line([pts[0], pts[1]], K, G)
            b.dash_line(O, S(*P(Re + 14, 0), s), K, F)
        b.dash_line(O, (O[0] + axis[0] * 150, O[1] + axis[1] * 150), K, F)
    gear_corte((-1, 0), (0, -1), d1, 45)                        # piñón: eje horizontal
    gear_corte((0, 1), (-1, 0), d2, 135, oculto_lado=1)         # rueda: eje vertical
    b.circle(O[0], O[1], 3, fill=K)
    b.text(O[0] + 8, O[1] - 20, "vértice", "txt", 11, C["muted"])
    b.text(O[0] - 128, O[1] - 74, "piñón", "txt", 11, C["muted"])
    b.text(O[0] + 70, O[1] + 70, "rueda", "txt", 11, C["muted"])
    b.text(609, 352, "Corte axial de la pareja", "cond", 13, C["muted"], "ma")
    b.text(28, 446, "El piñón (verde) hace girar la rueda (azul) con un eje a 90°", "txt", 14, C["ink"])
    fondo = b.im

    # ---------- animación 3D: conos macizos con los dientes, vistos desde el lado del vértice
    yaw, pitch = math.radians(-34), math.radians(26)
    O3 = (250, 226)
    def rot(v):
        x, y, z = v
        x1 = x * math.cos(yaw) + z * math.sin(yaw); z1 = -x * math.sin(yaw) + z * math.cos(yaw)
        y2 = y * math.cos(pitch) - z1 * math.sin(pitch); z2 = y * math.sin(pitch) + z1 * math.cos(pitch)
        return x1, y2, z2
    def proy(p):
        x1, y2, z2 = rot(p)
        return (O3[0] + x1, O3[1] - y2), z2
    Re3, Ri3 = 158, 100
    gears = [dict(e=(-1, 0, 0), u=(0, 1, 0), v=(0, 0, 1), d=d1, z=z1, col=C["verde"], osc=C["verde_d"]),
             dict(e=(0, -1, 0), u=(1, 0, 0), v=(0, 0, 1), d=d2, z=z2, col=C["azul"], osc=C["azul_d"])]
    def radial(g, phi):
        return tuple(math.cos(phi) * g["u"][k] + math.sin(phi) * g["v"][k] for k in range(3))
    def pc(g, sl, phi, off=0.0):
        cd, sd = math.cos(g["d"]), math.sin(g["d"]); r = radial(g, phi); e = g["e"]
        n = tuple(-sd * e[k] + cd * r[k] for k in range(3))
        return tuple(sl * (cd * e[k] + sd * r[k]) + off * n[k] for k in range(3))
    def normal(g, phi):
        cd, sd = math.cos(g["d"]), math.sin(g["d"]); r = radial(g, phi); e = g["e"]
        return tuple(-sd * e[k] + cd * r[k] for k in range(3))
    frames, dur = [], []
    N = 48
    for i in range(N):
        th = [TAU * 1.5 * i / N, TAU * 1.5 * i / N * z1 / z2 + math.pi / z2 + math.pi]
        L = Lienzo(W, H, base=fondo)
        caras = []
        # ejes (por detrás)
        for g, wv, larg in ((gears[0], 22, 270), (gears[1], 26, 205)):
            a, za = proy(tuple(c * Re3 * math.cos(g["d"]) for c in g["e"]))
            b_, zb = proy(tuple(c * larg for c in g["e"]))
            caras.append((min(za, zb) - 500, "eje", [a, b_], g["osc"], wv))
        for gi, g in enumerate(gears):
            # cara frontal (junto al vértice): disco a s = Ri
            disco = [proy(pc(g, Ri3, TAU * k / 48))[0] for k in range(48)]
            cen = proy(tuple(c * Ri3 * math.cos(g["d"]) for c in g["e"]))[1]
            caras.append((cen - 30, "poly", disco, sombra(g["col"], .7), g["osc"]))
            hw = math.pi / g["z"]
            for k in range(g["z"]):
                ph = th[gi] + k * TAU / g["z"]
                for a0, a1, alto, tono in ((ph - hw * .55, ph + hw * .55, 5, 1.12), (ph + hw * .55, ph + hw * 1.45, -2, .78)):
                    nn = rot(normal(g, (a0 + a1) / 2))
                    if nn[2] <= 0.02: continue
                    q = [pc(g, Ri3, a0, alto * Ri3 / Re3), pc(g, Re3, a0, alto), pc(g, Re3, a1, alto), pc(g, Ri3, a1, alto * Ri3 / Re3)]
                    pr = [proy(p_) for p_ in q]
                    zz = sum(z_ for _, z_ in pr) / 4
                    luz = (0.58 + 0.55 * nn[2]) * tono
                    caras.append((zz, "poly", [p_ for p_, _ in pr], sombra(g["col"], luz), g["osc"]))
        caras.sort(key=lambda c: c[0])
        for c in caras:
            if c[1] == "eje":
                L.line(c[2], sombra(c[3], .85), c[4] + 3); L.line(c[2], c[3], c[4])
            else:
                L.poly(c[2], fill=c[3], outline=c[4], w=1.0)
        L.text(30, 352, "Piñón (motriz)", "cond", 16, C["verde_d"])
        L.text(30, 370, "z = 12", "txt", 13, C["muted"])
        L.text(312, 392, "Rueda (conducida)", "cond", 16, C["azul_d"])
        L.text(312, 410, "z = 18", "txt", 13, C["muted"])
        frames.append(L.fin()); dur.append(80)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Tornillo sin fin
def sinfin(ruta):
    b = base_gif("Tornillo sin fin y corona", "Gran reducción en poco espacio entre ejes que se cruzan a 90°",
                 [("gruesa", "contornos de cabeza"), ("punto", "líneas primitivas y ejes"),
                  ("oculta", "dientes de la corona ocultos por el tornillo"), ("nota", "en corte, los dientes no se rayan")])
    # ---------- normalizada: corona en vista frontal + tornillo de lado; a la derecha, corte de la corona
    m, z = 4.5, 24
    rp = m * z / 2; ra = rp + m
    cx, cy = 530, 252
    rw = 13
    ywy = cy - rp - rw            # eje del tornillo
    circ_punto(b, cx, cy, rp)
    # cabeza de la corona: arco visible fuera del tornillo, discontinuo dentro
    b.arc(cx, cy, ra, -64, 244, K, G)
    b.dash_circle(cx, cy, ra, K, F, (5, 3), a0=244, a1=296)
    chavetero(b, cx, cy, 12)
    ejes_cruz(b, cx, cy, ra + 10)
    b.rect(cx - 60, ywy - rw - m, cx + 60, ywy + rw + m, fill=(255, 255, 255), outline=K, w=G)
    b.dash_line((cx - 68, ywy + rw), (cx + 68, ywy + rw), K, F)
    b.dash_line((cx - 68, ywy - rw), (cx + 68, ywy - rw), K, F)
    b.dash_line((cx - 92, ywy), (cx + 92, ywy), K, F)
    b.rect(cx - 84, ywy - 6, cx - 60, ywy + 6, outline=K, w=G); b.rect(cx + 60, ywy - 6, cx + 84, ywy + 6, outline=K, w=G)
    # corte de la corona y tornillo de frente
    x2 = 712
    b.circle(x2, ywy, rw + m, outline=K, w=G); circ_punto(b, x2, ywy, rw); b.circle(x2, ywy, 6, outline=K, w=G)
    ejes_cruz(b, x2, ywy, rw + m + 8)
    # corona en corte: cuerpo rayado y zona de dientes cóncava (garganta)
    bw = 34
    for s in (-1, 1):
        top = cy + s * (rp - 1.25 * m)
        cuerpo = [(x2 - bw / 2, cy + s * 12), (x2 + bw / 2, cy + s * 12), (x2 + bw / 2, top), (x2 - bw / 2, top)]
        rayar(b, cuerpo, 45)
        b.line([(x2 - bw / 2, top), (x2 - bw / 2, cy + s * ra)], K, G)
        b.line([(x2 + bw / 2, top), (x2 + bw / 2, cy + s * ra)], K, G)
        if s < 0:
            garg = [(x2 - bw / 2 + bw * k / 16, ywy + math.sqrt(max(0, (rw + m + 3) ** 2 - (bw / 2 - bw * k / 16) ** 2))) for k in range(17)]
            b.line(garg, K, G)
        else:
            b.line([(x2 - bw / 2, cy + s * ra), (x2 + bw / 2, cy + s * ra)], K, G)
        b.dash_line((x2 - bw / 2 - 8, cy + s * rp), (x2 + bw / 2 + 8, cy + s * rp), K, F)
    b.dash_line((x2 - bw / 2 - 12, cy), (x2 + bw / 2 + 12, cy), K, F)
    b.text(cx, 362, "Vista frontal", "cond", 13, C["muted"], "ma")
    b.text(x2 - 4, 362, "Lateral (corona en corte)", "cond", 13, C["muted"], "ma")
    b.text(28, 446, "Una vuelta del tornillo hace avanzar la corona un solo diente", "txt", 14, C["ink"])
    fondo = b.im

    # ---------- animación
    M, Z = 8, 24
    RP = M * Z / 2
    CW = (220, 312)
    RW = 24
    YW = CW[1] - RP - RW
    p = math.pi * M
    x0w, x1w = 92, 348
    frames, dur = [], []
    N = 48
    for i in range(N):
        th = TAU * 2 * i / N                      # dos vueltas del tornillo por ciclo
        tw = -math.pi / 2 + math.pi / Z - th / Z  # corona: avanza un diente por vuelta
        L = Lienzo(W, H, base=fondo)
        dibuja_engranaje(L, *CW, M, Z, tw, C["azul"], C["azul_d"])
        # tornillo: eje, cilindro y filete
        L.rect(40, YW - 9, 400, YW + 9, fill=C["verde_d"])
        L.rect(x0w, YW - RW - M, x1w, YW + RW + M, fill=sombra(C["verde"], .85), outline=C["verde_d"], w=1.8, r=6)
        RT = RW + M
        base_x = CW[0] - 3 * p / 4
        kmin = int((x0w - base_x) // p) - 2
        for k in range(kmin, kmin + int((x1w - x0w) / p) + 5):
            pts = []
            for j in range(25):
                a = -math.pi / 2 + math.pi * j / 24
                xx = base_x + p * (a - th) / TAU + k * p
                pts.append((xx, YW + RT * math.sin(a)))
            pts = [(x, y) for x, y in pts if x0w + 2 < x < x1w - 2]
            if len(pts) > 1:
                L.line(pts, sombra(C["verde"], 1.25), 6)
                L.line(pts, C["verde_d"], 1.6)
        L.rect(x0w, YW - RW - M, x1w, YW + RW + M, outline=C["verde_d"], w=1.8, r=6)
        # marca en el eje del tornillo
        if math.cos(th) > 0:
            L.rect(60, YW + 9 * math.sin(th) - 3, 74, YW + 9 * math.sin(th) + 3, fill=C["rojo"])
        L.text(30, YW - RW - 38, "Tornillo sin fin (motriz)", "cond", 16, C["verde_d"])
        L.text(CW[0], CW[1] + RP + M + 12, "Corona (conducida) · z = 24", "cond", 16, C["azul_d"], "ma")
        L.text(250, 98, "Vueltas del tornillo", "txt", 13, C["muted"])
        L.text(420, 98, f"{2 * i / N:.2f}".replace(".", ","), "neg", 13, C["ink"], "ra")
        L.text(250, 116, "Dientes que avanza la corona", "txt", 13, C["muted"])
        L.text(420, 116, f"{2 * i / N:.2f}".replace(".", ","), "neg", 13, C["ink"], "ra")
        frames.append(L.fin()); dur.append(60)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Dentado interior
def interior(ruta):
    b = base_gif("Engranaje de dentado interior", "Los dientes de la corona miran hacia dentro: las dos ruedas giran en el mismo sentido",
                 [("gruesa", "circunferencias de cabeza y contorno"), ("punto", "circunferencias primitivas y ejes"),
                  ("oculta", "dientes ocultos en la zona de engrane"), ("nota", "en corte, los dientes no se rayan")])
    m, z1, z2 = 5, 10, 30
    r1, r2 = m * z1 / 2, m * z2 / 2
    cx, cy = 540, 236
    c1y = cy + (r2 - r1)
    # vista frontal
    circ_gruesa(b, cx, cy, r2 + 1.25 * m + 12)          # contorno exterior de la corona
    circ_gruesa(b, cx, cy, r2 - m)                      # cabeza de la corona (hacia dentro)
    circ_punto(b, cx, cy, r2)
    circ_gruesa(b, cx, c1y, r1 + m); circ_punto(b, cx, c1y, r1); chavetero(b, cx, c1y, 6)
    ejes_cruz(b, cx, cy, r2 + 30)
    b.dash_line((cx - r1 - m - 8, c1y), (cx + r1 + m + 8, c1y), K, F)
    b.text(cx, 366, "Vista frontal", "cond", 13, C["muted"], "ma")
    # corte axial (a la derecha)
    xa, xb = 690, 740
    ro = r2 + 1.25 * m + 12
    for s in (-1, 1):
        rf = r2 + 1.25 * m
        cuerpo = [(xa, cy + s * rf), (xb, cy + s * rf), (xb, cy + s * ro), (xa, cy + s * ro)]
        rayar(b, cuerpo, 45)
        b.line([(xa, cy + s * rf), (xa, cy + s * (r2 - m))], K, G)
        b.line([(xb, cy + s * rf), (xb, cy + s * (r2 - m))], K, G)
        if s > 0: b.dash_line((xa, cy + s * (r2 - m)), (xb, cy + s * (r2 - m)), K, F, (5, 3))
        else: b.line([(xa, cy + s * (r2 - m)), (xb, cy + s * (r2 - m))], K, G)
        b.dash_line((xa - 8, cy + s * r2), (xb + 8, cy + s * r2), K, F)
    corte_rueda(b, xa + 4, xb - 4, c1y, r1 + m, r1, r1 - 1.25 * m, 6, 135)
    b.dash_line((xa - 14, cy), (xb + 14, cy), K, F); b.dash_line((xa - 10, c1y), (xb + 10, c1y), K, F)
    b.text((xa + xb) / 2, 366, "Corte axial", "cond", 13, C["muted"], "ma")
    b.text(28, 446, "Muy compacto: es la base de los trenes epicicloidales", "txt", 14, C["ink"])
    fondo = b.im

    M, Z1, Z2 = 7, 10, 30
    R1, R2 = M * Z1 / 2, M * Z2 / 2
    CC = (214, 280)
    phi = math.pi / 2
    CP = (CC[0] + (R2 - R1) * math.cos(phi), CC[1] + (R2 - R1) * math.sin(phi))
    frames, dur = [], []
    N = 48
    for i in range(N):
        t1 = 3 * TAU * i / N
        t2 = t1 * Z1 / Z2
        L = Lienzo(W, H, base=fondo)
        RO = R2 + 1.25 * M + 16
        L.circle(CC[0], CC[1], RO, fill=C["azul"], outline=C["azul_d"], w=2)
        L.poly(corona_pts(CC[0], CC[1], M, Z2, phi + math.pi / Z2 + t2), fill=C["bg"], outline=C["azul_d"], w=1.6)
        a = phi + math.pi / Z2 + t2 + math.pi
        L.circle(CC[0] + (RO - 8) * math.cos(a), CC[1] + (RO - 8) * math.sin(a), 5.5, fill=C["rojo"])
        dibuja_engranaje(L, *CP, M, Z1, phi + t1, C["verde"], C["verde_d"])
        L.circle(CC[0], CC[1], 4, fill=C["azul_d"])
        L.arrow_arc(CP[0], CP[1], R1 + M + 14, -150, -40, 1, C["verde_d"], 3)
        L.arrow_arc(CC[0], CC[1], RO + 14, -130, -60, 1, C["azul_d"], 3)
        L.text(CC[0] - RO - 6, 112, "Corona (conducida) · z = 30", "cond", 16, C["azul_d"])
        L.text(CC[0], CC[1] + RO + 10, "Piñón (motriz) · z = 10", "cond", 16, C["verde_d"], "ma")
        frames.append(L.fin()); dur.append(75)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Piñón-cremallera (solo normalizada, PNG)
def pinon_cremallera_norma(ruta):
    L = Lienzo(800, 330, bg=(255, 255, 255))
    L.text(24, 16, "REPRESENTACIÓN NORMALIZADA · UNE-EN ISO 2203", "neg", 13, C["muted"])
    m, z = 7, 18
    rp = m * z / 2
    cx, cy = 300, 150
    circ_gruesa(L, cx, cy, rp + m); circ_punto(L, cx, cy, rp); chavetero(L, cx, cy, 13)
    ejes_cruz(L, cx, cy, rp + m + 12)
    yp = cy + rp
    x0, x1 = 120, 520
    # cremallera: línea de cabeza (oculta donde la tapa el piñón), primitiva y contorno
    L.dash_line((cx - 58, yp - m), (cx + 58, yp - m), K, F, (5, 3))
    L.line([(x0, yp - m), (cx - 58, yp - m)], K, G); L.line([(cx + 58, yp - m), (x1, yp - m)], K, G)
    L.dash_line((x0 - 12, yp), (x1 + 12, yp), K, F)
    L.line([(x0, yp - m), (x0, yp + 34), (x1, yp + 34), (x1, yp - m)], K, G)
    L.text(cx, 302, "piñón (vista frontal) sobre la cremallera (vista lateral)", "cond", 14, C["muted"], "ma")
    leyenda = [("gruesa", "cabeza: circunferencia y línea"), ("punto", "primitivas: tangentes entre sí"),
               ("oculta", "dientes ocultos en el engrane"), ("nota", "la línea de pie no se dibuja")]
    for i, (tipo, txt) in enumerate(leyenda):
        yy = 92 + 32 * i
        if tipo == "gruesa": L.line([(548, yy), (582, yy)], K, G)
        elif tipo == "punto": L.dash_line((548, yy), (582, yy), K, F)
        elif tipo == "oculta": L.dash_line((548, yy), (582, yy), K, F, (5, 3))
        else: L.text(565, yy - 8, "•", "txt", 13, C["muted"], "ma")
        L.text(592, yy - 9, txt, "txt", 14, C["ink"])
    im = L.fin()
    im.save(ruta, optimize=True)
    import os
    return os.path.getsize(ruta)

TODOS = {"engranajes-rectos": rectos, "engranajes-helicoidales": helicoidales, "engranajes-conicos": conicos,
         "tornillo-sin-fin": sinfin, "dentado-interior": interior}

if __name__ == "__main__":
    salida = sys.argv[1]
    nombres = sys.argv[2:] or list(TODOS) + ["pinon-cremallera-normalizada"]
    for n in nombres:
        if n == "pinon-cremallera-normalizada":
            print(n, pinon_cremallera_norma(f"{salida}/{n}.png"))
        else:
            print(n, TODOS[n](f"{salida}/{n}.gif"))
