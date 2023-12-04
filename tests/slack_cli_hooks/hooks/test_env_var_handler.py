import os
from slack_cli_hooks.hooks.start import EnvVarHandler
from tests.utils import remove_os_env_temporarily, restore_os_env

TEST_VAR = "TEST"


class TestEnvVarHandler:
    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        os.environ.pop(TEST_VAR, None)
        restore_os_env(self.old_os_env)

    def test_set_default(self):
        expected = "expected test value"
        test_var = EnvVarHandler(TEST_VAR)

        test_var.set_default(expected)

        assert test_var.name in os.environ
        assert os.environ[test_var.name] == expected

    def test_set_default_does_not_overwrite(self):
        expected = "default test value"
        os.environ[TEST_VAR] = expected

        test_var = EnvVarHandler(TEST_VAR)
        test_var.set_default("nothing")

        assert test_var.name in os.environ
        assert os.environ[test_var.name] == expected

    def test_clean(self):
        expected = "expected test value"
        test_var = EnvVarHandler(TEST_VAR)

        test_var.set_default(expected)
        test_var.clean()

        assert not (test_var.name in os.environ)

    def test_clean_does_not_overwrite(self):
        expected = "expected test value"
        os.environ[TEST_VAR] = expected

        test_var = EnvVarHandler(TEST_VAR)
        test_var.clean()

        assert test_var.name in os.environ
        assert os.environ[test_var.name] == expected
