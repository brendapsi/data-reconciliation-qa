# config.py
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DWH = os.path.join(BASE_DIR, "dwh_oracle.db")
DB_DENODO = os.path.join(BASE_DIR, "denodo.db")

CLAVES_PRIMARIAS = ["clave_persona"]  # lista para soportar claves compuestas

CAMPOS = [
    ("campus",    "campus"),
    ("programa",  "programa"),
    ("nivel",     "nivel"),
    ("periodo",   "periodo"),
    ("estatus",   "estatus"),
    ("modalidad", "modalidad"),
]
