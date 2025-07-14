
# 📦 Telegram Data Pipeline: Scraping, Modeling, and Transformation

This project is part of **10 Academy Week 7 Challenge**. It demonstrates an end-to-end data engineering workflow to collect, clean, structure, and analyze data from Telegram channels. The pipeline leverages Telegram scraping, PostgreSQL ingestion, and dbt modeling.

---


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




