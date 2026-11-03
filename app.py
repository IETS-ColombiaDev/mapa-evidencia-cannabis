"""
Mapa de Evidencia en Cannabis Medicinal — IETS
Aplicación Flask con base de datos SQLite y control de acceso administrativo.

Rutas públicas:
    /              mapa de evidencia interactivo, documentación y guía de lectura
    /login         inicio de sesión para administradores
    /logout        cierre de sesión administrativo
    /api/datos     estructura + estudios (fuente pública del mapa)
    /api/catalogos listas controladas
    /api/salud     estado de la plataforma

Rutas restringidas (Solo perfil Administrador):
    /admin                      panel de administración y gestión
    POST   /api/estudios        crear estudio
    PUT    /api/estudios/<id>   actualizar estudio
    DELETE /api/estudios/<id>   eliminar estudio
    POST/PUT/DELETE /api/intervenciones
    POST/PUT/DELETE /api/desenlaces
    POST/PUT/DELETE /api/categorias
    POST/PUT/DELETE /api/dominios
    POST   /api/importar        carga masiva desde JSON
    POST   /api/importar-excel  carga masiva desde archivo Excel (.xlsx)
"""

from datetime import timedelta
import functools
import io
import os
import re
import sqlite3
import unicodedata

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from database import (
    AMBITOS,
    CERTEZAS,
    ESTADOS,
    HALLAZGOS,
    POBLACIONES,
    TIPOS_ESTUDIO,
    TIPOS_PRIMARIO,
    TIPOS_SINTESIS,
    eje_de_tipo,
    get_conn,
    init_db,
    siguiente_codigo,
    verificar_usuario,
)
from data.mapeo_taxonomia import mapear_estudio

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.secret_key = os.environ.get("SECRET_KEY", "iets-mapa-cannabis-secreto-2025-cambiar-en-prod")
app.permanent_session_lifetime = timedelta(hours=12)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

init_db()


# ── Utilidades de Seguridad y Control de Acceso ────────────────────────────
def error(mensaje, codigo=400):
    return jsonify({"ok": False, "error": mensaje}), codigo


def campo(datos, nombre, por_defecto=""):
    valor = datos.get(nombre, por_defecto)
    return valor.strip() if isinstance(valor, str) else valor


def entero_o_nulo(valor):
    try:
        return int(valor) if valor not in (None, "", "null") else None
    except (TypeError, ValueError):
        return None


def admin_requerido(f):
    """Decorador que restringe el acceso exclusivamente a administradores autenticados."""
    @functools.wraps(f)
    def decorada(*args, **kwargs):
        if not session.get("admin_autenticado"):
            if request.path.startswith("/api/"):
                return error("Acceso no autorizado. Se requiere perfil de administrador para realizar esta operación.", 401)
            siguiente = request.full_path if request.query_string else request.path
            return redirect(url_for("vista_login", siguiente=siguiente))
        return f(*args, **kwargs)
    return decorada


# ── Vistas Públicas y Autenticación ────────────────────────────────────────
@app.route("/")
def vista_mapa():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def vista_login():
    siguiente = request.args.get("siguiente") or request.form.get("siguiente") or url_for("vista_admin")
    if request.method == "POST":
        usuario = (request.form.get("usuario") or "").strip()
        clave = (request.form.get("clave") or "").strip()

        usuario_valido = None
        # 1. Comprobar contra base de datos (con hash seguro)
        usuario_db = verificar_usuario(usuario, clave)
        
        # 2. Comprobar contra variables de entorno institucionales si están configuradas
        env_user = os.environ.get("ADMIN_USER", "admin")
        env_pass = os.environ.get("ADMIN_PASSWORD")
        if env_pass and usuario == env_user and clave == env_pass:
            usuario_valido = {"username": env_user, "nombre": "Administrador IETS", "rol": "admin"}
        elif usuario_db:
            usuario_valido = usuario_db

        if usuario_valido:
            session.clear()
            session.permanent = True
            session["admin_autenticado"] = True
            session["admin_usuario"] = usuario_valido["username"]
            session["admin_nombre"] = usuario_valido.get("nombre", "Administrador")
            session["admin_rol"] = usuario_valido.get("rol", "admin")
            return redirect(siguiente)
        else:
            return render_template(
                "login.html",
                error="Credenciales incorrectas. Verifique su usuario y contraseña institucional.",
                usuario=usuario,
                siguiente=siguiente,
            ), 401

    if session.get("admin_autenticado"):
        return redirect(siguiente)
    return render_template("login.html", siguiente=siguiente)


