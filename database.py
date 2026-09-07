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
from data.estudios_semilla import ESTUDIOS, NORMATIVA_COLOMBIA

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
}
TIPOS_PRIMARIO = {
    "Ensayo clínico aleatorizado",
    "Ensayo clínico no aleatorizado",
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
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo          TEXT UNIQUE NOT NULL,
    titulo          TEXT NOT NULL,
    autores         TEXT DEFAULT '',
    anio            INTEGER,
    fuente          TEXT DEFAULT '',
    tipo_estudio    TEXT NOT NULL,
    poblacion       TEXT DEFAULT 'Mixta',
    ambito          TEXT DEFAULT 'Global',
    pais            TEXT DEFAULT '',
    certeza         TEXT DEFAULT 'No evaluada',
    hallazgo        TEXT DEFAULT 'No concluyente',
    n_participantes INTEGER,
    doi             TEXT DEFAULT '',
    url             TEXT DEFAULT '',
    resumen         TEXT DEFAULT '',
    estado          TEXT DEFAULT 'Por verificar',
    creado_en       TEXT DEFAULT (datetime('now')),
    actualizado_en  TEXT DEFAULT (datetime('now'))
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

CREATE INDEX IF NOT EXISTS idx_ei_estudio ON estudio_intervencion(estudio_id);
CREATE INDEX IF NOT EXISTS idx_ed_estudio ON estudio_desenlace(estudio_id);
CREATE INDEX IF NOT EXISTS idx_estudios_anio ON estudios(anio);
"""


def init_db(force: bool = False) -> None:
    """Crea el esquema y carga los datos iniciales si la base está vacía."""
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with get_conn() as conn:
        conn.executescript(SCHEMA)
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

    int_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM intervenciones")}
    des_ids = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM desenlaces")}

    for e in ESTUDIOS:
        cur = conn.execute(
            """INSERT INTO estudios (codigo, titulo, autores, anio, fuente, tipo_estudio,
                                     poblacion, ambito, pais, certeza, hallazgo, n_participantes,
                                     doi, url, resumen, estado)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                e["codigo"], e["titulo"], e["autores"], e["anio"], e["fuente"], e["tipo_estudio"],
                e["poblacion"], e["ambito"], e["pais"], e["certeza"], e["hallazgo"],
                e.get("n_participantes"), e.get("doi", ""), e.get("url", ""), e["resumen"],
                "Por verificar",
            ),
        )
        eid = cur.lastrowid
        for cod in e["intervenciones"]:
            if cod in int_ids:
                conn.execute(
                    "INSERT OR IGNORE INTO estudio_intervencion VALUES (?,?)", (eid, int_ids[cod])
                )
        for cod in e["desenlaces"]:
            if cod in des_ids:
                conn.execute(
                    "INSERT OR IGNORE INTO estudio_desenlace VALUES (?,?)", (eid, des_ids[cod])
                )

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
