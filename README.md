# python-slack-hooks

Helper library implementing the contract between the [Slack CLI](https://api.slack.com/automation/cli) and [Bolt for Python](https://slack.dev/bolt-python/)

## Setup

Before getting started, make sure you have a development workspace where you have permissions to install apps. If you don’t have one set up, go ahead and create one.

### Install the Slack CLI

Install the Slack CLI. Step-by-step instructions can be found in this [Quickstart Guide](https://api.slack.com/automation/cli).

### Install this package

```bash
# Python 3.6+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install slack-cli-hooks
```

## Creating a Bolt app

Next, we will create a Bolt for Python app in the same directory where we installed `slack-cli-hooks`, define basic information and metadata about our app via an [App Manifest](https://api.slack.com/reference/manifests) (`manifest.json`) and finally create a `slack.json` file that defines the interface between the [Slack CLI](https://api.slack.com/automation/cli) and [Bolt for Python](https://slack.dev/bolt-python/concepts).

### Source code

Create a [Bolt for Python](https://slack.dev/bolt-python/concepts) app in a file named `app.py`.

```python
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.DEBUG)

app = App()

# Add functionality here

if __name__ == "__main__":
    SocketModeHandler(app.start(3000)).start()
```

### Application Configuration

Define your [Application Manifest](https://api.slack.com/reference/manifests) in a `manifest.json` file.

```json
{
  "$schema": "https://raw.githubusercontent.com/slackapi/manifest-schema/main/manifest.schema.json",
  "_metadata": {
    "major_version": 1,
    "minor_version": 1
  },
  "display_information": {
    "name": "most-basic-app"
  },
  "outgoing_domains": [],
  "settings": {
    "org_deploy_enabled": true,
    "socket_mode_enabled": true,
    "token_rotation_enabled": false
  },
  "features": {
    "bot_user": {
      "display_name": "most-basic-app"
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": ["chat:write"]
    }
  }
}
```

Define the Slack CLI configuration in a file named `slack.json`.

```json
{
  "hooks": {
    "get-hooks": "python3 -m slack_cli_hooks.hooks.get_hooks"
  }
}
```

Create an empty folder named `.slack`

### Running the app

You should now be able to harness the power of the Slack CLI and Bolt.

Run the app this way:

```zsh
slack run
```
