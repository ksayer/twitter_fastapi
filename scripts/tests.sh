#! /usr/bin/env sh

# Exit in case of error
set -e
export COMPOSE_PROJECT_NAME=test_twitter

sed -i 's/8000:8000/8888:8000/g' docker-compose.yml

docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml down -v --remove-orphans
docker-compose -f docker-compose.yml up -d
docker exec -i test_twitter_db_1 psql -U ${POSTGRES_USER} postgres -c "CREATE DATABASE ${TEST_POSTGRES_DB}"
docker exec -i test_twitter_app_1 pytest
docker-compose -f docker-compose.yml down -v --remove-orphans
