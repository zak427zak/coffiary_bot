from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_datas import coffiary_callback
from tgbot.keyboards.inline import create_months_keyboard
from tgbot.services.get_recipes_service import get_recipes_service


async def recipe(message: Message):
    new_months_keyboard = create_months_keyboard(message.from_user.id, "concrete", 1)
    await message.answer(
        "Выберите нужный рецепт из списка:",
        reply_markup=new_months_keyboard)


async def recipes_final(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    current_data = callback_data
    resp = get_recipes_service(call, "true", current_data)
    for item in resp:
        await call.message.answer_photo(photo=item['image'], caption=item['text'])


def register_get_recipes(dp: Dispatcher):
    dp.register_message_handler(recipe, commands=["ungrouped"], state="*")
    dp.register_callback_query_handler(recipes_final, coffiary_callback.filter())
