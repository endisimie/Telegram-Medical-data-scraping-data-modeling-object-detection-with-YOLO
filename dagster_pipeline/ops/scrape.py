from dagster import op

@op
def scrape_telegram_data():
    import subprocess
    subprocess.run(["python", "src/scrape_telegram.py"], check=True)
