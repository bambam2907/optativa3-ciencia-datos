# Pipeline ETL de ventas con esquema estrella

Práctica de Ingeniería de Datos (Optativa 3 · Ciencia de Datos, UNE).
El script `etl.py` extrae ventas de un CSV, las limpia, crea la feature `total`, las modela en un **esquema estrella** y las carga a una base **SQLite** que se puede consultar con SQL.

```
ventas.csv  ──►  EXTRACT  ──►  TRANSFORM  ──►  LOAD  ──►  almacen.db
 (fuente)        pandas        limpieza +      SQLite     dim_categoria
                               feature +                  fact_ventas
                               esquema estrella
```

## Estructura del proyecto

| Archivo | Qué es |
| --- | --- |
| `ventas.csv` | Datos fuente: 15 ventas con `producto, categoria, precio, cantidad` (incluye errores a propósito) |
| `etl.py` | El pipeline completo |
| `requirements.txt` | Dependencias (`pandas`; `sqlite3` ya viene con Python) |
| `almacen.db` | Base generada al correr el script (no se sube al repo) |

## Cómo correrlo

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python etl.py
```

## Fases del pipeline

### 1. EXTRACT — leer la fuente
`pd.read_csv("ventas.csv")` carga el archivo en un DataFrame. En un caso real la fuente podría ser una API, otra base de datos o archivos de un sistema de ventas; aquí es un CSV.

### 2. TRANSFORM — limpiar, enriquecer y modelar
1. **Limpieza.** El CSV trae errores típicos de captura:
   - `" electrónica "` con espacios y minúscula, y `"HOGAR"` en mayúsculas. Se corrigen con `str.strip().str.capitalize()`.
   - Una venta duplicada (`Mouse inalámbrico`). Se elimina con `drop_duplicates()`.
   - También se descartan filas con nulos o con precio/cantidad ≤ 0.
2. **Feature nueva.** `total = precio × cantidad`, el ingreso de cada venta.
3. **Modelado dimensional.** Se separan los datos en dos tablas (ver abajo).

**¿Por qué importa la limpieza?** Sin ella, la consulta final muestra 6 categorías en vez de 4: "Hogar" y "HOGAR" salen separadas y Hogar reporta $2,857 en lugar de $4,253 (33 % menos), mientras que Electrónica cuenta el mouse dos veces.

### 3. LOAD — cargar al almacén
`to_sql()` escribe ambas tablas en `almacen.db`. Con `if_exists="replace"` el pipeline es **idempotente**: puedes correrlo varias veces y siempre obtienes el mismo resultado, sin filas duplicadas.

Al final, el script valida que la suma de `total` en la base coincida con la calculada en pandas.

## Esquema estrella

```
                 ┌───────────────────┐
                 │   dim_categoria   │
                 │───────────────────│
                 │ cat_id (PK)       │
                 │ categoria         │
                 └─────────▲─────────┘
                           │ 1 : N
                 ┌─────────┴─────────┐
                 │    fact_ventas    │
                 │───────────────────│
                 │ venta_id (PK)     │
                 │ producto          │
                 │ cat_id (FK)       │
                 │ precio            │
                 │ cantidad          │
                 │ total             │
                 └───────────────────┘
```

- **`fact_ventas` (tabla de hechos):** una fila por venta. Guarda las **métricas numéricas** (`precio`, `cantidad`, `total`) y la **llave foránea** `cat_id` que apunta a la dimensión.
- **`dim_categoria` (dimensión):** una fila por categoría, con su llave sustituta `cat_id`. Describe el "qué" de cada venta.

Así el nombre de la categoría se guarda una sola vez y las consultas analíticas se resuelven con un solo `JOIN`. Con más datos se agregarían otras dimensiones alrededor de la misma tabla de hechos (`dim_fecha`, `dim_producto`, `dim_tienda`), formando la "estrella".

## Consulta de verificación

```sql
SELECT d.categoria, COUNT(*) AS num_ventas, SUM(f.total) AS ingresos
FROM fact_ventas f
JOIN dim_categoria d ON f.cat_id = d.cat_id
GROUP BY d.categoria
ORDER BY ingresos DESC;
```

### Salida

```
[EXTRACT]   15 filas leídas de ventas.csv
[TRANSFORM] 1 fila(s) descartada(s) en la limpieza
[TRANSFORM] dim_categoria: 4 filas | fact_ventas: 14 filas
[LOAD]      Tablas cargadas en almacen.db

Ingresos por categoría:
  categoria  num_ventas  ingresos
Electrónica           4    7334.5
       Ropa           3    4471.0
      Hogar           4    4253.0
  Papelería           3    2539.0

Validación OK: ingreso total = $18,597.50 MXN
```

![Salida en la terminal de VS Code](captura_salida.png)
