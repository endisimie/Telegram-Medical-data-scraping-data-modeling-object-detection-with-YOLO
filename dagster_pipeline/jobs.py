from dagster import job
from ops.scrape import scrape_telegram_data
from ops.load import load_raw_to_postgres
from ops.transform import run_dbt_transformations
from ops.enrich import run_yolo_enrichment

@job
def telegram_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
