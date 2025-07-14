import os
import json
import psycopg2
from glob import glob

# 🧪 Database credentials – customize or use .env for safety
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "telegram_db"
DB_USER = "postgres"
DB_PASS = "postgres123"  # <-- CHANGE THIS!

# 📂 Directory containing raw JSON files
DATA_DIR = "data/raw"

# 🛠 Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# ✅ Create schema and table if they don’t exist
def setup_schema_and_table():
    cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw_data;

    CREATE TABLE IF NOT EXISTS raw_data.telegram_messages (
        id BIGINT PRIMARY KEY,
        channel_id BIGINT,
        date TIMESTAMP,
        message TEXT,
        media TEXT
    );
    """)
    conn.commit()
    print("✅ Schema and table ready")

# 📥 Load and insert JSON files recursively
def load_json_files():
    json_files = glob(f"{DATA_DIR}/**/*.json", recursive=True)
    total_inserted = 0

    for file in json_files:
        try:
            with open(file, encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    msg_id = msg.get("id")
                    channel_id = msg.get("peer_id", {}).get("channel_id")
                    date = msg.get("date")
                    message = msg.get("message")
                    media = str(msg.get("media"))  # convert media to text

                    cur.execute("""
                        INSERT INTO raw_data.telegram_messages (id, channel_id, date, message, media)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """, (msg_id, channel_id, date, message, media))
                    total_inserted += 1

            conn.commit()
            print(f"✅ Inserted from: {file}")
        except Exception as e:
            print(f"❌ Failed to load {file}: {e}")

    print(f"\n🎉 Total records attempted: {total_inserted}")

# 🚀 Main workflow
if __name__ == "__main__":
    try:
        setup_schema_and_table()
        load_json_files()
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        cur.close()
        conn.close()
