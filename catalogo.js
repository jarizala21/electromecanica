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
     oculta       true = no sale en la lista (se abre solo por su enlace #id,
                  por ejemplo desde una ficha que la lleva dentro)
     miniatura    (opcional) imagen redonda de la lista. Si no se pone, se usa
                  miniaturas/<nombre-del-archivo>.webp dentro de la carpeta,
                  y si no existe, el icono.
   ===================================================================== */

/* ---------- Avisos y peticiones de los alumnos ----------
   El botón de avisos envía un correo al profesor con Web3Forms (gratis).
   Para activarlo: entra en https://web3forms.com, escribe el correo donde
   quieres recibir los avisos y te llegará una «Access Key». Pégala aquí.
   Mientras esté vacía, el formulario funciona en modo prueba (no envía nada). */
var AVISOS = {
  clave: "405c341a-8642-4ed6-9fab-38c4757e60f6"
};

self.CATALOGO = {
  secciones: [
    {
      carpeta: "electrica",
      nombre: "Electricidad",
      descripcion: "Magnitudes, protección, instalaciones, control y potencia.",
      imagen: "imagenes/area-electrica.webp",
      icono: "lampara",
      eu: { nombre: "Elektrizitatea", descripcion: "Magnitudeak, babesa, instalazioak, kontrola eta potentzia." },
      /* Submenú: al entrar en Electricidad salen estos apartados en una sola pantalla.
         Cada apartado reúne las simulaciones cuyo «tema» coincide. El orden de las
         simulaciones dentro de cada apartado es el de la lista de abajo. */
      submenu: [
        { id: "magnitudes", tema: "Magnitudes", icono: "rayo",
          descripcion: "Tensión, intensidad, potencia, consumo, energía y trifásica.",
          eu: { nombre: "Magnitudeak", descripcion: "Tentsioa, intentsitatea, potentzia, kontsumoa, energia eta trifasikoa." } },
        { id: "proteccion", tema: "Elementos de protección", icono: "diferencial",
          descripcion: "Diferencial, magnetotérmico, ICP y guardamotor.",
          eu: { nombre: "Babes-elementuak", descripcion: "Diferentziala, magnetotermikoa, PKE eta disyuntorea." } },
        { id: "instalaciones", tema: "Instalaciones eléctricas", icono: "conmutada",
          descripcion: "Interruptor, conmutada, cruzamiento y enchufe.",
          eu: { nombre: "Instalazio elektrikoak", descripcion: "Etengailua, konmutatua, gurutzagailua eta entxufea." } },
        { id: "control", tema: "Elementos de control", icono: "pulsador",
          descripcion: "Pulsador, contactor, piloto luminoso y bornero.",
          eu: { nombre: "Kontrol-elementuak", descripcion: "Sakagailua, kontaktorea, seinale-argia eta borne-regleta." } },
        { id: "potencia", tema: "Elementos de potencia", icono: "motor",
          descripcion: "Motores trifásicos y su placa de características.",
          eu: { nombre: "Potentzia-elementuak", descripcion: "Motor trifasikoak eta haien ezaugarri-plaka." } }
      ],
      simulaciones: [
        /* ---------- Magnitudes ---------- */
        { archivo: "tension.html", id: "tension", tema: "Magnitudes", icono: "rayo",
          titulo: "Tensión",
          descripcion: "Qué es el voltio, cómo se mide con el voltímetro y valores típicos.",
          eu: { titulo: "Tentsioa", descripcion: "Zer den boltioa, nola neurtzen den boltmetroarekin eta balio ohikoak." } },
        { archivo: "intensidad.html", id: "intensidad", tema: "Magnitudes", icono: "rayo",
          titulo: "Intensidad",
          descripcion: "La corriente eléctrica, el amperio y cómo se mide en serie.",
          eu: { titulo: "Intentsitatea", descripcion: "Korronte elektrikoa, amperea eta nola neurtzen den seriean." } },
        { archivo: "potencia.html", id: "potencia", tema: "Magnitudes", icono: "rayo",
          titulo: "Potencia",
          descripcion: "P = U · I: vatios, kilovatios y la potencia de los aparatos.",
          eu: { titulo: "Potentzia", descripcion: "P = U · I: wattak, kilowattak eta aparatuen potentzia." } },
        { archivo: "consumo.html", id: "consumo", tema: "Magnitudes", icono: "rayo",
          titulo: "Consumo",
          descripcion: "kWh, contador y factura: calcula lo que gastan los aparatos.",
          eu: { titulo: "Kontsumoa", descripcion: "kWh, kontagailua eta faktura: kalkulatu aparatuek zenbat kontsumitzen duten." } },
        { archivo: "energia.html", id: "energia", tema: "Magnitudes", icono: "rayo",
          titulo: "Energía",
          descripcion: "Julios y kWh, transformaciones de la energía y rendimiento.",
          eu: { titulo: "Energia", descripcion: "Jouleak eta kWh, energiaren eraldaketak eta errendimendua." } },
        { archivo: "monofasica-trifasica.html", id: "monofasica-trifasica", tema: "Magnitudes", icono: "rayo",
          titulo: "Monofásica vs trifásica",
          descripcion: "230 V y 400 V, las tres fases desfasadas y la potencia en cada sistema.",
          eu: { titulo: "Monofasikoa vs trifasikoa", descripcion: "230 V eta 400 V, hiru fase desfasatuak eta sistema bakoitzeko potentzia." } },

        /* ---------- Elementos de protección ---------- */
        { archivo: "ficha-diferencial.html", id: "diferencial", tema: "Elementos de protección", icono: "diferencial",
          titulo: "Diferencial",
          descripcion: "Protege a las personas: toroide, 30 mA, tipos y simulador.",
          eu: { titulo: "Diferentziala", descripcion: "Pertsonak babesten ditu: toroidea, 30 mA, motak eta simulagailua." } },
        { archivo: "ficha-magnetotermico.html", id: "magnetotermico", tema: "Elementos de protección", icono: "magnetotermico",
          titulo: "Magnetotérmico",
          descripcion: "Partes, curvas B, C y D, símbolos y simulador por dentro.",
          eu: { titulo: "Magnetotermikoa", descripcion: "Zatiak, B, C eta D kurbak, sinboloak eta barruko simulagailua." } },
        { archivo: "icp.html", id: "icp", tema: "Elementos de protección", icono: "magnetotermico",
          titulo: "ICP (control de potencia)",
          descripcion: "Corta la luz si se supera la potencia contratada. Pruébalo encendiendo aparatos.",
          eu: { titulo: "PKE (potentzia kontrolatzeko etengailua)", descripcion: "Kontratatutako potentzia gainditzean argia mozten du. Probatu aparatuak piztuz." } },
        { archivo: "guardamotor.html", id: "guardamotor", tema: "Elementos de protección", icono: "magnetotermico",
          titulo: "Guardamotor",
          descripcion: "Protege el motor contra sobrecargas y cortocircuitos. Simulador de disparo y símbolo.",
          eu: { titulo: "Disyuntorea (guardamotorra)", descripcion: "Motorra gainkargen eta zirkuitulaburren aurka babesten du. Jauzi-simulagailua eta sinboloa." } },

        /* ---------- Instalaciones eléctricas ---------- */
        { archivo: "interruptor.html", id: "interruptor", tema: "Instalaciones eléctricas", icono: "conmutada",
          titulo: "Interruptor simple",
          descripcion: "Un punto de luz mandado desde un sitio: esquema, cables y simulador.",
          eu: { titulo: "Etengailu sinplea", descripcion: "Leku batetik agindutako argi-puntua: eskema, kableak eta simulagailua." } },
        {
          archivo: "conmutada-2-bombillas.html",
          id: "conmutada",
          titulo: "Conmutada con 2 bombillas",
          tema: "Instalaciones eléctricas",
          descripcion: "Dos conmutadores encienden las mismas bombillas desde dos puntos, como en un pasillo.",
          icono: "conmutada",
          eu: { titulo: "Konmutatua 2 bonbillarekin", descripcion: "Bi konmutadorek bonbilla berberak pizten dituzte bi lekutatik, korridore batean bezala." }
        },
        {
          archivo: "cruzamiento-2-bombillas.html",
          id: "cruzamiento",
          titulo: "Conmutada con cruzamiento",
          tema: "Instalaciones eléctricas",
          descripcion: "Un cruzamiento entre los dos conmutadores permite mandar las bombillas desde tres puntos.",
          icono: "cruzamiento",
          eu: { titulo: "Konmutatua gurutzagailuarekin", descripcion: "Bi konmutadoreen arteko gurutzagailu bati esker, bonbillak hiru lekutatik agin daitezke." }
        },
        { archivo: "enchufe.html", id: "enchufe", tema: "Instalaciones eléctricas", icono: "simulacion",
          titulo: "Base de enchufe",
          descripcion: "Tipos, bornes L, N y tierra, y por qué la toma de tierra salva vidas.",
          eu: { titulo: "Entxufe-oinarria", descripcion: "Motak, L, N eta lur-borneak, eta zergatik salbatzen dituen bizitzak lur-hartuneak." } },

        /* ---------- Elementos de control ---------- */
        { archivo: "pulsador.html", id: "pulsador", tema: "Elementos de control", icono: "pulsador",
          titulo: "Pulsador",
          descripcion: "Contactos NA y NC, colores normalizados y símbolo. Púlsalo y mira qué cambia.",
          eu: { titulo: "Sakagailua", descripcion: "NA eta NC kontaktuak, kolore normalizatuak eta sinboloa. Sakatu eta begiratu zer aldatzen den." } },
        { archivo: "contactor.html", id: "contactor", tema: "Elementos de control", icono: "simulacion",
          titulo: "Contactor",
          descripcion: "Partes, tipos, símbolo y marcha-paro con autorretención.",
          eu: { titulo: "Kontaktorea", descripcion: "Atalak, motak, sinboloa eta martxa-geldialdia autoatxikimenduarekin." } },
        { archivo: "piloto-luminoso.html", id: "piloto-luminoso", tema: "Elementos de control", icono: "lampara",
          titulo: "Piloto luminoso",
          descripcion: "Qué significa cada color y cómo se conecta. Cuadro de señalización para probar.",
          eu: { titulo: "Seinale-argia", descripcion: "Kolore bakoitzak zer esan nahi duen eta nola konektatzen den. Seinaleztapen-koadroa probatzeko." } },
        { archivo: "bornero.html", id: "bornero", tema: "Elementos de control", icono: "simulacion",
          titulo: "Bornero",
          descripcion: "Bornes de paso, tierra, neutro y seccionables; accesorios y numeración.",
          eu: { titulo: "Borne-regleta", descripcion: "Pasabideko, lurreko, neutroko eta ebakigarriak diren borneak; osagarriak eta zenbakitzea." } },

        /* ---------- Elementos de potencia ---------- */
        { archivo: "motor-jaula-ardilla.html", id: "motor-jaula-ardilla", tema: "Elementos de potencia", icono: "motor",
          titulo: "Motor de jaula de ardilla",
          descripcion: "El motor más usado: partes, campo magnético giratorio, deslizamiento y sentido de giro.",
          eu: { titulo: "Katagorri-kaiolako motorra", descripcion: "Motorrik erabiliena: atalak, eremu magnetiko birakaria, labainketa eta biraketa-noranzkoa." } },
        { archivo: "motor-rotor-bobinado.html", id: "motor-rotor-bobinado", tema: "Elementos de potencia", icono: "motor",
          titulo: "Motor de rotor bobinado",
          descripcion: "Anillos rozantes, escobillas y reóstato de arranque para mucho par.",
          eu: { titulo: "Errotore harilkatuko motorra", descripcion: "Eraztun irristakorrak, eskobillak eta abiarazte-erreostatoa momentu handia lortzeko." } },
        { archivo: "motor-imanes-permanentes.html", id: "motor-imanes-permanentes", tema: "Elementos de potencia", icono: "motor",
          titulo: "Motor de imanes permanentes",
          descripcion: "Síncrono y de alto rendimiento: rotor con imanes, variador y usos.",
          eu: { titulo: "Iman iraunkorreko motorra", descripcion: "Sinkronoa eta errendimendu handikoa: imandun errotorea, abiadura-aldagailua eta erabilerak." } },
        { archivo: "placa-motor.html", id: "placa-motor", tema: "Elementos de potencia", icono: "motor",
          titulo: "Placa de características",
          descripcion: "Qué significa cada dato de la placa de un motor trifásico. Estrella o triángulo.",
          eu: { titulo: "Ezaugarri-plaka", descripcion: "Motor trifasiko baten plakako datu bakoitzak zer esan nahi duen. Izarra edo triangelua." } },

        /* ---------- Fichas antiguas: no salen en la lista, pero sus enlaces siguen funcionando ---------- */
        { archivo: "magnitudes-electricas.html", id: "magnitudes-electricas", tema: "Magnitudes", icono: "simulacion", oculta: true,
          titulo: "Magnitudes eléctricas",
          descripcion: "Tensión, intensidad y potencia, con un circuito para medir.",
          eu: { titulo: "Magnitude elektrikoak", descripcion: "Tentsioa, intentsitatea eta potentzia, neurtzeko zirkuitu batekin." } },
        { archivo: "cc-ca.html", id: "cc-ca", tema: "Magnitudes", icono: "simulacion", oculta: true,
          titulo: "Corriente continua vs alterna",
          descripcion: "Diferencias, gráfica interactiva y valor eficaz.",
          eu: { titulo: "Korronte zuzena vs alternoa", descripcion: "Desberdintasunak, grafiko interaktiboa eta balio eraginkorra." } },
        {
          archivo: "magnetotermico.html",
          id: "magnetotermico-sim",
          oculta: true,
          titulo: "Magnetotérmico por dentro",
          tema: "Elementos de protección",
          descripcion: "Bimetal y bobina en acción: sobrecarga, cortocircuito y curvas de disparo B, C y D.",
          icono: "magnetotermico",
          eu: { titulo: "Magnetotermikoa barrutik", descripcion: "Bimetala eta bobina lanean: gainkarga, zirkuitulaburra eta B, C eta D etete-kurbak." }
        },
        {
          archivo: "diferencial.html",
          id: "diferencial-sim",
          oculta: true,
          titulo: "Diferencial por dentro",
          tema: "Elementos de protección",
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
        "Mando por presión": "Presio bidezko agintea",
        "Magnitudes": "Magnitudeak",
        "Elementos neumáticos": "Elementu neumatikoak"
      },
      simulaciones: [
        { archivo: "magnitudes-neumaticas.html", id: "magnitudes-neumaticas", tema: "Magnitudes", icono: "manometro",
          titulo: "Magnitudes neumáticas",
          descripcion: "Presión, caudal, fuerza, temperatura y humedad.",
          eu: { titulo: "Magnitude neumatikoak", descripcion: "Presioa, emaria, indarra, tenperatura eta hezetasuna." } },
        { archivo: "compresor.html", id: "compresor", tema: "Elementos neumáticos", icono: "simulacion",
          titulo: "Compresor",
          descripcion: "Partes y simulador con depósito y presostato.",
          eu: { titulo: "Konpresorea", descripcion: "Zatiak eta simulagailua depositoarekin eta presostatoarekin." } },
        { archivo: "secadores.html", id: "secadores", tema: "Elementos neumáticos", icono: "simulacion",
          titulo: "Secadores de aire",
          descripcion: "Frigorífico, de adsorción y de membrana.",
          eu: { titulo: "Lehorgailuak", descripcion: "Hozkailua, adsortziozkoa eta mintzazkoa." } },
        { archivo: "regulador.html", id: "regulador", tema: "Elementos neumáticos", icono: "regulador",
          titulo: "Regulador de presión",
          descripcion: "Partes, características, símbolo y simulador.",
          eu: { titulo: "Presio erreguladorea", descripcion: "Zatiak, ezaugarriak, sinboloa eta simulagailua." } },
        { archivo: "lubricador.html", id: "lubricador", tema: "Elementos neumáticos", icono: "simulacion",
          titulo: "Lubricador",
          descripcion: "Efecto Venturi: regula el goteo de aceite.",
          eu: { titulo: "Lubrikadorea", descripcion: "Venturi efektua: erregulatu olio-tantak." } },
        { archivo: "tubos.html", id: "tubos", tema: "Elementos neumáticos", icono: "simulacion",
          titulo: "Tubos neumáticos",
          descripcion: "Diámetros, materiales y velocidad del aire.",
          eu: { titulo: "Tutu neumatikoak", descripcion: "Diametroak, materialak eta airearen abiadura." } },
        { archivo: "racores.html", id: "racores", tema: "Elementos neumáticos", icono: "simulacion",
          titulo: "Racores",
          descripcion: "Racor instantáneo: meter y sacar el tubo. Tipos.",
          eu: { titulo: "Rakorrak", descripcion: "Berehalako rakorra: tutua sartu eta atera. Motak." } },
        {
          archivo: "regulador_presion.html",
          id: "regulador-sim",
          oculta: true,
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
      descripcion: "Planos, croquis, acotación, hojas de proceso, plegado y perfiles.",
      imagen: "imagenes/area-dibujo.webp",
      icono: "simulacion",
      eu: { nombre: "Marrazketa teknikoa", descripcion: "Planoak, krokisak, akotazioa, prozesu-orriak, tolestura eta profilak." },
      temas_eu: { "Fabricación": "Fabrikazioa", "Dibujo técnico": "Marrazketa teknikoa" },
      simulaciones: [
        { archivo: "planos.html", id: "planos", tema: "Dibujo técnico", icono: "simulacion",
          titulo: "Interpretación de planos y croquizado",
          descripcion: "Vistas, líneas, escalas, cajetín, croquis y normas.",
          eu: { titulo: "Planoen interpretazioa eta krokizazioa", descripcion: "Bistak, lerroak, eskalak, kajetina, krokisa eta arauak." } },
        { archivo: "hojas-proceso.html", id: "hojas-proceso", tema: "Fabricación", icono: "simulacion",
          titulo: "Hojas de proceso",
          descripcion: "Qué son, sus partes y un ejercicio para ordenar las operaciones.",
          eu: { titulo: "Prozesu-orriak", descripcion: "Zer diren, haien atalak eta eragiketak ordenatzeko ariketa bat." } },
        { archivo: "plegado.html", id: "plegado", tema: "Fabricación", icono: "simulacion",
          titulo: "Plegado de chapa",
          descripcion: "Pasos, radios de plegado y cálculo del desarrollo.",
          eu: { titulo: "Txaparen tolestura", descripcion: "Urratsak, tolestura-erradioak eta garapenaren kalkulua." } },
        { archivo: "acotacion.html", id: "acotacion", tema: "Dibujo técnico", icono: "simulacion",
          titulo: "Acotación",
          descripcion: "Elementos de una cota, normas, tipos y símbolos.",
          eu: { titulo: "Akotazioa", descripcion: "Kota baten elementuak, arauak, motak eta ikurrak." } },
        { archivo: "perfiles.html", id: "perfiles", tema: "Dibujo técnico", icono: "simulacion",
          titulo: "Perfiles metálicos normalizados",
          descripcion: "IPE, HEB, UPN, L, tubos… medidas, designación y peso.",
          eu: { titulo: "Metalezko profil normalizatuak", descripcion: "IPE, HEB, UPN, L, hodiak… neurriak, izendapena eta pisua." } }
      ]
    },
    {
      carpeta: "soldadura",
      nombre: "Soldadura",
      descripcion: "Preparación, parámetros y defectos de la soldadura.",
      imagen: "imagenes/area-soldadura.webp",
      icono: "simulacion",
      eu: { nombre: "Soldadura", descripcion: "Soldaduraren prestaketa, parametroak eta akatsak." },
      simulaciones: [
        { archivo: "preparacion.html", id: "soldadura-preparacion", icono: "simulacion",
          titulo: "Preparación de las superficies",
          descripcion: "Limpieza, bordes según el espesor, tipos de unión y punteado.",
          eu: { titulo: "Gainazalen prestaketa", descripcion: "Garbiketa, ertzak lodieraren arabera, lotura motak eta puntuazioa." } },
        { archivo: "parametros.html", id: "soldadura-parametros", icono: "simulacion",
          titulo: "Parámetros de soldadura",
          descripcion: "Electrodo, MIG/MAG y TIG: ajuste según material y espesor.",
          eu: { titulo: "Soldadura-parametroak", descripcion: "Elektrodoa, MIG/MAG eta TIG: doikuntza materialaren eta lodieraren arabera." } },
        { archivo: "defectos.html", id: "soldadura-defectos", icono: "simulacion",
          titulo: "Defectos de soldadura",
          descripcion: "Proyecciones, poros, falta de penetración… causas y soluciones.",
          eu: { titulo: "Soldaduretako akatsak", descripcion: "Proiekzioak, poroak, barneratze eskasa… kausak eta konponbideak." } }
      ]
    },
    {
      carpeta: "herramientas",
      nombre: "Herramientas",
      descripcion: "Herramientas manuales, neumáticas y eléctricas.",
      imagen: "imagenes/area-herramientas.webp",
      icono: "simulacion",
      eu: { nombre: "Erremintak", descripcion: "Eskuzko erreminta, neumatiko eta elektrikoak." },
      simulaciones: [
        { archivo: "manuales.html", id: "herramientas-manuales", icono: "simulacion",
          titulo: "Herramientas manuales",
          descripcion: "Golpe, sujeción, destornilladores, alicates, llaves, medir, marcar…",
          eu: { titulo: "Eskuzko erremintak", descripcion: "Kolpekoak, eusteko tresnak, torlojugailuak, alikateak, giltzak, neurtu, markatu…" } },
        { archivo: "neumaticas.html", id: "herramientas-neumaticas", icono: "simulacion",
          titulo: "Herramientas neumáticas",
          descripcion: "Taladro, roscadora, amoladora, remachadora, atornillador, martillo.",
          eu: { titulo: "Erreminta neumatikoak", descripcion: "Zulagailua, harizkatzeko makina, arteska, errematxagailua, torlojugailua, mailua." } },
        { archivo: "electricas.html", id: "herramientas-electricas", icono: "simulacion",
          titulo: "Herramientas eléctricas",
          descripcion: "Taladro, amoladora, cizalla, remachadora y atornillador.",
          eu: { titulo: "Erreminta elektrikoak", descripcion: "Zulagailua, arteska, zizaila, errematxagailua eta torlojugailua." } }
      ]
    }
  ]
};
