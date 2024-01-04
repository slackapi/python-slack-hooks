import re
from slack_cli_hooks.hooks.get_hooks import hooks_payload


class TestGetHooks:
    def test_hooks_payload(self):
        hooks = hooks_payload["hooks"]

        assert "slack_cli_hooks.hooks.get_manifest" in hooks["get-manifest"]
        assert "slack_cli_hooks.hooks.start" in hooks["start"]
        assert "slack_cli_hooks.hooks.check_update" in hooks["check-update"]

    def test_hooks_payload_config(self):
        config = hooks_payload["config"]

        assert config["sdk-managed-connection-enabled"] is True
        assert config["protocol-version"] == ["message-boundaries", "default"]

    def test_hooks_watch_regex(self):
        config = hooks_payload["config"]

        assert config["watch"] is not None

        filter_regex = config["watch"]["filter-regex"]
        assert re.match(filter_regex, "manifest.json") is not None
