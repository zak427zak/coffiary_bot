import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert as mysql_insert

from infrastructure.database.models import Recipe
from infrastructure.database.repo.base import BaseRepo


class RecipeRepo(BaseRepo):

    def get_user_recipes(self, user_id: int, payload: dict):
        """
        Получение всех рецептов пользователя с фильтрацией по параметрам.
        :param user_id: ID пользователя
        :param payload: Дополнительные параметры фильтрации
        :return: Список рецептов
        """
        # Логируем входные параметры
        logging.info(f"Fetching recipes for user_id: {user_id} with payload: {payload}")

        # Начинаем с базового запроса по user_id
        query = self.session.query(Recipe).filter(Recipe.user_id == user_id)

        # Если isConcrete == "false", возвращаем все рецепты пользователя
        if payload.get('isConcrete') == "false":
            logging.info("isConcrete is false - fetching all recipes")
            return query.order_by(Recipe.add_date.desc()).all()

        # Если isConcrete == "true", применяем фильтры
        if payload.get('isConcrete') == "true":
            logging.info("isConcrete is true - applying filters")

            # Если передан конкретный id
            if payload.get('id') != "none":
                query = query.filter(Recipe.id == payload['id'])
                logging.info(f"Filtering by id: {payload['id']}")

            # Если переданы monthBlock и dayBlock
            elif 'monthBlock' in payload and 'dayBlock' in payload:
                month_block = payload['monthBlock']
                day_block = payload['dayBlock']
                logging.info(f"Filtering by monthBlock: {month_block} and dayBlock: {day_block}")
                query = query.filter(Recipe.month_block == month_block)
                query = query.filter(Recipe.day_block == day_block)

        # Сортируем рецепты по дате добавления и возвращаем список
        recipes = query.order_by(Recipe.add_date.desc()).all()
        logging.info(f"Found {len(recipes)} recipes after applying filters.")

        return recipes

    def to_collection_recipes(self, recipes_list, page, per_page, current_user):
        """
        Конвертирует результат запроса в список словарей.
        :param recipes_list: Список рецептов
        :param page: Номер страницы
        :param per_page: Количество элементов на странице
        :param current_user: Текущий пользователь
        :return: Список рецептов в формате словаря
        """
        # Реализация кастомной пагинации
        offset = (page - 1) * per_page
        resources = recipes_list[offset:offset + per_page]

        data = [item.to_dict(current_user) for item in resources]

        return data

    def add_recipe(self, user_id: int, data: dict, month_block: str, day_block: str, ):
        """
        Adds a new recipe to the database.
        :param user_id: The ID of the user who created the recipe.
        :param data: The data of the recipe.
        :param month_block: The month block information.
        :param day_block: The day block information.
        """
        # Создаем рецепт в базе данных с помощью метода create_or_update_recipe
        self.create_or_update_recipe(user_id=user_id, name=data['name'], photo_url=data.get('photoUrl'),
                                     water_volume=float(data['waterVolume']),
                                     water_temperature=float(data['waterTemperature']),
                                     amount_of_coffee=float(data['amountOfCoffee']), brew_time=int(data['brewTime']),
                                     grind_size=int(data['grindSize']), grade=int(data['grade']),
                                     coffee_type=data['coffeeType'], description=data['description'],
                                     add_date=datetime.utcnow() + timedelta(hours=3), month_block=month_block,
                                     day_block=day_block, )

    def get_recipes_grouped_by_month(self, user_id: int):
        """
        Returns recipes grouped by month for a specific user.
        :param user_id: The ID of the user.
        :return: List of tuples containing (month_block, count).
        """
        return (self.session.query(Recipe.month_block, func.count(Recipe.month_block)).filter(
            Recipe.user_id == user_id).group_by(Recipe.month_block).order_by(Recipe.add_date.desc()).all())

    def get_recipes_grouped_by_day(self, user_id: int, month_block: str):
        """
        Returns recipes grouped by day for a specific user and month.
        :param user_id: The ID of the user.
        :param month_block: The month block for filtering.
        :return: List of tuples containing (day_block, count).
        """
        return (self.session.query(Recipe.day_block, func.count(Recipe.day_block)).filter(Recipe.user_id == user_id,
                                                                                          Recipe.month_block == month_block).group_by(
            Recipe.day_block).order_by(Recipe.add_date.desc()).all())

    def get_recipes_by_user(self, user_id: int):
        """
        Returns all recipes for a specific user.
        :param user_id: The ID of the user.
        :return: List of Recipe objects.
        """
        return (self.session.query(Recipe).filter(Recipe.user_id == user_id).order_by(Recipe.add_date.desc()).all())

    def create_or_update_recipe(self, user_id: int, name: str, photo_url: Optional[str] = None,
                                water_volume: Optional[float] = None, water_temperature: Optional[float] = None,
                                amount_of_coffee: Optional[float] = None, brew_time: Optional[float] = None,
                                grind_size: Optional[int] = None, grade: Optional[int] = None,
                                coffee_type: Optional[str] = None, description: Optional[str] = None,
                                add_date: Optional[datetime] = None, month_block: Optional[str] = None,
                                day_block: Optional[str] = None, ):
        """
        Creates or updates a recipe in the database and returns the recipe object.
        :param user_id: The ID of the user who created the recipe.
        :param name: The name of the recipe.
        :param photo_url: The photo URL of the recipe. It's an optional parameter.
        :param water_volume: The volume of water used. It's an optional parameter.
        :param water_temperature: The temperature of water used. It's an optional parameter.
        :param amount_of_coffee: The amount of coffee used. It's an optional parameter.
        :param brew_time: The brewing time in seconds. It's an optional parameter.
        :param grind_size: The grind size used. It's an optional parameter.
        :param grade: The grade of the recipe. It's an optional parameter.
        :param coffee_type: The type of coffee used. It's an optional parameter.
        :param description: The description of the recipe. It's an optional parameter.
        :param add_date: The date the recipe was added. It's an optional parameter.
        :param month_block: The month block information. It's an optional parameter.
        :param day_block: The day block information. It's an optional parameter.
        :return: Recipe object, None if there was an error while making a transaction.
        """

        # Используем MySQL синтаксис для upsert
        insert_stmt = mysql_insert(Recipe).values(user_id=user_id, name=name, photo_url=photo_url,
                                                  water_volume=water_volume, water_temperature=water_temperature,
                                                  amount_of_coffee=amount_of_coffee, brew_time=brew_time,
                                                  grind_size=grind_size, grade=grade, coffee_type=coffee_type,
                                                  description=description, add_date=add_date, month_block=month_block,
                                                  day_block=day_block, )

        update_stmt = insert_stmt.on_duplicate_key_update(photo_url=insert_stmt.inserted.photo_url,
                                                          water_volume=insert_stmt.inserted.water_volume,
                                                          water_temperature=insert_stmt.inserted.water_temperature,
                                                          amount_of_coffee=insert_stmt.inserted.amount_of_coffee,
                                                          brew_time=insert_stmt.inserted.brew_time,
                                                          grind_size=insert_stmt.inserted.grind_size,
                                                          grade=insert_stmt.inserted.grade,
                                                          coffee_type=insert_stmt.inserted.coffee_type,
                                                          description=insert_stmt.inserted.description,
                                                          add_date=insert_stmt.inserted.add_date,
                                                          month_block=insert_stmt.inserted.month_block,
                                                          day_block=insert_stmt.inserted.day_block, )

        # Выполняем запрос и коммитим
        self.session.execute(update_stmt)
        self.session.commit()

        # Получаем рецепт из базы данных после вставки или обновления
        recipe = self.session.query(Recipe).filter(Recipe.user_id == user_id, Recipe.name == name).first()

        return recipe
