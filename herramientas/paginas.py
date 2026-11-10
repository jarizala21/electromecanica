"""Genera las páginas HTML de la sección Mecánica a partir de los datos de abajo.
Uso: python3 herramientas/paginas.py   (escribe en simulaciones/mecanica/)"""
import html, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "simulaciones", "mecanica")

REPRES_ENGRANAJES = "Cómo se representa"

P = {}
def pagina(id, titulo, desc, lead, alt, tarjetas, usos, extra_img=None):
    P[id] = dict(titulo=titulo, desc=desc, lead=lead, alt=alt, tarjetas=tarjetas, usos=usos, extra_img=extra_img)

# ------------------------------------------------------------------ Guías de deslizamiento
pagina("guia-redonda", "Guía redonda", "Un casquillo desliza sobre un eje cilíndrico rectificado.",
       "Un eje cilíndrico rectificado sirve de guía y el carro se desliza sobre él mediante casquillos de bronce o de bolas (rodamientos lineales). Es una guía sencilla y económica.",
       "Animación: un carro con casquillo se desliza adelante y atrás sobre un eje redondo apoyado en un soporte; a la derecha, su sección.",
       [("Qué observar", ["El carro solo puede moverse en una dirección: a lo largo del eje.",
                          "El casquillo es la pieza que roza; se cambia cuando se desgasta.",
                          "Si el eje está apoyado en toda su longitud, no flecta con la carga."]),
        ("Ventajas e inconvenientes", ["Fácil de montar y de alinear.",
                                       "Con casquillos de bolas el rozamiento es muy bajo.",
                                       "Soporta menos carga que una guía plana o prismática."])],
       ["Impresoras 3D, plotters y pequeñas máquinas CNC.", "Columnas de prensas y troqueles.", "Puertas correderas ligeras y automatismos neumáticos."])

pagina("guia-plana", "Guía plana", "El carro apoya sobre superficies planas; unas regletas evitan que se levante.",
       "El carro apoya sobre superficies planas de la bancada. Unas regletas por debajo impiden que el carro se levante. Soporta cargas grandes.",
       "Animación: una mesa se desliza sobre una guía plana con forma de T; a la derecha, su sección con las regletas.",
       [("Qué observar", ["Las superficies de contacto son planas y amplias.",
                          "Las regletas abrazan la guía por debajo.",
                          "Para guiar de lado hacen falta superficies laterales o una segunda guía."]),
        ("Ventajas e inconvenientes", ["Gran capacidad de carga y buena rigidez.",
                                       "Fácil de fabricar y de rectificar.",
                                       "No se centra sola: el juego se ajusta con regletas."])],
       ["Bancadas de tornos y fresadoras.", "Mesas de rectificadoras.", "Carros de máquinas herramienta convencionales."])

pagina("guia-prismatica", "Guía prismática", "Guía en V: el carro se centra al apoyar en los dos flancos.",
       "La guía tiene forma de V (prisma) y el carro una ranura con la misma forma. Al apoyar en los dos flancos, el carro queda centrado y sin holgura lateral.",
       "Animación: un carro con ranura en V se desliza sobre una guía en V invertida; a la derecha, su sección.",
       [("Qué observar", ["El carro apoya en los dos flancos de la V, no en la punta.",
                          "El propio peso del carro lo mantiene centrado.",
                          "Suele combinarse con una guía plana al otro lado."]),
        ("Ventajas e inconvenientes", ["Se autocentra y compensa el desgaste con su peso.",
                                       "Guiado muy preciso.",
                                       "Más difícil de fabricar que una guía plana."])],
       ["Bancadas de tornos: una guía en V y otra plana.", "Carros longitudinales de máquinas herramienta.", "Mesas de precisión."])

