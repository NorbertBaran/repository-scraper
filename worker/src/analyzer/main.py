import logging
import os
import subprocess
from celery import Celery
from src.database.models import AnalyzeModel
from src.updater.main import updating
from src.extractor.parser.components import Repository
from src.extractor.main import extract, post_master

WORKER_BROKER = os.environ.get("WORKER_BROKER")
app = Celery('analyzing-worker', broker=WORKER_BROKER)

@app.task(queue='analyzing-queue')
def analyzing(repository_id: int, name: str, url: str, path: str):
    logging.info(f"Extracting repository with id {repository_id}")
    repository = extract(repository_id, name, url, path)
    logging.info(f"Extracted repository with id {repository_id}")
    logging.info(f"Posting to mongo repository with id {repository_id}")
    post_master(repository)
    logging.info(f"Posted to mongo repository with id {repository_id}")

    
    logging.info(f"Analyzing repository with id {repository_id}")
    metric = AnalyzeModel(repository_id=repository_id, comment=f"Repository {repository_id} analyzed")
    logging.info(f"Analyzed repository with id: {repository_id}")
    updating.delay(metric.dict())
    logging.info(f"Deleting repository with id: {repository_id}")
    destination = f"/repositories/github/{repository_id}"
    subprocess.run(['rm', '-rf', destination])
    logging.info(f"Deleted repository with id: {repository_id}")
