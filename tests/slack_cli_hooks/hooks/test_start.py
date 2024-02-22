import os

from slack_cli_hooks.hooks.start import get_main_file, get_main_path
from tests.utils import remove_os_env_temporarily, restore_os_env

SLACK_APP_PATH = "SLACK_APP_PATH"


class TestStart:
    working_directory = "tests/slack_bolt/cli/test_app"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        os.environ.pop(SLACK_APP_PATH, None)
        restore_os_env(self.old_os_env)

    def test_get_main_file(self):
        assert get_main_file() == "app.py"

    def test_get_main_file_with_override(self):
        os.environ[SLACK_APP_PATH] = "my_app.py"
        assert get_main_file() == "my_app.py"

    def test_get_main_path(self):
        assert get_main_path("/dir") == "/dir/app.py"

    def test_get_main_path_from_var(self):
        os.environ[SLACK_APP_PATH] = "my_app.py"
        assert get_main_path("/dir") == "/dir/my_app.py"
