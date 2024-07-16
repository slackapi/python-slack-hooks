from unittest.mock import patch
from urllib import request

from slack_cli_hooks.hooks import check_update
from slack_cli_hooks.hooks.check_update import build_output
from tests.mock_protocol import MockProtocol
from tests.utils import build_fake_dependency, build_fake_pypi_urlopen


class TestGetManifest:
    def setup_method(self):
        check_update.PROTOCOL = MockProtocol()

    def test_build_output(self):
        test_project = "test_proj"
        fake_pypi_urlopen = build_fake_pypi_urlopen(status=200, body={"info": {"version": "0.0.1"}})
        test_dependency = build_fake_dependency(test_project, "0.0.0")

        with patch.object(request, "urlopen") as mock_urlopen:
            mock_urlopen.side_effect = fake_pypi_urlopen
            actual = build_output([test_dependency])

        assert actual["name"] == "Slack Bolt"
        assert len(actual["releases"]) == 1
        assert actual["releases"][0]["name"] == test_project
        assert actual["releases"][0]["current"] == "0.0.0"
        assert actual["releases"][0]["latest"] == "0.0.1"
        assert actual["releases"][0]["update"] is True
        assert actual["releases"][0]["breaking"] is False
        assert "error" not in actual["releases"][0]

    def test_build_output_error(self):
        test_project = "test_proj"
        fake_pypi_urlopen = build_fake_pypi_urlopen(status=200, body={"info": {}})
        test_dependency = build_fake_dependency(test_project, "0.0.0")

        with patch.object(request, "urlopen") as mock_urlopen:
            mock_urlopen.side_effect = fake_pypi_urlopen
            actual = build_output([test_dependency])

        assert actual["name"] == "Slack Bolt"
        assert len(actual["releases"]) == 1
        assert actual["releases"][0]["name"] == test_project
        assert "error" in actual["releases"][0]
        assert "message" in actual["releases"][0]["error"]
        assert "error" in actual
        assert "message" in actual["error"]
