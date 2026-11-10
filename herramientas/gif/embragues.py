"""Embragues: de dientes y de disco (fricción)."""
import math, sys
from lib import Lienzo, guardar_gif, suave, C, sombra

W, H = 800, 480
TAU = 2 * math.pi

def estado(L, x, y, titulo, texto, col):
    L.text(x, y, titulo.upper(), "neg", 13, col)
    for i, t in enumerate(texto):
        L.text(x, y + 22 + 20 * i, t, "txt", 14, C["ink"])

# ======================================================================= De dientes
def dientes(ruta):
    base = Lienzo(W, H)
    base.titulo("Embrague de dientes", "Dos piezas con dientes frontales que encajan: unen o separan dos ejes")
    base.panel(560, 96, 780, 462, "Giro")
    fondo = base.im
    cy = 262
    R = 66
    def dientes_proy(L, xcara, sentido, ang, col, osc, w=0.34, prof=26):
        items = []
        for k in range(4):
            a = ang + k * TAU / 4
            items.append((math.sin(a), a))
        for z, a in sorted(items):
            y0, y1 = sorted((cy - (R - 6) * math.cos(a - w), cy - (R - 6) * math.cos(a + w)))
            if y1 - y0 < 1.5: continue
            luz = 0.72 + 0.32 * max(0, z)
            x0, x1 = (xcara, xcara + prof) if sentido > 0 else (xcara - prof, xcara)
            L.rect(x0, y0, x1, y1, fill=sombra(col, luz), outline=osc, w=1.2)
    frames, dur = [], []
    ain, aout, wout = 0.0, 0.3, 0.0
    w_in = TAU / 30
    fases = [("libre", 26), ("embraga", 16), ("unido", 34), ("suelta", 16), ("frena", 14)]
    for fase, n in fases:
        for i in range(n):
            t = suave(i / max(1, n - 1))
            if fase == "libre": pos = 0.0
            elif fase == "embraga": pos = t
            elif fase == "unido": pos = 1.0
            elif fase == "suelta": pos = 1 - t
            else: pos = 0.0
            ain += w_in
            if fase in ("embraga", "unido") and pos > 0.55:
                wout = w_in; aout = ain + TAU / 8
            elif fase in ("suelta", "frena"):
                wout = max(0.0, wout - w_in / 14); aout += wout
            L = Lienzo(W, H, base=fondo)
            xf = 300                          # cara de la pieza fija (motriz)
            xm = 300 + 26 + 56 * (1 - pos)    # cara de la pieza móvil
            # eje motriz y pieza fija
            L.rect(36, cy - 16, 230, cy + 16, fill=C["verde_d"])
            L.rect(230, cy - R, xf, cy + R, fill=C["verde"], outline=C["verde_d"], w=1.8, r=4)
            dientes_proy(L, xf, +1, ain, C["verde"], C["verde_d"])
            # eje conducido con estrías y manguito deslizante
            L.rect(xm - 4, cy - 16, 540, cy + 16, fill=C["azul_d"])
            for k in range(9):
                xx = 400 + k * 12
                L.line([(xx, cy - 16), (xx, cy + 16)], sombra(C["azul_d"], 1.3), 1.2)
            dientes_proy(L, xm, -1, aout, C["azul"], C["azul_d"])
            L.rect(xm, cy - R, xm + 96, cy + R, fill=C["azul"], outline=C["azul_d"], w=1.8, r=4)
            L.rect(xm + 38, cy - R - 2, xm + 58, cy + R + 2, fill=C["azul_d"])                 # garganta para la horquilla
            # horquilla
            hx = xm + 48
            L.rect(hx - 6, cy - R - 70, hx + 6, cy - R + 8, fill=C["acero"], outline=C["acero_d"], w=1.4)
            L.rect(hx - 6, cy + R - 8, hx + 6, cy + R + 30, fill=C["acero"], outline=C["acero_d"], w=1.4)
            L.line([(hx, cy - R - 70), (hx - 30, cy - R - 110)], C["acero_d"], 6)
            L.circle(hx - 30, cy - R - 110, 7, fill=C["acero_d"])
            if fase in ("embraga", "suelta"):
                d = -1 if fase == "embraga" else 1
                L.arrow((hx + 34 - 16 * d, cy - R - 40), (hx + 34 + 18 * d, cy - R - 40), C["rojo"], 3, 11)
            L.text(265, cy + R + 14, "Pieza fija", "cond", 15, C["verde_d"], "ma")
            L.text(265, cy + R + 31, "(eje motriz)", "txt", 12, C["muted"], "ma")
            L.text(xm + 48, cy + R + 40, "Manguito deslizante", "cond", 15, C["azul_d"], "ma")
            L.text(xm + 48, cy + R + 57, "(sobre estrías del eje conducido)", "txt", 12, C["muted"], "ma")
            L.text(hx + 14, cy - R - 104, "Horquilla", "cond", 15, C["acero_d"])
            # diales
            L.dial(620, 186, 36, ain, C["verde"], "Eje motriz")
            L.dial(718, 186, 36, aout - TAU / 8, C["azul"], "Eje conducido")
            if fase == "libre" or fase == "frena":
                estado(L, 576, 278, "Desembragado", ["Los dientes no se tocan:", "el eje conducido no gira."], C["muted"])
            elif fase == "embraga":
                estado(L, 576, 278, "Embragando", ["La horquilla empuja el", "manguito hacia los dientes."], C["rojo"])
            elif fase == "unido":
                estado(L, 576, 278, "Embragado", ["Los dientes encajan y los", "dos ejes giran juntos."], C["verde_d"])
            else:
                estado(L, 576, 278, "Desembragando", ["La horquilla retira", "el manguito."], C["rojo"])
            L.text(576, 392, "Se acopla con los ejes parados", "txt", 12.5, C["muted"])
            L.text(576, 410, "o girando a la misma velocidad:", "txt", 12.5, C["muted"])
            L.text(576, 428, "no patina.", "txt", 12.5, C["muted"])
            frames.append(L.fin()); dur.append(60)
    return guardar_gif(frames, dur, ruta)

