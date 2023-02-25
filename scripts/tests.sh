#! /usr/bin/env sh

# Exit in case of error
set -e

docker-compose -f docker-compose.tests.yml build
docker-compose -f docker-compose.tests.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-compose.tests.yml up -d
docker-compose -f docker-compose.tests.yml exec -T test_app pytest
docker-compose -f docker-compose.tests.yml down -v --remove-orphans
