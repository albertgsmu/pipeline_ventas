"""
FASE 4: ANÁLISIS CON SQL
=========================
Ejecutamos consultas sobre PostgreSQL para obtener
métricas de negocio.
"""

import os
os.environ['PGCLIENTENCODING'] = 'UTF8'

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import PASSWORD, USUARIO, HOST, PUERTO, BASE_DATOS



engine = create_engine(
    f'postgresql+psycopg2://{USUARIO}:{quote_plus(PASSWORD)}@{HOST}:{PUERTO}/{BASE_DATOS}',
    connect_args={'client_encoding': 'utf8'}
)


def mostrar(titulo, query):
    """
    Ejecuta una consulta SQL y la muestra bonita.
    pd.read_sql() convierte el resultado en DataFrame.
    """
    print("\n" + "=" * 65)
    print(f"  {titulo}")
    print("=" * 65)
    df = pd.read_sql(query, engine)
    print(df.to_string(index=False))
    return df


print("\n" + "🔷" * 32)
print("     DASHBOARD DE VENTAS - ANÁLISIS SQL")
print("🔷" * 32)


# ============================================
# KPI GENERALES
# ============================================
mostrar("📈 KPIs GENERALES DEL NEGOCIO", """
SELECT
    COUNT(*)                              AS total_ventas,
    COUNT(DISTINCT cliente_id)            AS clientes_activos,
    COUNT(DISTINCT producto_id)           AS productos_vendidos,
    SUM(cantidad)                         AS unidades_totales,
    ROUND(SUM(total), 2)                  AS ingresos_totales,
    ROUND(AVG(total), 2)                  AS ticket_promedio,
    ROUND(MAX(total), 2)                  AS venta_mas_alta
FROM ventas;
""")


# ============================================
# MÉTRICA 1: Ventas totales por mes
# ============================================
# GROUP BY agrupa las filas que comparten el mismo mes
# SUM/AVG/COUNT son funciones de agregación
mostrar("📅 1. VENTAS TOTALES POR MES", """
SELECT
    mes,
    nombre_mes,
    COUNT(*)             AS transacciones,
    SUM(cantidad)        AS unidades,
    ROUND(SUM(total), 2) AS ingresos,
    ROUND(AVG(total), 2) AS ticket_promedio
FROM ventas
GROUP BY mes, nombre_mes
ORDER BY mes;
""")


# ============================================
# MÉTRICA 2: Producto más vendido
# ============================================
# JOIN conecta la tabla de hechos (ventas)
# con la dimensión (productos) usando producto_id
mostrar("🏆 2. TOP 10 PRODUCTOS MÁS VENDIDOS", """
SELECT
    p.nombre_producto,
    p.categoria,
    SUM(v.cantidad)        AS unidades_vendidas,
    COUNT(v.venta_id)      AS veces_comprado,
    ROUND(SUM(v.total), 2) AS ingresos
FROM ventas v
JOIN productos p ON v.producto_id = p.producto_id
GROUP BY p.nombre_producto, p.categoria
ORDER BY ingresos DESC
LIMIT 10;
""")


# ============================================
# MÉTRICA 3: Clientes con más compras
# ============================================
mostrar("👑 3. TOP CLIENTES (mejores compradores)", """
SELECT
    c.nombre_cliente,
    c.ciudad,
    COUNT(v.venta_id)      AS num_compras,
    ROUND(SUM(v.total), 2) AS total_gastado,
    ROUND(AVG(v.total), 2) AS promedio_compra,
    MIN(v.fecha)           AS primera_compra,
    MAX(v.fecha)           AS ultima_compra
FROM ventas v
JOIN clientes c ON v.cliente_id = c.cliente_id
GROUP BY c.nombre_cliente, c.ciudad
ORDER BY total_gastado DESC;
""")


