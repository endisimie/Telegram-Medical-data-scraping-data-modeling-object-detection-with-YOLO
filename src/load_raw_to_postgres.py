import os
import json
import psycopg2
from glob import glob

# --------------------
# Database Config
# --------------------
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "telegram_db"
DB_USER = "postgres"
DB_PASS = "postgres123"  # 🔁 Change this to your actual password

# --------------------
# Paths
# --------------------
DATA_DIR = "data/raw"  # Folder containing JSON files

# --------------------
# Connect to PostgreSQL
# --------------------
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# --------------------
# Create Schema and Table
# --------------------
def create_schema_and_table():
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw_data;

        CREATE TABLE IF NOT EXISTS raw_data.telegram_messages (
            id BIGINT PRIMARY KEY,
            text TEXT,
            date TIMESTAMP,
            media TEXT
        );
    """)
    conn.commit()
    print("✅ Schema and table created (if not exists).")

# --------------------
# Load JSON Files and Insert
# --------------------
def load_json_files():
    json_files = glob(os.path.join(DATA_DIR, "**", "*.json"), recursive=True)
    inserted = 0

    for file_path in json_files:
        try:
            with open(file_path, encoding="utf-8") as f:
                messages = json.load(f)

            for msg in messages:
                msg_id = msg.get("id")
                msg_text = (msg.get("text") or "").strip()
                msg_date = msg.get("date")
                msg_media = msg.get("media")

                if not msg_id or not msg_text:
                    continue  # Skip empty records

                cur.execute("""
                    INSERT INTO raw_data.telegram_messages (id, text, date, media)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (msg_id, msg_text, msg_date, msg_media))

                inserted += 1

            conn.commit()
            print(f"✅ Inserted data from {file_path}")

        except Exception as e:
            print(f"❌ Failed to load {file_path}: {e}")

    print(f"\n🎉 Total records inserted: {inserted}")

# --------------------
# Main
# --------------------
if __name__ == "__main__":
    try:
        create_schema_and_table()
        load_json_files()
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        cur.close()
        conn.close()
        print("🔌 Connection closed.")
