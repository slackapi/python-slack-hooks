from http.client import HTTPMessage
import json
from unittest import mock

import pytest
from slack_cli_hooks.error import CliError

from slack_cli_hooks.hooks.check_update import PypiResponse, extract_latest_version, get_pypi_response, get_pypi_json_payload


def resolve_module(func) -> str:
    return f"slack_cli_hooks.hooks.check_update.{func.__name__}"


class TestGetManifest:
    def test_get_pypi_response(self):
        mock_headers = HTTPMessage()
        mock_headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        mock_resp = mock.MagicMock()
        mock_resp.headers = mock_headers
        mock_resp.getcode = mock.MagicMock(return_value=200)
        mock_resp.read = mock.MagicMock(return_value=b"{}")

        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = mock_resp
            response = get_pypi_response("test")

        assert response.status == 200
        assert response.body == "{}"

    def test_get_pypi_json(self):
        project = "my_test_project"
        mock_headers = HTTPMessage()
        mock_headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        mock_response = PypiResponse(
            url="https://pypi.org/pypi/{project}/json",
            status=200,
            headers=mock_headers,
            body=json.dumps({"info": {}, "releases": {}}),
        )

        with mock.patch(resolve_module(get_pypi_response)) as mock_get_pypi_response:
            mock_get_pypi_response.return_value = mock_response
            json_response = get_pypi_json_payload(project)

        assert json_response == {"info": {}, "releases": {}}

    def test_get_pypi_json_fail(self):
        project = "my_test_project"
        mock_headers = HTTPMessage()
        mock_headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        mock_response = PypiResponse(
            url="https://pypi.org/pypi/{project}/json",
            status=300,
            headers=mock_headers,
            body=json.dumps({"info": {}, "releases": {}}),
        )

        with mock.patch(resolve_module(get_pypi_response)) as mock_get_pypi_response:
            mock_get_pypi_response.return_value = mock_response
            with pytest.raises(CliError) as e:
                get_pypi_json_payload(project)

            assert "300" in str(e)
            assert "https://pypi.org/pypi/{project}/json" in str(e)

    def extract_latest_version(self):
        test_payload = {"info": {"version": "0.0.0"}}
        actual = extract_latest_version(test_payload)
        assert actual == "0.0.0"

    def extract_latest_version_missing_info(self):
        test_payload = {}
        with pytest.raises(CliError) as e:
            extract_latest_version(test_payload)
            assert "info" in str(e)

    def extract_latest_version_missing_version(self):
        test_payload = {"info": {}}
        with pytest.raises(CliError) as e:
            extract_latest_version(test_payload)
            assert "version" in str(e)
            assert "payload['info']" in str(e)
