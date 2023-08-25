FROM python:3.10.12-alpine3.18
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "python database-init.py & celery -A src.indexer.main worker -Q indexing-queue --loglevel=info & uvicorn src.api.main:app --host 0.0.0.0 --port 80"]