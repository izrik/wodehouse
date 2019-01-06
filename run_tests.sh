#!/bin/sh

coverage run --source=wodehouse,wtypes,functions,macros ./run_tests.py && \
    coverage html && \
    ./wodehouse.py tests/*tests.w && \
    flake8 *.py functions macros wtypes
