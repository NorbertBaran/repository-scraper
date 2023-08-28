FROM python:3.10.12-alpine3.18
WORKDIR /app
RUN apk add --no-cache --update git
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "celery -A src.downloader.main worker -Q downloading-queue --loglevel=warning & celery -A src.analyzer.main worker -Q analyzing-queue --loglevel=warning & celery -A src.updater.main worker -Q updating-queue --loglevel=warning"]