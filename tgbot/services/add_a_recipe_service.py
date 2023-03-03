import requests

from tgbot.config import load_config


def add_a_recipe_service(message, recipe):
    config = load_config(".env")
    url = f"https://services.llqq.ru/coffiary/recipe"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": message.from_user.id, "waterVolume": str(recipe.get('water_volume')),
            "waterTemperature": str(recipe.get('water_temperature')),
            "amountOfCoffee": str(recipe.get('amount_of_coffee')),
            "brewTime": str(recipe.get('brew_time')),
            "coffeeType": str(recipe.get('coffee_type')),
            "description": str(recipe.get('description')),
            "name": str(recipe.get('name')), "photoUrl": str(recipe.get('photo_url'))}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result'], r.status_code
    else:
        return r.json()['errorMessage'], r.status_code
