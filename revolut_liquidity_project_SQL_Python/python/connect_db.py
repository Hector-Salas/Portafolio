# python/connect_db.py
import os
from dotenv import load_dotenv
import psycopg2
from pathlib import Path

# Buscar el archivo .env en la carpeta raíz del proyecto (un nivel arriba de 'python')
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "revolut_db"),
        user=os.getenv("DB_USER", "revolut_user"),
        password=os.getenv("DB_PASSWORD"),  # Debe existir
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

def execute_sql_file(conn, filepath):
    """Execute a complete SQL file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    with conn.cursor() as cur:
        cur.execute(sql_script)
    conn.commit()
    print(f"Ejecutado: {filepath}")