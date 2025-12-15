import psycopg2
from app.config import DB_CONFIG

# app/db.py
DB_CONFIG = {
    "dbname": "videos_db",
    "user": "postgres",
    "password": "050666",
    "host": "localhost",
    "port": 5432,
}

def get_connection():
    import psycopg2
    return psycopg2.connect(**DB_CONFIG)
