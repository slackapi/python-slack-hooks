from http.client import HTTPMessage
import json
from unittest.mock import MagicMock, patch

import pytest
from slack_cli_hooks.error import PypiError

from slack_cli_hooks.hooks import check_update
from slack_cli_hooks.hooks.check_update import (
    PypiResponse,
    build_output,
    build_release,
    extract_latest_version,
    pypi_get,
    pypi_get_json,
)


class TestGetManifest:
    def test_pypi_get(self):
        mock_headers = HTTPMessage()
        mock_headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        mock_resp = MagicMock()
        mock_resp.headers = mock_headers
        mock_resp.getcode = MagicMock(return_value=200)
        mock_resp.read = MagicMock(return_value=b"{}")

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = mock_resp
            response = pypi_get("test")

        assert response.status == 200
        assert response.body == "{}"

    def test_pypi_get_json(self):
        project = "my_test_project"
        mock_headers = HTTPMessage()
        mock_headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        mock_response = PypiResponse(
            url="https://pypi.org/pypi/{project}/json",
            status=200,
            headers=mock_headers,
            body=json.dumps({"info": {}, "releases": {}}),
        )

        with patch.object(check_update, pypi_get.__name__) as mock_pypi_get:
            mock_pypi_get.return_value = mock_response
            json_response = pypi_get_json(project)

        assert json_response == {"info": {}, "releases": {}}

    def test_pypi_get_json_fail(self):
        project = "my_test_project"
        mock_headers = HTTPMessage()
        mock_headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        mock_response = PypiResponse(
            url="https://pypi.org/pypi/{project}/json",
            status=300,
            headers=mock_headers,
            body=json.dumps({"info": {}, "releases": {}}),
        )

        with patch.object(check_update, pypi_get.__name__) as mock_pypi_get:
            mock_pypi_get.return_value = mock_response
            with pytest.raises(PypiError) as e:
                pypi_get_json(project)

            assert "300" in str(e)
            assert "https://pypi.org/pypi/{project}/json" in str(e)

    def test_extract_latest_version(self):
        test_payload = {"info": {"version": "0.0.0"}}
        actual = extract_latest_version(test_payload)
        assert actual == "0.0.0"

    def test_extract_latest_version_missing_info(self):
        test_payload = {}
        with pytest.raises(PypiError) as e:
            extract_latest_version(test_payload)
            assert "info" in str(e)

    def test_extract_latest_version_missing_version(self):
        test_payload = {"info": {}}
        with pytest.raises(PypiError) as e:
            extract_latest_version(test_payload)
            assert "version" in str(e)
            assert "payload['info']" in str(e)

    def test_build_release(self):
        test_dependency = MagicMock()
        test_dependency.version.__version__ = "0.0.0"
        test_dependency.__name__ = "test-dependency"

        with patch.object(check_update, pypi_get_json.__name__) as mock_pypi_get_json:
            mock_pypi_get_json.return_value = {"info": {"version": "0.0.1"}}
            actual = build_release(test_dependency)

        assert actual == {
            "name": "test-dependency",
            "current": "0.0.0",
            "latest": "0.0.1",
            "update": True,
            "breaking": False,
            "error": None,
        }

    def test_build_output(self):
        actual = build_output([])

        assert actual == {
            "name": "Slack Bolt",
            "message": "",
            "url": "https://api.slack.com/future/changelog",
            "releases": [],
            "error": None,
        }
