import os
import runpy
import sys
from unittest.mock import patch

import pytest

from slack_cli_hooks.error import CliError
from slack_cli_hooks.hooks import start
from tests.mock_socket_mode_server import start_socket_mode_server, stop_socket_mode_server
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestStart:
    working_directory = "tests/scenario_test/test_app"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        os.environ["SLACK_BOT_TOKEN"] = "xoxb-valid"
        os.environ["SLACK_APP_TOKEN"] = "xapp-A111-222-xyz"
        setup_mock_web_api_server(self)
        start_socket_mode_server(self, 3012)

        cli_args = [start.__file__, "--protocol", "message-boundaries", "--boundary", ""]
        self.argv_mock = patch.object(sys, "argv", cli_args)
        self.argv_mock.start()

        self.cwd = os.getcwd()

    def teardown_method(self):
        self.argv_mock.stop()
        os.chdir(self.cwd)
        os.environ.pop("SLACK_BOT_TOKEN", None)
        os.environ.pop("SLACK_APP_TOKEN", None)
        os.environ.pop("SLACK_APP_PATH", None)
        cleanup_mock_web_api_server(self)
        stop_socket_mode_server(self)
        restore_os_env(self.old_os_env)

    def test_start_script(self, capsys, caplog):
        os.chdir(self.working_directory)

        runpy.run_path(start.__file__, run_name="__main__")

        captured_sys = capsys.readouterr()

        assert "ran as __main__" in captured_sys.out
        assert "INFO A new session has been established" in caplog.text

    def test_start_with_entrypoint(self, capsys, caplog):
        os.environ["SLACK_APP_PATH"] = "my_app.py"
        os.chdir(self.working_directory)

        runpy.run_path(start.__file__, run_name="__main__")

        captured_sys = capsys.readouterr()

        assert "ran as __main__" in captured_sys.out
        assert "INFO A new session has been established" in caplog.text

    def test_start_no_entrypoint(self):
        working_directory = "tests/scenario_test/"
        os.chdir(working_directory)

        with pytest.raises(CliError) as e:
            runpy.run_path(start.__file__, run_name="__main__")

        assert "Could not find app.py file" in str(e.value)
