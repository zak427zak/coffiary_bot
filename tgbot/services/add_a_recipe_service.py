import logging

import requests


def add_a_recipe_service(message, recipe):
    url = "http://coffiary_api:8000/recipe"
    headers = {'Content-Type': 'application/json'}
    data = {"userId": message.from_user.id, "waterVolume": str(recipe.get('water_volume')),
            "waterTemperature": str(recipe.get('water_temperature')),
            "amountOfCoffee": str(recipe.get('amount_of_coffee')), "brewTime": str(recipe.get('brew_time')),
            "coffeeType": str(recipe.get('coffee_type')), "description": str(recipe.get('description')),
            "grindSize": str(recipe.get('grind_size')), "grade": str(recipe.get('grade')),
            "name": str(recipe.get('name')), "photoUrl": str(recipe.get('photo_url'))}

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()

        # Возвращаем респонс и статус код отдельно
        return r.json(), r.status_code
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - {r.text}")
        return {'errorMessage': str(http_err)}, r.status_code
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred: {err}")
        return {'errorMessage': str(err)}, 500
    except ValueError as json_err:
        logging.error(f"JSON decode error: {json_err} - Response content: {r.text}")
        return {'errorMessage': str(json_err)}, 500
