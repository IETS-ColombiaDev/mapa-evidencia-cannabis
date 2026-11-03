/* =========================================================================
   Mapa de Evidencia en Cannabis Medicinal — IETS
   Lógica del mapa público: filtros, matriz, tooltip, modal y exportación.
   ========================================================================= */

const CAMPOS_FILTRO = ["tipo_estudio", "poblacion", "decada"];

const estado = {
  datos: null,
  filtros: Object.fromEntries(CAMPOS_FILTRO.map((c) => [c, new Set()])),
  texto: "",
  vista: "burbujas",
  resaltarVacios: false,
  resaltarAprobados: false,
  indiceAprobados: new Map(),
  seleccion: null,      // { intervencionId, desenlaceId } o filtro por fila/columna
  estudioActivo: null,
};

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

/* ── Utilidades ─────────────────────────────────────────────────────── */
function normalizar(texto) {
  return (texto || "").toString().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function escapar(texto) {
  const d = document.createElement("div");
  d.textContent = texto == null ? "" : texto;
  return d.innerHTML;
}

function avisar(mensaje, tipo = "") {
  const cont = $("#avisos");
  const el = document.createElement("div");
  el.className = `aviso-flotante ${tipo}`;
  el.textContent = mensaje;
  cont.appendChild(el);
  setTimeout(() => el.remove(), 4200);
}

function decadaDe(anio) {
  if (!anio) return "Sin año";
  if (anio >= 2020) return "2020 en adelante";
  if (anio >= 2010) return "2010 a 2019";
  if (anio >= 2000) return "2000 a 2009";
  return "Antes de 2000";
}

/* ── Carga ──────────────────────────────────────────────────────────── */
async function cargar() {
  try {
    const resp = await fetch("/api/datos");
    const datos = await resp.json();
    if (!datos.ok) throw new Error("Respuesta inválida");
    estado.datos = datos;
    estado.indiceAprobados = new Map();
    (estado.datos.aprobados_colombia || []).forEach((m) => {
      const clave = `${m.intervencion_codigo}:${m.desenlace_codigo}`;
      if (!estado.indiceAprobados.has(clave)) {
        estado.indiceAprobados.set(clave, []);
      }
      estado.indiceAprobados.get(clave).push(m);
    });
    estado.datos.estudios.forEach((e) => {
      const rawPob = (e.poblacion_especial || "").trim();
      e.poblacion = rawPob || "Población general";
      e._poblaciones = rawPob
        ? rawPob.split(",").map((s) => s.trim()).filter(Boolean)
        : ["Población general"];
      e._busqueda = normalizar([
        e.titulo, e.autores, e.fuente, e.resumen, e.codigo,
        e.dominio_indicacion, e.indicacion, e.intervencion_texto,
        e.desenlaces_texto, e.abstract, e.poblacion,
        e._poblaciones.join(" "),
        e.intervenciones.map((i) => i.nombre).join(" "),
        e.desenlaces.map((d) => d.nombre).join(" "),
      ].join(" "));
      e.decada = decadaDe(e.anio);
    });
    construirPanelesDeFiltro();
    leerEstadoDeLaUrl();
    pintarNormativa();
    dibujar();
    $("#estado-carga").remove();
    $("#matriz").hidden = false;
  } catch (err) {
    console.error(err);
    $("#estado-carga").innerHTML =
      '<h3>No fue posible cargar los datos</h3><p>Revisa que el servidor esté en ejecución y vuelve a intentarlo.</p>';
  }
}

/* ── Filtros ────────────────────────────────────────────────────────── */
function valoresUnicos(campo) {
  if (campo === "poblacion") {
    const set = new Set();
    estado.datos.estudios.forEach((e) => {
      (e._poblaciones || []).forEach((p) => set.add(p));
    });
    const lista = Array.from(set).sort((a, b) => a.localeCompare(b, "es"));
    const idxGeneral = lista.indexOf("Población general");
    if (idxGeneral !== -1) {
      lista.splice(idxGeneral, 1);
      lista.unshift("Población general");
    }
    return lista;
  }
  const set = new Set();
  estado.datos.estudios.forEach((e) => { if (e[campo]) set.add(e[campo]); });
  const valores = Array.from(set);
  if (campo === "decada") {
    const orden = ["2020 en adelante", "2010 a 2019", "2000 a 2009", "Antes de 2000", "Sin año"];
    return valores.sort((a, b) => orden.indexOf(a) - orden.indexOf(b));
  }
  return valores.sort((a, b) => a.localeCompare(b, "es"));
}

function construirPanelesDeFiltro() {
  $$(".desplegable").forEach((det) => {
    const campo = det.dataset.filtro;
    const panel = $(".desplegable__panel", det);
    panel.innerHTML = "";
    valoresUnicos(campo).forEach((valor) => {
      const id = `f-${campo}-${normalizar(valor).replace(/\W+/g, "-")}`;
      const label = document.createElement("label");
      label.className = "opcion";
      label.innerHTML = `<input type="checkbox" id="${id}" value="${escapar(valor)}"><span>${escapar(valor)}</span>`;
      label.querySelector("input").addEventListener("change", (ev) => {
        const set = estado.filtros[campo];
        ev.target.checked ? set.add(valor) : set.delete(valor);
        actualizarResumenFiltros();
        dibujar();
      });
      panel.appendChild(label);
    });
  });

  document.addEventListener("click", (ev) => {
    $$(".desplegable[open]").forEach((d) => { if (!d.contains(ev.target)) d.open = false; });
  });
}

function actualizarResumenFiltros() {
  $$(".desplegable").forEach((det) => {
    const n = estado.filtros[det.dataset.filtro].size;
    const cuenta = $(".cuenta", det);
    cuenta.hidden = n === 0;
    cuenta.textContent = n;
  });

  const chips = $("#chips-activos");
  chips.innerHTML = "";
  const agregarChip = (etiqueta, alQuitar) => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.innerHTML = `<span>${escapar(etiqueta)}</span>`;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.setAttribute("aria-label", `Quitar filtro ${etiqueta}`);
    btn.textContent = "×";
    btn.addEventListener("click", alQuitar);
    chip.appendChild(btn);
    chips.appendChild(chip);
  };

  if (estado.texto) {
    agregarChip(`Búsqueda: ${estado.texto}`, () => {
      estado.texto = ""; $("#q").value = ""; actualizarResumenFiltros(); dibujar();
    });
  }
  CAMPOS_FILTRO.forEach((campo) => {
    estado.filtros[campo].forEach((valor) => {
      agregarChip(valor, () => {
        estado.filtros[campo].delete(valor);
        const casilla = $$(`.desplegable[data-filtro="${campo}"] input`)
          .find((i) => i.value === valor);
        if (casilla) casilla.checked = false;
        actualizarResumenFiltros();
        dibujar();
      });
    });
  });
  escribirEstadoEnLaUrl();
}

