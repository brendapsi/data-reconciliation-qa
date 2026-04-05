#imports
import sqlite3
import pandas as pd
#constantes
CAMPOS = [
    ("campus",    "campus"),
    ("programa",  "programa"),
    ("nivel",     "nivel"),
    ("periodo",   "periodo"),
    ("estatus",   "estatus"),
    ("modalidad", "modalidad"),
]

#funciones
def validar_conteo(dwh, den, campos):
    for campo_dwh, campo_den in campos:        
        df_dwh = pd.read_sql_query(f"SELECT COUNT(*) AS total FROM estudiantes WHERE {campo_dwh} IS NOT NULL", dwh)       
        df_den = pd.read_sql_query(f"SELECT COUNT(*) AS total FROM vista_estudiante WHERE {campo_den} IS NOT NULL", den)        

        cnt_dwh = int(df_dwh["total"].iloc[0])
        cnt_den = int(df_den["total"].iloc[0])
        
        if cnt_dwh == cnt_den:               
            print(f"✅ PASS | DWH={campo_dwh:<15} Denodo={campo_den:<20} | {cnt_dwh}")            
        else:                               
            print(f"❌ FAIL | DWH={campo_dwh:<15} Denodo={campo_den:<20} | DWH={cnt_dwh} Denodo={cnt_den} Diff={abs(cnt_dwh-cnt_den)}")            

def validar_nulos(dwh, den, campos):
    for campo_dwh, campo_den in campos:    
        df_dwh = pd.read_sql_query(f"SELECT COUNT(*) AS nulos FROM estudiantes WHERE {campo_dwh} IS NULL", dwh)       
        df_den = pd.read_sql_query(f"SELECT COUNT(*) AS nulos FROM vista_estudiante WHERE {campo_den} IS NULL", den)       

        nulos_dwh = int(df_dwh["nulos"].iloc[0])
        nulos_den = int(df_den["nulos"].iloc[0])
        
        if nulos_dwh == nulos_den:                 
            print(f"✅ PASS | DWH={campo_dwh:<15} Denodo={campo_den:<20} | {nulos_dwh}")          
        else:                                 
            print(f"❌ FAIL | DWH={campo_dwh:<15} Denodo={campo_den:<20} | DWH={nulos_dwh} Denodo={nulos_den} Diff={abs(nulos_dwh-nulos_den)}")    

def validar_catalogo(dwh, den, campos):
    for campo_dwh, campo_den in campos:      
        #print(f"Procesando: {campo_dwh}")
        df_dwh = pd.read_sql_query(f"SELECT DISTINCT({campo_dwh}) AS valor FROM estudiantes ORDER BY {campo_dwh}", dwh)       
        df_den = pd.read_sql_query(f"SELECT DISTINCT({campo_den}) AS valor FROM vista_estudiante ORDER BY {campo_den}", den)        

        vals_dwh = set(df_dwh["valor"].tolist())
        vals_den = set(df_den["valor"].tolist())

        solo_en_dwh = vals_dwh - vals_den
        solo_en_den = vals_den - vals_dwh
        
        if len(solo_en_dwh) == len(solo_en_den) ==0 :           
            print(f"✅ PASS | DWH={campo_dwh:<15} Denodo={campo_den:<20} | {len(vals_dwh)} valores únicos")            
        else:                                  
            print(f"❌ FAIL | DWH={campo_dwh:<15} Denodo={campo_den:<20} | Solo en DWH={solo_en_dwh} | Solo en Denodo={solo_en_den}")  

def validar_tiposdedato(dwh,den,campos):
    for campo_dwh, campo_den in campos:     
        df_dwh = pd.read_sql_query(f"SELECT typeof({campo_dwh}) AS tipo FROM estudiantes LIMIT 1", dwh)      
        df_den = pd.read_sql_query(f"SELECT typeof({campo_den}) AS tipo FROM vista_estudiante LIMIT 1", den)

        tipo_dwh = df_dwh["tipo"].iloc[0] #EXTRAE LOS VALORES DEL DF
        tipo_den = df_den["tipo"].iloc[0]

        if tipo_dwh == tipo_den:
            print(f"✅ PASS | DWH={campo_dwh:<15} Denodo={campo_den:<20} | {tipo_dwh} es el tipo de dato")             
        else:                              
            print(f"❌ FAIL | DWH={campo_dwh:<15} Denodo={campo_den:<20} | Tipo de dato DWH={tipo_dwh} | Tipo de dato en Denodo={tipo_den}")  

def main():
    # 1. conectar
    dwh = sqlite3.connect("dwh_oracle.db")
    den = sqlite3.connect("denodo.db")
    print("✅ Conectada a DWH y Denodo")
    # 2. llamar a las 3 funciones
    print("\n── Conteo de registros no nulos ──────────────────────────")
    validar_conteo(dwh,den,CAMPOS)
    print("\n── Nulos por campo ───────────────────────────────────────")
    validar_nulos(dwh,den,CAMPOS)
    print("\n── Catálogo de valores permitidos ────────────────────────")
    validar_catalogo(dwh,den,CAMPOS)
    print("\n── Coincidencia de tipos de dato ─────────────────────────")
    validar_tiposdedato(dwh,den,CAMPOS)
    # 3. cerrar conexiones
    dwh.close()
    den.close()

if __name__ == "__main__":
    main()