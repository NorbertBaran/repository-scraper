import os
import subprocess

REPOSITORIES = os.environ.get('REPOSITORIES','repositories/example')

def clone_repository_mock(source):
    try:
        subprocess.run(['cp', source, f'{REPOSITORIES}/{id}'])
        return True
    except:
        return False