function estudiosFiltrados() {
  const texto = normalizar(estado.texto);
  return estado.datos.estudios.filter((e) => {
    if (texto && !e._busqueda.includes(texto)) return false;
    for (const campo of CAMPOS_FILTRO) {
      const set = estado.filtros[campo];
      if (!set.size) continue;
      if (campo === "poblacion") {
        const coincide = Array.from(set).some((pob) => e._poblaciones && e._poblaciones.includes(pob));
        if (!coincide) return false;
      } else {
        if (!set.has(e[campo])) return false;
      }
    }
    return true;
  });
}

/* ── Estado en la URL ───────────────────────────────────────────────── */
function escribirEstadoEnLaUrl() {
  const p = new URLSearchParams();
  if (estado.texto) p.set("q", estado.texto);
  CAMPOS_FILTRO.forEach((c) => {
    if (estado.filtros[c].size) p.set(c, Array.from(estado.filtros[c]).join("|"));
  });
  if (estado.vista !== "burbujas") p.set("vista", estado.vista);
  if (estado.resaltarVacios) p.set("vacios", "1");
  if (estado.resaltarAprobados) p.set("aprobados", "1");
  const cadena = p.toString();
  history.replaceState(null, "", cadena ? `?${cadena}` : location.pathname);
}

function leerEstadoDeLaUrl() {
  const p = new URLSearchParams(location.search);
  estado.texto = p.get("q") || "";
  $("#q").value = estado.texto;
  CAMPOS_FILTRO.forEach((c) => {
    const bruto = p.get(c);
    if (!bruto) return;
    bruto.split("|").forEach((v) => estado.filtros[c].add(v));
    $$(`.desplegable[data-filtro="${c}"] input`).forEach((i) => {
      if (estado.filtros[c].has(i.value)) i.checked = true;
    });
  });
  const vista = p.get("vista");
  if (["burbujas", "calor"].includes(vista)) {
    estado.vista = vista;
    $$(".segmentado [data-vista]").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.vista === vista)));
  }
  if (p.get("vacios") === "1") {
    estado.resaltarVacios = true;
    const bVac = $("#btn-vacios");
    if (bVac) {
      bVac.setAttribute("aria-pressed", "true");
      bVac.textContent = "Ocultar vacíos";
    }
  }
  if (p.get("aprobados") === "1") {
    estado.resaltarAprobados = true;
    const bApr = $("#btn-aprobados");
    if (bApr) {
      bApr.setAttribute("aria-pressed", "true");
      bApr.classList.add("boton--activo");
      bApr.textContent = "Ocultar aprobados";
    }
  }
  actualizarResumenFiltros();
}

