from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def orm_menu():
    buttons = [
        [
            InlineKeyboardButton(
                text="Find",
                callback_data="find_by_name",
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def cancel(target: str):
    """
    Cancel any
    :param target: callback to specificity what to cancel
    :return: keyboard
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="Cancel",
                callback_data="cancel_"+target,
            )
        ]
    ]
