import requests


def get_recipes_months_service(user_id, keyboard_type):
    url = "http://coffiary_api:8000/recipes/catalog"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {"userId": user_id, "keyboardType": keyboard_type}

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {r.text}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err} - Response content: {r.text}")


    return []
