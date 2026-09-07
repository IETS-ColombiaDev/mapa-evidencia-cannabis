# Mapa de Evidencia en Cannabis Medicinal — IETS

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0%2B-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20Vanilla%20JS-F16529.svg?logo=javascript&logoColor=white)](https://developer.mozilla.org/)
[![Status](https://img.shields.io/badge/Estado-Producci%C3%B3n%20%2F%20Activo-success.svg)](#)
[![Institución](https://img.shields.io/badge/Instituci%C3%B3n-IETS%20Colombia-003189.svg)](https://www.iets.org.co/)

Aplicación web institucional desarrollada para el **Instituto de Evaluación Tecnológica en Salud (IETS)**. Proporciona una herramienta interactiva de síntesis científica basada en el estándar internacional de los **Mapas de Evidencia y Brechas** (*Evidence and Gap Maps — EGM*, promovido por organizaciones como Campbell Collaboration y 3ie).

Permite a investigadores biomédicos, profesionales de la salud, comités de evaluación y tomadores de decisiones regulatorias (Ministerio de Salud y Protección Social, Invima) explorar con rigor qué formulaciones y derivados de cannabis cuentan con evidencia clínica contrastada, para qué desenlaces terapéuticos, con qué nivel de certeza metodológica (GRADE) y dónde radican los vacíos críticos de investigación (*research gaps*).

---

## Tabla de Contenido

- [1. Características Principales](#1-características-principales)
- [2. Arquitectura y Metodología](#2-arquitectura-y-metodología)
  - [2.1 Taxonomía de Intervenciones (Filas)](#21-taxonomía-de-intervenciones-filas)
  - [2.2 Dominios de Desenlace (Columnas)](#22-dominios-de-desenlace-columnas)
  - [2.3 Jerarquía de Evidencia y Certeza GRADE](#23-jerarquía-de-evidencia-y-certeza-grade)
- [3. Estructura del Proyecto](#3-estructura-del-proyecto)
- [4. Instalación y Puesta en Marcha Local](#4-instalación-y-puesta-en-marcha-local)
- [5. Panel de Administración](#5-panel-de-administración)
- [6. Especificación de la API REST](#6-especificación-de-la-api-rest)
- [7. Despliegue en Producción](#7-despliegue-en-producción)
- [8. Navegación, Accesibilidad y Teclado](#8-navegación-accesibilidad-y-teclado)
- [9. Protocolo de Verificación de Datos Semilla](#9-protocolo-de-verificación-de-datos-semilla)
- [10. Seguridad y Consideraciones Técnicas](#10-seguridad-y-consideraciones-técnicas)
- [11. Créditos y Licencia](#11-créditos-y-licencia)

---

## 1. Características Principales

- **Matriz Cruzada Bidimensional Interactiva**: Cruce matricial de 13 intervenciones farmacológicas y regulatorias contra 15 desenlaces clínicos y del sistema de salud.
- **Visualización Científica en Tres Modos**:
  - **Burbujas**: Representa el volumen de publicaciones con círculos proporcionales diferenciando síntesis de evidencia (turquesa) y estudios primarios (amarillo).
  - **Densidad (Mapa de Calor)**: Gradiente monocromático que resalta la concentración de literatura por celda.
  - **Certeza Máxima**: Muestra el nivel más alto de certeza metodológica reportado en cada intersección (Alta, Moderada, Baja, Muy baja).
- **Detección Visual de Vacíos (*Research Gaps*)**: Celdas con trama rayada que identifican vacíos de investigación; incluye botón *«Resaltar vacíos»* para iluminación inmediata de brechas críticas.
- **Filtrado Multidimensional en Tiempo Real**: Filtrado cruzado por tipo de diseño (ECA, revisiones sistemáticas, cohortes, etc.), certeza GRADE, dirección del hallazgo (favorable, mixto, sin diferencia, desfavorable), población diana, ámbito geográfico y década de publicación.
- **Sincronización de Estado en la URL**: Los filtros y vistas activas se reflejan en los parámetros `URLSearchParams`, permitiendo compartir enlaces a vistas filtradas específicas.
- **Arquitectura de Pestañas Superiores (Zero Scroll Overload)**: Interfaz organizada en vistas independientes:
  - *Mapa interactivo*: Matriz protagónica con altura natural y amplia visualización sin scroll vertical interno.
  - *Documentación técnica*: Informe institucional completo con 9 apartados estructurados y navegación lateral fija.
  - *Cómo leerlo*: Resumen ejecutivo de interpretación y marco normativo colombiano en tiempo real.
- **Exportación de Microdatos en CSV**: Descarga inmediata de los estudios filtrados en formato CSV normalizado con punto y coma (`;`) y BOM UTF-8 para apertura directa en Excel, R, Python, Stata o SPSS.
- **Ficha Técnica Modal de Estudios**: Al hacer clic en cualquier celda, fila o columna, se despliega una ventana modal con los estudios asociados ordenados por certeza, resumen estructurado, población, tamaño de muestra (*n*), estado de verificación y enlaces a PubMed/DOI.
- **Frontend Ligero sin Dependencias Externas**: Desarrollado en JavaScript vainilla y CSS corporativo institucional del IETS, garantizando máxima velocidad de carga y cero dependencias de empaquetadores como Webpack o Vite.

---

## 2. Arquitectura y Metodología

El mapa adopta la estructura bidimensional estandarizada para revisiones panorámicas sistemáticas de tecnologías sanitarias:

### 2.1 Taxonomía de Intervenciones (Filas)

Organizadas en cuatro categorías principales (**C1 a C4**) que comprenden 13 intervenciones específicas (**I1 a I13**):

| Código | Categoría | Intervención | Descripción Farmacológica / Sanitaria |
|:---:|:---|:---|:---|
| **I1** | C1. Registrados | Cannabidiol purificado (grado farmacéutico) | Solución oral de CBD altamente purificado (>98%, ej. Epidiolex) para encefalopatías epilépticas farmacorresistentes (Dravet, Lennox-Gastaut, Esclerosis Tuberosa). |
| **I2** | C1. Registrados | Nabiximoles (THC:CBD 1:1 oromucoso) | Spray oromucoso estandarizado con proporción equimolar (ej. Sativex) indicado en espasticidad por esclerosis múltiple. |
| **I3** | C1. Registrados | Dronabinol (THC sintético) | Isómero sintético oral del Δ9-THC (ej. Marinol) indicado en emesis por quimioterapia y anorexia en VIH/SIDA. |
| **I4** | C1. Registrados | Nabilona (análogo sintético del THC) | Cannabinoide oral análogo al THC (ej. Cesamet) para náuseas refractarias y dolor espástico. |
| **I5** | C2. Magistrales | Extracto con predominio de THC | Fórmulas magistrales con ratio THC:CBD alto (>5:1 o solo THC) para dolor oncológico o cuidados paliativos. |
| **I6** | C2. Magistrales | Extracto con predominio de CBD | Fórmulas magistrales con ratio CBD:THC alto (>10:1 o solo CBD) sin registro formal. |
| **I7** | C2. Magistrales | Extracto balanceado THC:CBD | Preparaciones magistrales con proporciones comparables de THC y CBD (~1:1 a 1:2). |
| **I8** | C2. Magistrales | Fórmula magistral de espectro completo | Extractos crudos o descarboxilados que preservan el perfil completo de cannabinoides menores y terpenos. |
| **I9** | C3. Flor y otras vías | Cannabis vaporizado | Inhalación por calentamiento térmico de inflorescencias a 180–210°C, minimizando compuestos pirolíticos. |
| **I10** | C3. Flor y otras vías | Cannabis fumado | Inhalación por combustión directa; históricamente evaluada en dolor neuropático inicial, con toxicidad respiratoria. |
| **I11** | C3. Flor y otras vías | Formulaciones tópicas y transdérmicas | Geles, ungüentos y parches de acción local o transdérmica sistémica con baja penetración cerebral. |
| **I12** | C4. Gobernanza | Programas de acceso regulado y registros | Sistemas de acceso controlado y cohortes de farmacovigilancia activa en salud pública. |
| **I13** | C4. Gobernanza | Formación y guías para prescriptores | Algoritmos de dosificación, guías clínicas y educación médica para mitigar riesgos e interacciones. |

### 2.2 Dominios de Desenlace (Columnas)

Comprende 15 desenlaces distribuidos en cuatro dominios clave (**D1 a D4**):

| Código | Dominio | Desenlace | Medición e Indicador Clínico |
|:---:|:---|:---|:---|
| **O1** | D1. Eficacia | Dolor crónico | Reducción ≥30% o ≥50% en escalas analógicas (EVA/NRS) en dolor neuropático, musculoesquelético u oncológico. |
| **O2** | D1. Eficacia | Espasticidad | Modificaciones en la Escala de Ashworth Modificada o autoinforme numérico en esclerosis múltiple. |
| **O3** | D1. Eficacia | Náusea y vómito | Control de emesis inducida por quimioterapia citotóxica (CINV). |
| **O4** | D1. Eficacia | Crisis epilépticas | Reducción porcentual de crisis convulsivas mayores al mes. |
| **O5** | D1. Eficacia | Apetito y peso | Ganancia ponderal y consumo calórico en síndromes de desgaste asociados a cáncer o VIH. |
| **O6** | D1. Eficacia | Sueño | Latencia del sueño, despertares nocturnos y arquitectura del descanso. |
| **O7** | D1. Eficacia | Ansiedad, depresión y TEPT | Puntajes en escalas estandarizadas (GAD-7, PHQ-9, CAPS-5). |
| **O8** | D1. Eficacia | Movimientos anormales | Severidad de tics en síndrome de Tourette, temblor y discinesias por levodopa. |
| **O9** | D2. Calidad de vida | Calidad de vida | Cuestionarios validados globales o específicos (EQ-5D, SF-36, EORTC QLQ-C30). |
| **O10** | D2. Calidad de vida | Funcionalidad | Desempeño físico cotidiano, autonomía y retorno laboral. |
| **O11** | D3. Seguridad | Eventos adversos | Incidencia de eventos adversos totales, eventos graves (SAE) y retiros por toxicidad. |
| **O12** | D3. Seguridad | Efectos psiquiátricos y cognitivos | Episodios psicóticos agudos, sedación profunda, disforia y alteración de memoria de trabajo. |
| **O13** | D3. Seguridad | Dependencia y accidentes | Trastorno por uso de cannabis (CUD), síndrome de abstinencia y caídas/accidentes vehiculares. |
| **O14** | D4. Sistema de salud | Otros medicamentos | Efecto ahorrador de opioides (*opioid-sparing*), antiepilépticos o benzodiacepinas. |
| **O15** | D4. Sistema de salud | Costos y uso de servicios | Razones de costo-efectividad incremental (ICER), impacto presupuestal y visitas a urgencias. |

### 2.3 Jerarquía de Evidencia y Certeza GRADE

El sistema clasifica las publicaciones en dos grandes categorías visuales mutuamente excluyentes:

- **Círculo Turquesa (`--turquesa: #289E93`) — Síntesis de Evidencia**:
  - Revisiones sistemáticas con metaanálisis.
  - Revisiones sistemáticas Cochrane o PRISMA.
  - Revisiones de revisiones (*overviews*).
  - Guías de Práctica Clínica (GPC).
  - Evaluaciones de Tecnología Sanitaria (ETS).
- **Círculo Amarillo (`--amarillo: #EAA000`) — Estudios Primarios**:
  - Ensayos Clínicos Aleatorizados (ECA).
  - Ensayos cuasi-experimentales y no aleatorizados.
  - Estudios observacionales analíticos (cohortes prospectivas y casos-controles).
  - Evaluaciones económicas en salud (costo-efectividad, costo-utilidad).
  - Series y reportes de casos.

#### Niveles de Confianza Metodológica (GRADE)
- **Alta**: Muy alta certeza de que el verdadero efecto coincide con el estimado.
- **Moderada**: Confianza moderada; el verdadero efecto probablemente sea cercano al reportado.
- **Baja**: Confianza limitada; nuevas investigaciones probablemente cambiarán el resultado.
- **Muy baja**: Incertidumbre sustancial; estimación metodológicamente frágil.

---

## 3. Estructura del Proyecto

```
mapa-evidencia-cannabis/
├── app.py                      # Servidor Flask, rutas web y endpoints de la API REST
├── database.py                 # Esquema SQLite, configuración de catálogos y carga semilla
├── requirements.txt            # Dependencias de producción (Flask, Gunicorn)
├── Procfile                    # Comando de inicio para servidores PaaS (Gunicorn)
├── render.yaml                 # Manifiesto de despliegue automatizado en Render con disco persistente
├── README.md                   # Documentación técnica integral
│
├── data/
│   ├── taxonomia.py            # Definición canónica de filas (intervenciones) y columnas (desenlaces)
│   └── estudios_semilla.py     # Conjunto semilla de 55 estudios biomédicos y normativa colombiana
│
├── templates/
│   ├── index.html              # Vista principal: Mapa interactivo, Documentación y Cómo leerlo
│   └── admin.html              # Panel de administración: Gestión CRUD, filtros y carga masiva
│
└── static/
    ├── css/
    │   └── app.css             # Sistema de diseño institucional IETS (variables, grid, tipografía)
    └── js/
        ├── mapa.js             # Lógica del mapa: renderizado de matriz, filtros, tooltip y exportación
        └── admin.js            # Lógica de administración: tablas reactivas, formularios modales y API
```

---

## 4. Instalación y Puesta en Marcha Local

### Requisitos Previos
- **Python 3.10** o superior instalado en el sistema.
- Gestor de paquetes `pip`.

### Paso 1: Clonar y Navegar al Repositorio
```bash
git clone <url-del-repositorio>
cd mapa-evidencia-cannabis
```

### Paso 2: Crear y Activar un Entorno Virtual
En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Linux / macOS (Bash):
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Inicializar la Base de Datos SQLite
La base de datos se inicializa automáticamente al arrancar la aplicación si no existe el archivo `mapa_cannabis.db`. Si deseas regenerarla manualmente desde cero con los 55 estudios semilla:
```bash
python database.py
```

### Paso 5: Iniciar el Servidor de Desarrollo
```bash
python app.py
```
El servicio quedará disponible en:
```
http://localhost:5000
```

### Variables de Entorno Opcionales
| Variable | Descripción | Valor por Defecto |
|:---|:---|:---|
| `PORT` | Puerto de escucha del servidor HTTP | `5000` |
| `DEBUG` | Habilita el modo de depuración y recarga en caliente de Flask | `False` (desactivado) |
| `MAPA_DB_PATH` | Ruta absoluta o relativa del archivo SQLite | `./mapa_cannabis.db` |

Ejemplo de ejecución con depuración en Windows PowerShell:
```powershell
$env:DEBUG="1"
python app.py
```

---

## 5. Panel de Administración

El panel de administración se encuentra en:
```
http://localhost:5000/admin
```

### Funcionalidades del Panel:
1. **Gestión Completa de Estudios**:
   - Creación manual con selección múltiple de intervenciones y desenlaces.
   - Edición de metadatos bibliográficos, certeza GRADE, dirección del efecto, número de pacientes y URL/DOI.
   - Eliminación directa con confirmación.
2. **Filtro Rápido de Calidad**:
   - Filtro directo por estado: *«Por verificar»* vs *«Verificada»*.
   - Búsqueda textual sobre título, autores y revista.
3. **Carga Masiva por Lotes (Batch Import)**:
   - Formulario de importación directa vía JSON estructurado.
4. **Mantenimiento de Taxonomías**:
   - Los catálogos de categorías, dominios, intervenciones y desenlaces pueden extenderse mediante la API interna.

---

## 6. Especificación de la API REST

Todas las respuestas exitosas devuelven `{"ok": true, ...}` y las excepciones `{"ok": false, "error": "motivo"}` con su código HTTP correspondiente.

### Endpoints de Consulta y Operación

| Método | Endpoint | Parámetros / Cuerpo | Descripción |
|:---:|:---|:---|:---|
| `GET` | `/api/salud` | Ninguno | Health check del servicio. Retorna el número de estudios indexados. |
| `GET` | `/api/datos` | Ninguno | Estructura completa de la matriz, taxonomías, normativa y estudios con sus relaciones M:N. |
| `GET` | `/api/catalogos` | Ninguno | Listas controladas de tipos de estudio, certeza, hallazgos, poblaciones y ámbitos. |
| `POST` | `/api/estudios` | JSON con datos del estudio | Crea un nuevo estudio y sus relaciones cruzadas. |
| `PUT` | `/api/estudios/<id>` | JSON con datos modificados | Actualiza la información y relaciones de un estudio existente. |
| `DELETE` | `/api/estudios/<id>` | Ninguno | Elimina permanentemente el estudio y sus relaciones en cascada. |
| `POST` | `/api/intervenciones` | `{"codigo", "categoria_id", "nombre", "descripcion", "orden"}` | Crea una nueva fila en el mapa. |
| `PUT` | `/api/intervenciones/<id>` | JSON de intervención | Actualiza una intervención existente. |
| `DELETE` | `/api/intervenciones/<id>` | Ninguno | Elimina una intervención y sus relaciones. |
| `POST` | `/api/desenlaces` | `{"codigo", "dominio_id", "nombre", "descripcion", "orden"}` | Crea una nueva columna en el mapa. |
| `PUT` | `/api/desenlaces/<id>` | JSON de desenlace | Actualiza un desenlace existente. |
| `DELETE` | `/api/desenlaces/<id>` | Ninguno | Elimina un desenlace y sus relaciones. |
| `POST` | `/api/importar` | `{"estudios": [...]}` | Inserción masiva por lotes a partir de códigos de intervención y desenlace. |

### Ejemplo: Creación de un Estudio (`POST /api/estudios`)
```json
{
  "titulo": "Efficacy of Cannabidiol in Patients with Treatment-Resistant Dravet Syndrome",
  "autores": "Devinsky O; Cross JH; Laux L; et al.",
  "anio": 2017,
  "fuente": "New England Journal of Medicine",
  "tipo_estudio": "Ensayo clínico aleatorizado",
  "poblacion": "Pediatría",
  "ambito": "Global",
  "pais": "Multicéntrico",
  "certeza": "Alta",
  "hallazgo": "Favorable",
  "n_participantes": 120,
  "doi": "10.1056/NEJMoa1611618",
  "url": "https://doi.org/10.1056/NEJMoa1611618",
  "resumen": "Ensayo pivotal doble ciego que demostró reducción significativa de crisis convulsivas...",
  "estado": "Verificada",
  "intervenciones": [1],
  "desenlaces": [4, 9, 11]
}
```

### Ejemplo: Importación Masiva por Códigos (`POST /api/importar`)
```json
{
  "estudios": [
    {
      "titulo": "Cannabinoids for Medical Use: A Systematic Review and Meta-analysis",
      "autores": "Whiting PF; Wolff RF; Deshpande S; et al.",
      "anio": 2015,
      "fuente": "JAMA",
      "tipo_estudio": "Revisión sistemática con metaanálisis",
      "certeza": "Moderada",
      "hallazgo": "Favorable",
      "intervenciones": ["I1", "I2", "I3"],
      "desenlaces": ["O1", "O2", "O3", "O11"]
    }
  ]
}
```

---

## 7. Despliegue en Producción

### Despliegue en Render
El proyecto incluye configuración nativa lista para producción mediante `render.yaml` y `Procfile`:

1. Conecta el repositorio GitHub / GitLab a tu cuenta de Render.
2. Render detectará automáticamente el archivo `render.yaml`:
   - **Entorno de ejecución**: Python 3.
   - **Comando de construcción**: `pip install -r requirements.txt`.
   - **Comando de inicio**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`.
   - **Disco Persistente (Imprescindible)**: Monta un volumen persistente en `/var/data` y define la variable de entorno:
     ```bash
     MAPA_DB_PATH=/var/data/mapa_cannabis.db
     ```
   > [!IMPORTANT]
   > El disco persistente es crítico. Sin él, el sistema de archivos efímero de los contenedores reiniciará la base de datos a su estado semilla inicial con cada despliegue o reinicio automático.

### Despliegue en Servidor Propio (Linux / VPS con Gunicorn y Nginx)
1. Instala los requerimientos en un entorno virtual.
2. Configura un servicio `systemd` para ejecutar Gunicorn:
   ```ini
   [Unit]
   Description=Gunicorn instance for Mapa de Evidencia Cannabis IETS
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/mapa-evidencia-cannabis
   Environment="PATH=/var/www/mapa-evidencia-cannabis/venv/bin"
   Environment="MAPA_DB_PATH=/var/www/mapa-evidencia-cannabis/data_prod/mapa_cannabis.db"
   ExecStart=/var/www/mapa-evidencia-cannabis/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```
3. Configura Nginx como proxy inverso hacia `http://127.0.0.1:5000`.

---

## 8. Navegación, Accesibilidad y Teclado

La interfaz está optimizada para cumplimiento de pautas de accesibilidad y navegación rápida por teclado:

| Tecla / Atajo | Acción |
|:---:|:---|
| `/` | Enfoca automáticamente la barra de búsqueda de estudios. |
| `Flechas` (`↑`, `↓`, `←`, `→`) | Desplazamiento accesible entre celdas contiguas de la matriz interactiva. |
| `Enter` / `Espacio` | Abre la ficha técnica modal de estudios de la celda seleccionada. |
| `Esc` | Cierra cualquier modal o diálogo emergente activo. |
| `Tab` | Navega en orden lógico a través de filtros, vistas y botones. |

---

## 9. Protocolo de Verificación de Datos Semilla

La base de datos incluye 55 estudios seminales de alto impacto. Todos los registros semilla inician con el estado **«Por verificar»**. 

Flujo recomendado antes del lanzamiento oficial:
1. Accede a `/admin` y activa el filtro de estado **«Por verificar»**.
2. Contrasta los datos bibliográficos (autores, año, revista, DOI, resumen y certeza GRADE) contra la publicación original en PubMed o Crossref.
3. Si la referencia está completa y validada, modifica su estado a **«Verificada»**.
4. El mapa público exhibe una insignia distintiva de verificación en el panel de detalle de cada estudio.

---

## 10. Seguridad y Consideraciones Técnicas

1. **Protección del Panel `/admin`**:
   - En esta versión de desarrollo, `/admin` no cuenta con capa de autenticación integrada.
   - Para despliegues públicos en producción, se debe proteger la ruta `/admin` mediante:
     - Autenticación básica HTTP en Nginx / Apache.
     - Middleware de autenticación de Flask (ej. Flask-Login o sesión JWT).
     - Restricción de acceso por VPN o lista blanca de direcciones IP corporativas.
2. **Inyección SQL**:
   - Todas las consultas a la base de datos se parametrizan utilizando placeholders seguros de SQLite (`?`), previniendo cualquier riesgo de inyección SQL.
3. **Optimización de Metadatos Sociales**:
   - Antes de divulgar el enlace en redes o canales de mensajería (WhatsApp, LinkedIn), completa las etiquetas `og:url` y `og:image` en el encabezado `<head>` de `templates/index.html`.

---

## 11. Créditos y Licencia

- **Institución**: [Instituto de Evaluación Tecnológica en Salud — IETS](https://www.iets.org.co/)
- **Ubicación**: Bogotá D.C., Colombia
- **Marco Metodológico**: Directrices para *Evidence and Gap Maps* (3ie / Campbell Collaboration / PRISMA / GRADE Working Group).
- **Licencia**: Uso institucional y científico bajo los lineamientos de acceso a información en salud del IETS.
