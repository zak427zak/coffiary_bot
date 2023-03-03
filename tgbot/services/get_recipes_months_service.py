import requests

from tgbot.config import load_config


def get_recipes_months_service(user_id, keyboard_type):
    config = load_config(".env")
    url = f"https://services.llqq.ru/coffiary/recipes/catalog"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": user_id, "keyboardType": keyboard_type}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()
    else:
        return r.json()
