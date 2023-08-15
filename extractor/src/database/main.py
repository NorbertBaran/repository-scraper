import os
from pymongo import MongoClient
from parser.model import Repository

DATABASE_CONNECTION = os.environ.get("DATABASE_CONNECTION", "mongodb://admin:admin@localhost:27017/")
client = MongoClient(DATABASE_CONNECTION)

db = client['data']

def save_repository(repository: Repository):
    modules = db[f'modules-{repository.github_id}']
    ids = []
    for module in repository.modules:
        ids.append(modules.insert_one(module.__dict__()).inserted_id)
    repositories = db['repositories']
    repository_dict = repository.__dict__()
    repository_dict['modules'] = ids
    repositories.insert_one(repository_dict)