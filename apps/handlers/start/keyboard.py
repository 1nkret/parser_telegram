from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_keyboard(status: str):
    if status != "Admin":
        return InlineKeyboardMarkup(inline_keyboard=[])
    menu = [
        [
            InlineKeyboardButton(
                text="ORM",
                callback_data="orm_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=menu)


def projects_founded(founded: bool):
    if not founded:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Back to menu",
                        callback_data="orm_menu"
                    )
                ]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="test_proj",
                    callback_data="test_proj"
                )
            ]
        ]
    )
