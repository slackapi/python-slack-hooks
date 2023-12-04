#!/bin/bash
source ./scripts/_utils.sh

set_prj_as_cwd

clean_project

build

twine upload dist/*
