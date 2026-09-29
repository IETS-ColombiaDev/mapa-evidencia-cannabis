"""
Mapeo automático de los 203 estudios del Excel a la taxonomía del mapa.

Analiza los campos de texto libre (intervencion_texto, desenlaces_texto,
indicacion, dominio_indicacion, abstract, titulo) y crea vínculos con las
13 intervenciones (I1-I13) y 15 desenlaces (O1-O15) de la taxonomía.

Se ejecuta una sola vez al sembrar la base de datos.
"""

import re
import unicodedata

def _n(texto):
    """Normaliza texto para búsqueda: minúsculas, sin acentos."""
    if not texto:
        return ""
    t = texto.lower()
    t = unicodedata.normalize("NFD", t)
    t = re.sub(r'[\u0300-\u036f]', '', t)
    return t


# ── Reglas de mapeo para INTERVENCIONES ────────────────────────────────────
# Cada regla: (código_intervención, [patrones_que_incluyen], [patrones_que_excluyen])
# Se busca en: intervencion_texto + titulo + abstract (normalizado)

REGLAS_INTERVENCION = [
    # I1 — Cannabidiol purificado (grado farmacéutico): Epidiolex, CBD purificado
    ("I1", [
        r'epidiolex', r'epidyolex', r'gw\s*pharma', r'gwp\d',
        r'cannabidiol\s*purificad', r'purified\s*cannabidiol',
        r'highly\s*purified\s*cbd', r'pharmaceutical.grade\s*cbd',
        r'cbd\s*purificad', r'plant.derived.*purified.*cbd',
        r'100\s*mg.ml.*cannabidiol',
    ], []),

    # I2 — Nabiximoles (THC:CBD 1:1 oromucoso): Sativex, nabiximol
    ("I2", [
        r'nabiximol', r'sativex', r'thc.?cbd\s*1.?1', r'oromucos',
        r'spray\s*oromucos', r'aerosol\s*oromucos',
    ], []),

    # I3 — Dronabinol (THC sintético): Marinol, dronabinol
    ("I3", [
        r'dronabinol', r'marinol', r'thc\s*sintetico', r'thc\s*synthetic',
        r'\bthc\b.*\bsynthetic\b', r'synthetic\s*thc',
    ], []),

    # I4 — Nabilona: Cesamet, nabilona
    ("I4", [
        r'nabilon[ea]', r'cesamet',
    ], []),

    # I5 — Extracto con predominio de THC
    ("I5", [
        r'predominio\s*de?\s*thc', r'thc\s*predomin', r'rich\s*in\s*thc',
        r'thc.?rich', r'high.?thc', r'thc.?domin', r'thc\s*extract',
        r'\bthc\b.*\bextract', r'extract.*\bthc\b',
    ], [r'nabilon', r'dronabinol', r'marinol', r'cesamet', r'synthetic']),

    # I6 — Extracto con predominio de CBD (no purificado farmacéutico)
    ("I6", [
        r'predominio\s*de?\s*cbd', r'cbd\s*predomin', r'rich\s*in\s*cbd',
        r'cbd.?rich', r'high.?cbd', r'cbd.?domin', r'cbd\s*extract',
        r'cbd\s*oil', r'aceite\s*(de\s*)?cbd', r'cbd\s*oral',
        r'extracto.*cbd', r'cbd.*extract',
        r'\bcbd\b', r'cannabidiol',
    ], [r'epidiolex', r'epidyolex', r'purificad', r'pharmaceutical.grade',
        r'highly\s*purified']),

    # I7 — Extracto balanceado THC:CBD
    ("I7", [
        r'thc.*cbd.*balance', r'balanc.*thc.*cbd', r'thc\s*y\s*cbd',
        r'thc.?cbd', r'cbd.?thc', r'thc\s*:\s*cbd', r'cbd\s*:\s*thc',
        r'combinaci.*thc.*cbd', r'combination.*thc.*cbd',
    ], [r'nabiximol', r'sativex', r'1.?:.*1', r'oromucos']),

    # I8 — Fórmula magistral de espectro completo
    ("I8", [
        r'espectro\s*complet', r'full.?spectrum', r'whole.?plant',
        r'planta\s*complet', r'aceite\s*de\s*cannabis', r'cannabis\s*oil',
        r'magistral', r'cannabis.?based\s*oil', r'cannabis\s*extract',
        r'extracto\s*de\s*cannabis', r'medical\s*cannabis.*oil',
        r'cannabis\s*medicinal', r'medicinal\s*cannabis',
    ], []),

    # I9 — Cannabis vaporizado
    ("I9", [
        r'vaporiz', r'vaporis', r'vaporized', r'vaporised', r'vaping',
        r'inhala', r'inhalat', r'inhalacion',
    ], [r'fumad', r'smok']),

    # I10 — Cannabis fumado
    ("I10", [
        r'fumad', r'smoked', r'smoking', r'combustion', r'flor\s*seca',
        r'dried\s*flower', r'herbal\s*cannabis',
    ], []),

    # I11 — Formulaciones tópicas y transdérmicas
    ("I11", [
        r'topic[ao]', r'topical', r'transdermic', r'transderm',
        r'crema', r'cream', r'gel\b', r'parche', r'patch',
        r'pomada', r'ointment', r'locion', r'lotion', r'unguento',
    ], []),

    # I12 — Programas de acceso regulado y registro de pacientes
    ("I12", [
        r'acceso\s*regulad', r'registro\s*de\s*pacient', r'program.*acceso',
        r'access\s*program', r'patient\s*registry', r'regulated\s*access',
        r'prescription\s*pattern', r'dispensar', r'dispensing',
        r'autoriza', r'licenci',
    ], []),

    # I13 — Formación y guías para prescriptores
    ("I13", [
        r'guia.*prescri', r'prescriptor', r'formacion.*medic',
        r'clinical\s*practice\s*guideline', r'physician\s*training',
        r'knowledge.*cannabis.*prescri', r'attitude.*prescri',
        r'percepcion.*prescri',
    ], []),
]

