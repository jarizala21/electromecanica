"""Imágenes 3D realistas (Blender Cycles) del engranaje y del regulador de presión del menú de áreas,
con fondo transparente. Necesita el módulo bpy (pip install bpy, con Python 3.11) y la esfera del
manómetro (python3 herramientas/imagenes/esfera_manometro.py).
Uso: python3.11 herramientas/imagenes/render_areas.py engranaje|regulador salida.png [ancho] [muestras]
Después se recorta y se pasa a WebP (ver LEEME)."""
import bpy, bmesh, math, os, sys
from mathutils import Vector

QUE = sys.argv[1]
SALIDA = sys.argv[2]
ANCHO = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
MUESTRAS = int(sys.argv[4]) if len(sys.argv) > 4 else 96
DIAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "esfera_manometro.png")

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = MUESTRAS
sc.cycles.use_denoising = True
sc.render.film_transparent = True
sc.render.resolution_x = ANCHO
sc.render.resolution_y = ANCHO
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
sc.view_settings.view_transform = "AgX"
for look in ("AgX - Punchy", "Punchy", "AgX - Medium High Contrast"):
    try:
        sc.view_settings.look = look
        break
    except Exception:
        pass

# ---------- materiales ----------
def mat(nombre, color, metal=0.0, rough=0.4, **extra):
    m = bpy.data.materials.new(nombre)
    try: m.use_nodes = True
    except Exception: pass
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    for k, v in extra.items():
        p.inputs[k].default_value = v
    return m

def mat_imagen(nombre, ruta):
    m = bpy.data.materials.new(nombre)
    try: m.use_nodes = True
    except Exception: pass
    nt = m.node_tree
    p = nt.nodes.get("Principled BSDF")
    p.inputs["Roughness"].default_value = 0.5
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(ruta)
    nt.links.new(tex.outputs["Color"], p.inputs["Base Color"])
    return m

# ---------- geometría ----------
def objeto(nombre, mesh, material, loc=(0, 0, 0), rot=(0, 0, 0), smooth_ang=None):
    o = bpy.data.objects.new(nombre, mesh)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    if material: o.data.materials.append(material)
    if smooth_ang is not None:
        for f in o.data.polygons: f.use_smooth = True
        try:
            o.data.set_sharp_from_angle(angle=math.radians(smooth_ang))
        except Exception:
            mod = o.modifiers.new("ss", "SMOOTH_BY_ANGLE") if hasattr(bpy.types, "NodesModifier") else None
    return o

def perfil(nombre, contornos, grosor, material, bisel=0.01, loc=(0, 0, 0), rot=(0, 0, 0)):
    """Extruye una o varias curvas cerradas 2D (los contornos interiores hacen de agujeros)."""
    cu = bpy.data.curves.new(nombre, "CURVE")
    cu.dimensions = "2D"
    cu.fill_mode = "BOTH"
    cu.extrude = max(grosor / 2 - bisel, 0.0005)
    cu.bevel_depth = bisel
    cu.bevel_resolution = 2
    for pts in contornos:
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for i, (x, y) in enumerate(pts):
            sp.points[i].co = (x, y, 0, 1)
        sp.use_cyclic_u = True
    o = bpy.data.objects.new(nombre, cu)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    o.data.materials.append(material)
    return o

def circulo(r, n=96, c=(0, 0), fase=0.0):
    return [(c[0] + r * math.cos(fase + 2 * math.pi * i / n), c[1] + r * math.sin(fase + 2 * math.pi * i / n)) for i in range(n)]

def chavetero(r, ancho, prof, n=72):
    """Agujero del eje con chavetero arriba."""
    pts = []
    a0 = math.asin(ancho / 2 / r)
    for i in range(n + 1):
        a = math.pi / 2 + a0 + (2 * math.pi - 2 * a0) * i / n
        pts.append((r * math.cos(a), r * math.sin(a)))
    pts += [(ancho / 2, r + prof), (-ancho / 2, r + prof)]
    pts.reverse()
    return pts

def inv(a): return math.tan(a) - a

