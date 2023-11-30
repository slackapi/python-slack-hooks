#!/bin/bash

sh scripts/setup.sh

test_target="$1"
python_version=`python --version | awk '{print $2}'`

if [ ${python_version:0:3} == "3.6" ]
then
  pip install -r requirements.txt
else
  pip install -e .
fi

pip install -r requirements/testing.txt
pip install -r requirements/format.txt
