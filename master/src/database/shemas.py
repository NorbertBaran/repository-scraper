from src.database.engine import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Variable(Base):
    __tablename__ = 'variables'
    name = Column(String, primary_key=True)
    value = Column(String)

class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)  
    repository_id = Column(Integer) 
    url = Column(String)

    metrics = relationship("Metric", back_populates="repository_metadata")

class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    metadata_id = Column(Integer, ForeignKey('metadata.id'))
    comment = Column(String)

    repository_metadata = relationship("Metadata", back_populates="metrics")