pagina("guia-cola-de-milano", "Guía de cola de milano", "Perfil trapecial con regleta cónica para ajustar el juego.",
       "El perfil de la guía es un trapecio más ancho arriba que abajo. El carro lo abraza y no puede levantarse. Una regleta cónica con tornillos permite ajustar el juego.",
       "Animación: un carro se desliza sobre una guía de cola de milano; a la derecha, la sección con la regleta y sus tornillos.",
       [("Qué observar", ["El carro solo se puede sacar deslizándolo por un extremo.",
                          "La regleta va entre un flanco de la guía y el carro.",
                          "Apretando los tornillos se elimina la holgura."]),
        ("Ventajas e inconvenientes", ["Compacta y muy rígida.",
                                       "El juego se ajusta fácilmente con la regleta.",
                                       "Más rozamiento que las guías con rodadura."])],
       ["Carro transversal y charriot del torno.", "Mesas de fresadoras convencionales.", "Utillajes y mesas de coordenadas."])

# ------------------------------------------------------------------ Acoplamientos
pagina("acoplamiento-oldham", "Acoplamiento Oldham", "Une ejes paralelos desplazados con un disco de lengüetas cruzadas.",
       "Une dos ejes paralelos que están desplazados. Tiene dos cubos con una ranura cada uno y un disco intermedio con dos lengüetas cruzadas a 90° que se deslizan por las ranuras.",
       "Animación: vista frontal del acoplamiento Oldham girando; el disco intermedio se desliza en las ranuras y su centro describe un círculo.",
       [("Qué observar", ["Los dos ejes giran a la misma velocidad.",
                          "El disco intermedio se desliza en las ranuras mientras gira.",
                          "El centro del disco describe un círculo pequeño."]),
        ("Características", ["Admite desalineación paralela (radial).",
                             "Casi no admite desalineación angular.",
                             "El disco suele ser de plástico técnico y hace de fusible."])],
       ["Accionamiento de husillos y encoders.", "Bombas y pequeños motores.", "Equipos en los que los ejes no quedan perfectamente alineados."])

pagina("acoplamiento-jaw", "Acoplamiento de garras (Jaw)", "Dos cubos con garras y una araña elástica entre ellas.",
       "Dos cubos con garras frontales encajan en una pieza elástica en forma de estrella, la araña. El giro pasa de un cubo al otro a través de la araña.",
       "Animación: los dos cubos y la araña se montan y el conjunto gira; a la derecha, vista frontal con las garras y la araña.",
       [("Qué observar", ["Las garras de los dos cubos nunca se tocan entre sí.",
                          "La araña de elastómero se comprime al transmitir el giro.",
                          "Se monta y desmonta separando los cubos a lo largo del eje."]),
        ("Características", ["Amortigua vibraciones y golpes.",
                             "Admite pequeñas desalineaciones angulares, radiales y axiales.",
                             "La araña es la pieza que se desgasta y se cambia."])],
       ["Unión motor-bomba.", "Motores eléctricos con reductores.", "Transportadores y maquinaria en general."])

pagina("acoplamiento-fuelle", "Acoplamiento de fuelle", "Un fuelle metálico: flexible a flexión y rígido a torsión.",
       "Un fuelle metálico de pared fina une los dos cubos. Se dobla para absorber desalineaciones, pero es muy rígido a torsión, así que transmite el giro sin holgura.",
       "Animación: el acoplamiento de fuelle gira mientras se muestran las desalineaciones angular, radial y axial.",
       [("Qué observar", ["La animación muestra tres desalineaciones: angular, radial y axial.",
                          "El fuelle se deforma, pero los dos cubos giran igual.",
                          "No hay piezas que rocen ni holguras."]),
        ("Características", ["Sin holgura: ideal para posicionar con precisión.",
                             "Muy rígido a torsión.",
                             "No admite grandes desalineaciones ni golpes fuertes."])],
       ["Servomotores y husillos de bolas.", "Encoders y tacómetros.", "Máquinas CNC y equipos de medida."])

