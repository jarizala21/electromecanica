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
     tema         apartado dentro de la sección (las que comparten tema
                  se muestran juntas bajo ese título)
     icono        magnetotermico · diferencial · conmutada · cruzamiento ·
                  presostato · regulador · cremallera · engranaje · sinfin ·
                  guia · acoplamiento · cardan · embrague · biela · leva ·
                  polea · cadena · lampara · manometro · simulacion
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
      descripcion: "Guías, acoplamientos, embragues, transformadores de movimiento, engranajes y transmisiones.",
      tono: "verde",
      icono: "engranaje",
      // El campo "tema" agrupa las simulaciones en apartados dentro de la sección.
      simulaciones: [
        { archivo: "guia-redonda.html", id: "guia-redonda", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía redonda",
          descripcion: "Un casquillo desliza sobre un eje cilíndrico rectificado." },
        { archivo: "guia-plana.html", id: "guia-plana", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía plana",
          descripcion: "El carro apoya en superficies planas; las regletas evitan que se levante." },
        { archivo: "guia-prismatica.html", id: "guia-prismatica", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía prismática",
          descripcion: "Guía en V: el carro se centra al apoyar en los dos flancos." },
        { archivo: "guia-cola-de-milano.html", id: "guia-cola-de-milano", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía de cola de milano",
          descripcion: "Perfil trapecial con regleta cónica para ajustar el juego." },
        { archivo: "acoplamiento-oldham.html", id: "acoplamiento-oldham", tema: "Acoplamientos flexibles", icono: "acoplamiento",
          titulo: "Acoplamiento Oldham",
          descripcion: "Une ejes paralelos desplazados con un disco de lengüetas cruzadas." },
        { archivo: "acoplamiento-jaw.html", id: "acoplamiento-jaw", tema: "Acoplamientos flexibles", icono: "acoplamiento",
          titulo: "Acoplamiento de garras (Jaw)",
          descripcion: "Dos cubos con garras y una araña elástica entre ellas." },
        { archivo: "acoplamiento-fuelle.html", id: "acoplamiento-fuelle", tema: "Acoplamientos flexibles", icono: "acoplamiento",
          titulo: "Acoplamiento de fuelle",
          descripcion: "Flexible a flexión y rígido a torsión: sin holgura." },
        { archivo: "cardan.html", id: "cardan", tema: "Acoplamientos flexibles", icono: "cardan",
          titulo: "Junta cardán",
          descripcion: "Transmite el giro entre ejes que forman un ángulo." },
        { archivo: "embrague-dientes.html", id: "embrague-dientes", tema: "Embragues", icono: "embrague",
          titulo: "Embrague de dientes",
          descripcion: "Dientes frontales que encajan para unir dos ejes." },
        { archivo: "embrague-disco.html", id: "embrague-disco", tema: "Embragues", icono: "embrague",
          titulo: "Embrague de disco",
          descripcion: "El disco transmite el giro por rozamiento entre volante y plato." },
        { archivo: "biela-manivela.html", id: "biela-manivela", tema: "Transformadores de movimiento", icono: "biela",
          titulo: "Biela-manivela (cigüeñal)",
          descripcion: "Convierte el giro en vaivén del pistón, y al revés." },
        { archivo: "pinon-cremallera.html", id: "pinon-cremallera", tema: "Transformadores de movimiento", icono: "cremallera",
          titulo: "Piñón y cremallera",
          descripcion: "El giro del piñón se convierte en desplazamiento rectilíneo de la cremallera." },
        { archivo: "levas.html", id: "levas", tema: "Transformadores de movimiento", icono: "leva",
          titulo: "Levas: tipos",
          descripcion: "Cuatro levas con su seguidor y la gráfica de su movimiento." },
        { archivo: "engranajes-rectos.html", id: "engranajes-rectos", tema: "Engranajes", icono: "engranaje",
          titulo: "Dientes rectos",
          descripcion: "Ejes paralelos; giran en sentidos contrarios. Con representación normalizada." },
        { archivo: "engranajes-helicoidales.html", id: "engranajes-helicoidales", tema: "Engranajes", icono: "engranaje",
          titulo: "Dientes helicoidales",
          descripcion: "Dientes inclinados: más silenciosos. Con representación normalizada." },
        { archivo: "engranajes-conicos.html", id: "engranajes-conicos", tema: "Engranajes", icono: "engranaje",
          titulo: "Cónicos",
          descripcion: "Ejes que se cortan, normalmente a 90°. Con representación normalizada." },
        { archivo: "tornillo-sin-fin.html", id: "tornillo-sin-fin", tema: "Engranajes", icono: "sinfin",
          titulo: "Tornillo sin fin y corona",
          descripcion: "Gran reducción entre ejes que se cruzan. Con representación normalizada." },
        { archivo: "dentado-interior.html", id: "dentado-interior", tema: "Engranajes", icono: "engranaje",
          titulo: "Dentado interior",
          descripcion: "El piñón engrana dentro de la corona. Con representación normalizada." },
        { archivo: "pinon-cremallera.html", id: "engranaje-pinon-cremallera", tema: "Engranajes", icono: "cremallera",
          titulo: "Piñón y cremallera",
          descripcion: "Animación y representación normalizada." },
        { archivo: "formas-poleas.html", id: "formas-poleas", tema: "Poleas, correas y cadenas", icono: "polea",
          titulo: "Poleas: formas",
          descripcion: "La forma de la garganta según la correa." },
        { archivo: "tipos-correas.html", id: "tipos-correas", tema: "Poleas, correas y cadenas", icono: "polea",
          titulo: "Correas: tipos",
          descripcion: "Plana, trapezoidal, poli-V, dentada y redonda." },
        { archivo: "tipos-cadenas.html", id: "tipos-cadenas", tema: "Poleas, correas y cadenas", icono: "cadena",
          titulo: "Cadenas: tipos",
          descripcion: "Partes de la cadena de rodillos y tipos de cadena." }
      ]
    }
  ]
};
