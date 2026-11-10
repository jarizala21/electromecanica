/* Electromecánica · lógica de la app
   Lee el catálogo (catalogo.js) y el índice de archivos que se genera al publicar
   (simulaciones/indice.json), pinta la portada, el menú de áreas y la lista de cada
   área, y abre cada simulación en el visor.
   Rutas: (vacía) o #inicio = portada · #areas = menú de áreas ·
          #carpeta-del-area = lista · #id-de-simulacion = visor. */
(function(){
  "use strict";

  /* ---------- símbolos dibujados en una rejilla de 48 × 48 ---------- */
  var GLIFOS = {
    lampara: '<circle cx="24" cy="24" r="11"/><path d="M16.2 16.2l15.6 15.6M31.8 16.2L16.2 31.8M24 4v9M24 35v9"/>',
    manometro: '<circle cx="24" cy="21" r="13"/><path d="M16 29L31 14M25.5 14H31v5.5M24 34v10"/>',
    engranaje: '<path d="M21.3 12.8L21.6 8.2L26.4 8.2L26.7 12.8L30.0 14.2L33.5 11.1L36.9 14.5L33.8 18.0L35.2 21.3L39.8 21.6L39.8 26.4L35.2 26.7L33.8 30.0L36.9 33.5L33.5 36.9L30.0 33.8L26.7 35.2L26.4 39.8L21.6 39.8L21.3 35.2L18.0 33.8L14.5 36.9L11.1 33.5L14.2 30.0L12.8 26.7L8.2 26.4L8.2 21.6L12.8 21.3L14.2 18.0L11.1 14.5L14.5 11.1L18.0 14.2Z"/><circle cx="24" cy="24" r="4.5"/>',
    magnetotermico: '<path d="M24 4v12M21 13l6 6M27 13l-6 6M24 44V32L15 18"/><path class="d" d="M19.5 25H32"/><rect x="32" y="21" width="9" height="8" rx="1"/>',
    diferencial: '<path d="M24 4v12M21 13l6 6M27 13l-6 6M24 44V32L15 18"/><ellipse cx="24" cy="38" rx="8" ry="3"/><path class="d" d="M32 38h6V25H19.5"/>',
    conmutada: '<path d="M4 24h8M12 24l20-9M34 14h10M34 34h10"/><circle class="f" cx="12" cy="24" r="2.2"/><circle class="t" cx="34" cy="14" r="2.2"/><circle class="t" cx="34" cy="34" r="2.2"/>',
    cruzamiento: '<path d="M4 14h8M4 34h8M36 14h8M36 34h8M12 14l24 20M12 34l24-20"/><circle class="t" cx="12" cy="14" r="2.2"/><circle class="t" cx="12" cy="34" r="2.2"/><circle class="t" cx="36" cy="14" r="2.2"/><circle class="t" cx="36" cy="34" r="2.2"/>',
    presostato: '<path d="M4 32h10M14 32l18-9M34 32h10"/><circle class="t" cx="14" cy="32" r="2.2"/><circle class="t" cx="34" cy="32" r="2.2"/><path class="d" d="M23 27.5V14"/><rect x="16" y="4" width="14" height="10" rx="1.5"/><path d="M21 12V6.5h3a2.2 2.2 0 0 1 0 4.4h-3"/>',
    regulador: '<rect x="14" y="10" width="20" height="28" rx="1.5"/><path d="M24 3v7M24 38v7M21 33V15M18 18.5l3-4 3 4M34 24l2.5-4 2.5 8 2.5-8 2 4"/><path class="d" d="M24 42H8V20h6"/>',
    cremallera: '<path d="M22.2 7.2L22.4 4.1L25.6 4.1L25.8 7.2L27.9 8.1L30.2 6.1L32.4 8.3L30.4 10.6L31.3 12.7L34.4 12.9L34.4 16.1L31.3 16.3L30.4 18.4L32.4 20.7L30.2 22.9L27.9 20.9L25.8 21.8L25.6 24.9L22.4 24.9L22.2 21.8L20.1 20.9L17.8 22.9L15.6 20.7L17.6 18.4L16.7 16.3L13.6 16.1L13.6 12.9L16.7 12.7L17.6 10.6L15.6 8.3L17.8 6.1L20.1 8.1Z"/><circle class="f" cx="24" cy="14.5" r="2"/><path d="M4 33h3l2-4h3l2 4h3l2-4h3l2 4h3l2-4h3l2 4h3l2-4h3l2 4M4 33v8h40v-8"/>',
    guia: '<path d="M4 41h40M8 41v-8h32v8"/><rect x="14" y="17" width="20" height="16" rx="1.5"/><path d="M11 10h26M15 6l-4 4 4 4M33 6l4 4-4 4"/>',
    acoplamiento: '<path d="M3 24h11M34 24h11"/><rect x="14" y="13" width="9" height="22" rx="1.5"/><rect x="25" y="13" width="9" height="22" rx="1.5"/><path class="d" d="M24 15v18"/>',
    cardan: '<path d="M3 30h13"/><path d="M31 20l13-10"/><path d="M16 21v18M16 21h4M16 39h4"/><path d="M25 15l9 11M25 15l-3 3M34 26l-3 3"/><circle class="f" cx="23" cy="27" r="3"/>',
    embrague: '<path d="M3 24h11M34 24h11"/><rect x="14" y="9" width="7" height="30" rx="1.5"/><rect x="27" y="9" width="7" height="30" rx="1.5"/><path class="d" d="M24 12v24"/>',
    biela: '<circle cx="15" cy="33" r="9"/><circle class="f" cx="15" cy="33" r="2"/><path d="M21 28l9-15"/><rect x="24" y="4" width="14" height="10" rx="1.5"/><circle class="t" cx="21" cy="28" r="2.6"/>',
    leva: '<path d="M24 15c5 0 7 7 10 11 3 5 2 15-10 15s-13-10-10-15c3-4 5-11 10-11z"/><circle class="f" cx="24" cy="31" r="2.2"/><path d="M24 3v12"/><path d="M19 3h10"/>',
    polea: '<circle cx="13" cy="29" r="8"/><circle cx="34" cy="22" r="11"/><circle class="f" cx="13" cy="29" r="2"/><circle class="f" cx="34" cy="22" r="2.2"/><path d="M12 21l21-10M14 37l21-4"/>',
    cadena: '<rect x="3" y="17" width="20" height="14" rx="7"/><rect x="16" y="17" width="16" height="14" rx="7"/><rect x="25" y="17" width="20" height="14" rx="7"/><circle class="f" cx="10" cy="24" r="2"/><circle class="f" cx="24" cy="24" r="2"/><circle class="f" cx="38" cy="24" r="2"/>',
    sinfin: '<rect x="6" y="5" width="36" height="12" rx="2"/><path d="M12 5l-4 12M19 5l-4 12M26 5l-4 12M33 5l-4 12M40 5l-4 12"/><circle cx="24" cy="32" r="11"/><circle class="f" cx="24" cy="32" r="2"/>',
    simulacion: '<path d="M8 24h32"/><circle class="t" cx="28" cy="24" r="5"/>'
  };

  var $ = function(id){ return document.getElementById(id); };
  var root = document.documentElement;
  function esc(s){ return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){ return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function norm(s){ return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function slug(s){ return norm(s).replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "x"; }
  function sinExt(f){ return String(f || "").replace(/\.html?$/i, ""); }
  function bonito(s){ s = String(s || "").replace(/[-_]+/g, " ").trim(); return s.charAt(0).toUpperCase() + s.slice(1); }
  /* ---------- idioma de los menús (las simulaciones siguen en su idioma) ---------- */
  var TEXTOS = {
    es: { app: "Electromecánica", elige: "Elige un área", areas: "Áreas", buscar: "Buscar simulación", instalar: "Instalar la app",
          portada: "Volver a la portada", volverAreas: "Volver a las áreas", volverA: "Volver a ", cerrar: "Cerrar aviso",
          anterior: "Simulación anterior", siguiente: "Simulación siguiente", reiniciar: "Reiniciar", completa: "Pantalla completa",
          cargando: "Cargando…", ant: "Anterior", sig: "Siguiente",
          sim: function(n){ return n + (n === 1 ? " simulación" : " simulaciones"); },
          res: function(n){ return n + (n === 1 ? " resultado" : " resultados"); },
          escribe: function(n){ return "Escribe para buscar entre " + n + " simulaciones."; },
          nada: function(t){ return "Ninguna simulación coincide con «" + t + "»."; },
          pos: function(i, n){ return i + " de " + n; } },
    eu: { app: "Elektromekanika", elige: "Aukeratu arlo bat", areas: "Arloak", buscar: "Bilatu simulazioa", instalar: "Instalatu aplikazioa",
          portada: "Itzuli azalera", volverAreas: "Itzuli arloetara", volverA: "Itzuli: ", cerrar: "Itxi oharra",
          anterior: "Aurreko simulazioa", siguiente: "Hurrengo simulazioa", reiniciar: "Berrabiarazi", completa: "Pantaila osoa",
          cargando: "Kargatzen…", ant: "Aurrekoa", sig: "Hurrengoa",
          sim: function(n){ return n === 1 ? "simulazio 1" : n + " simulazio"; },
          res: function(n){ return n === 1 ? "emaitza 1" : n + " emaitza"; },
          escribe: function(n){ return "Idatzi bilatzeko (" + n + " simulazio daude)."; },
          nada: function(t){ return "Ez dago «" + t + "» bilaketarekin bat datorren simulaziorik."; },
          pos: function(i, n){ return i + " / " + n; } }
  };
  var CLAVE_IDIOMA = "electromecanica:idioma";
  var IDIOMA = "es";
  try { IDIOMA = localStorage.getItem(CLAVE_IDIOMA) === "eu" ? "eu" : "es"; } catch (e) {}
  function L(){ return TEXTOS[IDIOMA]; }
  function plural(n){ return L().sim(n); }
  // Textos del catálogo en el idioma elegido (si falta la traducción, en castellano)
  function nombre(sec){ return (IDIOMA === "eu" && sec.eu.nombre) || sec.nombre; }
  function frase(sec){ return (IDIOMA === "eu" && sec.eu.descripcion) || sec.descripcion; }
  function titulo(sim){ return (IDIOMA === "eu" && sim.eu.titulo) || sim.titulo; }
  function desc(sim){ return (IDIOMA === "eu" && sim.eu.descripcion) || sim.descripcion; }
  function tema(sec, t){ return (IDIOMA === "eu" && sec.temasEu[t]) || t; }
  function traducirPagina(){
    document.documentElement.lang = IDIOMA;
    document.title = L().app;
    [].forEach.call(document.querySelectorAll("[data-t]"), function(el){ el.textContent = L()[el.getAttribute("data-t")]; });
    [].forEach.call(document.querySelectorAll("[data-t-aria]"), function(el){
      var t = L()[el.getAttribute("data-t-aria")];
      el.setAttribute("aria-label", t);
      if (el.hasAttribute("title")) el.title = t;
    });
    [].forEach.call(document.querySelectorAll("[data-t-ph]"), function(el){ el.placeholder = L()[el.getAttribute("data-t-ph")]; });
  }
  function ponerIdioma(id){
    IDIOMA = id === "eu" ? "eu" : "es";
    try { localStorage.setItem(CLAVE_IDIOMA, IDIOMA); } catch (e) {}
    traducirPagina(); pintarAreas();
  }
  function glifo(n){
    return '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      (GLIFOS[n] || GLIFOS.simulacion) + '</svg>';
  }
  var FLECHA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  var CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
  function foto(sec){
    return sec.imagen
      ? '<span class="disco"></span><img src="' + esc(sec.imagen) + '" alt="" decoding="async">'
      : '<span class="disco"></span><span class="glifo-grande">' + glifo(sec.icono) + '</span>';
  }

  /* ---------- catálogo + archivos realmente publicados ---------- */
  function construir(cat, indice){
    var secs = ((cat && cat.secciones) || []).map(function(s){
      var carpeta = s.carpeta || s.id;
      return {
        id: s.id || carpeta, carpeta: carpeta, nombre: s.nombre || bonito(carpeta), eu: s.eu || {}, temasEu: s.temas_eu || {},
        descripcion: s.descripcion || "", imagen: s.imagen || "", icono: s.icono || "simulacion",
        simulaciones: (s.simulaciones || []).map(function(x){
          return { id: x.id, archivo: x.archivo, titulo: x.titulo || bonito(sinExt(x.archivo)), tema: x.tema || "",
                   descripcion: x.descripcion || "", icono: x.icono || "simulacion", miniatura: x.miniatura || "", eu: x.eu || {} };
        })
      };
    });

    if (indice && Array.isArray(indice.carpetas)) {
      var hay = {};
      indice.carpetas.forEach(function(c){ hay[c.carpeta] = c.archivos || []; });
      // Quita del catálogo lo que ya no está publicado.
      secs.forEach(function(s){
        var lista = hay[s.carpeta] || [];
        s.simulaciones = s.simulaciones.filter(function(x){ return lista.some(function(f){ return f.archivo === x.archivo; }); });
      });
      // Añade las carpetas y los archivos nuevos que no están en el catálogo.
      indice.carpetas.forEach(function(c){
        var s = null;
        secs.forEach(function(z){ if (z.carpeta === c.carpeta) s = z; });
        if (!s) {
          s = { id: c.carpeta, carpeta: c.carpeta, nombre: bonito(c.carpeta), eu: {}, temasEu: {}, descripcion: "", imagen: "", icono: "simulacion", simulaciones: [] };
          secs.push(s);
        }
        (c.archivos || []).forEach(function(f){
          if (s.simulaciones.some(function(x){ return x.archivo === f.archivo; })) return;
          s.simulaciones.push({ id: null, archivo: f.archivo, titulo: f.titulo || bonito(sinExt(f.archivo)), tema: "",
                                descripcion: f.descripcion || "", icono: "simulacion", miniatura: "", eu: {} });
        });
      });
      secs = secs.filter(function(s){ return s.simulaciones.length > 0; });
    }

    var usados = { inicio: 1, areas: 1 };
    function unico(s){ var base = s, n = 2; while (usados[s]) s = base + "-" + (n++); usados[s] = 1; return s; }
    secs.forEach(function(s){ s.id = unico(slug(s.id)); });
    secs.forEach(function(s){
      s.simulaciones.forEach(function(x){
        x.id = unico(slug(x.id || sinExt(x.archivo)));
        x.ruta = "simulaciones/" + encodeURIComponent(s.carpeta) + "/" + encodeURIComponent(x.archivo);
        // Miniatura: la del catálogo o, si existe, simulaciones/<carpeta>/miniaturas/<archivo>.webp
        var m = x.miniatura ? s.carpeta + "/" + x.miniatura : s.carpeta + "/miniaturas/" + sinExt(x.archivo) + ".webp";
        x.foto = (!RECURSOS || RECURSOS[m]) ? "simulaciones/" + m.split("/").map(encodeURIComponent).join("/") : "";
      });
    });
    return secs;
  }

  var CATALOGO = self.CATALOGO || { secciones: [] };
  var SECCIONES = [], TODAS = [], RECURSOS = null;
  function aplicar(secs){
    SECCIONES = secs; TODAS = [];
    SECCIONES.forEach(function(sec){ sec.simulaciones.forEach(function(sim, i){ TODAS.push({ sec: sec, sim: sim, i: i }); }); });
    pintarAreas();
  }
  function porId(id){ for (var k = 0; k < TODAS.length; k++) if (TODAS[k].sim.id === id) return TODAS[k]; return null; }

  /* ---------- menú de áreas ---------- */
  function pintarAreas(){
    var nav = $("areas");
    nav.style.setProperty("--n", Math.max(SECCIONES.length, 1));
    nav.innerHTML = SECCIONES.map(function(sec){
      return '<a class="area" href="#' + esc(sec.id) + '">' +
        '<span class="area-foto" aria-hidden="true">' + foto(sec) + '</span>' +
        '<span class="area-texto">' +
          '<h3>' + esc(nombre(sec)) + '</h3>' +
          (frase(sec) ? '<span class="area-desc">' + esc(frase(sec)) + '</span>' : '') +
          '<span class="area-pie"><span class="pastilla">' + plural(sec.simulaciones.length) + '</span>' +
          '<span class="flecha">' + FLECHA + '</span></span>' +
        '</span></a>';
    }).join("");
  }

  // Temas en orden de aparición
  function temas(sec){
    var out = [];
    sec.simulaciones.forEach(function(x){ if (x.tema && out.indexOf(x.tema) < 0) out.push(x.tema); });
    return out;
  }
  function agrupada(sec){ return sec.simulaciones.length > 6 && temas(sec).length > 1; }

  function tarjeta(e, conSeccion, sinTema){
    var tm = e.sim.tema ? tema(e.sec, e.sim.tema) : "";
    var chip = conSeccion ? nombre(e.sec) + (tm ? " · " + tm : "") : (sinTema ? "" : tm);
    var mini = '<span class="mini">' + glifo(e.sim.icono) +
      (e.sim.foto ? '<img src="' + esc(e.sim.foto) + '" alt="" loading="lazy" decoding="async" onerror="this.remove()">' : '') + '</span>';
    return '<a class="card" href="#' + esc(e.sim.id) + '">' + mini +
      '<span class="card-body">' +
        (chip ? '<span class="chip">' + esc(chip) + '</span>' : '') +
        '<span class="card-title">' + esc(titulo(e.sim)) + '</span>' +
        (desc(e.sim) ? '<span class="card-desc">' + esc(desc(e.sim)) + '</span>' : '') +
      '</span><span class="ir">' + CHEV + '</span></a>';
  }

  var buscar = $("buscar"), abrirBuscar = $("abrir-buscar"), vAreas = $("vista-areas");
  function pintarBusqueda(){
    var abierto = !$("buscador").hidden;
    var texto = buscar.value.trim(), q = norm(texto), res = $("resultados");
    vAreas.classList.toggle("buscando", abierto);
    $("areas").hidden = $("areas-head").hidden = abierto;
    res.hidden = !abierto;
    if (!abierto) return;
    if (!q) {
      var unicas = {}; TODAS.forEach(function(e){ unicas[e.sim.ruta] = 1; });
      res.innerHTML = '<p class="res-head">' + esc(L().escribe(Object.keys(unicas).length)) + '</p>';
      return;
    }
    var palabras = q.split(/\s+/);
    var hits = TODAS.filter(function(e){
      var pajar = norm([e.sim.titulo, e.sim.descripcion, e.sim.tema, e.sec.nombre, e.sim.eu.titulo, e.sim.eu.descripcion,
                        e.sec.eu.nombre, e.sec.temasEu[e.sim.tema]].join(" "));
      return palabras.every(function(p){ return pajar.indexOf(p) >= 0; });
    });
    res.innerHTML = hits.length
      ? '<p class="res-head">' + esc(L().res(hits.length)) + '</p><div class="cards">' +
        hits.map(function(h){ return tarjeta(h, true); }).join("") + '</div>'
      : '<p class="empty">' + esc(L().nada(texto)) + '</p>';
  }
  buscar.addEventListener("input", pintarBusqueda);
  function mostrarBuscador(si){
    $("buscador").hidden = !si;
    abrirBuscar.setAttribute("aria-expanded", si ? "true" : "false");
    if (!si) buscar.value = "";
    pintarBusqueda();
    if (si) try { buscar.focus(); } catch (e) {}
  }
  abrirBuscar.addEventListener("click", function(){ mostrarBuscador($("buscador").hidden); });
  buscar.addEventListener("keydown", function(ev){ if (ev.key === "Escape") mostrarBuscador(false); });

  /* ---------- vistas ---------- */
  var COLOR_BARRA = { "vista-portada": "#fdb02e", "vista-areas": "#f5f3ef", "vista-seccion": "#f5f3ef" };
  function mostrarVista(id){
    ["vista-portada", "vista-areas", "vista-seccion"].forEach(function(v){ $(v).hidden = v !== id; });
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute("content", COLOR_BARRA[id]);
  }
  function verPortada(){ mostrarVista("vista-portada"); window.scrollTo(0, 0); }
  function verAreas(mover){
    mostrarVista("vista-areas"); pintarBusqueda();
    if (mover) window.scrollTo(0, 0);
  }
  function verSeccion(sec, mover){
    $("sec-barra").textContent = nombre(sec);
    $("sec-nombre").textContent = nombre(sec);
    $("sec-desc").textContent = frase(sec) || "";
    $("sec-desc").hidden = !frase(sec);
    $("sec-count").textContent = plural(sec.simulaciones.length);
    $("sec-foto").innerHTML = foto(sec);
    if (agrupada(sec)) {
      $("sec-cards").className = "lista";
      $("sec-cards").innerHTML = temas(sec).map(function(t){
        var items = [];
        sec.simulaciones.forEach(function(sim, i){ if (sim.tema === t) items.push(tarjeta({ sec: sec, sim: sim, i: i }, false, true)); });
        return '<section class="grupo"><h3>' + esc(tema(sec, t)) + ' <span class="num">' + items.length + '</span></h3><div class="cards">' + items.join("") + '</div></section>';
      }).join("");
    } else {
      $("sec-cards").className = "lista";
      $("sec-cards").innerHTML = '<div class="cards">' + sec.simulaciones.map(function(sim, i){ return tarjeta({ sec: sec, sim: sim, i: i }, false); }).join("") + '</div>';
    }
    mostrarVista("vista-seccion");
    if (mover) { window.scrollTo(0, 0); try { $("sec-nombre").focus({ preventScroll: true }); } catch (e) {} }
  }

  /* ---------- visor ---------- */
  var app = $("app"), visor = $("visor"), stage = $("stage"), frame = $("frame"), loading = $("loading");
  var abierta = null, entrada = null, turno = 0, esperando = -1;

  function cargar(e){
    esperando = ++turno;
    stage.classList.remove("listo"); loading.hidden = false;
    frame.src = e.sim.ruta;
  }
  frame.addEventListener("load", function(){
    if (esperando !== turno || !abierta) return;
    try { if (frame.contentWindow.location.href === "about:blank") return; } catch (err) {}
    stage.classList.add("listo"); loading.hidden = true;
  });

  function navegacion(btn, sim, etiqueta){
    btn.disabled = !sim;
    btn.setAttribute("data-ir", sim ? sim.id : "");
    btn.title = sim ? etiqueta + ": " + titulo(sim) : "";
  }
  function abrirVisor(e){
    var sec = e.sec, sim = e.sim, i = e.i;
    $("v-back").href = "#" + sec.id;
    $("v-back").setAttribute("aria-label", L().volverA + nombre(sec));
    $("v-sec").textContent = nombre(sec) + " · ";
    $("v-pos").textContent = L().pos(i + 1, sec.simulaciones.length);
    $("v-name").textContent = titulo(sim);
    frame.title = titulo(sim);
    navegacion($("v-prev"), sec.simulaciones[i - 1], L().ant);
    navegacion($("v-next"), sec.simulaciones[i + 1], L().sig);
    app.hidden = true; visor.hidden = false; root.classList.add("con-visor");
    if (abierta !== sim.id) { abierta = sim.id; entrada = e; cargar(e); }
  }
  function cerrarVisor(){
    if (visor.hidden) return;
    turno++; abierta = null; entrada = null;
    if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(function(){});
    frame.src = "about:blank";
    visor.hidden = true; app.hidden = false; root.classList.remove("con-visor");
  }

  ["v-prev", "v-next"].forEach(function(id){
    $(id).addEventListener("click", function(){ var d = this.getAttribute("data-ir"); if (d) location.hash = d; });
  });
  $("v-reload").addEventListener("click", function(){
    if (!entrada) return;
    esperando = ++turno;
    stage.classList.remove("listo"); loading.hidden = false;
    try { frame.contentWindow.location.reload(); } catch (err) { frame.src = entrada.sim.ruta; }
  });

  var vFull = $("v-full");
  if (document.fullscreenEnabled && visor.requestFullscreen) vFull.hidden = false;
  vFull.addEventListener("click", function(){
    try {
      if (document.fullscreenElement) document.exitFullscreen().catch(function(){});
      else { var p = visor.requestFullscreen(); if (p && p.catch) p.catch(function(){}); }
    } catch (e) {}
  });
  document.addEventListener("fullscreenchange", function(){
    vFull.setAttribute("aria-pressed", document.fullscreenElement ? "true" : "false");
  });
  document.addEventListener("keydown", function(ev){
    if (ev.key === "Escape" && !visor.hidden && !document.fullscreenElement && entrada) location.hash = entrada.sec.id;
  });

  /* ---------- rutas ---------- */
  function enrutar(mover){
    var id = "";
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) {}
    if (!id || id === "inicio") { cerrarVisor(); verPortada(); return; }
    if (id === "areas") { cerrarVisor(); verAreas(mover); return; }
    var sec = null;
    for (var k = 0; k < SECCIONES.length; k++) if (SECCIONES[k].id === id) sec = SECCIONES[k];
    var e = sec ? null : porId(id);
    if (e) abrirVisor(e);
    else { cerrarVisor(); if (sec) verSeccion(sec, mover); else verAreas(mover); }
  }
  window.addEventListener("hashchange", function(){ enrutar(true); });

  [].forEach.call(document.querySelectorAll("[data-idioma]"), function(a){
    a.addEventListener("click", function(){ ponerIdioma(a.getAttribute("data-idioma")); });
  });
  traducirPagina();
  aplicar(construir(CATALOGO, null));
  enrutar(false);

  // El índice lo genera la publicación automática: incluye simulaciones nuevas
  // aunque no estén en el catálogo, y oculta las que se hayan borrado.
  fetch("simulaciones/indice.json", { cache: "no-cache" })
    .then(function(r){ return r.ok ? r.json() : null; })
    .then(function(indice){
      if (!indice) return;
      RECURSOS = {};
      (indice.recursos || []).forEach(function(r){ RECURSOS[r] = 1; });
      aplicar(construir(CATALOGO, indice)); enrutar(false);
      // Pide al modo sin conexión que guarde también las simulaciones nuevas.
      if (navigator.serviceWorker && navigator.serviceWorker.ready) {
        navigator.serviceWorker.ready.then(function(reg){
          var rutas = TODAS.map(function(e){ return e.sim.ruta; });
          (indice.recursos || []).forEach(function(r){
            rutas.push("simulaciones/" + String(r).split("/").map(encodeURIComponent).join("/"));
          });
          if (reg.active) reg.active.postMessage({ tipo: "guardar", rutas: rutas });
        }).catch(function(){});
      }
    })
    .catch(function(){});

  /* ---------- instalación como app ---------- */
  var enApp = (window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true;
  var esIOS = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var instalar = $("instalar"), avisoIOS = $("aviso-ios"), peticion = null;

  if (!enApp && esIOS) instalar.hidden = false;
  window.addEventListener("beforeinstallprompt", function(ev){
    ev.preventDefault(); peticion = ev; instalar.hidden = false;
  });
  window.addEventListener("appinstalled", function(){ peticion = null; instalar.hidden = true; avisoIOS.hidden = true; });
  instalar.addEventListener("click", function(){
    if (peticion) {
      peticion.prompt();
      peticion.userChoice.then(function(r){ if (r && r.outcome === "accepted") instalar.hidden = true; peticion = null; }).catch(function(){});
    } else if (esIOS) {
      avisoIOS.hidden = !avisoIOS.hidden;
    }
  });
  $("cerrar-ios").addEventListener("click", function(){ avisoIOS.hidden = true; });

  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
    window.addEventListener("load", function(){ navigator.serviceWorker.register("sw.js").catch(function(){}); });
  }
})();