def dientes(z, m, fase=0.0, paso=10):
    alfa = math.radians(20)
    rp, ra, rf = m * z / 2, m * z / 2 + m, m * z / 2 - 1.25 * m
    rb = rp * math.cos(alfa)
    psi = math.pi / (2 * z) + inv(alfa)
    def ang(r):
        r = max(r, rb)
        return psi - inv(math.acos(rb / r))
    radios = [rf] + [max(rb, rf) + (ra - max(rb, rf)) * k / paso for k in range(paso + 1)]
    pts = []
    for t in range(z):
        c = fase + 2 * math.pi * t / z
        flanco = [(r, ang(r)) for r in radios]
        for r, a in flanco:  # flanco izquierdo, de pie a cabeza
            pts.append((r * math.cos(c - a), r * math.sin(c - a)))
        a_tip = ang(ra)
        for k in range(1, 4):
            a = -a_tip + 2 * a_tip * k / 4
            pts.append((ra * math.cos(c + a), ra * math.sin(c + a)))
        for r, a in reversed(flanco):
            pts.append((r * math.cos(c + a), r * math.sin(c + a)))
        # fondo hasta el diente siguiente
        a0 = c + ang(rf)
        a1 = c + 2 * math.pi / z - ang(rf)
        for k in range(1, 4):
            a = a0 + (a1 - a0) * k / 4
            pts.append((rf * math.cos(a), rf * math.sin(a)))
    return pts, rf

# ---------- estudio ----------
def estudio(objetivo, dist, alt_grados, azim_grados, focal=85, luz=1.0):
    w = bpy.data.worlds.new("Mundo")
    sc.world = w
    try: w.use_nodes = True
    except Exception: pass
    nt = w.node_tree
    bg = nt.nodes.get("Background") or nt.nodes.new("ShaderNodeBackground")
    out = nt.nodes.get("World Output") or nt.nodes.new("ShaderNodeOutputWorld")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (0.06, 0.065, 0.075, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1)
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -1
    mr.inputs["From Max"].default_value = 1
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.8
    nt.links.new(bg.outputs[0], out.inputs[0])

    def area(nombre, pos, energia, tam, color=(1, 1, 1)):
        l = bpy.data.lights.new(nombre, "AREA")
        l.energy = energia * luz
        l.size = tam
        l.color = color
        o = bpy.data.objects.new(nombre, l)
        bpy.context.collection.objects.link(o)
        o.location = pos
        d = Vector(objetivo) - Vector(pos)
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        return o
    area("clave", (-4, -5, 5), 1500, 3.5)
    area("relleno", (5, -3, 1.5), 500, 4, (0.92, 0.95, 1.0))
    area("contra", (1, 5, 5), 1200, 3, (1.0, 0.93, 0.85))
    area("bajo", (0, -4, -2.5), 120, 4)
    # softbox grande junto a la cámara: da brillo a las caras que miran al frente
    alt, az = math.radians(alt_grados + 14), math.radians(azim_grados - 22)
    area("frente", (objetivo[0] + 9 * math.cos(alt) * math.sin(az), objetivo[1] - 9 * math.cos(alt) * math.cos(az),
                    objetivo[2] + 9 * math.sin(alt)), 900, 6)

    cam_d = bpy.data.cameras.new("Camara")
    cam_d.lens = focal
    cam = bpy.data.objects.new("Camara", cam_d)
    bpy.context.collection.objects.link(cam)
    alt, az = math.radians(alt_grados), math.radians(azim_grados)
    cam.location = (objetivo[0] + dist * math.cos(alt) * math.sin(az),
                    objetivo[1] - dist * math.cos(alt) * math.cos(az),
                    objetivo[2] + dist * math.sin(alt))
    d = Vector(objetivo) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam

# ---------- engranaje ----------
def engranajes():
    acero = mat("acero", (0.66, 0.67, 0.69), 1.0, 0.32)
    pavonado = mat("pavonado", (0.42, 0.43, 0.46), 1.0, 0.36)
    m = 0.075
    z1, z2 = 32, 14
    # rueda grande: corona dentada + alma con aligeramientos + cubo
    perfil_g, rf = dientes(z1, m)
    r_alma = rf - 0.16
    perfil("corona", [perfil_g, circulo(r_alma, 128)], 0.36, acero, 0.012)
    agujeros = [circulo(0.17, 48, (0.82 * math.cos(a), 0.82 * math.sin(a))) for a in [math.pi / 2 + 2 * math.pi * k / 5 for k in range(5)]]
    perfil("alma", [circulo(r_alma + 0.01, 128)] + agujeros + [circulo(0.42, 64)], 0.16, acero, 0.006)
    perfil("cubo", [circulo(0.45, 96), chavetero(0.2, 0.09, 0.05)], 0.52, acero, 0.015)
    # piñón
    a = m * (z1 + z2) / 2
    perfil_p, _ = dientes(z2, m, fase=math.pi + math.pi / z2)
    perfil("pinon", [perfil_p, chavetero(0.13, 0.06, 0.035)], 0.4, pavonado, 0.012, loc=(a, 0, 0))
    perfil("cubo_p", [circulo(0.3, 72), chavetero(0.13, 0.06, 0.035)], 0.62, pavonado, 0.012, loc=(a, 0, 0))
    # de pie, mirando hacia la cámara
    for o in list(bpy.data.objects):
        if o.type in ("CURVE", "MESH"):
            o.location = (o.location.x, o.location.z, o.location.y)
            o.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.empty_add(location=(0, 0, 0))
    raiz = bpy.context.active_object
    for o in bpy.data.objects:
        if o.type in ("CURVE", "MESH"): o.parent = raiz
    raiz.rotation_euler = (0, math.radians(-8), math.radians(-28))
    raiz.location = (-a / 2 + 0.3, 0, 0)
    estudio((0.05, 0, -0.05), 13.5, 18, -12, focal=85)

