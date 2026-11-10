"""Transmisión por poleas, correas y cadenas: formas de poleas, tipos de correas y tipos de cadenas."""
import math, sys
from lib import Lienzo, guardar_gif, C, sombra, engranaje_pts

W, H = 800, 480
TAU = 2 * math.pi
GOMA = (52, 58, 66)          # caucho de la correa
GOMA_L = (96, 104, 114)

# ---------------------------------------------------------------- recorrido abierto alrededor de dos círculos
class Recorrido:
    def __init__(self, C1, r1, C2, r2):
        self.C1, self.r1, self.C2, self.r2 = C1, r1, C2, r2
        D = C2[0] - C1[0]
        nx = -(r2 - r1) / D
        ny = math.sqrt(1 - nx * nx)
        self.au = math.atan2(-ny, nx); self.al = math.atan2(ny, nx)
        T1u = (C1[0] + r1 * nx, C1[1] - r1 * ny); T2u = (C2[0] + r2 * nx, C2[1] - r2 * ny)
        T1l = (C1[0] + r1 * nx, C1[1] + r1 * ny); T2l = (C2[0] + r2 * nx, C2[1] + r2 * ny)
        self.seg = [("l", T1u, T2u), ("a", C2, r2, self.au, self.al), ("l", T2l, T1l), ("a", C1, r1, self.al, self.au + TAU)]
        self.len = []
        for s in self.seg:
            if s[0] == "l": self.len.append(math.dist(s[1], s[2]))
            else: self.len.append(s[2] * (s[4] - s[3]))
        self.total = sum(self.len)
    def punto(self, s):
        s %= self.total
        for sg, l in zip(self.seg, self.len):
            if s <= l:
                if sg[0] == "l":
                    t = s / l if l else 0
                    p = (sg[1][0] + (sg[2][0] - sg[1][0]) * t, sg[1][1] + (sg[2][1] - sg[1][1]) * t)
                    d = ((sg[2][0] - sg[1][0]) / l, (sg[2][1] - sg[1][1]) / l)
                    return p, d, None
                a = sg[3] + s / sg[2]
                p = (sg[1][0] + sg[2] * math.cos(a), sg[1][1] + sg[2] * math.sin(a))
                return p, (-math.sin(a), math.cos(a)), (sg[1], a)
            s -= l
        return self.punto(0)
    def polilinea(self, n=240):
        return [self.punto(self.total * k / n)[0] for k in range(n + 1)]

def offset(rec, d, n=240):
    pts = []
    for k in range(n + 1):
        p, t, _ = rec.punto(rec.total * k / n)
        nx, ny = t[1], -t[0]         # normal hacia fuera (el recorrido va en sentido horario)
        pts.append((p[0] + nx * d, p[1] + ny * d))
    return pts

def polea_frente(L, cx, cy, r, ang, col, osc, radios=3):
    L.circle(cx, cy, r + 6, fill=sombra(col, .9), outline=osc, w=1.8)
    L.circle(cx, cy, r - 6, fill=col, outline=osc, w=1.2)
    for k in range(radios):
        a = ang + k * TAU / radios
        L.line([(cx + 14 * math.cos(a), cy + 14 * math.sin(a)), (cx + (r - 10) * math.cos(a), cy + (r - 10) * math.sin(a))], sombra(col, .75), 9)
    L.circle(cx, cy, 16, fill=sombra(col, 1.5), outline=osc, w=1.5)
    L.circle(cx, cy, 5, fill=C["ink"])

