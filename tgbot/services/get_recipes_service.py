import logging

import requests


def get_recipes_service(message, is_concrete, data):
    url = "http://coffiary_api:8000/recipes"
    headers = {
        'Content-Type': 'application/json'
    }
    # Добавьте необходимые данные для конкретного запроса
    if is_concrete == "true":
        data = {
            "userId": message.from_user.id,
            "isConcrete": is_concrete,
            "monthBlock": data.get("parent"),
            "dayBlock": data.get("link"),
            "id": data.get("id")
        }
    else:
        data = {"userId": message.from_user.id, "isConcrete": is_concrete}

    logging.info(f"data data: {data}")

    # Преобразуйте data в JSON перед отправкой
    r = requests.post(url, headers=headers, json=data)
    return r.json()