/* ── Índice de celdas ───────────────────────────────────────────────── */
function construirIndice(estudios) {
  const indice = new Map();
  estudios.forEach((e) => {
    e.intervenciones.forEach((i) => {
      e.desenlaces.forEach((d) => {
        const clave = `${i.id}:${d.id}`;
        if (!indice.has(clave)) indice.set(clave, []);
        indice.get(clave).push(e);
      });
    });
  });
  return indice;
}

/* ── Dibujo de la matriz ────────────────────────────────────────────── */
function diametro(n, maximo) {
  if (!n) return 0;
  const min = 9, max = 30;
  if (maximo <= 1) return min + 6;
  return Math.round(min + (max - min) * Math.sqrt(n / maximo));
}

function dibujar() {
  const { intervenciones, desenlaces, categorias, dominios } = estado.datos;
  const estudios = estudiosFiltrados();
  const indice = construirIndice(estudios);

  const matriz = $("#matriz");
  matriz.style.setProperty("--n-cols", desenlaces.length);
  matriz.classList.toggle("vacio-visible", estado.resaltarVacios);
  matriz.classList.toggle("aprobados-visible", estado.resaltarAprobados);
  matriz.innerHTML = "";

  let maxSintesis = 0, maxPrimario = 0, maxTotal = 0;
  indice.forEach((lista) => {
    const s = lista.filter((e) => e.eje === "sintesis").length;
    const p = lista.length - s;
    maxSintesis = Math.max(maxSintesis, s);
    maxPrimario = Math.max(maxPrimario, p);
    maxTotal = Math.max(maxTotal, lista.length);
  });

  // Fila 1: esquinas + dominios
  const esquinaRail = document.createElement("div");
  esquinaRail.className = "m-esquina m-esquina--rail";
  esquinaRail.style.gridRow = "1 / span 2";
  matriz.appendChild(esquinaRail);

  const esquinaFila = document.createElement("div");
  esquinaFila.className = "m-esquina m-esquina--fila";
  esquinaFila.style.gridRow = "1 / span 2";
  esquinaFila.innerHTML = "Intervención &nbsp;/&nbsp; Desenlace";
  matriz.appendChild(esquinaFila);

  dominios.forEach((dom) => {
    const cuantos = desenlaces.filter((d) => d.dominio_id === dom.id).length;
    if (!cuantos) return;
    const celda = document.createElement("div");
    celda.className = "m-dominio";
    celda.style.gridColumn = `span ${cuantos}`;
    celda.textContent = dom.nombre;
    celda.title = dom.descripcion || "";
    matriz.appendChild(celda);
  });

  // Fila 2: desenlaces
  desenlaces.forEach((d) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "m-desenlace";
    btn.style.top = "34px";
    btn.innerHTML = `<span><span class="codigo">${escapar(d.codigo)}</span>${escapar(d.nombre)}</span>`;
    btn.title = d.descripcion || d.nombre;
    btn.setAttribute("aria-label", `Ver todos los estudios sobre ${d.nombre}`);
    btn.addEventListener("click", () => abrirModalColumna(d, estudios));
    matriz.appendChild(btn);
  });

  // Filas de intervenciones
  let filaVisual = 0;
  categorias.forEach((cat) => {
    const deCategoria = intervenciones.filter((i) => i.categoria_id === cat.id);
    if (!deCategoria.length) return;

    const rail = document.createElement("div");
    rail.className = "m-categoria";
    rail.style.gridRow = `span ${deCategoria.length}`;
    rail.textContent = cat.nombre;
    rail.title = cat.descripcion || "";
    matriz.appendChild(rail);

    deCategoria.forEach((inter) => {
      const totalFila = estudios.filter((e) =>
        e.intervenciones.some((x) => x.id === inter.id)).length;

      const encabezado = document.createElement("button");
      encabezado.type = "button";
      encabezado.className = "m-intervencion";
      encabezado.innerHTML =
        `<span class="codigo">${escapar(inter.codigo)}</span>` +
        `<span>${escapar(inter.nombre)}</span>` +
        `<span class="total">${totalFila} ${totalFila === 1 ? "estudio" : "estudios"}</span>`;
      encabezado.setAttribute("aria-label", `Ver todos los estudios sobre ${inter.nombre}`);
      encabezado.title = inter.descripcion || inter.nombre;
      encabezado.addEventListener("click", () => abrirModalFila(inter, estudios));
      matriz.appendChild(encabezado);

      desenlaces.forEach((des, c) => {
        const lista = indice.get(`${inter.id}:${des.id}`) || [];
        matriz.appendChild(crearCelda({
          lista, inter, des, filaVisual, columna: c,
          maxSintesis, maxPrimario, maxTotal,
        }));
      });
      filaVisual += 1;
    });
  });

  actualizarCifras(estudios, indice);
  requestAnimationFrame(ajustarEncabezadosFijos);
}

