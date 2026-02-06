#!/bin/bash
# ./scripts/lint.sh [--no-install]

script_dir=$(dirname "$0")
cd "${script_dir}/.."

if [[ "$1" != "--no-install" ]]; then
    export PIP_REQUIRE_VIRTUALENV=1
    pip install -U pip
    pip install -U -r requirements/format.txt
fi

black --check slack_cli_hooks/ tests/
flake8 slack_cli_hooks/ tests/
