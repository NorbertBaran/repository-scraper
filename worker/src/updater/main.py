import logging
import os
from celery import Celery
import requests
from src.database.models import AnalyzeModel

WORKER_BROKER = os.environ.get("WORKER_BROKER")
API = os.environ.get("API")

app = Celery('updating-worker', broker=WORKER_BROKER)

@app.task(queue='updating-queue')
def updating(metric):
    logging.info(f"Updating repository with id {metric['repository_id']}")
    response = requests.post(f'{API}/metric', json=metric)
    logging.info(f"Updated repository with id: {metric['repository_id']} and status code: {response.status_code}")
