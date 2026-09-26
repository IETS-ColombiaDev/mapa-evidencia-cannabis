"""
Mapa de Evidencia en Cannabis Medicinal — IETS
Aplicación Flask con base de datos SQLite.

Rutas públicas:
    /              mapa de evidencia
    /admin         panel de administración (sin autenticación en esta versión)

API:
    GET    /api/datos                  estructura + estudios (fuente única del mapa)
    GET    /api/catalogos              listas controladas para los formularios
    POST   /api/estudios               crear estudio
    PUT    /api/estudios/<id>          actualizar estudio
    DELETE /api/estudios/<id>          eliminar estudio
    POST   /api/intervenciones         crear intervención     (idem PUT / DELETE)
    POST   /api/desenlaces             crear desenlace        (idem PUT / DELETE)
    POST   /api/categorias             crear categoría        (idem PUT / DELETE)
    POST   /api/dominios               crear dominio          (idem PUT / DELETE)
    POST   /api/importar               carga masiva desde JSON
    POST   /api/importar-excel         carga masiva desde archivo Excel (.xlsx)
"""

import io
import sqlite3

from flask import Flask, jsonify, render_template, request

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
)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

init_db()


# ── Utilidades ─────────────────────────────────────────────────────────────
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


# ── Vistas ─────────────────────────────────────────────────────────────────
@app.route("/")
def vista_mapa():
    return render_template("index.html")


@app.route("/admin")
def vista_admin():
    return render_template("admin.html")


@app.route("/api/salud")
def salud():
    with get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM estudios").fetchone()["n"]
    return jsonify({"ok": True, "estudios": n})


# ── Lectura ────────────────────────────────────────────────────────────────
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

    return jsonify({
        "ok": True,
        "categorias": categorias,
        "intervenciones": intervenciones,
        "dominios": dominios,
        "desenlaces": desenlaces,
        "estudios": estudios,
        "normativa": normativa,
    })


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


# ── Estudios ───────────────────────────────────────────────────────────────
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
        campo(d, "poblacion", "Mixta"),
        campo(d, "ambito", "Global"),
        campo(d, "pais"),
        campo(d, "certeza", "No evaluada"),
        campo(d, "hallazgo", "No concluyente"),
        entero_o_nulo(d.get("n_participantes")),
        campo(d, "url"),
        campo(d, "resumen"),
        campo(d, "estado", estado_defecto),
        campo(d, "poblacion_especial"),
        campo(d, "dominio_indicacion"),
        campo(d, "indicacion"),
        campo(d, "intervencion_texto"),
        campo(d, "desenlaces_texto"),
        campo(d, "abstract"),
    )


@app.route("/api/estudios", methods=["POST"])
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
def eliminar_estudio(estudio_id):
    with get_conn() as conn:
        fila = conn.execute("SELECT codigo FROM estudios WHERE id = ?", (estudio_id,)).fetchone()
        if not fila:
            return error("No se encontró el estudio.", 404)
        conn.execute("DELETE FROM estudios WHERE id = ?", (estudio_id,))
    return jsonify({"ok": True, "codigo": fila["codigo"]})


# ── Taxonomía: intervenciones, desenlaces, categorías y dominios ───────────
@app.route("/api/intervenciones", methods=["POST"])
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
def eliminar_intervencion(iid):
    with get_conn() as conn:
        usos = conn.execute(
            "SELECT COUNT(*) AS n FROM estudio_intervencion WHERE intervencion_id=?", (iid,)
        ).fetchone()["n"]
        conn.execute("DELETE FROM intervenciones WHERE id=?", (iid,))
    return jsonify({"ok": True, "vinculos_eliminados": usos})


@app.route("/api/desenlaces", methods=["POST"])
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
def eliminar_desenlace(did):
    with get_conn() as conn:
        usos = conn.execute(
            "SELECT COUNT(*) AS n FROM estudio_desenlace WHERE desenlace_id=?", (did,)
        ).fetchone()["n"]
        conn.execute("DELETE FROM desenlaces WHERE id=?", (did,))
    return jsonify({"ok": True, "vinculos_eliminados": usos})


@app.route("/api/categorias", methods=["POST"])
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


# ── Importación por lotes (JSON) ──────────────────────────────────────────
@app.route("/api/importar", methods=["POST"])
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
            tipo = campo(fila, "tipo_estudio")
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


# ── Importación masiva desde Excel ─────────────────────────────────────────
@app.route("/api/importar-excel", methods=["POST"])
def importar_excel():
    """Carga estudios desde un archivo Excel (.xlsx) con las columnas de la matriz de extracción.

    Columnas esperadas (por posición):
        A: ID | B: Autor | C: Año | D: Título | E: Revista | F: Volumen | G: Número
        H: DOI | I: Tipo de estudio | J: Población especial
        K: Dominio general de la indicación clínica | L: Indicación
        M: Intervención con cannabis | N: Desenlaces evaluados | O: Abstract
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

    # Use first sheet
    ws = wb.active

    creados, omitidos = 0, []
    with get_conn() as conn:
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is None and row[3] is None:
                continue  # skip empty rows

            titulo = str(row[3]).strip() if row[3] else ""
            tipo_estudio = str(row[8]).strip() if row[8] else ""
            if not titulo:
                omitidos.append("(sin título)")
                continue

            codigo = siguiente_codigo(conn, "estudios", "E")
            fila_datos = {
                "titulo": titulo,
                "id_excel": row[0],
                "autores": str(row[1]).strip() if row[1] else "",
                "anio": row[2],
                "fuente": str(row[4]).strip() if row[4] else "",
                "volumen": str(row[5]).strip() if row[5] else "",
                "numero": str(row[6]).strip() if row[6] else "",
                "doi": str(row[7]).strip() if row[7] else "",
                "tipo_estudio": tipo_estudio,
                "poblacion_especial": str(row[9]).strip() if row[9] else "",
                "dominio_indicacion": str(row[10]).strip() if row[10] and len(row) > 10 else "",
                "indicacion": str(row[11]).strip() if row[11] and len(row) > 11 else "",
                "intervencion_texto": str(row[12]).strip() if row[12] and len(row) > 12 else "",
                "desenlaces_texto": str(row[13]).strip() if row[13] and len(row) > 13 else "",
                "abstract": str(row[14]).strip() if len(row) > 14 and row[14] else "",
            }

            try:
                conn.execute(
                    f"INSERT INTO estudios {_COLS_INSERT} VALUES ({','.join('?' * 25)})",
                    _vals_de(fila_datos, codigo),
                )
                creados += 1
            except sqlite3.IntegrityError:
                omitidos.append(titulo[:80])

    wb.close()
    return jsonify({"ok": True, "creados": creados, "omitidos": omitidos})


if __name__ == "__main__":
    import os
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=bool(os.environ.get("DEBUG")))
