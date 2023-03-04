import requests

from tgbot.config import load_config


def get_recipes_service(message, is_concrete, data):
    config = load_config(".env")
    url = f"https://services.llqq.ru/coffiary/recipes"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    if is_concrete == "true":
        data = {"userId": message.from_user.id, "isConcrete": is_concrete, "monthBlock": data.get("parent"),
                "dayBlock": data.get("link"), "id": data.get("id")}
    else:
        data = {"userId": message.from_user.id, "isConcrete": is_concrete}
    r = requests.post(url, headers=headers, data=data)
    return r.json()