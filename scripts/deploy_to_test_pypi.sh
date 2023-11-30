#!/bin/bash

sh scripts/build_pypi_package.sh

twine upload --repository testpypi dist/*
