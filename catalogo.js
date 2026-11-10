/* =====================================================================
   CATÁLOGO DE LA APP «ELECTROMECÁNICA»

   No hace falta tocar este archivo para añadir simulaciones: cualquier
   .html que subas a simulaciones/<carpeta>/ aparece solo en la app, con
   el título que tenga el propio archivo (su etiqueta <title>).

   Este catálogo sirve para dejarlas más bonitas:
     · nombre, nombre en euskera, frase, foto e icono de cada área
     · título, tema, descripción e icono de cada simulación
     · el orden (también el de los botones Anterior / Siguiente)

   Campos de un área (sección)
     carpeta      nombre de la carpeta dentro de simulaciones/ (sin tildes
                  ni espacios). También es su enlace directo: #carpeta
     nombre       lo que se ve en la app
     eu           nombre y frase en euskera: { nombre: "…", descripcion: "…" }
     temas_eu     traducción de los apartados: { "Engranajes": "Engranajeak", … }
     descripcion  una frase corta
     imagen       foto del botón del área, con fondo transparente
                  (por ejemplo imagenes/area-electrica.webp)
     icono        se usa si no hay foto: lampara · manometro · engranaje · simulacion

   Campos de una simulación
     archivo      nombre del .html dentro de la carpeta de la sección
     id           enlace directo (#id). Si no se pone, se usa el nombre
                  del archivo
     titulo, tema, descripcion
     eu           título y descripción en euskera: { titulo: "…", descripcion: "…" }
                  (lo que no esté traducido sale en castellano)
     tema         apartado dentro de la sección (las que comparten tema
                  se muestran juntas bajo ese título)
     icono        magnetotermico · diferencial · conmutada · cruzamiento ·
                  presostato · regulador · cremallera · engranaje · sinfin ·
                  guia · acoplamiento · cardan · embrague · biela · leva ·
                  polea · cadena · lampara · manometro · simulacion
     miniatura    (opcional) imagen redonda de la lista. Si no se pone, se usa
                  miniaturas/<nombre-del-archivo>.webp dentro de la carpeta,
                  y si no existe, el icono.
   ===================================================================== */
