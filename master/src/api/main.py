from fastapi import FastAPI
from src.database.models import MetadataModel, MetricModel, AnalyzeModel, RepositoryModel
from src.database.clients.api import ApiClient, PostgresApiClient
from fastapi.responses import JSONResponse
from fastapi import status

app = FastAPI()
database: ApiClient = PostgresApiClient()

@app.get('/metadata', status_code=200, response_model=MetadataModel)
def get_metadata():
    metadata_model = database.get_metadata()
    if not metadata_model:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "No metadata available"})
    return metadata_model

@app.post('/repository', status_code=200)
def post_repository(repository: RepositoryModel):
    database.post_repository(repository.metadata, repository.modules)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Repository saved successfully"})

@app.post('/metric', status_code=200)
def post_metrics(request: AnalyzeModel):
    database.post_metric(request)
