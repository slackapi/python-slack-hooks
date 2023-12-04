#!/bin/bash

source ./scripts/_utils.sh

set_prj_as_cwd

install_development_requirements

pytype slack_cli_hooks/