/* La segunda fila de encabezados debe quedar justo debajo de la primera,
   cuya altura depende del texto de los dominios. */
function ajustarEncabezadosFijos() {
  const dominio = $(".m-dominio");
  if (!dominio) return;
  const alto = Math.round(dominio.getBoundingClientRect().height) + 1;
  $$(".m-desenlace").forEach((el) => { el.style.top = `${alto}px`; });
}

function crearCelda({ lista, inter, des, filaVisual, columna, maxSintesis, maxPrimario, maxTotal }) {
  const sintesis = lista.filter((e) => e.eje === "sintesis").length;
  const primarios = lista.length - sintesis;
  const claveAprobados = `${inter.codigo}:${des.codigo}`;
  const aprobados = estado.indiceAprobados ? (estado.indiceAprobados.get(claveAprobados) || []) : [];
  const tieneAprobados = aprobados.length > 0;

  const celda = document.createElement("button");
  celda.type = "button";
  let clases = "m-celda" + (filaVisual % 2 ? " par" : "") + (lista.length ? "" : " vacia");
  if (tieneAprobados) clases += " celda--aprobado";
  celda.className = clases;
  celda.dataset.fila = filaVisual;
  celda.dataset.columna = columna;
  celda.tabIndex = filaVisual === 0 && columna === 0 ? 0 : -1;

  let descAria = "";
  if (!lista.length) {
    descAria = `${inter.nombre} y ${des.nombre}: sin evidencia cargada.`;
    celda.disabled = false;
  } else {
    descAria = `${inter.nombre} y ${des.nombre}: ${lista.length} estudio(s). ${sintesis} de síntesis y ${primarios} primarios. Abrir detalle.`;
  }
  if (tieneAprobados) {
    descAria += ` Cuenta con ${aprobados.length} medicamento(s) con registro sanitario INVIMA vigente en Colombia.`;
  }
  celda.setAttribute("aria-label", descAria);

  if (tieneAprobados) {
    const badge = document.createElement("span");
    badge.className = "insignia-invima";
    badge.setAttribute("aria-hidden", "true");
    badge.title = `INVIMA: ${aprobados.map((a) => a.producto).join(", ")}`;
    badge.textContent = "🇨🇴";
    celda.appendChild(badge);
  }

  if (estado.vista === "burbujas") {
    if (sintesis) {
      const b = document.createElement("span");
      b.className = "burbuja burbuja--sintesis";
      const d = diametro(sintesis, maxSintesis);
      b.style.width = b.style.height = `${d}px`;
      celda.appendChild(b);
    }
    if (primarios) {
      const b = document.createElement("span");
      b.className = "burbuja burbuja--primario";
      const d = diametro(primarios, maxPrimario);
      b.style.width = b.style.height = `${d}px`;
      celda.appendChild(b);
    }
  } else if (estado.vista === "calor") {
    if (lista.length) {
      const intensidad = maxTotal ? lista.length / maxTotal : 0;
      const fondo = document.createElement("span");
      fondo.className = "calor";
      fondo.style.background = `rgba(50, 180, 168, ${0.14 + intensidad * 0.82})`;
      celda.appendChild(fondo);
      const valor = document.createElement("span");
      valor.className = "calor-valor" + (intensidad > 0.55 ? " claro" : "");
      valor.textContent = lista.length;
      celda.appendChild(valor);
    }
  }

  celda.addEventListener("mouseenter", (ev) => mostrarTooltip(ev, { lista, inter, des, sintesis, primarios, aprobados }));
  celda.addEventListener("mousemove", moverTooltip);
  celda.addEventListener("mouseleave", ocultarTooltip);
  celda.addEventListener("focus", (ev) => mostrarTooltip(ev, { lista, inter, des, sintesis, primarios, aprobados }, true));
  celda.addEventListener("blur", ocultarTooltip);
  celda.addEventListener("click", () => {
    if (!lista.length && !tieneAprobados) {
      avisar("Ese cruce no tiene evidencia cargada todavía.");
      return;
    }
    abrirModalCelda(inter, des, lista, aprobados);
  });
  celda.addEventListener("keydown", navegarConTeclado);

  return celda;
}

