#!/usr/bin/env python
import json
import sys

from slack_cli_hooks.protocol import DefaultProtocol, MessageBoundaryProtocol, Protocol, build_protocol

PROTOCOL: Protocol

# Wrap sys.executable in quotes to prevent execution failures if a white space is present in the absolute python path
if sys.executable:
    EXEC = f"& '{sys.executable}'" if sys.platform == "win32" else f"'{sys.executable}'"
else:
    EXEC = "python"


hooks_payload = {
    "hooks": {
        "get-manifest": f"{EXEC} -m slack_cli_hooks.hooks.get_manifest",
        "start": f"{EXEC} -X dev -m slack_cli_hooks.hooks.start",
        "check-update": f"{EXEC} -m slack_cli_hooks.hooks.check_update",
        "doctor": f"{EXEC} -m slack_cli_hooks.hooks.doctor",
    },
    "config": {
        "protocol-version": [MessageBoundaryProtocol.name, DefaultProtocol.name],
        "sdk-managed-connection-enabled": True,
        "watch": {
            "app": {
                "filter-regex": "\\.py$",
                "paths": ["."],
            },
            "manifest": {
                "paths": ["manifest.json"],
            },
        },
    },
    "runtime": "python",
}

if __name__ == "__main__":
    PROTOCOL = build_protocol(argv=sys.argv)
    PROTOCOL.respond(json.dumps(hooks_payload))
