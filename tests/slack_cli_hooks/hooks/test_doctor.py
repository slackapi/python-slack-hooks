import platform

from slack_cli_hooks.hooks.doctor import doctor_payload


class TestDoctor:
    def test_versions(self):
        versions = doctor_payload.get("versions")
        assert versions is not None

        assert versions[0].get("name") == "python"
        assert versions[0].get("current") == platform.python_version()
        assert versions[1].get("name") == "implementation"
        assert versions[1].get("current") == platform.python_implementation()
        assert versions[2].get("name") == "compiler"
        assert versions[2].get("current") == platform.python_compiler()
