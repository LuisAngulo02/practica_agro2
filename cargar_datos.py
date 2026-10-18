import pandas as pd
from sqlalchemy import create_engine

# 1. Configuración de conexión a PostgreSQL
USUARIO = 'postgres'
PASSWORD = 'luis123'
HOST = 'localhost'
PUERTO = '5432'
BASE_DATOS = 'clima_agro'

cadena_conexion = f'postgresql://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BASE_DATOS}'
engine = create_engine(cadena_conexion)

# 2. Detectar dónde termina el encabezado
archivo_csv = 'datos_guayas.csv'
filas_a_saltar = 0

with open(archivo_csv, 'r') as f:
    for i, linea in enumerate(f):
        if '-END HEADER-' in linea:
            filas_a_saltar = i + 1
            break

# 3. Leer el CSV separado por comas
df = pd.read_csv(archivo_csv, skiprows=filas_a_saltar, sep=',')
df.columns = [col.strip().lower() for col in df.columns]

# 4. Convertir YEAR y DOY a Fecha real
fechas_dt = pd.to_datetime(
    df['year'].astype(str) + '-' + df['doy'].astype(str),
    format='%Y-%j'
)

df['fecha'] = fechas_dt.dt.date
df['anio'] = fechas_dt.dt.year
df['mes'] = fechas_dt.dt.month
df['dia'] = fechas_dt.dt.day

df_final = df[['fecha', 'anio', 'mes', 'dia', 't2m', 'rh2m']]

# 5. Guardar en PostgreSQL
df_final.to_sql('lecturas', engine, if_exists='append', index=False)
print("¡Datos cargados exitosamente en la tabla 'lecturas' de PostgreSQL!")
print(df_final.head())