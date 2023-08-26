from abc import ABC, abstractmethod
from src.database.engine import Session
from src.database.models import ComponentModel, FileModel, MetadataModel, RepositoryModel
from src.database.shemas import Metadata, Repository, File, Component, RawMetrics, HaltestMetrics

class ApiClient(ABC):
    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def post_metric(self, repository: RepositoryModel):
        pass

class PostgresApiClient(ApiClient):
    def get_metadata(self):
        session = Session()
        metadata = session.query(Metadata).first()
        if not metadata:
            session.close()
            return None
        metadata_model = MetadataModel(repository_id=metadata.repository_id, name=metadata.name, clone_url=metadata.clone_url)
        session.close()
        return metadata_model

    def post_metric(self, repository_model: RepositoryModel):
        session = Session()
        repository = Repository(repository_id = repository_model.repository_id, name = repository_model.name, clone_url = repository_model.clone_url)
        
        file_models: list[FileModel] = repository_model.files
        for file_model in file_models:
            global_raw_metrics = RawMetrics(loc = file_model.raw_metrics.loc, lloc = file_model.raw_metrics.lloc, comments = file_model.raw_metrics.comments, multi = file_model.raw_metrics.multi, blank = file_model.raw_metrics.blank, single_comments = file_model.raw_metrics.single_comments)
            session.add(global_raw_metrics)

            global_haltest_metrics = HaltestMetrics(h1 = file_model.haltest_metrics.h1, n1 = file_model.haltest_metrics.n1, n2 = file_model.haltest_metrics.n2, vocabulary = file_model.haltest_metrics.vocabulary, calculated_length = file_model.haltest_metrics.calculated_length, volume = file_model.haltest_metrics.validate, difficulty = file_model.haltest_metrics.difficulty, effort = file_model.haltest_metrics.effort, time = file_model.haltest_metrics.time, bugs = file_model.haltest_metrics.bugs)
            session.add(global_haltest_metrics)

            file = File(path = file_model.path, score = file_model.score)
            file.raw_metrics = global_raw_metrics
            file.haltest_metrics = global_haltest_metrics
            
            component_models: list[ComponentModel] = file_model.components
            for component_model in component_models:
                component_raw_metrics = RawMetrics(loc = file_model.raw_metrics.loc, lloc = file_model.raw_metrics.lloc, comments = file_model.raw_metrics.comments, multi = file_model.raw_metrics.multi, blank = file_model.raw_metrics.blank, single_comments = file_model.raw_metrics.single_comments)
                session.add(component_raw_metrics)
                
                component = Component(type = component_model.type , name = component_model.name, begin = component_model.begin, end = component_model.end, classname = component_model.classname)
                component.raw_metrics = component_raw_metrics
                session.add(component)
                
                file.components.append(component)
            session.add(file)

            repository.files.append(file)
        session.add(repository)

        metadata = session.query(Metadata).filter_by(repository_id=repository_model.repository_id).first()
        session.delete(metadata)

        session.commit()


            