FROM python:3.11-alpine
RUN mkdir /app
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . /app/
RUN poetry install --no-root

RUN ["chmod", "+x", "/app/scripts/fastapi_entrypoint.sh"]
ENTRYPOINT ["sh", "/app/scripts/fastapi_entrypoint.sh"]