@app.route("/logout")
def vista_logout():
    session.clear()
    return redirect(url_for("vista_mapa"))


@app.route("/api/auth/estado")
def auth_estado():
    return jsonify({
        "ok": True,
        "autenticado": bool(session.get("admin_autenticado")),
        "usuario": session.get("admin_usuario", ""),
        "nombre": session.get("admin_nombre", ""),
        "rol": session.get("admin_rol", ""),
    })


# ── Panel de Administración Restringido ────────────────────────────────────
@app.route("/admin")
@admin_requerido
def vista_admin():
    return render_template("admin.html")


@app.route("/api/salud")
def salud():
    with get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM estudios").fetchone()["n"]
    return jsonify({"ok": True, "estudios": n})


# ── Lectura Pública del Mapa ───────────────────────────────────────────────
@app.route("/api/datos")
def datos():
    with get_conn() as conn:
        categorias = [dict(r) for r in conn.execute(
            "SELECT * FROM categorias_intervencion ORDER BY orden, id")]
        intervenciones = [dict(r) for r in conn.execute(
            """SELECT i.*, c.codigo AS categoria_codigo, c.nombre AS categoria_nombre
               FROM intervenciones i
               JOIN categorias_intervencion c ON c.id = i.categoria_id
               ORDER BY c.orden, i.orden, i.id""")]
        dominios = [dict(r) for r in conn.execute(
            "SELECT * FROM dominios_desenlace ORDER BY orden, id")]
        desenlaces = [dict(r) for r in conn.execute(
            """SELECT d.*, dom.codigo AS dominio_codigo, dom.nombre AS dominio_nombre
               FROM desenlaces d
               JOIN dominios_desenlace dom ON dom.id = d.dominio_id
               ORDER BY dom.orden, d.orden, d.id""")]
        normativa = [dict(r) for r in conn.execute(
            "SELECT * FROM normativa ORDER BY orden, id")]
        aprobados_colombia = [dict(r) for r in conn.execute(
            "SELECT * FROM medicamentos_aprobados ORDER BY orden, id")]

        estudios = [dict(r) for r in conn.execute("SELECT * FROM estudios ORDER BY anio DESC, id DESC")]
        rel_i, rel_d = {}, {}
        for r in conn.execute(
                """SELECT ei.estudio_id, i.id, i.codigo, i.nombre
                   FROM estudio_intervencion ei JOIN intervenciones i ON i.id = ei.intervencion_id"""):
            rel_i.setdefault(r["estudio_id"], []).append(
                {"id": r["id"], "codigo": r["codigo"], "nombre": r["nombre"]})
        for r in conn.execute(
                """SELECT ed.estudio_id, d.id, d.codigo, d.nombre
                   FROM estudio_desenlace ed JOIN desenlaces d ON d.id = ed.desenlace_id"""):
            rel_d.setdefault(r["estudio_id"], []).append(
                {"id": r["id"], "codigo": r["codigo"], "nombre": r["nombre"]})

    for e in estudios:
        e["intervenciones"] = rel_i.get(e["id"], [])
        e["desenlaces"] = rel_d.get(e["id"], [])
        e["eje"] = eje_de_tipo(e["tipo_estudio"])
        pob_esp = (e.get("poblacion_especial") or "").strip()
        e["poblacion"] = pob_esp if pob_esp else "Población general"

    return jsonify({
        "ok": True,
        "categorias": categorias,
        "intervenciones": intervenciones,
        "dominios": dominios,
        "desenlaces": desenlaces,
        "estudios": estudios,
        "normativa": normativa,
        "aprobados_colombia": aprobados_colombia,
    })


