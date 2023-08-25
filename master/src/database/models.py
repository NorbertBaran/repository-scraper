from pydantic import BaseModel

class MetadataModel(BaseModel):
    repository_id: int
    name: str
    url: str

class RawMetricsModel(BaseModel):
    loc: int
    lloc: int
    comments: int
    multi: int
    blank: int
    single_comments: int

class HaltestMetricsModel(BaseModel):
    h1: int
    h2: int
    n1: int
    n2: int
    vocabulary: int
    length: int
    calculated_length: int
    volume: int
    difficulty: int
    effort: int
    time: int
    bugs: int

class ComponentModel(BaseModel):
    type: str
    name: str
    begin: int
    end: int
    classname: str
    raw_metrics: RawMetricsModel

class FileModel(BaseModel):
    path: str
    score: float
    raw_metrics: RawMetricsModel
    haltest_metrics: HaltestMetricsModel
    components: list[ComponentModel]

class RepositoryModel(BaseModel):
    repository_id: int
    name: str
    clone_url: str
    files: list[FileModel]
