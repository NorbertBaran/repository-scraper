from src.extractor.parser.languages.python import process_repository
from src.extractor.parser.components import Repository
from src.database.models import RepositoryModel
import os
import requests

API = os.environ.get("API")

def extract(github_id: int, name: str, url: str, path: str):
    return process_repository(github_id, name, url, path)

def post_master(repository: Repository):
    metadata = repository.__dict__()
    modules = [module.__dict__() for module in repository.modules]
    repository_model = RepositoryModel(metadata=metadata, modules=modules)
    response = requests.post(f'{API}/repository', json=repository_model.dict())
    print(response)

# repository = process_repository(0, 'example', 'example.github.com', 'repositories/example/python')
# post_master(repository)
# repository = process_repository(1, 'example', 'example.github.com', 'repositories/example/python_structure')
# post_master(repository)
# repository = process_repository(2, 'wagtail', 'wagtail.github.com', 'repositories/github/wagtail')
# post_master(repository)
# repository = process_repository(3, 'auto-gpt', 'auto-gpt.github.com', 'repositories/github/Auto-GPT')
# post_master(repository)
