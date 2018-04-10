#!/bin/sh

coverage run --source=wodehouse ./run_tests.py && \
    coverage html && \
    flake8 *.py
