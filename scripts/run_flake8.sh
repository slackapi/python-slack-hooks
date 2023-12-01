#!/bin/bash
# ./scripts/run_flake8.sh

source ./scripts/_utils.sh

set_prj_as_cwd

pip install -U pip
pip install -r requirements/format.txt

flake8 slack_cli_hooks/ && flake8 tests/
