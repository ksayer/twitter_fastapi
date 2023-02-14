#!/bin/bash

black --check --diff src/
isort --check-only --diff --profile black src/
flake8 src/
