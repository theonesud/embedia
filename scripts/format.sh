#!/usr/bin/env bash

set -e
set -x

ruff embedia tests scripts --fix
black embedia tests scripts
