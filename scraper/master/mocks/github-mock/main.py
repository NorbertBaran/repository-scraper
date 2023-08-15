from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse
from data import repositories

app = FastAPI()

@app.get('/search/repositories', status_code=200)
def search_repositories():
    try:
        search_repositories.count += 1
        if search_repositories.count > 1:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Requests limit exceeded"})
        return repositories
    except:
        search_repositories.count = 1
        return repositories

@app.put('/search/repositories', status_code=200)
def restart_requests():
    search_repositories.count = 0
    return {"message": "Requests limit restarted"}