#!/bin/bash

sh scripts/_setup.sh

pip install -r requirements/build.txt && \
  rm -rf dist/ build/ slack_cli_hooks.egg-info/ && \
  python -m build --sdist --wheel && \
  twine check dist/*
