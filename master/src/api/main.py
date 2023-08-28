from fastapi import FastAPI
from src.database.models import MetadataModel, RepositoryModel
from src.database.clients.api import ApiClient, PostgresApiClient
from fastapi.responses import JSONResponse
from fastapi import status
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
database: ApiClient = PostgresApiClient()

@app.get('/metadata', status_code=200, response_model=MetadataModel)
def get_metadata():
    metadata_model = database.get_metadata()
    try:
        if not metadata_model:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "No metadata available"})
        return metadata_model
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to fetch metadata"})

@app.post('/metric', status_code=201)
def post_metric(repository: RepositoryModel):
    try:
        database.post_metric(repository)
        return {"message": "Repository metrics saved successfully"}
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to save repository metrics"})
