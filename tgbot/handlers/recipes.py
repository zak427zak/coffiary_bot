from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.get_recipes_service import get_recipes_service


async def recipe(message: Message):
    resp, code = get_recipes_service(message)
    await message.answer(resp)


def register_get_recipes(dp: Dispatcher):
    dp.register_message_handler(recipe, commands=["recipes"], state="*")
