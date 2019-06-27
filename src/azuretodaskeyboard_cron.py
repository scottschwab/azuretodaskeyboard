import logging
import requests
import json


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

SOURCE_URL = "http://localhost:7071/api/az2keyboard"

BACKEND_URL = "http://localhost:27301"
API = "/api/1.0/signals"
HEADERS = {"Content-type": "application/json"}
PID = "DK5QPID"


def send_signal(display_info, message):
    signal = dict()
    signal['name'] = f"Message from: {display_info['user_name']}"
    signal['message'] = message
    signal['zoneId'] = f"KEY_{display_info['key']}"
    signal['color'] = display_info['color']
    signal['effect'] = display_info['effect']
    signal['pid'] = PID
    signal['clientName'] = "tron01"

    signal_json = json.dumps(signal)

    res_signal = requests.post(f"{BACKEND_URL}{API}", data = signal_json, headers = HEADERS)


def driver():
    logger.info(f"loading from {SOURCE_URL}")
    response = requests.get(SOURCE_URL)
    request_body_str = response.content.decode("utf-8")
    request_body = json.loads(request_body_str)

    logger.info(f"found {len(request_body['messages'])} messages")
    users = dict()
    for message in request_body['messages']:
        user = message['user_name']
        if user not in users:
            users[user] = list()
        users[user].append(message)
    
    logger.info(f"have {len(users)} unique users")

    for user in users.keys():
        message_out = ""
        logger.info(f"{user} has {len(users[user])}")
        for message in users[user]:
            message_out = f"{message_out} | {message['text']}"
        logger.info(len(message_out))
        send_signal(users[user][0], message_out[0:256])


if __name__ == '__main__':
    driver()
