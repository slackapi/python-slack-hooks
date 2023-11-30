#!/bin/bash
# ./scripts/run_pytype.sh

sh scripts/install.sh

pip install -r requirements/format.txt

pytype slack_cli_hooks/
