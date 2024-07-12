from unittest.mock import Mock

from slack_cli_hooks.protocol.protocol import Protocol


def debug(self, msg: str, *args, **kwargs):
    """This is a mock"""
    pass


def info(self, msg: str, *args, **kwargs):
    """This is a mock"""
    pass


def warning(self, msg: str, *args, **kwargs):
    """This is a mock"""
    pass


def error(self, msg: str, *args, **kwargs):
    """This is a mock"""
    pass


def respond(self, data: str):
    """This is a mock"""
    pass


class MockProtocol(Protocol):
    name: str = "MockProtocol"

    debug = Mock(spec=debug, return_value=None)
    info = Mock(spec=info, return_value=None)
    warning = Mock(spec=warning, return_value=None)
    error = Mock(spec=error, return_value=None)
    respond = Mock(spec=respond, return_value=None)
