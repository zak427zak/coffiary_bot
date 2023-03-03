import requests

from tgbot.config import load_config


def register_new_user(message):
    config = load_config(".env")
    url = f"https://services.llqq.ru/coffiary/user/register"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": message.from_user.id, "firstName": str(message.from_user.first_name),
            "lastName": str(message.from_user.last_name), "username": str(message.from_user.username)}
    r = requests.post(url, headers=headers, data=data)
    print(r.text)
