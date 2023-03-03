from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.get_recipes_service import get_recipes_service


async def recipe(message: Message):
    resp = get_recipes_service(message, "false", "")
    for item in resp:
        await message.answer_photo(photo=item['image'], caption=item['text'])


def register_get_recipes(dp: Dispatcher):
    dp.register_message_handler(recipe, commands=["unsorted"], state="*")
