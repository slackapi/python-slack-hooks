import argparse
from typing import List

from .default_protocol import DefaultProtocol
from .message_boundary_protocol import MessageBoundaryProtocol
from .protocol import Protocol

__all__ = ["DefaultProtocol", "MessageBoundaryProtocol", "Protocol"]


def build_protocol(argv: List[str]) -> Protocol:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=str, required=False)
    parser.add_argument("--boundary", type=str, required=False)

    args, unknown = parser.parse_known_args(args=argv[1:])

    if args.protocol == MessageBoundaryProtocol.name:
        return MessageBoundaryProtocol(boundary=args.boundary)
    return DefaultProtocol()
