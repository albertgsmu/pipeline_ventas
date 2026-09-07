"""
FASE 2: LIMPIEZA DE DATOS
========================
Leemos los CSV, detectamos problemas y los corregimos.
"""

import pandas as pd
import os

print("=" * 50)
print("FASE 2: LIMPIEZA DE DATOS")
print("=" * 50)

# ============================================
# 1. EXTRAER (leer CSV)
# ============================================
print("\n[1] Leyendo archivos CSV...")

productos = pd.read_csv('data/productos.csv')
clientes = pd.read_csv('data/clientes.csv')
ventas = pd.read_csv('data/ventas.csv')

print(f"  Productos: {len(productos)} filas")
print(f"  Clientes:  {len(clientes)} filas")
print(f"  Ventas:    {len(ventas)} filas")

# ============================================
# 2. DIAGNÓSTICO (ver problemas)
# ============================================
print("\n[2] Diagnóstico de VENTAS (antes de limpiar):")
print(f"  Nulos por columna:")
print(ventas.isnull().sum().to_string())
print(f"  Duplicados: {ventas.duplicated().sum()}")
print(f"  Cantidades negativas: {(ventas['cantidad'] < 0).sum()}")

# ============================================
# 3. LIMPIAR VENTAS
# ============================================
print("\n[3] Limpiando ventas...")

df = ventas.copy()
inicial = len(df)

# 3.1 Eliminar duplicados
antes = len(df)
df = df.drop_duplicates(keep='first')
print(f"  Duplicados eliminados: {antes - len(df)}")

# 3.2 Eliminar filas sin cliente_id (no sabemos quién compró)
nulos_cliente = df['cliente_id'].isnull().sum()
df = df.dropna(subset=['cliente_id'])
print(f"  Filas sin cliente eliminadas: {nulos_cliente}")

# 3.3 Rellenar cantidad nula con 1
nulos_cant = df['cantidad'].isnull().sum()
df['cantidad'] = df['cantidad'].fillna(1)
print(f"  Cantidades nulas rellenadas con 1: {nulos_cant}")

# 3.4 Corregir cantidades negativas (valor absoluto)
negativos = (df['cantidad'] < 0).sum()
df['cantidad'] = df['cantidad'].abs()
print(f"  Cantidades negativas corregidas: {negativos}")

# 3.5 Recalcular total = cantidad * precio
df['total'] = (df['cantidad'] * df['precio_unitario']).round(2)
print("  Totales recalculados")

# 3.6 Tipos de datos correctos
df['fecha'] = pd.to_datetime(df['fecha'])
df['cliente_id'] = df['cliente_id'].astype(int)
df['producto_id'] = df['producto_id'].astype(int)
df['cantidad'] = df['cantidad'].astype(int)
print("  Tipos de datos corregidos")

# 3.7 Columnas extra para análisis
df['anio'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df['nombre_mes'] = df['fecha'].dt.strftime('%B')
df['dia_semana'] = df['fecha'].dt.day_name()
print("  Columnas agregadas: anio, mes, nombre_mes, dia_semana")

ventas_clean = df

# ============================================
# 4. LIMPIAR CLIENTES Y PRODUCTOS
# ============================================
print("\n[4] Limpiando clientes y productos...")

clientes_clean = clientes.drop_duplicates().copy()
clientes_clean['nombre_cliente'] = clientes_clean['nombre_cliente'].str.title()
clientes_clean['ciudad'] = clientes_clean['ciudad'].str.title()
clientes_clean['email'] = clientes_clean['email'].str.lower()
clientes_clean['fecha_registro'] = pd.to_datetime(clientes_clean['fecha_registro'])

productos_clean = productos.drop_duplicates().copy()
productos_clean['categoria'] = productos_clean['categoria'].str.title()

print(f"  Clientes limpios: {len(clientes_clean)}")
print(f"  Productos limpios: {len(productos_clean)}")

# ============================================
# 5. VERIFICACIÓN FINAL
# ============================================
print("\n[5] Verificación final de VENTAS:")
print(f"  Filas iniciales:  {inicial}")
print(f"  Filas finales:    {len(ventas_clean)}")
print(f"  Nulos restantes:  {ventas_clean.isnull().sum().sum()}")
print(f"  Duplicados:       {ventas_clean.duplicated().sum()}")

# ============================================
# 6. GUARDAR DATOS LIMPIOS
# ============================================
print("\n[6] Guardando datos limpios...")

productos_clean.to_csv('data/productos_clean.csv', index=False)
clientes_clean.to_csv('data/clientes_clean.csv', index=False)
ventas_clean.to_csv('data/ventas_clean.csv', index=False)

print("  data/productos_clean.csv")
print("  data/clientes_clean.csv")
print("  data/ventas_clean.csv")

print("\n" + "=" * 50)
print("LIMPIEZA COMPLETADA")
print("=" * 50)