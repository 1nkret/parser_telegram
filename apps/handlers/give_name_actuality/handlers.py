import asyncio
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from apps.database.core import db_unnamed
from apps.states.get_name import GetName
from apps.keyboards.confirm import confirm_keyboard
from apps.main import bot


router = Router()


@router.callback_query(lambda c: c.data.endswith("_give_name_actuality"))
async def give_name_actuality_callback_handler(query: types.CallbackQuery, state: FSMContext):
    msg_id = query.data.split("_")[0]
    response_db = db_unnamed.read_all_documents({"msg_id": int(msg_id)})

    if not response_db:
        await query.message.edit_text("Data not found or already processed")
        await asyncio.sleep(30)
        await query.message.delete()
        return

    await query.answer("Input name...")
    await query.message.edit_text("Waiting name\\.\\.\\.")

    await state.set_state(GetName.name)
    await state.update_data(message_id=query.message.message_id)
    await state.update_data(msg_id=msg_id)


@router.message(GetName.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text

    await state.update_data(name=name)

    data = await state.get_data()
    msg_id = data.get('msg_id')
    message_id = data.get('message_id')

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message_id,
        text=f"Confirm name\\: **{name}**",
        reply_markup=confirm_keyboard(
            msg_id=msg_id,
            action=f"name_{name}"
        )
    )
    await state.clear()