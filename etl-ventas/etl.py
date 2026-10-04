"""
Pipeline ETL: ventas.csv -> almacen.db (SQLite) con esquema estrella.

Uso:
    python etl.py
"""
from pathlib import Path
import sqlite3

import pandas as pd

# Rutas relativas al script, así funciona aunque lo corras desde otra carpeta
BASE = Path(__file__).resolve().parent
CSV = BASE / "ventas.csv"
DB = BASE / "almacen.db"


# ===== EXTRACT: leer los datos de la fuente =====
df = pd.read_csv(CSV, encoding="utf-8")
print(f"[EXTRACT]   {len(df)} filas leídas de {CSV.name}")


# ===== TRANSFORM: limpiar y crear una feature nueva =====
# 1) Limpieza: espacios sobrantes y mayúsculas inconsistentes
#    (" electrónica " y "HOGAR" se vuelven "Electrónica" y "Hogar")
df["producto"] = df["producto"].str.strip()
df["categoria"] = df["categoria"].str.strip().str.capitalize()

# 2) Quitar filas incompletas, duplicadas o con valores imposibles
filas_antes = len(df)
df = df.dropna(subset=["producto", "categoria", "precio", "cantidad"])
df = df.drop_duplicates()
df = df[(df["precio"] > 0) & (df["cantidad"] > 0)]
print(f"[TRANSFORM] {filas_antes - len(df)} fila(s) descartada(s) en la limpieza")

# 3) Feature nueva: ingreso por venta
df["total"] = df["precio"] * df["cantidad"]

# 4) Modelado dimensional: esquema estrella
#    Dimensión: una fila por categoría, con su llave sustituta cat_id
dim_categoria = pd.DataFrame({"categoria": sorted(df["categoria"].unique())})
dim_categoria["cat_id"] = range(1, len(dim_categoria) + 1)
dim_categoria = dim_categoria[["cat_id", "categoria"]]

#    Hechos: métricas numéricas + la llave que apunta a la dimensión
fact = df.merge(dim_categoria, on="categoria")
fact_ventas = fact[["producto", "cat_id", "precio", "cantidad", "total"]].copy()
fact_ventas.insert(0, "venta_id", range(1, len(fact_ventas) + 1))
print(f"[TRANSFORM] dim_categoria: {len(dim_categoria)} filas | "
      f"fact_ventas: {len(fact_ventas)} filas")


# ===== LOAD: cargar a SQLite =====
conn = sqlite3.connect(DB)
dim_categoria.to_sql("dim_categoria", conn, if_exists="replace", index=False)
fact_ventas.to_sql("fact_ventas", conn, if_exists="replace", index=False)
print(f"[LOAD]      Tablas cargadas en {DB.name}")


# ===== Consulta analítica (esquema estrella en acción) =====
query = """
SELECT d.categoria,
       COUNT(*)     AS num_ventas,
       SUM(f.total) AS ingresos
FROM fact_ventas f
JOIN dim_categoria d ON f.cat_id = d.cat_id
GROUP BY d.categoria
ORDER BY ingresos DESC
"""
resultado = pd.read_sql(query, conn)
print("\nIngresos por categoría:")
print(resultado.to_string(index=False))

# Validación: lo que quedó en la base debe cuadrar con lo que calculó pandas
total_db = pd.read_sql("SELECT SUM(total) AS t FROM fact_ventas", conn)["t"].iloc[0]
assert abs(total_db - df["total"].sum()) < 0.01, "Los totales no coinciden"
print(f"\nValidación OK: ingreso total = ${total_db:,.2f} MXN")

conn.close()
