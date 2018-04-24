#!/bin/sh

coverage run --source=wodehouse ./run_tests.py && \
    coverage html && \
    ./wodehouse.py tests/*tests.w && \
    flake8 *.py
