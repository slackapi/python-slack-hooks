from slack_cli_hooks.protocol import build_protocol, MessageBoundaryProtocol, Protocol


class TestProtocolFactory:
    def test_default(self):
        args = []
        try:
            build_protocol(args)
            assert False, "Expected an exception to be thrown"
        except Exception as e:
            assert isinstance(e, NotImplementedError)

    def test_message_boundaries(self):
        args = [f"--protocol={MessageBoundaryProtocol.name}", "--bound=boundary"]
        protocol = build_protocol(args)
        assert isinstance(protocol, Protocol)
        assert isinstance(protocol, MessageBoundaryProtocol)
