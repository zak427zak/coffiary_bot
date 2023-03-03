from aiogram.dispatcher.filters.state import StatesGroup, State


class Recipe(StatesGroup):
    water_volume = State()
    water_temperature = State()
    amount_of_coffee = State()
    coffee_type = State()
    brew_time = State()
    description = State()
    name = State()
    photo_url = State()
