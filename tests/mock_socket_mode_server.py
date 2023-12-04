import json
import logging
import threading
import time
from urllib.request import urlopen
from urllib.error import URLError
from typing import List
from unittest import TestCase
from flask import Flask
from flask_sockets import Sockets

socket_mode_envelopes = json.dumps(
    [
        {
            "envelope_id": "57d6a792-4d35-4d0b-b6aa-3361493e1caf",
            "payload": {
                "type": "shortcut",
                "token": "xxx",
                "action_ts": "1610198080.300836",
                "team": {"id": "T111", "domain": "seratch"},
                "user": {"id": "U111", "username": "seratch", "team_id": "T111"},
                "is_enterprise_install": False,
                "enterprise": None,
                "callback_id": "do-something",
                "trigger_id": "111.222.xxx",
            },
            "type": "interactive",
            "accepts_response_payload": False,
        },
        {
            "envelope_id": "1d3c79ab-0ffb-41f3-a080-d19e85f53649",
            "payload": {
                "token": "xxx",
                "team_id": "T111",
                "team_domain": "xxx",
                "channel_id": "C111",
                "channel_name": "random",
                "user_id": "U111",
                "user_name": "seratch",
                "command": "/hello-socket-mode",
                "text": "",
                "api_app_id": "A111",
                "response_url": "https://hooks.slack.com/commands/T111/111/xxx",
                "trigger_id": "111.222.xxx",
            },
            "type": "slash_commands",
            "accepts_response_payload": True,
        },
        {
            "envelope_id": "08cfc559-d933-402e-a5c1-79e135afaae4",
            "payload": {
                "token": "xxx",
                "team_id": "T111",
                "api_app_id": "A111",
                "event": {
                    "client_msg_id": "c9b466b5-845c-49c6-a371-57ae44359bf1",
                    "type": "message",
                    "text": "<@W111>",
                    "user": "U111",
                    "ts": "1610197986.000300",
                    "team": "T111",
                    "blocks": [
                        {
                            "type": "rich_text",
                            "block_id": "1HBPc",
                            "elements": [{"type": "rich_text_section", "elements": [{"type": "user", "user_id": "U111"}]}],
                        }
                    ],
                    "channel": "C111",
                    "event_ts": "1610197986.000300",
                    "channel_type": "channel",
                },
                "type": "event_callback",
                "event_id": "Ev111",
                "event_time": 1610197986,
                "authorizations": [
                    {
                        "enterprise_id": None,
                        "team_id": "T111",
                        "user_id": "U111",
                        "is_bot": True,
                        "is_enterprise_install": False,
                    }
                ],
                "is_ext_shared_channel": False,
                "event_context": "1-message-T111-C111",
            },
            "type": "events_api",
            "accepts_response_payload": False,
            "retry_attempt": 1,
            "retry_reason": "timeout",
        },
    ]
)


def start_thread_socket_mode_server(test: TestCase, port: int):
    def _start_thread_socket_mode_server():
        logger = logging.getLogger(__name__)
        app: Flask = Flask(__name__)

        @app.route("/state")
        def state():
            return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

        sockets: Sockets = Sockets(app)

        envelopes_to_consume: List[str] = list(socket_mode_envelopes)

        @sockets.route("/link")
        def link(ws):
            while not ws.closed:
                message = ws.read_message()
                if message is not None:
                    if len(envelopes_to_consume) > 0:
                        e = envelopes_to_consume.pop(0)
                        logger.debug(f"Send an envelope: {e}")
                        ws.send(e)

                    logger.debug(f"Server received a message: {message}")
                    ws.send(message)

        from gevent import pywsgi
        from geventwebsocket.handler import WebSocketHandler

        server = pywsgi.WSGIServer(("", port), app, handler_class=WebSocketHandler)
        test.server = server
        server.serve_forever(stop_timeout=1)

    return _start_thread_socket_mode_server


def start_socket_mode_server(test, port: int):
    test.sm_thread = threading.Thread(target=start_thread_socket_mode_server(test, port))
    test.sm_thread.daemon = True
    test.sm_thread.start()
    wait_for_socket_mode_server(port, 4)  # wait for the server


def wait_for_socket_mode_server(port: int, secs: int):
    start_time = time.time()
    while (time.time() - start_time) < secs:
        try:
            urlopen(f"http://localhost:{port}/state")
            break
        except URLError:
            pass


def stop_socket_mode_server(test):
    print(test)
    test.server.stop()
    test.server.close()


async def stop_socket_mode_server_async(test: TestCase):
    test.server.stop()
    test.server.close()