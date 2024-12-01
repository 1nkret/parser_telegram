from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from apps.handlers.orm.keyboards import orm_menu, cancel
from apps.handlers.orm.state import FindName


router = Router()


@router.callback_query(lambda c: c.data == "orm_menu")
async def orm_menu_callback(query: types.CallbackQuery):
    text = "**Hyan Database**\nProjects\:\nUnnamed projects\:\nMessages\:\nORM Admins\:"
    await query.message.edit_text(
        text=text,
        reply_markup=orm_menu()
    )


@router.callback_query(lambda c: c.data == "find_by_name")
async def orm_find_by_name_callback(query: types.CallbackQuery, state: FSMContext):
    text = "Input keyword of project name:"
    await query.message.edit_text(
        text=text,
        reply_markup=cancel("finderName")
    )
    await state.set_state(FindName.name)
    await state.set_data({"msg_id": query.inline_message_id})


@router.message(FindName.name)
async def find_by_name_callback(message: types.CallbackQuery, state: FSMContext):
    founded = True
    if founded:
        text = f"Founded projects by \"{message.text}\""
    else:
        text = f"Projects not found by name \"{message.text}\""

    await message.answer(
        text=text,
        reply_markup=cancel("find_by_name")
    )

@router.callback_query(lambda c: c.data.startswith("cancel"))
async def orm_cancel_callback(query: types.CallbackQuery):
    data = query.data.split("_")
    target = data[1]

    if target == "finderName":
        text = "**Hyan Database**\nProjects\:\nUnnamed projects\:\nMessages\:\nORM Admins\:"
        await query.message.edit_text(
            text=text,
            reply_markup=orm_menu()
        )
