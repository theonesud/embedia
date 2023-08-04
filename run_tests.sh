#!/bin/bash

command="python -m pytest"

for arg in "$@"
do
    command="$command $arg"
done

eval $command
