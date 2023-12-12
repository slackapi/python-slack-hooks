import os
from slack_cli_hooks.hooks.utils import ManagedOSEnvVars
from slack_cli_hooks.protocol import DefaultProtocol
from tests.utils import remove_os_env_temporarily, restore_os_env

TEST_VAR = "TEST"
TEST_VAR2 = "TEST2"


class TestEnvVarHandler:
    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        os.environ.pop(TEST_VAR, None)
        os.environ.pop(TEST_VAR2, None)
        restore_os_env(self.old_os_env)

    def test_set_if_absent(self):
        expected = "expected test value"
        os_env_vars = ManagedOSEnvVars(DefaultProtocol())
        os_env_vars.set_if_absent(TEST_VAR, expected)

        assert TEST_VAR in os.environ
        assert os.environ[TEST_VAR] == expected

    def test_set_default_does_not_overwrite(self):
        expected = "default test value"
        os.environ[TEST_VAR] = expected

        os_env_vars = ManagedOSEnvVars(DefaultProtocol())
        os_env_vars.set_if_absent(TEST_VAR, "nothing")

        assert TEST_VAR in os.environ
        assert os.environ[TEST_VAR] == expected

    def test_clear(self):
        expected = "expected test value"
        os_env_vars = ManagedOSEnvVars(DefaultProtocol())
        os_env_vars.set_if_absent(TEST_VAR, expected)

        os_env_vars.clear()

        assert not (TEST_VAR in os.environ)

    def test_clear_does_not_overwrite(self):
        expected = "expected test value"
        os.environ[TEST_VAR] = expected

        os_env_vars = ManagedOSEnvVars(DefaultProtocol())
        os_env_vars.set_if_absent(TEST_VAR, "nothing")

        os_env_vars.clear()

        assert TEST_VAR in os.environ
        assert os.environ[TEST_VAR] == expected

    def test_clear_only_clears_absent_vars(self):
        expected = "expected test value"
        os.environ[TEST_VAR] = expected

        os_env_vars = ManagedOSEnvVars(DefaultProtocol())
        os_env_vars.set_if_absent(TEST_VAR, "nothing")
        os_env_vars.set_if_absent(TEST_VAR2, expected)

        os_env_vars.clear()

        assert TEST_VAR in os.environ
        assert os.environ[TEST_VAR] == expected
        assert not (TEST_VAR2 in os.environ)

    def test_no_env_var_set(self):
        os_env_vars = ManagedOSEnvVars(DefaultProtocol())

        os_env_vars.clear()
        assert TEST_VAR not in os.environ
