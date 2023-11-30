#!/bin/bash
# Generate API documents from the latest source code

sh scripts/_setup.sh

pip install -U pdoc3
rm -rf docs/api-docs
pdoc slack_cli_hooks --html -o docs/api-docs
open docs/api-docs/slack_cli_hooks/index.html
