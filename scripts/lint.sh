#!/usr/bin/env bash

set -e
set -x

mypy embedia
ruff embedia tests scripts
black embedia tests --check