# ======================================================================= Formas de poleas
def poleas(ruta):
    b = Lienzo(W, H)
    b.titulo("Poleas: formas", "La forma de la garganta depende del tipo de correa")
    # tarjetas de perfiles (sección de la llanta con su correa)
    tarjetas = ["Plana (abombada)", "Trapezoidal (en V)", "Poli-V (nervada)", "Dentada (síncrona)", "Redonda (de garganta)"]
    notas = ["correa plana", "trabaja por los flancos", "varios nervios", "no patina", "pequeñas potencias"]
    for i, (t, n) in enumerate(zip(tarjetas, notas)):
        x0 = 24 + i * 152
        b.panel(x0, 300, x0 + 144, 462)
        cx, base = x0 + 72, 410
        def T(p): return (cx + p[0], base - p[1])
        def llanta(pts):
            q = [T(p) for p in pts]
            b.poly(q, fill=C["acero_l"]); b.hatch(q, C["acero"], 6); b.poly(q, outline=C["acero_d"], w=1.6)
        def correa(pts):
            b.poly([T(p) for p in pts], fill=GOMA, outline=C["ink"], w=1.2)
        if i == 0:
            llanta([(-52, 0), (52, 0), (52, 30)] + [(52 - 104 * k / 16, 30 + 5 * math.sin(math.pi * k / 16)) for k in range(17)] + [(-52, 30)])
            correa([(-44, 31), (-44, 39)] + [(-44 + 88 * k / 12, 39 + 4 * math.sin(math.pi * k / 12)) for k in range(13)] + [(44, 39), (44, 31)] + [(44 - 88 * k / 12, 31 + 4 * math.sin(math.pi * k / 12)) for k in range(13)])
        elif i == 1:
            llanta([(-52, 0), (52, 0), (52, 46), (24, 46), (10, 10), (-10, 10), (-24, 46), (-52, 46)])
            correa([(-22, 52), (22, 52), (11, 20), (-11, 20)])
        elif i == 2:
            pts = [(-52, 0), (52, 0), (52, 34)]
            for k in range(5):
                xa = 40 - k * 20
                pts += [(xa, 34), (xa - 10, 22)]
            pts += [(-50, 34), (-52, 34)]
            llanta(pts)
            cp = [(-46, 48), (46, 48), (46, 38)]
            for k in range(5):
                xa = 40 - k * 20
                cp += [(xa + 4, 36), (xa - 10, 24.5), (xa - 16, 36)] if k < 4 else [(xa + 4, 36), (xa - 10, 24.5), (-46, 36)]
            cp += [(-46, 38)]
            correa(cp)
        elif i == 3:
            pts = [(-52, 0), (52, 0), (52, 30)]
            for k in range(6):
                xa = 52 - k * 18
                pts += [(xa, 30), (xa - 4, 30), (xa - 6, 22), (xa - 12, 22), (xa - 14, 30)]
            pts += [(-52, 30)]
            llanta(pts)
            cp = [(-50, 42), (50, 42), (50, 32)]
            for k in range(6):
                xa = 52 - k * 18
                cp += [(xa - 4, 32), (xa - 5.5, 24), (xa - 12.5, 24), (xa - 14, 32)]
            cp += [(-50, 32)]
            correa(cp)
            b.text(cx, 314, "vista de frente", "txt", 10.5, C["muted"], "ma")
        else:
            llanta([(-52, 0), (52, 0), (52, 40), (18, 40)] + [(18 * math.cos(math.pi * k / 16), 40 - 18 * math.sin(math.pi * k / 16)) for k in range(17)] + [(-18, 40), (-52, 40)])
            b.circle(*T((0, 38)), 15, fill=GOMA, outline=C["ink"], w=1.2)
        b.text(cx, 424, t, "tit", 15, C["ink"], "ma")
        b.text(cx, 442, n, "txt", 12, C["muted"], "ma")
    b.text(28, 96, "TRANSMISIÓN POR CORREA", "neg", 12, C["muted"])
    b.text(560, 140, "Relación de transmisión", "tit", 17, C["ink"])
    b.text(560, 164, "i = D₂ / D₁", "sim", 17, C["ink"])
    b.text(560, 192, "La polea pequeña da 1,5 vueltas", "txt", 14, C["muted"])
    b.text(560, 210, "por cada vuelta de la grande.", "txt", 14, C["muted"])
    b.text(560, 238, "Las dos giran en el mismo sentido.", "txt", 14, C["muted"])
    fondo = b.im
    r1, r2 = 50, 75
    C1, C2 = (130, 196), (420, 196)
    rec = Recorrido(C1, r1, C2, r2)
    frames, dur = [], []
    N = 48
    esp = TAU * r1 / 12
    for i in range(N):
        sh = TAU * r1 * i / N
        L = Lienzo(W, H, base=fondo)
        polea_frente(L, *C2, r2, sh / r2, C["azul"], C["azul_d"], 3)
        polea_frente(L, *C1, r1, sh / r1, C["verde"], C["verde_d"], 4)
        L.line(rec.polilinea(), GOMA, 10)
        for k in range(int(rec.total / esp) + 1):
            p, t, _ = rec.punto(sh + k * esp)
            L.line([(p[0] - t[0] * 4, p[1] - t[1] * 4), (p[0] + t[0] * 4, p[1] + t[1] * 4)], GOMA_L, 6)
        L.text(C1[0], C1[1] + r1 + 18, "Motriz", "cond", 15, C["verde_d"], "ma")
        L.text(C2[0] + r2 + 14, C2[1] + 30, "Conducida", "cond", 15, C["azul_d"])
        L.arrow(((C1[0] + C2[0]) / 2 - 40, C1[1] - r2 - 24), ((C1[0] + C2[0]) / 2 + 40, C1[1] - r2 - 24), C["ink"], 3, 11)
        frames.append(L.fin()); dur.append(60)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Tipos de correas
