import logging
import os
from celery import Celery
import requests

WORKER_BROKER = os.environ.get("WORKER_BROKER")
MASTER = os.environ.get("MASTER")

app = Celery('updating-worker', broker=WORKER_BROKER)

def save_repository_metrics(metrics):
    response = requests.post(f'{MASTER}/repository', json=metrics)
    if response.status_code == 201:
        return True
    return False

@app.task(queue='updating-queue')
def updating(metrics):
    response = requests.post(f'{MASTER}/metric', json=metrics)
    if response:
        logging.info(f'Metrics saved successfully for repository {metrics["repository_id"]}')
    else:
        logging.error(f'Failed to save metrics for repository {metrics["repository_id"]}')
