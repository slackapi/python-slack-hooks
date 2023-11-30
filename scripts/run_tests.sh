#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/run_tests.sh
# single: ./scripts/run_tests.sh tests/scenario_tests/test_app.py

test_target="$1"
python_version=`python --version | awk '{print $2}'`

sh scripts/setup.sh
black slack_cli_hooks/ tests/

if [[ $test_target != "" ]]
then
  pytest -vv $1
else
  pytest tests/*
fi