@app.route("/api/aprobados-colombia")
def api_aprobados_colombia():
    with get_conn() as conn:
        aprobados = [dict(r) for r in conn.execute(
            "SELECT * FROM medicamentos_aprobados ORDER BY orden, id")]
    return jsonify({"ok": True, "medicamentos": aprobados})


@app.route("/api/catalogos")
def catalogos():
    return jsonify({
        "ok": True,
        "tipos_estudio": TIPOS_ESTUDIO,
        "tipos_sintesis": sorted(TIPOS_SINTESIS),
        "tipos_primario": sorted(TIPOS_PRIMARIO),
        "certezas": CERTEZAS,
        "hallazgos": HALLAZGOS,
        "poblaciones": POBLACIONES,
        "ambitos": AMBITOS,
        "estados": ESTADOS,
    })


# ── Gestión de Estudios (Solo Administrador) ──────────────────────────────
def _guardar_relaciones(conn, estudio_id, intervenciones, desenlaces):
    conn.execute("DELETE FROM estudio_intervencion WHERE estudio_id = ?", (estudio_id,))
    conn.execute("DELETE FROM estudio_desenlace WHERE estudio_id = ?", (estudio_id,))
    for iid in intervenciones or []:
        conn.execute("INSERT OR IGNORE INTO estudio_intervencion VALUES (?,?)", (estudio_id, int(iid)))
    for did in desenlaces or []:
        conn.execute("INSERT OR IGNORE INTO estudio_desenlace VALUES (?,?)", (estudio_id, int(did)))


def _validar_estudio(d):
    if not campo(d, "titulo"):
        return "El título es obligatorio."
    if not campo(d, "tipo_estudio"):
        return "El tipo de estudio es obligatorio."
    return None


_COLS_INSERT = """(codigo, id_excel, titulo, autores, anio, fuente, volumen, numero,
                   doi, tipo_estudio, poblacion, ambito, pais, certeza, hallazgo,
                   n_participantes, url, resumen, estado, poblacion_especial,
                   dominio_indicacion, indicacion, intervencion_texto,
                   desenlaces_texto, abstract)"""


def _vals_de(d, codigo, estado_defecto="Por verificar"):
    pob_esp = campo(d, "poblacion_especial")
    pob = campo(d, "poblacion") or (pob_esp if pob_esp else "Población general")
    return (
        codigo,
        entero_o_nulo(d.get("id_excel")),
        campo(d, "titulo"),
        campo(d, "autores"),
        entero_o_nulo(d.get("anio")),
        campo(d, "fuente"),
        campo(d, "volumen"),
        campo(d, "numero"),
        campo(d, "doi"),
        campo(d, "tipo_estudio"),
        pob,
        campo(d, "ambito", "Global"),
        campo(d, "pais", ""),
        campo(d, "certeza", "No evaluada"),
        campo(d, "hallazgo", "No concluyente"),
        entero_o_nulo(d.get("n_participantes")),
        campo(d, "url"),
        campo(d, "resumen"),
        campo(d, "estado", estado_defecto),
        pob_esp,
        campo(d, "dominio_indicacion"),
        campo(d, "indicacion"),
        campo(d, "intervencion_texto"),
        campo(d, "desenlaces_texto"),
        campo(d, "abstract"),
    )


@app.route("/api/estudios", methods=["POST"])
@admin_requerido
def crear_estudio():
    d = request.get_json(silent=True) or {}
    problema = _validar_estudio(d)
    if problema:
        return error(problema)

    with get_conn() as conn:
        codigo = campo(d, "codigo") or siguiente_codigo(conn, "estudios", "E")
        try:
            cur = conn.execute(
                f"INSERT INTO estudios {_COLS_INSERT} VALUES ({','.join('?' * 25)})",
                _vals_de(d, codigo),
            )
        except sqlite3.IntegrityError:
            return error(f"Ya existe un estudio con el código {codigo}.", 409)
        _guardar_relaciones(conn, cur.lastrowid, d.get("intervenciones"), d.get("desenlaces"))
        nuevo_id = cur.lastrowid

    return jsonify({"ok": True, "id": nuevo_id, "codigo": codigo})


