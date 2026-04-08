# Data Reconciliation QA — Automated Test Suite
### Suite Automatizada de Pruebas de Reconciliación de Datos

[![Data Reconciliation QA](https://github.com/brendapsi/data-reconciliation-qa/actions/workflows/tests.yml/badge.svg)](https://github.com/brendapsi/data-reconciliation-qa/actions/workflows/tests.yml)

---

## 🇲🇽 Español

### Descripción
Este proyecto simula un escenario real de automatización de QA de datos: validar la consistencia entre un **Data Warehouse Oracle** y una **capa semántica Denodo**, dos sistemas ampliamente utilizados en pipelines de datos empresariales.

La suite de pruebas está construida con **pytest** y ejecuta 9 validaciones automáticas que replican el trabajo manual de reconciliación que realiza un QA de datos. Está diseñada para adaptarse fácilmente a conexiones de bases de datos reales modificando el archivo de configuración.

Este proyecto incluye integración continua con **GitHub Actions** que ejecuta la suite automáticamente en cada push a `main`.

### Contexto del Problema
En entornos de datos empresariales, los datos se extraen de sistemas fuente, se transforman y se exponen a través de capas semánticas (como Denodo) para reportes y análisis. Las discrepancias entre el DWH y la capa semántica pueden generar reportes incorrectos, decisiones de negocio erróneas y problemas de confianza en los datos.

Esta suite automatiza la detección de:
- Diferencias en conteo de registros entre capas
- Valores nulos inesperados
- Inconsistencias en catálogos de valores permitidos
- Discrepancias en tipos de dato
- Anomalías en longitud de campos
- Diferencias en distribución por categoría
- Discrepancias a nivel de fila mediante muestreo aleatorio

### Suite de Pruebas — 9 Tests

| Test | Descripción |
|------|-------------|
| `test_conteo_campus` | Conteo de registros no nulos en campo campus |
| `test_conteo_modalidad` | Conteo de registros no nulos en campo modalidad |
| `test_conteo_total` | Comparación del total de filas entre ambas fuentes |
| `test_validar_nulos` | Conteo de nulos por campo en todas las columnas configuradas |
| `test_validar_catalogo` | Validación de dominios de valores permitidos por campo |
| `test_validar_tiposdedato` | Consistencia de tipos de dato por campo |
| `test_conteo_por_campo` | Conteo de registros por valor de catálogo para cada campo |
| `test_longitud` | Comparación de longitud máxima por campo |
| `test_muestreo` | Muestreo aleatorio a nivel de fila con semilla fija (comparación campo a campo) |

### Tecnologías
- Python 3.14
- pytest 9.0.2
- pandas 3.0.1
- SQLite3 (simulando Oracle DWH y Denodo)
- pytest-html (reportes HTML de pruebas)
- GitHub Actions (CI/CD)

### Cómo Ejecutarlo

**1. Clonar el repositorio**
```bash
git clone https://github.com/brendapsi/data-reconciliation-qa.git
cd data-reconciliation-qa
```

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**3. Generar las bases de datos de prueba**
```bash
python scripts/01_setup_datos_prueba.py
```

**4. Correr la suite de pruebas**
```bash
pytest tests/test_reconciliacion.py -v
```

**5. Generar reporte HTML**
```bash
pytest tests/test_reconciliacion.py -v --html=reports/reporte.html --self-contained-html
```

### Resultados Esperados
La suite detecta intencionalmente 7 fallas y 2 pruebas exitosas, reflejando discrepancias reales inyectadas en la capa Denodo:
- `EST005`: valor de campus cambiado de MTY a GDL
- `EST021`: modalidad cambiada de NULL a 'HIBRIDO'
- `EST026`: registro extra presente solo en Denodo

📄 [Ver el reporte HTML](reports/reporte.html)

### Estructura del Proyecto
```
data-reconciliation-qa/
├── scripts/
│   ├── 01_setup_datos_prueba.py       # Crea las bases de datos SQLite de prueba
│   └── 02_reconciliacion_funciones.py # Funciones base de validación (pre-pytest)
├── tests/
│   └── test_reconciliacion.py         # Suite de pruebas pytest (9 tests)
├── reports/
│   └── reporte.html                   # Último reporte HTML generado
├── config.py                          # Configuración centralizada (campos, rutas de BD, claves primarias)
├── conftest.py                        # Configuración raíz de pytest
├── requirements.txt
└── README.md
```

---

## 🇺🇸 English

### Overview
This project simulates a real-world Data QA automation scenario: validating data consistency between an **Oracle Data Warehouse** and a **Denodo semantic layer**, two systems commonly used in enterprise data pipelines.

The test suite is built with **pytest** and runs 9 automated validations that replicate the manual reconciliation work typically performed by Data QA engineers. It is designed to be easily adapted to real database connections by updating the configuration file.

This project includes continuous integration with **GitHub Actions** that runs the test suite automatically on every push to `main`.

### Problem Context
In enterprise data environments, data is extracted from source systems, transformed, and exposed through semantic layers (such as Denodo) for reporting and analytics. Discrepancies between the DWH and the semantic layer can cause incorrect reports, wrong business decisions, and data trust issues.

This suite automates the detection of:
- Record count differences between layers
- Unexpected null values
- Catalog/domain value inconsistencies
- Data type mismatches
- Field length anomalies
- Distribution differences per category
- Row-level discrepancies via random sampling

### Test Suite — 9 Tests

| Test | Description |
|------|-------------|
| `test_conteo_campus` | Non-null record count for campus field |
| `test_conteo_modalidad` | Non-null record count for modalidad field |
| `test_conteo_total` | Total row count comparison between both sources |
| `test_validar_nulos` | Null count per field across all configured columns |
| `test_validar_catalogo` | Allowed value domains per field (catalog validation) |
| `test_validar_tiposdedato` | Data type consistency per field |
| `test_conteo_por_campo` | Record count per category value for each field |
| `test_longitud` | Maximum field length comparison |
| `test_muestreo` | Random row-level sampling with fixed seed (field-by-field comparison) |

### Technologies
- Python 3.14
- pytest 9.0.2
- pandas 3.0.1
- SQLite3 (simulating Oracle DWH and Denodo)
- pytest-html (HTML test reports)
- GitHub Actions (CI/CD)

### How to Run

**1. Clone the repository**
```bash
git clone https://github.com/brendapsi/data-reconciliation-qa.git
cd data-reconciliation-qa
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Generate test databases**
```bash
python scripts/01_setup_datos_prueba.py
```

**4. Run the test suite**
```bash
pytest tests/test_reconciliacion.py -v
```

**5. Generate HTML report**
```bash
pytest tests/test_reconciliacion.py -v --html=reports/reporte.html --self-contained-html
```

### Expected Results
The suite intentionally detects 7 failures and 2 passes, reflecting real data discrepancies injected into the Denodo layer:
- `EST005`: campus value changed from MTY to GDL
- `EST021`: modalidad changed from NULL to 'HIBRIDO'
- `EST026`: extra record only present in Denodo

📄 [View the HTML report](reports/reporte.html)

### Project Structure
```
data-reconciliation-qa/
├── scripts/
│   ├── 01_setup_datos_prueba.py       # Creates test SQLite databases
│   └── 02_reconciliacion_funciones.py # Base validation functions (pre-pytest)
├── tests/
│   └── test_reconciliacion.py         # pytest test suite (9 tests)
├── reports/
│   └── reporte.html                   # Latest HTML test report
├── config.py                          # Centralized configuration (fields, DB paths, primary keys)
├── conftest.py                        # pytest root configuration
├── requirements.txt
└── README.md
```
