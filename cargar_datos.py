"""
FASE 3: CARGA DE DATOS A POSTGRESQL (Versión corregida de codificación)
=====================================================================
"""

import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus # Importante para caracteres especiales
from config import PASSWORD, USUARIO, HOST, PUERTO, BASE_DATOS


# Codificamos la contraseña para evitar errores con @, #, ñ, tildes, etc.
password_safe = quote_plus(PASSWORD)

# Crear URL de conexión segura
DATABASE_URL = f'postgresql://{USUARIO}:{password_safe}@{HOST}:{PUERTO}/{BASE_DATOS}'

print("=" * 50)
print("FASE 3: CARGA DE DATOS A POSTGRESQL")
print("=" * 50)

try:
    # Crear el motor de conexión
    engine = create_engine(DATABASE_URL)
    
    # Probar la conexión
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("\n✅ Conexión exitosa a PostgreSQL")
    
except Exception as e:
    print(f"\n❌ Error de conexión.")
    print("💡 Posibles causas:")
    print("   1. La contraseña escrita en PASSWORD no coincide con la de PostgreSQL.")
    print("   2. La base de datos 'pipeline_ventas' no está creada en pgAdmin.")
    print(f"   Detalle técnico: {e}")
    exit()

# ============================================
# 2. CREAR LAS TABLAS CON ESTRUCTURA (DDL)
# ============================================
print("\n[1] Creando la estructura de tablas (DDL)...")

sql_crear_tablas = """
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS productos CASCADE;

CREATE TABLE productos (
    producto_id INT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL
);

CREATE TABLE clientes (
    cliente_id INT PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    ciudad VARCHAR(50),
    fecha_registro DATE
);

CREATE TABLE ventas (
    venta_id INT PRIMARY KEY,
    fecha DATE NOT NULL,
    cliente_id INT REFERENCES clientes(cliente_id),
    producto_id INT REFERENCES productos(producto_id),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    anio INT,
    mes INT,
    nombre_mes VARCHAR(20),
    dia_semana VARCHAR(20)
);
"""

with engine.connect() as conn:
    for query in sql_crear_tablas.split(';'):
        query = query.strip()
        if query:
            conn.execute(text(query))
    conn.commit()

print("  ✅ Tablas creadas en PostgreSQL")

# ============================================
# 3. LEER CSVs LIMPIOS Y CARGAR A POSTGRES
# ============================================
print("\n[2] Leyendo archivos CSV limpios...")

productos_clean = pd.read_csv('data/productos_clean.csv')
clientes_clean = pd.read_csv('data/clientes_clean.csv')
ventas_clean = pd.read_csv('data/ventas_clean.csv')

print("\n[3] Insertando registros en PostgreSQL...")

productos_clean.to_sql('productos', con=engine, if_exists='append', index=False)
print(f"  ✅ Productos insertados: {len(productos_clean)} filas")

clientes_clean.to_sql('clientes', con=engine, if_exists='append', index=False)
print(f"  ✅ Clientes insertados:  {len(clientes_clean)} filas")

ventas_clean.to_sql('ventas', con=engine, if_exists='append', index=False)
print(f"  ✅ Ventas insertadas:    {len(ventas_clean)} filas")

# ============================================
# 4. VERIFICACIÓN FINAL EN LA BASE DE DATOS
# ============================================
print("\n[4] Verificando conteo de filas en PostgreSQL...")

with engine.connect() as conn:
    for tabla in ['productos', 'clientes', 'ventas']:
        res = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
        conteo = res.scalar()
        print(f"  📊 Tabla '{tabla}': {conteo} registros en DB")

print("\n" + "=" * 50)
print("¡CARGA COMPLETADA EXITOSAMENTE! 🎉")
print("=" * 50)