@app.route("/api/estudios/<int:estudio_id>", methods=["PUT"])
@admin_requerido
def actualizar_estudio(estudio_id):
    d = request.get_json(silent=True) or {}
    problema = _validar_estudio(d)
    if problema:
        return error(problema)

    with get_conn() as conn:
        existe = conn.execute("SELECT id FROM estudios WHERE id = ?", (estudio_id,)).fetchone()
        if not existe:
            return error("No se encontró el estudio.", 404)
        try:
            conn.execute(
                """UPDATE estudios SET codigo=?, id_excel=?, titulo=?, autores=?, anio=?,
                       fuente=?, volumen=?, numero=?, doi=?, tipo_estudio=?,
                       poblacion=?, ambito=?, pais=?, certeza=?, hallazgo=?,
                       n_participantes=?, url=?, resumen=?, estado=?,
                       poblacion_especial=?, dominio_indicacion=?, indicacion=?,
                       intervencion_texto=?, desenlaces_texto=?, abstract=?,
                       actualizado_en=datetime('now')
                   WHERE id=?""",
                _vals_de(d, campo(d, "codigo")) + (estudio_id,),
            )
        except sqlite3.IntegrityError:
            return error("Ese código ya está en uso por otro estudio.", 409)
        _guardar_relaciones(conn, estudio_id, d.get("intervenciones"), d.get("desenlaces"))

    return jsonify({"ok": True, "id": estudio_id})


@app.route("/api/estudios/<int:estudio_id>", methods=["DELETE"])
@admin_requerido
def eliminar_estudio(estudio_id):
    with get_conn() as conn:
        fila = conn.execute("SELECT codigo FROM estudios WHERE id = ?", (estudio_id,)).fetchone()
        if not fila:
            return error("No se encontró el estudio.", 404)
        conn.execute("DELETE FROM estudios WHERE id = ?", (estudio_id,))
    return jsonify({"ok": True, "codigo": fila["codigo"]})


# ── Taxonomía: intervenciones, desenlaces, categorías y dominios ───────────
@app.route("/api/intervenciones", methods=["POST"])
@admin_requerido
def crear_intervencion():
    d = request.get_json(silent=True) or {}
    if not campo(d, "nombre"):
        return error("El nombre de la intervención es obligatorio.")
    if not d.get("categoria_id"):
        return error("Selecciona la categoría a la que pertenece.")
    with get_conn() as conn:
        codigo = campo(d, "codigo") or siguiente_codigo(conn, "intervenciones", "I")
        try:
            cur = conn.execute(
                "INSERT INTO intervenciones (codigo, categoria_id, nombre, descripcion, orden)"
                " VALUES (?,?,?,?,?)",
                (codigo, int(d["categoria_id"]), campo(d, "nombre"), campo(d, "descripcion"),
                 entero_o_nulo(d.get("orden")) or 99),
            )
        except sqlite3.IntegrityError:
            return error(f"El código {codigo} ya existe.", 409)
        return jsonify({"ok": True, "id": cur.lastrowid, "codigo": codigo})


@app.route("/api/intervenciones/<int:iid>", methods=["PUT"])
@admin_requerido
def actualizar_intervencion(iid):
    d = request.get_json(silent=True) or {}
    if not campo(d, "nombre"):
        return error("El nombre de la intervención es obligatorio.")
    with get_conn() as conn:
        conn.execute(
            "UPDATE intervenciones SET codigo=?, categoria_id=?, nombre=?, descripcion=?, orden=?"
            " WHERE id=?",
            (campo(d, "codigo"), int(d["categoria_id"]), campo(d, "nombre"),
             campo(d, "descripcion"), entero_o_nulo(d.get("orden")) or 99, iid),
        )
    return jsonify({"ok": True})


