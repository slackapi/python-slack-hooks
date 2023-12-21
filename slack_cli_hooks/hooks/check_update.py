#!/usr/bin/env python
import json
from http.client import HTTPResponse
from types import ModuleType
from typing import Any, Dict, List, Optional
from urllib import request

import slack_bolt
import slack_sdk
from pkg_resources import parse_version as Version

import slack_cli_hooks.version
from slack_cli_hooks.error import PypiError
from slack_cli_hooks.protocol import Protocol, build_protocol

PROTOCOL: Protocol

DEPENDENCIES: List[ModuleType] = [slack_cli_hooks, slack_bolt, slack_sdk]


def parse_major(v: Version) -> int:
    """The first item of :attr:`release` or ``0`` if unavailable.

    >>> parse_major(Version("1.2.3"))
    1
    """
    # This implementation comes directly from the Version implementation since it is not supported in 3.6
    # source: https://github.com/pypa/packaging/blob/main/src/packaging/version.py
    return v._version.release[0] if len(v._version) >= 1 else 0  # type: ignore


class Release:
    def __init__(
        self,
        name: str,
        current: Optional[Version] = None,
        latest: Optional[Version] = None,
        message: Optional[str] = None,
        url: Optional[str] = None,
        error: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        if current and latest:
            self.current = current.base_version
            self.latest = latest.base_version
            self.update = current < latest
            self.breaking = (parse_major(current) - parse_major(latest)) != 0
        if error:
            self.error = error
        if message:
            self.message = message
        if url:
            self.url = url


def pypi_get(project: str, headers={"Accept": "application/json"}) -> HTTPResponse:
    # Based on https://warehouse.pypa.io/api-reference/json.html
    url = f"https://pypi.org/pypi/{project}/json"
    pypi_request = request.Request(method="GET", url=url, headers=headers)
    return request.urlopen(pypi_request)


def pypi_get_json(project: str) -> Dict[str, Any]:
    pypi_response = pypi_get(project)
    charset = pypi_response.headers.get_content_charset() or "utf-8"
    raw_body = pypi_response.read().decode(charset)
    if pypi_response.status > 200:
        PROTOCOL.debug(f"Received status {pypi_response.status} from {pypi_response.url}")
        PROTOCOL.debug(f"Headers {dict(pypi_response.getheaders())}")
        PROTOCOL.debug(f"Body {raw_body}")
        raise PypiError(f"Received status {pypi_response.status} from {pypi_response.url}")
    return json.loads(raw_body)


def extract_latest_version(payload: Dict[str, Any]) -> str:
    if "info" not in payload:
        raise PypiError("Missing `info` field in pypi payload")
    if "version" not in payload["info"]:
        raise PypiError("Missing `version` field in pypi payload['info']")
    return payload["info"]["version"]


def build_release(dependency: ModuleType) -> Release:
    name = dependency.__name__
    try:
        pypi_json_payload = pypi_get_json(name)
        return Release(
            name=name,
            current=Version(dependency.version.__version__),
            latest=Version(extract_latest_version(pypi_json_payload)),
        )
    except PypiError as e:
        return Release(name=name, error={"message": str(e)})


def build_output(dependencies: List[ModuleType] = DEPENDENCIES) -> Dict[str, Any]:
    output = {"name": "Slack Bolt", "url": "https://api.slack.com/future/changelog", "releases": []}
    errors = []

    for dep in dependencies:
        release = build_release(dep)
        output["releases"].append(vars(release))

        if hasattr(release, "error"):
            errors.append(release.name)

    if errors:
        output["error"] = {"message": f"An error occurred fetching updates for the following packages: {', '.join(errors)}"}
    return output


if __name__ == "__main__":
    PROTOCOL = build_protocol()
    PROTOCOL.respond(json.dumps(build_output()))
