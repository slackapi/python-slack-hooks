<h1 align="center">Python Slack Hooks</h1>

A helper library implementing the contract between the
[Slack CLI][slack-cli-docs] and
[Bolt for Python](https://slack.dev/bolt-python/)

## Environment requirements

Before getting started, make sure you have a development workspace where you
have permissions to install apps. **Please note that leveraging all features in
this project require that the workspace be part of
[a Slack paid plan](https://slack.com/pricing).**

### Install the Slack CLI

Install the Slack CLI. Step-by-step instructions can be found in this
[Quickstart Guide][slack-cli-docs].

### Environment Setup

Create a project folder and a
[virtual environment](https://docs.python.org/3/library/venv.html#module-venv)
within it

```zsh
# Python 3.6+ required
mkdir myproject
cd myproject
python3 -m venv .venv
```

Activate the environment

```zsh
source .venv/bin/activate
```

### Pypi

Install this package using pip.

```zsh
pip install -U slack-cli-hooks
```

### Clone

Clone this project using git.

```zsh
git clone https://github.com/slackapi/python-slack-hooks.git
```

Follow the
[Develop Locally](https://github.com/slackapi/python-slack-hooks/blob/main/.github/maintainers_guide.md#develop-locally)
steps in the maintainers guide to build and use this package.

## Simple project

In the same directory where we installed `slack-cli-hooks`

1. Define basic information and metadata about our app via an
   [App Manifest](https://api.slack.com/reference/manifests) (`manifest.json`).
2. Create a `slack.json` file that defines the interface between the
   [Slack CLI][slack-cli-docs] and [Bolt for Python][bolt-python-docs].
3. Use an `app.py` file to define the entrypoint for a
   [Bolt for Python][bolt-python-docs] project.

### Application Configuration

Define your [Application Manifest](https://api.slack.com/reference/manifests) in
a `manifest.json` file.

```json
{
  "display_information": {
    "name": "simple-app"
  },
  "outgoing_domains": [],
  "settings": {
    "org_deploy_enabled": true,
    "socket_mode_enabled": true,
  },
  "features": {
    "bot_user": {
      "display_name": "simple-app"
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": ["chat:write"]
    }
  }
}
```

### CLI/Bolt Interface Configuration

Define the Slack CLI configuration in a file named `slack.json`.

```json
{
  "hooks": {
    "get-hooks": "python3 -m slack_cli_hooks.hooks.get_hooks"
  }
}
```

### Source code

Create a [Bolt for Python][bolt-python-docs] app in a file named `app.py`.
Alternatively you can use an existing app instead.

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App()

# Add functionality here

if __name__ == "__main__":
    SocketModeHandler(app).start()
```

## Running the app

You should now be able to harness the power of the Slack CLI and Bolt.

Run the app this way:

```zsh
slack run
```

## Getting Help

If you get stuck we're here to help. Ensure your issue is related to this
project and not to [Bolt for Python][bolt-python-docs]. The following are the
best ways to get assistance working through your issue:

- [Issue Tracker](https://github.com/slackapi/python-slack-hooks/issues) for
  questions, bug reports, feature requests, and general discussion. **Try
  searching for an existing issue before creating a new one.**
- Email our developer support team: `support@slack.com`

## Contributing

Contributions are more then welcome. Please look at the
[contributing guidelines](https://github.com/slackapi/python-slack-hooks/blob/main/.github/CONTRIBUTING.md)
for more info!

[slack-cli-docs]: https://api.slack.com/automation/cli
[bolt-python-docs]: https://slack.dev/bolt-python/concepts
