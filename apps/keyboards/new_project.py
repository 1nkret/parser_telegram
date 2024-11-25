from aiogram import types


def new_project_keyboard(
        msg_id
):
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Call by name",
                callback_data=f"{msg_id}_give_name_actuality"
            ),
            types.InlineKeyboardButton(
                text="Delete",
                callback_data=f"{msg_id}_delete_actuality"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="Save as unnamed",
                callback_data=f"{msg_id}_save_as_unnamed"
            )
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
