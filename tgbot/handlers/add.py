from datetime import datetime, timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import Recipe
from tgbot.services.add_a_recipe_service import add_a_recipe_service


async def set_water(message: Message):
    await message.answer(
        "Введи объем воды:")
    await Recipe.water_volume.set()


async def set_coffee(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(water_volume=answer)
    await message.answer("Введи количество кофе:")
    await Recipe.amount_of_coffee.set()


async def set_water_temperature(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(amount_of_coffee=answer)
    await message.answer("Введи температуру воды:")
    await Recipe.water_temperature.set()


async def set_brew_time(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(water_temperature=answer)
    await message.answer("Введи общее время заваривания:")
    await Recipe.brew_time.set()


async def set_coffee_type(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(brew_time=answer)
    await message.answer("Расскажи, что за кофе:")
    await Recipe.coffee_type.set()


async def recipe_result(message: Message, state: FSMContext):
    answer = message.text
    now = datetime.utcnow() + timedelta(hours=3)
    await state.update_data(coffee_type=answer)
    await state.update_data(name=f"Рецепт от {now.strftime('%d.%m.%Y в %H:%M')}")
    await state.update_data(photo_url="/aaad")
    data = await state.get_data()
    resp, code = add_a_recipe_service(message, data)
    await message.answer(resp)
    if code != 200:
        await state.reset_state(with_data=False)
    else:
        await state.reset_state(with_data=False)


def register_add_recipe(dp: Dispatcher):
    dp.register_message_handler(set_water, commands=["add"], state="*")
    dp.register_message_handler(set_coffee, state=Recipe.water_volume)
    dp.register_message_handler(set_water_temperature, state=Recipe.amount_of_coffee)
    dp.register_message_handler(set_brew_time, state=Recipe.water_temperature)
    dp.register_message_handler(set_coffee_type, state=Recipe.brew_time)
    dp.register_message_handler(recipe_result, state=Recipe.coffee_type)
