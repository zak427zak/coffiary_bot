from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import coffiary_callback
from tgbot.services.get_recipes_months_service import get_recipes_months_service


def create_months_keyboard(user_id, keyboard_type, width):
    all_reciklomats_keyboard = InlineKeyboardMarkup(row_width=width)
    data = get_recipes_months_service(user_id, keyboard_type)
    if keyboard_type == "clear":
        icon = "📦"
    elif keyboard_type == "concrete":
        icon = "📅"
    else:
        icon = "📅"
    for item in data:
        reciklomat_button = InlineKeyboardButton(text=f"{icon} {item['block']}",
                                                 callback_data=coffiary_callback.new(id=item['id'],
                                                                                     parent=item['parent'],
                                                                                     period=item['period'],
                                                                                     link=item['link']))
        all_reciklomats_keyboard.insert(reciklomat_button)

    return all_reciklomats_keyboard
