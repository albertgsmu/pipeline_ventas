"""
🚀 PIPELINE COMPLETO DE VENTAS (ETL + SQL)
===========================================
Ejecuta las 4 fases de forma secuencial:
  1. Generar / Extraer datos
  2. Limpiar y transformar
  3. Cargar a PostgreSQL
  4. Ejecutar reporte SQL

Para ejecutarlo solo usas: python pipeline.py
"""

import os
os.environ['PGCLIENTENCODING'] = 'UTF8'

import time
from datetime import datetime

def banner(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)

def ejecutar_pipeline():
    tiempo_inicio = time.time()
    
    print("🚀" * 30)
    print("      INICIANDO PIPELINE DE VENTAS")
    print(f"      Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀" * 30)
    
    try:
        # --------------------------------------------------
        # FASE 1: GENERAR / EXTRAER DATOS
        # --------------------------------------------------
        banner("FASE 1: GENERANDO DATOS (Extract)")
        import generar_datos
        print("✅ Fase 1 completada exitosamente.")

        # --------------------------------------------------
        # FASE 2: LIMPIAR DATOS
        # --------------------------------------------------
        banner("FASE 2: LIMPIANDO DATOS (Transform)")
        import limpiar_datos
        print("✅ Fase 2 completada exitosamente.")

        # --------------------------------------------------
        # FASE 3: CARGAR A POSTGRESQL
        # --------------------------------------------------
        banner("FASE 3: CARGANDO A POSTGRESQL (Load)")
        import cargar_datos
        print("✅ Fase 3 completada exitosamente.")

        # --------------------------------------------------
        # FASE 4: CONSULTAS ANALÍTICAS
        # --------------------------------------------------
        banner("FASE 4: EJECUTANDO CONSULTAS SQL (Analyze)")
        import consultas_sql
        print("✅ Fase 4 completada exitosamente.")

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EN EL PIPELINE: {e}")
        import traceback
        traceback.print_exc()
        return

    duracion = round(time.time() - tiempo_inicio, 2)
    print("\n" + "🎉" * 30)
    print(f"  ¡PIPELINE EJECUTADO CON ÉXITO EN {duracion} SEGUNDOS!")
    print("🎉" * 30)

if __name__ == "__main__":
    ejecutar_pipeline()