function navegarConTeclado(ev) {
  const teclas = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] };
  if (!teclas[ev.key]) return;
  ev.preventDefault();
  const [df, dc] = teclas[ev.key];
  const f = Number(ev.currentTarget.dataset.fila) + df;
  const c = Number(ev.currentTarget.dataset.columna) + dc;
  const destino = $(`.m-celda[data-fila="${f}"][data-columna="${c}"]`);
  if (destino) {
    ev.currentTarget.tabIndex = -1;
    destino.tabIndex = 0;
    destino.focus();
  }
}

function actualizarCifras(estudios, indice) {
  const { intervenciones, desenlaces } = estado.datos;
  const totalCeldas = intervenciones.length * desenlaces.length;
  const conEvidencia = indice.size;
  const sintesis = estudios.filter((e) => e.eje === "sintesis").length;
  $("#cifra-estudios").textContent = estudios.length;
  $("#cifra-sintesis").textContent = sintesis;
  $("#cifra-primarios").textContent = estudios.length - sintesis;
  $("#cifra-vacios").textContent = totalCeldas - conEvidencia;
  const rotulo = $("#rotulo-vacios");
  if (rotulo) rotulo.textContent = `celdas sin evidencia, de ${totalCeldas}`;
}

/* ── Tooltip ────────────────────────────────────────────────────────── */
let tooltipFijo = false;

function mostrarTooltip(ev, { lista, inter, des, sintesis, primarios, aprobados = [] }, porFoco = false) {
  const tip = $("#tooltip");
  let bloqueEvidencia = "";
  if (lista.length) {
    bloqueEvidencia =
      `<div class="linea"><span class="punto punto--sintesis" style="width:10px;height:10px"></span>
         <b>${sintesis}</b> síntesis de evidencia</div>
       <div class="linea"><span class="punto punto--primario" style="width:10px;height:10px"></span>
         <b>${primarios}</b> estudios primarios</div>
       <div class="pista">Clic para leer los estudios</div>`;
  } else {
    bloqueEvidencia =
      `<div class="linea">Sin evidencia cargada para este cruce.</div>
       <div class="pista">Vacío de investigación</div>`;
  }

  let bloqueInvima = "";
  if (aprobados && aprobados.length) {
    const nombres = aprobados.map((a) => escapar(a.producto)).join(", ");
    bloqueInvima = `
      <div class="tooltip-invima">
        <div class="tooltip-invima__titulo"><span aria-hidden="true">🇨🇴</span> Aprobado INVIMA en Colombia</div>
        <div class="tooltip-invima__texto"><b>${aprobados.length}</b> producto(s): ${nombres}</div>
      </div>
    `;
  }

  tip.innerHTML = `<h4>${escapar(inter.nombre)} · ${escapar(des.nombre)}</h4>${bloqueEvidencia}${bloqueInvima}`;
  tip.dataset.visible = "true";
  tooltipFijo = porFoco;
  if (porFoco) {
    const r = ev.currentTarget.getBoundingClientRect();
    ubicarTooltip(r.left + r.width / 2, r.top);
  } else {
    ubicarTooltip(ev.clientX, ev.clientY);
  }
}

function moverTooltip(ev) {
  if (tooltipFijo) return;
  ubicarTooltip(ev.clientX, ev.clientY);
}

function ubicarTooltip(x, y) {
  const tip = $("#tooltip");
  const ancho = tip.offsetWidth || 280;
  const alto = tip.offsetHeight || 120;
  let izq = x + 16;
  let arr = y + 16;
  if (izq + ancho > window.innerWidth - 12) izq = x - ancho - 16;
  if (arr + alto > window.innerHeight - 12) arr = y - alto - 16;
  tip.style.left = `${Math.max(8, izq)}px`;
  tip.style.top = `${Math.max(8, arr)}px`;
}

function ocultarTooltip() {
  $("#tooltip").dataset.visible = "false";
  tooltipFijo = false;
}

/* ── Modal ──────────────────────────────────────────────────────────── */
function abrirModalCelda(inter, des, lista, aprobados = []) {
  abrirModal({
    titulo: `${inter.nombre} · ${des.nombre}`,
    descripcion: `${lista.length} ${lista.length === 1 ? "estudio evalúa" : "estudios evalúan"} este cruce con los filtros aplicados.`,
    lista,
    aprobados,
  });
}

function abrirModalFila(inter, estudios) {
  const lista = estudios.filter((e) => e.intervenciones.some((x) => x.id === inter.id));
  const aprobados = (estado.datos && estado.datos.aprobados_colombia)
    ? estado.datos.aprobados_colombia.filter((m) => m.intervencion_codigo === inter.codigo)
    : [];
  abrirModal({
    titulo: inter.nombre,
    descripcion: inter.descripcion || "",
    lista,
    aprobados,
  });
}

