#!/bin/sh

SOURCES=wodehouse,wtypes,functions,macros

coverage run --branch --source=$SOURCES ./run_tests.py && \
    coverage run -a --branch --source=$SOURCES ./wodehouse.py tests/*tests.w && \
# TODO: coverage run -a --branch --source=$SOURCES ./wodehouse.py wodehouse.w -- tests/*tests.w && \
#   TODO: argparse
    coverage html && \
    flake8 *.py functions macros wtypes && \
    ./compare_sources.py
