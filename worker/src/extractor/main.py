from parser.languages.python import process_repository
from database.main import save_repository
from worker.src.database.models import RepositoryModel
from worker.src.extractor.src.parser.components import Repository

def extract():
    pass

def post_master(repository: Repository):
    metadata = repository.__dict__()
    modules = [module.__dict__() for module in repository.modules]
    repository_model = RepositoryModel(metadata, modules)
    # TODO: Post request to master

# repository = process_repository(0, 'example', 'example.github.com', 'repositories/example/python')
# post_master(repository)
# repository = process_repository(1, 'example', 'example.github.com', 'repositories/example/python_structure')
# post_master(repository)
# repository = process_repository(2, 'wagtail', 'wagtail.github.com', 'repositories/github/wagtail')
# post_master(repository)
repository = process_repository(3, 'auto-gpt', 'auto-gpt.github.com', 'repositories/github/Auto-GPT')
post_master(repository)
