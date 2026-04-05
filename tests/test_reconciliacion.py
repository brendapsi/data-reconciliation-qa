import sqlite3
import pandas as pd
import pytest
import random
from config import CAMPOS, DB_DWH, DB_DENODO, CLAVES_PRIMARIAS

# ── Conexiones ────────────────────────────────────────────────────
@pytest.fixture
def conexiones():
    dwh = sqlite3.connect(DB_DWH)
    den = sqlite3.connect(DB_DENODO)
    yield dwh, den
    dwh.close()
    den.close()

# ── Primer test ───────────────────────────────────────────────────
def test_conteo_campus(conexiones):
    dwh, den = conexiones

    df_dwh = pd.read_sql_query("SELECT COUNT(*) AS total FROM estudiantes WHERE campus IS NOT NULL", dwh)
    df_den = pd.read_sql_query("SELECT COUNT(*) AS total FROM vista_estudiante WHERE campus IS NOT NULL", den)

    cnt_dwh = int(df_dwh["total"].iloc[0])
    cnt_den = int(df_den["total"].iloc[0])

    assert cnt_dwh == cnt_den, f"Conteo diferente en campus: DWH={cnt_dwh} Denodo={cnt_den}"

# ── Segundo test ──────────────────────────────────────────────────
def test_conteo_modalidad(conexiones):
    dwh, den = conexiones

    df_dwh = pd.read_sql_query("SELECT COUNT(*) AS total FROM estudiantes WHERE modalidad IS NOT NULL", dwh)
    df_den = pd.read_sql_query("SELECT COUNT(*) AS total FROM vista_estudiante WHERE modalidad IS NOT NULL", den)

    cnt_dwh = int(df_dwh["total"].iloc[0])
    cnt_den = int(df_den["total"].iloc[0])

    assert cnt_dwh == cnt_den, f"Conteo diferente en modalidad: DWH={cnt_dwh} Denodo={cnt_den}"

# ── Conteo total test ───────────────────────────────────────────────────

def test_conteo_total(conexiones):
    dwh, den = conexiones
      
    df_dwh = pd.read_sql_query("SELECT COUNT(*) AS total FROM estudiantes", dwh)       
    df_den = pd.read_sql_query("SELECT COUNT(*) AS total FROM vista_estudiante", den)        

    cnt_dwh = int(df_dwh["total"].iloc[0])
    cnt_den = int(df_den["total"].iloc[0])
        
    assert cnt_dwh == cnt_den, f"Conteo total en DWH={cnt_dwh} | en Denodo={cnt_den} | Diferencia={abs(cnt_dwh-cnt_den)}"    

# ── Tercer test ───────────────────────────────────────────────────
def test_validar_nulos(conexiones):
    dwh, den = conexiones

    for campo_dwh, campo_den in CAMPOS:    
        df_dwh = pd.read_sql_query(f"SELECT COUNT(*) AS nulos FROM estudiantes WHERE {campo_dwh} IS NULL", dwh)       
        df_den = pd.read_sql_query(f"SELECT COUNT(*) AS nulos FROM vista_estudiante WHERE {campo_den} IS NULL", den)       

        nulos_dwh = int(df_dwh["nulos"].iloc[0])
        nulos_den = int(df_den["nulos"].iloc[0])
          
        assert nulos_dwh == nulos_den, f"Nulos diferentes en '{campo_dwh}': DWH={nulos_dwh} | '{campo_den}': Denodo={nulos_den}"           
        
# ── Cuarto test ───────────────────────────────────────────────────
def test_validar_catalogo(conexiones):
    dwh, den = conexiones

    for campo_dwh, campo_den in CAMPOS:      
        df_dwh = pd.read_sql_query(f"SELECT DISTINCT({campo_dwh}) AS valor FROM estudiantes ORDER BY {campo_dwh}", dwh)       
        df_den = pd.read_sql_query(f"SELECT DISTINCT({campo_den}) AS valor FROM vista_estudiante ORDER BY {campo_den}", den)        

        vals_dwh = set(df_dwh["valor"].dropna().tolist())
        vals_den = set(df_den["valor"].dropna().tolist())

        solo_en_dwh = vals_dwh - vals_den
        solo_en_den = vals_den - vals_dwh
        
        assert len(solo_en_dwh) == len(solo_en_den) == 0, \
            f"Catálogo diferente en campo '{campo_dwh}': solo en DWH={solo_en_dwh} | '{campo_den}': solo en Denodo={solo_en_den}"

