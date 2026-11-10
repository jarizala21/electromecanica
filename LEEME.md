# Electromecánica

App con simulaciones interactivas de electricidad y neumática para clase. Funciona en el móvil, la tablet y el PC; se puede instalar como app y, una vez abierta, funciona sin internet.

## Abrirla e instalarla

- **Android (Chrome) y PC (Chrome o Edge):** abre la dirección de la app y pulsa **Instalar app**.
- **iPhone o iPad (Safari):** pulsa *Compartir* y elige *Añadir a pantalla de inicio*.

Cada sección y cada simulación tiene su enlace directo: añade `#electrica`, `#neumatica`, `#magnetotermico`… al final de la dirección. Sirve para ponerlas en Moodle.

## Añadir una simulación

1. En GitHub, entra en la carpeta de su sección dentro de `simulaciones/` (por ejemplo `simulaciones/electrica`).
2. Pulsa **Add file → Upload files**, arrastra el `.html` y pulsa **Commit changes**.
3. En uno o dos minutos aparece en la app, con el título que tenga el archivo.

Las apps ya instaladas se actualizan solas la próxima vez que se abren con internet.

Para darle un título, una descripción o un icono más cuidados, o cambiar el orden, edita `catalogo.js` (las instrucciones están dentro).

## Añadir una sección

Crea una carpeta nueva dentro de `simulaciones/` con al menos un `.html` (en **Upload files** puedes arrastrar la carpeta entera). Usa un nombre corto, en minúsculas, sin tildes ni espacios: `mecanica`, `automatizacion`… Aparece sola como sección nueva; para ponerle nombre con tildes, color e icono, añádela en `catalogo.js`.

## Qué es cada archivo

| Archivo | Para qué sirve |
|---|---|
| `simulaciones/` | Las simulaciones, una carpeta por sección |
| `catalogo.js` | Nombres, descripciones, iconos y orden |
| `index.html`, `estilos.css`, `app.js` | La app |
| `sw.js` | Funcionamiento sin internet |
| `manifest.webmanifest`, `iconos/` | Nombre e icono al instalarla (los PNG se generan solos a partir de los SVG) |
| `herramientas/preparar.mjs`, `.github/workflows/publicar.yml` | Publicación automática en GitHub Pages |
