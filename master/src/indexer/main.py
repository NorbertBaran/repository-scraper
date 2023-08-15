import logging
import os
from celery import Celery
import requests
import time
from src.database.clients.indexing import IndexingClient, PostgresIndexingClient
from src.database.models import MetadataModel

MASTER_BROKER = os.environ.get("MASTER_BROKER")
GITHUB_API = os.environ.get("GITHUB_API")

app = Celery('indexing-worker', broker=MASTER_BROKER)
# from main import app
database: IndexingClient = PostgresIndexingClient()

def get_next_github_metadata_batch(): 
    page = database.get_page()
    logging.info(f'Downloading github repositories matadata from page: {page}')
    params = {'q': 'stars:>0', 'sort': 'stars', 'order': 'desc', 'per_page': 3, 'page': page}
    metadata_batch_response = requests.get(f'{GITHUB_API}/search/repositories', params=params)
    logging.info(f'Downloading status code: {metadata_batch_response.status_code}')
    
    while metadata_batch_response.status_code == 403:
        time.sleep(60)
        metadata_batch_response = requests.get(f'{GITHUB_API}/search/repositories', params=params)
        
    metadata_batch = metadata_batch_response.json()

    selected_metadata_list = [MetadataModel(
        repository_id= metadata['id'],
        url=metadata['clone_url']
        ) for metadata in metadata_batch['items']]

    logging.info(f'Downloaded github repositories matadata from page: {page}')
    return selected_metadata_list

@app.task(queue='indexing-queue')
def github_indexing():
    page = database.get_page()
    logging.info(f"Indexing page: {page}")
    metadata_list = get_next_github_metadata_batch()
    database.save_metadata_batch(metadata_list)
    logging.info(f"Indexed page: {page}")
    database.increment_page()
    github_indexing.delay()

def indexing_init():
    connected = False
    while connected == False:
        try:
            database.get_page()
            connected = True
            logging.info("Database connection accepted")
        except Exception:
            logging.info("Database connection refused")
            time.sleep(1)

    logging.info(f"Indexing run")
    page = database.get_page()
    logging.info(f"Indexing initialized with page: {page}")
    github_indexing.delay()

indexing_init()