#!/bin/bash
# ./scripts/run_flake8.sh

sh script/setup.py

pip install -r requirements/format.txt

flake8 slack_cli_hooks/ && flake8 tests/
