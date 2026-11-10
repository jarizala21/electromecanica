/* Fichas de herramientas: catálogo con detalle y test.
   Uso: fichaHerramientas({ lista: [...], test: [...] })
   Cada herramienta: { n:[es,eu], ico:'<svg…>', que:[es,eu], tipos:[es,eu], uso:[es,eu], ojo:[es,eu] }
   Cada pregunta:    { s:[es,eu], ops:[[es,eu],…], ok: índice } */
window.fichaHerramientas = function(D){
  var $ = function(id){ return document.getElementById(id); };
  var sel = 0, R = {};
  function L(x){ return T(x[0], x[1]); }
  function catalogo(){
    $("h-lista").innerHTML = D.lista.map(function(h, i){
      return '<button class="h-boton" data-i="' + i + '" aria-pressed="' + (i === sel) + '"><span class="h-ico">' + h.ico + '</span><span>' + L(h.n) + '</span></button>';
    }).join("");
    var h = D.lista[sel];
    $("h-detalle").innerHTML =
      '<div class="h-cab"><span class="h-ico grande">' + h.ico + '</span><h2>' + L(h.n) + '</h2></div>' +
      '<div class="rejilla">' +
      '<div class="card"><h3>' + T("¿Para qué sirve?", "Zertarako balio du?") + '</h3><p style="margin:0">' + L(h.que) + '</p></div>' +
      (h.tipos ? '<div class="card"><h3>' + T("Tipos", "Motak") + '</h3><p style="margin:0">' + L(h.tipos) + '</p></div>' : '') +
      (h.uso ? '<div class="card"><h3>' + T("Cómo se usa", "Nola erabiltzen da") + '</h3><p style="margin:0">' + L(h.uso) + '</p></div>' : '') +
      (h.ojo ? '<div class="card aviso-h"><h3>' + T("Seguridad", "Segurtasuna") + '</h3><p style="margin:0">' + L(h.ojo) + '</p></div>' : '') +
      '</div>';
  }
  function test(){
    if (!$("h-test")) return;
    $("h-test").innerHTML = D.test.map(function(q, i){
      var r = R[i], res = r === undefined ? "" : '<p class="' + (r === q.ok ? "ok" : "mal") + '" style="margin:6px 0 0">' + (r === q.ok ? T("¡Bien!", "Ondo!") : T("No. Prueba otra.", "Ez. Probatu beste bat.")) + '</p>';
      return '<div class="card"><h3>' + (i + 1) + '. ' + L(q.s) + '</h3><div class="chips">' + q.ops.map(function(o, j){ return '<button data-q="' + i + '" data-j="' + j + '" aria-pressed="' + (r === j) + '">' + L(o) + '</button>'; }).join("") + '</div>' + res + '</div>';
    }).join("");
    var hechas = Object.keys(R).length, bien = Object.keys(R).filter(function(k){ return R[k] === D.test[k].ok; }).length;
    if ($("h-nota")) $("h-nota").textContent = hechas ? T("Aciertos: ", "Asmatuak: ") + bien + " / " + D.test.length : "";
  }
  document.addEventListener("click", function(ev){
    var b = ev.target.closest(".h-boton");
    if (b) { sel = +b.getAttribute("data-i"); catalogo(); var d = $("h-detalle"); if (d && d.scrollIntoView && window.innerWidth < 760) d.scrollIntoView({ behavior: "smooth", block: "start" }); return; }
    var q = ev.target.closest("#h-test button");
    if (q) { R[+q.getAttribute("data-q")] = +q.getAttribute("data-j"); test(); }
  });
  alCambiarIdioma(function(){ catalogo(); test(); });
};
