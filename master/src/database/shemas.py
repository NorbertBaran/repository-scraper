from src.database.engine import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

class Variable(Base):
    __tablename__ = 'variables'
    name = Column(String, primary_key=True)
    value = Column(String)

class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer)
    name = Column(String)
    clone_url = Column(String)

class RawMetrics(Base):
    __tablename__ = 'raw_metrics'
    id = Column(Integer, primary_key=True)
    loc = Column(Integer)
    lloc = Column(Integer)
    comments = Column(Integer)
    multi = Column(Integer)
    blank = Column(Integer)
    single_comments = Column(Integer)

class HaltestMetrics(Base):
    __tablename__ = 'haltest_metrics'
    id = Column(Integer, primary_key=True)
    h1 = Column(Integer)
    h2 = Column(Integer)
    n1 = Column(Integer)
    n2 = Column(Integer)
    vocabulary = Column(Integer)
    length = Column(Integer)
    calculated_length = Column(Integer)
    volume = Column(Integer)
    difficulty = Column(Integer)
    effort = Column(Integer)
    time = Column(Integer)
    bugs = Column(Integer)

class Component(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    begin = Column(Integer)
    end = Column(Integer)
    classname = Column(String)
    complexity = Column(Integer)
    file_id = Column(Integer, ForeignKey('files.id'))
    raw_metrics_id = Column(Integer, ForeignKey('raw_metrics.id'))
    
    file = relationship("File", back_populates="components")
    raw_metrics = relationship("RawMetrics")

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    score = Column(Float)
    repository_id = Column(Integer, ForeignKey('repositories.id'))
    raw_metrics_id = Column(Integer, ForeignKey('raw_metrics.id'))
    haltest_metrics_id = Column(Integer, ForeignKey('haltest_metrics.id'))
    
    repository = relationship("Repository", back_populates="files")
    raw_metrics = relationship("RawMetrics")
    haltest_metrics = relationship("HaltestMetrics")
    components = relationship("Component", back_populates="file")

class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer)
    name = Column(String)
    clone_url = Column(String)
    
    files = relationship("File", back_populates="repository")
