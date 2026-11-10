"""Miniaturas redondas de la lista de cada área.
Crea simulaciones/<carpeta>/miniaturas/<archivo>.webp para cada simulación:
  · si hay un GIF con el mismo nombre, recorta un fotograma;
  · si no, abre el HTML en Chromium y captura su dibujo principal (svg/canvas/img más grande).
Los recortes de cada una se ajustan en CAP y GIF (centro x, centro y y lado, en fracciones).
Uso (desde la raíz del repositorio): python3 herramientas/imagenes/miniaturas.py [carpeta/archivo ...]
Necesita Pillow y Playwright (pip install pillow playwright && playwright install chromium)."""
import os, sys, io
from PIL import Image, ImageSequence
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "simulaciones")
CAP = {  # simulaciones HTML: centro x, centro y, lado (fracciones del ancho de la captura)
    'electrica/conmutada-2-bombillas': (0.80, 0.50, 0.30),
    'electrica/cruzamiento-2-bombillas': (0.62, 0.40, 0.27),
    'electrica/diferencial': (0.42, 0.40, 0.62),
    'electrica/magnetotermico': (0.40, 0.42, 0.70),
    'neumatica/presostato_interactivo': (0.42, 0.40, 0.46),
    'neumatica/regulador_presion': (0.52, 0.40, 0.42),
    # fichas: (centro x, centro y, lado, pestaña que se captura)
    'electrica/guardamotor': (0.5, 0.5, 0.62, 'zer-da'),
    'electrica/contactor': (0.5, 0.42, 0.75, 'deskribapena'),
    'dibujo/hojas-proceso': (0.32, 0.36, 0.42, 'atalak'),
    'dibujo/acotacion': (0.42, 0.5, 0.56, 'zer-da'),
    'dibujo/perfiles': (0.53, 0.5, 0.95, 'motak'),
    'mecanica/tornillos': (0.35, 0.5, 0.5, 'atalak'),
    'mecanica/tuercas': (0.5, 0.45, 0.46, 'zer-da'),
    'mecanica/roscachapas': (0.3, 0.5, 0.36, 'ezaugarriak'),
    'neumatica/magnitudes-neumaticas': (0.5, 0.5, 0.85, 'presioa'),
    'neumatica/compresor': (0.42, 0.42, 0.75, 'zatiak'),
    'neumatica/secadores': (0.5, 0.42, 0.7, 'zatiak'),
    'neumatica/regulador': (0.5, 0.45, 0.85, 'zatiak'),
    'neumatica/lubricador': (0.5, 0.42, 0.85, 'zatiak'),
    'neumatica/tubos': (0.84, 0.5, 0.36, 'zatiak'),
    'neumatica/racores': (0.55, 0.5, 0.6, 'zatiak'),
    'electrica/magnitudes-electricas': (0.55, 0.5, 0.62, 'proba'),
    'electrica/cc-ca': (0.4, 0.5, 0.6, 'grafikoa'),
    'electrica/ficha-magnetotermico': (0.5, 0.42, 0.95, 'zatiak'),
    'electrica/ficha-diferencial': (0.5, 0.5, 0.95, 'zatiak'),
    'dibujo/planos': (0.5, 0.5, 0.95, 'bistak'),
    'dibujo/plegado': (0.42, 0.45, 0.62, 'erradioak'),
    'soldadura/preparacion': (0.5, 0.5, 0.5, 'ertzak'),
    'soldadura/parametros': (0.5, 0.3, 0.7, 'kalkulagailua'),
    'soldadura/defectos': (0.5, 0.42, 0.55, 'akatsak'),
    'herramientas/manuales': (0.5, 0.5, 0.62, 'motak'),
    'herramientas/neumaticas': (0.5, 0.5, 0.62, 'motak'),
    'herramientas/electricas': (0.5, 0.5, 0.62, 'motak'),
    'mecanica/remaches': (0.5, 0.5, 0.9, 'motak'),
}
GIF = {  # fotograma (fracción del total), centro x, centro y, lado (fracción del ancho)
    'acoplamiento-fuelle': (0.3, 0.36, 0.52, 0.32), 'acoplamiento-jaw': (0.3, 0.75, 0.6, 0.36),
    'acoplamiento-oldham': (0.3, 0.28, 0.56, 0.4), 'biela-manivela': (0.3, 0.32, 0.56, 0.42),
    'cardan': (0.3, 0.2, 0.56, 0.38), 'dentado-interior': (0.3, 0.27, 0.6, 0.4),
    'embrague-dientes': (0.3, 0.5, 0.6, 0.36), 'embrague-disco': (0.3, 0.4, 0.62, 0.42),
    'engranajes-conicos': (0.3, 0.18, 0.62, 0.36), 'engranajes-helicoidales': (0.3, 0.17, 0.5, 0.3),
    'engranajes-rectos': (0.3, 0.27, 0.62, 0.36), 'formas-poleas': (0.3, 0.24, 0.38, 0.32),
    'guia-cola-de-milano': (0.3, 0.2, 0.62, 0.36), 'guia-plana': (0.3, 0.2, 0.62, 0.36),
    'guia-prismatica': (0.3, 0.2, 0.62, 0.36), 'guia-redonda': (0.3, 0.22, 0.6, 0.36),
    'levas': (0.3, 0.14, 0.42, 0.2), 'pinon-cremallera': (0.3, 0.5, 0.42, 0.42),
    'tipos-cadenas': (0.3, 0.24, 0.42, 0.32), 'tipos-correas': (0.3, 0.86, 0.42, 0.3),
    'tornillo-sin-fin': (0.3, 0.18, 0.55, 0.42),
}

