"""
01_setup_datos_prueba.py
========================
Crea dos bases de datos SQLite que simulan:
  - dwh_oracle.db  → tu Oracle DWH (tabla de estudiantes)
  - denodo.db      → tu capa Denodo (vista de estudiantes)

Con diferencias intencionales para que puedas ver FAILs reales.

Ejecuta UNA SOLA VEZ:
    python 01_setup_datos_prueba.py
"""

import sqlite3
import os

# ── Datos de estudiantes ficticios ────────────────────────────────
# Estos van al DWH (Oracle simulado)
# Campos: id, clave_persona, campus, programa, nivel, periodo, estatus, modalidad
ESTUDIANTES_DWH = [
    (1,  "EST001", "MTY", "ITC",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (2,  "EST002", "GDL", "LAE",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (3,  "EST003", "MTY", "ITC",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (4,  "EST004", "CVM", "ARQ",  "PRE", "2024-1", "BAJA",     "PRESENCIAL"),
    (5,  "EST005", "MTY", "MED",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (6,  "EST006", "GDL", "ITC",  "POS", "2024-2", "ACTIVO",   "EN_LINEA"),
    (7,  "EST007", "MTY", "LAE",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (8,  "EST008", "CVM", "ITC",  "PRE", "2024-2", "EGRESADO", "PRESENCIAL"),
    (9,  "EST009", "MTY", "ARQ",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (10, "EST010", "GDL", "MED",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (11, "EST011", "MTY", "ITC",  "PRE", "2024-2", "BAJA",     "PRESENCIAL"),
    (12, "EST012", "CVM", "LAE",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (13, "EST013", "MTY", "ITC",  "PRE", "2024-2", "ACTIVO",   "EN_LINEA"),
    (14, "EST014", "GDL", "ARQ",  "POS", "2024-2", "ACTIVO",   "EN_LINEA"),
    (15, "EST015", "MTY", "MED",  "PRE", "2024-1", "EGRESADO", "PRESENCIAL"),
    (16, "EST016", "CVM", "ITC",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (17, "EST017", "MTY", "LAE",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (18, "EST018", "GDL", "ITC",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (19, "EST019", "MTY", "ARQ",  "PRE", "2024-2", "BAJA",     "PRESENCIAL"),
    (20, "EST020", "CVM", "MED",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (21, "EST021", "MTY", "ITC",  "PRE", "2024-1", "ACTIVO",   None),          # null intencional
    (22, "EST022", "GDL", "LAE",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (23, "EST023", None,  "ITC",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),  # null en campus
    (24, "EST024", "MTY", "ITC",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (25, "EST025", "GDL", "MED",  "PRE", "2024-2", "EGRESADO", "PRESENCIAL"),
]

# Tabla de dimensión de campus (para simular JOINs)
DIM_CAMPUS = [
    ("MTY", "Monterrey"),
    ("GDL", "Guadalajara"),
    ("CVM", "Ciudad de México"),
    ("PUE", "Puebla"),   # existe en dim pero NO en estudiantes → sin_match = 0
]

# ── Denodo simulado ───────────────────────────────────────────────
# Igual que DWH pero con DIFERENCIAS INTENCIONALES para ver FAILs:
#   - EST005: campus cambiado de MTY a GDL  (discrepancia en catálogo)
#   - EST021: modalidad tiene valor distinto en lugar de null
#   - EST026: registro extra que no está en Oracle  (conteo diferente)
ESTUDIANTES_DENODO = [
    (1,  "EST001", "MTY", "ITC",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (2,  "EST002", "GDL", "LAE",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (3,  "EST003", "MTY", "ITC",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (4,  "EST004", "CVM", "ARQ",  "PRE", "2024-1", "BAJA",     "PRESENCIAL"),
    (5,  "EST005", "GDL", "MED",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),  # ← campus cambiado
    (6,  "EST006", "GDL", "ITC",  "POS", "2024-2", "ACTIVO",   "EN_LINEA"),
    (7,  "EST007", "MTY", "LAE",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (8,  "EST008", "CVM", "ITC",  "PRE", "2024-2", "EGRESADO", "PRESENCIAL"),
    (9,  "EST009", "MTY", "ARQ",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (10, "EST010", "GDL", "MED",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (11, "EST011", "MTY", "ITC",  "PRE", "2024-2", "BAJA",     "PRESENCIAL"),
    (12, "EST012", "CVM", "LAE",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (13, "EST013", "MTY", "ITC",  "PRE", "2024-2", "ACTIVO",   "EN_LINEA"),
    (14, "EST014", "GDL", "ARQ",  "POS", "2024-2", "ACTIVO",   "EN_LINEA"),
    (15, "EST015", "MTY", "MED",  "PRE", "2024-1", "EGRESADO", "PRESENCIAL"),
    (16, "EST016", "CVM", "ITC",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (17, "EST017", "MTY", "LAE",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (18, "EST018", "GDL", "ITC",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (19, "EST019", "MTY", "ARQ",  "PRE", "2024-2", "BAJA",     "PRESENCIAL"),
    (20, "EST020", "CVM", "MED",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (21, "EST021", "MTY", "ITC",  "PRE", "2024-1", "ACTIVO",   "HIBRIDO"),     # ← null → valor distinto
    (22, "EST022", "GDL", "LAE",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),
    (23, "EST023", None,  "ITC",  "PRE", "2024-1", "ACTIVO",   "PRESENCIAL"),
    (24, "EST024", "MTY", "ITC",  "POS", "2024-1", "ACTIVO",   "EN_LINEA"),
    (25, "EST025", "GDL", "MED",  "PRE", "2024-2", "EGRESADO", "PRESENCIAL"),
    (26, "EST026", "MTY", "ITC",  "PRE", "2024-2", "ACTIVO",   "PRESENCIAL"),  # ← registro extra
]

DIM_CAMPUS_DENODO = [
    ("MTY", "Monterrey"),
    ("GDL", "Guadalajara"),
    ("CVM", "Ciudad de México"),
    ("PUE", "Puebla"),
]


def crear_dwh():
    """Crea dwh_oracle.db simulando Oracle DWH."""
    if os.path.exists("dwh_oracle.db"):
        os.remove("dwh_oracle.db")

    con = sqlite3.connect("dwh_oracle.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE estudiantes (
            id               INTEGER PRIMARY KEY,
            clave_persona    TEXT NOT NULL,
            campus           TEXT,
            programa         TEXT NOT NULL,
            nivel            TEXT NOT NULL,
            periodo          TEXT NOT NULL,
            estatus          TEXT NOT NULL,
            modalidad        TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE dim_campus (
            clave_campus TEXT PRIMARY KEY,
            nombre_campus TEXT NOT NULL
        )
    """)

    cur.executemany(
        "INSERT INTO estudiantes VALUES (?,?,?,?,?,?,?,?)",
        ESTUDIANTES_DWH
    )
    cur.executemany(
        "INSERT INTO dim_campus VALUES (?,?)",
        DIM_CAMPUS
    )

    con.commit()
    con.close()
    print("✅ dwh_oracle.db creado con", len(ESTUDIANTES_DWH), "estudiantes y",
          len(DIM_CAMPUS), "campus")


def crear_denodo():
    """Crea denodo.db simulando la capa semántica Denodo."""
    if os.path.exists("denodo.db"):
        os.remove("denodo.db")

    con = sqlite3.connect("denodo.db")
    cur = con.cursor()

    # En Denodo los nombres van con espacios y minúsculas — aquí los normalizamos
    cur.execute("""
        CREATE TABLE vista_estudiante (
            id               INTEGER PRIMARY KEY,
            clave_persona    TEXT NOT NULL,
            campus           TEXT,
            programa         TEXT NOT NULL,
            nivel            TEXT NOT NULL,
            periodo          TEXT NOT NULL,
            estatus          TEXT NOT NULL,
            modalidad        TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE dim_campus (
            clave_campus  TEXT PRIMARY KEY,
            nombre_campus TEXT NOT NULL
        )
    """)

    cur.executemany(
        "INSERT INTO vista_estudiante VALUES (?,?,?,?,?,?,?,?)",
        ESTUDIANTES_DENODO
    )
    cur.executemany(
        "INSERT INTO dim_campus VALUES (?,?)",
        DIM_CAMPUS_DENODO
    )

    con.commit()
    con.close()
    print("✅ denodo.db creado con", len(ESTUDIANTES_DENODO), "estudiantes y",
          len(DIM_CAMPUS_DENODO), "campus")
    print()
    print("⚠️  Diferencias intencionales en Denodo para practicar FAILs:")
    print("   - EST005: campus cambiado MTY → GDL")
    print("   - EST021: modalidad NULL en Oracle, 'HIBRIDO' en Denodo")
    print("   - EST026: registro extra solo en Denodo (conteo diferente)")


if __name__ == "__main__":
    print("Creando bases de datos de prueba...\n")
    crear_dwh()
    crear_denodo()
    print("\n¡Listo! Ahora ejecuta los tests con pytest")
