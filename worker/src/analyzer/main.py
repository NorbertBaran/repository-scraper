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

analyze_logger = logging.getLogger('analyzed-repositories')
analyze_handler = logging.FileHandler('/logs/analyzed-repositories.log')
analyze_logger.addHandler(analyze_handler)

processed_file_logger = logging.getLogger('processed-file-logger')
processable_file_handler = logging.FileHandler('/logs/processed-files.log')
processed_file_logger.addHandler(processable_file_handler)

timeout_logger = logging.getLogger('timeout-repositories')
timeout_handler = logging.FileHandler('/logs/tiemout-repositories.log')
timeout_logger.addHandler(timeout_handler)

def analyze_repository(id: int, name: str, clone_url: str):

    def create_structure(path: str, code:str):
        try:
            global_raw_metrics_module = analyze(code)
            global_raw_metrics = RawMetricsModel(
                loc=global_raw_metrics_module.loc,
                lloc=global_raw_metrics_module.lloc,
                comments=global_raw_metrics_module.comments,
                multi=global_raw_metrics_module.multi,
                blank=global_raw_metrics_module.blank,
                single_comments=global_raw_metrics_module.single_comments
            )
            global_haltest_metrics_module = h_visit(code)
            global_haltest_metrics = HaltestMetricsModel(
                h1=global_haltest_metrics_module.total.h1,
                h2=global_haltest_metrics_module.total.h2,
                n1=global_haltest_metrics_module.total.N1,
                n2=global_haltest_metrics_module.total.N2,
                vocabulary=global_haltest_metrics_module.total.vocabulary,
                length=global_haltest_metrics_module.total.length,
                calculated_length=global_haltest_metrics_module.total.calculated_length,
                volume=global_haltest_metrics_module.total.volume,
                difficulty=global_haltest_metrics_module.total.difficulty,
                effort=global_haltest_metrics_module.total.effort,
                time=global_haltest_metrics_module.total.time,
                bugs=global_haltest_metrics_module.total.bugs
            )

            file_structure = FileModel(
                path=path,
                score=mi_visit(code, True),
                raw_metrics=global_raw_metrics,
                haltest_metrics=global_haltest_metrics,
                components=[]
            )
            visit = cc_visit(code)
            lines = code.split('\n')
            for component in visit:
                component_type = None
                component_classname = 'undefined'
                if type(component) == Function:
                    component_type = 'function'
                    if component.classname:
                        component_classname = component.classname
                elif type(component) == Class:
                    component_type = 'class'
                    component_classname = 'undefined'

                component_name = component.name
                component_begin = component.lineno
                component_end = component.endline
                component_complexity = component.complexity

                component_code = '\n'.join(lines[component.lineno-1:component.endline])
                raw_metrics_module = analyze(component_code)
                raw_metrics = RawMetricsModel(
                    loc=raw_metrics_module.loc,
                    lloc=raw_metrics_module.lloc,
                    comments=raw_metrics_module.comments,
                    multi=raw_metrics_module.multi,
                    blank=raw_metrics_module.blank,
                    single_comments=raw_metrics_module.single_comments
                )
                component_raw_metrics = raw_metrics
                
                component_metrics = ComponentModel(
                    type=component_type,
                    name=component_name,
                    begin=component_begin,
                    end=component_end,
                    classname=component_classname,
                    complexity=component_complexity,
                    raw_metrics=component_raw_metrics
                )
                file_structure.components.append(component_metrics)
            
            processed_file_logger.info(f'repository_id: {id}, name {name}, clone_url {clone_url}, path: {path}')
            return file_structure
        except:
            # logging.error(f'Not processable file: {path} for repository {name} with id {id} and clone url {clone_url}')
            # not_processed_file_logger.info(f'repository_id: {id}, name {name}, clone_url {clone_url}, path: {path}')
            return False

    try:
        root = f'{REPOSITORIES}/{id}'
        files = glob.glob(os.path.join(root, "**/*.py"), recursive=True)

        repository_metrics = RepositoryModel(
            repository_id=id,
            name=name,
            clone_url=clone_url,
            files=[]
        )
        for filename in files:
            with open(filename, 'r') as f:
                try:
                    relative_path = filename[len(root)+1:]
                    code = f.read()
                    # logging.info(f'Processing file: {relative_path} for repository {name} with id {id} and clone url {clone_url}')
                    # file_metrics = run_with_timeout(create_structure, (relative_path, code))
                    file_metrics = create_structure(relative_path, code)
                    if file_metrics:
                        repository_metrics.files.append(file_metrics)
                    # logging.info(f'Processed file: {relative_path} for repository {name} with id {id} and clone url {clone_url}')
                except:
                    # logging.error(f'Not readable file: {relative_path} for repository {name} with id {id} and clone url {clone_url}')
                    pass

        return repository_metrics
    except Exception as e:
        logging.error(f'Error analyzing repository {name}: {e}')
        return None

def delete_git_history(id: int):
    try:
        subprocess.run(['rm', '-rf', f'{REPOSITORIES}/{id}/.git'])
        return True
    except:
        return False

def delete_repository(id: int):
    try:
        subprocess.run(['rm', '-rf', f'{REPOSITORIES}/{id}'])
        return True
    except:
        return False

@app.task(queue='analyzing-queue', soft_time_limit=30)
def analyzing(repository_id: int, name: str, clone_url: str):
    try:
        metrics = analyze_repository(repository_id, name, clone_url)
        if metrics:
            logging.info(f'Repository {repository_id} analyzed')
            analyze_logger.info(f'repository_id: {repository_id}, name: {name}, clone_url: {clone_url}')
            updating.delay(metrics.dict())
        else:
            logging.error(f'Failed to analyze repository {repository_id}')
    except:
        logging.error(f'Time limit exceeded while analyzing repository {repository_id}')
        timeout_logger.info(f'repository_id: {repository_id}, name: {name}, clone_url: {clone_url}')
    finally:
        deleted = delete_repository(repository_id)
        if deleted:
            logging.info(f'Repository {repository_id} deleted')
        else:
            logging.error(f'Failed to delete repository {repository_id}')
    
