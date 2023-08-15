from abc import ABC, abstractmethod
from src.database.engine import Session
from src.database.shemas import Metadata, Metric
from src.database.models import MetadataModel, MetricModel, AnalyzeModel

class ApiClient(ABC):
    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def post_metric(self, metrics: MetricModel):
        pass

class PostgresApiClient(ApiClient):  
    def get_metadata(self):
        session = Session()
        metadata = session.query(Metadata).filter(~Metadata.metrics.any()).first()
        if not metadata:
            session.close()
            return None
        metadata_model = MetadataModel(repository_id=metadata.repository_id, url=metadata.url)
        metric = Metric(metadata_id=metadata.id, comment=None)
        session.add(metric)
        session.commit()
        session.close()
        return metadata_model
    
    def post_metric(self, analyze: AnalyzeModel):
        session = Session()
        metadata = session.query(Metadata).filter_by(repository_id=analyze.repository_id).first()
        metric = session.query(Metric).filter_by(metadata_id=metadata.id).first()
        metric.comment = analyze.comment
        session.commit()
        session.close()