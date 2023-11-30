#!/bin/bash

# Set root of project as current working directory
script_dir=`dirname $0`
cd ${script_dir}/.. 

rm -rf ./slack_cli_hooks.egg-info
pip install -U pip
