from slack_cli_hooks.protocol import MessageBoundaryProtocol, Protocol, build_protocol
from slack_cli_hooks.protocol.default_protocol import DefaultProtocol


class TestProtocolFactory:
    def test_default(self):
        args = []
        protocol = build_protocol(argv=args)
        assert isinstance(protocol, Protocol)
        assert isinstance(protocol, DefaultProtocol)

    def test_message_boundaries(self):
        args = [f"--protocol={MessageBoundaryProtocol.name}", "--bound=boundary"]
        protocol = build_protocol(argv=args)
        assert isinstance(protocol, Protocol)
        assert isinstance(protocol, MessageBoundaryProtocol)
