"""
Capa de datos del Mapa de Evidencia en Cannabis Medicinal — IETS.

SQLite con claves foráneas activas. La base se crea y se puebla la primera vez
que se ejecuta la aplicación; si el archivo ya existe, no se sobrescribe.
"""

import os
import sqlite3
from contextlib import contextmanager

from data.taxonomia import (
    CATEGORIAS_INTERVENCION,
    DESENLACES,
    DOMINIOS_DESENLACE,
    INTERVENCIONES,
)
from data.estudios_semilla import cargar_estudios, NORMATIVA_COLOMBIA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("MAPA_DB_PATH", os.path.join(BASE_DIR, "mapa_cannabis.db"))

# Tipos de estudio clasificados por eje del mapa.
TIPOS_SINTESIS = {
    "Revisión sistemática",
    "Revisión sistemática con metaanálisis",
    "Revisión de revisiones",
    "Revisión narrativa",
    "Mapa de evidencia",
    "Guía de práctica clínica",
    "Evaluación de tecnología sanitaria",
    "Revisión paraguas",
    "Revisión rápida",
    "Revisión de alcance",
    "Revisión viva",
}
TIPOS_PRIMARIO = {
    "Ensayo clínico aleatorizado",
    "Ensayo clínico no aleatorizado",
    "Ensayo clínico",
    "Estudio observacional",
    "Estudio cualitativo",
    "Evaluación económica",
    "Serie o reporte de casos",
}
TIPOS_ESTUDIO = sorted(TIPOS_SINTESIS | TIPOS_PRIMARIO)

CERTEZAS = ["Alta", "Moderada", "Baja", "Muy baja", "No evaluada"]
HALLAZGOS = ["Favorable", "Mixto", "Sin diferencia", "Desfavorable", "No concluyente"]
POBLACIONES = ["Adultos", "Pediátrica", "Adultos mayores", "Mixta"]
AMBITOS = ["Global", "América Latina", "Colombia", "Norteamérica", "Europa", "Asia", "Oceanía", "África"]
ESTADOS = ["Por verificar", "Verificada"]


