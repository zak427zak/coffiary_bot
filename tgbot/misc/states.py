from aiogram.dispatcher.filters.state import StatesGroup, State


class Recipe(StatesGroup):
    water_volume = State()
    water_temperature = State()
    amount_of_coffee = State()
    name = State()
    photo_url = State()
