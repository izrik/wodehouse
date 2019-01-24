#!/bin/sh

SOURCES=wodehouse,wtypes,functions,macros

coverage run --branch --source=$SOURCES -m unittest discover -s tests -p '*.py' -t . && \
    coverage run -a --branch --source=$SOURCES ./wodehouse.py --run-files tests/*tests.w && \
# TODO: coverage run -a --branch --source=$SOURCES ./wodehouse.py wodehouse.w -- tests/*tests.w && \
    coverage html && \
    flake8 *.py functions macros wtypes && \
    # TODO: wlint
    ./compare_sources.py
