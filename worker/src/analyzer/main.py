import logging
import os
import subprocess
from celery import Celery
from src.database.models import AnalyzeModel
from src.updater.main import updating

WORKER_BROKER = os.environ.get("WORKER_BROKER")
app = Celery('analyzing-worker', broker=WORKER_BROKER)

@app.task(queue='analyzing-queue')
def analyzing(repository_id: int):
    logging.info(f"Analyzing repository with id {repository_id}")
    metric = AnalyzeModel(repository_id=repository_id, comment=f"Repository {repository_id} analyzed")
    logging.info(f"Analyzed repository with id: {repository_id}")
    updating.delay(metric.dict())
    logging.info(f"Deleting repository with id: {repository_id}")
    destination = f"/repositories/github/{repository_id}"
    subprocess.run(['rm', '-rf', destination])
    logging.info(f"Deleted repository with id: {repository_id}")