# ============================================
# MÉTRICA 4: Promedio de venta por cliente
# ============================================
# Subconsulta: primero agrupamos por cliente,
# luego calculamos estadísticas sobre ese resultado
mostrar("💵 4. PROMEDIO DE GASTO POR CLIENTE", """
SELECT
    ROUND(AVG(gasto_total), 2)  AS gasto_promedio_cliente,
    ROUND(AVG(num_compras), 2)  AS compras_promedio_cliente,
    ROUND(MIN(gasto_total), 2)  AS gasto_minimo,
    ROUND(MAX(gasto_total), 2)  AS gasto_maximo
FROM (
    SELECT
        cliente_id,
        SUM(total)  AS gasto_total,
        COUNT(*)    AS num_compras
    FROM ventas
    GROUP BY cliente_id
) AS resumen;
""")


# ============================================
# MÉTRICA 5: Ventas por categoría
# ============================================
# Subconsulta escalar para calcular el % del total
mostrar("📦 5. VENTAS POR CATEGORÍA", """
SELECT
    p.categoria,
    COUNT(v.venta_id)      AS transacciones,
    SUM(v.cantidad)        AS unidades,
    ROUND(SUM(v.total), 2) AS ingresos,
    ROUND(
        SUM(v.total) * 100.0 / (SELECT SUM(total) FROM ventas),
        2
    ) AS porcentaje_ingresos
FROM ventas v
JOIN productos p ON v.producto_id = p.producto_id
GROUP BY p.categoria
ORDER BY ingresos DESC;
""")


# ============================================
# MÉTRICA 6: Ventas por ciudad
# ============================================
mostrar("🌎 6. VENTAS POR CIUDAD", """
SELECT
    c.ciudad,
    COUNT(DISTINCT c.cliente_id) AS clientes,
    COUNT(v.venta_id)            AS transacciones,
    ROUND(SUM(v.total), 2)       AS ingresos
FROM ventas v
JOIN clientes c ON v.cliente_id = c.cliente_id
GROUP BY c.ciudad
ORDER BY ingresos DESC;
""")


# ============================================
# MÉTRICA 7: Día de la semana con más ventas
# ============================================
mostrar("📆 7. RENDIMIENTO POR DÍA DE LA SEMANA", """
SELECT
    dia_semana,
    COUNT(*)             AS ventas,
    ROUND(SUM(total), 2) AS ingresos,
    ROUND(AVG(total), 2) AS ticket_promedio
FROM ventas
GROUP BY dia_semana
ORDER BY ingresos DESC;
""")


# ============================================
# BONUS: Window Function (nivel intermedio)
# ============================================
# RANK() asigna un puesto dentro de cada grupo
# PARTITION BY = "reinicia el ranking por cada categoría"
mostrar("⭐ BONUS: PRODUCTO #1 DE CADA CATEGORÍA", """
WITH ranking AS (
    SELECT
        p.categoria,
        p.nombre_producto,
        SUM(v.total) AS ingresos,
        RANK() OVER (
            PARTITION BY p.categoria
            ORDER BY SUM(v.total) DESC
        ) AS puesto
    FROM ventas v
    JOIN productos p ON v.producto_id = p.producto_id
    GROUP BY p.categoria, p.nombre_producto
)
SELECT categoria, nombre_producto, ROUND(ingresos, 2) AS ingresos
FROM ranking
WHERE puesto = 1
ORDER BY ingresos DESC;
""")


# ============================================
# BONUS 2: Crecimiento mes a mes
# ============================================
# LAG() mira el valor de la fila anterior
mostrar("📈 BONUS: CRECIMIENTO MES A MES", """
WITH mensual AS (
    SELECT mes, nombre_mes, SUM(total) AS ingresos
    FROM ventas
    GROUP BY mes, nombre_mes
)
SELECT
    mes,
    nombre_mes,
    ROUND(ingresos, 2)                        AS ingresos,
    ROUND(LAG(ingresos) OVER (ORDER BY mes), 2) AS mes_anterior,
    ROUND(
        (ingresos - LAG(ingresos) OVER (ORDER BY mes))
        * 100.0 / LAG(ingresos) OVER (ORDER BY mes),
        1
    ) AS crecimiento_pct
FROM mensual
ORDER BY mes;
""")


print("\n" + "=" * 65)
print("  ✅ ANÁLISIS COMPLETADO")
print("=" * 65)