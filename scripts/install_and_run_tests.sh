#!/bin/bash
# all: ./scripts/install_and_run_tests.sh
# single: ./scripts/install_and_run_tests.sh tests/scenario_tests/test_app.py

test_target="$1"
source ./scripts/_utils.sh

set_prj_as_cwd

install_development_requirements

format

if [[ $test_target != "" ]]
then
    pytest -vv $1
else
    pytest && \
    pytype slack_cli_hooks/
fi
