import logging

import requests


def register_new_user(message):
    url = "http://coffiary_api:8000/user/register"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "telegram_id": message.from_user.id,
        "first_name": str(message.from_user.first_name),
        "last_name": str(message.from_user.last_name),
        "username": str(message.from_user.username)
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        logging.info(f"Response from registration API: {r.status_code} - {r.text}")
    except Exception as e:
        logging.error(f"Failed to register user: {e}")