# ======================================================================= De disco
def disco(ruta):
    base = Lienzo(W, H)
    base.titulo("Embrague de disco", "El disco queda apretado entre el volante y el plato: transmite el giro por rozamiento")
    base.panel(560, 96, 780, 462, "Giro")
    base.text(28, 96, "SECCIÓN", "neg", 12, C["muted"])
    fondo = base.im
    cy = 272
    frames, dur = [], []
    a_m = a_c = 0.0
    rpm_c = 0.0
    RPM = 1500
    fases = [("pisado", 22), ("suelta", 12), ("patina", 26), ("unido", 26), ("pisa", 12)]
    for fase, n in fases:
        for i in range(n):
            t = suave(i / max(1, n - 1))
            if fase == "pisado": libre = 1.0
            elif fase == "suelta": libre = 1 - t
            elif fase == "pisa": libre = t
            else: libre = 0.0
            if fase == "patina": rpm_c = RPM * suave(i / (n - 1))
            elif fase == "unido": rpm_c = RPM
            elif fase in ("pisa", "pisado"): rpm_c = max(0.0, rpm_c - RPM / 16)
            a_m += TAU / 18
            a_c += TAU / 18 * rpm_c / RPM
            L = Lienzo(W, H, base=fondo)
            xv = 236                       # cara del volante
            xd = xv + 5 + 4 * libre        # placa del disco
            xp = xd + 11 + 10 * libre      # cara del plato de presión
            xb = 380 - 26 * libre          # cojinete de empuje
            def sim(pts):  # mitad superior y su simétrica
                return pts, [(x, 2 * cy - y) for x, y in pts]
            # eje motriz (no se raya) y volante
            L.rect(40, cy - 14, 200, cy + 14, fill=C["verde_d"])
            for pts in sim([(200, cy - 22), (xv, cy - 22), (xv, cy - 134), (200, cy - 134)]):
                L.poly(pts, fill=C["verde_l"]); L.hatch(pts, C["verde"], 7, ang=45); L.poly(pts, outline=C["verde_d"], w=1.8)
            # eje conducido
            L.rect(xv + 2, cy - 12, 540, cy + 12, fill=C["azul_d"])
            # disco: cubo, placa y forros
            for pts in sim([(xd - 8, cy - 12), (xd + 14, cy - 12), (xd + 14, cy - 30), (xd - 8, cy - 30)]):
                L.poly(pts, fill=C["azul"], outline=C["azul_d"], w=1.4)
            for pts in sim([(xd, cy - 30), (xd + 6, cy - 30), (xd + 6, cy - 120), (xd, cy - 120)]):
                L.poly(pts, fill=C["azul"], outline=C["azul_d"], w=1.2)
            for pts in sim([(xd - 5, cy - 72), (xd, cy - 72), (xd, cy - 120), (xd - 5, cy - 120)]) + sim([(xd + 6, cy - 72), (xd + 11, cy - 72), (xd + 11, cy - 120), (xd + 6, cy - 120)]):
                L.poly(pts, fill=C["cobre"], outline=C["cobre_d"], w=1.1)
            # plato de presión
            for pts in sim([(xp, cy - 64), (xp + 24, cy - 64), (xp + 24, cy - 124), (xp, cy - 124)]):
                L.poly(pts, fill=C["verde_l"]); L.hatch(pts, C["verde"], 7, ang=135); L.poly(pts, outline=C["verde_d"], w=1.8)
            # tapa (chapa) unida al volante
            for pts in sim([(xv, cy - 134), (338, cy - 134), (338, cy - 56)]):
                L.line(pts, C["verde_d"], 5)
            # muelles entre tapa y plato
            for s in (-1, 1):
                yy = cy + s * 98
                x0, x1 = xp + 24, 338
                zz = [(x0 + (x1 - x0) * k / 10, yy + (0 if k in (0, 10) else (7 if k % 2 else -7))) for k in range(11)]
                L.line(zz, C["acero_d"], 2.4)
            # palancas: pivote en la tapa, empujadas por el cojinete
            for s in (-1, 1):
                piv = (338, cy + s * 66)
                ext = (xp + 30, cy + s * 80)
                inn = (xb - 2, cy + s * 40)
                L.line([inn, piv, ext], C["acero_d"], 4)
                L.circle(piv[0], piv[1], 4.5, fill=C["ink"])
            # cojinete de empuje (collarín) y horquilla
            for pts in sim([(xb, cy - 14), (xb + 26, cy - 14), (xb + 26, cy - 42), (xb, cy - 42)]):
                L.poly(pts, fill=C["acero_l"], outline=C["acero_d"], w=1.4)
            L.line([(xb + 13, cy - 42), (xb + 13, cy - 118), (xb + 34, cy - 146)], C["acero_d"], 6)
            L.circle(xb + 13, cy - 118, 6, fill=C["ink"])
            if fase in ("suelta", "pisa"):
                d = 1 if fase == "suelta" else -1
                L.arrow((xb + 50, cy - 98), (xb + 50 + 30 * d, cy - 98), C["rojo"], 3, 11)
            # rozamiento
            if fase == "patina":
                for s in (-1, 1):
                    for k in range(3):
                        yy = cy + s * (80 + 14 * k)
                        L.line([(xd - 9, yy), (xd - 16 - (i + k) % 3 * 3, yy - 3)], C["rojo"], 2)
                        L.line([(xd + 15, yy), (xd + 22 + (i + k) % 3 * 3, yy - 3)], C["rojo"], 2)
            # rótulos
            L.text(176, 120, "Volante", "cond", 15, C["verde_d"])
            L.text(150, 414, "Disco (forros)", "cond", 15, C["cobre_d"])
            L.leader((xd - 3, cy + 100), (230, 412), C["cobre_d"])
            L.text(262, 98, "Plato de presión", "cond", 15, C["verde_d"])
            L.leader((xp + 10, cy - 118), (290, 116), C["verde_d"])
            L.text(400, 360, "Muelles", "cond", 15, C["acero_d"])
            L.leader((xp + 44, cy + 98), (402, 368), C["acero_d"])
            L.text(xb + 40, cy - 160, "Horquilla", "cond", 15, C["acero_d"])
            L.text(430, cy + 52, "Cojinete de empuje", "cond", 15, C["acero_d"])
            L.text(470, cy - 32, "eje de la caja", "txt", 12, C["azul_d"])
            L.text(46, cy - 32, "eje del motor", "txt", 12, C["verde_d"])
            # diales y estado
            L.dial(620, 182, 36, a_m, C["verde"], "Motor", f"{RPM} rpm")
            L.dial(718, 182, 36, a_c, C["azul"], "Caja", f"{int(round(rpm_c / 10) * 10)} rpm")
            if fase == "pisado":
                estado(L, 576, 290, "Pedal pisado", ["El plato se retira y el disco", "queda libre: no hay giro."], C["muted"])
            elif fase == "suelta":
                estado(L, 576, 290, "Soltando el pedal", ["Los muelles empujan el plato", "contra el disco."], C["rojo"])
            elif fase == "patina":
                estado(L, 576, 290, "Patinando", ["El disco roza y va cogiendo", "velocidad poco a poco."], C["rojo"])
            elif fase == "unido":
                estado(L, 576, 290, "Embragado", ["Disco apretado: todo gira", "junto, sin patinar."], C["verde_d"])
            else:
                estado(L, 576, 290, "Pisando el pedal", ["El cojinete empuja las palancas", "y el plato se separa."], C["rojo"])
            L.text(576, 410, "Permite arrancar en marcha", "txt", 12.5, C["muted"])
            L.text(576, 428, "de forma progresiva.", "txt", 12.5, C["muted"])
            frames.append(L.fin()); dur.append(65)
    return guardar_gif(frames, dur, ruta)

TODOS = {"embrague-dientes": dientes, "embrague-disco": disco}

if __name__ == "__main__":
    salida = sys.argv[1]
    for n in sys.argv[2:] or TODOS.keys():
        print(n, TODOS[n](f"{salida}/{n}.gif"))
