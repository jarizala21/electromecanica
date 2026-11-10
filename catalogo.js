/* =====================================================================
   CATÁLOGO DE LA APP «ELECTROMECÁNICA»

   No hace falta tocar este archivo para añadir simulaciones: cualquier
   .html que subas a simulaciones/<carpeta>/ aparece solo en la app, con
   el título que tenga el propio archivo (su etiqueta <title>).

   Este catálogo sirve para dejarlas más bonitas:
     · nombre, descripción, color e icono de cada sección
     · título, tema, descripción e icono de cada simulación
     · el orden (también el de los botones Anterior / Siguiente)

   Campos de una sección
     carpeta      nombre de la carpeta dentro de simulaciones/ (sin tildes
                  ni espacios). También es su enlace directo: #carpeta
     nombre       lo que se ve en la app
     descripcion  una frase
     tono         cobre · azul · verde · violeta · gris
     icono        lampara · manometro · engranaje · simulacion

   Campos de una simulación
     archivo      nombre del .html dentro de la carpeta de la sección
     id           enlace directo (#id). Si no se pone, se usa el nombre
                  del archivo
     titulo, tema, descripcion
     icono        magnetotermico · diferencial · conmutada · cruzamiento ·
                  presostato · regulador · cremallera · lampara ·
                  manometro · engranaje · simulacion
   ===================================================================== */
self.CATALOGO = {
  secciones: [
    {
      carpeta: "electrica",
      nombre: "Eléctrica",
      descripcion: "Instalaciones de vivienda y protecciones del cuadro eléctrico.",
      tono: "cobre",
      icono: "lampara",
      simulaciones: [
        {
          archivo: "conmutada-2-bombillas.html",
          id: "conmutada",
          titulo: "Conmutada con 2 bombillas",
          tema: "Instalaciones",
          descripcion: "Dos conmutadores encienden las mismas bombillas desde dos puntos, como en un pasillo.",
          icono: "conmutada"
        },
        {
          archivo: "cruzamiento-2-bombillas.html",
          id: "cruzamiento",
          titulo: "Conmutada con cruzamiento",
          tema: "Instalaciones",
          descripcion: "Un cruzamiento entre los dos conmutadores permite mandar las bombillas desde tres puntos.",
          icono: "cruzamiento"
        },
        {
          archivo: "magnetotermico.html",
          id: "magnetotermico",
          titulo: "Magnetotérmico por dentro",
          tema: "Protecciones",
          descripcion: "Bimetal y bobina en acción: sobrecarga, cortocircuito y curvas de disparo B, C y D.",
          icono: "magnetotermico"
        },
        {
          archivo: "diferencial.html",
          id: "diferencial",
          titulo: "Diferencial por dentro",
          tema: "Protecciones",
          descripcion: "Toroide, relé y botón de test. Cómo detecta una fuga a tierra y por qué 30 mA.",
          icono: "diferencial"
        }
      ]
    },
    {
      carpeta: "neumatica",
      nombre: "Neumática",
      descripcion: "Preparación del aire comprimido y mando por presión.",
      tono: "azul",
      icono: "manometro",
      simulaciones: [
        {
          archivo: "regulador_presion.html",
          id: "regulador",
          titulo: "Regulador de presión",
          tema: "Preparación del aire",
          descripcion: "El tornillo comprime el muelle y fija la presión de salida; el diafragma la mantiene aunque cambie el consumo.",
          icono: "regulador"
        },
        {
          archivo: "presostato_interactivo.html",
          id: "presostato",
          titulo: "Presostato",
          tema: "Mando por presión",
          descripcion: "Al llegar a la presión de corte, la membrana conmuta el contacto NA/NC y se enciende la bombilla.",
          icono: "presostato"
        }
      ]
    },
    {
      carpeta: "mecanica",
      nombre: "Mecánica",
      descripcion: "Mecanismos que transmiten y transforman el movimiento.",
      tono: "verde",
      icono: "engranaje",
      simulaciones: [
        {
          archivo: "pinon-cremallera.html",
          id: "pinon-cremallera",
          titulo: "Piñón y cremallera",
          tema: "Transformación del movimiento",
          descripcion: "El giro del piñón se convierte en desplazamiento rectilíneo de la cremallera, y al revés.",
          icono: "cremallera"
        }
      ]
    }
  ]
};
