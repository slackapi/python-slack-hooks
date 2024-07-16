#!/usr/bin/env python
import os
import runpy
import sys

from slack_cli_hooks.error import CliError
from slack_cli_hooks.protocol import Protocol, build_protocol

PROTOCOL: Protocol

DEFAULT_MAIN_FILE = "app.py"


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
    entrypoint_path = get_main_path(working_directory)

    if not os.path.exists(entrypoint_path):
        raise CliError(f"Could not find {get_main_file()} file")

    parent_package = os.path.dirname(entrypoint_path)

    try:
        sys.path.insert(0, parent_package)  # Add parent package to sys path
        runpy.run_path(entrypoint_path, run_name="__main__")
    finally:
        sys.path.remove(parent_package)


if __name__ == "__main__":
    PROTOCOL = build_protocol(argv=sys.argv)
    start(os.getcwd())
