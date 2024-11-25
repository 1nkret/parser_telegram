import asyncio
from aiogram import Router, types

from apps.keyboards.confirm import confirm_keyboard
from apps.database.core import db_unnamed


router = Router()


@router.callback_query(lambda c: c.data.endswith("_save_as_unnamed"))
async def save_as_unnamed_callback_handler(query: types.CallbackQuery):
    msg_id = query.data.split("_")[0]
    response_db = db_unnamed.read_all_documents({"msg_id": int(msg_id)})

    if not response_db:
        await query.message.edit_text("Data not found or already processed")
        await asyncio.sleep(30)
        await query.message.delete()
        return

    await query.message.edit_text(
        text="Confirm",
        reply_markup=confirm_keyboard(msg_id, "unnamed")
    )
