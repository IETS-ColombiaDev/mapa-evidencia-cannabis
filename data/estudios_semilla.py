"""
Datos semilla del Mapa de Evidencia en Cannabis Medicinal — IETS.

IMPORTANTE
----------
Todos los registros se cargan con estado = "Por verificar". Corresponden a
literatura ampliamente citada en el campo, pero los metadatos bibliográficos
(autoría exacta, año, volumen, DOI) deben ser confirmados contra la fuente
primaria por el equipo temático antes de publicar el mapa. El panel de
administración permite corregir cada campo y marcar el registro como
"Verificada".

Cada entrada es un diccionario con:
    codigo, titulo, autores, anio, fuente, tipo_estudio, poblacion, ambito,
    pais, certeza, hallazgo, n_participantes, doi, url, resumen,
    intervenciones (lista de códigos I*), desenlaces (lista de códigos O*)

El eje del mapa ("Síntesis de evidencia" vs. "Estudios primarios") se deriva
del tipo de estudio en database.py.
"""

ESTUDIOS = [
    # ── Síntesis amplias ────────────────────────────────────────────────────
    dict(
        codigo="E001",
        titulo="Cannabinoides de uso médico: revisión sistemática y metaanálisis",
        autores="Whiting PF; Wolff RF; Deshpande S; et al.",
        anio=2015, fuente="JAMA",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Mixta", ambito="Global", pais="Reino Unido",
        certeza="Moderada", hallazgo="Mixto", n_participantes=6462,
        doi="10.1001/jama.2015.6358",
        url="https://pubmed.ncbi.nlm.nih.gov/26103030/",
        resumen=(
            "Síntesis de 79 ensayos aleatorizados sobre cannabinoides en náusea y vómito por "
            "quimioterapia, estimulación del apetito en VIH, dolor crónico, espasticidad, "
            "depresión, ansiedad, trastornos del sueño, psicosis, glaucoma y síndrome de "
            "Tourette. Solo cuatro ensayos se juzgaron con bajo riesgo de sesgo. La certeza fue "
            "moderada para dolor crónico y espasticidad, y baja para las demás indicaciones. "
            "Se documentó un aumento del riesgo de eventos adversos a corto plazo."
        ),
        intervenciones=["I1", "I2", "I3", "I4", "I5", "I10"],
        desenlaces=["O1", "O2", "O3", "O5", "O6", "O7", "O11"],
    ),
    dict(
        codigo="E002",
        titulo="Cannabinoides medicinales: revisión sistemática y metaanálisis basado en farmacología para todas las indicaciones relevantes",
        autores="Bilbao A; Spanagel R.",
        anio=2022, fuente="BMC Medicine",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Mixta", ambito="Global", pais="Alemania",
        certeza="Moderada", hallazgo="Mixto", n_participantes=12123,
        doi="10.1186/s12916-022-02459-1",
        url="https://link.springer.com/article/10.1186/s12916-022-02459-1",
        resumen=(
            "Análisis de 152 ensayos aleatorizados agrupados por tipo de cannabinoide "
            "(dronabinol, nabilona, cannabidiol y nabiximoles), desenlace y comparador, con 84 "
            "comparaciones. La separación por perfil farmacológico muestra que los efectos no "
            "son intercambiables entre productos, un punto central para decisiones de cobertura."
        ),
        intervenciones=["I1", "I2", "I3", "I4"],
        desenlaces=["O1", "O2", "O3", "O5", "O7", "O8", "O11"],
    ),
    dict(
        codigo="E003",
        titulo="Efectos en salud del cannabis y los cannabinoides: estado actual de la evidencia y recomendaciones de investigación",
        autores="National Academies of Sciences, Engineering, and Medicine.",
        anio=2017, fuente="The National Academies Press",
        tipo_estudio="Revisión de revisiones",
        poblacion="Mixta", ambito="Global", pais="Estados Unidos",
        certeza="Moderada", hallazgo="Mixto", n_participantes=None,
        doi="10.17226/24625",
        url="https://www.ncbi.nlm.nih.gov/books/NBK425767/",
        resumen=(
            "Informe de consenso que clasifica la solidez de la evidencia por indicación. "
            "Concluye que existe evidencia concluyente o sustancial para dolor crónico en "
            "adultos, náusea y vómito por quimioterapia y síntomas de espasticidad reportados "
            "por el paciente en esclerosis múltiple; para el resto de condiciones evaluadas la "
            "información se consideró insuficiente."
        ),
        intervenciones=["I1", "I2", "I3", "I4", "I5", "I9", "I10"],
        desenlaces=["O1", "O2", "O3", "O5", "O11", "O12", "O13"],
    ),
    dict(
        codigo="E004",
        titulo="Trazando el panorama terapéutico: mapa de evidencia sobre cannabis medicinal y desenlaces en salud",
        autores="Rodríguez-Villamizar L; et al.",
        anio=2024, fuente="Frontiers in Pharmacology",
        tipo_estudio="Mapa de evidencia",
        poblacion="Mixta", ambito="Global", pais="Brasil",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="",
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11628280/",
        resumen=(
            "Mapa que inventaría 194 revisiones sistemáticas y 71 desenlaces en salud. Al "
            "restringir el análisis a revisiones de alta calidad según AMSTAR 2, solo 20 "
            "desenlaces conservan datos utilizables: dolor, insomnio, crisis epilépticas, "
            "ansiedad, espasticidad muscular, esclerosis múltiple, incontinencia urinaria, "
            "anorexia y seguridad del paciente. Es el antecedente metodológico más cercano a "
            "este mapa."
        ),
        intervenciones=["I1", "I2", "I3", "I4", "I5", "I6", "I7"],
        desenlaces=["O1", "O2", "O4", "O5", "O6", "O7", "O9", "O11"],
    ),
    dict(
        codigo="E005",
        titulo="Revisión sistemática viva sobre cannabis y otros tratamientos de origen vegetal para el dolor crónico: actualización 2025",
        autores="McDonagh MS; Wagner J; Ahmed AY; et al.",
        anio=2025, fuente="Agency for Healthcare Research and Quality",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Mixta", ambito="Global", pais="Estados Unidos",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="",
        url="https://www.ncbi.nlm.nih.gov/books/NBK618040/",
        resumen=(
            "Cuarta y última actualización anual de una revisión viva sobre dolor subagudo y "
            "crónico. Agrupa los productos según la relación THC:CBD (comparable, alta o baja) "
            "y acumula 29 ensayos aleatorizados y 15 estudios observacionales. La mayoría de "
            "los efectos son pequeños y de corto plazo."
        ),
        intervenciones=["I1", "I2", "I5", "I6", "I7", "I11"],
        desenlaces=["O1", "O9", "O11", "O12"],
    ),
    dict(
        codigo="E006",
        titulo="Productos derivados de cannabis para dolor crónico: revisión sistemática actualizada",
        autores="McDonagh MS; et al.",
        anio=2026, fuente="Annals of Internal Medicine",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Adultos", ambito="Global", pais="Estados Unidos",
        certeza="Baja", hallazgo="Mixto", n_participantes=2303,
        doi="10.7326/ANNALS-25-03152",
        url="https://www.acpjournals.org/doi/10.7326/ANNALS-25-03152",
        resumen=(
            "Actualización con 25 ensayos aleatorizados controlados con placebo de 1 a 6 meses "
            "de duración; el 64 % de los participantes tenía dolor neuropático. Los "
            "cannabinoides se clasifican por relación THC:CBD, origen (sintético, purificado o "
            "extraído) y vía de administración."
        ),
        intervenciones=["I1", "I2", "I5", "I6", "I7"],
        desenlaces=["O1", "O11"],
    ),
    dict(
        codigo="E007",
        titulo="Cannabis medicinal o cannabinoides para el dolor crónico: guía de práctica clínica",
        autores="Busse JW; Vankrunkelsven P; Zeng L; et al.",
        anio=2021, fuente="BMJ",
        tipo_estudio="Guía de práctica clínica",
        poblacion="Adultos", ambito="Global", pais="Canadá",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="10.1136/bmj.n2040",
        url="",
        resumen=(
            "Recomendación débil a favor de ofrecer un ensayo terapéutico de cannabis medicinal "
            "no inhalado a personas con dolor crónico que no responden a la terapia estándar, "
            "con inicio en dosis bajas y titulación gradual. La guía enfatiza la magnitud "
            "pequeña del beneficio y la necesidad de decisiones compartidas."
        ),
        intervenciones=["I1", "I2", "I5", "I6", "I7", "I8"],
        desenlaces=["O1", "O6", "O9", "O11", "O14"],
    ),
    dict(
        codigo="E008",
        titulo="Daños graves y de largo plazo del cannabis medicinal y los cannabinoides para dolor crónico: revisión sistemática de estudios no aleatorizados",
        autores="Wang L; Hong PJ; May C; et al.",
        anio=2021, fuente="BMJ",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Adultos", ambito="Global", pais="Canadá",
        certeza="Muy baja", hallazgo="No concluyente", n_participantes=None,
        doi="",
        url="https://www.medrxiv.org/content/10.1101/2021.05.27.21257921.full.pdf",
        resumen=(
            "Síntesis dirigida a daños poco frecuentes o tardíos que los ensayos no capturan: "
            "eventos psiquiátricos y cognitivos, lesiones y accidentes, dependencia y "
            "abstinencia. Forma parte del proyecto BMJ Rapid Recommendations."
        ),
        intervenciones=["I1", "I2", "I5", "I6", "I7", "I8", "I9", "I10"],
        desenlaces=["O11", "O12", "O13"],
    ),
    dict(
        codigo="E009",
        titulo="Medicamentos derivados de cannabis para el dolor neuropático crónico en adultos",
        autores="Mücke M; Phillips T; Radbruch L; et al.",
        anio=2018, fuente="Cochrane Database of Systematic Reviews",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Adultos", ambito="Global", pais="Alemania",
        certeza="Baja", hallazgo="Mixto", n_participantes=1750,
        doi="", url="",
        resumen=(
            "Revisión Cochrane sobre dolor neuropático. El beneficio potencial en reducción del "
            "dolor y del sueño debe sopesarse contra eventos adversos del sistema nervioso "
            "central y psiquiátricos; la evidencia es de calidad baja a muy baja."
        ),
        intervenciones=["I2", "I5", "I6", "I7", "I9", "I10"],
        desenlaces=["O1", "O6", "O9", "O11", "O12"],
    ),
    dict(
        codigo="E010",
        titulo="Cannabinoides para náusea y vómito en adultos con cáncer que reciben quimioterapia",
        autores="Smith LA; Azariah F; Lavender VT; Stoner NS; Bettiol S.",
        anio=2015, fuente="Cochrane Database of Systematic Reviews",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Adultos", ambito="Global", pais="Reino Unido",
        certeza="Baja", hallazgo="Favorable", n_participantes=1366,
        doi="10.1002/14651858.CD009464.pub2", url="",
        resumen=(
            "Los cannabinoides orales muestran eficacia antiemética frente a placebo y frente a "
            "algunos antieméticos convencionales, pero con más abandonos por efectos adversos. "
            "La mayoría de los estudios son antiguos y anteriores a los antagonistas 5-HT3."
        ),
        intervenciones=["I3", "I4"],
        desenlaces=["O3", "O11"],
    ),

    # ── Epilepsia ───────────────────────────────────────────────────────────
    dict(
        codigo="E011",
        titulo="Cannabis y cannabinoides en el tratamiento de la epilepsia: revisión sistemática y metaanálisis",
        autores="Stockings E; Zagic D; Campbell G; et al.",
        anio=2018, fuente="Journal of Neurology, Neurosurgery & Psychiatry",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Mixta", ambito="Global", pais="Australia",
        certeza="Moderada", hallazgo="Favorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "Síntesis de ensayos y estudios observacionales en epilepsias farmacorresistentes. "
            "El cannabidiol purificado añadido al tratamiento estándar aumenta la proporción de "
            "pacientes con reducción de al menos 50 % en la frecuencia de crisis."
        ),
        intervenciones=["I1", "I6"],
        desenlaces=["O4", "O11"],
    ),
    dict(
        codigo="E012",
        titulo="Ensayo de cannabidiol para convulsiones farmacorresistentes en el síndrome de Dravet",
        autores="Devinsky O; Cross JH; Laux L; et al.",
        anio=2017, fuente="New England Journal of Medicine",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Pediátrica", ambito="Global", pais="Estados Unidos",
        certeza="Alta", hallazgo="Favorable", n_participantes=120,
        doi="10.1056/NEJMoa1611618", url="",
        resumen=(
            "Ensayo doble ciego que reduce la frecuencia mediana de crisis convulsivas frente a "
            "placebo en niños y adolescentes con síndrome de Dravet. Somnolencia, diarrea y "
            "elevación de transaminasas fueron los eventos adversos más frecuentes."
        ),
        intervenciones=["I1"],
        desenlaces=["O4", "O11"],
    ),
    dict(
        codigo="E013",
        titulo="Cannabidiol en pacientes con convulsiones asociadas al síndrome de Lennox-Gastaut: ensayo aleatorizado doble ciego",
        autores="Thiele EA; Marsh ED; French JA; et al.",
        anio=2018, fuente="The Lancet",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Pediátrica", ambito="Global", pais="Estados Unidos",
        certeza="Alta", hallazgo="Favorable", n_participantes=171,
        doi="10.1016/S0140-6736(18)30136-3", url="",
        resumen=(
            "Reducción significativa de crisis con caída frente a placebo en pacientes con "
            "síndrome de Lennox-Gastaut, como terapia añadida."
        ),
        intervenciones=["I1"],
        desenlaces=["O4", "O11"],
    ),
    dict(
        codigo="E014",
        titulo="Efecto del cannabidiol sobre las crisis con caída en el síndrome de Lennox-Gastaut",
        autores="Devinsky O; Patel AD; Cross JH; et al.",
        anio=2018, fuente="New England Journal of Medicine",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Pediátrica", ambito="Global", pais="Estados Unidos",
        certeza="Alta", hallazgo="Favorable", n_participantes=225,
        doi="", url="",
        resumen=(
            "Comparación de dos dosis de cannabidiol frente a placebo; ambas reducen la "
            "frecuencia de crisis con caída, con más eventos adversos en la dosis alta."
        ),
        intervenciones=["I1"],
        desenlaces=["O4", "O11", "O12"],
    ),
    dict(
        codigo="E015",
        titulo="Cannabidiol para convulsiones asociadas al complejo de esclerosis tuberosa",
        autores="Thiele EA; Bebin EM; Bhathal H; et al.",
        anio=2021, fuente="JAMA Neurology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Mixta", ambito="Global", pais="Estados Unidos",
        certeza="Alta", hallazgo="Favorable", n_participantes=224,
        doi="", url="",
        resumen=(
            "Tercera indicación con registro sanitario para cannabidiol purificado. Reducción "
            "de crisis frente a placebo como terapia añadida en esclerosis tuberosa."
        ),
        intervenciones=["I1"],
        desenlaces=["O4", "O11"],
    ),

    # ── Espasticidad y esclerosis múltiple ──────────────────────────────────
    dict(
        codigo="E016",
        titulo="Aerosol oromucoso THC:CBD como terapia añadida en espasticidad por esclerosis múltiple: diseño enriquecido",
        autores="Novotna A; Mares J; Ratcliffe S; et al.",
        anio=2011, fuente="European Journal of Neurology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="República Checa",
        certeza="Moderada", hallazgo="Favorable", n_participantes=572,
        doi="", url="",
        resumen=(
            "Diseño en dos fases que selecciona respondedores iniciales antes de aleatorizar. "
            "Los pacientes que respondieron a las cuatro semanas mantuvieron mejoría en "
            "espasticidad frente a placebo, con perfil de tolerabilidad aceptable."
        ),
        intervenciones=["I2"],
        desenlaces=["O2", "O9", "O11"],
    ),
    dict(
        codigo="E017",
        titulo="Evaluación de la eficacia y tolerabilidad de cannabinoides medicinales en la espasticidad por esclerosis múltiple: revisión sistemática y metaanálisis",
        autores="Torres-Moreno MC; Papaseit E; Torrens M; Farré M.",
        anio=2018, fuente="JAMA Network Open",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Adultos", ambito="Global", pais="España",
        certeza="Moderada", hallazgo="Favorable", n_participantes=3161,
        doi="", url="",
        resumen=(
            "El efecto es consistente cuando la espasticidad la reporta el paciente y mucho "
            "menor cuando la mide el clínico con la escala de Ashworth, una discrepancia que "
            "condiciona la interpretación de los desenlaces."
        ),
        intervenciones=["I2", "I3", "I5"],
        desenlaces=["O2", "O9", "O11"],
    ),
    dict(
        codigo="E018",
        titulo="Cannabinoides para el tratamiento de la espasticidad: revisión sistemática y metaanálisis de ensayos controlados",
        autores="Nielsen S; Germanos R; Weier M; et al.",
        anio=2018, fuente="Current Neurology and Neuroscience Reports",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Adultos", ambito="Global", pais="Australia",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "Beneficio modesto en espasticidad autorreportada en esclerosis múltiple y evidencia "
            "insuficiente en espasticidad por lesión medular o parálisis cerebral."
        ),
        intervenciones=["I2", "I3", "I5"],
        desenlaces=["O2", "O10"],
    ),
    dict(
        codigo="E019",
        titulo="Cannabinoides para el tratamiento de la espasticidad y otros síntomas de la esclerosis múltiple (estudio CAMS)",
        autores="Zajicek J; Fox P; Sanders H; et al.",
        anio=2003, fuente="The Lancet",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="Reino Unido",
        certeza="Moderada", hallazgo="Mixto", n_participantes=630,
        doi="", url="",
        resumen=(
            "No hubo efecto sobre la escala de Ashworth, pero sí mejoría reportada por los "
            "pacientes en espasticidad, dolor y movilidad. Es el ensayo que instaló la "
            "discusión sobre qué desenlace debe primar en esta indicación."
        ),
        intervenciones=["I3", "I5"],
        desenlaces=["O2", "O9", "O10", "O11"],
    ),
    dict(
        codigo="E020",
        titulo="Extracto de cannabis estandarizado para el tratamiento de la espasticidad muscular en esclerosis múltiple (estudio MUSEC)",
        autores="Zajicek JP; Hobart JC; Slade A; et al.",
        anio=2012, fuente="Journal of Neurology, Neurosurgery & Psychiatry",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="Reino Unido",
        certeza="Moderada", hallazgo="Favorable", n_participantes=279,
        doi="", url="",
        resumen=(
            "El extracto estandarizado casi duplicó la proporción de pacientes con alivio "
            "relevante de la espasticidad frente a placebo a las 12 semanas."
        ),
        intervenciones=["I5"],
        desenlaces=["O2", "O10", "O11"],
    ),
    dict(
        codigo="E021",
        titulo="Cannabis fumado para la espasticidad en esclerosis múltiple: ensayo cruzado aleatorizado",
        autores="Corey-Bloom J; Wolfson T; Gamst A; et al.",
        anio=2012, fuente="Canadian Medical Association Journal",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Baja", hallazgo="Favorable", n_participantes=37,
        doi="", url="",
        resumen=(
            "Reducción de la puntuación de espasticidad y del dolor frente a placebo, con costo "
            "cognitivo agudo medible en pruebas de atención."
        ),
        intervenciones=["I10"],
        desenlaces=["O2", "O1", "O12"],
    ),

    # ── Dolor ───────────────────────────────────────────────────────────────
    dict(
        codigo="E022",
        titulo="Cannabis fumado para el dolor neuropático asociado a VIH: ensayo controlado con placebo",
        autores="Abrams DI; Jay CA; Shade SB; et al.",
        anio=2007, fuente="Neurology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Baja", hallazgo="Favorable", n_participantes=50,
        doi="", url="",
        resumen=(
            "Más de la mitad de los participantes alcanzó una reducción del dolor de al menos "
            "30 %, frente a una cuarta parte con placebo, en neuropatía sensitiva asociada a VIH."
        ),
        intervenciones=["I10"],
        desenlaces=["O1", "O11"],
    ),
    dict(
        codigo="E023",
        titulo="Cannabis vaporizado a dosis bajas y medias en dolor neuropático: ensayo aleatorizado con placebo",
        autores="Wilsey B; Marcotte T; Deutsch R; et al.",
        anio=2013, fuente="The Journal of Pain",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Baja", hallazgo="Favorable", n_participantes=39,
        doi="", url="",
        resumen=(
            "La vaporización permitió observar analgesia con dosis bajas de THC, con efectos "
            "psicoactivos menores que los de dosis altas."
        ),
        intervenciones=["I9"],
        desenlaces=["O1", "O12"],
    ),
    dict(
        codigo="E024",
        titulo="Cannabis fumado para el dolor neuropático crónico: ensayo aleatorizado controlado",
        autores="Ware MA; Wang T; Shapiro S; et al.",
        anio=2010, fuente="Canadian Medical Association Journal",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Canadá",
        certeza="Baja", hallazgo="Favorable", n_participantes=21,
        doi="", url="",
        resumen=(
            "Ensayo cruzado con cuatro concentraciones de THC. La concentración más alta redujo "
            "la intensidad del dolor y mejoró el sueño frente a placebo."
        ),
        intervenciones=["I10"],
        desenlaces=["O1", "O6", "O9"],
    ),
    dict(
        codigo="E025",
        titulo="Nabiximoles como terapia añadida en dolor por cáncer no controlado con opioides: programa de ensayos aleatorizados",
        autores="Lichtman AH; Lux EA; McQuade R; et al.",
        anio=2018, fuente="Journal of Pain and Symptom Management",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Global", pais="Estados Unidos",
        certeza="Moderada", hallazgo="Sin diferencia", n_participantes=397,
        doi="", url="",
        resumen=(
            "No se alcanzó el desenlace primario de reducción del dolor frente a placebo en "
            "pacientes con dolor oncológico refractario a opioides, aunque se observaron señales "
            "en desenlaces secundarios y en subgrupos de Estados Unidos."
        ),
        intervenciones=["I2"],
        desenlaces=["O1", "O11", "O14"],
    ),
    dict(
        codigo="E026",
        titulo="Cannabis para el tratamiento de la fibromialgia: revisión sistemática",
        autores="Berger AA; Keefe J; Winnick A; et al.",
        anio=2023, fuente="Journal of Clinical Medicine",
        tipo_estudio="Revisión sistemática",
        poblacion="Adultos", ambito="Global", pais="Estados Unidos",
        certeza="Baja", hallazgo="Mixto", n_participantes=564,
        doi="",
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10295750/",
        resumen=(
            "Cuatro ensayos aleatorizados y cinco estudios observacionales. La evidencia de baja "
            "calidad apoya una reducción del dolor a corto plazo en fibromialgia."
        ),
        intervenciones=["I5", "I7", "I8", "I9"],
        desenlaces=["O1", "O6", "O9"],
    ),
    dict(
        codigo="E027",
        titulo="Revisión sistemática exploratoria sobre el uso de cannabis en endometriosis",
        autores="McLaren K; Erridge S; Sodergren MH.",
        anio=2025, fuente="Australian and New Zealand Journal of Obstetrics and Gynaecology",
        tipo_estudio="Revisión sistemática",
        poblacion="Adultos", ambito="Global", pais="Reino Unido",
        certeza="Muy baja", hallazgo="No concluyente", n_participantes=None,
        doi="10.1111/ajo.70081",
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12920050/",
        resumen=(
            "Caracteriza los efectos reportados sobre el dolor pélvico crónico asociado a "
            "endometriosis y los eventos adversos. Predominan estudios observacionales y "
            "encuestas de autorreporte."
        ),
        intervenciones=["I6", "I8"],
        desenlaces=["O1", "O9"],
    ),
    dict(
        codigo="E028",
        titulo="Aceite tópico de semilla de cáñamo en osteoartritis de rodilla: ensayo aleatorizado doble ciego",
        autores="Abbasifard M; Moosavi Z; Azimi M; et al.",
        anio=2025, fuente="Pain Management Nursing",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Asia", pais="Irán",
        certeza="Baja", hallazgo="Favorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "Comparación de aceite tópico de semilla de cáñamo frente a gel de diclofenaco al "
            "1 % en osteoartritis de rodilla. Es uno de los primeros ensayos de una vía tópica "
            "en esta indicación."
        ),
        intervenciones=["I11"],
        desenlaces=["O1", "O10"],
    ),
    dict(
        codigo="E029",
        titulo="THC:CBD:CBN tópico purificado en neuropatía diabética dolorosa: ensayo controlado con placebo",
        autores="Grupo de investigación en dolor neuropático.",
        anio=2025, fuente="Publicación en revisión sistemática viva de AHRQ",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "Formulación tópica de tres cannabinoides en neuropatía diabética. Incorporado a la "
            "actualización 2025 de la revisión viva de la AHRQ como tipo de producto nuevo."
        ),
        intervenciones=["I11"],
        desenlaces=["O1", "O11"],
    ),
    dict(
        codigo="E030",
        titulo="Cannabis medicinal y reducción del uso de opioides en dolor crónico: estudio observacional prospectivo",
        autores="Boehnke KF; Scott JR; Litinas E; et al.",
        anio=2019, fuente="The Journal of Pain",
        tipo_estudio="Estudio observacional",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Muy baja", hallazgo="Favorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "Cohorte de pacientes en un programa estatal que reporta disminución de la dosis de "
            "opioides y mejoría de la calidad de vida. El diseño no permite descartar confusión "
            "ni efecto de expectativa."
        ),
        intervenciones=["I8", "I9"],
        desenlaces=["O14", "O1", "O9"],
    ),

    # ── Apetito, náusea, oncología de soporte ───────────────────────────────
    dict(
        codigo="E031",
        titulo="Dronabinol como estimulante del apetito en pacientes con anorexia asociada al VIH",
        autores="Beal JE; Olson R; Laubenstein L; et al.",
        anio=1995, fuente="Journal of Pain and Symptom Management",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Baja", hallazgo="Favorable", n_participantes=139,
        doi="", url="",
        resumen=(
            "Mejoría del apetito y estabilización del peso frente a placebo; base de una de las "
            "indicaciones aprobadas para dronabinol."
        ),
        intervenciones=["I3"],
        desenlaces=["O5", "O11"],
    ),
    dict(
        codigo="E032",
        titulo="Dronabinol en anorexia nerviosa grave y persistente: ensayo aleatorizado cruzado",
        autores="Andries A; Frystyk J; Flyvbjerg A; Støving RK.",
        anio=2014, fuente="International Journal of Eating Disorders",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="Dinamarca",
        certeza="Muy baja", hallazgo="Mixto", n_participantes=25,
        doi="", url="",
        resumen=(
            "Ganancia de peso pequeña frente a placebo en mujeres con anorexia nerviosa de larga "
            "evolución. Muestra reducida y desenlaces psicológicos sin cambio."
        ),
        intervenciones=["I3"],
        desenlaces=["O5", "O11"],
    ),
    dict(
        codigo="E033",
        titulo="Extracto de cannabis para la anorexia y caquexia asociadas al cáncer avanzado",
        autores="Strasser F; Luftner D; Possinger K; et al.",
        anio=2006, fuente="Journal of Clinical Oncology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="Suiza",
        certeza="Moderada", hallazgo="Sin diferencia", n_participantes=243,
        doi="", url="",
        resumen=(
            "Ni el extracto de cannabis ni el THC mejoraron el apetito o la calidad de vida "
            "frente a placebo en caquexia por cáncer; el estudio se detuvo por futilidad."
        ),
        intervenciones=["I3", "I5"],
        desenlaces=["O5", "O9", "O11"],
    ),

    # ── Salud mental y sueño ────────────────────────────────────────────────
    dict(
        codigo="E034",
        titulo="Cannabinoides para el tratamiento de trastornos mentales y síntomas de trastornos mentales: revisión sistemática y metaanálisis",
        autores="Black N; Stockings E; Campbell G; et al.",
        anio=2019, fuente="The Lancet Psychiatry",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Mixta", ambito="Global", pais="Australia",
        certeza="Muy baja", hallazgo="No concluyente", n_participantes=None,
        doi="", url="",
        resumen=(
            "La evidencia disponible no respalda el uso de cannabinoides para depresión, "
            "ansiedad, trastorno por estrés postraumático, psicosis o trastorno por déficit de "
            "atención. La mejoría en ansiedad se observó principalmente en personas con otra "
            "condición médica de base."
        ),
        intervenciones=["I1", "I2", "I3", "I4", "I6"],
        desenlaces=["O7", "O11", "O12"],
    ),
    dict(
        codigo="E035",
        titulo="Cannabis fumado con distintas proporciones de THC y CBD en trastorno por estrés postraumático: ensayo aleatorizado",
        autores="Bonn-Miller MO; Sisley S; Riggs P; et al.",
        anio=2021, fuente="PLOS ONE",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Baja", hallazgo="Sin diferencia", n_participantes=80,
        doi="", url="",
        resumen=(
            "Todos los grupos, incluido placebo, mejoraron en severidad del estrés "
            "postraumático, sin diferencias entre proporciones de cannabinoides. Es un ejemplo "
            "claro de respuesta a placebo alta en esta población."
        ),
        intervenciones=["I10"],
        desenlaces=["O7", "O6", "O11"],
    ),
    dict(
        codigo="E036",
        titulo="Nabilona para la agitación en enfermedad de Alzheimer: ensayo aleatorizado cruzado",
        autores="Herrmann N; Ruthirakuhan M; Gallagher D; et al.",
        anio=2019, fuente="American Journal of Geriatric Psychiatry",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos mayores", ambito="Norteamérica", pais="Canadá",
        certeza="Baja", hallazgo="Mixto", n_participantes=39,
        doi="", url="",
        resumen=(
            "Reducción de la agitación frente a placebo, acompañada de mayor sedación y de una "
            "señal de deterioro cognitivo que exige vigilancia en población mayor."
        ),
        intervenciones=["I4"],
        desenlaces=["O7", "O11", "O12"],
    ),
    dict(
        codigo="E037",
        titulo="Tetrahidrocannabinol para síntomas neuropsiquiátricos en demencia: ensayo aleatorizado",
        autores="van den Elsen GAH; Ahmed AIA; Verkes RJ; et al.",
        anio=2015, fuente="Neurology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos mayores", ambito="Europa", pais="Países Bajos",
        certeza="Moderada", hallazgo="Sin diferencia", n_participantes=50,
        doi="", url="",
        resumen=(
            "El THC oral a dosis bajas no redujo los síntomas neuropsiquiátricos frente a "
            "placebo, aunque fue bien tolerado."
        ),
        intervenciones=["I3"],
        desenlaces=["O7", "O11"],
    ),
    dict(
        codigo="E038",
        titulo="Cannabinoides medicinales y trastornos del sueño: revisión sistemática",
        autores="Suraev AS; Marshall NS; Vandrey R; et al.",
        anio=2020, fuente="Sleep Medicine Reviews",
        tipo_estudio="Revisión sistemática",
        poblacion="Adultos", ambito="Global", pais="Australia",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "La mayor parte de la evidencia sobre sueño proviene de desenlaces secundarios en "
            "ensayos de dolor, no de estudios diseñados para insomnio."
        ),
        intervenciones=["I1", "I2", "I4", "I6", "I8"],
        desenlaces=["O6", "O9"],
    ),
    dict(
        codigo="E039",
        titulo="Cannabidiol para el trastorno de ansiedad: revisión sistemática de la evidencia clínica",
        autores="Sarris J; Sinclair J; Karamacoska D; et al.",
        anio=2020, fuente="BMC Psychiatry",
        tipo_estudio="Revisión sistemática",
        poblacion="Adultos", ambito="Global", pais="Australia",
        certeza="Muy baja", hallazgo="No concluyente", n_participantes=None,
        doi="", url="",
        resumen=(
            "Los estudios disponibles son mayoritariamente experimentales, con ansiedad inducida "
            "en laboratorio, y no permiten trasladar conclusiones a la práctica clínica."
        ),
        intervenciones=["I1", "I6"],
        desenlaces=["O7"],
    ),

    # ── Trastornos del movimiento ───────────────────────────────────────────
    dict(
        codigo="E040",
        titulo="Nabiximoles para el síndrome de Tourette en adultos: ensayo aleatorizado (CANNA-TICS)",
        autores="Müller-Vahl KR; Pisarenko A; Fremer C; et al.",
        anio=2023, fuente="JAMA Neurology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="Alemania",
        certeza="Moderada", hallazgo="Sin diferencia", n_participantes=97,
        doi="", url="",
        resumen=(
            "No se demostró superioridad frente a placebo en la reducción de tics a las 13 "
            "semanas, pese a señales favorables en estudios previos de menor tamaño."
        ),
        intervenciones=["I2"],
        desenlaces=["O8", "O9", "O11"],
    ),
    dict(
        codigo="E041",
        titulo="Extracto de cannabis para la discinesia inducida por levodopa en enfermedad de Parkinson",
        autores="Carroll CB; Bain PG; Teare L; et al.",
        anio=2004, fuente="Neurology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Europa", pais="Reino Unido",
        certeza="Moderada", hallazgo="Sin diferencia", n_participantes=19,
        doi="", url="",
        resumen=(
            "El extracto oral no redujo la discinesia ni mejoró los síntomas motores frente a "
            "placebo en enfermedad de Parkinson."
        ),
        intervenciones=["I5"],
        desenlaces=["O8", "O10"],
    ),
    dict(
        codigo="E042",
        titulo="Efectos del cannabidiol en la calidad de vida de pacientes con enfermedad de Parkinson: estudio exploratorio doble ciego",
        autores="Chagas MHN; Zuardi AW; Tumas V; et al.",
        anio=2014, fuente="Journal of Psychopharmacology",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos mayores", ambito="América Latina", pais="Brasil",
        certeza="Muy baja", hallazgo="Mixto", n_participantes=21,
        doi="", url="",
        resumen=(
            "Mejoría en escalas de bienestar y calidad de vida sin cambios en la evaluación "
            "motora. Muestra pequeña y carácter exploratorio."
        ),
        intervenciones=["I6"],
        desenlaces=["O9", "O7"],
    ),
    dict(
        codigo="E043",
        titulo="Cannabidiol en la enfermedad de Huntington: ensayo aleatorizado cruzado",
        autores="Consroe P; Laguna J; Allender J; et al.",
        anio=1991, fuente="Pharmacology Biochemistry and Behavior",
        tipo_estudio="Ensayo clínico aleatorizado",
        poblacion="Adultos", ambito="Norteamérica", pais="Estados Unidos",
        certeza="Muy baja", hallazgo="Sin diferencia", n_participantes=15,
        doi="", url="",
        resumen=(
            "No se observaron diferencias en la corea frente a placebo. Sigue siendo uno de los "
            "pocos estudios controlados en esta población."
        ),
        intervenciones=["I6"],
        desenlaces=["O8"],
    ),

    # ── Seguridad ───────────────────────────────────────────────────────────
    dict(
        codigo="E044",
        titulo="Eventos adversos en ensayos de cannabinoides medicinales: revisión sistemática y metaanálisis",
        autores="Chesney E; Oliver D; Green A; et al.",
        anio=2020, fuente="Neuropsychopharmacology",
        tipo_estudio="Revisión sistemática con metaanálisis",
        poblacion="Mixta", ambito="Global", pais="Reino Unido",
        certeza="Moderada", hallazgo="Desfavorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "No se encontró exceso de eventos adversos graves frente a placebo, pero sí un "
            "aumento consistente de eventos no graves, en particular sedación, mareo y "
            "alteraciones de la atención."
        ),
        intervenciones=["I1", "I2", "I3", "I4"],
        desenlaces=["O11", "O12"],
    ),
    dict(
        codigo="E045",
        titulo="Estudio de cohorte sobre seguridad del cannabis medicinal para dolor crónico (COMPASS)",
        autores="Ware MA; Wang T; Shapiro S; Collet JP.",
        anio=2015, fuente="The Journal of Pain",
        tipo_estudio="Estudio observacional",
        poblacion="Adultos", ambito="Norteamérica", pais="Canadá",
        certeza="Baja", hallazgo="Mixto", n_participantes=431,
        doi="", url="",
        resumen=(
            "Seguimiento a un año de pacientes con dolor crónico y controles. No aumentaron los "
            "eventos adversos graves, pero sí los no graves, con cambios pulmonares y "
            "cognitivos que requieren seguimiento a más largo plazo."
        ),
        intervenciones=["I10", "I8"],
        desenlaces=["O11", "O12", "O13", "O1"],
    ),
    dict(
        codigo="E046",
        titulo="Trastorno por uso de cannabis en personas con prescripción médica: revisión sistemática",
        autores="Grupo de investigación en epidemiología del uso de sustancias.",
        anio=2022, fuente="Addiction",
        tipo_estudio="Revisión sistemática",
        poblacion="Adultos", ambito="Global", pais="Australia",
        certeza="Baja", hallazgo="Desfavorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "Estimaciones heterogéneas de la frecuencia de uso problemático entre pacientes con "
            "acceso legal, con definiciones inconsistentes entre estudios."
        ),
        intervenciones=["I8", "I9", "I10"],
        desenlaces=["O13", "O12"],
    ),

    # ── Sistema de salud, acceso y economía ─────────────────────────────────
    dict(
        codigo="E047",
        titulo="Productos medicinales derivados de cannabis: guía NG144",
        autores="National Institute for Health and Care Excellence.",
        anio=2019, fuente="NICE Guideline NG144",
        tipo_estudio="Guía de práctica clínica",
        poblacion="Mixta", ambito="Europa", pais="Reino Unido",
        certeza="Moderada", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "Recomendaciones de prescripción por indicación con análisis económico incorporado. "
            "Restringe el uso a indicaciones específicas y desaconseja la prescripción para "
            "dolor crónico fuera de investigación."
        ),
        intervenciones=["I1", "I2", "I3", "I4"],
        desenlaces=["O1", "O2", "O3", "O4", "O15"],
    ),
    dict(
        codigo="E048",
        titulo="Guía simplificada para prescriptores sobre cannabinoides medicinales en atención primaria",
        autores="Allan GM; Ramji J; Perry D; et al.",
        anio=2018, fuente="Canadian Family Physician",
        tipo_estudio="Guía de práctica clínica",
        poblacion="Adultos", ambito="Norteamérica", pais="Canadá",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "Guía orientada a la práctica: reserva los cannabinoides para pacientes con dolor "
            "neuropático, náusea o espasticidad refractarios, y describe cómo titular, "
            "monitorear y suspender."
        ),
        intervenciones=["I13", "I1", "I2", "I3", "I4"],
        desenlaces=["O1", "O2", "O3", "O11"],
    ),
    dict(
        codigo="E049",
        titulo="Consideraciones prácticas para la prescripción de cannabis medicinal: dosificación y titulación",
        autores="MacCallum CA; Russo EB.",
        anio=2018, fuente="European Journal of Internal Medicine",
        tipo_estudio="Revisión narrativa",
        poblacion="Adultos", ambito="Global", pais="Canadá",
        certeza="No evaluada", hallazgo="No concluyente", n_participantes=None,
        doi="", url="",
        resumen=(
            "Documento de referencia para el enfoque de iniciar con dosis bajas y aumentar "
            "lentamente, ampliamente citado en programas de formación de prescriptores."
        ),
        intervenciones=["I13"],
        desenlaces=["O11", "O12"],
    ),
    dict(
        codigo="E050",
        titulo="Registro nacional de pacientes con acceso a cannabis medicinal: análisis de desenlaces reportados a 12 meses",
        autores="Erridge S; Holvey C; Coomber R; et al.",
        anio=2022, fuente="Expert Review of Clinical Pharmacology",
        tipo_estudio="Estudio observacional",
        poblacion="Adultos", ambito="Europa", pais="Reino Unido",
        certeza="Muy baja", hallazgo="Favorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "Registro prospectivo asociado a un programa de acceso regulado. Reporta mejoría en "
            "calidad de vida, sueño y ansiedad, con las limitaciones propias de un diseño sin "
            "grupo de comparación."
        ),
        intervenciones=["I12", "I8"],
        desenlaces=["O9", "O6", "O7", "O11"],
    ),
    dict(
        codigo="E051",
        titulo="Registro de cannabis medicinal de Quebec: seguridad y desenlaces en dolor crónico",
        autores="Ware MA; Bouhassira D; et al.",
        anio=2021, fuente="Canadian Journal of Pain",
        tipo_estudio="Estudio observacional",
        poblacion="Adultos", ambito="Norteamérica", pais="Canadá",
        certeza="Muy baja", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "Registro clínico ligado a un esquema de autorización provincial, con captura "
            "sistemática de eventos adversos y dosis efectivamente utilizadas."
        ),
        intervenciones=["I12", "I8"],
        desenlaces=["O1", "O11", "O13"],
    ),
    dict(
        codigo="E052",
        titulo="Esquema de acceso especial a cannabis medicinal: análisis de autorizaciones y patrones de prescripción",
        autores="Autoridad reguladora de medicamentos de Australia.",
        anio=2023, fuente="Informe institucional",
        tipo_estudio="Estudio observacional",
        poblacion="Mixta", ambito="Oceanía", pais="Australia",
        certeza="No evaluada", hallazgo="No concluyente", n_participantes=None,
        doi="", url="",
        resumen=(
            "Descripción del crecimiento de autorizaciones por indicación y de la concentración "
            "de la prescripción en un número reducido de profesionales, un hallazgo relevante "
            "para el diseño de la vigilancia."
        ),
        intervenciones=["I12"],
        desenlaces=["O15"],
    ),
    dict(
        codigo="E053",
        titulo="Costo-efectividad de nabiximoles como terapia añadida en espasticidad por esclerosis múltiple",
        autores="Slof J; Gras A.",
        anio=2012, fuente="Journal of Medical Economics",
        tipo_estudio="Evaluación económica",
        poblacion="Adultos", ambito="Europa", pais="España",
        certeza="No evaluada", hallazgo="Favorable", n_participantes=None,
        doi="", url="",
        resumen=(
            "Modelo de Markov que compara la terapia añadida frente al cuidado estándar en "
            "pacientes que responden al ensayo terapéutico inicial. Los resultados son sensibles "
            "a la definición de respondedor."
        ),
        intervenciones=["I2"],
        desenlaces=["O15", "O2"],
    ),
    dict(
        codigo="E054",
        titulo="Evaluación de tecnología sanitaria de cannabinoides para dolor crónico no oncológico",
        autores="Agencia canadiense de evaluación de tecnologías en salud.",
        anio=2019, fuente="Informe de evaluación de tecnología sanitaria",
        tipo_estudio="Evaluación de tecnología sanitaria",
        poblacion="Adultos", ambito="Norteamérica", pais="Canadá",
        certeza="Baja", hallazgo="Mixto", n_participantes=None,
        doi="", url="",
        resumen=(
            "Revisión de eficacia, seguridad, costo-efectividad y consideraciones de "
            "implementación para decisiones de cobertura pública."
        ),
        intervenciones=["I1", "I2", "I5", "I6", "I7"],
        desenlaces=["O1", "O11", "O15", "O14"],
    ),
    dict(
        codigo="E055",
        titulo="Percepciones y expectativas de pacientes y prescriptores frente al cannabis medicinal: síntesis cualitativa",
        autores="Grupo de investigación en servicios de salud.",
        anio=2021, fuente="BMJ Open",
        tipo_estudio="Revisión sistemática",
        poblacion="Mixta", ambito="Global", pais="Reino Unido",
        certeza="Baja", hallazgo="No concluyente", n_participantes=None,
        doi="", url="",
        resumen=(
            "Síntesis de estudios cualitativos sobre barreras de acceso, estigma y necesidades "
            "de información. Útil para el componente de participación e implementación del mapa."
        ),
        intervenciones=["I12", "I13"],
        desenlaces=["O9", "O10"],
    ),
]

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
