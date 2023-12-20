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
from slack_cli_hooks.protocol.default_protocol import DefaultProtocol


class TestGetManifest:
    def setup_method(self):
        check_update.PROTOCOL = DefaultProtocol()

    def build_pypi_response(self, project: str, status: int = 200, headers=HTTPMessage(), body={}) -> PypiResponse:
        headers.add_header("Content-Type", 'application/json; charset="UTF-8"')

        return PypiResponse(
            url=f"https://pypi.org/pypi/{project}/json",
            status=status,
            headers=headers,
            body=json.dumps(body),
        )

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
        mock_response = self.build_pypi_response(project, body={"info": {}, "releases": {}})

        with patch.object(check_update, pypi_get.__name__) as mock_pypi_get:
            mock_pypi_get.return_value = mock_response
            json_response = pypi_get_json(project)

        assert json_response == {"info": {}, "releases": {}}

    def test_pypi_get_json_fail(self):
        project = "my_test_project"
        mock_response = self.build_pypi_response(project, status=300)

        with patch.object(check_update, pypi_get.__name__) as mock_pypi_get:
            mock_pypi_get.return_value = mock_response
            with pytest.raises(PypiError) as e:
                pypi_get_json(project)

            assert "300" in str(e)
            assert f"https://pypi.org/pypi/{project}/json" in str(e)

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

        assert vars(actual) == {
            "name": "test-dependency",
            "current": "0.0.0",
            "latest": "0.0.1",
            "update": True,
            "breaking": False,
        }

    def test_error_build_release(self):
        test_dependency = MagicMock()
        test_dependency.version.__version__ = "0.0.0"
        test_dependency.__name__ = "test-dependency"

        with patch.object(check_update, pypi_get_json.__name__) as mock_pypi_get_json:
            mock_pypi_get_json.return_value = {"info": {"version": "0.0.1"}}
            actual = build_release(test_dependency)

        assert vars(actual) == {
            "name": "test-dependency",
            "current": "0.0.0",
            "latest": "0.0.1",
            "update": True,
            "breaking": False,
        }

    def test_build_output(self):
        actual = build_output([])

        assert actual == {
            "name": "Slack Bolt",
            "url": "https://api.slack.com/future/changelog",
            "releases": [],
        }
