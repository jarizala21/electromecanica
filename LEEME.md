# Electromecánica

App del departamento de Mantenimiento Electromecánico de La Salle Berrozpe con simulaciones y animaciones de electricidad, neumática y mecánica para entender la teoría del ciclo. Funciona en el móvil, la tablet y el PC; se puede instalar como app y, una vez abierta, funciona sin internet.

Licencia: Creative Commons BY-NC-SA 4.0.

## Cómo se usa

Portada de bienvenida (euskera y castellano) → **Sartu · Entrar** → menú de áreas (cabe en una pantalla) → lista de simulaciones del área → simulación.

- **Android (Chrome) y PC (Chrome o Edge):** en el menú de áreas, pulsa el botón naranja de descarga para instalarla.
- **iPhone o iPad (Safari):** pulsa *Compartir* y elige *Añadir a pantalla de inicio*.

Enlaces directos para Moodle: añade al final de la dirección `#areas` (menú de áreas), `#electrica`, `#neumatica`, `#mecanica` (cada área) o el de una simulación (`#magnetotermico`, `#engranajes-rectos`…).

## Añadir una simulación

1. En GitHub, entra en la carpeta de su área dentro de `simulaciones/` (por ejemplo `simulaciones/electrica`).
2. Pulsa **Add file → Upload files**, arrastra el `.html` y pulsa **Commit changes**.
3. En uno o dos minutos aparece en la app, con el título que tenga el archivo.

Las apps ya instaladas se actualizan solas la próxima vez que se abren con internet.

Para darle un título, una descripción o un icono más cuidados, cambiar el orden o agruparla en un apartado (campo `tema`), edita `catalogo.js` (las instrucciones están dentro).

La imagen redonda de la lista sale de `simulaciones/<área>/miniaturas/<archivo>.webp`. Si no existe, se ve el icono. Para crearlas: `python3 herramientas/imagenes/miniaturas.py`.

## Fichas bilingües

Las fichas didácticas (guardamotor, contactor, hojas de proceso, acotación, perfiles, tornillos, tuercas, roscachapas y remaches) usan `simulaciones/comun/ficha.css` y `ficha.js`: pestañas, partes que se resaltan al tocarlas y textos en euskera y castellano (`class="es"` / `class="eu"`). Se ven en el idioma elegido en la portada y tienen un botón EU · ES arriba. Una ficha puede llevar dentro un simulador ya hecho (`<iframe class="sim-embebida">`); ese simulador se marca en `catalogo.js` con `oculta: true` para que no salga repetido en la lista.

La app y las fichas siguen el modo claro u oscuro del móvil o del ordenador. Los dibujos van siempre sobre fondo claro.

## Añadir un área

Crea una carpeta nueva dentro de `simulaciones/` con al menos un `.html` (en **Upload files** puedes arrastrar la carpeta entera). Usa un nombre corto, en minúsculas, sin tildes ni espacios: `automatizacion`, `hidraulica`… Aparece sola como área nueva; para ponerle nombre con tildes, nombre en euskera, frase y foto, añádela en `catalogo.js`.

La foto del botón de un área es una imagen con fondo transparente en `imagenes/` (WebP o PNG). Una foto hecha sobre fondo blanco se puede recortar con `python3 herramientas/imagenes/recortar_foto.py foto.jpg imagenes/area-xxx.webp`.

## Qué es cada archivo

| Archivo | Para qué sirve |
|---|---|
| `simulaciones/` | Las simulaciones, una carpeta por área (con sus miniaturas); `comun/` tiene el estilo de las fichas |
| `catalogo.js` | Nombres (también en euskera), frases, fotos, iconos y orden |
| `index.html`, `estilos.css`, `app.js` | La app |
| `imagenes/` | Logo de La Salle, fotos de las áreas y distintivo de la licencia |
| `sw.js` | Funcionamiento sin internet |
| `manifest.webmanifest`, `iconos/` | Nombre e icono al instalarla (los PNG se generan solos a partir de los SVG) |
| `herramientas/preparar.mjs`, `.github/workflows/publicar.yml` | Publicación automática en GitHub Pages |
| `herramientas/gif/` | Scripts que dibujan los GIF de Mecánica (`python3 herramientas/gif/todos.py`) |
| `herramientas/paginas.py` | Genera las páginas de Mecánica a partir de sus textos |
| `herramientas/imagenes/` | Miniaturas, recorte de fotos y las imágenes 3D del regulador y el engranaje (Blender) |

## Avisos y peticiones de los alumnos

El botón con el bocadillo (en el menú de áreas, en la lista de cada área y en el
visor de cada ficha) abre un formulario anónimo: avisar de un error, proponer una
mejora, pedir un tema nuevo u otra cosa. Se rellena solo con la ficha en la que
estaba el alumno, el idioma, el dispositivo y la versión de la app.

Los avisos llegan por correo a través de Web3Forms (gratis):

1. Entra en https://web3forms.com, escribe el correo donde quieres recibirlos y
   te llegará una «Access Key».
2. Pégala en `catalogo.js`, en `AVISOS.clave`, y publica.

Mientras la clave esté vacía, el formulario funciona en **modo prueba**: no envía
nada y enseña el correo que se recibiría. Sin conexión, el aviso se guarda en el
móvil y se envía solo cuando vuelve internet.
