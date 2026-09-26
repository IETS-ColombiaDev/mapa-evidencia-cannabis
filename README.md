# 🎫 Mapa de Evidencia en Cannabis Medicinal — IETS

<div align="center">
  <img src="https://iets.org.co/wp-content/uploads/2021/05/Logo-IETS-color-1024x512.png" alt="Logo IETS" width="280"/>
</div>

<br/>

> **Autora principal:** Silvana Zapata  
> **Coautores y soporte tecnológico:** Coordinación de TIC — Instituto de Evaluación Tecnológica en Salud (IETS)  
> **Entidad:** Instituto de Evaluación Tecnológica en Salud (IETS), República de Colombia  
> **Versión:** 1.0.0  
> **Estado:** Operativo / Producción  

---

## 📋 Descripción

El **Mapa de Evidencia en Cannabis Medicinal del IETS** es una plataforma científica, analítica e interactiva diseñada para la síntesis visual y estructurada del estado del conocimiento biomédico y clínico sobre el uso terapéutico del cannabis y sus derivados cannabinoides. Desarrollado para el **Instituto de Evaluación Tecnológica en Salud (IETS)**, el aplicativo se fundamenta en la metodología internacional de los **Mapas de Evidencia y Brechas** (*Evidence and Gap Maps — EGM*), promovida y estandarizada por organismos globales de síntesis científica como la *Campbell Collaboration* y *3ie*.

La herramienta responde a los desafíos que enfrentan los tomadores de decisiones sanitarias, médicos especialistas, investigadores, evaluadores de tecnologías en salud y entidades rectoras del sistema de salud colombiano (Ministerio de Salud y Protección Social, Invima) al evaluar formulaciones de cannabis: heterogeneidad en composiciones, dispersión de la literatura clínica, disparidad metodológica y vacíos regulatorios.

El sistema cruza matricialmente dos ejes analíticos fundamentales:
- **Eje Vertical (Filas - 13 Intervenciones):** Agrupadas en 4 categorías taxonómicas que van desde cannabinoides con registro sanitario formal (CBD purificado, Nabiximoles, Dronabinol, Nabilona), pasando por extractos y fórmulas magistrales (predominio THC, predominio CBD, balanceados, espectro completo), flor y vías no convencionales (vaporizado, fumado, formulaciones tópicas), hasta gobernanza y prescripción médica.
- **Eje Horizontal (Columnas - 15 Desenlaces):** Clasificados en 4 dominios clínicos y sistémicos: Eficacia terapéutica (dolor crónico, espasticidad, emesis, epilepsia refractaria, apetito, sueño, trastornos neuropsiquiátricos, movimientos anormales), Calidad de vida y funcionalidad, Seguridad y toxicología (eventos adversos, efectos cognitivos, dependencia), e Impacto en el sistema de salud (ahorro de otros fármacos, costo-efectividad y uso de servicios).

Cada intersección de la matriz consolida el volumen de publicaciones clasificando visualmente entre **síntesis de evidencia** (revisiones sistemáticas, metaanálisis, GPC, ETS) y **estudios primarios** (ensayos clínicos aleatorizados, cohortes, estudios observacionales), evaluados bajo el marco metodológico **GRADE** (*Grading of Recommendations Assessment, Development and Evaluation*) y señalando de forma unívoca las **brechas de investigación** (*research gaps*) donde se requiere generar nueva evidencia empírica.

---

## 🌐 URL del aplicativo