function abrirModalColumna(des, estudios) {
  const lista = estudios.filter((e) => e.desenlaces.some((x) => x.id === des.id));
  const aprobados = (estado.datos && estado.datos.aprobados_colombia)
    ? estado.datos.aprobados_colombia.filter((m) => m.desenlace_codigo === des.codigo)
    : [];
  abrirModal({
    titulo: des.nombre,
    descripcion: des.descripcion || "",
    lista,
    aprobados,
  });
}

function abrirModal({ titulo, descripcion, lista, aprobados = [] }) {
  const dialogo = $("#modal-estudios");
  $("#modal-titulo").textContent = titulo;
  $("#modal-descripcion").textContent = descripcion;
  $("#modal-conteo").textContent = `${lista.length} ${lista.length === 1 ? "estudio" : "estudios"}`;

  const alertaInvima = $("#modal-invima-alerta");
  if (alertaInvima) {
    if (aprobados && aprobados.length) {
      alertaInvima.hidden = false;
      alertaInvima.innerHTML = `
        <div class="alerta-invima">
          <div class="alerta-invima__cabecera">
            <span class="alerta-invima__icono" aria-hidden="true">🇨🇴</span>
            <div>
              <strong>Medicamentos con registro sanitario vigente emitido por el INVIMA (${aprobados.length})</strong>
              <p>Esta selección cuenta con <b>${aprobados.length}</b> medicamento(s) con registro sanitario en Colombia para esta indicación clínica.</p>
            </div>
          </div>
          <div class="alerta-invima__lista">
            ${aprobados.map((m) => `
              <div class="tarjeta-med-invima">
                <div class="tarjeta-med-invima__top">
                  <span class="tarjeta-med-invima__nombre">${escapar(m.producto)}</span>
                  <span class="tarjeta-med-invima__registro">${escapar(m.registro_sanitario)} · ${escapar(m.estado_registro || "Vigente")}</span>
                </div>
                <div class="tarjeta-med-invima__meta">
                  <div><b>Principio activo:</b> ${escapar(m.principio_activo)}</div>
                  <div><b>Forma:</b> ${escapar(m.forma_farmaceutica)} · <b>Vía:</b> ${escapar(m.via_administracion)} · <b>Concentración:</b> ${escapar(m.concentracion || "N/A")}</div>
                </div>
                ${m.indicaciones ? `
                  <details class="tarjeta-med-invima__detalles">
                    <summary>Ver indicación aprobada INVIMA</summary>
                    <p>${escapar(m.indicaciones)}</p>
                  </details>
                ` : ""}
              </div>
            `).join("")}
          </div>
        </div>
      `;
    } else {
      alertaInvima.hidden = true;
      alertaInvima.innerHTML = "";
    }
  }

  const ordenados = [...lista].sort((a, b) => {
    return (b.anio || 0) - (a.anio || 0) || a.titulo.localeCompare(b.titulo);
  });

  const contenedor = $("#modal-lista");
  contenedor.innerHTML = "";
  ordenados.forEach((e, i) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "item-estudio";
    item.setAttribute("role", "option");
    item.setAttribute("aria-selected", String(i === 0));
    const pob = e.poblacion || ((e.poblacion_especial && e.poblacion_especial.trim()) ? e.poblacion_especial.trim() : "Población general");
    item.innerHTML =
      `<span class="titulo">${escapar(e.titulo)}</span>` +
      `<span class="meta">${escapar(e.autores || "Sin autoría registrada")} · ${e.anio || "s. f."} · ${escapar(e.tipo_estudio)} · <b>${escapar(pob)}</b></span>`;
    item.addEventListener("click", () => {
      $$(".item-estudio", contenedor).forEach((x) => x.setAttribute("aria-selected", "false"));
      item.setAttribute("aria-selected", "true");
      pintarDetalle(e);
    });
    contenedor.appendChild(item);
  });

  if (ordenados.length) {
    pintarDetalle(ordenados[0]);
  } else {
    $("#modal-detalle").innerHTML = `
      <div class="vacio">
        <h3>Sin estudios cargados</h3>
        <p>No se encontraron publicaciones que cumplan los filtros activos para este cruce en el mapa.</p>
        ${aprobados && aprobados.length ? '<p style="color:#047857;font-weight:600;margin-top:.5rem">Sin embargo, cuenta con medicamentos aprobados por INVIMA arriba descritos.</p>' : ''}
      </div>
    `;
  }

  if (!dialogo.open) dialogo.showModal();
}

