#!/usr/bin/env python
import json
from slack_cli_hooks.protocol import Protocol, MessageBoundaryProtocol, DefaultProtocol, build_protocol

PROTOCOL: Protocol
EXEC = "python3"


hooks_payload = {
    "hooks": {
        "get-manifest": f"{EXEC} -m slack_cli_hooks.hooks.get_manifest",
        "start": f"{EXEC} -X dev -m slack_cli_hooks.hooks.start",
    },
    "config": {
        "watch": {"filter-regex": "(^manifest\\.json$)", "paths": ["."]},
        "protocol-version": [MessageBoundaryProtocol.name, DefaultProtocol.name],
        "sdk-managed-connection-enabled": True,
    },
}

if __name__ == "__main__":
    PROTOCOL = build_protocol()
    PROTOCOL.respond(json.dumps(hooks_payload))
