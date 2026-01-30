from slack_cli_hooks.hooks.get_hooks import hooks_payload


class TestGetHooks:
    def test_hooks_payload(self):
        hooks = hooks_payload["hooks"]

        assert "slack_cli_hooks.hooks.get_manifest" in hooks["get-manifest"]
        assert "slack_cli_hooks.hooks.start" in hooks["start"]
        assert "slack_cli_hooks.hooks.check_update" in hooks["check-update"]
        assert "slack_cli_hooks.hooks.doctor" in hooks["doctor"]

    def test_hooks_payload_config(self):
        config = hooks_payload["config"]

        assert config["sdk-managed-connection-enabled"] is True
        assert config["protocol-version"] == ["message-boundaries", "default"]

    def test_hooks_watch_app(self):
        config = hooks_payload["config"]
        assert config["watch"] is not None
        assert config["watch"]["app"] is not None
        assert config["watch"]["app"]["filter-regex"] == "\\.py$"
        assert config["watch"]["app"]["paths"] == ["."]

    def test_hooks_watch_manifest(self):
        config = hooks_payload["config"]
        assert config["watch"] is not None
        assert config["watch"]["manifest"] is not None
        assert config["watch"]["manifest"]["paths"] == ["manifest.json"]

    def test_hooks_runtime(self):
        runtime = hooks_payload["runtime"]

        assert runtime == "python"
