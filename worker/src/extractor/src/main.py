from parser.languages.python import process_repository
from database.main import save_repository

# repository = process_repository(0, 'example', 'example.github.com', 'repositories/example/python')
# save_repository(repository)
# repository = process_repository(1, 'example', 'example.github.com', 'repositories/example/python_structure')
# save_repository(repository)
# repository = process_repository(2, 'wagtail', 'wagtail.github.com', 'repositories/github/wagtail')
# save_repository(repository)
repository = process_repository(3, 'auto-gpt', 'auto-gpt.github.com', 'repositories/github/Auto-GPT')
save_repository(repository)
