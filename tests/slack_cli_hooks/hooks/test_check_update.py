from unittest.mock import patch
from urllib import request

import pytest
from packaging.version import Version

from slack_cli_hooks.error import PypiError
from slack_cli_hooks.hooks import check_update
from slack_cli_hooks.hooks.check_update import (
    Release,
    build_output,
    build_release,
    extract_latest_version,
    pypi_get,
    pypi_get_json,
)
from tests.mock_protocol import MockProtocol
from tests.utils import build_fake_dependency, build_fake_pypi_urlopen


class TestRelease:
    test_project = "test_proj"

    def setup_method(self):
        check_update.PROTOCOL = MockProtocol()

    def test_release_with_same_version(self):
        release = Release(name=self.test_project, current=Version("0.0.0"), latest=Version("0.0.0"))
        assert release.current == release.latest
        assert release.breaking is False
        assert release.update is False

    def test_release_with_diff_version(self):
        release = Release(name=self.test_project, current=Version("0.0.0"), latest=Version("0.0.1"))
        assert release.current == "0.0.0"
        assert release.latest == "0.0.1"
        assert release.breaking is False
        assert release.update is True

    def test_release_with_dev(self):
        release = Release(name=self.test_project, current=Version("0.0.0"), latest=Version("0.0.0.dev0"))
        assert release.current == "0.0.0"
        assert release.latest == "0.0.0.dev0"
        assert release.breaking is False
        assert release.update is False

    def test_release_with_downgrades(self):
        release = Release(name=self.test_project, current=Version("1.0.0"), latest=Version("0.0.0"))
        assert release.breaking is False
        assert release.update is False

    def test_release_with_major_upgrade(self):
        release = Release(name=self.test_project, current=Version("0.0.0"), latest=Version("1.0.0"))
        assert release.breaking is True
        assert release.update is True


class TestCheckUpdate:
    def setup_method(self):
        check_update.PROTOCOL = MockProtocol()

    def test_pypi_get(self):
        test_project = "test_proj"
        fake_pypi_urlopen = build_fake_pypi_urlopen()

        with patch.object(request, "urlopen") as mock_urlopen:
            mock_urlopen.side_effect = fake_pypi_urlopen
            response = pypi_get(test_project)

        assert response.url == f"https://pypi.org/pypi/{test_project}/json"
        assert response.status == 200
        assert response.read().decode("utf-8") == "{}"

    def test_pypi_get_json(self):
        project = "my_test_project"
        fake_pypi_urlopen = build_fake_pypi_urlopen(body={"info": {}, "releases": {}})

        with patch.object(request, "urlopen") as mock_urlopen:
            mock_urlopen.side_effect = fake_pypi_urlopen
            json_response = pypi_get_json(project)

        assert json_response == {"info": {}, "releases": {}}

    def test_pypi_get_json_fail(self):
        project = "my_test_project"
        fake_pypi_urlopen = build_fake_pypi_urlopen(status=300)

        with patch.object(request, "urlopen") as mock_urlopen:
            mock_urlopen.side_effect = fake_pypi_urlopen
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
        test_project = "test-dependency"
        test_dependency = build_fake_dependency(test_project, "0.0.0")

        with patch.object(check_update, pypi_get_json.__name__) as mock_pypi_get_json:
            mock_pypi_get_json.return_value = {"info": {"version": "0.0.1"}}
            actual = build_release(test_dependency)

        assert vars(actual) == {
            "name": test_project,
            "current": "0.0.0",
            "latest": "0.0.1",
            "update": True,
            "breaking": False,
        }

    def test_build_release_error(self):
        test_project = "test-dependency"
        test_dependency = build_fake_dependency(test_project, "0.0.0")

        with patch.object(check_update, pypi_get_json.__name__) as mock_pypi_get_json:
            mock_pypi_get_json.return_value = {}
            actual = build_release(test_dependency)

        assert vars(actual) == {
            "name": test_project,
            "error": {"message": "Missing `info` field in pypi payload"},
        }

    def test_build_output(self):
        actual = build_output([])

        assert actual == {
            "name": "Slack Bolt",
            "url": "https://api.slack.com/automation/changelog",
            "releases": [],
        }