function pintarDetalle(e) {
  const claseEje = e.eje === "sintesis" ? "etiqueta--sintesis" : "etiqueta--primario";
  const claseEstado = e.estado === "Verificada" ? "etiqueta--ok" : "etiqueta--alerta";
  const enlace = e.url || (e.doi ? `https://doi.org/${e.doi}` : "");

  // Build source line: autores · año · fuente vol(num)
  let fuenteCompleta = e.fuente || "";
  if (e.volumen) fuenteCompleta += ` ${e.volumen}`;
  if (e.numero) fuenteCompleta += `(${e.numero})`;

  const poblacionTexto = (e.poblacion_especial && e.poblacion_especial.trim())
    ? e.poblacion_especial.trim()
    : "Población general";

  // Build extra fields section
  let extras = "";
  if (e.dominio_indicacion) {
    extras += `<div><dt>Dominio de la indicación</dt><dd>${escapar(e.dominio_indicacion)}</dd></div>`;
  }
  if (e.indicacion) {
    extras += `<div><dt>Indicación</dt><dd>${escapar(e.indicacion)}</dd></div>`;
  }
  if (e.intervencion_texto) {
    extras += `<div><dt>Intervención (según autores)</dt><dd>${escapar(e.intervencion_texto)}</dd></div>`;
  }
  if (e.desenlaces_texto) {
    extras += `<div><dt>Desenlaces (según autores)</dt><dd>${escapar(e.desenlaces_texto)}</dd></div>`;
  }

  // Build abstract section
  let abstractHtml = "";
  if (e.abstract) {
    abstractHtml = `
      <details class="abstract-detalle" style="margin-top:.8rem">
        <summary style="cursor:pointer;font-weight:600;font-size:.85rem;color:var(--azul-700)">
          Ver abstract
        </summary>
        <p class="resumen" style="margin-top:.5rem;font-size:.82rem;line-height:1.6;max-height:300px;overflow-y:auto;padding-right:.5rem">${escapar(e.abstract)}</p>
      </details>`;
  }

  // Build map links section (only if study has taxonomy links)
  let mapeoHtml = "";
  if (e.intervenciones.length || e.desenlaces.length) {
    mapeoHtml = `<div class="mapeo">
      ${e.intervenciones.length ? `<h4>Intervenciones evaluadas (mapa)</h4>
      <div class="etiquetas">${e.intervenciones.map((i) => `<span class="etiqueta">${escapar(i.nombre)}</span>`).join("")}</div>` : ""}
      ${e.desenlaces.length ? `<h4>Desenlaces reportados (mapa)</h4>
      <div class="etiquetas">${e.desenlaces.map((d) => `<span class="etiqueta">${escapar(d.nombre)}</span>`).join("")}</div>` : ""}
    </div>`;
  }

  $("#modal-detalle").innerHTML = `
    <div class="etiquetas">
      <span class="etiqueta ${claseEje}">${escapar(e.tipo_estudio)}</span>
      <span class="etiqueta ${claseEstado}">${escapar(e.estado)}</span>
    </div>
    <h3>${escapar(e.titulo)}</h3>
    <p class="autoria">${escapar(e.autores || "Sin autoría registrada")} · ${e.anio || "s. f."}${fuenteCompleta ? " · " + escapar(fuenteCompleta) : ""}</p>
    ${e.resumen ? `<p class="resumen">${escapar(e.resumen)}</p>` : ""}
    <dl class="ficha">
      <div><dt>Población</dt><dd><b>${escapar(poblacionTexto)}</b></dd></div>
      <div><dt>Participantes</dt><dd>${e.n_participantes ? e.n_participantes.toLocaleString("es-CO") : "No reportado"}</dd></div>
      <div><dt>Identificador</dt><dd>${escapar(e.codigo)}</dd></div>
      ${extras}
    </dl>
    ${enlace ? `<p><a href="${escapar(enlace)}" target="_blank" rel="noopener">Abrir la fuente original</a></p>` : ""}
    ${abstractHtml}
    ${mapeoHtml}`;
  $("#modal-detalle").scrollTop = 0;
}

