#!/bin/bash

set_prj_as_cwd() {
	script_dir=`dirname $0`
	cd ${script_dir}/.. 
}

clean_project() {
	rm -rf dist/ build/ slack_cli_hooks.egg-info/
}

install_development_requirements() {
	pip install -U pip
	pip install -e .
	pip install -r requirements/testing.txt
	pip install -r requirements/format.txt
}

build() {
	pip install -r requirements/build.txt && \
	python -m build && \
	twine check dist/*
}

format() {
	black slack_cli_hooks/ tests/
}