# ---------- regulador ----------
def regulador():
    alu = mat("aluminio", (0.74, 0.75, 0.77), 1.0, 0.45)
    negro = mat("plastico", (0.025, 0.025, 0.028), 0.0, 0.42)
    niquel = mat("niquel", (0.8, 0.8, 0.8), 1.0, 0.16)
    laton = mat("laton", (0.85, 0.62, 0.32), 1.0, 0.25)
    azul = mat("tubo", (0.02, 0.18, 0.72), 0.0, 0.32, **{"Coat Weight": 0.4})
    cromo = mat("cromo", (0.9, 0.9, 0.92), 1.0, 0.06)
    vidrio = mat("vidrio", (1, 1, 1), 0.0, 0.0, **{"Transmission Weight": 1.0, "IOR": 1.5})
    dial = mat_imagen("dial", DIAL)

    # cuerpo
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.55))
    c = bpy.context.active_object
    c.scale = (1.0, 1.0, 1.1)
    bpy.ops.object.transform_apply(scale=True)
    bv = c.modifiers.new("bisel", "BEVEL"); bv.width = 0.07; bv.segments = 4
    c.data.materials.append(alu)
    for f in c.data.polygons: f.use_smooth = True
    # tuerca de panel y bonete
    perfil("tuerca", [circulo(0.5, 6, fase=math.pi / 6), circulo(0.3, 48)], 0.12, niquel, 0.012, loc=(0, 0, 1.16))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.55, vertices=96, location=(0, 0, 1.38))
    b = bpy.context.active_object; b.data.materials.append(negro)
    bv = b.modifiers.new("bisel", "BEVEL"); bv.width = 0.03; bv.segments = 3
    for f in b.data.polygons: f.use_smooth = True
    # pomo moleteado
    estrella = []
    n = 44
    for i in range(2 * n):
        r = 0.52 if i % 2 == 0 else 0.485
        a = math.pi * i / n
        estrella.append((r * math.cos(a), r * math.sin(a)))
    perfil("pomo", [estrella], 0.42, negro, 0.02, loc=(0, 0, 1.86))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.44, depth=0.04, vertices=96, location=(0, 0, 2.08))
    t = bpy.context.active_object; t.data.materials.append(negro)
    # conexiones a los lados con tubo azul
    for s in (-1, 1):
        perfil("hex%d" % s, [circulo(0.24, 6, fase=math.pi / 6)], 0.14, laton, 0.01,
               loc=(s * 0.57, 0, 0.55), rot=(0, math.radians(90), 0))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.19, depth=0.3, vertices=64, location=(s * 0.79, 0, 0.55), rotation=(0, math.radians(90), 0))
        o = bpy.context.active_object; o.data.materials.append(niquel)
        for f in o.data.polygons: f.use_smooth = True
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.07, vertices=64, location=(s * 0.97, 0, 0.55), rotation=(0, math.radians(90), 0))
        o = bpy.context.active_object; o.data.materials.append(azul)
        for f in o.data.polygons: f.use_smooth = True
        bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=1.1, vertices=64, location=(s * 1.52, 0, 0.55), rotation=(0, math.radians(90), 0))
        o = bpy.context.active_object; o.data.materials.append(azul)
        for f in o.data.polygons: f.use_smooth = True
    # manómetro en el frente
    yf = -0.5
    def cil(r, prof, y, material, verts=96, bisel=0.0):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=prof, vertices=verts, location=(0, y, 0.55), rotation=(math.radians(90), 0, 0))
        o = bpy.context.active_object; o.data.materials.append(material)
        if bisel:
            bv = o.modifiers.new("bisel", "BEVEL"); bv.width = bisel; bv.segments = 3
        for f in o.data.polygons: f.use_smooth = True
        return o
    cil(0.08, 0.12, yf - 0.06, laton, 32)
    cil(0.44, 0.2, yf - 0.22, negro, 96, 0.02)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.415, minor_radius=0.04, major_segments=96, minor_segments=16,
                                     location=(0, yf - 0.32, 0.55), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object; o.data.materials.append(cromo)
    for f in o.data.polygons: f.use_smooth = True
    bpy.ops.mesh.primitive_circle_add(radius=0.39, vertices=96, fill_type="NGON", location=(0, yf - 0.325, 0.55), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object
    o.data.materials.append(dial)
    me = o.data
    uv = me.uv_layers.new(name="UV")
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (0.5 + v.x / 0.78, 0.5 + v.y / 0.78)
    # (sin cristal: el reflejo tapaba la escala)
    estudio((0, 0, 0.95), 9.5, 17, -22, focal=85, luz=0.9)

def perfiles():
    acero = mat("acero", (0.5, 0.52, 0.56), 1.0, 0.42)
    oscuro = mat("acero2", (0.34, 0.35, 0.38), 1.0, 0.38)
    # IPE 200 (cotas en dm: h=2, b=1, tw=0.056, tf=0.085) escalado ×1.6
    k = 1.6
    h, b, tw, tf = 2 * k, 1 * k, 0.056 * k * 1.4, 0.085 * k * 1.3
    ipe = [(-b/2, -h/2), (b/2, -h/2), (b/2, -h/2 + tf), (tw/2, -h/2 + tf), (tw/2, h/2 - tf), (b/2, h/2 - tf), (b/2, h/2), (-b/2, h/2), (-b/2, h/2 - tf), (-tw/2, h/2 - tf), (-tw/2, -h/2 + tf), (-b/2, -h/2 + tf)]
    from mathutils import Matrix
    def colocar(o, x, y, z):
        o.matrix_world = Matrix(((0, 0, 1, x), (1, 0, 0, y), (0, 1, 0, z), (0, 0, 0, 1)))
    colocar(perfil("ipe", [ipe], 6.5, acero, 0.01), 0, 0, 0)
    a, e = 1.1, 0.11
    colocar(perfil("L", [[(0, 0), (a, 0), (a, e), (e, e), (e, a), (0, a)]], 4.5, oscuro, 0.008), 1.6, -b / 2 - 1.3, -h / 2)
    t = 0.42
    colocar(perfil("tubo", [[(-t, -t), (t, -t), (t, t), (-t, t)], [(-t + .07, -t + .07), (t - .07, -t + .07), (t - .07, t - .07), (-t + .07, t - .07)]], 4.2, oscuro, 0.02), 2.2, b / 2 + 1.2, -h / 2 + t)
    estudio((0.6, -0.3, -0.3), 23, 24, -64, focal=85)

def llave():
    cromo = mat("cromo", (0.8, 0.81, 0.83), 1.0, 0.18)
    # mango
    perfil("mango", [[(-2.2, -0.42), (2.2, -0.32), (2.2, 0.32), (-2.2, 0.42)]], 0.26, cromo, 0.06)
    # cabeza de estrella (12 puntas)
    est = []
    for i in range(24):
        r = 0.62 if i % 2 == 0 else 0.55
        a = math.pi * i / 12
        est.append((-2.75 + r * math.cos(a), r * math.sin(a)))
    perfil("estrella", [circulo(0.92, 96, (-2.75, 0)), est], 0.3, cromo, 0.05)
    # boca fija (abierta) inclinada 15°
    cx, R, w, prof, inc = 2.85, 1.0, 0.62, 1.15, math.radians(15)
    a0 = math.asin(w / 2 / R)
    pts = []
    n = 60
    for i in range(n + 1):
        a = a0 + (2 * math.pi - 2 * a0) * i / n
        pts.append((R * math.cos(a), R * math.sin(a)))
    pts += [(R - prof, -w / 2), (R - prof, w / 2)]
    rot = [(cx + x * math.cos(inc) - y * math.sin(inc), x * math.sin(inc) + y * math.cos(inc)) for x, y in pts]
    perfil("boca", [rot], 0.24, cromo, 0.05)
    bpy.ops.object.empty_add(location=(0, 0, 0))
    raiz = bpy.context.active_object
    for o in bpy.data.objects:
        if o.type == "CURVE": o.parent = raiz
    raiz.rotation_euler = (math.radians(68), math.radians(8), math.radians(-24))
    estudio((0, 0, 0), 19, 22, -10, focal=85)

def soldadura():
    acero = mat("chapa", (0.3, 0.31, 0.33), 1.0, 0.55)
    cordon = mat("cordon", (0.5, 0.46, 0.4), 1.0, 0.32)
    oro = mat("tinte1", (0.85, 0.5, 0.12), 1.0, 0.35)
    azul = mat("tinte2", (0.12, 0.22, 0.7), 1.0, 0.3)
    for s_, x in ((1, 1.62), (-1, -1.62)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0))
        o = bpy.context.active_object; o.scale = (3.2, 5.0, 0.24); o.data.materials.append(acero)
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.02; bv.segments = 2
        for w, m, d in ((0.22, oro, 0.16), (0.2, azul, 0.42)):
            bpy.ops.mesh.primitive_plane_add(size=1, location=(s_ * (0.05 + d), 0, 0.1205))
            p = bpy.context.active_object; p.scale = (w, 4.6, 1); p.data.materials.append(m)
    k = 0
    y = -2.4
    while y < 2.45:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=24, ring_count=12, location=(0, y, 0.12))
        e = bpy.context.active_object
        e.scale = (0.36, 0.22, 0.13)
        e.rotation_euler = (math.radians(-28), 0, 0)
        e.data.materials.append(cordon)
        for f in e.data.polygons: f.use_smooth = True
        y += 0.13; k += 1
    bpy.ops.object.empty_add(location=(0, 0, 0))
    raiz = bpy.context.active_object
    for o in bpy.data.objects:
        if o.type == "MESH": o.parent = raiz
    raiz.rotation_euler = (0, 0, math.radians(-35))
    estudio((0, 0, 0), 17, 38, -30, focal=85)

if QUE == "llave":
    llave()
elif QUE == "soldadura":
    soldadura()
elif QUE == "perfiles":
    perfiles()
elif QUE == "engranaje":
    engranajes()
else:
    regulador()
sc.render.filepath = SALIDA
bpy.ops.render.render(write_still=True)
print("OK", SALIDA)
