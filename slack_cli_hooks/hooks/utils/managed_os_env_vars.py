import os
from typing import List
from slack_cli_hooks.protocol import Protocol


class ManagedOSEnvVars:
    def __init__(self, protocol: Protocol) -> None:
        self._protocol = protocol
        self._os_env_vars: List[str] = []

    def set_if_absent(self, os_env_var: str, value: str) -> None:
        if os_env_var in os.environ:
            self._protocol.info(f"{os_env_var} environment variable detected in session, using it over the provided one!")
            return
        self._os_env_vars.append(os_env_var)
        os.environ[os_env_var] = value

    def clear(self) -> None:
        for os_env_var in self._os_env_vars:
            os.environ.pop(os_env_var, None)
