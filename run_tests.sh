#!/bin/sh

SOURCES=wodehouse,wtypes,functions,macros,modules,runtime,version

echo "Running python unit tests in tests/ with coverage..." && \
    coverage run --branch --source=$SOURCES -m pytest -o python_files=\*.py tests/ && \
    echo "" && echo "Running w-lang unit tests in tests/ with w-coverage via wodehouse.py with py-coverage..." && \
    coverage run -a --branch --source=$SOURCES ./wodehouse.py -m coverage run -m unittest -s tests && \
# TODO: coverage run -a --branch --source=$SOURCES ./wodehouse.py wodehouse.w unittest.w -s tests -t . && \
    echo "" && echo "Converting py-coverage to html..." && \
    coverage html && \
    echo "" && echo "Running flake8..." && \
    flake8 ./*.py functions macros wtypes modules tests --exclude=.svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg,.venv && \
    shellcheck ./*.sh && /
    # TODO: wlint
    echo "" && echo "Comparing python and w-lang sources..." && \
    ./compare_sources.py