@app.route("/api/intervenciones/<int:iid>", methods=["DELETE"])
@admin_requerido
def eliminar_intervencion(iid):
    with get_conn() as conn:
        usos = conn.execute(
            "SELECT COUNT(*) AS n FROM estudio_intervencion WHERE intervencion_id=?", (iid,)
        ).fetchone()["n"]
        conn.execute("DELETE FROM intervenciones WHERE id=?", (iid,))
    return jsonify({"ok": True, "vinculos_eliminados": usos})


@app.route("/api/desenlaces", methods=["POST"])
@admin_requerido
def crear_desenlace():
    d = request.get_json(silent=True) or {}
    if not campo(d, "nombre"):
        return error("El nombre del desenlace es obligatorio.")
    if not d.get("dominio_id"):
        return error("Selecciona el dominio al que pertenece.")
    with get_conn() as conn:
        codigo = campo(d, "codigo") or siguiente_codigo(conn, "desenlaces", "O")
        try:
            cur = conn.execute(
                "INSERT INTO desenlaces (codigo, dominio_id, nombre, descripcion, orden)"
                " VALUES (?,?,?,?,?)",
                (codigo, int(d["dominio_id"]), campo(d, "nombre"), campo(d, "descripcion"),
                 entero_o_nulo(d.get("orden")) or 99),
            )
        except sqlite3.IntegrityError:
            return error(f"El código {codigo} ya existe.", 409)
        return jsonify({"ok": True, "id": cur.lastrowid, "codigo": codigo})


@app.route("/api/desenlaces/<int:did>", methods=["PUT"])
@admin_requerido
def actualizar_desenlace(did):
    d = request.get_json(silent=True) or {}
    if not campo(d, "nombre"):
        return error("El nombre del desenlace es obligatorio.")
    with get_conn() as conn:
        conn.execute(
            "UPDATE desenlaces SET codigo=?, dominio_id=?, nombre=?, descripcion=?, orden=?"
            " WHERE id=?",
            (campo(d, "codigo"), int(d["dominio_id"]), campo(d, "nombre"),
             campo(d, "descripcion"), entero_o_nulo(d.get("orden")) or 99, did),
        )
    return jsonify({"ok": True})


@app.route("/api/desenlaces/<int:did>", methods=["DELETE"])
@admin_requerido
def eliminar_desenlace(did):
    with get_conn() as conn:
        usos = conn.execute(
            "SELECT COUNT(*) AS n FROM estudio_desenlace WHERE desenlace_id=?", (did,)
        ).fetchone()["n"]
        conn.execute("DELETE FROM desenlaces WHERE id=?", (did,))
    return jsonify({"ok": True, "vinculos_eliminados": usos})


@app.route("/api/categorias", methods=["POST"])
@admin_requerido
def crear_categoria():
    d = request.get_json(silent=True) or {}
    if not campo(d, "nombre"):
        return error("El nombre de la categoría es obligatorio.")
    with get_conn() as conn:
        codigo = campo(d, "codigo") or siguiente_codigo(conn, "categorias_intervencion", "C")
        try:
            cur = conn.execute(
                "INSERT INTO categorias_intervencion (codigo, nombre, descripcion, orden)"
                " VALUES (?,?,?,?)",
                (codigo, campo(d, "nombre"), campo(d, "descripcion"),
                 entero_o_nulo(d.get("orden")) or 99),
            )
        except sqlite3.IntegrityError:
            return error(f"El código {codigo} ya existe.", 409)
        return jsonify({"ok": True, "id": cur.lastrowid, "codigo": codigo})


@app.route("/api/categorias/<int:cid>", methods=["PUT"])
@admin_requerido
def actualizar_categoria(cid):
    d = request.get_json(silent=True) or {}
    with get_conn() as conn:
        conn.execute(
            "UPDATE categorias_intervencion SET nombre=?, descripcion=?, orden=? WHERE id=?",
            (campo(d, "nombre"), campo(d, "descripcion"),
             entero_o_nulo(d.get("orden")) or 99, cid),
        )
    return jsonify({"ok": True})


