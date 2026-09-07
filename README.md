# 🚀 Pipeline ETL de Ventas End-to-End

Este proyecto implementa un **Pipeline de Ingeniería de Datos completo (ETL)** que automatiza la extracción, limpieza, modelado en PostgreSQL, análisis avanzado con SQL y visualización interactiva en Power BI.

---

## 🏗️ Arquitectura del Pipeline
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ EXTRACT │───>│ TRANSFORM │───>│ LOAD │───>│ ANALYZE & BI │
│ Archivos CSV │ │ Python / Pandas │ │ PostgreSQL DB │ │ SQL & Power BI │
│ (Datos Crudos) │ │(Limpieza/Calidad)│ │ (Modelo Estrella)│ │ (Dashboard) │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘

text


---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.12+
- **Procesamiento y Calidad de Datos:** Pandas, NumPy
- **Base de Datos Relacional:** PostgreSQL
- **Conexión & ORM:** SQLAlchemy, Psycopg2
- **Consultas & Métricas:** SQL Avanzado (CTEs, Window Functions: `RANK()`, `LAG()`)
- **Visualización:** Power BI Desktop

---

## 📊 Modelo de Datos (Esquema en Estrella / Star Schema)

El almacenamiento se estructuró siguiendo las mejores prácticas de **Data Warehousing** usando un modelo dimensional:

- **`ventas` (Tabla de Hechos / Fact Table):** Almacena las métricas cuantitativas de las transacciones (cantidad, precio, total) y claves foráneas.
- **`productos` (Dimensión):** Información descriptiva de productos, categorías y precios de lista.
- **`clientes` (Dimensión):** Datos demográficos y ubicación geográfica de los compradores.
text

   ┌──────────────┐         ┌──────────────┐
   │   clientes   │         │  productos   │
   └──────┬───────┘         └──────┬───────┘
          │ (1)                    │ (1)
          │                        │
          └─────────┐    ┌─────────┘
                   (*)  (*)
                  ┌───────────┐
                  │  ventas   │
                  └───────────┘
text


---

## 🧹 Reglas de Calidad y Limpieza de Datos (Transform)

Durante la fase de transformación (`limpiar_datos.py`), se aplicaron las siguientes reglas de negocio:

1. **Eliminación de Duplicados:** Detección y remoción de registros repetidos en transacciones.
2. **Manejo de Nulos (Null Imputation & Filtering):**
   - Eliminación de ventas "huérfanas" que no poseían un `cliente_id` asociado.
   - Imputación por defecto (valor `1`) para cantidades nulas.
   - Recálculo automático de los totales (`total = cantidad * precio_unitario`).
3. **Corrección de Inconsistencias:** Conversión de cantidades negativas a valores absolutos.
4. **Normalización de Tipos de Datos:** Conversión de cadenas de texto a `DATETIME` para análisis temporal.
5. **Feature Engineering:** Generación de columnas analíticas derivadas (`anio`, `mes`, `nombre_mes`, `dia_semana`).

---

## 📈 Consultas SQL e Insights de Negocio

El script `consultas_sql.py` ejecuta consultas analíticas avanzadas directamente en PostgreSQL:

* **KPIs Principales:** Total de ingresos ($52,985.97), 99 transacciones, ticket promedio ($535.21).
* **Ventas por Categoría:** *Computadoras* domina el 33.97% de los ingresos totales.
* **Top Producto por Categoría (Window Function `RANK()`):** Identificación del producto líder de cada segmento.
* **Crecimiento MoM (Month-over-Month con `LAG()`):** Análisis de variación porcentual de ventas entre meses consecutivos.

---

## 📂 Estructura del Repositorio

```text
pipeline_ventas/
├── data/                  # Archivos CSV crudos y procesados
│   ├── ventas_clean.csv
│   ├── productos_clean.csv
│   └── clientes_clean.csv
├── generar_datos.py       # Generador/Extractor de datos de prueba
├── limpiar_datos.py       # Transformación y validación de calidad
├── cargar_datos.py        # Carga a PostgreSQL (DDL e ingesta)
├── consultas_sql.py       # Engine de analítica SQL
├── pipeline.py            # Orquestador principal (módulo único)
├── config.example.py      # Plantilla de variables de entorno / credenciales
├── requirements.txt       # Dependencias de Python
└── README.md              # Documentación del proyecto