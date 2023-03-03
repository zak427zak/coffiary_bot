from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.register_new_user import register_new_user


async def user_start(message: Message):
    register_new_user(message)

    await message.answer(
        f"Привет! Это бот для удобного ведения дневников кофейных рецептов.\n\nОн поможет лучше понять процесс заваривания, и через него научиться понимать, как небольшие вещи (например, изменение температуры воды на 10 градусов) способны влиять на результат.\n\nДля добавления нового рецепта вызовите команду /add\nДля просмотра всех своих рецептов вызовите команду /unsorted\nРецепты, отсортированные по датам - командой /sorted")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
