import logging
import os
from celery import Celery
import requests
import subprocess
import time
from src.analyzer.main import analyzing

WORKER_BROKER = os.environ.get("WORKER_BROKER")
API = os.environ.get("API")

app = Celery('downloading-worker', broker=WORKER_BROKER)

@app.task(queue='downloading-queue')
def downloading():
    logging.info(f"Metadata requesting")
    response = requests.get(f'{API}/metadata')
    logging.info(f"Metadata response status code: {response.status_code}")
    if response.status_code == 200:
        metadata = response.json()
        logging.info(f"Downloading repository (id: {metadata['repository_id']}, url: {metadata['url']})")
        destination = f"/repositories/github/{metadata['repository_id']}"
        subprocess.run(['git', 'clone', metadata['url'], destination])
        logging.info(f"Repository downloaded to {destination}")
        analyzing.delay(metadata['repository_id'], 'undefined', metadata['url'], destination)
    else:
        logging.error(f"No metadata available")
        time.sleep(60)
    downloading.delay()

def downloading_init():
    logging.info(f"Downloading init")
    downloading.delay()

downloading_init()