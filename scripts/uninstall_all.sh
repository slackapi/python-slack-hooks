#!/bin/bash

pip uninstall -y slack-cli-hooks

PACKAGES=$(pip freeze | grep -v "^-e" | sed 's/@.*//' | sed 's/\=\=.*//')

for package in $PACKAGES; do
  pip uninstall -y $package
done
