"""
Módulo para la carga y gestión de medicamentos aprobados por el INVIMA en Colombia
relacionados con cannabis medicinal.

Fuente: insumos/Medicamentos aprobados INVIMA (1).xlsx
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_EXCEL_DEFAULT = os.path.join(BASE_DIR, "insumos", "Medicamentos aprobados INVIMA (1).xlsx")

# Semilla fija de respaldo con los 9 medicamentos vigentes registrados ante el INVIMA
MEDICAMENTOS_INVIMA_SEED = [
    {
        "orden": 1,
        "expediente": "20098801",
        "producto": "Sativex®",
        "registro_sanitario": "INVIMA 2022M-0017373-R1",
        "fecha_expedicion": "2016-09-28",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol (CBD) 25 mg/ml + Delta-9-tetrahidrocannabinol (THC) 27 mg/ml",
        "forma_farmaceutica": "Solución bucal",
        "via_administracion": "Bucal / Oromucosa",
        "concentracion": "25 mg/ml CBD, 27 mg/ml THC",
        "atc": "N02BG10",
        "descripcion_atc": "Cannabinoides",
        "relacion_cbd_thc": "Aproximadamente 1:1 CBD:THC",
        "indicaciones": (
            "Tratamiento coadyuvante para la mejoría de los síntomas en pacientes con espasticidad "
            "moderada o grave debida a la esclerosis múltiple (EM) que no han respondido de forma "
            "adecuada a otros medicamentos antiespásticos y que han mostrado una mejoría clínicamente "
            "significativa de los síntomas relacionados con la espasticidad durante un período inicial "
            "de prueba del tratamiento."
        ),
        "intervencion_codigo": "I2",
        "desenlace_codigo": "O2",
    },
    {
        "orden": 2,
        "expediente": "20147754",
        "producto": "Neviot®",
        "registro_sanitario": "INVIMA 2020M-0019590",
        "fecha_expedicion": "2020-02-24",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol",
        "forma_farmaceutica": "Solución oral",
        "via_administracion": "Oral",
        "concentracion": "10 g/100 ml",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Indicado para el tratamiento complementario de crisis asociadas con síndrome de Lennox-Gastaut (SLG), "
            "síndrome de Dravet (SD) o el complejo de esclerosis tuberosa (CET) en pacientes a partir de 1 año de edad."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 3,
        "expediente": "20197216",
        "producto": "Cannepi® solución oral",
        "registro_sanitario": "INVIMA 2023M-0021102",
        "fecha_expedicion": "2023-10-23",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol",
        "forma_farmaceutica": "Solución oral",
        "via_administracion": "Oral",
        "concentracion": "10 g/100 ml",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Tratamiento adyuvante de las convulsiones asociadas con el síndrome de Lennox-Gastaut (SLG), "
            "síndrome de Dravet (SD) en pacientes de 2 o más años de edad que no han respondido a combinaciones "
            "convencionales de terapias anticonvulsivas quienes persisten con 2 o más episodios convulsivos por semana. "
            "Complejo de esclerosis tuberosa (CET) en pacientes a partir de 1 año de edad. Diagnósticos confirmados por especialista."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 4,
        "expediente": "20198801",
        "producto": "Neviot® 100 mg cápsula blanda",
        "registro_sanitario": "INVIMA 2022M-0020699",
        "fecha_expedicion": "2022-07-08",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol",
        "forma_farmaceutica": "Cápsula blanda",
        "via_administracion": "Oral",
        "concentracion": "100 mg",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Tratamiento adyuvante de las convulsiones asociadas con el síndrome de Lennox-Gastaut (LGS) y el "
            "síndrome de Dravet (SD) en pacientes de 2 o más años de edad que puedan deglutir cápsulas y no han respondido "
            "a combinaciones convencionales de terapias anticonvulsivas quienes persisten con 2 o más episodios convulsivos por semana."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 5,
        "expediente": "20200273",
        "producto": "Neviot® 200 mg cápsula blanda",
        "registro_sanitario": "INVIMA 2022M-0020700",
        "fecha_expedicion": "2022-07-08",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol",
        "forma_farmaceutica": "Cápsula blanda",
        "via_administracion": "Oral",
        "concentracion": "200 mg",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Tratamiento adyuvante de las convulsiones asociadas con el síndrome de Lennox-Gastaut (LGS) y el "
            "síndrome de Dravet (SD) en pacientes de 2 o más años de edad que puedan deglutir cápsulas y no han respondido "
            "a combinaciones convencionales de terapias anticonvulsivas quienes persisten con 2 o más episodios convulsivos por semana."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 6,
        "expediente": "20215366",
        "producto": "Trunerox®",
        "registro_sanitario": "INVIMA 2024M-0021290",
        "fecha_expedicion": "2024-02-09",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol (CBD)",
        "forma_farmaceutica": "Solución oral",
        "via_administracion": "Oral",
        "concentracion": "100 mg/ml",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Tratamiento adyuvante de las convulsiones asociadas con el síndrome de Lennox-Gastaut (LGS) y el "
            "síndrome de Dravet (SD) en pacientes de 2 o más años de edad que no han respondido a combinaciones convencionales "
            "de terapias anticonvulsivas quienes persisten con 2 o más episodios convulsivos por semana."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 7,
        "expediente": "20236218",
        "producto": "Remsol®",
        "registro_sanitario": "INVIMA 2023M-0021185",
        "fecha_expedicion": "2023-12-04",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol CBD cristales",
        "forma_farmaceutica": "Solución oral",
        "via_administracion": "Oral",
        "concentracion": "10 g/100 ml",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Indicado para el tratamiento de las convulsiones asociadas con el síndrome de Lennox-Gastaut (LGS), "
            "el síndrome de Dravet (SD) o el complejo de esclerosis tuberosa (CET) en pacientes de 1 año de edad o mayores."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 8,
        "expediente": "20262841",
        "producto": "Animox® 100 mg/ml solución oral",
        "registro_sanitario": "INVIMA 2025M-0021731",
        "fecha_expedicion": "2025-01-23",
        "estado_registro": "Vigente",
        "principio_activo": "Cannabidiol",
        "forma_farmaceutica": "Solución oral",
        "via_administracion": "Oral",
        "concentracion": "100 mg/ml",
        "atc": "N03AX24",
        "descripcion_atc": "Cannabidiol",
        "relacion_cbd_thc": "CBD",
        "indicaciones": (
            "Tratamiento adyuvante de las convulsiones asociadas con el síndrome de Lennox-Gastaut (LGS) y el "
            "síndrome de Dravet (SD) en pacientes de 2 o más años de edad que no han respondido a combinaciones convencionales "
            "de terapias anticonvulsivas quienes persisten con 2 o más episodios convulsivos por semana."
        ),
        "intervencion_codigo": "I1",
        "desenlace_codigo": "O4",
    },
    {
        "orden": 9,
        "expediente": "20233134",
        "producto": "Laxenol® 5 mg",
        "registro_sanitario": "INVIMA 2025M-0022380",
        "fecha_expedicion": "2025-10-08",
        "estado_registro": "Vigente",
        "principio_activo": "Dronabinol en aceite de sésamo equivalente a dronabinol",
        "forma_farmaceutica": "Cápsula blanda",
        "via_administracion": "Oral",
        "concentracion": "5 mg",
        "atc": "A04AD10",
        "descripcion_atc": "Dronabinol",
        "relacion_cbd_thc": "THC (sintético)",
        "indicaciones": (
            "Indicado en adultos para el tratamiento de náuseas y vómitos asociados con la quimioterapia "
            "contra el cáncer en pacientes que no han respondido adecuadamente a los tratamientos antieméticos convencionales."
        ),
        "intervencion_codigo": "I3",
        "desenlace_codigo": "O3",
    },
]


def mapear_intervencion_desenlace(producto: str, principio: str, indicacion: str) -> tuple[str, str]:
    """Determina los códigos de intervención y desenlace en la taxonomía del mapa."""
    p = (producto or "").lower()
    pr = (principio or "").lower()
    ind = (indicacion or "").lower()

    if "sativex" in p or "espasticidad" in ind:
        return "I2", "O2"
    if "dronabinol" in pr or "laxenol" in p or "vmit" in ind or "vomit" in ind or "nause" in ind:
        return "I3", "O3"
    if "cannabidiol" in pr or "lennox" in ind or "dravet" in ind or "cet" in ind or "convulsi" in ind or "epilep" in ind:
        return "I1", "O4"
    return "", ""


def limpiar_texto(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor)
    texto = texto.replace("_x000D_", "").replace("_x0002_", "")
    texto = re.sub(r"[ \t]+", " ", texto)
    return texto.strip()


def limpiar_fecha(valor) -> str:
    if valor is None:
        return ""
    s = str(valor).strip()
    return s[:10]


def cargar_medicamentos_invima(ruta_excel: str | None = None) -> list[dict]:
    """
    Lee el archivo Excel de medicamentos aprobados por INVIMA si existe.
    Si no existe o falla la lectura, devuelve la semilla oficial precargada.
    """
    ruta = ruta_excel or RUTA_EXCEL_DEFAULT
    if not os.path.exists(ruta):
        return MEDICAMENTOS_INVIMA_SEED

    try:
        import openpyxl
        wb = openpyxl.load_workbook(ruta, data_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        if not rows or len(rows) < 2:
            return MEDICAMENTOS_INVIMA_SEED

        headers = [str(h).strip().upper() for h in rows[0]]
        medicamentos = []

        for idx, r in enumerate(rows[1:], start=1):
            d = dict(zip(headers, r))
            prod = limpiar_texto(d.get("PRODUCTO"))
            princ = limpiar_texto(d.get("PRINCIPIOACTIVO"))
            ind = limpiar_texto(d.get("INDICACIONES APROBADA INVIMA"))
            if ind.startswith("Ndicado"):
                ind = "I" + ind[1:]

            i_cod, d_cod = mapear_intervencion_desenlace(prod, princ, ind)
            fec = limpiar_fecha(d.get("FECHA EXPEDICIÓN") or d.get("FECHA EXPEDICIN") or "")

            item = {
                "orden": idx,
                "expediente": limpiar_texto(d.get("EXPEDIENTE")),
                "producto": prod,
                "registro_sanitario": limpiar_texto(d.get("REGISTRO SANITARIO")),
                "fecha_expedicion": fec,
                "estado_registro": limpiar_texto(d.get("ESTADO REGISTRO") or "Vigente"),
                "principio_activo": princ,
                "forma_farmaceutica": limpiar_texto(d.get("FORMA FARMACÉUTICA") or d.get("FORMA FARMACUTICA")),
                "via_administracion": limpiar_texto(d.get("VIA ADMINISTRACIÓN") or d.get("VIA ADMINISTRACIN")),
                "concentracion": limpiar_texto(d.get("CONCENTRACIÓN") or d.get("CONCENTRACIN")),
                "atc": limpiar_texto(d.get("ATC")),
                "descripcion_atc": limpiar_texto(d.get("DESCRIPCIÓN ATC") or d.get("DESCRIPCIN ATC")),
                "relacion_cbd_thc": limpiar_texto(d.get("RELACIÓN CBD:THC") or d.get("RELACIN CBD:THC")),
                "indicaciones": ind,
                "intervencion_codigo": i_cod,
                "desenlace_codigo": d_cod,
            }
            medicamentos.append(item)

        return medicamentos if medicamentos else MEDICAMENTOS_INVIMA_SEED
    except Exception:
        return MEDICAMENTOS_INVIMA_SEED

