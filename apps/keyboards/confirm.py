from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_keyboard(msg_id, action="none"):
    buttons = [
        [
            InlineKeyboardButton(
                text="Yes",
                callback_data=f"{msg_id}_{action}_confirm_yes"
            ),
            InlineKeyboardButton(
                text="No",
                callback_data=f"{msg_id}_{action}_confirm_no"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