@app.route("/api/categorias/<int:cid>", methods=["DELETE"])
@admin_requerido
def eliminar_categoria(cid):
    with get_conn() as conn:
        n = conn.execute(
            "SELECT COUNT(*) AS n FROM intervenciones WHERE categoria_id=?", (cid,)
        ).fetchone()["n"]
        if n:
            return error(
                f"La categoría tiene {n} intervención(es). Muévelas o elimínalas primero.", 409)
        conn.execute("DELETE FROM categorias_intervencion WHERE id=?", (cid,))
    return jsonify({"ok": True})


@app.route("/api/dominios", methods=["POST"])
@admin_requerido
def crear_dominio():
    d = request.get_json(silent=True) or {}
    if not campo(d, "nombre"):
        return error("El nombre del dominio es obligatorio.")
    with get_conn() as conn:
        codigo = campo(d, "codigo") or siguiente_codigo(conn, "dominios_desenlace", "D")
        try:
            cur = conn.execute(
                "INSERT INTO dominios_desenlace (codigo, nombre, descripcion, orden)"
                " VALUES (?,?,?,?)",
                (codigo, campo(d, "nombre"), campo(d, "descripcion"),
                 entero_o_nulo(d.get("orden")) or 99),
            )
        except sqlite3.IntegrityError:
            return error(f"El código {codigo} ya existe.", 409)
        return jsonify({"ok": True, "id": cur.lastrowid, "codigo": codigo})


@app.route("/api/dominios/<int:did>", methods=["PUT"])
@admin_requerido
def actualizar_dominio(did):
    d = request.get_json(silent=True) or {}
    with get_conn() as conn:
        conn.execute(
            "UPDATE dominios_desenlace SET nombre=?, descripcion=?, orden=? WHERE id=?",
            (campo(d, "nombre"), campo(d, "descripcion"),
             entero_o_nulo(d.get("orden")) or 99, did),
        )
    return jsonify({"ok": True})


@app.route("/api/dominios/<int:did>", methods=["DELETE"])
@admin_requerido
def eliminar_dominio(did):
    with get_conn() as conn:
        n = conn.execute(
            "SELECT COUNT(*) AS n FROM desenlaces WHERE dominio_id=?", (did,)
        ).fetchone()["n"]
        if n:
            return error(
                f"El dominio tiene {n} desenlace(s). Muévelos o elimínalos primero.", 409)
        conn.execute("DELETE FROM dominios_desenlace WHERE id=?", (did,))
    return jsonify({"ok": True})


# ── Importación por lotes JSON (Solo Administrador) ───────────────────────
@app.route("/api/importar", methods=["POST"])
@admin_requerido
def importar():
    """Carga varios estudios a la vez desde un arreglo JSON con códigos de taxonomía."""
    payload = request.get_json(silent=True) or {}
    filas = payload.get("estudios")
    if not isinstance(filas, list) or not filas:
        return error("Envía un arreglo 'estudios' con al menos un registro.")

    creados, omitidos = 0, []
    with get_conn() as conn:
        int_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM intervenciones")}
        des_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM desenlaces")}
        for fila in filas:
            titulo = campo(fila, "titulo")
            if not titulo:
                omitidos.append(titulo or "(sin título)")
                continue
            codigo = campo(fila, "codigo") or siguiente_codigo(conn, "estudios", "E")
            try:
                cur = conn.execute(
                    f"INSERT INTO estudios {_COLS_INSERT} VALUES ({','.join('?' * 25)})",
                    _vals_de(fila, codigo),
                )
            except sqlite3.IntegrityError:
                omitidos.append(titulo)
                continue
            eid = cur.lastrowid
            for cod in fila.get("intervenciones", []):
                if cod in int_ids:
                    conn.execute("INSERT OR IGNORE INTO estudio_intervencion VALUES (?,?)",
                                 (eid, int_ids[cod]))
            for cod in fila.get("desenlaces", []):
                if cod in des_ids:
                    conn.execute("INSERT OR IGNORE INTO estudio_desenlace VALUES (?,?)",
                                 (eid, des_ids[cod]))
            creados += 1

    return jsonify({"ok": True, "creados": creados, "omitidos": omitidos})


