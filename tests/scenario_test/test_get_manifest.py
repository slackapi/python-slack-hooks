import json
import os
import runpy
import sys
from unittest.mock import patch

import pytest

from slack_cli_hooks.error import CliError
from slack_cli_hooks.hooks import get_manifest


class TestGetManifest:

    def setup_method(self):
        cli_args = [get_manifest.__file__, "--protocol", "message-boundaries", "--boundary", ""]
        self.argv_mock = patch.object(sys, "argv", cli_args)
        self.argv_mock.start()
        self.cwd = os.getcwd()

    def teardown_method(self):
        os.chdir(self.cwd)
        self.argv_mock.stop()

    def test_get_manifest_script(self, capsys):
        working_directory = "tests/scenario_test/test_app"
        os.chdir(working_directory)

        runpy.run_path(get_manifest.__file__, run_name="__main__")

        out, err = capsys.readouterr()
        assert err == ""
        assert {"_metadata": {}, "display_information": {"name": "Bolt app"}} == json.loads(out)

    def test_get_manifest_script_no_manifest(self):
        working_directory = "tests/scenario_test/test_app_no_manifest"
        os.chdir(working_directory)

        with pytest.raises(CliError) as e:
            runpy.run_path(get_manifest.__file__, run_name="__main__")

        assert str(e.value) == "Could not find a manifest.json file"
