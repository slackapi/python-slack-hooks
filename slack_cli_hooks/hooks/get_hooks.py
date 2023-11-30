#!/usr/bin/env python
import json
from slack_cli_hooks.protocol import Protocol, MessageBoundaryProtocol, DefaultProtocol, protocol_factory
from slack_cli_hooks.hooks import get_manifest, start

PROTOCOL: Protocol
EXEC = "python3"

hooks_payload = {
    "hooks": {
        "get-manifest": f"{EXEC} -m {get_manifest.__name__}",
        "start": f"{EXEC} -m {start.__name__}",
    },
    "config": {
        "watcher": {"filter-regex": "^manifest\\.(json)$", "paths": ["."]},
        "protocol-version": [MessageBoundaryProtocol.name, DefaultProtocol.name],
        "sdk-managed-connection-enabled": True,
    },
}

if __name__ == "__main__":
    PROTOCOL = protocol_factory()
    PROTOCOL.respond(json.dumps(hooks_payload))
