#!/bin/bash

# mypy embedia
# mypy tests
# flake8
# autopep8
# isort

command="python -m pytest -s"

for arg in "$@"
do
    command="$command $arg"
done

eval $command

# --cov=./ --cov-report=html

# python -m pytest