# ── Reglas de mapeo para DESENLACES ────────────────────────────────────────
REGLAS_DESENLACE = [
    # O1 — Dolor crónico
    ("O1", [
        r'\bdolor\b', r'\bpain\b', r'analges', r'nocicepti', r'neuropat',
        r'dolor\s*cronic', r'chronic\s*pain', r'dolor\s*neuropat',
        r'neuropathic\s*pain', r'fibromialg', r'fibromyalg',
        r'artrit', r'arthrit', r'artrosis', r'osteoart',
        r'migra[nñ]', r'cefalea', r'headache',
        r'endometri', r'dismenorre', r'dysmenorrh',
    ], []),

    # O2 — Espasticidad
    ("O2", [
        r'espasticid', r'spasticit', r'spasm', r'espasm',
        r'esclerosis\s*multipl', r'multiple\s*sclerosis',
        r'ashworth', r'rigidez\s*muscul', r'muscle\s*rigid',
    ], []),

    # O3 — Náusea y vómito
    ("O3", [
        r'nause', r'nausea', r'vomit', r'emesis', r'emetic', r'antiemetic',
        r'antiemetico', r'quimioterapi', r'chemotherapy.*nause',
    ], []),

    # O4 — Crisis epilépticas
    ("O4", [
        r'epilep', r'convulsi', r'seizure', r'crisis\s*convulsiv',
        r'dravet', r'lennox', r'tuberosa', r'tuberous',
        r'anticonvuls', r'antiepileptic',
    ], []),

    # O5 — Apetito y peso
    ("O5", [
        r'apetit', r'appetit', r'anorexi', r'caquex', r'cachex',
        r'peso\s*corporal', r'body\s*weight', r'imc\b', r'\bbmi\b',
        r'ganancia\s*de\s*peso', r'weight\s*gain', r'weight\s*loss',
        r'perdida\s*de\s*peso', r'nutricion', r'nutrition',
    ], []),

    # O6 — Sueño
    ("O6", [
        r'sue[nñ]o', r'sleep', r'insomnio', r'insomnia', r'somnolenc',
        r'calidad\s*del\s*sue', r'sleep\s*quality', r'sleep\s*disorder',
        r'latencia.*sue[nñ]o', r'sleep\s*latency', r'sleep\s*onset',
        r'pesadill', r'nightmare',
    ], []),

    # O7 — Ansiedad, depresión y TEPT
    ("O7", [
        r'ansiedad', r'anxiety', r'depresion', r'depression',
        r'tept', r'ptsd', r'estres\s*postraum', r'post.?traumat',
        r'trastorno.*mental', r'mental\s*disorder',
        r'bipolar', r'mood\s*disorder',
        r'trastorno.*animo', r'estado\s*de\s*animo',
        r'agitacion', r'agitation', r'irritabilidad', r'irritability',
        r'burnout',
        r'autismo', r'autism', r'trastorno.*espectro\s*autista',
        r'autism\s*spectrum', r'\basd\b',
        r'trastorno.*atencion', r'adhd', r'\btdah\b',
    ], [r'estres\s*oxidat', r'oxidative\s*stress']),

    # O8 — Movimientos anormales
    ("O8", [
        r'\btics?\b', r'tourette', r'discinesi', r'dyskinesi',
        r'distoni', r'dystoni', r'temblor', r'tremor',
        r'corea', r'chorea', r'huntington', r'movimiento.*anormal',
        r'movement\s*disorder', r'blefaroespasm', r'blepharospasm',
    ], []),

    # O9 — Calidad de vida
    ("O9", [
        r'calidad\s*de\s*vida', r'quality\s*of\s*life', r'\bqol\b',
        r'\bhrqol\b', r'bienestar', r'well.?being', r'satisf',
        r'impresion\s*global', r'global\s*impression',
        r'whoqol', r'sf.?36', r'eq.?5d',
    ], []),

    # O10 — Funcionalidad
    ("O10", [
        r'funcionalidad', r'functionality', r'function.*physical',
        r'funcion\s*fisic', r'desempe[nñ]o', r'performance',
        r'actividades\s*cotidian', r'daily\s*activit',
        r'discapacidad', r'disability', r'autocuidado', r'self.?care',
        r'rehabilit',
    ], []),

    # O11 — Eventos adversos
    ("O11", [
        r'evento.*advers', r'adverse\s*event', r'efecto.*advers',
        r'adverse\s*effect', r'side\s*effect',
        r'\bsafety\b', r'tolerab', r'toxicid', r'toxicit',
        r'reaccion.*advers', r'adverse\s*reaction',
        r'hepatotox', r'nefrotox', r'cardiotox',
    ], []),

    # O12 — Efectos psiquiátricos y cognitivos
    ("O12", [
        r'funcion\s*cognitiv', r'cognitive\s*function',
        r'sedacion', r'sedation', r'somnolencia', r'drowsiness',
        r'psicosis', r'psychosis', r'psicotic', r'psychotic',
        r'neurodesarrollo', r'neurodevelop',
        r'efecto.*psiquiatr', r'psychiatric\s*effect',
        r'deterioro.*cognitiv', r'cognitive\s*impairment',
    ], []),

    # O13 — Dependencia y accidentes
    ("O13", [
        r'dependencia', r'dependenc', r'adiccion', r'addiction',
        r'abuso', r'\babuse\b', r'abstinencia', r'abstinence',
        r'trastorno.*uso.*cannabis', r'cannabis\s*use\s*disorder',
        r'accidente', r'accident', r'caida', r'\bfall\b',
        r'\bcud\b', r'misuse', r'withdrawal\s*syndrom',
    ], []),

    # O14 — Otros medicamentos (sustitución/reducción)
    ("O14", [
        r'opioide', r'opioid', r'reduccion.*medicament',
        r'medication\s*reduc', r'sustitucion', r'substitut',
        r'ahorro.*farmac', r'drug\s*spar', r'reduc.*opiad',
        r'opioid\s*spar', r'polimedicacion', r'polypharmac',
        r'interaccion.*farmac', r'drug\s*interaction',
        r'antiepileptic.*reduc', r'anticonvuls.*reduc',
    ], []),

    # O15 — Costos y uso de servicios
    ("O15", [
        r'costo', r'\bcost\b', r'cost.?effect', r'costo.?efect',
        r'presupuest', r'budget', r'economic', r'economia',
        r'hospitalizacion', r'hospitalization', r'urgent',
        r'servicio.*salud', r'health\s*service', r'utiliz',
        r'gasto', r'expenditure', r'farmaco.?economic',
        r'pharmacoeconomic',
    ], []),
]


