#!/usr/bin/env python
import json
import platform
import sys

from slack_cli_hooks.protocol import Protocol, build_protocol

PROTOCOL: Protocol


doctor_payload = {
    "versions": [
        {
            "name": "python",
            "current": platform.python_version(),
        },
        {
            "name": "implementation",
            "current": platform.python_implementation(),
        },
        {
            "name": "compiler",
            "current": platform.python_compiler(),
        },
    ],
}

if __name__ == "__main__":
    PROTOCOL = build_protocol(argv=sys.argv)
    PROTOCOL.respond(json.dumps(doctor_payload))