pagina("cardan", "Junta cardán", "Transmite el giro entre ejes que forman un ángulo.",
       "Dos horquillas unidas por una cruceta transmiten el giro entre dos ejes que forman un ángulo. Es un acoplamiento articulado.",
       "Animación: junta cardán girando con 30° entre ejes; a la derecha, la gráfica de la velocidad del eje de salida.",
       [("Qué observar", ["La cruceta oscila mientras gira.",
                          "Con un solo cardán, el eje de salida acelera y frena dos veces por vuelta.",
                          "Cuanto mayor es el ángulo, mayor es la variación de velocidad."]),
        ("Para que la velocidad sea constante", ["Se montan dos cardanes con un eje intermedio.",
                                                 "Las horquillas del eje intermedio deben estar en el mismo plano.",
                                                 "Los dos ángulos deben ser iguales."])],
       ["Transmisiones de camiones y tractores.", "Columna de dirección de los coches.", "Tomas de fuerza agrícolas."])

# ------------------------------------------------------------------ Embragues
pagina("embrague-dientes", "Embrague de dientes", "Dientes frontales que encajan para unir dos ejes.",
       "Dos piezas con dientes frontales: una fija en el eje motriz y otra que se desliza sobre estrías del eje conducido. Una horquilla las acerca hasta que los dientes encajan.",
       "Animación: la horquilla acerca el manguito, los dientes encajan y el eje conducido empieza a girar; luego se separan.",
       [("Qué observar", ["Desembragado, el eje conducido no gira.",
                          "Con los dientes encajados, los dos ejes giran juntos sin deslizar.",
                          "La horquilla mueve el manguito a lo largo del eje."]),
        ("Características", ["Transmite mucho par en poco espacio.",
                             "No patina: la unión es rígida.",
                             "Solo se embraga con los ejes parados o a la misma velocidad."])],
       ["Cajas de cambios (con sincronizadores).", "Máquinas herramienta, para seleccionar velocidades.", "Cabrestantes y tornos de cable."])

pagina("embrague-disco", "Embrague de disco", "El disco transmite el giro por rozamiento entre volante y plato.",
       "Un disco con forros de fricción queda apretado por los muelles entre el volante del motor y el plato de presión. El giro se transmite por rozamiento.",
       "Animación en sección: al soltar el pedal, el plato aprieta el disco, que patina y coge velocidad hasta girar junto al motor.",
       [("Qué observar", ["Con el pedal pisado, el plato se separa y el disco gira libre.",
                          "Al soltar el pedal, el disco patina al principio y va cogiendo velocidad.",
                          "Embragado, todo gira junto."]),
        ("Características", ["Permite arrancar de forma progresiva.",
                             "Puede embragar con los ejes a distinta velocidad.",
                             "Los forros se desgastan con el uso."])],
       ["Coches y motos.", "Prensas mecánicas y máquinas con volante de inercia.", "Maquinaria agrícola."])

# ------------------------------------------------------------------ Transformadores de movimiento
pagina("biela-manivela", "Biela-manivela (cigüeñal)", "Convierte el giro en vaivén, y al revés.",
       "La manivela (o el cigüeñal) gira y la biela convierte ese giro en un movimiento de vaivén del pistón. También funciona al revés, como en los motores.",
       "Animación: el cigüeñal gira, la biela mueve el pistón entre el PMS y el PMI.",
       [("Qué observar", ["En el PMS y en el PMI el pistón se para un instante y cambia de sentido.",
                          "Media vuelta del cigüeñal es una carrera del pistón.",
                          "El pistón va más rápido en la zona central de la carrera."]),
        ("La cuenta", {"formula": "carrera = 2 · r",
                       "texto": ["r es el radio de la manivela: la distancia entre el eje del cigüeñal y el de la muñequilla.",
                                 "Con r = 40 mm, la carrera es de 80 mm."]})],
       ["Motores de combustión.", "Compresores de pistón.", "Prensas excéntricas y sierras alternativas."])

pagina("levas", "Levas: tipos", "Cuatro levas con su seguidor y la gráfica de su movimiento.",
       "Una leva es una pieza que, al girar, empuja a un seguidor y le da un movimiento de subida y bajada (o de ida y vuelta). La forma de la leva decide cómo se mueve el seguidor.",
       "Animación: cuatro tipos de leva girando con su seguidor y la gráfica de la posición del seguidor en una vuelta.",
       [("Qué observar", ["Cada gráfica muestra la posición del seguidor durante una vuelta.",
                          "La excéntrica da un movimiento suave, de vaivén.",
                          "La de corazón sube y baja a velocidad constante."]),
        ("Tipos de seguidor", ["De punta: preciso, pero se desgasta.",
                               "De rodillo: rueda sobre la leva y roza poco.",
                               "Plano: sencillo y robusto."])],
       ["Árbol de levas de los motores (válvulas).", "Máquinas automáticas y de embalaje.", "Tornos automáticos y programadores mecánicos."])

