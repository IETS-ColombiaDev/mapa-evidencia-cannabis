"""
Taxonomía del Mapa de Evidencia en Cannabis Medicinal — IETS.

Filas  = intervenciones (agrupadas por categoría)
Columnas = desenlaces (agrupados por dominio)

Esta estructura es editable desde el panel de administración; aquí solo se define
el estado inicial de la base de datos.
"""

CATEGORIAS_INTERVENCION = [
    {
        "codigo": "C1",
        "nombre": "Cannabinoides con registro sanitario",
        "descripcion": (
            "Productos farmacéuticos de composición conocida y estandarizada, con "
            "aprobación regulatoria en al menos una agencia de referencia."
        ),
        "orden": 1,
    },
    {
        "codigo": "C2",
        "nombre": "Extractos y preparaciones magistrales",
        "descripcion": (
            "Derivados de cannabis elaborados bajo licencia, clasificados por la "
            "relación entre tetrahidrocannabinol (THC) y cannabidiol (CBD)."
        ),
        "orden": 2,
    },
    {
        "codigo": "C3",
        "nombre": "Cannabis en flor y otras vías",
        "descripcion": (
            "Uso de la flor seca o de formulaciones no orales, donde la dosis "
            "efectiva depende en buena medida de la vía de administración."
        ),
        "orden": 3,
    },
    {
        "codigo": "C4",
        "nombre": "Acceso, prescripción y gobernanza",
        "descripcion": (
            "Intervenciones sobre el sistema de salud más que sobre el paciente: "
            "cómo se autoriza, prescribe, dispensa y vigila el uso medicinal."
        ),
        "orden": 4,
    },
]

INTERVENCIONES = [
    # C1
    ("I1", "C1", "Cannabidiol purificado (grado farmacéutico)",
     "CBD altamente purificado de origen vegetal, en solución oral, usado como terapia añadida.", 1),
    ("I2", "C1", "Nabiximoles (THC:CBD 1:1 oromucoso)",
     "Extracto estandarizado en aerosol oromucoso, con proporción aproximada 1:1 entre THC y CBD.", 2),
    ("I3", "C1", "Dronabinol (THC sintético)",
     "THC sintético de administración oral, con indicaciones aprobadas en náusea por quimioterapia y anorexia asociada a VIH.", 3),
    ("I4", "C1", "Nabilona (análogo sintético del THC)",
     "Cannabinoide sintético oral, estudiado sobre todo como antiemético y en dolor asociado a espasticidad.", 4),
    # C2
    ("I5", "C2", "Extracto con predominio de THC",
     "Preparaciones con relación THC:CBD alta, incluidas las formulaciones de solo THC.", 5),
    ("I6", "C2", "Extracto con predominio de CBD",
     "Preparaciones con relación THC:CBD baja, incluidas las formulaciones de solo CBD sin registro sanitario.", 6),
    ("I7", "C2", "Extracto balanceado THC:CBD",
     "Preparaciones con proporciones comparables de THC y CBD, distintas de los productos con registro sanitario.", 7),
    ("I8", "C2", "Fórmula magistral de espectro completo",
     "Aceites y preparaciones magistrales que conservan el perfil completo de cannabinoides y terpenos.", 8),
    # C3
    ("I9", "C3", "Cannabis vaporizado",
     "Flor o extracto administrado por vaporización, con inicio de acción rápido y titulación por el propio paciente.", 9),
    ("I10", "C3", "Cannabis fumado",
     "Flor seca administrada por combustión; vía más estudiada en ensayos tempranos de dolor neuropático.", 10),
    ("I11", "C3", "Formulaciones tópicas y transdérmicas",
     "Cremas, geles y parches de aplicación local, con exposición sistémica limitada.", 11),
    # C4
    ("I12", "C4", "Programas de acceso regulado y registro de pacientes",
     "Esquemas nacionales o subnacionales que autorizan el acceso y hacen seguimiento sistemático de los pacientes.", 12),
    ("I13", "C4", "Formación y guías para prescriptores",
     "Lineamientos, capacitación y herramientas de apoyo a la decisión dirigidas a quienes prescriben.", 13),
]

DOMINIOS_DESENLACE = [
    {
        "codigo": "D1",
        "nombre": "Eficacia clínica",
        "descripcion": "Cambio en el síntoma o signo que motiva el uso terapéutico.",
        "orden": 1,
    },
    {
        "codigo": "D2",
        "nombre": "Calidad de vida y función",
        "descripcion": "Efectos sobre el desempeño diario y la percepción de bienestar del paciente.",
        "orden": 2,
    },
    {
        "codigo": "D3",
        "nombre": "Seguridad",
        "descripcion": "Daños atribuibles al tratamiento, incluidos los de aparición tardía.",
        "orden": 3,
    },
    {
        "codigo": "D4",
        "nombre": "Sistema de salud",
        "descripcion": "Consecuencias sobre el uso de otros tratamientos, los servicios y los costos.",
        "orden": 4,
    },
]

DESENLACES = [
    # D1
    ("O1", "D1", "Dolor crónico",
     "Reducción de la intensidad del dolor en condiciones de más de tres meses de evolución.", 1),
    ("O2", "D1", "Espasticidad",
     "Espasticidad reportada por el paciente o medida por el clínico, principalmente en esclerosis múltiple.", 2),
    ("O3", "D1", "Náusea y vómito",
     "Control de náusea y vómito, sobre todo los inducidos por quimioterapia.", 3),
    ("O4", "D1", "Crisis epilépticas",
     "Reducción del número de crisis en epilepsias farmacorresistentes.", 4),
    ("O5", "D1", "Apetito y peso",
     "Estimulación del apetito y cambios de peso en anorexia, caquexia o infección por VIH.", 5),
    ("O6", "D1", "Sueño",
     "Latencia, continuidad y calidad del sueño reportadas por el paciente.", 6),
    ("O7", "D1", "Ansiedad, depresión y TEPT",
     "Cambio en escalas de síntomas mentales, incluidos los usos fuera de indicación aprobada.", 7),
    ("O8", "D1", "Movimientos anormales",
     "Tics, temblor, distonía y discinesias en trastornos del movimiento.", 8),
    # D2
    ("O9", "D2", "Calidad de vida",
     "Instrumentos genéricos o específicos de calidad de vida.", 9),
    ("O10", "D2", "Funcionalidad",
     "Capacidad de realizar actividades cotidianas, trabajo y autocuidado.", 10),
    # D3
    ("O11", "D3", "Eventos adversos",
     "Eventos adversos totales, eventos graves y retiros por intolerancia.", 11),
    ("O12", "D3", "Efectos psiquiátricos y cognitivos",
     "Psicosis, sedación, alteración de la atención y de la memoria.", 12),
    ("O13", "D3", "Dependencia y accidentes",
     "Trastorno por uso de cannabis, síndrome de abstinencia, caídas y accidentes de tránsito.", 13),
    # D4
    ("O14", "D4", "Otros medicamentos",
     "Sustitución o reducción de opioides, antiepilépticos, antieméticos y otros tratamientos.", 14),
    ("O15", "D4", "Costos y uso de servicios",
     "Costo-efectividad, impacto presupuestal, consultas y hospitalizaciones.", 15),
]
