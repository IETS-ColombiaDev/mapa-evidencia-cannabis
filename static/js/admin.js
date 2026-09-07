/* =========================================================================
   Panel de administración — Mapa de Evidencia en Cannabis Medicinal (IETS)
   ========================================================================= */

const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

const estado = {
  datos: null,
  catalogos: null,
  editando: null,          // estudio en edición
  taxonomia: { tipo: null, registro: null },
  porEliminar: null,       // { url, etiqueta, alTerminar }
  busqueda: "",
};

function escapar(t) {
  const d = document.createElement("div");
  d.textContent = t == null ? "" : t;
  return d.innerHTML;
}

function normalizar(t) {
  return (t || "").toString().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function avisar(mensaje, tipo = "") {
  const el = document.createElement("div");
  el.className = `aviso-flotante ${tipo}`;
  el.textContent = mensaje;
  $("#avisos").appendChild(el);
  setTimeout(() => el.remove(), 4200);
}

async function api(url, opciones = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  const cuerpo = await resp.json().catch(() => ({ ok: false, error: "Respuesta ilegible del servidor." }));
  if (!resp.ok || !cuerpo.ok) throw new Error(cuerpo.error || "No fue posible completar la operación.");
  return cuerpo;
}

/* ── Carga inicial ──────────────────────────────────────────────────── */
async function cargar() {
  const [datos, catalogos] = await Promise.all([
    fetch("/api/datos").then((r) => r.json()),
    fetch("/api/catalogos").then((r) => r.json()),
  ]);
  estado.datos = datos;
  estado.catalogos = catalogos;
  llenarSelectores();
  pintarTodo();
}

function pintarTodo() {
  pintarEstudios();
  pintarIntervenciones();
  pintarDesenlaces();
  pintarTaxonomia();
}

async function recargar() {
  estado.datos = await fetch("/api/datos").then((r) => r.json());
  pintarTodo();
}

/* ── Tabla de estudios ──────────────────────────────────────────────── */
function estudiosVisibles() {
  const texto = normalizar(estado.busqueda);
  const filtroEstado = $("#filtro-estado").value;
  const filtroTipo = $("#filtro-tipo").value;
  return estado.datos.estudios.filter((e) => {
    if (filtroEstado && e.estado !== filtroEstado) return false;
    if (filtroTipo && e.tipo_estudio !== filtroTipo) return false;
    if (!texto) return true;
    return normalizar(`${e.titulo} ${e.autores} ${e.codigo} ${e.fuente}`).includes(texto);
  });
}

function pintarEstudios() {
  const cuerpo = $("#tabla-estudios");
  const lista = estudiosVisibles();
  $("#conteo-estudios").textContent =
    `${lista.length} de ${estado.datos.estudios.length} estudios`;

  if (!lista.length) {
    cuerpo.innerHTML =
      '<tr><td colspan="8"><div class="vacio"><h3>Sin resultados</h3>' +
      '<p>Ajusta la búsqueda o agrega un estudio nuevo.</p></div></td></tr>';
    return;
  }

  cuerpo.innerHTML = "";
  lista.forEach((e) => {
    const tr = document.createElement("tr");
    const cruces = e.intervenciones.length * e.desenlaces.length;
    const claseEstado = e.estado === "Verificada" ? "etiqueta--ok" : "etiqueta--alerta";
    tr.innerHTML = `
      <td style="font-weight:700;color:var(--tinta-suave)">${escapar(e.codigo)}</td>
      <td class="celda-titulo">${escapar(e.titulo)}
        <div style="font-weight:400;color:var(--tinta-suave);font-size:.8rem">${escapar(e.autores || "Sin autoría")}</div>
      </td>
      <td>${e.anio || "—"}</td>
      <td>${escapar(e.tipo_estudio)}</td>
      <td>${escapar(e.certeza)}</td>
      <td>${e.intervenciones.length} × ${e.desenlaces.length} = <b>${cruces}</b></td>
      <td><span class="etiqueta ${claseEstado}">${escapar(e.estado)}</span></td>
      <td><div class="acciones">
        <button class="icono-boton" data-accion="editar">Editar</button>
        <button class="icono-boton" data-accion="duplicar">Duplicar</button>
        <button class="icono-boton peligro" data-accion="eliminar">Eliminar</button>
      </div></td>`;
    $('[data-accion="editar"]', tr).addEventListener("click", () => abrirFormularioEstudio(e));
    $('[data-accion="duplicar"]', tr).addEventListener("click", () => {
      const copia = { ...e, id: null, codigo: "", titulo: `${e.titulo} (copia)` };
      abrirFormularioEstudio(copia, true);
    });
    $('[data-accion="eliminar"]', tr).addEventListener("click", () =>
      confirmarEliminacion(`/api/estudios/${e.id}`, `el estudio “${e.titulo}”`));
    cuerpo.appendChild(tr);
  });
}

/* ── Tablas de taxonomía ────────────────────────────────────────────── */
function conteoPorIntervencion(id) {
  return estado.datos.estudios.filter((e) => e.intervenciones.some((i) => i.id === id)).length;
}
function conteoPorDesenlace(id) {
  return estado.datos.estudios.filter((e) => e.desenlaces.some((d) => d.id === id)).length;
}

function pintarIntervenciones() {
  const cuerpo = $("#tabla-intervenciones");
  cuerpo.innerHTML = "";
  estado.datos.intervenciones.forEach((i) => {
    const n = conteoPorIntervencion(i.id);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight:700;color:var(--tinta-suave)">${escapar(i.codigo)}</td>
      <td class="celda-titulo">${escapar(i.nombre)}
        <div style="font-weight:400;color:var(--tinta-suave);font-size:.8rem">${escapar(i.descripcion || "")}</div></td>
      <td>${escapar(i.categoria_nombre)}</td>
      <td>${i.orden}</td>
      <td>${n}</td>
      <td><div class="acciones">
        <button class="icono-boton" data-accion="editar">Editar</button>
        <button class="icono-boton peligro" data-accion="eliminar">Eliminar</button>
      </div></td>`;
    $('[data-accion="editar"]', tr).addEventListener("click", () =>
      abrirFormularioTaxonomia("intervencion", i));
    $('[data-accion="eliminar"]', tr).addEventListener("click", () =>
      confirmarEliminacion(`/api/intervenciones/${i.id}`,
        `la intervención “${i.nombre}”`,
        n ? `Se desvinculará de ${n} estudio(s), que seguirán existiendo.` : ""));
    cuerpo.appendChild(tr);
  });
}

function pintarDesenlaces() {
  const cuerpo = $("#tabla-desenlaces");
  cuerpo.innerHTML = "";
  estado.datos.desenlaces.forEach((d) => {
    const n = conteoPorDesenlace(d.id);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight:700;color:var(--tinta-suave)">${escapar(d.codigo)}</td>
      <td class="celda-titulo">${escapar(d.nombre)}
        <div style="font-weight:400;color:var(--tinta-suave);font-size:.8rem">${escapar(d.descripcion || "")}</div></td>
      <td>${escapar(d.dominio_nombre)}</td>
      <td>${d.orden}</td>
      <td>${n}</td>
      <td><div class="acciones">
        <button class="icono-boton" data-accion="editar">Editar</button>
        <button class="icono-boton peligro" data-accion="eliminar">Eliminar</button>
      </div></td>`;
    $('[data-accion="editar"]', tr).addEventListener("click", () =>
      abrirFormularioTaxonomia("desenlace", d));
    $('[data-accion="eliminar"]', tr).addEventListener("click", () =>
      confirmarEliminacion(`/api/desenlaces/${d.id}`,
        `el desenlace “${d.nombre}”`,
        n ? `Se desvinculará de ${n} estudio(s), que seguirán existiendo.` : ""));
    cuerpo.appendChild(tr);
  });
}

function pintarTaxonomia() {
  const filaSimple = (item, tipo, url) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight:700;color:var(--tinta-suave)">${escapar(item.codigo)}</td>
      <td class="celda-titulo">${escapar(item.nombre)}</td>
      <td>${item.orden}</td>
      <td><div class="acciones">
        <button class="icono-boton" data-accion="editar">Editar</button>
        <button class="icono-boton peligro" data-accion="eliminar">Eliminar</button>
      </div></td>`;
    $('[data-accion="editar"]', tr).addEventListener("click", () =>
      abrirFormularioTaxonomia(tipo, item));
    $('[data-accion="eliminar"]', tr).addEventListener("click", () =>
      confirmarEliminacion(`${url}/${item.id}`, `“${item.nombre}”`));
    return tr;
  };

  const cats = $("#tabla-categorias");
  cats.innerHTML = "";
  estado.datos.categorias.forEach((c) => cats.appendChild(filaSimple(c, "categoria", "/api/categorias")));

  const doms = $("#tabla-dominios");
  doms.innerHTML = "";
  estado.datos.dominios.forEach((d) => doms.appendChild(filaSimple(d, "dominio", "/api/dominios")));
}

/* ── Selectores del formulario ──────────────────────────────────────── */
function opciones(select, valores, seleccionado) {
  select.innerHTML = "";
  valores.forEach((v) => {
    const op = document.createElement("option");
    op.value = v;
    op.textContent = v;
    if (v === seleccionado) op.selected = true;
    select.appendChild(op);
  });
}

function llenarSelectores() {
  const c = estado.catalogos;
  opciones($("#f-tipo"), c.tipos_estudio);
  opciones($("#f-certeza"), c.certezas);
  opciones($("#f-hallazgo"), c.hallazgos);
  opciones($("#f-poblacion"), c.poblaciones);
  opciones($("#f-ambito"), c.ambitos);
  opciones($("#f-estado"), c.estados);

  const filtro = $("#filtro-tipo");
  c.tipos_estudio.forEach((t) => {
    const op = document.createElement("option");
    op.value = t; op.textContent = t;
    filtro.appendChild(op);
  });

  $("#f-tipo").addEventListener("change", mostrarEje);
}

function mostrarEje() {
  const tipo = $("#f-tipo").value;
  const esSintesis = estado.catalogos.tipos_sintesis.includes(tipo);
  $("#ayuda-eje").textContent = esSintesis
    ? "Se dibuja como círculo turquesa (síntesis de evidencia)."
    : "Se dibuja como círculo amarillo (estudio primario).";
}

function pintarSelectorMultiple(contenedor, grupos, seleccionados) {
  contenedor.innerHTML = "";
  grupos.forEach((grupo) => {
    const titulo = document.createElement("div");
    titulo.className = "grupo";
    titulo.textContent = grupo.nombre;
    contenedor.appendChild(titulo);
    grupo.items.forEach((item) => {
      const label = document.createElement("label");
      label.className = "opcion";
      const marcado = seleccionados.includes(item.id) ? "checked" : "";
      label.innerHTML =
        `<input type="checkbox" value="${item.id}" ${marcado}>` +
        `<span>${escapar(item.codigo)} · ${escapar(item.nombre)}</span>`;
      contenedor.appendChild(label);
    });
  });
}

function seleccionDe(contenedor) {
  return $$("input:checked", contenedor).map((i) => Number(i.value));
}

/* ── Formulario de estudio ──────────────────────────────────────────── */
function abrirFormularioEstudio(estudio = null, esCopia = false) {
  estado.editando = estudio && !esCopia ? estudio : null;
  const form = $("#form-estudio");
  form.reset();
  $("#mensaje-estudio").textContent = "";
  $("#titulo-form-estudio").textContent = estado.editando
    ? `Editar ${estudio.codigo}`
    : (esCopia ? "Duplicar estudio" : "Nuevo estudio");

  const v = estudio || {};
  $("#f-titulo").value = v.titulo || "";
  $("#f-codigo").value = esCopia ? "" : (v.codigo || "");
  $("#f-autores").value = v.autores || "";
  $("#f-anio").value = v.anio || "";
  $("#f-fuente").value = v.fuente || "";
  $("#f-pais").value = v.pais || "";
  $("#f-n").value = v.n_participantes || "";
  $("#f-doi").value = v.doi || "";
  $("#f-url").value = v.url || "";
  $("#f-resumen").value = v.resumen || "";
  opciones($("#f-tipo"), estado.catalogos.tipos_estudio, v.tipo_estudio || "Revisión sistemática");
  opciones($("#f-certeza"), estado.catalogos.certezas, v.certeza || "No evaluada");
  opciones($("#f-hallazgo"), estado.catalogos.hallazgos, v.hallazgo || "No concluyente");
  opciones($("#f-poblacion"), estado.catalogos.poblaciones, v.poblacion || "Mixta");
  opciones($("#f-ambito"), estado.catalogos.ambitos, v.ambito || "Global");
  opciones($("#f-estado"), estado.catalogos.estados, v.estado || "Por verificar");
  mostrarEje();

  const gruposInt = estado.datos.categorias.map((c) => ({
    nombre: c.nombre,
    items: estado.datos.intervenciones.filter((i) => i.categoria_id === c.id),
  }));
  const gruposDes = estado.datos.dominios.map((d) => ({
    nombre: d.nombre,
    items: estado.datos.desenlaces.filter((x) => x.dominio_id === d.id),
  }));
  pintarSelectorMultiple($("#sel-intervenciones"), gruposInt, (v.intervenciones || []).map((i) => i.id));
  pintarSelectorMultiple($("#sel-desenlaces"), gruposDes, (v.desenlaces || []).map((d) => d.id));

  $("#modal-estudio").showModal();
  $("#f-titulo").focus();
}

$("#form-estudio").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const datos = Object.fromEntries(new FormData(ev.target).entries());
  datos.intervenciones = seleccionDe($("#sel-intervenciones"));
  datos.desenlaces = seleccionDe($("#sel-desenlaces"));

  if (!datos.intervenciones.length || !datos.desenlaces.length) {
    $("#mensaje-estudio").textContent = "Selecciona al menos una intervención y un desenlace.";
    return;
  }

  const editando = estado.editando;
  try {
    if (editando) {
      await api(`/api/estudios/${editando.id}`, { method: "PUT", body: JSON.stringify(datos) });
      avisar("Estudio actualizado.", "exito");
    } else {
      const r = await api("/api/estudios", { method: "POST", body: JSON.stringify(datos) });
      avisar(`Estudio creado con el código ${r.codigo}.`, "exito");
    }
    $("#modal-estudio").close();
    await recargar();
  } catch (err) {
    $("#mensaje-estudio").textContent = err.message;
  }
});

/* ── Formulario de taxonomía ────────────────────────────────────────── */
const CONFIG_TAX = {
  intervencion: {
    titulo: "intervención", url: "/api/intervenciones",
    padre: { etiqueta: "Categoría", fuente: "categorias", campo: "categoria_id" },
  },
  desenlace: {
    titulo: "desenlace", url: "/api/desenlaces",
    padre: { etiqueta: "Dominio", fuente: "dominios", campo: "dominio_id" },
  },
  categoria: { titulo: "categoría de intervención", url: "/api/categorias", padre: null },
  dominio: { titulo: "dominio de desenlace", url: "/api/dominios", padre: null },
};

function abrirFormularioTaxonomia(tipo, registro = null) {
  const cfg = CONFIG_TAX[tipo];
  estado.taxonomia = { tipo, registro };
  const form = $("#form-taxonomia");
  form.reset();
  $("#mensaje-taxonomia").textContent = "";
  $("#titulo-form-tax").textContent = registro
    ? `Editar ${cfg.titulo}` : `Nueva ${cfg.titulo}`;

  $("#t-codigo").value = registro?.codigo || "";
  $("#t-codigo").disabled = Boolean(registro) && !cfg.padre;
  $("#t-nombre").value = registro?.nombre || "";
  $("#t-descripcion").value = registro?.descripcion || "";
  $("#t-orden").value = registro?.orden ?? 99;

  const campoPadre = $("#campo-padre");
  if (cfg.padre) {
    campoPadre.hidden = false;
    $("#lbl-padre").textContent = cfg.padre.etiqueta;
    const select = $("#t-padre");
    select.innerHTML = "";
    estado.datos[cfg.padre.fuente].forEach((p) => {
      const op = document.createElement("option");
      op.value = p.id;
      op.textContent = p.nombre;
      if (registro && registro[cfg.padre.campo] === p.id) op.selected = true;
      select.appendChild(op);
    });
  } else {
    campoPadre.hidden = true;
  }

  $("#modal-taxonomia").showModal();
  $("#t-nombre").focus();
}

$("#form-taxonomia").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const { tipo, registro } = estado.taxonomia;
  const cfg = CONFIG_TAX[tipo];
  const datos = Object.fromEntries(new FormData(ev.target).entries());
  const cuerpo = {
    codigo: datos.codigo || "",
    nombre: datos.nombre,
    descripcion: datos.descripcion,
    orden: Number(datos.orden) || 99,
  };
  if (cfg.padre) cuerpo[cfg.padre.campo] = Number($("#t-padre").value);

  try {
    if (registro) {
      await api(`${cfg.url}/${registro.id}`, { method: "PUT", body: JSON.stringify(cuerpo) });
      avisar("Cambios guardados.", "exito");
    } else {
      await api(cfg.url, { method: "POST", body: JSON.stringify(cuerpo) });
      avisar("Elemento creado.", "exito");
    }
    $("#modal-taxonomia").close();
    await recargar();
  } catch (err) {
    $("#mensaje-taxonomia").textContent = err.message;
  }
});

/* ── Eliminación ────────────────────────────────────────────────────── */
function confirmarEliminacion(url, etiqueta, nota = "") {
  estado.porEliminar = { url };
  $("#texto-confirmar").innerHTML =
    `Vas a eliminar ${escapar(etiqueta)}. Esta acción no se puede deshacer.` +
    (nota ? `<br><br>${escapar(nota)}` : "");
  $("#modal-confirmar").showModal();
}

$("#btn-confirmar").addEventListener("click", async () => {
  if (!estado.porEliminar) return;
  try {
    await api(estado.porEliminar.url, { method: "DELETE" });
    avisar("Registro eliminado.", "exito");
    $("#modal-confirmar").close();
    await recargar();
  } catch (err) {
    $("#modal-confirmar").close();
    avisar(err.message, "error");
  } finally {
    estado.porEliminar = null;
  }
});

/* ── Carga por lotes ────────────────────────────────────────────────── */
const EJEMPLO = {
  estudios: [
    {
      titulo: "Título del estudio",
      autores: "Apellido AA; Apellido BB",
      anio: 2024,
      fuente: "Nombre de la revista",
      tipo_estudio: "Ensayo clínico aleatorizado",
      poblacion: "Adultos",
      ambito: "América Latina",
      pais: "Colombia",
      certeza: "Moderada",
      hallazgo: "Favorable",
      n_participantes: 180,
      doi: "10.0000/ejemplo",
      url: "https://",
      resumen: "Qué se evaluó, en quiénes y qué encontró.",
      intervenciones: ["I2", "I7"],
      desenlaces: ["O1", "O11"],
    },
  ],
};

$("#btn-ejemplo").addEventListener("click", () => {
  $("#json-importar").value = JSON.stringify(EJEMPLO, null, 2);
});

$("#btn-importar").addEventListener("click", async () => {
  const salida = $("#resultado-importacion");
  let contenido;
  try {
    contenido = JSON.parse($("#json-importar").value);
  } catch {
    salida.innerHTML = '<span style="color:var(--alerta);font-weight:700">El texto no es JSON válido. Revisa comas y comillas.</span>';
    return;
  }
  const cuerpo = Array.isArray(contenido) ? { estudios: contenido } : contenido;
  try {
    const r = await api("/api/importar", { method: "POST", body: JSON.stringify(cuerpo) });
    salida.innerHTML =
      `<strong>${r.creados} registro(s) cargado(s).</strong>` +
      (r.omitidos.length
        ? `<div style="color:var(--alerta);margin-top:.4rem">Omitidos: ${escapar(r.omitidos.join(", "))}</div>`
        : "");
    avisar(`${r.creados} registro(s) cargado(s).`, "exito");
    await recargar();
  } catch (err) {
    salida.innerHTML = `<span style="color:var(--alerta);font-weight:700">${escapar(err.message)}</span>`;
  }
});

/* ── Navegación y eventos ───────────────────────────────────────────── */
$$('.pestanas [role="tab"]').forEach((tab) => {
  tab.addEventListener("click", () => {
    $$('.pestanas [role="tab"]').forEach((t) => t.setAttribute("aria-selected", String(t === tab)));
    $$(".panel").forEach((p) => { p.hidden = p.dataset.panel !== tab.dataset.panel; });
  });
});

$("#btn-nuevo").addEventListener("click", () => {
  const activa = $('.pestanas [role="tab"][aria-selected="true"]').dataset.panel;
  if (activa === "intervenciones") abrirFormularioTaxonomia("intervencion");
  else if (activa === "desenlaces") abrirFormularioTaxonomia("desenlace");
  else if (activa === "taxonomia") abrirFormularioTaxonomia("categoria");
  else abrirFormularioEstudio();
});

$$("[data-nuevo]").forEach((btn) =>
  btn.addEventListener("click", () => abrirFormularioTaxonomia(btn.dataset.nuevo)));

$$("[data-cerrar]").forEach((b) =>
  b.addEventListener("click", () => b.closest("dialog").close()));

let temporizador;
$("#q-admin").addEventListener("input", (ev) => {
  clearTimeout(temporizador);
  temporizador = setTimeout(() => {
    estado.busqueda = ev.target.value.trim();
    pintarEstudios();
  }, 200);
});

$("#filtro-estado").addEventListener("change", pintarEstudios);
$("#filtro-tipo").addEventListener("change", pintarEstudios);

cargar().catch((err) => {
  console.error(err);
  avisar("No fue posible cargar los datos. Revisa que el servidor esté activo.", "error");
});
