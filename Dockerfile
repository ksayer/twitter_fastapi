FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_HOME=/app

ARG INSTALL_DEV=${INSTALL_DEV}

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . /app/
RUN sh -c "if [ -n $INSTALL_DEV ] && [ $INSTALL_DEV == 'True' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

RUN ["chmod", "+x", "/app/scripts/fastapi_entrypoint.sh"]
ENTRYPOINT ["sh", "/app/scripts/fastapi_entrypoint.sh"]