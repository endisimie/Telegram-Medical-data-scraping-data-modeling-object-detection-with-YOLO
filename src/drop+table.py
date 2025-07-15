import psycopg2

conn = psycopg2.connect(
    dbname="telegram_db",
    user="postgres",
    password="postgres123",
    host="localhost"
)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS raw_data.telegram_messages CASCADE;")

conn.commit()

cur.close()
conn.close()
print("✅ Table dropped successfully.")
