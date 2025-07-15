from dagster import op

@op
def run_yolo_enrichment():
    import subprocess
    subprocess.run(["python", "src/enrich_with_yolo.py"], check=True)