def recorte(im, cx, cy, s):
    w, h = im.size
    lado = min(s * w, h)
    x0 = min(max(cx * w - lado / 2, 0), w - lado); y0 = min(max(cy * h - lado / 2, 0), h - lado)
    return im.crop((int(x0), int(y0), int(x0 + lado), int(y0 + lado))).resize((192, 192), Image.LANCZOS)

def captura(pagina, ruta, pestana=None):
    pagina.goto("file://" + ruta + ("#" + pestana if pestana else ""))
    pagina.wait_for_timeout(1800)
    el = pagina.evaluate_handle("""() => {
      let best = null, area = 0;
      for (const el of document.querySelectorAll('svg, canvas, img')) {
        if (el.closest('button') || el.closest('[hidden]')) continue;
        const r = el.getBoundingClientRect(), a = r.width * r.height;
        if (a > area) { area = a; best = el; }
      }
      return best;
    }""").as_element()
    datos = el.screenshot() if el else pagina.screenshot()
    return Image.open(io.BytesIO(datos)).convert("RGB")

def main():
    pedidas = set(a.replace(".html", "") for a in sys.argv[1:])
    tareas = []
    for carpeta in sorted(os.listdir(SIM)):
        d = os.path.join(SIM, carpeta)
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"): continue
            clave = carpeta + "/" + f[:-5]
            if not pedidas or clave in pedidas: tareas.append((carpeta, f[:-5]))
    navegador = None
    for carpeta, nombre in tareas:
        gif = os.path.join(SIM, carpeta, nombre + ".gif")
        if os.path.exists(gif):
            t, cx, cy, s = GIF.get(nombre, (0.3, 0.5, 0.55, 0.5))
            fr = [x.convert("RGB") for x in ImageSequence.Iterator(Image.open(gif))]
            im = recorte(fr[int(t * len(fr))], cx, cy, s)
        else:
            if navegador is None:
                from playwright.sync_api import sync_playwright
                pw = sync_playwright().start()
                navegador = pw.chromium.launch()
                pagina = navegador.new_page(viewport={"width": 900, "height": 900})
            c = CAP.get(carpeta + "/" + nombre, (0.5, 0.5, 0.6))
            im = recorte(captura(pagina, os.path.join(SIM, carpeta, nombre + ".html"), c[3] if len(c) > 3 else None), c[0], c[1], c[2])
        os.makedirs(os.path.join(SIM, carpeta, "miniaturas"), exist_ok=True)
        im.save(os.path.join(SIM, carpeta, "miniaturas", nombre + ".webp"), quality=82, method=6)
        print("miniatura", carpeta + "/" + nombre)
    if navegador: navegador.close()

if __name__ == "__main__":
    main()
