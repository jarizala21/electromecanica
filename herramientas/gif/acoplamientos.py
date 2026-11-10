"""Acoplamientos flexibles: Oldham, de garras (Jaw) con araña, de fuelle y cardán."""
import math, sys
from lib import Lienzo, guardar_gif, suave, C, sombra, mezcla

W, H = 800, 480
TAU = 2 * math.pi

def sector(cx, cy, r0, r1, a0, a1, n=10):
    pts = [(cx + r1 * math.cos(a0 + (a1 - a0) * i / n), cy + r1 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    pts += [(cx + r0 * math.cos(a1 - (a1 - a0) * i / n), cy + r0 * math.sin(a1 - (a1 - a0) * i / n)) for i in range(n + 1)]
    return pts

def banda(cx, cy, ang, largo, ancho):
    ux, uy = math.cos(ang), math.sin(ang); nx, ny = -uy, ux
    l, a = largo / 2, ancho / 2
    return [(cx - ux * l - nx * a, cy - uy * l - ny * a), (cx + ux * l - nx * a, cy + uy * l - ny * a),
            (cx + ux * l + nx * a, cy + uy * l + ny * a), (cx - ux * l + nx * a, cy - uy * l + ny * a)]

# ======================================================================= Oldham
def oldham(ruta):
    base = Lienzo(W, H)
    base.titulo("Acoplamiento Oldham", "Une dos ejes paralelos que no están alineados")
    # vista lateral despiezada (estática) a la derecha
    base.panel(470, 96, 780, 316, "Despiece (vista lateral)")
    e = 14
    cy = 214
    # eje de entrada y cubo verde
    base.rect(484, cy - e / 2 - 9, 540, cy - e / 2 + 9, fill=C["verde_d"])
    base.rect(536, cy - e / 2 - 46, 566, cy - e / 2 + 46, fill=C["verde"], outline=C["verde_d"], w=1.5)
    base.rect(566, cy - e / 2 - 12, 572, cy - e / 2 + 12, fill=C["verde_l"], outline=C["verde_d"], w=1.2)   # ranura (hueco)
    # disco intermedio con dos lengüetas cruzadas
    base.rect(600, cy - 40, 616, cy + 40, fill=C["goma"], outline=C["goma_d"], w=1.5)
    base.rect(592, cy - 10, 600, cy + 10, fill=C["goma"], outline=C["goma_d"], w=1.2)      # lengüeta horizontal (vista de canto)
    base.rect(616, cy - 36, 624, cy + 36, fill=C["goma"], outline=C["goma_d"], w=1.2)      # lengüeta vertical
    # cubo azul y eje de salida (desplazado e)
    base.rect(650, cy + e / 2 - 46, 680, cy + e / 2 + 46, fill=C["azul"], outline=C["azul_d"], w=1.5)
    base.rect(644, cy + e / 2 - 40, 650, cy + e / 2 + 40, fill=C["azul_l"], outline=C["azul_d"], w=1.2)
    base.rect(676, cy + e / 2 - 9, 764, cy + e / 2 + 9, fill=C["azul_d"])
    base.dash_line((484, cy - e / 2), (600, cy - e / 2), C["verde_d"], 1.2)
    base.dash_line((616, cy + e / 2), (770, cy + e / 2), C["azul_d"], 1.2)
    base.text(540, 274, "Cubo motriz", "cond", 14, C["verde_d"], "ma")
    base.text(608, 150, "Disco", "cond", 14, C["goma_d"], "ma")
    base.text(690, 274, "Cubo conducido", "cond", 14, C["azul_d"], "ma")
    base.text(612, 292, "las lengüetas del disco forman 90°", "txt", 12, C["muted"], "ma")
    base.panel(470, 326, 780, 462, "Qué observar")
    for i, t in enumerate(["Los dos ejes giran a la misma velocidad.",
                           "El disco se desliza en las dos ranuras",
                           "y su centro describe un círculo pequeño.",
                           "Admite desalineación paralela, no angular."]):
        base.text(484, 352 + 24 * i, t, "txt", 14, C["ink"])
    fondo = base.im

    O = (240, 272); e2 = 26     # desalineación exagerada para verla
    O1 = (O[0] - e2 / 2, O[1]); O2 = (O[0] + e2 / 2, O[1])
    frames, dur = [], []
    N = 48
    for i in range(N):
        th = TAU * i / N
        L = Lienzo(W, H, base=fondo)
        L.text(28, 96, "VISTA FRONTAL", "neg", 12, C["muted"])
        ux, uy = math.cos(th), math.sin(th)
        # cubo motriz con su ranura
        L.circle(*O1, 128, fill=C["verde"], outline=C["verde_d"], w=2)
        L.poly(banda(O1[0], O1[1], th, 256, 34), fill=C["verde_d"])
        # disco intermedio: centro M en la intersección de las dos ranuras
        d = (O2[0] - O1[0]) * ux + (O2[1] - O1[1]) * uy
        M = (O1[0] + ux * d, O1[1] + uy * d)
        L.circle(*M, 104, fill=C["goma"], outline=C["goma_d"], w=2)
        L.poly(banda(M[0], M[1], th, 208, 30), fill=sombra(C["goma"], .86))                  # lengüeta trasera (en la ranura verde)
        L.poly(banda(M[0], M[1], th + math.pi / 2, 208, 30), fill=sombra(C["goma"], 1.25), outline=C["goma_d"], w=1.6)   # lengüeta delantera
        # ranura del cubo conducido (cubo azul quitado para verlo por dentro)
        vx, vy = -uy, ux
        for s in (-1, 1):
            a = (O2[0] + s * ux * 17 - vx * 138, O2[1] + s * uy * 17 - vy * 138)
            b = (O2[0] + s * ux * 17 + vx * 138, O2[1] + s * uy * 17 + vy * 138)
            L.line([a, b], C["azul_d"], 3)
        L.circle(*O2, 138, outline=C["azul"], w=4)
        # trayectoria del centro del disco
        L.dash_circle(O[0], O[1], e2 / 2, C["ink"], 1.2, (4, 3))
        L.circle(*M, 5, fill=C["ink"])
        L.circle(*O1, 4, fill=C["verde_d"]); L.circle(*O2, 4, fill=C["azul_d"])
        # marcas de giro
        L.circle(O1[0] + 112 * math.cos(th + 2.3), O1[1] + 112 * math.sin(th + 2.3), 6, fill=C["rojo"])
        L.arrow_arc(O[0], O[1], 160, -120, -60, 1, C["ink"], 3)
        L.text(28, 446, "Verde: cubo motriz · Naranja: disco · Azul: ranura del cubo conducido", "txt", 13, C["muted"])
        frames.append(L.fin()); dur.append(70)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Jaw (de garras)
def jaw(ruta):
    base = Lienzo(W, H)
    base.titulo("Acoplamiento de garras (Jaw)", "Dos cubos con garras y una araña elástica entre ellas")
    base.panel(470, 96, 780, 462, "Vista frontal (por dentro)")
    fondo = base.im
    frames, dur = [], []
    FC = (625, 290)
    def vista_frontal(L, th):
        L.circle(FC[0], FC[1], 120, fill=C["acero_l"], outline=C["acero_d"], w=1.5)
        for k in range(3):   # garras del cubo motriz y del conducido, alternas
            a = th + k * TAU / 3
            L.poly(sector(FC[0], FC[1], 46, 112, a - 0.36, a + 0.36), fill=C["verde"], outline=C["verde_d"], w=1.5)
            b = a + TAU / 6
            L.poly(sector(FC[0], FC[1], 46, 112, b - 0.36, b + 0.36), fill=C["azul"], outline=C["azul_d"], w=1.5)
        for k in range(6):   # brazos de la araña entre garras
            a = th + TAU / 12 + k * TAU / 6
            L.poly(sector(FC[0], FC[1], 40, 112, a - 0.16, a + 0.16), fill=C["goma"], outline=C["goma_d"], w=1.4)
        L.circle(FC[0], FC[1], 46, fill=C["goma"], outline=C["goma_d"], w=1.5)
        L.circle(FC[0], FC[1], 22, fill=C["ink"])
        L.circle(FC[0] + 86 * math.cos(th), FC[1] + 86 * math.sin(th), 5, fill=C["rojo"])
        L.text(FC[0], 424, "Las garras empujan a la araña de goma", "txt", 13, C["muted"], "ma")
        L.text(FC[0], 442, "y no se tocan entre sí", "txt", 13, C["muted"], "ma")

    def vista_lateral(L, sep, th):
        cy = 280
        R = 70
        xa = 250 - 46 - sep      # cara del cubo motriz
        xb = 250 + 46 + sep      # cara del cubo conducido
        # ejes
        L.rect(30, cy - 14, xa - 80, cy + 14, fill=C["verde_d"])
        L.rect(xb + 80, cy - 14, 450, cy + 14, fill=C["azul_d"])
        # cubos
        L.rect(xa - 80, cy - R, xa, cy + R, fill=C["verde"], outline=C["verde_d"], w=1.8, r=4)
        L.rect(xb, cy - R, xb + 80, cy + R, fill=C["azul"], outline=C["azul_d"], w=1.8, r=4)
        # garras proyectadas (3 por cubo), primero las de detrás
        items = []
        for k in range(3):
            a = th + k * TAU / 3
            items.append((math.sin(a), "v", a))
            items.append((math.sin(a + TAU / 6), "a", a + TAU / 6))
        for k in range(6):
            a = th + TAU / 12 + k * TAU / 6
            items.append((math.sin(a) + 0.01, "g", a))
        items.sort(key=lambda t: t[0])
        for prof, tipo, a in items:
            y0, y1 = sorted((cy - 62 * math.cos(a - .36), cy - 62 * math.cos(a + .36)))
            luz = 0.75 + 0.3 * max(0, prof)
            if tipo == "v":
                L.rect(xa, y0, xa + 40, y1, fill=sombra(C["verde"], luz), outline=C["verde_d"], w=1.2)
            elif tipo == "a":
                L.rect(xb - 40, y0, xb, y1, fill=sombra(C["azul"], luz), outline=C["azul_d"], w=1.2)
            else:
                g0, g1 = sorted((cy - 62 * math.cos(a - .16), cy - 62 * math.cos(a + .16)))
                L.rect(250 - 20, g0, 250 + 20, g1, fill=sombra(C["goma"], luz), outline=C["goma_d"], w=1.1)
        L.text(xa - 40, cy + R + 12, "Cubo motriz", "cond", 15, C["verde_d"], "ma")
        L.text(xb + 40, cy + R + 12, "Cubo conducido", "cond", 15, C["azul_d"], "ma")
        L.text(250, cy - R - 30, "Araña", "cond", 15, C["goma_d"], "ma")
        L.text(28, 96, "VISTA LATERAL", "neg", 12, C["muted"])

    N1, N2 = 16, 40
    th = 0.0
    seq = []
    for i in range(N1 + 1): seq.append(("monta", 1 - suave(i / N1)))
    for i in range(N2): seq.append(("gira", 0.0))
    for i in range(N1 + 1): seq.append(("monta", suave(i / N1)))
    for fase, s in seq:
        L = Lienzo(W, H, base=fondo)
        if fase == "gira": th += TAU / N2
        vista_lateral(L, 70 * s, th)
        vista_frontal(L, th)
        if fase == "gira":
            L.arrow_arc(FC[0], FC[1], 136, -120, -60, 1, C["ink"], 3)
            L.text(28, 446, "Montado: el giro pasa de un cubo a otro a través de la araña", "txt", 14, C["muted"])
        else:
            L.text(28, 446, "Montaje: las garras encajan en los huecos de la araña", "txt", 14, C["muted"])
        frames.append(L.fin()); dur.append(50)
    dur[N1] = 500
    dur[-1] = 700
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Fuelle
def fuelle(ruta):
    base = Lienzo(W, H)
    base.titulo("Acoplamiento de fuelle", "Un fuelle metálico une los dos cubos: se dobla, pero no se retuerce")
    fondo = base.im
    cy = 262
    xa = 250            # cara del cubo motriz
    R1, R0 = 64, 46     # radios exterior e interior de las ondas
    frames, dur = [], []
    fases = [("angular", "Desalineación angular", "los ejes forman un pequeño ángulo"),
             ("radial", "Desalineación radial", "los ejes están desplazados en paralelo"),
             ("axial", "Desalineación axial", "los ejes se acercan o se separan")]
    N = 30
    th = 0.0
    for fi, (tipo, tit, sub) in enumerate(fases):
        for i in range(N):
            t = math.sin(math.pi * i / N) ** 2     # 0 → 1 → 0
            th += TAU / 30
            beta = math.radians(9) * t if tipo == "angular" else 0.0
            dy = 22 * t if tipo == "radial" else 0.0
            dx = 22 * t if tipo == "axial" else 0.0
            L = Lienzo(W, H, base=fondo)
            # cara B (cubo conducido): posición y orientación
            lb = 150 + dx
            ux, uy = math.cos(-beta), math.sin(-beta)
            if tipo == "angular":
                piv = (xa + lb / 2, cy)
                B = (piv[0] + ux * lb / 2, piv[1] + uy * lb / 2)
            else:
                B = (xa + lb, cy + dy)
            # curva central del fuelle (Bézier cúbica de A a B)
            A = (xa, cy)
            P1 = (xa + lb * .38, cy); P2 = (B[0] - ux * lb * .38, B[1] - uy * lb * .38)
            def bez(t):
                m = 1 - t
                return (m**3 * A[0] + 3 * m * m * t * P1[0] + 3 * m * t * t * P2[0] + t**3 * B[0],
                        m**3 * A[1] + 3 * m * m * t * P1[1] + 3 * m * t * t * P2[1] + t**3 * B[1])
            n_ond = 7
            sup, inf, rad = [], [], []
            K = n_ond * 2
            for k in range(K + 1):
                tt = k / K
                p = bez(tt); q = bez(min(1, tt + 1e-3)) if tt < 1 else bez(tt); q0 = bez(max(0, tt - 1e-3))
                tx, ty = q[0] - q0[0], q[1] - q0[1]; ln = math.hypot(tx, ty) or 1
                nx, ny = -ty / ln, tx / ln
                r = R1 if k % 2 else R0
                if k in (0, K): r = R0
                sup.append((p[0] + nx * r, p[1] + ny * r)); inf.append((p[0] - nx * r, p[1] - ny * r)); rad.append((sup[-1], inf[-1]))
            # eje y cubo motriz
            L.rect(40, cy - 16, xa - 70, cy + 16, fill=C["verde_d"])
            L.rect(xa - 70, cy - 62, xa, cy + 62, fill=C["verde"], outline=C["verde_d"], w=1.8, r=4)
            # fuelle
            L.poly(sup + inf[::-1], fill=C["acero_l"], outline=C["acero_d"], w=1.6)
            for k, (a, b) in enumerate(rad[1:-1], 1):
                L.line([a, b], C["acero"] if k % 2 else C["acero_d"], 1.4 if k % 2 else 1.1)
            # cubo conducido y eje (girados beta)
            def rot(px, py): return (B[0] + ux * px - uy * py, B[1] + uy * px + ux * py)
            cubo = [rot(0, -62), rot(70, -62), rot(70, 62), rot(0, 62)]
            L.poly(cubo, fill=C["azul"], outline=C["azul_d"], w=1.8)
            eje = [rot(70, -16), rot(300, -16), rot(300, 16), rot(70, 16)]
            L.poly(eje, fill=C["azul_d"])
            # marcas de giro (tornillo de apriete que da vueltas)
            for (cx0, col, f) in ((xa - 35, C["verde_d"], None), (None, C["azul_d"], rot)):
                yy = 50 * math.cos(th)
                vis = math.sin(th) > 0
                if f is None:
                    if vis: L.rect(cx0 - 8, cy + yy - 5, cx0 + 8, cy + yy + 5, fill=C["rojo"])
                else:
                    if vis:
                        p = f(35, yy); L.circle(p[0], p[1], 6, fill=C["rojo"])
            L.dash_line((40, cy), (740, cy), C["muted"], 1.0)
            # rótulos
            L.text(xa - 35, cy + 76, "Cubo motriz", "cond", 15, C["verde_d"], "ma")
            L.text(B[0] + 35, cy + 76 + dy, "Cubo conducido", "cond", 15, C["azul_d"], "ma")
            L.text((xa + B[0]) / 2, cy - 98, "Fuelle metálico", "cond", 15, C["acero_d"], "ma")
            L.panel(28, 380, 772, 462)
            L.text(46, 394, tit.upper(), "neg", 12.5, C["rojo"])
            L.text(46, 414, sub[0].upper() + sub[1:] + ": el fuelle se deforma y lo absorbe.", "txt", 15, C["ink"])
            L.text(46, 436, "A torsión es muy rígido: transmite el giro sin holgura (ideal para encoders y servomotores).", "txt", 13.5, C["muted"])
            for j in range(3):
                L.circle(720 + j * 16, 401, 5, fill=C["rojo"] if j == fi else C["linea"])
            frames.append(L.fin()); dur.append(65)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Cardán
def cardan(ruta):
    base = Lienzo(W, H)
    base.titulo("Junta cardán", "Transmite el giro entre dos ejes que forman un ángulo")
    base.panel(498, 96, 780, 462, "Velocidad del eje de salida")
    fondo = base.im
    beta = math.radians(30)
    u = (math.cos(beta), math.sin(beta), 0.0)
    yaw, pitch = math.radians(-28), math.radians(16)
    O = (250, 272)
    def proy(p):
        x, y, z = p
        x1 = x * math.cos(yaw) + z * math.sin(yaw); z1 = -x * math.sin(yaw) + z * math.cos(yaw)
        y2 = y * math.cos(pitch) - z1 * math.sin(pitch); z2 = y * math.sin(pitch) + z1 * math.cos(pitch)
        return (O[0] + x1, O[1] - y2), z2
    def cruz(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    def esc(a, k): return (a[0] * k, a[1] * k, a[2] * k)
    def suma(*vs): return tuple(sum(v[i] for v in vs) for i in range(3))
    def norm(a):
        l = math.sqrt(sum(c * c for c in a)); return esc(a, 1 / l)
    # gráfica de la relación de velocidades
    gx0, gx1, gy0, gy1 = 520, 760, 160, 330
    def ratio(th): return math.cos(beta) / (1 - (math.sin(beta) ** 2) * (math.cos(th) ** 2))
    rmin, rmax = math.cos(beta), 1 / math.cos(beta)
    def gy(r): return gy1 - (r - 0.8) / (1.2 - 0.8) * (gy1 - gy0)
    base.line([(gx0, gy0), (gx0, gy1), (gx1, gy1)], C["muted"], 1.4)
    base.dash_line((gx0, gy(1.0)), (gx1, gy(1.0)), C["verde_d"], 1.2, (6, 4))
    base.text(gx0 - 6, gy(1.0) - 8, "1", "cond", 13, C["verde_d"], "ra")
    base.text(gx0 - 6, gy(rmax) - 8, f"{rmax:.2f}".replace(".", ","), "cond", 12, C["muted"], "ra")
    base.text(gx0 - 6, gy(rmin) - 8, f"{rmin:.2f}".replace(".", ","), "cond", 12, C["muted"], "ra")
    pts = [(gx0 + (gx1 - gx0) * k / 120, gy(ratio(TAU * k / 120))) for k in range(121)]
    base.line(pts, C["azul"], 2.6)
    base.text(gx1, gy1 + 8, "una vuelta", "txt", 12, C["muted"], "ra")
    base.text(512, 120, "salida / entrada (ángulo 30°)", "txt", 13, C["muted"])
    for i, t in enumerate(["La entrada gira a velocidad constante,",
                           "pero la salida acelera y frena dos veces",
                           "por vuelta. Con dos cardanes bien",
                           "montados la variación se compensa."]):
        base.text(512, 360 + 22 * i, t, "txt", 13.5, C["ink"])
    fondo = base.im
    frames, dur = [], []
    N = 64
    for i in range(N):
        th = TAU * i / N
        a = (0.0, math.cos(th), math.sin(th))
        b = norm(cruz(a, u))
        R = 60
        segs = []   # (puntos 3D, color, ancho)
        # eje y horquilla de entrada
        segs.append(([(-230, 0, 0), (-80, 0, 0)], C["verde_d"], 24))
        segs.append(([suma((-80, 0, 0), esc(a, -R)), suma((-80, 0, 0), esc(a, R))], C["verde"], 16))
        for s in (-1, 1):
            segs.append(([suma((-80, 0, 0), esc(a, s * R)), esc(a, s * R)], C["verde"], 15))
        # cruceta
        segs.append(([esc(a, -R), esc(a, R)], C["goma"], 11))
        segs.append(([esc(b, -R), esc(b, R)], C["goma_d"], 11))
        # horquilla y eje de salida
        for s in (-1, 1):
            segs.append(([esc(b, s * R), suma(esc(b, s * R), esc(u, 80))], C["azul"], 15))
        segs.append(([suma(esc(u, 80), esc(b, -R)), suma(esc(u, 80), esc(b, R))], C["azul"], 16))
        segs.append(([esc(u, 80), esc(u, 240)], C["azul_d"], 24))
        # marcas rojas en los ejes (giran con ellos)
        m1 = suma((-170, 0, 0), esc(a, 13))
        c2 = esc(u, 170)
        m2 = suma(c2, esc(b, 13))
        L = Lienzo(W, H, base=fondo)
        # prolongación del eje motriz y ángulo de 30° entre ejes
        p0 = proy((0, 0, 0))[0]; p1 = proy((230, 0, 0))[0]
        L.dash_line(p0, p1, C["muted"], 1.3, (8, 4))
        arco3 = [proy((150 * math.cos(beta * k / 16), 150 * math.sin(beta * k / 16), 0))[0] for k in range(17)]
        L.line(arco3, C["ink"], 2)
        pm = proy((172 * math.cos(beta / 2), 172 * math.sin(beta / 2), 0))[0]
        L.text(pm[0], pm[1] - 10, "30°", "tit", 18, C["ink"], "la")
        orden = []
        for pts3, col, w in segs:
            pr = [proy(p) for p in pts3]
            orden.append((sum(z for _, z in pr) / len(pr), [p for p, _ in pr], col, w))
        for (z, pts2, col, w) in sorted(orden, key=lambda t: t[0]):
            L.line(pts2, sombra(col, .8), w + 3)
            L.line(pts2, col, w)
            for p in pts2: L.circle(p[0], p[1], w / 2, fill=col)
        for mp, col in ((m1, C["rojo"]), (m2, C["rojo"])):
            (p, z) = proy(mp)
            L.circle(p[0], p[1], 5.5, fill=col)
        L.circle(*proy((0, 0, 0))[0], 9, fill=C["goma_d"])
        L.text(60, 318, "Eje motriz", "cond", 15, C["verde_d"])
        L.text(318, 146, "Eje conducido", "cond", 15, C["azul_d"])
        pc = proy((0, 0, 0))[0]
        L.leader(pc, (196, 366), C["goma_d"])
        L.text(150, 368, "Cruceta", "cond", 15, C["goma_d"])
        # punto en la gráfica
        L.circle(gx0 + (gx1 - gx0) * i / N, gy(ratio(th)), 6.5, fill=C["rojo"])
        frames.append(L.fin()); dur.append(55)
    return guardar_gif(frames, dur, ruta)

TODOS = {"acoplamiento-oldham": oldham, "acoplamiento-jaw": jaw, "acoplamiento-fuelle": fuelle, "cardan": cardan}

if __name__ == "__main__":
    salida = sys.argv[1]
    for n in sys.argv[2:] or TODOS.keys():
        print(n, TODOS[n](f"{salida}/{n}.gif"))
