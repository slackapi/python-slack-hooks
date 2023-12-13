from slack_cli_hooks.protocol import build_protocol, DefaultProtocol, MessageBoundaryProtocol, Protocol


class TestProtocolFactory:
    def test_default(self):
        args = []
        protocol = build_protocol(args)
        assert isinstance(protocol, Protocol)
        assert isinstance(protocol, DefaultProtocol)

    def test_message_boundaries(self):
        args = [f"--protocol={MessageBoundaryProtocol.name}", "--bound=boundary"]
        protocol = build_protocol(args)
        assert isinstance(protocol, Protocol)
        assert isinstance(protocol, MessageBoundaryProtocol)
