import os
import psycopg2
from glob import glob
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Constants
IMAGE_DIR = "data/raw/telegram_messages/images"  # contains folders like /channel_name/*.jpg
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "telegram_db",
    "user": "postgres",
    "password": "postgres123"  # change this
}

def extract_message_id(filepath):
    """Extract message_id from the filename (e.g., 50001.jpg)"""
    try:
        filename = os.path.basename(filepath)
        return int(os.path.splitext(filename)[0])
    except ValueError:
        return None

def scan_and_detect():
    image_paths = glob(os.path.join(IMAGE_DIR, "*", "*.jpg"))
    print(f"🔍 Found {len(image_paths)} image(s)")

    detections = []

    for path in image_paths:
        message_id = extract_message_id(path)
        if not message_id:
            continue

        results = model(path)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = r.names[cls]
                detections.append((message_id, class_name, conf))

    return detections

def insert_to_postgres(detections):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Ensure the table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_data.image_detections (
            message_id BIGINT,
            object_class TEXT,
            confidence_score FLOAT,
            FOREIGN KEY (message_id) REFERENCES raw_data.telegram_messages(id)
        );
    """)
    conn.commit()

    valid_detections = []
    for row in detections:
        message_id, obj_class, conf = row
        cur.execute("SELECT 1 FROM raw_data.telegram_messages WHERE id = %s", (message_id,))
        if cur.fetchone():
            valid_detections.append(row)
        else:
            print(f"⚠️ Skipping detection for unknown message_id: {message_id}")

    for row in valid_detections:
        cur.execute("""
            INSERT INTO raw_data.image_detections (message_id, object_class, confidence_score)
            VALUES (%s, %s, %s)
        """, row)

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted {len(valid_detections)} valid detections.")


if __name__ == "__main__":
    detections = scan_and_detect()
    insert_to_postgres(detections)