def mapear_intervenciones(estudio):
    """Devuelve la lista de códigos de intervención (I1..I13) que aplican al estudio."""
    texto_intervencion = _n(estudio.get("intervencion_texto", ""))
    titulo = _n(estudio.get("titulo", ""))
    abstract = _n(estudio.get("abstract", ""))
    
    # Textos donde buscar para intervenciones: priorizar intervencion_texto, luego titulo+abstract
    textos_prim = texto_intervencion  # alta prioridad
    textos_sec = f"{titulo} {abstract}"  # baja prioridad
    
    codigos = set()
    
    for codigo, patrones_incl, patrones_excl in REGLAS_INTERVENCION:
        # Buscar en texto de intervención primero
        encontrado = False
        for patron in patrones_incl:
            if re.search(patron, textos_prim):
                encontrado = True
                break
        
        if not encontrado:
            # Buscar en titulo + abstract (solo para algunos más genéricos)
            for patron in patrones_incl:
                if re.search(patron, textos_sec):
                    encontrado = True
                    break
        
        if encontrado:
            # Verificar exclusiones
            excluido = False
            for patron_excl in patrones_excl:
                if re.search(patron_excl, textos_prim) or re.search(patron_excl, textos_sec):
                    excluido = True
                    break
            if not excluido:
                codigos.add(codigo)
    
    # Si detectamos I8 (genérico: cannabis medicinal) junto con otros más específicos,
    # mantener I8 porque el estudio podría incluir formulaciones genéricas
    # No filtrar nada — es válido que un estudio tenga múltiples intervenciones
    
    # Si no se detectó nada, asignar I8 como fallback (fórmula magistral genérica)
    if not codigos:
        codigos.add("I8")
    
    return sorted(codigos)


