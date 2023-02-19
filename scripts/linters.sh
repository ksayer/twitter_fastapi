#!/bin/bash

echo black.......
black --check --diff --skip-string-normalization src/
echo Black completed

echo isort.......
isort --check-only --diff --profile black src/
echo isort completed.

echo flake8.......
flake8 src/
echo flake8 completed

echo mypy.......
mypy src/
echo mypy completed