# ------------------------------------------------------------------ Engranajes
def repres(lista): return (REPRES_ENGRANAJES, lista)

pagina("engranajes-rectos", "Engranajes de dientes rectos", "Ejes paralelos; giran en sentidos contrarios. Con representación normalizada.",
       "Dos ruedas dentadas con los dientes paralelos al eje transmiten el giro entre ejes paralelos. Giran en sentidos contrarios y la más pequeña, el piñón, gira más deprisa.",
       "Animación: piñón de 10 dientes y rueda de 20 engranando; a la derecha, su representación normalizada en vista frontal y en corte axial.",
       [("Qué observar", ["Las dos ruedas giran en sentidos contrarios.",
                          "El piñón de 10 dientes da dos vueltas por cada vuelta de la rueda de 20.",
                          "Las circunferencias primitivas ruedan una sobre otra sin deslizar."]),
        repres(["Circunferencia de cabeza: línea continua gruesa.",
                "Circunferencia primitiva: línea fina de trazo y punto.",
                "Circunferencia de pie: no se dibuja en vista; en corte, línea gruesa.",
                "En corte axial los dientes no se rayan y, en el engrane, los de una rueda se dibujan ocultos."]),
        ("La cuenta", {"formula": "i = z₂ / z₁ = n₁ / n₂",
                       "texto": ["z es el número de dientes y n la velocidad de giro.",
                                 "Con z₁ = 10 y z₂ = 20, i = 2: si el piñón gira a 1400 rpm, la rueda gira a 700 rpm."]})],
       ["Cajas de velocidades de máquinas herramienta.", "Relojes y mecanismos de precisión.", "Reductores sencillos."])

pagina("engranajes-helicoidales", "Engranajes helicoidales", "Dientes inclinados: más silenciosos y con más carga. Con representación normalizada.",
       "Los dientes están inclinados respecto al eje. Entran en contacto poco a poco, por eso son más silenciosos y soportan más carga que los rectos.",
       "Animación: engranajes helicoidales en vista frontal y lateral; a la derecha, su representación normalizada con las tres líneas finas.",
       [("Qué observar", ["En la vista lateral se ve la inclinación de los dientes.",
                          "Las dos ruedas tienen la hélice en sentidos opuestos: una a derechas y otra a izquierdas.",
                          "El contacto empieza en un extremo del diente y avanza hacia el otro."]),
        repres(["Se dibujan igual que los de dientes rectos.",
                "En la vista paralela al eje, tres líneas finas indican la dirección del dentado.",
                "Cada rueda lleva sus líneas inclinadas en sentido contrario."]),
        ("Ventajas e inconvenientes", ["Más silenciosos y suaves.",
                                       "Hay más dientes en contacto: soportan más carga.",
                                       "Producen empuje axial: necesitan rodamientos que lo soporten."])],
       ["Cajas de cambios de coches.", "Reductores industriales.", "Bombas y compresores."])

pagina("engranajes-conicos", "Engranajes cónicos", "Ejes que se cortan, normalmente a 90°. Con representación normalizada.",
       "Las ruedas tienen forma de cono truncado y transmiten el giro entre ejes que se cortan, casi siempre a 90°. Los conos primitivos de las dos ruedas tienen el vértice en el mismo punto.",
       "Animación: piñón cónico de 12 dientes y rueda de 18 engranando a 90°; a la derecha, el corte axial normalizado de la pareja.",
       [("Qué observar", ["Los ejes del piñón y de la rueda se cortan.",
                          "La rueda de 18 dientes gira más despacio que el piñón de 12.",
                          "Los dientes se estrechan hacia el vértice."]),
        repres(["Normalmente se dibujan en corte axial.",
                "Los conos primitivos van con trazo y punto y se cortan en el vértice.",
                "El contorno de cabeza y el cuerpo, con línea gruesa; los dientes no se rayan."]),
        ("La cuenta", {"formula": "i = z₂ / z₁", "texto": ["Aquí i = 18 / 12 = 1,5."]})],
       ["Diferencial de los coches.", "Taladros de mano y amoladoras angulares.", "Reenvíos a 90° en maquinaria."])

