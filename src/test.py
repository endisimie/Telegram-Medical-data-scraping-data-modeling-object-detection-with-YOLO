import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="telegram_db",
    user="postgres",
    password="postgres123"
)
cur = conn.cursor()
cur.execute("SELECT * FROM raw_data.image_detections LIMIT 10;")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()
