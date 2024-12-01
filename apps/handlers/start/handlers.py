from aiogram import Router, types
from aiogram.filters import Command
from apps.main import bot_admins
from apps.handlers.start.keyboard import menu_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    status = "User"
    if message.from_user.id in bot_admins:
        status = "Admin"

    text = f"Hi there\\! Your status \\- {status}\\."
    await message.answer(
        text=text,
        reply_markup=menu_keyboard(status)
    )