# ── Importación masiva desde Excel (Solo Administrador) ────────────────────
@app.route("/api/importar-excel", methods=["POST"])
@admin_requerido
def importar_excel():
    """Carga estudios desde un archivo Excel (.xlsx) con columnas estándar o formatos de insumos.
    Mapea automáticamente a la taxonomía (intervenciones y desenlaces).
    """
    try:
        import openpyxl
    except ImportError:
        return error("El módulo 'openpyxl' no está instalado en el servidor.", 500)

    archivo = request.files.get("archivo")
    if not archivo:
        return error("No se recibió ningún archivo.")

    nombre = archivo.filename or ""
    if not nombre.lower().endswith(".xlsx"):
        return error("El archivo debe ser un .xlsx (Excel).")

    try:
        wb = openpyxl.load_workbook(io.BytesIO(archivo.read()), read_only=True, data_only=True)
    except Exception:
        return error("No fue posible leer el archivo Excel. Verifica el formato.")

    # Usar la primera hoja con contenido
    ws = wb.active
    for sname in wb.sheetnames:
        sheet = wb[sname]
        if sheet.max_row and sheet.max_row > 1:
            ws = sheet
            break

    # Mapeo dinámico de encabezados para soportar Extraction_Matrix y archivos de insumos
    iter_filas = ws.iter_rows(values_only=True)
    encabezados = next(iter_filas, None)
    if not encabezados:
        wb.close()
        return error("El archivo Excel no contiene datos o está vacío.")

    def _norm(s):
        if not s:
            return ""
        s = str(s).lower().strip()
        s = unicodedata.normalize("NFD", s)
        return re.sub(r"[\u0300-\u036f]", "", s)

    indices = {}
    for idx, celda in enumerate(encabezados):
        h = _norm(celda)
        if not h:
            continue
        if "intervenciones asignadas" in h or "codigos intervencion" in h:
            indices["intervenciones_asignadas"] = idx
        elif "desenlaces asignados" in h or "codigos desenlace" in h:
            indices["desenlaces_asignados"] = idx
        elif ("intervencion" in h or "cannabis" in h) and "asignad" not in h and "intervencion_texto" not in indices:
            indices["intervencion_texto"] = idx
        elif "desenlace" in h and "asignad" not in h and "desenlaces_texto" not in indices:
            indices["desenlaces_texto"] = idx
        elif "indicacion" in h and "dominio" not in h and "indicacion" not in indices:
            indices["indicacion"] = idx
        elif "dominio" in h and "dominio_indicacion" not in indices:
            indices["dominio_indicacion"] = idx
        elif ("titulo" in h or "title" in h) and "titulo" not in indices:
            indices["titulo"] = idx
        elif ("primer autor" in h or h.startswith("autor") or h == "autores" or "author" in h) and "autores" not in indices:
            indices["autores"] = idx
        elif ("an" in h and ("io" in h or "o" in h or "year" in h)) and "anio" not in indices:
            indices["anio"] = idx
        elif ("revista" in h or "fuente" in h or "journal" in h or "source" in h) and "fuente" not in indices:
            indices["fuente"] = idx
        elif "volumen" in h and "volumen" not in indices:
            indices["volumen"] = idx
        elif ("numero" in h or "issue" in h) and "numero" not in indices:
            indices["numero"] = idx
        elif "doi" in h and "doi" not in indices:
            indices["doi"] = idx
        elif ("tipo de estudio" in h or "diseno" in h or "study type" in h) and "tipo_estudio" not in indices:
            indices["tipo_estudio"] = idx
        elif "poblacion" in h and "poblacion_especial" not in indices:
            indices["poblacion_especial"] = idx
        elif ("abstract" in h or "resumen" in h) and "abstract" not in indices:
            indices["abstract"] = idx
        elif ("id del estudio" in h or "id estudio" in h or h == "id" or "id excel" in h) and "id_excel" not in indices:
            indices["id_excel"] = idx

    def _val(row, clave, por_defecto=""):
        idx = indices.get(clave)
        if idx is not None and idx < len(row):
            v = row[idx]
            return str(v).strip() if v is not None else por_defecto
        return por_defecto

    creados, omitidos = 0, []
    with get_conn() as conn:
        int_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM intervenciones")}
        des_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM desenlaces")}

        for row in iter_filas:
            if not row or all(c is None for c in row):
                continue

            titulo = _val(row, "titulo")
            if not titulo and len(row) > 3 and row[3]:
                titulo = str(row[3]).strip()

            if not titulo:
                omitidos.append("(fila sin título)")
                continue

            tipo_estudio = _val(row, "tipo_estudio") or (str(row[8]).strip() if len(row) > 8 and row[8] else "Revisión sistemática")
            codigo = siguiente_codigo(conn, "estudios", "E")

            fila_datos = {
                "titulo": titulo,
                "id_excel": entero_o_nulo(_val(row, "id_excel") or (row[0] if len(row) > 0 else None)),
                "autores": _val(row, "autores") or (str(row[1]).strip() if len(row) > 1 and row[1] else ""),
                "anio": entero_o_nulo(_val(row, "anio") or (row[2] if len(row) > 2 else None)),
                "fuente": _val(row, "fuente") or (str(row[4]).strip() if len(row) > 4 and row[4] else ""),
                "volumen": _val(row, "volumen") or (str(row[5]).strip() if len(row) > 5 and row[5] else ""),
                "numero": _val(row, "numero") or (str(row[6]).strip() if len(row) > 6 and row[6] else ""),
                "doi": _val(row, "doi") or (str(row[7]).strip() if len(row) > 7 and row[7] else ""),
                "tipo_estudio": tipo_estudio,
                "poblacion_especial": _val(row, "poblacion_especial") or (str(row[9]).strip() if len(row) > 9 and row[9] else ""),
                "dominio_indicacion": _val(row, "dominio_indicacion") or (str(row[10]).strip() if len(row) > 10 and row[10] else ""),
                "indicacion": _val(row, "indicacion") or (str(row[11]).strip() if len(row) > 11 and row[11] else ""),
                "intervencion_texto": _val(row, "intervencion_texto") or (str(row[12]).strip() if len(row) > 12 and row[12] else ""),
                "desenlaces_texto": _val(row, "desenlaces_texto") or (str(row[13]).strip() if len(row) > 13 and row[13] else ""),
                "abstract": _val(row, "abstract") or (str(row[14]).strip() if len(row) > 14 and row[14] else ""),
            }

            try:
                cur = conn.execute(
                    f"INSERT INTO estudios {_COLS_INSERT} VALUES ({','.join('?' * 25)})",
                    _vals_de(fila_datos, codigo),
                )
                eid = cur.lastrowid
                creados += 1

                # Determinar códigos de intervención y desenlace
                cods_int_str = _val(row, "intervenciones_asignadas")
                cods_des_str = _val(row, "desenlaces_asignados")
                cods_int = [c.strip() for c in cods_int_str.split(",") if c.strip()] if cods_int_str else []
                cods_des = [c.strip() for c in cods_des_str.split(",") if c.strip()] if cods_des_str else []

                if not cods_int or not cods_des:
                    m_int, m_des = mapear_estudio(fila_datos)
                    if not cods_int:
                        cods_int = m_int
                    if not cods_des:
                        cods_des = m_des

                for cod in cods_int:
                    if cod in int_ids:
                        conn.execute("INSERT OR IGNORE INTO estudio_intervencion VALUES (?,?)", (eid, int_ids[cod]))
                for cod in cods_des:
                    if cod in des_ids:
                        conn.execute("INSERT OR IGNORE INTO estudio_desenlace VALUES (?,?)", (eid, des_ids[cod]))

            except sqlite3.IntegrityError:
                omitidos.append(titulo[:80])

    wb.close()
    return jsonify({"ok": True, "creados": creados, "omitidos": omitidos})


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=bool(os.environ.get("DEBUG")))
