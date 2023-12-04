#!/usr/bin/env python
import os
import runpy
import sys

from slack_cli_hooks.error import CliError
from slack_cli_hooks.protocol import Protocol, protocol_factory

PROTOCOL: Protocol

DEFAULT_MAIN_FILE = "app.py"

SLACK_CLI_XOXB = "SLACK_CLI_XOXB"
SLACK_CLI_XAPP = "SLACK_CLI_XAPP"
SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN"
SLACK_APP_TOKEN = "SLACK_APP_TOKEN"


class EnvVarHandler:
    def __init__(self, name: str) -> None:
        self.name = name
        self._is_set = name in os.environ

    def set_default(self, value: str) -> None:
        if not self._is_set:
            os.environ[self.name] = value

    def clean(self) -> None:
        if not self._is_set:
            os.environ.pop(self.name, None)


def validate_env() -> None:
    if not os.environ.get(SLACK_CLI_XOXB):
        raise CliError(f"Missing local run bot token ({SLACK_CLI_XOXB}).")
    if not os.environ.get(SLACK_CLI_XAPP):
        raise CliError(f"Missing local run app token ({SLACK_CLI_XAPP}).")


def get_main_file() -> str:
    custom_file = os.environ.get("SLACK_APP_PATH")
    if custom_file:
        return custom_file
    return DEFAULT_MAIN_FILE


def get_main_path(working_directory: str) -> str:
    main_file = get_main_file()
    main_raw_path = os.path.join(working_directory, main_file)
    return os.path.abspath(main_raw_path)


def start(working_directory: str) -> None:
    validate_env()

    entrypoint_path = get_main_path(working_directory)

    if not os.path.exists(entrypoint_path):
        raise CliError(f"Could not find {get_main_file()} file")

    parent_package = os.path.dirname(entrypoint_path)

    bot_token_var = EnvVarHandler(SLACK_BOT_TOKEN)
    app_token_var = EnvVarHandler(SLACK_APP_TOKEN)

    try:
        bot_token_var.set_default(os.environ[SLACK_CLI_XOXB])
        app_token_var.set_default(os.environ[SLACK_CLI_XAPP])
        sys.path.insert(0, parent_package)  # Add parent package to sys path

        runpy.run_path(entrypoint_path, run_name="__main__")
    finally:
        sys.path.remove(parent_package)
        bot_token_var.clean()
        app_token_var.clean()


if __name__ == "__main__":
    PROTOCOL = protocol_factory()
    start(os.getcwd())
