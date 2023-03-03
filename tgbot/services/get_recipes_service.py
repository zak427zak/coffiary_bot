import requests

from tgbot.config import load_config


def get_recipes_service(message):
    config = load_config(".env")
    url = f"https://services.llqq.ru/coffiary/recipes"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": message.from_user.id}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result'], r.status_code
    else:
        return r.json()['errorMessage'], r.status_code

