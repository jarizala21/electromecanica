"""Genera todos los GIF de Mecánica en simulaciones/mecanica/.
Necesita Pillow y las fuentes Barlow de @fontsource (variable FONTSOURCE) y DejaVu.
Uso: python3 herramientas/gif/todos.py [nombre ...]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guias, acoplamientos, embragues, transformadores, engranajes, transmision

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "simulaciones", "mecanica")

TAREAS = {}
for n in guias.GUIAS:
    TAREAS[n] = (lambda n=n: lambda r: guias.hacer(n, r))()
for mod in (acoplamientos, embragues, transformadores, engranajes, transmision):
    TAREAS.update(mod.TODOS)

if __name__ == "__main__":
    os.makedirs(DEST, exist_ok=True)
    nombres = sys.argv[1:] or list(TAREAS) + ["pinon-cremallera-normalizada"]
    for n in nombres:
        if n == "pinon-cremallera-normalizada":
            t = engranajes.pinon_cremallera_norma(os.path.join(DEST, n + ".png"))
        else:
            t = TAREAS[n](os.path.join(DEST, n + ".gif"))
        print(f"{n:28s} {t / 1024:7.0f} KB")
