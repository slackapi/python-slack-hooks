# Python Slack Hooks

This library defines the contract between the
[Slack CLI](https://api.slack.com/automation/cli/install) and
[Bolt for Python](https://slack.dev/bolt-python/).

## Overview
This library enables inter-process communication between the [Slack CLI](https://api.slack.com/automation/cli/install) and applications built with Bolt for Python. 

When used together, the CLI delegates various tasks to the Bolt application by invoking processes ("hooks") and then making use of the responses provided by each hook's `stdout`. 

For a complete list of available hooks, read the [Supported Hooks](#supported-hooks) section.

## Requirements
The latest minor version of [Bolt v1](https://pypi.org/project/slack-bolt/) is recommended.

## Usage
A Slack CLI-compatible Slack application includes a `./slack.json` file that contains hooks specific to that project. Each hook is associated with commands that are available in the Slack CLI. By default, `get-hooks` retrieves all of the [supported hooks](#supported-hooks) and their corresponding scripts as defined in this library.

The CLI will always use the version of the `python-slack-hooks` that is specified in the project's `requirements.txt`.

### Supported Hooks

The hooks currently supported for use within the Slack CLI include `check-update`, `get-hooks`, `get-manifest`, and `start`:

| Hook Name  | CLI Command  | File  |  Description  |
| --- | --- | --- | --- |
| `check-update` | `slack update` | [check_update.py](./slack_cli_hooks/hooks/check_update.py) | Checks the project's Slack dependencies to determine whether or not any libraries need to be updated. |
| `get-hooks` | All | [get_hooks.py](./slack_cli_hooks/hooks/get_hooks.py) | Fetches the list of available hooks for the CLI from this repository. |
| `get-manifest` | `slack manifest` | [get_manifest.py](./slack_cli_hooks/hooks/get_manifest.py) | Converts a `manifest.json` file into a valid manifest JSON payload. |
| `start` | `slack run` | [start.py](./slack_cli_hooks/hooks/start.py) | While developing locally, the CLI manages a socket connection with Slack's backend and utilizes this hook for events received via this connection. |


### Overriding Hooks
To customize the behavior of a hook, add the hook to your application's `/slack.json` file, and provide a corresponding script to be executed. 

When commands are run, the Slack CLI will look to the project's hook definitions and use those instead of what's defined in this library, if provided.

Below is an example `/slack.json` file that overrides the default `start`:

```
{
  "hooks": {
    "get-hooks": "python3 -m slack_cli_hooks.hooks.get_hooks",
    "start": "python3 app.py"
  }
}
```

## Contributing

Contributions are always welcome! Please review the
[contributing guidelines](https://github.com/slackapi/python-slack-hooks/blob/main/.github/CONTRIBUTING.md)
for more information.