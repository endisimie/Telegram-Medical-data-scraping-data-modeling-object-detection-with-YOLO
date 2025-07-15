from dagster import op

@op
def load_raw_to_postgres():
    import subprocess
    subprocess.run(["python", "src/load_raw_to_postgres.py"], check=True)
