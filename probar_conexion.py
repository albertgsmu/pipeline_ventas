import sys
import psycopg2

# ⚠️ PON TU CONTRASEÑA AQUÍ
PASSWORD = 'Estrada9709.' 
USUARIO = 'postgres'
HOST = 'localhost'
PUERTO = '5432'
BASE_DATOS = 'pipeline_ventas'

print("🔍 Probando conexión a PostgreSQL (modo seguro)...")

try:
    conn = psycopg2.connect(
        dbname=BASE_DATOS,
        user=USUARIO,
        password=PASSWORD,
        host=HOST,
        port=PUERTO
    )
    print("\n🎉 ¡CONEXIÓN EXITOSA! Todo está perfecto.")
    conn.close()

except Exception as e:
    print("\n❌ ERROR DE CONEXIÓN CAPTURADO:")
    print("-" * 50)
    # Forzamos a imprimir sin que falle por tildes o caracteres especiales
    print(repr(e))
    print("-" * 50)
    
    print("\n💡 Diagnóstico:")
    print("   - Si tu contraseña tiene tildes (ej: 'contraseña'), ñ o símbolos especiales,")
    print("     prueba cambiando temporalmente la contraseña en pgAdmin por una sin tildes")
    print("     (ej: 'Password123') y actualízala en el script.")
    print("   - Asegúrate de que la base de datos 'pipeline_ventas' exista en pgAdmin.")