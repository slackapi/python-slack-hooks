#!/bin/bash

# Remove slack-cli-hooks without a version specifier so that local builds are cleaned up
pip uninstall -y slack-cli-hooks
# Collect all installed packages
PACKAGES=$(pip freeze | grep -v "^-e" | sed 's/@.*//' | sed 's/\=\=.*//')
# Uninstall packages without exiting on a failure
for package in $PACKAGES; do
  pip uninstall -y $package
done
