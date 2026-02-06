#!/bin/bash
# Run all the tests or a single test with installation
# all: ./scripts/install_and_run_tests.sh
# single: ./scripts/install_and_run_tests.sh tests/scenario_tests/test_app.py

script_dir=$(dirname $0)
cd ${script_dir}/..

test_target="$1"

./scripts/install.sh

if [[ $test_target != "" ]]
then
    ./scripts/format.sh --no-install
    pytest -vv $test_target
else
    ./scripts/format.sh --no-install
    ./scripts/lint.sh --no-install
    pytest
fi