pagina("tornillo-sin-fin", "Tornillo sin fin y corona", "Gran reducción entre ejes que se cruzan. Con representación normalizada.",
       "Un tornillo, llamado sin fin, engrana con una rueda dentada llamada corona. Los ejes se cruzan a 90° sin cortarse y se consigue una gran reducción en muy poco espacio.",
       "Animación: el tornillo sin fin gira y la corona avanza un diente por vuelta; a la derecha, su representación normalizada.",
       [("Qué observar", ["Cada vuelta del tornillo hace avanzar la corona un diente (tornillo de una entrada).",
                          "El tornillo es el elemento motriz.",
                          "Suele ser irreversible: la corona no puede mover el tornillo, y eso hace de freno."]),
        repres(["Corona en vista frontal: cabeza con línea gruesa y primitiva con trazo y punto.",
                "Tornillo de lado: líneas de cabeza gruesas y primitiva tangente a la de la corona.",
                "La parte de la corona tapada por el tornillo, en discontinua."]),
        ("La cuenta", {"formula": "i = z₂ / entradas",
                       "texto": ["Con una corona de 24 dientes y un tornillo de una entrada, i = 24:",
                                 "el tornillo da 24 vueltas por cada vuelta de la corona."]})],
       ["Reductores de velocidad.", "Elevadores, polipastos y clavijas de guitarra.", "Divisores de fresadora y mesas giratorias."])

pagina("dentado-interior", "Engranaje de dentado interior", "El piñón engrana por dentro de la corona; giran en el mismo sentido.",
       "La corona tiene los dientes por dentro y el piñón engrana en su interior. A diferencia de dos ruedas exteriores, las dos giran en el mismo sentido.",
       "Animación: piñón de 10 dientes girando dentro de una corona de 30; a la derecha, su representación normalizada.",
       [("Qué observar", ["El piñón y la corona giran en el mismo sentido.",
                          "El piñón da tres vueltas por cada vuelta de la corona.",
                          "Los ejes quedan muy cerca: el conjunto es compacto."]),
        repres(["Corona: contorno exterior y circunferencia de cabeza (la interior) con línea gruesa.",
                "Circunferencias primitivas con trazo y punto, tangentes por dentro.",
                "En corte, los dientes no se rayan."]),
        ("La cuenta", {"formula": "i = z₂ / z₁", "texto": ["Aquí i = 30 / 10 = 3."]})],
       ["Trenes epicicloidales: cajas automáticas y reductores planetarios.", "Bombas de engranajes internos.", "Mecanismos de giro de grúas."])

# ------------------------------------------------------------------ Poleas, correas y cadenas
pagina("formas-poleas", "Poleas: formas", "Formas de la garganta de las poleas según la correa.",
       "La polea transmite el giro a la correa por rozamiento (o mediante dientes). La forma de su garganta tiene que coincidir con la sección de la correa.",
       "Animación: transmisión por correa entre dos poleas; debajo, la sección de cinco tipos de polea con su correa.",
       [("Qué observar", ["Las dos poleas giran en el mismo sentido.",
                          "La polea pequeña gira más deprisa que la grande.",
                          "La correa en V no toca el fondo de la garganta: trabaja por los flancos."]),
        ("La cuenta", {"formula": "i = D₂ / D₁ = n₁ / n₂",
                       "texto": ["D es el diámetro de cada polea y n su velocidad.",
                                 "Con D₁ = 100 mm y D₂ = 150 mm, i = 1,5: si la motriz gira a 1500 rpm, la conducida gira a 1000 rpm."]})],
       ["Motores eléctricos que mueven taladros de columna, compresores o bombas.", "Distribución de motores (poleas dentadas).", "Lavadoras y secadoras."])

