import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from connect_db import get_db_connection, execute_sql_file
from generate_reports import generate_all_reports_and_charts

def run_sql_pipeline():
    conn = get_db_connection()
    try:
        # Rutas relativas desde la raíz del proyecto (porque ejecutamos desde ahí)
        execute_sql_file(conn, 'sql/01_create_tables.sql')
        execute_sql_file(conn, 'sql/02_etl_views.sql')
        print("+ Pipeline SQL completado.")
    except Exception as e:
        print(f"X Error at pipeline SQL: {e}")
    finally:
        conn.close()

def main():
    print("=== Iniciando pipeline Revolut ===\n")
    run_sql_pipeline()
    print("\n=== Generando reportes y dashboards ===\n")
    generate_all_reports_and_charts()
    print("\n Process completed. Check the outputs folder./")

if __name__ == "__main__":
    main()