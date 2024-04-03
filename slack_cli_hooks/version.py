"""Check the latest version at https://pypi.org/project/slack-cli-hooks/"""

import os

__version__ = os.environ.get("SLACK_CLI_HOOKS_VERSION", "0.0.0.dev0")
