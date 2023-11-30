#!/bin/bash

sh scripts/_setup.sh

pip install -r requirements/format.txt
black slack_cli_hooks/ tests/
