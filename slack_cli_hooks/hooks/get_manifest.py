#!/usr/bin/env python
import os
import re
from typing import List

from slack_cli_hooks.error import CliError
from slack_cli_hooks.protocol import Protocol, build_protocol

PROTOCOL: Protocol

EXCLUDED_DIRECTORIES = [
    "lib",
    "bin",
    "include",
    "node_modules",
    "packages",
    "logs",
    "build",
    "coverage",
    "target",
    "tmp",
    "test",
    "tests",
]

DIRECTORY_IGNORE_REGEX = re.compile(r"(^\.|^\_|^{}$)".format("$|^".join(EXCLUDED_DIRECTORIES)), re.IGNORECASE)


def filter_directories(directories: List[str]) -> List[str]:
    return [directory for directory in directories if not DIRECTORY_IGNORE_REGEX.match(directory)]


def find_file_path(path: str, file_name: str) -> str:
    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        dirs[:] = filter_directories(dirs)
        if file_name in files:
            return os.path.join(root, file_name)
    raise CliError(f"Could not find a {file_name} file")


def get_manifest(working_directory: str) -> str:
    file_path = find_file_path(working_directory, "manifest.json")

    with open(file_path, "r") as manifest:
        return manifest.read()


if __name__ == "__main__":
    PROTOCOL = build_protocol()
    PROTOCOL.respond(get_manifest(os.getcwd()))