def mapear_desenlaces(estudio):
    """Devuelve la lista de códigos de desenlace (O1..O15) que aplican al estudio."""
    texto_desenlaces = _n(estudio.get("desenlaces_texto", ""))
    indicacion = _n(estudio.get("indicacion", ""))
    dominio = _n(estudio.get("dominio_indicacion", ""))
    titulo = _n(estudio.get("titulo", ""))
    abstract = _n(estudio.get("abstract", ""))
    
    # Para desenlaces, buscar en desenlaces_texto (primario), indicacion+titulo (secundario)
    # Abstract solo para desenlaces específicos, NO para O11/O12 que son muy genéricos
    textos_prim = f"{texto_desenlaces} {indicacion}"
    textos_sec = f"{titulo} {dominio}"
    textos_full = f"{titulo} {abstract} {dominio}"
    
    # Desenlaces que NO deben buscarse en abstract (demasiado genéricos)
    solo_primario = {"O11", "O12"}
    
    codigos = set()
    
    for codigo, patrones_incl, patrones_excl in REGLAS_DESENLACE:
        encontrado = False
        for patron in patrones_incl:
            if re.search(patron, textos_prim):
                encontrado = True
                break
        
        if not encontrado:
            # Para O11/O12 solo buscar en titulo, no en abstract
            fuente = textos_sec if codigo in solo_primario else textos_full
            for patron in patrones_incl:
                if re.search(patron, fuente):
                    encontrado = True
                    break
        
        if encontrado:
            excluido = False
            for patron_excl in patrones_excl:
                if re.search(patron_excl, textos_prim):
                    excluido = True
                    break
            if not excluido:
                codigos.add(codigo)
    
    # Mapeos adicionales basados en dominio_indicacion
    dominio_lower = _n(estudio.get("dominio_indicacion", ""))
    if "dolor" in dominio_lower or "paliat" in dominio_lower:
        codigos.add("O1")  # Dolor crónico
    if "oncolog" in dominio_lower or "cancer" in dominio_lower:
        codigos.add("O3")  # Náusea y vómito (frecuente en oncología)
    if "seguridad" in dominio_lower:
        codigos.add("O11")  # Eventos adversos
    
    # Si no se detectó nada, usar O9 (calidad de vida) como mínimo
    if not codigos:
        codigos.add("O9")
    
    return sorted(codigos)


def mapear_estudio(estudio):
    """Devuelve (intervenciones, desenlaces) como listas de códigos."""
    return mapear_intervenciones(estudio), mapear_desenlaces(estudio)
