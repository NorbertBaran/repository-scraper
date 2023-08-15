from pydantic import BaseModel

class AnalyzeModel(BaseModel):
    repository_id: int
    comment: str