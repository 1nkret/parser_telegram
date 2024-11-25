import asyncio
from aiogram import Router, types
from apps.database.core import db_unnamed, db_actuals
from apps.utils.json_loader import get_dest_channels
from apps.utils.escape_markdown import escape_markdown
from apps.keyboards.new_project import new_project_keyboard
from apps.main import client, entity


router = Router()


@router.callback_query(lambda c: c.data.endswith("confirm_yes") or c.data.endswith("confirm_no"))
async def confirm_callback_handler(query: types.CallbackQuery):
    msg_id = query.data.split("_")[0]
    response_db = db_unnamed.read_all_documents({"msg_id": int(msg_id)})

    if not response_db:
        await query.message.edit_text("Data not found or already processed")
        await asyncio.sleep(30)
        await query.message.delete()
        return

    link = response_db[0].get("link")
    cat = response_db[0].get("category")
    doc_id = response_db[0].get("_id")

    if query.data.endswith("confirm_yes"):
        action = query.data.split("_")[1]
        match action:
            case "unnamed":
                actuality = get_dest_channels().get("actuality_project")
                db_unnamed.delete_document(doc_id)

                await client.send_message(
                    entity=entity,
                    message=f"1 | [Project]({link}) #{cat}",
                    reply_to=actuality
                )
                await query.message.edit_text(f"[Project]({link}) saved as unnamed")
                await asyncio.sleep(30)
            case "delete":
                db_unnamed.delete_document(response_db[0].get("_id"))
                await query.message.edit_text(f"[Project]({link}) with ID {msg_id} has been deleted from the database")
                await asyncio.sleep(30)
            case "name":
                name = query.data.split("_")[2]
                find_name = db_actuals.read_all_documents({"name": name})

                if find_name:
                    count = find_name[0].get("text").count("\n") + 2
                    message_id = find_name[0].get("message_id")
                    doc_id = find_name[0].get("_id")

                    if cat:
                        text = f"{count} | [{name}]({link}) #{cat}"
                    else:
                        text = f"{count} | {name}]({link})"
                    new_text = find_name[0].get("text") + f"\n{text}"

                    db_unnamed.delete_document(response_db[0].get("_id"))
                    db_actuals.update_document(
                        doc_id, {
                            "text": new_text
                        }
                    )

                    await client.edit_message(
                        entity=entity,
                        message=message_id,
                        text=new_text
                    )
                    await query.message.edit_text(f"Unnamed project renamed to [{name}]({escape_markdown(link)})")
                    await asyncio.sleep(30)
                else:
                    text = f"1 | [{name}]({link}) #{cat}"
                    msg = await client.send_message(
                        entity=entity,
                        message=text,
                        reply_to=get_dest_channels().get("actuality_project")
                    )

                    db_unnamed.delete_document(response_db[0].get("_id"))
                    db_actuals.create_document(
                        {
                            "name": name,
                            "message_id": msg.id,
                            "text": text,
                            "category": cat,
                        }
                    )
                    await query.message.edit_text(f"Created project with name [{name}]({escape_markdown(link)})")
                    await asyncio.sleep(30)
            case _:
                await query.message.edit_text(f"Data not found. For debug {query.data}")
                await asyncio.sleep(30)
        await query.message.delete()

    elif query.data.endswith("confirm_no"):
        await query.message.edit_text(
            f"{msg_id} \\| New unnamed [project]({escape_markdown(link)})\\!",
            reply_markup=new_project_keyboard(msg_id)
        )