FROM python:3.10.12-alpine3.18
WORKDIR /app
RUN apk add --no-cache --update git
RUN apk add build-base
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir vendor
RUN git clone https://github.com/tree-sitter/tree-sitter-python vendor/tree-sitter-python/
CMD ["sh", "-c", "celery -A src.downloader.main worker -Q downloading-queue --loglevel=info & celery -A src.analyzer.main worker -Q analyzing-queue --loglevel=info & celery -A src.updater.main worker -Q updating-queue --loglevel=info"]