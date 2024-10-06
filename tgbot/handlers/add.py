from datetime import datetime, timedelta

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from tgbot.misc.states import Recipe
from tgbot.services.add_a_recipe_service import add_a_recipe_service


async def set_water(message: Message):
    await message.answer(
        "❗ Пока бот работает в тестовом режиме, в нем нет валидации типов данных.\n\nПоэтому вводите данные в том виде, в котором указано в (ТЕКСТЕ В СКОБКАХ)")
    await message.answer(
        "🌊 Введите объем воды, число в миллилитрах:")
    await Recipe.water_volume.set()


async def set_coffee(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(water_volume=answer)
    await message.answer("⚖️ Введите количество кофе, в граммах (ЧИСЛО):")
    await Recipe.amount_of_coffee.set()


async def set_water_temperature(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(amount_of_coffee=answer)
    await message.answer("🌡️ Введите температуру воды, в градусах Цельсия (ЧИСЛО):")
    await Recipe.water_temperature.set()


async def set_brew_time(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(water_temperature=answer)
    await message.answer("⏱️ Введите общее время заваривания, в секундах (ЧИСЛО):")
    await Recipe.brew_time.set()


async def set_grind_size(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(brew_time=answer)
    await message.answer("📏 Укажите размер помола, в щелчках (ЧИСЛО):")
    await Recipe.grind_size.set()


async def set_coffee_type(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(grind_size=answer)
    await message.answer("🫘 Расскажите, что за кофе (ТЕКСТ):")
    await Recipe.coffee_type.set()


async def set_description(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(coffee_type=answer)
    await message.answer("💬 Опишите впечатления (ТЕКСТ):")
    await Recipe.description.set()


async def set_grade(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(description=answer)
    await message.answer("⭐ Поставьте общую оценку от 1 до 10 (ЧИСЛО):")
    await Recipe.grade.set()


async def set_photo(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(grade=answer)
    await message.answer("📷 Прикрепите фотографию (ФОТО):")
    await Recipe.photo_url.set()


async def recipe_result(message: Message, state: FSMContext):
    answer = message.photo[-1].file_id
    now = datetime.utcnow() + timedelta(hours=3)
    await state.update_data(photo_url=answer)
    await state.update_data(name=f"Рецепт от {now.strftime('%d.%m.%Y в %H:%M')}")
    data = await state.get_data()
    resp, code = add_a_recipe_service(message, data)

    # Отправляем только значение по ключу 'result'
    await message.answer(resp['result'])

    if code != 200:
        await state.reset_state(with_data=False)
    else:
        await state.reset_state(with_data=False)


def register_add_recipe(dp: Dispatcher):
    dp.register_message_handler(set_water, commands=["add"], state="*")
    dp.register_message_handler(set_coffee, state=Recipe.water_volume)
    dp.register_message_handler(set_water_temperature, state=Recipe.amount_of_coffee)
    dp.register_message_handler(set_brew_time, state=Recipe.water_temperature)
    dp.register_message_handler(set_grind_size, state=Recipe.brew_time)
    dp.register_message_handler(set_coffee_type, state=Recipe.grind_size)
    dp.register_message_handler(set_description, state=Recipe.coffee_type)
    dp.register_message_handler(set_grade, state=Recipe.description)
    dp.register_message_handler(set_photo, state=Recipe.grade)
    dp.register_message_handler(recipe_result, content_types=ContentType.PHOTO, state=Recipe.photo_url)