# ── Quinto test ───────────────────────────────────────────────────
def test_validar_tiposdedato(conexiones):
    dwh, den = conexiones

    for campo_dwh, campo_den in CAMPOS:     
        df_dwh = pd.read_sql_query(f"SELECT typeof({campo_dwh}) AS tipo FROM estudiantes LIMIT 1", dwh)      
        df_den = pd.read_sql_query(f"SELECT typeof({campo_den}) AS tipo FROM vista_estudiante LIMIT 1", den)

        tipo_dwh = df_dwh["tipo"].iloc[0] #EXTRAE LOS VALORES DEL DF
        tipo_den = df_den["tipo"].iloc[0]

        assert tipo_dwh == tipo_den, f"Tipos de dato diferentes en campo '{campo_dwh}': {tipo_dwh} | '{campo_den}': {tipo_den}"

# ── Conteo por campo ──────────────────────────────────────────────
def test_conteo_por_campo(conexiones):
    dwh, den = conexiones

    for campo_dwh, campo_den in CAMPOS:     
        df_dwh = pd.read_sql_query(f"SELECT {campo_dwh} AS valor, COUNT(*) AS total FROM estudiantes GROUP BY {campo_dwh} ORDER BY {campo_dwh}", dwh)      
        df_den = pd.read_sql_query(f"SELECT {campo_den} AS valor, COUNT(*) AS total FROM vista_estudiante GROUP BY {campo_den} ORDER BY {campo_den}", den)

        merged = df_dwh.merge(df_den, on="valor", suffixes=("_dwh", "_den"), how="outer")
        diferencias = merged[merged["total_dwh"] != merged["total_den"]]
        #print(diferencias.to_string())  

        assert len(diferencias)==0, \
            f"Conteo por categoría difiere en campo '{campo_dwh}', '{campo_den}':\n{diferencias.to_string()}"

# ── Longitud ──────────────────────────────────────────────
def test_longitud(conexiones):
    dwh, den = conexiones

    for campo_dwh, campo_den in CAMPOS:     
        df_dwh = pd.read_sql_query(f"SELECT MAX(LENGTH({campo_dwh})) AS longitud_max FROM estudiantes", dwh)      
        df_den = pd.read_sql_query(f"SELECT MAX(LENGTH({campo_den})) AS longitud_max FROM vista_estudiante", den)

        longitud_dwh = int(df_dwh["longitud_max"].iloc[0])
        longitud_den = int(df_den["longitud_max"].iloc[0])

        assert longitud_dwh == longitud_den, \
            f"Longitud máxima difiere en campo '{campo_dwh}':{longitud_dwh}, '{campo_den}':{longitud_den}"

# ── Muestreo ──────────────────────────────────────────────
def test_muestreo(conexiones):
    dwh, den = conexiones

    claves_str = ", ".join(CLAVES_PRIMARIAS)
    df_claves = pd.read_sql_query(f"SELECT {claves_str} FROM estudiantes", dwh)

    # Convierte cada fila a una tupla (clave1, clave2) o (clave1,) si es simple
    random.seed(42)
    muestra = random.sample(list(df_claves.itertuples(index=False, name=None)), 5) #muestra random de combinaciones de primary keys

    for fila_clave in muestra:
        where = " AND ".join([f"{col} = ?" for col in CLAVES_PRIMARIAS])
        valores = tuple(fila_clave)
    
        df_dwh_fila = pd.read_sql_query(f"SELECT * FROM estudiantes WHERE {where}", dwh, params=valores)
        df_den_fila = pd.read_sql_query(f"SELECT * FROM vista_estudiante WHERE {where}", den, params=valores)

        for campo_dwh, campo_den in CAMPOS:
            val_dwh = df_dwh_fila[campo_dwh].iloc[0]
            val_den = df_den_fila[campo_den].iloc[0]
            assert val_dwh == val_den, \
                f"Muestreo: clave primaria {valores} difiere en '{campo_dwh}'/'{campo_den}': DWH={val_dwh} Denodo={val_den}"
