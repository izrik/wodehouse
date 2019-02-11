#!/bin/sh

SOURCES=wodehouse,wtypes,functions,macros,modules,runtime,version

coverage run --branch --source=$SOURCES -m unittest discover -s tests -p '*.py' -t . && \
    coverage run -a --branch --source=$SOURCES ./wodehouse.py -m unittest -s tests && \
# TODO: coverage run -a --branch --source=$SOURCES ./wodehouse.py wodehouse.w unittest.w -s tests -t . && \
    coverage html && \
    flake8 *.py functions macros wtypes modules tests && \
    # TODO: wlint
    ./compare_sources.py
