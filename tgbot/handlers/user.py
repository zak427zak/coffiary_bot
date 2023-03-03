from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.register_new_user import register_new_user


async def user_start(message: Message):
    register_new_user(message)

    await message.answer(
        f"Привет! Это бот для удобного ведения дневников кофейных рецептов.\n\nЭто поможет лучше понять процесс приготовления, и через него научиться понимать, как небольшие вещи на примере кофе способны что-то менять. И не только в кофе.\n\nДля добавления нового рецепта вызови команду /add\nДля просмотра своих рецептов вызовки команду /recipes")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
