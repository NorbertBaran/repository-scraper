from pydantic import BaseModel

class MetadataModel(BaseModel):
    repository_id: int
    url: str

class MetricModel(BaseModel):
    metadata_id: int
    comment: str

class AnalyzeModel(BaseModel):
    repository_id: int
    comment: str

class RepositoryModel(BaseModel):
    metadata: dict
    modules: list[dict]