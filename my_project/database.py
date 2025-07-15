import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="telegram_db",
        user="postgres",
        password="postgres123"
    )

def fetch_all(query, params=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

