#!/bin/bash

script_dir=$(dirname $0)
cd ${script_dir}/..

rm -rf dist/ build/ slack_cli_hooks.egg-info/

pip install -r requirements/build.txt && \
python -m build && \
twine check dist/*

twine upload --repository testpypi dist/*
