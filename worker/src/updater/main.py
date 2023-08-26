import logging
import os
from celery import Celery
import requests

REDIS = os.environ.get("REDIS_CONNECTION")
MASTER = os.environ.get("MASTER_URL")

app = Celery('updating-worker', broker=REDIS)

def save_repository_metrics(metrics):
    response = requests.post(f'{MASTER}/metric', json=metrics)
    if response.status_code == 201:
        return True
    return False

@app.task(queue='updating-queue')
def updating(metrics):
    response = save_repository_metrics(metrics)
    if response:
        logging.info(f'Metrics saved successfully for repository {metrics["repository_id"]}')
    else:
        logging.error(f'Failed to save metrics for repository {metrics["repository_id"]}')
