#!/usr/bin/env python
import json
from urllib.request import urlopen, Request

from slack_cli_hooks.protocol import Protocol, build_protocol
from http.client import HTTPResponse, HTTPMessage

PROTOCOL: Protocol


class PypiResponse:
    def __init__(self, status: int, headers: HTTPMessage, body: str):
        self.status = status
        self.headers = headers
        self.body = body


def get_pypi_response(project: str) -> PypiResponse:
    # Based on https://warehouse.pypa.io/api-reference/json.html
    url = f"https://pypi.org/pypi/{project}/json"
    request = Request(method="GET", url=url, headers={"Accept": "application/json"})
    response: HTTPResponse = urlopen(request)
    charset = response.headers.get_content_charset() or "utf-8"
    return PypiResponse(status=response.getcode, headers=response.headers, body=response.read().decode(charset))


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
    PROTOCOL = build_protocol()
    resp = get_pypi_response("slack-bolt")
    PROTOCOL.respond(json.dumps({"status": resp.status, "headers": resp.headers, "body": json.loads(resp.body)}))
