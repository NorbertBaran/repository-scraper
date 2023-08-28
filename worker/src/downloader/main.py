import logging
import os
from celery import Celery
import requests
import subprocess
import time
from src.analyzer.main import analyzing

REDIS = os.environ.get("REDIS_CONNECTION")
MASTER = os.environ.get("MASTER_URL")
REPOSITORIES = os.environ.get('REPOSITORIES_PATH')
MAX_DOWNLOADED_REPOSITORIES = os.environ.get('MAX_DOWNLOADED_REPOSITORIES')
app = Celery('downloading-worker', broker=REDIS)

def get_repository_metadata():
    response = requests.get(f'{MASTER}/metadata')
    if response.status_code == 200:
        metadata = response.json()
        return metadata
    return None

def clone_repository(id: int, url: str):
    try:
        subprocess.run(['git', 'clone', url, f'{REPOSITORIES}/{id}'])
        while len(os.listdir(REPOSITORIES)) >= int(MAX_DOWNLOADED_REPOSITORIES):
            logging.info(f'Waiting for process downloaded repositories before dowlnoading more...')
            time.sleep(10)
        return True
    except:
        return False

@app.task(queue='downloading-queue')
def downloading():
    metadata = get_repository_metadata()
    if metadata:
        logging.info(f'Got metadata from master successfully')
        repository_id, name, clone_url = metadata['repository_id'], metadata['name'], metadata['clone_url']
        cloned = clone_repository(repository_id, clone_url)
        if cloned:
            logging.info(f'Repository {repository_id} cloned successfully')
            analyzing.delay(repository_id, name, clone_url)
        else:
            logging.error(f'Failed to clone repository {repository_id}')
    else:
        logging.error(f'Failed to get metadata from master')
        time.sleep(60)
    downloading.delay()

downloading.delay()