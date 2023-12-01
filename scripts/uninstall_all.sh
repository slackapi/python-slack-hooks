#!/bin/bash

pip uninstall -y slack-cli-hooks && \
  pip freeze | grep -v "^-e" | xargs pip uninstall -y
