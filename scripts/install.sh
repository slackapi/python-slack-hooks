#!/bin/bash

script_dir=$(dirname $0)
cd ${script_dir}/..

export PIP_REQUIRE_VIRTUALENV=1
pip install -U pip
pip install -e .
pip install -r requirements/testing.txt
pip install -r requirements/format.txt
