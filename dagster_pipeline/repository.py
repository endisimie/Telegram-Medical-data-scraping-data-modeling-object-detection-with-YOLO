from dagster import repository, schedule, define_asset_job
from telegram_dagster_pipeline.jobs import pipeline_job  # your defined job

# Schedule: Run every day at 2:00 AM
@schedule(job=pipeline_job, cron_schedule="0 2 * * *")
def daily_pipeline_schedule(context):
    return {}

@repository
def telegram_repo():
    return [pipeline_job, daily_pipeline_schedule]
