FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_HOME=/app
RUN echo $MY_UID
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . /app/
RUN poetry install --no-root

RUN ["chmod", "+x", "/app/scripts/fastapi_entrypoint.sh"]
ENTRYPOINT ["sh", "/app/scripts/fastapi_entrypoint.sh"]