### Entorno local de desarrollo y análisis
- **Visualizador público (Mapa interactivo):** [http://localhost:5000](http://localhost:5000)
- **Panel de administración de estudios y taxonomías:** [http://localhost:5000/admin](http://localhost:5000/admin)

### Entorno de producción institucional
- **Servicio en la nube (Render):** [https://mapa-evidencia-cannabis.onrender.com](https://mapa-evidencia-cannabis.onrender.com)
- **Dominio institucional IETS (Configurable vía CNAME):** `https://evidenciacannabis.iets.org.co`

### Endpoints principales de la API REST
- `GET /api/salud`: Verificación de disponibilidad y conteo total de estudios cargados.
- `GET /api/datos`: Dataset íntegro normalizado (matriz, taxonomías, estudios, relaciones y normativa).
- `GET /api/catalogos`: Listas maestras controladas (diseños, certeza GRADE, hallazgos, poblaciones, ámbitos).

---

## 📱 Responsive design

El aplicativo implementa una arquitectura de interfaz adaptativa (*Responsive Web Design*) desarrollada con Vanilla CSS y CSS Grid nativo, optimizada para ofrecer una experiencia fluida e idéntica en cualquier factor de forma:

- **Estaciones de trabajo de escritorio y pantallas de alta resolución (Monitores 4K / Ultrawide / Desktop > 1200px):**
  - Matriz bidimensional protagónica a pantalla ancha con altura natural y renderizado instantáneo.
  - Encabezados de categorías y dominios con posición fija (*sticky headers*) que permanecen visibles durante el paneo horizontal y vertical.
  - Panel superior de filtros y controles multidimensionales organizados en cuadrícula compacta y accesible.
  - Arquitectura de pestañas superiores (*Zero Scroll Overload*) para alternar entre el **Mapa Interactivo**, la **Documentación Técnica Metodológica** y la guía **Cómo Leerlo**, eliminando el desplazamiento vertical forzado.

- **Dispositivos portátiles y tabletas (Tablets y Laptops 768px – 1199px):**
  - Contenedor de matriz con desplazamiento horizontal táctil suave y amortiguado (*touch-momentum scrolling*).
  - Columnas fijas de intervenciones para no perder el contexto de la molécula analizada al desplazarse hacia desenlaces lejanos.
  - Ventanas modales de estudios adaptadas con márgenes dinámicos y barras de desplazamiento internas accesibles.

- **Teléfonos inteligentes y pantallas móviles (Mobile < 768px):**
  - Transformación táctil de las fichas técnicas modales en hojas de diálogo superpuestas de pantalla completa con botones de cierre accesibles.
  - Panel de filtros colapsable con indicador de filtros activos para maximizar el área visible.
  - Soporte completo para navegación por toques y gestos, además de compatibilidad estricta con lectores de pantalla y navegación por teclado (atajo `/` para búsqueda, `Flechas` direccionales, `Enter` y `Esc`).

---

## 🔐 Acceso y seguridad

El sistema adopta un modelo de gobernanza de información científica con dos niveles de interacción:

1. **Portal Público de Acceso Abierto (`/`):**
   - Acceso irrestricto y sin barreras para la comunidad científica, profesionales de la salud, entidades estatales y ciudadanía en general, en consonancia con la política de datos abiertos y transparencia del IETS.
   - Rutas públicas de consulta de solo lectura (`GET /`, `GET /api/datos`, `GET /api/catalogos`, `GET /api/salud`).

2. **Panel de Gestión y Curaduría de Evidencia (`/admin`):**
   - Espacio restringido para investigadores y administradores metodológicos del IETS, habilitando la creación, actualización, validación y eliminación de estudios clínicos, además del mantenimiento de la taxonomía.
   - En despliegues locales de desarrollo no exige inicio de sesión; para despliegues en entornos de producción institucional, se implementan las siguientes capas de seguridad:
     - **Autenticación HTTP Básica / Digest en Proxy Inverso:** Configuración obligatoria a nivel de Nginx o Ingress Controller con credenciales criptográficas seguras.
     - **Filtrado de Red y VPN Corporativa:** Restricción de tráfico al endpoint `/admin` y a los métodos `POST`, `PUT` y `DELETE` mediante listas blancas de direcciones IP institucionales o redes privadas virtuales (VPN IETS).
     - **Protección contra Inyección SQL:** Todas las transacciones a la base de datos SQLite utilizan parámetros enlazados nativos (`?`), previniendo cualquier vulnerabilidad de inyección SQL.
     - **Mitigación de Cross-Site Scripting (XSS):** Todo el texto inyectado en el DOM es sanitizado mediante `textContent` en Vanilla JavaScript y escape seguro nativo del motor de plantillas Jinja2 de Flask.
     - **Cabeceras de Seguridad HTTP:** Cabeceras preventivas `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN` y `X-XSS-Protection: 1; mode=block`.

---

## ✨ Características principales

- **Matriz Cruzada Bidimensional Interactiva:** Cruce dinámico de 13 intervenciones farmacológicas y regulatorias contra 15 desenlaces clínicos y de salud pública.
- **Visualización Científica en Tres Modos Intercambiables:**
  - **Modo Burbujas:** Visualización proporcional del volumen de estudios por celda, diferenciando con círculos bicolores la **síntesis de evidencia** (color turquesa `#289E93`) y los **estudios primarios** (color amarillo `#EAA000`).
  - **Modo Densidad (Mapa de Calor):** Gradiente cromático continuo que refleja visualmente la concentración de literatura por intersección clínica.
  - **Modo Certeza Máxima (GRADE):** Visualiza en cada casilla el nivel máximo de certidumbre metodológica reportado (Alta, Moderada, Baja, Muy baja).
- **Detección Automática de Brechas (*Research Gaps*):**
  - Identificación gráfica inmediata de celdas con ausencia de evidencia mediante trama rayada (*hatch pattern*).
  - Botón interactivo *«Resaltar vacíos»* que ilumina al instante las brechas de conocimiento prioritarias para guiar agendas de investigación biomédica.
- **Filtrado Multidimensional en Tiempo Real:**
  - Filtrado cruzado simultáneo por diseño de estudio (ECA, revisiones sistemáticas, cohortes, etc.), nivel de certeza GRADE, dirección del hallazgo (favorable, mixto, sin diferencia, desfavorable), grupo poblacional (adultos, pediatría, adultos mayores), ámbito geográfico y período cronológico.
- **Sincronización de Estado en la URL (`URLSearchParams`):**
  - Cada selección de filtros, pestaña o modo de vista se codifica automáticamente en los parámetros de la URL, permitiendo compartir enlaces directos a análisis específicos o reproducir hallazgos en comités técnicos.
- **Ficha Técnica Modal de Estudios:**
  - Al interactuar con cualquier celda, fila o columna, se despliega una ficha técnica detallada que lista los estudios correspondientes, ordenados por jerarquía de certeza, con resumen estructurado, tamaño de muestra ($n$), país, estado de validación y accesos directos a PubMed/DOI.
- **Exportación Normalizada de Microdatos (CSV):**
  - Botón de descarga directa con generación en tiempo real de archivos CSV codificados en UTF-8 con marca de orden de bytes (BOM) y delimitador punto y coma (`;`), listos para análisis en Excel, R, Python, SPSS o Stata.
- **Panel Administrativo CRUD y Carga Masiva por Lotes:**
  - Módulo en `/admin` con formularios de gestión integral, filtros rápidos por estado (*«Por verificar»* vs *«Verificada»*) y motor de importación masiva por lotes en formato JSON estructurado.
- **Documentación Técnica Integrada y Marco Normativo Colombiano:**
  - 9 capítulos técnicos con navegación lateral fija y resumen ejecutivo sobre el marco regulatorio del cannabis medicinal en Colombia (Ley 1787 de 2016, Decreto 811 de 2021 y Resoluciones reglamentarias).

---

## 🛠️ Tecnologías utilizadas

### Backend
- **Python (3.10+ / 3.12+):** Lenguaje principal para la lógica de servidor y procesamiento de datos.
- **Flask (v3.1.3):** Microframework web para el enrutamiento HTTP, renderizado modular de plantillas y construcción de la API RESTful.
- **Gunicorn (v23.0.0):** Servidor HTTP WSGI para entornos de producción de alto rendimiento en sistemas basados en UNIX/Linux.

### Frontend
- **HTML5 Semántico:** Marcado estructurado enfocado en accesibilidad, etiquetas de datos abiertos y compatibilidad con estándares W3C.
- **Vanilla CSS3 (Sistema de Diseño IETS):** Hoja de estilos corporativa moderna estructurada mediante variables CSS, paleta cromática institucional (`#003189`, `#289E93`, `#EAA000`), sombras sutiles, microanimaciones y diseño responsivo fluido sin necesidad de preprocesadores pesados.
- **Vanilla JavaScript (ES6+):** Programación reactiva nativa para la manipulación del DOM, gestión de filtros en tiempo real, renderizado de burbujas dinámicas en la matriz, sincronización de la URL y modales accesibles, con cero dependencias de empaquetadores como Webpack o Vite.
- **Tipografía Google Fonts:** Integración de la familia tipográfica moderna *Inter* con optimización de carga vía `preconnect`.

### Base de datos
- **SQLite3:** Motor de base de datos relacional ligero, embebido y de alto desempeño con soporte completo para transacciones ACID.
- **Integridad Referencial Estricta:** Claves foráneas activadas explícitamente mediante `PRAGMA foreign_keys = ON` con eliminación en cascada (`ON DELETE CASCADE`) para mantener la coherencia de las tablas de unión M:N.
- **Esquema Relacional Normalizado:**
  - `categorias_intervencion` y `intervenciones` (filas de la matriz).
  - `dominios_desenlace` y `desenlaces` (columnas de la matriz).
  - `estudios` (catálogo bibliográfico y evaluación metodológica).
  - `estudio_intervencion` y `estudio_desenlace` (relaciones muchos a muchos).
  - `normativa` (marco legal y regulatorio colombiano).

### Librerías e integraciones
- **Python Standard Library:** Uso exclusivo de módulos estándar (`sqlite3`, `contextlib`, `os`, `json`) que reducen la superficie de ataque y garantizan portabilidad absoluta.
- **FontAwesome / Iconografía Vectorial SVG:** Iconos SVG limpios incrustados de forma nativa para optimizar el peso de transferencia y acelerar los tiempos de despliegue.

---

## 🚀 Instalación

### Requisitos previos
- **Python 3.10** o superior instalado en el equipo.
- Gestor de paquetes **pip** configurado en el PATH del sistema.
- Cliente de control de versiones **Git**.

---

### Opción A: Instalación en Windows (PowerShell)

#### 1. Clonar el repositorio institucional
```powershell
git clone https://github.com/IETS-ColombiaDev/mapa-evidencia-cannabis.git
cd mapa-evidencia-cannabis
```

#### 2. Crear y activar el entorno virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
> *Nota: Si la política de ejecución de scripts de PowerShell bloquea la activación, ejecute previamente:*  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### 3. Instalar dependencias del proyecto
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Inicializar la base de datos (con catálogo semilla)
```powershell
python database.py
```

#### 5. Iniciar el servidor local de desarrollo
```powershell
python app.py
```
El aplicativo estará disponible en `http://localhost:5000`.

---

### Opción B: Instalación en macOS / Linux (Bash / Zsh)

#### 1. Clonar el repositorio
```bash
git clone https://github.com/IETS-ColombiaDev/mapa-evidencia-cannabis.git
cd mapa-evidencia-cannabis
```

#### 2. Crear y activar el entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar requerimientos
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Inicializar la base de datos relacional
```bash
python3 database.py
```

#### 5. Ejecutar la aplicación
```bash
python3 app.py
```

---

### Opción C: Despliegue con Gunicorn (Entornos de Producción Linux)
Para ejecutar la aplicación con múltiples trabajadores concurrentes en un servidor de producción:
```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 3 --threads 2 --timeout 60
```

---

## ⚙️ Configuración

### Web.config (variables clave)

El comportamiento de la plataforma puede ser parametrizado mediante variables de entorno en el sistema operativo, archivos `.env` o en el panel de control de la nube (como Render o Kubernetes):

| Variable de Entorno | Descripción | Valor por Defecto | Ámbito de Uso |
|:---|:---|:---|:---|
| `PORT` | Puerto TCP de escucha para el servidor HTTP | `5000` | Local / Producción |
| `DEBUG` | Activa el modo de depuración de Flask y recarga en caliente | `False` | Solo Desarrollo |
| `MAPA_DB_PATH` | Ruta absoluta o relativa al archivo de base de datos SQLite | `./mapa_cannabis.db` | Local / Producción |
| `PYTHON_VERSION` | Versión del intérprete en entornos de despliegue PaaS | `3.12.4` | Render / PaaS |

Ejemplo de configuración en entorno local (PowerShell):
```powershell
$env:PORT="5000"
$env:DEBUG="1"
$env:MAPA_DB_PATH="./mapa_cannabis.db"
python app.py
```

---

#### Conexiones a datos

La aplicación se comunica con un motor relacional SQLite local o montado en un volumen persistente. La conexión es administrada centralizadamente mediante un gestor de contexto seguro en [database.py](file:///Users/nicolasvargas/Documents/GitHub/mapa-evidencia-cannabis/database.py) con soporte para reconexión automática y rollback ante fallos.

##### Diccionario de datos principal:

1. **`categorias_intervencion`**: Agrupaciones taxonómicas de intervenciones (`id`, `codigo`, `nombre`, `descripcion`, `orden`).
2. **`intervenciones`**: Listado de intervenciones farmacológicas y de gobernanza (`id`, `codigo`, `categoria_id`, `nombre`, `descripcion`, `orden`).
3. **`dominios_desenlace`**: Agrupaciones funcionales de desenlaces (`id`, `codigo`, `nombre`, `descripcion`, `orden`).
4. **`desenlaces`**: Desenlaces clínicos, de calidad de vida y de sistema (`id`, `codigo`, `dominio_id`, `nombre`, `descripcion`, `orden`).
5. **`estudios`**: Registro estructurado de la literatura científica analizada:
   - `id`: Identificador numérico primario.
   - `titulo`: Título original de la publicación.
   - `autores`: Cita bibliográfica estandarizada de autores.
   - `anio`: Año de publicación.
   - `fuente`: Revista indexada, editorial u organismo emisor.
   - `tipo_estudio`: Clasificación del diseño metodológico (ECA, revisión sistemática, etc.).
   - `poblacion`: Grupo etario o subpoblación clínica.
   - `ambito`: Cobertura geográfica o país del estudio.
   - `pais`: País o carácter multicéntrico.
   - `certeza`: Grado de certidumbre metodológica GRADE (*Alta, Moderada, Baja, Muy baja, No evaluada*).
   - `hallazgo`: Dirección observada del efecto (*Favorable, Mixto, Sin diferencia, Desfavorable, No concluyente*).
   - `n_participantes`: Tamaño de la muestra poblacional analizada.
   - `doi` y `url`: Enlaces directos a repositorios PubMed, Crossref o revistas científicas.
   - `resumen`: Resumen estructurado del hallazgo clave.
   - `estado`: Estado de auditoría metodológica (*Por verificar* o *Verificada*).
6. **`estudio_intervencion` & `estudio_desenlace`**: Tablas de asociación relacional M:N con cascada de eliminación.
7. **`normativa`**: Catálogo histórico y vigente del marco legal colombiano del cannabis medicinal.

---

#### Configuración de almacenamiento

El aplicativo gestiona su persistencia de manera autónoma en disco:

- **Almacenamiento Local:** Los datos se escriben en el archivo local `mapa_cannabis.db`.
- **Almacenamiento en la Nube (Render Persistent Disk / Cloud Storage):**
  - En plataformas PaaS/Docker con sistemas de archivos efímeros, es **obligatorio** montar un volumen de almacenamiento persistente (disco SSD de al menos 1 GB) en la ruta `/var/data`.
  - La variable de entorno correspondiente debe definirse como:
    ```bash
    MAPA_DB_PATH=/var/data/mapa_cannabis.db
    ```
- **Copias de Seguridad Periódicas (Backups):**
  - Dado que SQLite encapsula toda la base de datos en un único archivo, se recomienda programar una sincronización periódica hacia servicios de almacenamiento institucional (OneDrive, Google Drive o Azure Blob Storage) utilizando el comando seguro de respaldo en caliente de SQLite:
    ```bash
    sqlite3 /var/data/mapa_cannabis.db ".backup '/var/data/backups/mapa_cannabis_$(date +%Y%m%d).db'"
    ```

---

#### Configuración de correo (SMTP)
> *(Opcional / Proyección de integración institucional)*

Para despliegues corporativos donde se requiera el envío automático de notificaciones a los revisores de evidencia (por ejemplo, al registrarse un nuevo estudio en estado *«Por verificar»* o al culminar una importación por lotes), se contemplan las siguientes variables opcionales:

```ini
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=notificaciones@iets.org.co
SMTP_PASSWORD=****************
SMTP_USE_TLS=True
SMTP_DESTINATARIOS_ALERTA=coordinaciontic@iets.org.co,evidencia@iets.org.co
```

---

## 📂 Estructura del proyecto

```
mapa-evidencia-cannabis/
│
├── app.py                      # Enrutador principal Flask, endpoints API REST y controladores de vistas
├── database.py                 # Conexión SQLite, esquema DDL relacional, catálogos y carga inicial
├── requirements.txt            # Dependencias del ecosistema Python (Flask, Gunicorn)
├── Procfile                    # Instrucción de arranque para servidores PaaS / Heroku / Render
├── render.yaml                 # Manifiesto de infraestructura como código (IaC) para Render con disco persistente
├── Plantilla README.md         # Plantilla estándar institucional para documentación de proyectos IETS
├── GUIA_DISENO.md              # Especificaciones y pautas del sistema de diseño corporativo IETS
├── README.md                   # Documentación técnica completa y exhaustiva del aplicativo
│
├── data/                       # Definiciones semilla y taxonomía canónica
│   ├── taxonomia.py            # Catálogo formal de intervenciones (C1-C4) y desenlaces (D1-D4)
│   └── estudios_semilla.py     # Base de datos inicial con 55 estudios biomédicos y normativa colombiana
│
├── templates/                  # Vistas HTML con motor de plantillas Jinja2
│   ├── index.html              # Vista pública: Mapa interactivo, Documentación y Cómo leerlo
│   └── admin.html              # Panel administrativo: Formularios CRUD, filtros y carga masiva JSON
│
└── static/                     # Archivos estáticos consumidos por el cliente
    ├── css/
    │   └── app.css             # Sistema de diseño institucional IETS (variables, grid, tipografía, modales)
    └── js/
        ├── mapa.js             # Lógica cliente del mapa: renderizado de matriz, filtros en tiempo real y CSV
        └── admin.js            # Lógica cliente del panel: tablas dinámicas, modales y llamadas a la API REST
```

---

## 📂 Estructura de almacenamiento

El modelo de almacenamiento del sistema está optimizado para garantizar máxima velocidad de consulta y cero sobrecarga de mantenimiento:

```
[Dispositivo Local / Servidor VPS / Contenedor PaaS]
│
├── /mapa-evidencia-cannabis/
│   ├── mapa_cannabis.db                # Base de datos relacional activa (entorno local)
│   └── data/
│       ├── taxonomia.py                # Estructura taxonómica base
│       └── estudios_semilla.py         # 55 estudios fundacionales precargados
│
└── /var/data/ (PaaS / Render Persistent Disk)
    ├── mapa_cannabis.db                # Base de datos activa y persistente
    └── backups/                        # Directorio para respaldos rotativos diarios (.db)
```

1. **Base de Datos Operativa (`mapa_cannabis.db`):** Contiene todas las tablas relacionales y registros actualizados en tiempo real.
2. **Capa Semilla (`data/`):** Garantiza que si la base de datos se crea por primera vez en un entorno nuevo, se autoinicialice sin intervención manual con el compendio completo de estudios y taxonomías institucionales.
3. **Persistencia Externa:** Los volúmenes montados protegen los datos contra reinicios o despliegues continuos del contenedor web.

---

## 👥 Roles y funcionalidades

### 👤 Funcionario
Orientado a profesionales clínicos, epidemiólogos, investigadores biomédicos, evaluadores de tecnologías sanitarias, decisores de políticas públicas (Ministerio de Salud, Invima) y ciudadanía interesada.

- **Exploración de la Matriz Científica:** Visualización de la distribución del conocimiento entre 13 intervenciones y 15 desenlaces.
- **Conmutación de Modos de Vista:** Alternancia instantánea entre volumen de estudios (burbujas bicolores), densidad de evidencia (mapa de calor) y certeza GRADE.
- **Detección de Brechas de Investigación:** Identificación inmediata de vacíos de evidencia mediante el botón *«Resaltar vacíos»*.
- **Filtrado Multidimensional:** Filtrado dinámico por diseño de estudio, grado de certidumbre, dirección del efecto, población y ámbito geográfico.
- **Consulta de Fichas Técnicas de Estudios:** Apertura modal con metadatos completos, tamaño de muestra ($n$), resumen clínico y enlaces directos a las fuentes originales (PubMed/DOI).
- **Exportación de Microdatos:** Descarga de los datos filtrados en formato CSV normalizado para análisis econométricos y estadísticos independientes.
- **Consulta de Documentación y Marco Normativo:** Acceso completo a los 9 capítulos de documentación técnica y al resumen histórico de la normativa colombiana.

---

### 🛡️ Administrador
Orientado a los profesionales metodológicos de la Dirección de Tecnologías en Salud y a los ingenieros de la Coordinación de TIC del IETS.

- **Gestión Integral de Estudios (CRUD):** Creación manual de nuevas publicaciones indexadas, edición de metadatos clínicos y eliminación de registros obsoletos o erróneos.
- **Proceso de Auditoría y Verificación:** Control de calidad de los datos semilla, permitiendo modificar el estado de cada estudio de *«Por verificar»* a *«Verificada»* tras contrastarlo con la fuente primaria.
- **Importación Masiva por Lotes (Batch Import):** Inserción estructurada de múltiples estudios clínicos simultáneamente a través del endpoint `/api/importar` utilizando códigos taxonómicos (`I1`-`I13`, `O1`-`O15`).
- **Mantenimiento Taxonómico:** Creación, actualización o reordenamiento de categorías de intervención, intervenciones específicas, dominios de desenlace y desenlaces clínicos según evolucione el consenso científico internacional.
- **Monitoreo de Salud del Sistema:** Supervisión de métricas de carga y disponibilidad a través del endpoint `/api/salud`.

---

## 📧 Plantilla de notificación
> *(Plantilla de comunicación institucional para actualizaciones y reportes de evidencia)*

A continuación se presenta el modelo estandarizado para comunicaciones institucionales vía correo electrónico a investigadores, sociedades científicas y entidades gubernamentales cuando se publiquen nuevas actualizaciones en el mapa:

```markdown
Asunto: [IETS] Actualización del Mapa de Evidencia en Cannabis Medicinal — Versión {VERSION}

Estimado(a) colega / Evaluador(a) del Sistema de Salud:

Le informamos que el Instituto de Evaluación Tecnológica en Salud (IETS) ha publicado una nueva actualización en el Mapa de Evidencia en Cannabis Medicinal, herramienta interactiva fundamentada en la metodología Evidence and Gap Maps (EGM):

📌 Resumen de la actualización:
--------------------------------------------------------------------------------
- Nuevos estudios clínicos y síntesis incorporados: {NUMERO_ESTUDIOS}
- Intervenciones actualizadas: {LISTA_INTERVENCIONES}
- Nuevas brechas de investigación identificadas: {NUMERO_BRECHAS}
- Estado de verificación metodológica: Verificado por el equipo técnico del IETS
--------------------------------------------------------------------------------

Lo invitamos a explorar la matriz interactiva, aplicar filtros por certeza GRADE o dirección del efecto, y exportar los microdatos actualizados para sus análisis técnicos y decisiones sanitarias:

🔗 Acceso al mapa interactivo: https://mapa-evidencia-cannabis.onrender.com
📄 Documentación y metodología: https://mapa-evidencia-cannabis.onrender.com#documentacion

Para reportar nuevas publicaciones o solicitar soporte técnico, comuníquese con la Coordinación de TIC del IETS al correo: coordinaciontic@iets.org.co.

Cordialmente,

Equipo de Evaluación de Tecnologías y Síntesis de Evidencia
Coordinación de Tecnologías de la Información y las Comunicaciones (TIC)
Instituto de Evaluación Tecnológica en Salud — IETS
República de Colombia
```

---

<div align="center">
  <p><strong>Instituto de Evaluación Tecnológica en Salud — IETS</strong></p>
  <p>Bogotá D.C., Colombia · Plataforma de Acceso Abierto a la Evidencia Científica</p>
</div>