def eje_de_tipo(tipo_estudio: str) -> str:
    """Devuelve el eje del mapa ('sintesis' o 'primario') para un tipo de estudio."""
    return "sintesis" if tipo_estudio in TIPOS_SINTESIS else "primario"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS categorias_intervencion (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT UNIQUE NOT NULL,
    nombre      TEXT NOT NULL,
    descripcion TEXT DEFAULT '',
    orden       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS intervenciones (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo       TEXT UNIQUE NOT NULL,
    categoria_id INTEGER NOT NULL REFERENCES categorias_intervencion(id) ON DELETE CASCADE,
    nombre       TEXT NOT NULL,
    descripcion  TEXT DEFAULT '',
    orden        INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS dominios_desenlace (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT UNIQUE NOT NULL,
    nombre      TEXT NOT NULL,
    descripcion TEXT DEFAULT '',
    orden       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS desenlaces (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT UNIQUE NOT NULL,
    dominio_id  INTEGER NOT NULL REFERENCES dominios_desenlace(id) ON DELETE CASCADE,
    nombre      TEXT NOT NULL,
    descripcion TEXT DEFAULT '',
    orden       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS estudios (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo              TEXT UNIQUE NOT NULL,
    id_excel            INTEGER,
    titulo              TEXT NOT NULL,
    autores             TEXT DEFAULT '',
    anio                INTEGER,
    fuente              TEXT DEFAULT '',
    volumen             TEXT DEFAULT '',
    numero              TEXT DEFAULT '',
    doi                 TEXT DEFAULT '',
    tipo_estudio        TEXT NOT NULL,
    poblacion           TEXT DEFAULT 'Mixta',
    ambito              TEXT DEFAULT 'Global',
    pais                TEXT DEFAULT '',
    certeza             TEXT DEFAULT 'No evaluada',
    hallazgo            TEXT DEFAULT 'No concluyente',
    n_participantes     INTEGER,
    url                 TEXT DEFAULT '',
    resumen             TEXT DEFAULT '',
    estado              TEXT DEFAULT 'Por verificar',
    poblacion_especial  TEXT DEFAULT '',
    dominio_indicacion  TEXT DEFAULT '',
    indicacion          TEXT DEFAULT '',
    intervencion_texto  TEXT DEFAULT '',
    desenlaces_texto    TEXT DEFAULT '',
    abstract            TEXT DEFAULT '',
    creado_en           TEXT DEFAULT (datetime('now')),
    actualizado_en      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS estudio_intervencion (
    estudio_id      INTEGER NOT NULL REFERENCES estudios(id) ON DELETE CASCADE,
    intervencion_id INTEGER NOT NULL REFERENCES intervenciones(id) ON DELETE CASCADE,
    PRIMARY KEY (estudio_id, intervencion_id)
);

CREATE TABLE IF NOT EXISTS estudio_desenlace (
    estudio_id   INTEGER NOT NULL REFERENCES estudios(id) ON DELETE CASCADE,
    desenlace_id INTEGER NOT NULL REFERENCES desenlaces(id) ON DELETE CASCADE,
    PRIMARY KEY (estudio_id, desenlace_id)
);

CREATE TABLE IF NOT EXISTS normativa (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    norma       TEXT NOT NULL,
    descripcion TEXT DEFAULT '',
    url         TEXT DEFAULT '',
    orden       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS usuarios (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre        TEXT DEFAULT 'Administrador',
    rol           TEXT DEFAULT 'admin',
    creado_en     TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS medicamentos_aprobados (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    orden               INTEGER DEFAULT 0,
    expediente          TEXT DEFAULT '',
    producto            TEXT NOT NULL,
    registro_sanitario  TEXT NOT NULL,
    fecha_expedicion    TEXT DEFAULT '',
    estado_registro     TEXT DEFAULT 'Vigente',
    principio_activo    TEXT NOT NULL,
    forma_farmaceutica  TEXT DEFAULT '',
    via_administracion  TEXT DEFAULT '',
    concentracion       TEXT DEFAULT '',
    atc                 TEXT DEFAULT '',
    descripcion_atc     TEXT DEFAULT '',
    relacion_cbd_thc    TEXT DEFAULT '',
    indicaciones        TEXT DEFAULT '',
    intervencion_codigo TEXT NOT NULL,
    desenlace_codigo    TEXT NOT NULL,
    creado_en           TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_ei_estudio ON estudio_intervencion(estudio_id);
CREATE INDEX IF NOT EXISTS idx_ed_estudio ON estudio_desenlace(estudio_id);
CREATE INDEX IF NOT EXISTS idx_estudios_anio ON estudios(anio);
CREATE INDEX IF NOT EXISTS idx_med_aprob_cruce ON medicamentos_aprobados(intervencion_codigo, desenlace_codigo);
"""


def asegurar_admin(conn: sqlite3.Connection) -> None:
    """Garantiza la existencia de al menos un usuario administrador."""
    n = conn.execute("SELECT COUNT(*) AS n FROM usuarios").fetchone()["n"]
    if n == 0:
        admin_user = os.environ.get("ADMIN_USER", "admin")
        admin_pass = os.environ.get("ADMIN_PASSWORD", "AdminIETS2025!")
        from werkzeug.security import generate_password_hash
        hash_clave = generate_password_hash(admin_pass)
        conn.execute(
            "INSERT INTO usuarios (username, password_hash, nombre, rol) VALUES (?, ?, ?, ?)",
            (admin_user, hash_clave, "Administrador IETS", "admin"),
        )


def verificar_usuario(username: str, clave: str) -> dict | None:
    """Verifica credenciales de un usuario y retorna sus datos o None si son inválidas."""
    if not username or not clave:
        return None
    from werkzeug.security import check_password_hash
    with get_conn() as conn:
        fila = conn.execute(
            "SELECT id, username, password_hash, nombre, rol FROM usuarios WHERE LOWER(username) = LOWER(?)",
            (username.strip(),),
        ).fetchone()
        if fila and check_password_hash(fila["password_hash"], clave):
            return {
                "id": fila["id"],
                "username": fila["username"],
                "nombre": fila["nombre"],
                "rol": fila["rol"],
            }
    return None


def crear_usuario(username: str, clave: str, nombre: str = "Administrador", rol: str = "admin") -> bool:
    """Crea o actualiza un usuario administrador."""
    from werkzeug.security import generate_password_hash
    hash_clave = generate_password_hash(clave)
    with get_conn() as conn:
        try:
            conn.execute(
                """INSERT INTO usuarios (username, password_hash, nombre, rol)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(username) DO UPDATE SET password_hash = excluded.password_hash, nombre = excluded.nombre""",
                (username.strip(), hash_clave, nombre.strip(), rol.strip()),
            )
            return True
        except Exception:
            return False


def asegurar_medicamentos_aprobados(conn: sqlite3.Connection) -> None:
    """Garantiza la existencia y poblamiento de la tabla medicamentos_aprobados (INVIMA)."""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos_aprobados (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        orden               INTEGER DEFAULT 0,
        expediente          TEXT DEFAULT '',
        producto            TEXT NOT NULL,
        registro_sanitario  TEXT NOT NULL,
        fecha_expedicion    TEXT DEFAULT '',
        estado_registro     TEXT DEFAULT 'Vigente',
        principio_activo    TEXT NOT NULL,
        forma_farmaceutica  TEXT DEFAULT '',
        via_administracion  TEXT DEFAULT '',
        concentracion       TEXT DEFAULT '',
        atc                 TEXT DEFAULT '',
        descripcion_atc     TEXT DEFAULT '',
        relacion_cbd_thc    TEXT DEFAULT '',
        indicaciones        TEXT DEFAULT '',
        intervencion_codigo TEXT NOT NULL,
        desenlace_codigo    TEXT NOT NULL,
        creado_en           TEXT DEFAULT (datetime('now'))
    );
    """)
    n = conn.execute("SELECT COUNT(*) AS n FROM medicamentos_aprobados").fetchone()["n"]
    if n == 0:
        from data.medicamentos_invima import cargar_medicamentos_invima
        items = cargar_medicamentos_invima()
        for item in items:
            conn.execute(
                """INSERT INTO medicamentos_aprobados (
                    orden, expediente, producto, registro_sanitario, fecha_expedicion,
                    estado_registro, principio_activo, forma_farmaceutica, via_administracion,
                    concentracion, atc, descripcion_atc, relacion_cbd_thc, indicaciones,
                    intervencion_codigo, desenlace_codigo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item.get("orden", 0),
                    item.get("expediente", ""),
                    item.get("producto", ""),
                    item.get("registro_sanitario", ""),
                    item.get("fecha_expedicion", ""),
                    item.get("estado_registro", "Vigente"),
                    item.get("principio_activo", ""),
                    item.get("forma_farmaceutica", ""),
                    item.get("via_administracion", ""),
                    item.get("concentracion", ""),
                    item.get("atc", ""),
                    item.get("descripcion_atc", ""),
                    item.get("relacion_cbd_thc", ""),
                    item.get("indicaciones", ""),
                    item.get("intervencion_codigo", ""),
                    item.get("desenlace_codigo", ""),
                ),
            )


def init_db(force: bool = False) -> None:
    """Crea el esquema y carga los datos iniciales si la base está vacía."""
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with get_conn() as conn:
        conn.executescript(SCHEMA)
        asegurar_admin(conn)
        asegurar_medicamentos_aprobados(conn)
        ya_tiene_datos = conn.execute("SELECT COUNT(*) AS n FROM estudios").fetchone()["n"] > 0
        if ya_tiene_datos:
            return
        _sembrar(conn)


def _sembrar(conn: sqlite3.Connection) -> None:
    for cat in CATEGORIAS_INTERVENCION:
        conn.execute(
            "INSERT OR IGNORE INTO categorias_intervencion (codigo, nombre, descripcion, orden)"
            " VALUES (?,?,?,?)",
            (cat["codigo"], cat["nombre"], cat["descripcion"], cat["orden"]),
        )

    cat_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM categorias_intervencion")}
    for codigo, cat_cod, nombre, desc, orden in INTERVENCIONES:
        conn.execute(
            "INSERT OR IGNORE INTO intervenciones (codigo, categoria_id, nombre, descripcion, orden)"
            " VALUES (?,?,?,?,?)",
            (codigo, cat_ids[cat_cod], nombre, desc, orden),
        )

    for dom in DOMINIOS_DESENLACE:
        conn.execute(
            "INSERT OR IGNORE INTO dominios_desenlace (codigo, nombre, descripcion, orden)"
            " VALUES (?,?,?,?)",
            (dom["codigo"], dom["nombre"], dom["descripcion"], dom["orden"]),
        )

    dom_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM dominios_desenlace")}
    for codigo, dom_cod, nombre, desc, orden in DESENLACES:
        conn.execute(
            "INSERT OR IGNORE INTO desenlaces (codigo, dominio_id, nombre, descripcion, orden)"
            " VALUES (?,?,?,?,?)",
            (codigo, dom_ids[dom_cod], nombre, desc, orden),
        )

    # Cargar estudios desde el JSON y crear vínculos con la taxonomía
    from data.mapeo_taxonomia import mapear_estudio

    estudios = cargar_estudios()
    int_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM intervenciones")}
    des_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM desenlaces")}

    for e in estudios:
        try:
            cur = conn.execute(
                """INSERT INTO estudios (codigo, id_excel, titulo, autores, anio, fuente,
                                         volumen, numero, doi, tipo_estudio, poblacion,
                                         ambito, pais, certeza, hallazgo, n_participantes,
                                         url, resumen, estado, poblacion_especial,
                                         dominio_indicacion, indicacion, intervencion_texto,
                                         desenlaces_texto, abstract)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    e["codigo"], e.get("id_excel"), e["titulo"], e["autores"], e["anio"],
                    e["fuente"], e.get("volumen", ""), e.get("numero", ""), e.get("doi", ""),
                    e["tipo_estudio"], "Mixta", "Global", "",
                    "No evaluada", "No concluyente", None,
                    "", "", "Por verificar",
                    e.get("poblacion_especial", ""),
                    e.get("dominio_indicacion", ""),
                    e.get("indicacion", ""),
                    e.get("intervencion_texto", ""),
                    e.get("desenlaces_texto", ""),
                    e.get("abstract", ""),
                ),
            )
            eid = cur.lastrowid

            # Mapear automáticamente a la taxonomía usando los campos de texto
            codigos_int, codigos_des = mapear_estudio(e)
            for cod in codigos_int:
                if cod in int_ids:
                    conn.execute(
                        "INSERT OR IGNORE INTO estudio_intervencion VALUES (?,?)",
                        (eid, int_ids[cod]),
                    )
            for cod in codigos_des:
                if cod in des_ids:
                    conn.execute(
                        "INSERT OR IGNORE INTO estudio_desenlace VALUES (?,?)",
                        (eid, des_ids[cod]),
                    )
        except sqlite3.IntegrityError:
            pass  # Skip duplicates

    for i, n in enumerate(NORMATIVA_COLOMBIA, start=1):
        conn.execute(
            "INSERT INTO normativa (norma, descripcion, url, orden) VALUES (?,?,?,?)",
            (n["norma"], n["descripcion"], n["url"], i),
        )


def siguiente_codigo(conn: sqlite3.Connection, tabla: str, prefijo: str) -> str:
    """Genera el siguiente código consecutivo del tipo E056, I14, O16."""
    filas = conn.execute(f"SELECT codigo FROM {tabla}").fetchall()
    maximo = 0
    for f in filas:
        cod = f["codigo"] or ""
        if cod.startswith(prefijo) and cod[len(prefijo):].isdigit():
            maximo = max(maximo, int(cod[len(prefijo):]))
    ancho = 3 if prefijo == "E" else 1
    return f"{prefijo}{str(maximo + 1).zfill(ancho)}"


if __name__ == "__main__":
    init_db(force=True)
    with get_conn() as c:
        print("Estudios cargados:", c.execute("SELECT COUNT(*) FROM estudios").fetchone()[0])
        print("Intervenciones:", c.execute("SELECT COUNT(*) FROM intervenciones").fetchone()[0])
        print("Desenlaces:", c.execute("SELECT COUNT(*) FROM desenlaces").fetchone()[0])
