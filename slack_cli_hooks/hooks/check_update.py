#!/usr/bin/env python
from http.client import HTTPMessage, HTTPResponse
import json
from types import ModuleType
from typing import Any, Dict, List
from urllib import request
from pkg_resources import parse_version
import slack_bolt
import slack_sdk
import slack_cli_hooks.version

from slack_cli_hooks.protocol import Protocol, build_protocol
from slack_cli_hooks.error import PypiError

PROTOCOL: Protocol = build_protocol()

DEPENDENCIES: List[ModuleType] = [slack_cli_hooks, slack_bolt, slack_sdk]


class PypiResponse:
    def __init__(self, url: str, status: int, headers: HTTPMessage, body: str):
        self.url = url
        self.status = status
        self.headers = headers
        self.body = body


def pypi_get(project: str) -> PypiResponse:
    # Based on https://warehouse.pypa.io/api-reference/json.html
    url = f"https://pypi.org/pypi/{project}/json"
    pypi_request = request.Request(method="GET", url=url, headers={"Accept": "application/json"})
    response: HTTPResponse = request.urlopen(pypi_request)
    charset = response.headers.get_content_charset() or "utf-8"
    return PypiResponse(
        url=response.url, status=response.getcode(), headers=response.headers, body=response.read().decode(charset)
    )


def pypi_get_json(project: str) -> Dict[str, Any]:
    pypi_response = pypi_get(project)
    if pypi_response.status > 200:
        PROTOCOL.debug(f"Received status {pypi_response.status} from {pypi_response.url}")
        PROTOCOL.debug(f"Headers {pypi_response.headers.items()}")
        PROTOCOL.debug(f"Body {pypi_response.body}")
        raise PypiError(f"Received status {pypi_response.status} from {pypi_response.url}")
    return json.loads(pypi_response.body)


def extract_latest_version(payload: Dict[str, Any]) -> str:
    if "info" not in payload:
        raise PypiError("Missing `info` field in pypi payload")
    if "version" not in payload["info"]:
        raise PypiError("Missing `version` field in pypi payload['info']")
    return payload["info"]["version"]


def build_release(dependency: ModuleType):
    name = dependency.__name__
    pypi_json_payload = pypi_get_json(name)
    latest_version = parse_version(extract_latest_version(pypi_json_payload))
    current_version = parse_version(dependency.version.__version__)
    return {
        "name": name,
        "current": current_version.base_version,
        "latest": latest_version.base_version,
        "update": current_version < latest_version,
        "breaking": (latest_version.major - current_version.major) != 0,
        "error": None,
    }


def build_check_update() -> Dict[str, Any]:
    releases = [build_release(dep) for dep in DEPENDENCIES]
    return {
        "name": "Slack Bolt",
        "message": "",
        "url": "https://api.slack.com/future/changelog",
        "releases": releases,
        "error": None,
    }


if __name__ == "__main__":
    PROTOCOL.respond(json.dumps(build_check_update()))
