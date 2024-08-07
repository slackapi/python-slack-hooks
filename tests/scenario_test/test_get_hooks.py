import json
import runpy
import sys
from unittest.mock import patch

from slack_cli_hooks.hooks import get_hooks, get_manifest, start


class TestGetHooks:

    def setup_method(self):
        cli_args = [get_hooks.__file__, "--protocol", "message-boundaries", "--boundary", ""]
        self.argv_mock = patch.object(sys, "argv", cli_args)
        self.argv_mock.start()

    def teardown_method(self):
        self.argv_mock.stop()

    def test_get_manifest(self, capsys):
        runpy.run_path(get_hooks.__file__, run_name="__main__")

        out, err = capsys.readouterr()
        json_response = json.loads(out)
        assert err == ""
        assert "hooks" in json_response
        assert get_manifest.__name__ in json_response["hooks"]["get-manifest"]

    def test_start(self, capsys):
        runpy.run_path(get_hooks.__file__, run_name="__main__")

        out, err = capsys.readouterr()
        json_response = json.loads(out)
        assert err == ""
        assert "hooks" in json_response
        assert start.__name__ in json_response["hooks"]["start"]
