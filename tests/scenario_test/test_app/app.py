import os

from slack_sdk import WebClient
from slack_bolt.app import App
from utils import get_test_socket_mode_handler, wait_for_test_socket_connection

web_client = WebClient(base_url="http://localhost:8888", token=os.environ.get("SLACK_BOT_TOKEN"))

app = App(signing_secret="valid", client=web_client)

result = {"shortcut": False}


@app.shortcut("do-something")
def shortcut_handler(ack):
    result["shortcut"] = True
    ack()


if __name__ == "__main__":
    print("ran as __main__")
    handler = get_test_socket_mode_handler(3012, app, os.environ.get("SLACK_APP_TOKEN"))
    handler.connect()
    wait_for_test_socket_connection(handler, 2)
