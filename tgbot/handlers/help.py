from aiogram import Dispatcher
from aiogram.types import Message


async def user_help(message: Message):
    await message.answer(
        f"Пожелания, предложения и иная обратная связь - @German_goncharov\n\nP.S. Бот находится в открытом доступе, исходный код проекта https://github.com/zak427zak/coffiary_bot",
        disable_web_page_preview=True)


def register_help(dp: Dispatcher):
    dp.register_message_handler(user_help, commands=["help"], state="*")
