from abc import ABC, abstractmethod
from src.database.engine import Session
from src.database.shemas import Variable, Metadata
from src.database.models import MetadataModel

class IndexingClient(ABC):
    @abstractmethod
    def get_page(self):
        pass

    @abstractmethod
    def increment_page(self):
        pass

    @abstractmethod
    def save_metadata_batch(self, request: list[MetadataModel]):
        pass

class PostgresIndexingClient(IndexingClient):

    def get_page(self):
        session = Session()
        variable = session.query(Variable).filter_by(name='page').first()

        if not variable:
            print('Not variable')
            variable = Variable(name='page', value='1')
            session.add(variable)
            session.commit()
        
        page = int(variable.value)
        session.close()

        return page
    
    def increment_page(self):
        session = Session()
        page = self.get_page() + 1
        variable = session.query(Variable).filter_by(name='page').first()
        variable.value = str(page)
        session.commit()
        session.close()
    
    def save_metadata_batch(self, request: list[MetadataModel]):
        session = Session()
        metadata_batch = [Metadata(**repository.dict()) for repository in request]
        session.bulk_save_objects(metadata_batch)
        session.commit()
        session.close()