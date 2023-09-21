#!/usr/bin/env bash

set -e
set -x

rm -r dist

pip install --upgrade build
python -m build

pip install --upgrade twine
twine upload dist/*
