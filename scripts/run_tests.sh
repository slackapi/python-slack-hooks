#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/run_tests.sh
# single: ./scripts/run_tests.sh tests/scenario_tests/test_app.py

test_target="$1"
source ./scripts/_utils.sh

set_prj_as_cwd

format

if [[ $test_target != "" ]]
then
  pytest -vv $1
else
  pytest
fi
