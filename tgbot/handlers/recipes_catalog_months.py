import logging

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_datas import coffiary_callback
from tgbot.keyboards.inline import create_months_keyboard
from tgbot.services.get_recipes_service import get_recipes_service


async def recipes_months(message: Message):
    new_months_keyboard = create_months_keyboard(message.from_user.id, "clear", 2)
    await message.answer(
        "Сгруппировали ваши рецепты по месяцам и дням, чтобы было удобнее с ними работать.\n\nВыберите месяц, за который хотите получить рецепты:",
        reply_markup=new_months_keyboard)


async def recipes_days(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    link = callback_data.get("link")
    new_months_keyboard = create_months_keyboard(call.from_user.id, link, 2)
    await call.message.answer("Теперь выберите день, за который хотите получить рецепты:",
        reply_markup=new_months_keyboard)


async def recipes_final(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    # Логируем входящий callback_data
    # logging.info(f"Callback data received: {callback_data}")

    current_data = callback_data
    resp = get_recipes_service(call, "true", current_data)

    # Логируем полученный ответ от get_recipes_service
    # logging.info(f"Response from get_recipes_service: {resp}")

    if not resp:
        logging.warning("No recipes found or response is None.")

    # Отправляем рецепты в Telegram
    for item in resp:
        # logging.info(f"Sending recipe photo: {item['image']} with caption: {item['text']}")
        await call.message.answer_photo(photo=item['image'], caption=item['text'])


def register_get_recipes_months(dp: Dispatcher):
    dp.register_message_handler(recipes_months, commands=["grouped"], state="*")
    dp.register_callback_query_handler(recipes_days, coffiary_callback.filter(period="months"))
    dp.register_callback_query_handler(recipes_final, coffiary_callback.filter(period="days"))
