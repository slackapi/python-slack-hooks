import json
import os
from http.client import HTTPMessage, HTTPResponse
from typing import Callable, Union
from unittest.mock import MagicMock
from urllib.request import Request


def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)


def build_fake_pypi_urlopen(status: int = 200, headers=HTTPMessage(), body={}) -> Callable[..., HTTPResponse]:
    headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

    mock_resp = HTTPResponse(MagicMock())
    mock_resp.headers = headers
    mock_resp.status = status
    mock_resp.read = MagicMock(return_value=json.dumps(body).encode("UTF-8"))

    def fake_urlopen(url: Union[str, Request]):
        mock_resp.url = url.full_url if isinstance(url, Request) else url
        return mock_resp

    return fake_urlopen


def build_fake_dependency(name: str, version: str):
    fake_dependency = MagicMock()
    fake_dependency.version.__version__ = version
    fake_dependency.__name__ = name
    return fake_dependency