def correas(ruta):
    b = Lienzo(W, H)
    b.titulo("Correas: tipos", "Cada correa tiene su sección y su uso")
    filas = [("Plana", "Grandes distancias y velocidades altas"),
             ("Trapezoidal (en V)", "La más usada: se encaja en la garganta"),
             ("Poli-V (nervada)", "Delgada y flexible: poleas pequeñas"),
             ("Dentada (síncrona)", "No patina: sincroniza ejes"),
             ("Redonda", "Pequeñas potencias")]
    y0 = 96
    hf = 72
    b.text(256, y0, "VISTA LATERAL (EN MOVIMIENTO)", "neg", 11, C["muted"])
    b.text(722, y0, "SECCIÓN", "neg", 11, C["muted"], "ma")
    for i, (t, d) in enumerate(filas):
        yc = y0 + 22 + i * hf + 30
        b.line([(24, yc + 34), (776, yc + 34)], C["linea"], 1)
        b.text(28, yc - 14, t, "tit", 17, C["ink"])
        b.text(28, yc + 6, d, "txt", 12.5, C["muted"])
        cx = 722
        def S(pts): return [(cx + x, yc - y) for x, y in pts]
        if i == 0:
            b.rect(cx - 44, yc - 5, cx + 44, yc + 5, fill=GOMA, outline=C["ink"], w=1.2)
            for k in range(9): b.circle(cx - 36 + k * 9, yc, 1.8, fill=C["acero_l"])
        elif i == 1:
            b.poly(S([(-22, 12), (22, 12), (11, -14), (-11, -14)]), fill=GOMA, outline=C["ink"], w=1.2)
            for k in range(5): b.circle(cx - 14 + k * 7, yc - 6, 2, fill=C["acero_l"])
        elif i == 2:
            pts = [(-40, 10), (40, 10), (40, 2)]
            for k in range(5): pts += [(32 - k * 16 + 6, 2), (32 - k * 16, -10), (32 - k * 16 - 6, 2)]
            pts += [(-40, 2)]
            b.poly(S(pts), fill=GOMA, outline=C["ink"], w=1.2)
            for k in range(9): b.circle(cx - 36 + k * 9, yc - 6, 1.6, fill=C["acero_l"])
        elif i == 3:
            b.rect(cx - 40, yc - 10, cx + 40, yc + 8, fill=GOMA, outline=C["ink"], w=1.2)
            b.line([(cx - 40, yc - 1), (cx + 40, yc - 1)], C["ink"], 1)
            for k in range(9): b.circle(cx - 36 + k * 9, yc - 5, 1.8, fill=C["acero_l"])
            b.text(cx, yc + 14, "diente abajo", "txt", 10, C["muted"], "ma")
        else:
            b.circle(cx, yc, 12, fill=GOMA, outline=C["ink"], w=1.2)
    fondo = b.im
    frames, dur = [], []
    N = 40
    x0, x1 = 256, 620
    for f in range(N):
        sh = 48 * f / N
        L = Lienzo(W, H, base=fondo)
        for i in range(5):
            yc = y0 + 22 + i * hf + 30
            if i == 0:
                L.rect(x0, yc - 5, x1, yc + 5, fill=GOMA)
                for k in range(-1, 10):
                    xx = x0 + (k * 48 + sh) % (x1 - x0 + 48) - 24
                    if x0 < xx < x1 - 10: L.line([(xx, yc), (xx + 10, yc)], GOMA_L, 3)
            elif i == 1:
                L.rect(x0, yc - 12, x1, yc + 14, fill=GOMA)
                L.line([(x0, yc - 5), (x1, yc - 5)], GOMA_L, 1.5)
                for k in range(-1, 10):
                    xx = x0 + (k * 48 + sh) % (x1 - x0 + 48) - 24
                    if x0 < xx < x1 - 12: L.text(xx, yc - 2, "|||", "txt", 11, GOMA_L)
            elif i == 2:
                L.rect(x0, yc - 10, x1, yc + 10, fill=GOMA)
                for yy in (yc + 3, yc + 7): L.line([(x0, yy), (x1, yy)], GOMA_L, 1.2)
                for k in range(-1, 10):
                    xx = x0 + (k * 48 + sh) % (x1 - x0 + 48) - 24
                    if x0 < xx < x1 - 10: L.line([(xx, yc - 4), (xx + 10, yc - 4)], GOMA_L, 3)
            elif i == 3:
                L.rect(x0, yc - 10, x1, yc - 1, fill=GOMA)
                p = 16
                k0 = -2
                while True:
                    xx = x0 + k0 * p + (sh % p)
                    if xx > x1: break
                    if xx + 9 > x0 and xx < x1:
                        a, bb = max(x0, xx), min(x1, xx + 9)
                        if bb > a: L.poly([(a, yc - 1), (bb, yc - 1), (min(bb, max(a, xx + 7.5)), yc + 8), (max(a, min(bb, xx + 1.5)), yc + 8)], fill=GOMA)
                    k0 += 1
            else:
                L.rect(x0, yc - 12, x1, yc + 12, fill=GOMA, r=12)
                L.line([(x0 + 10, yc - 6), (x1 - 10, yc - 6)], GOMA_L, 2.5)
                for k in range(-1, 10):
                    xx = x0 + (k * 48 + sh) % (x1 - x0 + 48) - 24
                    if x0 + 12 < xx < x1 - 22: L.line([(xx, yc + 2), (xx + 10, yc + 2)], GOMA_L, 2)
            L.arrow((x1 + 10, yc), (x1 + 34, yc), C["ink"], 2.4, 9)
        frames.append(L.fin()); dur.append(60)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= Tipos de cadenas
