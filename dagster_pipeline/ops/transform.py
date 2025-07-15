from dagster import op

@op
def run_dbt_transformations():
    import subprocess
    subprocess.run(["dbt", "run", "--project-dir", "telegram_dbt_project"], check=True)
