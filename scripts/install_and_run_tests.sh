#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/install_all_and_run_tests.sh
# single: ./scripts/install_all_and_run_tests.sh tests/scenario_tests/test_app.py

sh scripts/install.sh
sh scripts/format.sh

if [[ $test_target != "" ]]
then
    pytest $1
else
    pytest && \
      pytype slack_cli_hooks/
fi
