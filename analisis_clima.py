import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Configuración de conexión
USUARIO = 'postgres'
PASSWORD = 'luis123'
HOST = 'localhost'
PUERTO = '5432'
BASE_DATOS = 'clima_agro'

engine = create_engine(f'postgresql://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BASE_DATOS}')

# 1. Leer los datos desde PostgreSQL usando pandas.read_sql()
consulta = "SELECT fecha, t2m, rh2m FROM lecturas ORDER BY fecha ASC;"
df = pd.read_sql(consulta, engine)

# 2. Mostrar los primeros registros con df.head() y estadísticas con df.describe()
print("=== PRIMEROS REGISTROS (df.head()) ===")
print(df.head())

print("\n=== ESTADÍSTICAS DESCRIPTIVAS (df.describe()) ===")
print(df.describe())

# Días con mayor humedad y correlación para las preguntas de la Sesión 3
top_humedad = df.sort_values(by='rh2m', ascending=False).head(5)
print("\n=== TOP 5 DÍAS CON MAYOR HUMEDAD ===")
print(top_humedad[['fecha', 'rh2m', 't2m']])

correlacion = df['t2m'].corr(df['rh2m'])
print(f"\nCoeficiente de correlación (Pearson) entre T2M y RH2M: {correlacion:.4f}")

# 3. Crear un gráfico de líneas con matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Gráfico de Temperatura
ax1.plot(df['fecha'], df['t2m'], color='#d95f02', marker='o', linewidth=2, label='Temperatura a 2m (T2M)')
ax1.set_title('Tendencia de Temperatura y Humedad Relativa - Guayas (Junio 2024)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Temperatura (°C)', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='upper right')

# Gráfico de Humedad Relativa
ax2.plot(df['fecha'], df['rh2m'], color='#1f78b4', marker='s', linewidth=2, label='Humedad Relativa a 2m (RH2M)')
ax2.set_xlabel('Fecha', fontsize=11)
ax2.set_ylabel('Humedad Relativa (%)', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='upper right')

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_clima_guayas.png', dpi=300)
plt.show()