def cadenas(ruta):
    b = Lienzo(W, H)
    b.titulo("Cadenas: tipos", "Transmiten mucha fuerza sin patinar entre ejes paralelos")
    b.text(28, 96, "TRANSMISIÓN POR CADENA", "neg", 12, C["muted"])
    # partes de la cadena de rodillos (vista en planta, ampliada)
    b.panel(486, 92, 780, 282, "Partes (vista en planta)")
    px0, py = 520, 196
    P = 64
    for k in range(4):
        x = px0 + k * P
        ext = k % 2 == 0
        if k < 3:
            if ext:
                b.rect(x - 14, py - 42, x + P + 14, py - 30, fill=C["acero_d"], r=6)
                b.rect(x - 14, py + 30, x + P + 14, py + 42, fill=C["acero_d"], r=6)
            else:
                b.rect(x - 12, py - 30, x + P + 12, py - 20, fill=C["acero"], r=5)
                b.rect(x - 12, py + 20, x + P + 12, py + 30, fill=C["acero"], r=5)
        b.rect(x - 4, py - 46, x + 4, py + 46, fill=C["acero_l"], outline=C["acero_d"], w=1.2)
        b.rect(x - 11, py - 20, x + 11, py + 20, fill=C["cobre"], outline=C["cobre_d"], w=1.2)
    b.leader((px0 + P / 2, py - 36), (560, 128)); b.text(564, 120, "placa exterior", "txt", 12, C["ink"])
    b.leader((px0 + P * 1.5, py - 25), (668, 128)); b.text(672, 120, "placa interior", "txt", 12, C["ink"])
    b.leader((px0, py + 44), (548, 262)); b.text(552, 258, "pasador", "txt", 12, C["ink"])
    b.leader((px0 + P * 2, py + 10), (660, 262)); b.text(664, 258, "rodillo (sobre casquillo)", "txt", 12, C["ink"])
    # tipos (abajo)
    tipos = [("De rodillos simple", "la más común (bicicleta, motos)"),
             ("De rodillos doble (dúplex)", "dos filas: más potencia"),
             ("Silenciosa (de dientes)", "placas dentadas: menos ruido")]
    for i, (t, d) in enumerate(tipos):
        x0 = 24 + i * 252
        b.panel(x0, 300, x0 + 244, 462)
        b.text(x0 + 14, 312, t, "tit", 15, C["ink"])
        b.text(x0 + 14, 331, d, "txt", 12, C["muted"])
    fondo = b.im

    p = 22
    z1, z2 = 12, 20
    R1, R2 = z1 * p / TAU, z2 * p / TAU
    C1 = (118, 196)
    # distancia entre centros para un número entero de eslabones
    n = 34
    lo, hi = R1 + R2 + 10, 500
    for _ in range(60):
        mid = (lo + hi) / 2
        if Recorrido(C1, R1, (C1[0] + mid, C1[1]), R2).total < n * p: lo = mid
        else: hi = mid
    C2 = (C1[0] + lo, C1[1])
    rec = Recorrido(C1, R1, C2, R2)
    paso = rec.total / n
    frames, dur = [], []
    N = 30
    for f in range(N):
        sh = 2 * paso * f / N
        L = Lienzo(W, H, base=fondo)
        rod = [rec.punto(sh + k * paso) for k in range(n)]
        # piñones: un hueco en cada rodillo que apoya
        for (Cc, Rr, z, col, osc) in ((C2, R2, z2, C["azul"], C["azul_d"]), (C1, R1, z1, C["verde"], C["verde_d"])):
            ang = None
            for (pp, t, arc) in rod:
                if arc and arc[0] == Cc: ang = arc[1]; break
            if ang is None: ang = 0
            L.poly(engranaje_pts(Cc[0], Cc[1], 2 * Rr / z, z, ang + math.pi / z, wr=1.0, wt=0.55), fill=col, outline=osc, w=1.4)
            L.circle(Cc[0], Cc[1], Rr * .45, fill=sombra(col, 1.5), outline=osc, w=1.4)
            L.circle(Cc[0], Cc[1], 5, fill=C["ink"])
        # placas y rodillos
        for k in range(n):
            a = rod[k][0]; bpt = rod[(k + 1) % n][0]
            L.line([a, bpt], C["acero_d"] if k % 2 == 0 else C["acero"], 12 if k % 2 == 0 else 9)
        for k in range(n):
            L.circle(*rod[k][0], 5.5, fill=C["cobre"], outline=C["cobre_d"], w=1.2)
        L.text(C1[0], C1[1] + R1 + 28, "Piñón motriz", "cond", 15, C["verde_d"], "ma")
        L.text(C2[0] + R2 + 16, C2[1] - 18, "Corona", "cond", 15, C["azul_d"])
        L.text(C2[0] + R2 + 16, C2[1], "conducida", "cond", 15, C["azul_d"])
        # tiras de tipos en movimiento
        for i in range(3):
            x0 = 24 + i * 252
            ya = 400
            s = (2 * 20 * f / N)
            if i < 2:
                filas = 1 if i == 0 else 2
                for fi in range(filas):
                    yy = ya + (fi - (filas - 1) / 2) * 30
                    k = -2
                    while True:
                        x = x0 + 14 + k * 20 + s
                        if x > x0 + 232: break
                        if x > x0 + 10:
                            ext = (k % 2 == 0)
                            if x + 20 < x0 + 234:
                                L.rect(x - 6, yy - 14, x + 26, yy - 9, fill=C["acero_d"] if ext else C["acero"], r=2)
                                L.rect(x - 6, yy + 9, x + 26, yy + 14, fill=C["acero_d"] if ext else C["acero"], r=2)
                            L.rect(x - 2, yy - 16, x + 2, yy + 16, fill=C["acero_l"], outline=C["acero_d"], w=1)
                            L.rect(x - 6, yy - 8, x + 6, yy + 8, fill=C["cobre"], outline=C["cobre_d"], w=1)
                        k += 1
            else:
                k = -2
                while True:
                    x = x0 + 14 + k * 20 + s
                    if x > x0 + 232: break
                    if x > x0 + 8 and x + 24 < x0 + 236:
                        L.poly([(x, ya - 10), (x + 24, ya - 10), (x + 24, ya + 4), (x + 18, ya + 16), (x + 12, ya + 6), (x + 6, ya + 16), (x, ya + 4)],
                               fill=C["acero"] if k % 2 else C["acero_d"], outline=C["ink"], w=1)
                        L.circle(x + 3, ya - 3, 2.5, fill=C["acero_l"])
                    k += 1
            L.text(x0 + 122, 446, "vista lateral" if i == 2 else "vista en planta", "txt", 11, C["muted"], "ma")
        frames.append(L.fin()); dur.append(80)
    return guardar_gif(frames, dur, ruta)

TODOS = {"formas-poleas": poleas, "tipos-correas": correas, "tipos-cadenas": cadenas}

if __name__ == "__main__":
    salida = sys.argv[1]
    for n in sys.argv[2:] or TODOS.keys():
        print(n, TODOS[n](f"{salida}/{n}.gif"))