self.CATALOGO = {
  secciones: [
    {
      carpeta: "electrica",
      nombre: "Electricidad",
      descripcion: "Elementos de seguridad, control y actuadores eléctricos.",
      imagen: "imagenes/area-electrica.webp",
      icono: "lampara",
      eu: { nombre: "Elektrizitatea", descripcion: "Segurtasun- eta kontrol-elementuak eta eragingailuak." },
      temas_eu: {
        "Instalaciones": "Instalazioak",
        "Protecciones": "Babesak",
        "Mando y protección de motores": "Motorren agintea eta babesa"
      },
      simulaciones: [
        { archivo: "guardamotor.html", id: "guardamotor", tema: "Mando y protección de motores", icono: "magnetotermico",
          titulo: "Guardamotor",
          descripcion: "Protege el motor contra sobrecargas y cortocircuitos. Simulador de disparo y símbolo.",
          eu: { titulo: "Disyuntorea (guardamotorra)", descripcion: "Motorra gainkargen eta zirkuitulaburren aurka babesten du. Jauzi-simulagailua eta sinboloa." } },
        { archivo: "contactor.html", id: "contactor", tema: "Mando y protección de motores", icono: "simulacion",
          titulo: "Contactor",
          descripcion: "Partes, tipos, símbolo y marcha-paro con autorretención.",
          eu: { titulo: "Kontaktorea", descripcion: "Atalak, motak, sinboloa eta martxa-geldialdia autoatxikimenduarekin." } },
        {
          archivo: "conmutada-2-bombillas.html",
          id: "conmutada",
          titulo: "Conmutada con 2 bombillas",
          tema: "Instalaciones",
          descripcion: "Dos conmutadores encienden las mismas bombillas desde dos puntos, como en un pasillo.",
          icono: "conmutada",
          eu: { titulo: "Konmutatua 2 bonbillarekin", descripcion: "Bi konmutadorek bonbilla berberak pizten dituzte bi lekutatik, korridore batean bezala." }
        },
        {
          archivo: "cruzamiento-2-bombillas.html",
          id: "cruzamiento",
          titulo: "Conmutada con cruzamiento",
          tema: "Instalaciones",
          descripcion: "Un cruzamiento entre los dos conmutadores permite mandar las bombillas desde tres puntos.",
          icono: "cruzamiento",
          eu: { titulo: "Konmutatua gurutzagailuarekin", descripcion: "Bi konmutadoreen arteko gurutzagailu bati esker, bonbillak hiru lekutatik agin daitezke." }
        },
        {
          archivo: "magnetotermico.html",
          id: "magnetotermico",
          titulo: "Magnetotérmico por dentro",
          tema: "Protecciones",
          descripcion: "Bimetal y bobina en acción: sobrecarga, cortocircuito y curvas de disparo B, C y D.",
          icono: "magnetotermico",
          eu: { titulo: "Magnetotermikoa barrutik", descripcion: "Bimetala eta bobina lanean: gainkarga, zirkuitulaburra eta B, C eta D etete-kurbak." }
        },
        {
          archivo: "diferencial.html",
          id: "diferencial",
          titulo: "Diferencial por dentro",
          tema: "Protecciones",
          descripcion: "Toroide, relé y botón de test. Cómo detecta una fuga a tierra y por qué 30 mA.",
          icono: "diferencial",
          eu: { titulo: "Diferentziala barrutik", descripcion: "Toroidea, errelea eta proba-botoia. Lurrerako ihes bat nola hautematen duen eta zergatik 30 mA." }
        }
      ]
    },
    {
      carpeta: "neumatica",
      nombre: "Neumática",
      descripcion: "Elementos de regulación y mando del aire comprimido.",
      imagen: "imagenes/area-neumatica.webp",
      icono: "manometro",
      eu: { nombre: "Pneumatika", descripcion: "Aire konprimituaren erregulazio- eta agintze-elementuak." },
      temas_eu: {
        "Preparación del aire": "Airearen prestaketa",
        "Mando por presión": "Presio bidezko agintea"
      },
      simulaciones: [
        {
          archivo: "regulador_presion.html",
          id: "regulador",
          titulo: "Regulador de presión",
          tema: "Preparación del aire",
          descripcion: "El tornillo comprime el muelle y fija la presión de salida; el diafragma la mantiene aunque cambie el consumo.",
          icono: "regulador",
          eu: { titulo: "Presio-erregulagailua", descripcion: "Torlojuak malgukia estutzen du eta irteerako presioa finkatzen du; diafragmak mantendu egiten du, kontsumoa aldatu arren." }
        },
        {
          archivo: "presostato_interactivo.html",
          id: "presostato",
          titulo: "Presostato",
          tema: "Mando por presión",
          descripcion: "Al llegar a la presión de corte, la membrana conmuta el contacto NA/NC y se enciende la bombilla.",
          icono: "presostato",
          eu: { titulo: "Presostatoa", descripcion: "Ebaketa-presiora iristean, mintzak NA/NC kontaktua kommutatzen du eta bonbilla pizten da." }
        }
      ]
    },
    {
      carpeta: "mecanica",
      nombre: "Mecánica",
      descripcion: "Elementos de guiado, unión y transmisión del movimiento.",
      imagen: "imagenes/area-mecanica.webp",
      icono: "engranaje",
      eu: { nombre: "Mekanika", descripcion: "Gidatze-, lotura- eta transmisio-elementuak." },
      temas_eu: {
        "Elementos de unión": "Lotura-elementuak",
        "Guías de deslizamiento": "Irristatze-gidak",
        "Acoplamientos flexibles": "Akoplamendu malguak",
        "Embragues": "Enbrageak",
        "Transformadores de movimiento": "Mugimendu-eraldatzaileak",
        "Engranajes": "Engranajeak",
        "Poleas, correas y cadenas": "Poleak, uhalak eta kateak"
      },
      // El campo "tema" agrupa las simulaciones en apartados dentro de la sección.
      simulaciones: [
        { archivo: "tornillos.html", id: "tornillos", tema: "Elementos de unión", icono: "simulacion",
          titulo: "Tornillos",
          descripcion: "Partes, tipos de cabeza y designación: M10 × 40 – 8.8.",
          eu: { titulo: "Torlojuak", descripcion: "Atalak, buru motak eta izendapena: M10 × 40 – 8.8." } },
        { archivo: "tuercas.html", id: "tuercas", tema: "Elementos de unión", icono: "simulacion",
          titulo: "Tuercas",
          descripcion: "Tipos, cómo evitar que se aflojen y avance por vuelta.",
          eu: { titulo: "Azkoinak", descripcion: "Motak, askatu ez daitezen zer egin eta biraka aurrerapena." } },
        { archivo: "roscachapas.html", id: "roscachapas", tema: "Elementos de unión", icono: "simulacion",
          titulo: "Tornillos roscachapa",
          descripcion: "Hacen su propia rosca en chapa fina. Montaje paso a paso.",
          eu: { titulo: "Txapa-torlojuak (roskatxapak)", descripcion: "Txapa mehean beren haria egiten dute. Muntaketa urratsez urrats." } },
        { archivo: "remaches.html", id: "remaches", tema: "Elementos de unión", icono: "simulacion",
          titulo: "Remaches",
          descripcion: "Macizos y pop: cómo se colocan y cómo se eligen.",
          eu: { titulo: "Errematxeak", descripcion: "Trinkoak eta pop: nola jartzen diren eta nola aukeratzen diren." } },
        { archivo: "guia-redonda.html", id: "guia-redonda", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía redonda",
          descripcion: "Un casquillo desliza sobre un eje cilíndrico rectificado.",
          eu: { titulo: "Gida biribila", descripcion: "Kasketa bat ardatz zilindriko artezu baten gainean irristatzen da." } },
        { archivo: "guia-plana.html", id: "guia-plana", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía plana",
          descripcion: "El carro apoya en superficies planas; las regletas evitan que se levante.",
          eu: { titulo: "Gida laua", descripcion: "Gurdia gainazal lauen gainean bermatzen da; erregletek altxatzea eragozten dute." } },
        { archivo: "guia-prismatica.html", id: "guia-prismatica", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía prismática",
          descripcion: "Guía en V: el carro se centra al apoyar en los dos flancos.",
          eu: { titulo: "Gida prismatikoa", descripcion: "V formako gida: gurdia zentratu egiten da bi hegaletan bermatzean." } },
        { archivo: "guia-cola-de-milano.html", id: "guia-cola-de-milano", tema: "Guías de deslizamiento", icono: "guia",
          titulo: "Guía de cola de milano",
          descripcion: "Perfil trapecial con regleta cónica para ajustar el juego.",
          eu: { titulo: "Enara-buztan gida", descripcion: "Profil trapezoidala, jokoa doitzeko erregleta konikoarekin." } },
        { archivo: "acoplamiento-oldham.html", id: "acoplamiento-oldham", tema: "Acoplamientos flexibles", icono: "acoplamiento",
          titulo: "Acoplamiento Oldham",
          descripcion: "Une ejes paralelos desplazados con un disco de lengüetas cruzadas.",
          eu: { titulo: "Oldham akoplamendua", descripcion: "Lerrokatuta ez dauden ardatz paraleloak lotzen ditu, mihi gurutzatuko disko baten bidez." } },
        { archivo: "acoplamiento-jaw.html", id: "acoplamiento-jaw", tema: "Acoplamientos flexibles", icono: "acoplamiento",
          titulo: "Acoplamiento de garras (Jaw)",
          descripcion: "Dos cubos con garras y una araña elástica entre ellas.",
          eu: { titulo: "Atzapar-akoplamendua (Jaw)", descripcion: "Atzaparrak dituzten bi naba eta haien artean armiarma elastiko bat." } },
        { archivo: "acoplamiento-fuelle.html", id: "acoplamiento-fuelle", tema: "Acoplamientos flexibles", icono: "acoplamiento",
          titulo: "Acoplamiento de fuelle",
          descripcion: "Flexible a flexión y rígido a torsión: sin holgura.",
          eu: { titulo: "Hauspo-akoplamendua", descripcion: "Malgua flexioan eta zurruna bihurduran: jokorik gabe." } },
        { archivo: "cardan.html", id: "cardan", tema: "Acoplamientos flexibles", icono: "cardan",
          titulo: "Junta cardán",
          descripcion: "Transmite el giro entre ejes que forman un ángulo.",
          eu: { titulo: "Kardan-juntura", descripcion: "Angelu bat osatzen duten ardatzen artean transmititzen du biraketa." } },
        { archivo: "embrague-dientes.html", id: "embrague-dientes", tema: "Embragues", icono: "embrague",
          titulo: "Embrague de dientes",
          descripcion: "Dientes frontales que encajan para unir dos ejes.",
          eu: { titulo: "Hortz-enbragea", descripcion: "Aurrealdeko hortzak elkarri txertatzen zaizkio bi ardatz lotzeko." } },
        { archivo: "embrague-disco.html", id: "embrague-disco", tema: "Embragues", icono: "embrague",
          titulo: "Embrague de disco",
          descripcion: "El disco transmite el giro por rozamiento entre volante y plato.",
          eu: { titulo: "Disko-enbragea", descripcion: "Diskoak marruskaduraz transmititzen du biraketa bolantearen eta platerraren artean." } },
        { archivo: "biela-manivela.html", id: "biela-manivela", tema: "Transformadores de movimiento", icono: "biela",
          titulo: "Biela-manivela (cigüeñal)",
          descripcion: "Convierte el giro en vaivén del pistón, y al revés.",
          eu: { titulo: "Biela-birabarkia (birabarki-ardatza)", descripcion: "Biraketa pistoiaren joan-etorri bihurtzen du, eta alderantziz." } },
        { archivo: "pinon-cremallera.html", id: "pinon-cremallera", tema: "Transformadores de movimiento", icono: "cremallera",
          titulo: "Piñón y cremallera",
          descripcion: "El giro del piñón se convierte en desplazamiento rectilíneo de la cremallera.",
          eu: { titulo: "Pinoia eta kremailera", descripcion: "Pinoiaren biraketa kremaileraren desplazamendu zuzen bihurtzen da." } },
        { archivo: "levas.html", id: "levas", tema: "Transformadores de movimiento", icono: "leva",
          titulo: "Levas: tipos",
          descripcion: "Cuatro levas con su seguidor y la gráfica de su movimiento.",
          eu: { titulo: "Espekak: motak", descripcion: "Lau espeka, bakoitza bere jarraitzailearekin eta mugimenduaren grafikoarekin." } },
        { archivo: "engranajes-rectos.html", id: "engranajes-rectos", tema: "Engranajes", icono: "engranaje",
          titulo: "Dientes rectos",
          descripcion: "Ejes paralelos; giran en sentidos contrarios. Con representación normalizada.",
          eu: { titulo: "Hortz zuzenak", descripcion: "Ardatz paraleloak; aurkako noranzkoan biratzen dute. Irudikapen normalizatuarekin." } },
        { archivo: "engranajes-helicoidales.html", id: "engranajes-helicoidales", tema: "Engranajes", icono: "engranaje",
          titulo: "Dientes helicoidales",
          descripcion: "Dientes inclinados: más silenciosos. Con representación normalizada.",
          eu: { titulo: "Hortz helikoidalak", descripcion: "Hortz inklinatuak: isilagoak. Irudikapen normalizatuarekin." } },
        { archivo: "engranajes-conicos.html", id: "engranajes-conicos", tema: "Engranajes", icono: "engranaje",
          titulo: "Cónicos",
          descripcion: "Ejes que se cortan, normalmente a 90°. Con representación normalizada.",
          eu: { titulo: "Konikoak", descripcion: "Elkar ebakitzen duten ardatzak, normalean 90°-an. Irudikapen normalizatuarekin." } },
        { archivo: "tornillo-sin-fin.html", id: "tornillo-sin-fin", tema: "Engranajes", icono: "sinfin",
          titulo: "Tornillo sin fin y corona",
          descripcion: "Gran reducción entre ejes que se cruzan. Con representación normalizada.",
          eu: { titulo: "Torloju amaigabea eta koroa", descripcion: "Murrizketa handia gurutzatzen diren ardatzen artean. Irudikapen normalizatuarekin." } },
        { archivo: "dentado-interior.html", id: "dentado-interior", tema: "Engranajes", icono: "engranaje",
          titulo: "Dentado interior",
          descripcion: "El piñón engrana dentro de la corona. Con representación normalizada.",
          eu: { titulo: "Barne-hortzeria", descripcion: "Pinoia koroaren barruan engranatzen da. Irudikapen normalizatuarekin." } },
        { archivo: "pinon-cremallera.html", id: "engranaje-pinon-cremallera", tema: "Engranajes", icono: "cremallera",
          titulo: "Piñón y cremallera",
          descripcion: "Animación y representación normalizada.",
          eu: { titulo: "Pinoia eta kremailera", descripcion: "Animazioa eta irudikapen normalizatua." } },
        { archivo: "formas-poleas.html", id: "formas-poleas", tema: "Poleas, correas y cadenas", icono: "polea",
          titulo: "Poleas: formas",
          descripcion: "La forma de la garganta según la correa.",
          eu: { titulo: "Poleak: formak", descripcion: "Zirrikituaren forma uhalaren araberakoa da." } },
        { archivo: "tipos-correas.html", id: "tipos-correas", tema: "Poleas, correas y cadenas", icono: "polea",
          titulo: "Correas: tipos",
          descripcion: "Plana, trapezoidal, poli-V, dentada y redonda.",
          eu: { titulo: "Uhalak: motak", descripcion: "Laua, trapezoidala, poli-V, horzduna eta biribila." } },
        { archivo: "tipos-cadenas.html", id: "tipos-cadenas", tema: "Poleas, correas y cadenas", icono: "cadena",
          titulo: "Cadenas: tipos",
          descripcion: "Partes de la cadena de rodillos y tipos de cadena.",
          eu: { titulo: "Kateak: motak", descripcion: "Arrabol-katearen atalak eta kate motak." } }
      ]
    },
    {
      carpeta: "dibujo",
      nombre: "Dibujo técnico",
      descripcion: "Hojas de proceso, acotación y perfiles normalizados.",
      imagen: "imagenes/area-dibujo.webp",
      icono: "simulacion",
      eu: { nombre: "Marrazketa teknikoa", descripcion: "Prozesu-orriak, akotazioa eta profil normalizatuak." },
      temas_eu: { "Fabricación": "Fabrikazioa", "Dibujo técnico": "Marrazketa teknikoa" },
      simulaciones: [
        { archivo: "hojas-proceso.html", id: "hojas-proceso", tema: "Fabricación", icono: "simulacion",
          titulo: "Hojas de proceso",
          descripcion: "Qué son, sus partes y un ejercicio para ordenar las operaciones.",
          eu: { titulo: "Prozesu-orriak", descripcion: "Zer diren, haien atalak eta eragiketak ordenatzeko ariketa bat." } },
        { archivo: "acotacion.html", id: "acotacion", tema: "Dibujo técnico", icono: "simulacion",
          titulo: "Acotación",
          descripcion: "Elementos de una cota, normas, tipos y símbolos.",
          eu: { titulo: "Akotazioa", descripcion: "Kota baten elementuak, arauak, motak eta ikurrak." } },
        { archivo: "perfiles.html", id: "perfiles", tema: "Dibujo técnico", icono: "simulacion",
          titulo: "Perfiles metálicos normalizados",
          descripcion: "IPE, HEB, UPN, L, tubos… medidas, designación y peso.",
          eu: { titulo: "Metalezko profil normalizatuak", descripcion: "IPE, HEB, UPN, L, hodiak… neurriak, izendapena eta pisua." } }
      ]
    }
  ]
};
