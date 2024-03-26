import platform

from slack_cli_hooks.hooks.doctor import doctor_payload


class TestDoctor:
    def test_versions(self):
        versions = doctor_payload.get("versions")
        assert versions is not None

        assert versions[0].get("name") is "python"
        assert versions[0].get("current") is platform.python_build()[0]
        assert versions[1].get("name") is "implementation"
        assert versions[1].get("current") is platform.python_implementation()
        assert versions[2].get("name") is "compiler"
        assert versions[2].get("current") is platform.python_compiler()
