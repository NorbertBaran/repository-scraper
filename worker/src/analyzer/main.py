import logging
import os
import subprocess
from celery import Celery
from src.updater.main import updating

import glob
from radon.visitors import Function, Class
from radon.complexity import cc_visit
from radon.raw import analyze
from radon.metrics import h_visit, mi_visit

from src.models import *

REDIS = os.environ.get("REDIS_CONNECTION")
REPOSITORIES = os.environ.get('REPOSITORIES_PATH')
app = Celery('analyzing-worker', broker=REDIS)

def analyze_repository(id: int, name: str, clone_url: str):
    def create_structure(path: str, code:str):
        try:
            global_raw_metrics_module = analyze(code)
            global_raw_metrics = {
                'loc': global_raw_metrics_module.loc,
                'lloc': global_raw_metrics_module.lloc,
                'comments': global_raw_metrics_module.comments,
                'multi': global_raw_metrics_module.multi,
                'blank': global_raw_metrics_module.blank,
                'single_comments': global_raw_metrics_module.single_comments
            }

            global_haltest_metrics_module = h_visit(code)
            global_haltest_metrics = {
                'h1': global_haltest_metrics_module.total.h1,
                'h2': global_haltest_metrics_module.total.h2,
                'n1': global_haltest_metrics_module.total.N1,
                'n2': global_haltest_metrics_module.total.N2,
                'vocabulary': global_haltest_metrics_module.total.vocabulary,
                'length': global_haltest_metrics_module.total.length,
                'calculated_length': global_haltest_metrics_module.total.calculated_length,
                'volume': global_haltest_metrics_module.total.volume,
                'difficulty': global_haltest_metrics_module.total.difficulty,
                'effort': global_haltest_metrics_module.total.effort,
                'time': global_haltest_metrics_module.total.time,
                'bugs': global_haltest_metrics_module.total.bugs
            }

            structure = {
                'path': path,
                'raw_metrics': global_raw_metrics,
                'haltest_metrics': global_haltest_metrics,
                'components': [],
                'score': mi_visit(code, True)
            }

            visit = cc_visit(code)
            lines = code.split('\n')

            for component in visit:
                component_metrics = {}

                component_metrics['name'] = component.name
                component_metrics['begin'] = component.lineno
                component_metrics['end'] = component.endline
                if type(component) == Function:
                    component_metrics['type'] = 'function'
                    component_metrics['classname'] = component.classname
                elif type(component) == Class:
                    component_metrics['type'] = 'class'
                    component_metrics['classname'] = None
                component_metrics['complexity'] = component.complexity

                component_code = '\n'.join(lines[component.lineno-1:component.endline])
                
                raw_metrics_module = analyze(component_code)
                raw_metrics = {
                    'loc': raw_metrics_module.loc,
                    'lloc': raw_metrics_module.lloc,
                    'comments': raw_metrics_module.comments,
                    'multi': raw_metrics_module.multi,
                    'blank': raw_metrics_module.blank,
                    'single_comments': raw_metrics_module.single_comments
                }
                component_metrics['raw_metrics'] = raw_metrics

                structure['components'].append(component_metrics)

            return structure
        except:
            logging.error(f'Not processable file: {path} for repository {name} with id {id} and clone url {clone_url}')
            return False

    try:
        root = f'{REPOSITORIES}/{id}'
        files = glob.glob(os.path.join(root, "**/*.*"), recursive=True)
        repository_metrics = {
            'repository_id': id,
            'name': name,
            'clone_url': clone_url,
            'files': []
        }
        for filename in files:
            with open(filename, 'r') as f:
                try:
                    relative_path = filename[len(root)+1:]
                    code = f.read()
                    file_metrics = create_structure(relative_path, code)
                    if file_metrics:
                        repository_metrics['files'].append(file_metrics)
                except:
                    logging.error(f'Not readable file: {relative_path} for repository {name} with id {id} and clone url {clone_url}')
        
        logging.info(f'Metrics:\n {repository_metrics}')
        return repository_metrics
    except Exception as e:
        logging.error(f'Error analyzing repository {name}: {e}')
        return None

def delete_repository(id: int):
    try:
        subprocess.run(['rm', '-rf', f'{REPOSITORIES}/{id}'])
        return True
    except:
        return False

@app.task(queue='analyzing-queue')
def analyzing(repository_id: int, name: str, clone_url: str):
    metrics = analyze_repository(repository_id, name, clone_url)
    if metrics:
        logging.info(f'Repository {repository_id} analyzed')
        updating.delay(metrics)
    else:
        logging.error(f'Failed to analyze repository {repository_id}')
    deleted = delete_repository(repository_id)
    if deleted:
        logging.info(f'Repository {repository_id} deleted after analysis')
    else:
        logging.error(f'Failed to delete repository {repository_id}')
    
