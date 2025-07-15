
# 📦 Telegram Data Pipeline: Scraping, Modeling, and Transformation

This project is part of **10 Academy Week 7 Challenge**. It demonstrates an end-to-end data engineering workflow to collect, clean, structure, and analyze data from Telegram channels. The pipeline leverages Telegram scraping, PostgreSQL ingestion, and dbt modeling.

---


## 🎯 Tasks Overview

### ✅ Task 0: Environment Setup

- Created virtual environment with dependencies (`.venv`)
- Installed PostgreSQL and pgAdmin via Docker
- Verified container startup and access to DB at `localhost:5432`
- Set up `.env` for secure DB credentials (not committed)

### ✅ Task 1: Data Loading Script

- Parsed raw Telegram JSON files
- Extracted `id`, `text`, `date`, and `media`
- Created `raw_data.telegram_messages` table
- Inserted 4000+ messages into PostgreSQL
- Skipped duplicates and null records using `ON CONFLICT DO NOTHING`

### ✅ Task 2: DBT Transformation

- Initialized dbt project: `telegram_dbt_project`
- Created **staging model**: `stg_telegram_messages.sql`
- Built final **data mart models**: `dim_dates`, `dim_channels`, `fct_messages`
- Applied dbt tests:
  - `not_null` on important fields (e.g., `message_text`)
  - Custom test for non-empty messages
- Used `dbt docs generate` to document data models

---

## 🧪 Tests and Data Quality

| Test | Description | Result |
|------|-------------|--------|
| `not_null` on `text` | Ensures messages are not null | ✅ |
| `unique` on `id`     | Avoids duplication of messages | ✅ |
| `test_no_empty_messages` | Ensures `text` is not empty | ✅ |

---

## 🐘 Database Schema

| Table | Description |
|-------|-------------|
| `raw_data.telegram_messages` | Raw Telegram messages loaded from JSON |
| `stg_telegram_messages` | Cleaned view with typecasting and filtering |
| `dim_dates` | Date dimension (auto-generated) |
| `fct_messages` | Fact table with metrics per message |

---

🧠 Data Enrichment with YOLOv8
Installed ultralytics and used YOLOv8n to detect objects in scraped images.
Mapped predictions to their corresponding message_ids.
Created fct_image_detections fact table:

message_id, object_class, confidence_score

## 🌐 Analytical API with FastAPI
Developed REST endpoints to access insights from the modeled warehouse.
| Method | Route                                    | Description                |
| ------ | ---------------------------------------- | -------------------------- |
| GET    | `/api/reports/top-products?limit=10`     | Most mentioned terms       |
| GET    | `/api/channels/{channel_name}/activity`  | Message count by date      |
| GET    | `/api/search/messages?query=paracetamol` | Search messages by keyword |



## Pipeline Orchestration with Dagster
Installed and configured Dagster for orchestration.

Defined Ops for:
- Scraping Telegram data
- Loading raw data into PostgreSQL
- Running dbt transformations
- Enriching with YOLO


## ⚙️ Setup Instructions

### 🐳 Docker
```bash
docker-compose up -d  # Starts PostgreSQL and pgAdmin


### Python
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
pip install -r requirements.txt
python src/load_raw_to_postgres.py

dbt run       # Runs all models
dbt test      # Runs data tests
dbt docs serve  # Opens model documentation

```
## Run the Dagster UI:

```bash

dagster dev
Run each step from the Dagster UI or command line.

Serve API:

uvicorn main:app --reload
Visit:
http://localhost:8000/docs