pagina("tipos-correas", "Correas: tipos", "Plana, trapezoidal, poli-V, dentada y redonda.",
       "La correa es una banda flexible que une dos o más poleas. Según su sección se usa para distintas potencias, velocidades y precisión.",
       "Animación: cinco tipos de correa en movimiento con su sección a la derecha.",
       [("Qué observar", ["Las correas lisas transmiten por rozamiento y pueden patinar un poco.",
                          "La dentada no patina: mantiene los ejes sincronizados.",
                          "Por dentro llevan cuerdas de refuerzo (los puntos claros de la sección)."]),
        ("Mantenimiento", ["Comprobar la tensión: ni floja (patina) ni demasiado tensa (castiga los rodamientos).",
                           "Revisar grietas, desgaste y brillo en los flancos.",
                           "Cambiar a la vez todas las correas de un mismo juego."])],
       ["Trapezoidales: compresores, bombas y máquinas herramienta.", "Poli-V: alternador y accesorios del motor del coche.", "Dentadas: distribución de motores, impresoras 3D y CNC."])

pagina("tipos-cadenas", "Cadenas: tipos", "Partes de la cadena de rodillos y tipos de cadena.",
       "La cadena une un piñón y una corona dentados. Transmite mucha fuerza sin patinar, incluso con los ejes bastante separados.",
       "Animación: transmisión por cadena de rodillos; a la derecha, sus partes; abajo, cadena simple, doble y silenciosa.",
       [("Qué observar", ["Los rodillos encajan en los huecos de los dientes.",
                          "Las placas interiores y exteriores se alternan.",
                          "El piñón pequeño gira más deprisa que la corona."]),
        ("La cuenta", {"formula": "i = z₂ / z₁", "texto": ["Con un piñón de 12 dientes y una corona de 20, i ≈ 1,67."]}),
        ("Mantenimiento", ["Lubricar con regularidad.",
                           "Ajustar la tensión: debe quedar una pequeña flecha.",
                           "Cambiar cadena y piñones a la vez cuando están gastados."])],
       ["Bicicletas y motos.", "Transportadores y elevadores.", "Maquinaria agrícola y de obra pública."])

