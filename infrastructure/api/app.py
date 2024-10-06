import locale
import logging
import os
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from werkzeug.http import HTTP_STATUS_CODES

from infrastructure.database.models.base import db
from infrastructure.database.repo.recipes import RecipeRepo
from infrastructure.database.repo.users import UserRepo

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат вывода
                    handlers=[logging.StreamHandler()])  # Вывод логов в консоль

# Настройка базы данных из переменных окружения
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'mysql+pymysql://coffiary_adm:ujHoHGj5Zel4reP273dJAg@mysql:3306/coffiary')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем базу данных с приложением
db.init_app(app)

# Создание экземпляров репозиториев
user_repo = UserRepo(db.session)
recipe_repo = RecipeRepo(db.session)


def bad_request(message):
    return error_response(400, message)


def not_found(message):
    return error_response(404, message)


def error_response(status_code, message=None):
    payload = {'errorStatus': HTTP_STATUS_CODES.get(status_code, 'Unknown error'), 'errorCode': "1",
               'errorMessage': str(message), }
    response = jsonify(payload)
    response.status_code = status_code
    return response


@app.route('/recipes/catalog', methods=['POST'])
def coffiary_recipes_month_block():
    data = request.get_json() or request.form
    current_user = user_repo.get_by_telegram_id(data.get('userId'))
    if not current_user:
        return not_found('Не можем найти вас в системе. Напишите что-нибудь боту, чтобы он авторизовал вас')

    record_a_visit(current_user)

    vars_list = []
    if data['keyboardType'] == "clear":
        period = "months"
        data_periods = recipe_repo.get_recipes_grouped_by_month(current_user.id)

        for item in data_periods:
            di = {'id': 'none', 'block': f'{item[0]} ({item[1]} рец)', 'link': item[0], 'parent': data['keyboardType'],
                  'period': period, }
            vars_list.append(di)

        return jsonify(vars_list)

    elif data['keyboardType'] == "concrete":
        data_periods = recipe_repo.get_recipes_by_user(current_user.id)

        for item in data_periods:
            di = {'id': str(item.id), 'block': item.name, 'link': item.day_block, 'parent': item.month_block,
                  'period': "all", }
            vars_list.append(di)

        return jsonify(vars_list)

    else:
        period = "days"
        data_periods = recipe_repo.get_recipes_grouped_by_day(current_user.id, data['keyboardType'])

        for item in data_periods:
            di = {'id': 'none', 'block': f'{item[0]} ({item[1]} рец)', 'link': item[0], 'parent': data['keyboardType'],
                  'period': period, }
            vars_list.append(di)

        return jsonify(vars_list)


@app.route('/user/register', methods=['POST'])
def coffiary_register_new_user():
    payload = request.get_json() or request.form
    # logging.info(f"Received registration payload: {payload}")

    try:
        user = user_repo.get_or_create_user(**payload)
        # logging.info(f"User registered or updated: {user}")
        return 'ok'
    except Exception as e:
        logging.error(f"Error in user registration: {e}")
        return 'error', 500


@app.route('/recipe', methods=['POST'])
def coffiary_add_new_recipe():
    payload = request.get_json() or request.form

    # logging.info(f"Received payload: {payload}")

    check_user = user_repo.get_by_telegram_id(payload['userId'])
    if check_user:
        record_a_visit(check_user)
        add_new_recipe(check_user, payload)
        return jsonify({
            'result': "Рецепт успешно добавлен\n\nВы можете увидеть все добавленные вами рецепты командой /ungrouped\n\nПолучить рецепты, каталогизированные по датам - командой /grouped"})
    else:
        return not_found('Не можем найти вас в системе. Напишите что-нибудь боту, чтобы он авторизовал вас')


@app.route('/recipes', methods=['POST'])
def coffiary_recipes():
    print('4444')

    payload = request.get_json() or request.form
    # logging.info(f"Received payload: {payload}")

    current_user = user_repo.get_by_telegram_id(payload['userId'])
    if current_user:
        # logging.info(f"User found: {current_user}")
        record_a_visit(current_user)

        # Получаем рецепты пользователя с учетом фильтров
        recipes = recipe_repo.get_user_recipes(current_user.id, payload)
        # logging.info(f"Retrieved recipes: {recipes}")

        # Если рецепты найдены
        if recipes:
            # Преобразуем их в необходимый формат
            data = recipe_repo.to_collection_reciklomats(recipes, 1, 999, current_user)
            # logging.info(f"Transformed data: {data}")
            return jsonify(data)

        else:
            logging.warning("No recipes found for the user")
            return not_found("У вас пока нет рецептов. Сначала добавьте их - воспользуйтесь командой /add")
    else:
        logging.warning(f"User not found with telegram_id: {payload['userId']}")
        return not_found("Пользователя не существует! Попробуйте ещё раз, или вернитесь позже!")


def add_new_recipe(user, data):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    current = datetime.utcnow() + timedelta(hours=3)
    month_block = current.strftime("%b %Y")
    day_block = current.strftime("%d %a")
    recipe_repo.add_recipe(user.id, data, month_block, day_block)


def record_a_visit(user):
    user_repo.update_last_seen(user.id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
