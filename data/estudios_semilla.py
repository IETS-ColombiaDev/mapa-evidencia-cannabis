"""
Datos del Mapa de Evidencia en Cannabis Medicinal — IETS.

Los estudios se cargan desde el archivo JSON generado a partir de la
Extraction Matrix definitiva (203 registros). La normativa colombiana
se mantiene como constante de Python.

Cada estudio tiene los siguientes campos (tomados del Excel original):
    id_excel, titulo, autores, anio, fuente, volumen, numero, doi,
    tipo_estudio, poblacion_especial, dominio_indicacion, indicacion,
    intervencion_texto, desenlaces_texto, abstract
"""

import json
import os

_BASE = os.path.dirname(os.path.abspath(__file__))
_JSON_PATH = os.path.join(_BASE, "estudios_seed.json")


def cargar_estudios():
    """Lee el JSON de estudios y les asigna un código E001, E002, …"""
    with open(_JSON_PATH, encoding="utf-8") as f:
        filas = json.load(f)
    estudios = []
    for i, r in enumerate(filas, start=1):
        estudios.append({
            "codigo": f"E{str(i).zfill(3)}",
            "id_excel": r.get("id"),
            "titulo": (r.get("titulo") or "").strip(),
            "autores": (r.get("autor") or "").strip(),
            "anio": r.get("anio"),
            "fuente": (r.get("revista") or "").strip(),
            "volumen": (r.get("volumen") or "").strip(),
            "numero": (r.get("numero") or "").strip(),
            "doi": (r.get("doi") or "").strip(),
            "tipo_estudio": (r.get("tipo_estudio") or "").strip(),
            "poblacion_especial": (r.get("poblacion_especial") or "").strip(),
            "dominio_indicacion": (r.get("dominio_indicacion") or "").strip(),
            "indicacion": (r.get("indicacion") or "").strip(),
            "intervencion_texto": (r.get("intervencion") or "").strip(),
            "desenlaces_texto": (r.get("desenlaces") or "").strip(),
            "abstract": (r.get("abstract") or "").strip(),
        })
    return estudios


# Marco normativo colombiano — se muestra en la pestaña "Acerca del mapa".
NORMATIVA_COLOMBIA = [
    dict(
        norma="Ley 1787 de 2016",
        descripcion=(
            "Crea el marco regulatorio para el acceso seguro e informado al uso médico y "
            "científico del cannabis y sus derivados en el territorio nacional."
        ),
        url="https://compilacionmsf.ica.gov.co:4443/compilacion/docs/pdf/ley_1787_2016.pdf",
    ),
    dict(
        norma="Decreto 613 de 2017",
        descripcion=(
            "Reglamenta la Ley 1787 de 2016 y define el régimen inicial de licencias, con "
            "vigencia de cinco años y un límite de veinte plantas para autocultivo."
        ),
        url="https://www.invima.gov.co/biblioteca/preview/122395",
    ),
    dict(
        norma="Decreto Ley 2106 de 2019",
        descripcion=(
            "Traslada al Invima la competencia para expedir las licencias de fabricación de "
            "derivados de cannabis con fines medicinales y científicos."
        ),
        url="",
    ),
    dict(
        norma="Decreto 811 de 2021",
        descripcion=(
            "Sustituye el Título 11 de la Parte 8 del Libro 2 del Decreto 780 de 2016 y "
            "reordena el acceso al uso del cannabis y de la planta de cannabis."
        ),
        url="https://www.dmsjuridica.com/buscador_20179478954/legislacion/decretos/2023/08/23/decreto-811-de-2021/?pdf=55295",
    ),
    dict(
        norma="Resolución conjunta 227 de 2022",
        descripcion=(
            "Reglamenta el Decreto 811 de 2021: procedimiento de licencias, cupos, condiciones "
            "de seguridad, contenido del proyecto de investigación y régimen sancionatorio."
        ),
        url="https://www.invima.gov.co/biblioteca/download/131359",
    ),
]
