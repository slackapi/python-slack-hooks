#!/usr/bin/env python
import json
from typing import Any, Dict
from urllib import request

from slack_cli_hooks.protocol import Protocol, build_protocol
from slack_cli_hooks.error import CliError
from http.client import HTTPResponse, HTTPMessage

PROTOCOL: Protocol = build_protocol()


class PypiResponse:
    def __init__(self, url: str, status: int, headers: HTTPMessage, body: str):
        self.url = url
        self.status = status
        self.headers = headers
        self.body = body


def get_pypi_response(project: str) -> PypiResponse:
    # Based on https://warehouse.pypa.io/api-reference/json.html
    url = f"https://pypi.org/pypi/{project}/json"
    pypi_request = request.Request(method="GET", url=url, headers={"Accept": "application/json"})
    response: HTTPResponse = request.urlopen(pypi_request)
    charset = response.headers.get_content_charset() or "utf-8"
    return PypiResponse(
        url=response.url, status=response.getcode(), headers=response.headers, body=response.read().decode(charset)
    )


def get_pypi_json(project: str) -> Dict[str, Any]:
    pypi_response = get_pypi_response(project)
    if pypi_response.status > 200:
        PROTOCOL.debug(f"Received status {pypi_response.status} from {pypi_response.url}")
        PROTOCOL.debug(f"Headers {pypi_response.headers.items()}")
        PROTOCOL.debug(f"Body {pypi_response.body}")
        raise CliError(f"Received status {pypi_response.status} from {pypi_response.url}")
    return json.loads(pypi_response.body)


def extract_latest_version(payload: Dict[str, Any]) -> int:
    if "info" not in payload:
        raise CliError("Missing `info` field in pypi payload")
    if "version" not in payload["info"]:
        raise CliError("Missing `version` field in pypi payload['info']")
    return payload["info"]["version"]


example_output = {
    "name": "Slack Bolt",
    "message": "",
    "releases": [
        {
            "name": "deno_slack_hooks",
            "current": "1.2.2",
            "latest": "1.2.3",
            "update": True,
            "breaking": False,
            "error": None,
        },
        {"name": "deno_slack_sdk", "current": "2.5.0", "latest": "2.5.0", "update": False, "breaking": False, "error": None},
        {"name": "deno_slack_api", "current": "2.1.2", "latest": "2.1.2", "update": False, "breaking": False, "error": None},
    ],
    "url": "https://api.slack.com/future/changelog",
    "error": None,
}


if __name__ == "__main__":
    resp = get_pypi_response("slack-bolt")
    PROTOCOL.respond(json.dumps({"status": resp.status, "headers": resp.headers, "body": json.loads(resp.body)}))
