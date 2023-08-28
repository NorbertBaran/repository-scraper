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
        session.delete(metadata)
        session.commit()
        session.close()
        return metadata_model

    def post_metric(self, repository_model: RepositoryModel):
        # Create a new session
        session = Session()

        try:
            # Create Metadata instance
            repository = Repository(
                repository_id=repository_model.repository_id,
                name=repository_model.name,
                clone_url=repository_model.clone_url,
            )
            session.add(repository)
            session.commit()

            for file_model in repository_model.files:
                # Create RawMetrics instance
                raw_metrics = RawMetrics(**file_model.raw_metrics.dict())
                session.add(raw_metrics)
                session.commit()

                # Create HaltestMetrics instance
                haltest_metrics = HaltestMetrics(**file_model.haltest_metrics.dict())
                session.add(haltest_metrics)
                session.commit()

                # Create File instance
                file = File(
                    path=file_model.path,
                    score=file_model.score,
                    repository_id=repository.id,
                    raw_metrics_id=raw_metrics.id,
                    haltest_metrics_id=haltest_metrics.id,
                )
                session.add(file)
                session.commit()

                for component_model in file_model.components:
                    # Create Component instance
                    component = Component(
                        type=component_model.type,
                        name=component_model.name,
                        begin=component_model.begin,
                        end=component_model.end,
                        classname=component_model.classname,
                        complexity=component_model.complexity,
                        file_id=file.id,
                        raw_metrics_id=raw_metrics.id,
                    )
                    session.add(component)

            session.commit()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()


            