import json
import threading
import time
from urllib.request import urlopen
from urllib.error import URLError
from unittest import TestCase
from flask import Flask
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


def start_thread_socket_mode_server(test: TestCase, port: int):
    def _start_thread_socket_mode_server():
        app: Flask = Flask(__name__)

        @app.route("/state")
        def state():
            return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

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
