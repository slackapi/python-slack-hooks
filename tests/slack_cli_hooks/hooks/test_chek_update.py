from http.client import HTTPMessage
from unittest import mock

from slack_cli_hooks.hooks.check_update import get_pypi_response


class TestGetManifest:
    def test_find_file_path(self):
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