/* ── Exportación ────────────────────────────────────────────────────── */
function exportarCsv() {
  const estudios = estudiosFiltrados();
  if (!estudios.length) { avisar("No hay estudios que exportar con los filtros actuales.", "error"); return; }
  const columnas = [
    "codigo", "titulo", "autores", "anio", "fuente", "volumen", "numero",
    "tipo_estudio", "eje", "poblacion",
    "n_participantes", "doi", "url", "estado", "poblacion_especial",
    "dominio_indicacion", "indicacion", "intervencion_texto", "desenlaces_texto",
  ];
  const cabecera = [...columnas, "abstract", "intervenciones_mapa", "desenlaces_mapa"];
  const filas = estudios.map((e) => {
    const pob = (e.poblacion_especial && e.poblacion_especial.trim()) ? e.poblacion_especial.trim() : "Población general";
    const base = columnas.map((c) => {
      if (c === "poblacion") return pob;
      return e[c] ?? "";
    });
    base.push(e.abstract || "");
    base.push(e.intervenciones.map((i) => i.nombre).join(" | "));
    base.push(e.desenlaces.map((d) => d.nombre).join(" | "));
    return base;
  });
  const csv = [cabecera, ...filas]
    .map((fila) => fila.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(";"))
    .join("\r\n");

  const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `mapa-evidencia-cannabis-${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(a.href);
  avisar(`Descargamos ${estudios.length} registros.`, "exito");
}

/* ── Normativa ──────────────────────────────────────────────────────── */
function pintarNormativa() {
  const ul = $("#lista-normativa");
  ul.innerHTML = "";
  estado.datos.normativa.forEach((n) => {
    const li = document.createElement("li");
    li.innerHTML = n.url
      ? `<b><a href="${escapar(n.url)}" target="_blank" rel="noopener">${escapar(n.norma)}</a></b> ${escapar(n.descripcion)}`
      : `<b>${escapar(n.norma)}</b> ${escapar(n.descripcion)}`;
    ul.appendChild(li);
  });
}

/* ── Eventos globales ───────────────────────────────────────────────── */
let temporizadorBusqueda;
$("#q").addEventListener("input", (ev) => {
  clearTimeout(temporizadorBusqueda);
  temporizadorBusqueda = setTimeout(() => {
    estado.texto = ev.target.value.trim();
    actualizarResumenFiltros();
    dibujar();
  }, 220);
});

$$(".segmentado [data-vista]").forEach((btn) => {
  btn.addEventListener("click", () => {
    estado.vista = btn.dataset.vista;
    $$(".segmentado [data-vista]").forEach((b) =>
      b.setAttribute("aria-pressed", String(b === btn)));
    escribirEstadoEnLaUrl();
    dibujar();
  });
});

$("#btn-vacios").addEventListener("click", (ev) => {
  estado.resaltarVacios = !estado.resaltarVacios;
  ev.currentTarget.setAttribute("aria-pressed", String(estado.resaltarVacios));
  ev.currentTarget.textContent = estado.resaltarVacios ? "Ocultar vacíos" : "Resaltar vacíos";
  escribirEstadoEnLaUrl();
  dibujar();
});

const btnAprobados = $("#btn-aprobados");
if (btnAprobados) {
  btnAprobados.addEventListener("click", (ev) => {
    estado.resaltarAprobados = !estado.resaltarAprobados;
    btnAprobados.setAttribute("aria-pressed", String(estado.resaltarAprobados));
    btnAprobados.classList.toggle("boton--activo", estado.resaltarAprobados);
    btnAprobados.textContent = estado.resaltarAprobados ? "Ocultar aprobados" : "🇨🇴 Aprobados en Colombia";
    escribirEstadoEnLaUrl();
    dibujar();
    if (estado.resaltarAprobados) {
      avisar("Resaltando áreas donde existen medicamentos con registro INVIMA en Colombia.", "exito");
    }
  });
}

$("#btn-exportar").addEventListener("click", exportarCsv);

$("#btn-limpiar").addEventListener("click", () => {
  estado.texto = "";
  $("#q").value = "";
  CAMPOS_FILTRO.forEach((c) => estado.filtros[c].clear());
  $$(".desplegable input[type=checkbox]").forEach((i) => { i.checked = false; });
  estado.resaltarVacios = false;
  $("#btn-vacios").setAttribute("aria-pressed", "false");
  $("#btn-vacios").textContent = "Resaltar vacíos";
  estado.resaltarAprobados = false;
  if (btnAprobados) {
    btnAprobados.setAttribute("aria-pressed", "false");
    btnAprobados.classList.remove("boton--activo");
    btnAprobados.textContent = "🇨🇴 Aprobados en Colombia";
  }
  actualizarResumenFiltros();
  dibujar();
  avisar("Filtros restablecidos.");
});

$$("[data-cerrar]").forEach((b) =>
  b.addEventListener("click", () => b.closest("dialog").close()));

$("#modal-estudios").addEventListener("click", (ev) => {
  if (ev.target === ev.currentTarget) ev.currentTarget.close();
});

document.addEventListener("keydown", (ev) => {
  if (ev.key === "Escape") ocultarTooltip();
  if (ev.key === "/" && document.activeElement !== $("#q")) {
    ev.preventDefault();
    $("#q").focus();
  }
});

cargar();