# ------------------------------------------------------------------ Piñón y cremallera (se actualiza con su dibujo normalizado)
pagina("pinon-cremallera", "Piñón y cremallera", "El giro del piñón se convierte en desplazamiento rectilíneo de la cremallera.",
       "El piñón es una rueda dentada que engrana con una barra dentada recta, la cremallera. Cuando el piñón gira, la cremallera se desplaza en línea recta. También funciona al revés: si empujas la cremallera, el piñón gira.",
       "Animación: el piñón gira media vuelta en sentido antihorario y la cremallera avanza a la derecha; después gira en sentido horario y la cremallera vuelve a la izquierda.",
       [("Qué observar", ["Si el piñón cambia de sentido de giro, la cremallera cambia de sentido de avance.",
                          "La marca roja del piñón y la de la cremallera se encuentran en el punto de contacto: el piñón rueda sobre la cremallera sin deslizar.",
                          "Cuanto más grande es el piñón, más avanza la cremallera en cada vuelta."]),
        ("Cuánto avanza", {"formula": "avance por vuelta = π · d",
                           "texto": ["d es el diámetro primitivo del piñón. Con un piñón de 12 dientes y módulo 2 mm, d = 24 mm, así que cada vuelta mueve la cremallera π · 24 ≈ 75,4 mm.",
                                     "Media vuelta, como en la animación, son 37,7 mm."]}),
        repres(["Piñón: circunferencia de cabeza gruesa y primitiva de trazo y punto.",
                "Cremallera: línea de cabeza gruesa y línea primitiva tangente a la circunferencia primitiva del piñón.",
                "En la zona de engrane, los dientes de una de las piezas se dibujan ocultos."])],
       ["En el taladro de columna, la palanca de avance hace girar un piñón que baja el husillo con la broca.",
        "En la dirección de muchos coches, el volante gira el piñón y la cremallera orienta las ruedas.",
        "En puertas correderas automáticas y en ejes lineales de máquinas."],
       extra_img=("pinon-cremallera-normalizada.png", 800, 330, "Representación normalizada del piñón sobre la cremallera, con la leyenda de tipos de línea."))

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap">
<style>
:root{{
  --bg:#f5f3ef; --panel:#ffffff; --ink:#1b2147; --marino:#242d5f; --muted:#5d6382;
  --naranja:#f39200; --naranja-soft:#fff0dc; --naranja-osc:#b45f00;
  --sombra:0 10px 24px -16px rgba(36,45,95,.4),0 1px 3px rgba(36,45,95,.06);
  color-scheme:light;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Poppins",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:15.5px;line-height:1.6}}
.wrap{{max-width:900px;margin:0 auto;padding-block:22px 44px;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:18px}}
h1{{font-weight:700;font-size:clamp(25px,5vw,34px);line-height:1.12;letter-spacing:-.01em;margin:0;color:var(--marino)}}
h2{{font-weight:600;font-size:17px;margin:0 0 10px;color:var(--marino);display:flex;align-items:center;gap:10px}}
h2::before{{content:"";width:10px;height:10px;border-radius:50%;background:var(--naranja);flex:none}}
.lead{{margin:8px 0 0;color:var(--muted);max-width:62ch}}
figure{{margin:0;background:#f0f2f4;border-radius:22px;overflow:hidden;box-shadow:var(--sombra)}}
figure.norma{{background:#ffffff}}
figure img{{display:block;width:100%;height:auto;max-width:100%}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px}}
.card{{background:var(--panel);border-radius:22px;padding:18px 20px;box-shadow:var(--sombra)}}
ul{{margin:0;padding-left:20px;display:grid;gap:8px}}
li::marker{{color:var(--naranja)}}
.formula{{font-weight:600;font-size:20px;color:var(--marino);
  background:var(--naranja-soft);border-radius:12px;padding:6px 14px;display:inline-block;margin:2px 0 10px}}
.card p{{margin:0 0 8px}}
.card p:last-child{{margin-bottom:0}}
</style>
</head>
<body>
<main class="wrap">
  <header>
    <h1>{titulo}</h1>
    <p class="lead">{lead}</p>
  </header>

  <figure>
    <img src="{id}.gif" width="800" height="{alto}" alt="{alt}">
  </figure>
{extra}
  <div class="grid">
{tarjetas}
  </div>

  <section class="card">
    <h2>Dónde lo encontramos</h2>
    <ul>
{usos}
    </ul>
  </section>
</main>
</body>
</html>
"""

def tarjeta(t, cont):
    if isinstance(cont, dict):
        cuerpo = f'      <div class="formula">{html.escape(cont["formula"])}</div>\n' + "".join(f"      <p>{html.escape(p)}</p>\n" for p in cont["texto"])
    else:
        cuerpo = "      <ul>\n" + "".join(f"        <li>{html.escape(x)}</li>\n" for x in cont) + "      </ul>\n"
    return f'    <section class="card">\n      <h2>{html.escape(t)}</h2>\n{cuerpo}    </section>'

def main():
    os.makedirs(DEST, exist_ok=True)
    for id, d in P.items():
        extra = ""
        if d["extra_img"]:
            src, w, h, alt = d["extra_img"]
            extra = f'\n  <figure class="norma">\n    <img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}">\n  </figure>\n'
        out = PLANTILLA.format(id=id, titulo=html.escape(d["titulo"]), desc=html.escape(d["desc"]), lead=html.escape(d["lead"]),
                               alt=html.escape(d["alt"]), alto=480, extra=extra,
                               tarjetas="\n".join(tarjeta(t, c) for t, c in d["tarjetas"]),
                               usos="\n".join(f"      <li>{html.escape(u)}</li>" for u in d["usos"]))
        with open(os.path.join(DEST, f"{id}.html"), "w", encoding="utf-8") as f:
            f.write(out)
    print(len(P), "páginas en", DEST)

if __name__ == "__main__":
    main()
