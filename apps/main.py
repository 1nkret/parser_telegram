import asyncio

from os import getenv
from telethon import TelegramClient, events
from unicodedata import category

from apps.keyboards.new_project import new_project_keyboard
from apps.modules.forwarder import parser
from apps.utils.json_loader import get_dest_channels
from apps.keyboards.confirm import confirm_keyboard
from apps.database.core import db_unnamed, db_actuals

api_id = int(getenv("API_ID"))
api_hash = getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")
phone_number = getenv("PHONE_NUMBER")
entity = getenv("ENTITY")

bot_admins = [int(el) for el in getenv("BOT_ADMINS").split(",")]
chats = [int(el) for el in getenv("CHATS").split(",")]

last_processed_message_id = None

client = TelegramClient('client', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash)


@client.on(events.NewMessage(chats=chats))
async def handle_new_message(event):
    global last_processed_message_id

    last_processed_message_id = await parser(
        client=client,
        bot=bot,
        event=event,
        last_processed_message_id=last_processed_message_id,
        entity=entity,
        bot_admins=bot_admins
    )


@bot.on(events.CallbackQuery())
async def callback_handler(event):
    data = event.data.decode()

    if data.endswith("_save_as_unnamed"):
        async with client.conversation(event.sender_id) as conv:
            msg_id = data.split("_")[0]
            pups = msg_id.split("/")
            response_db = db_unnamed.read_all_documents({"msg_id": msg_id})

            await event.edit_message("Confirm", buttons=confirm_keyboard())
            response = conv.wait_event(events.CallbackQuery)

            if response_db:
                link = response_db[0].get("link")
                category = response_db[0].get("category")
                doc_id = response_db[0].get("_id")

                if response.data == b"confirm_yes":
                    actuality = get_dest_channels().get("actuality_project")
                    db_unnamed.delete_document(doc_id)
                    await client.send_message(
                        entity=entity,
                        message=f"1 | [Project]({link}) #{category}",
                        reply_to=actuality
                    )
                    await event.edit_message(
                        message=f"[Project]({link}) saved as unnamed."
                    )
                elif response.data == b"confirm_no":
                    await event.edit_message(
                        message=f"New unnamed project!\n({link})",
                        buttons=new_project_keyboard(pups[0], pups[1])
                    )
            else:
                await event.delete_message()

    elif data.endswith("_delete_actuality"):
        async with client.conversation(event.sender_id) as conv:
            await event.edit_message("Confirm", buttons=confirm_keyboard())
            response = conv.wait_event(events.CallbackQuery)

            msg_id = data.split("_")[0]
            pups = msg_id.split("/")
            response_db = db_unnamed.read_all_documents({"msg_id": msg_id})

            if response_db:
                link = response_db.get("link")

                if response.data == b"confirm_yes":
                    db_unnamed.delete_document(response_db[0].get("_id"))
                    await event.edit_message(
                        message=f"[Project]({link}) is deleted."
                    )
                elif response.data == b"confirm_no":
                    await event.edit_message(
                        message=f"New unnamed project!\n({link})",
                        buttons=new_project_keyboard(pups[0], pups[1])
                    )

    elif data.endswith("_give_name_actuality"):
        async with client.conversation(event.sender_id) as conv:
            await event.edit_message(
                message="Input name for this project:"
            )
            name = conv.get_response()

            msg_id = data.split("_")[0]
            pups = msg_id.split("/")
            await event.edit_message(
                message=f"Confirm name: **{name}**",
                buttons=confirm_keyboard()
            )
            response = conv.wait_event(events.CallbackQuery)
            db_response = db_unnamed.read_all_documents({"msg_id": msg_id})

            if db_response:
                link = db_response[0].get("link")
                category = db_response[0].get("category")
                if response.data == b"confirm_yes":
                    find_name = db_actuals.read_all_documents({"name": name})
                    if find_name:
                        count = find_name[0].get("text").count("\n")+2
                        message_id = find_name[0].get("message_id")
                        doc_id = find_name[0].get("_id")

                        if category:
                            text = f"{count} | [{name}]({link}) #{category}"
                        else:
                            text = f"{count} | {name}]({link})"
                        new_text = find_name[0].get("text")+f"\n{text}"
                        db_unnamed.delete_document(db_response[0].get("_id"))
                        db_actuals.update_document(doc_id, new_text)

                        await client.edit_message(
                            entity=entity,
                            message=message_id,
                            text=text
                        )
                        await event.edit_message(
                            message=f"Unnamed project renamed to [{name}]({link})",
                        )
                    else:
                        await client.send_message(
                            entity=entity,
                            message=f"1 | [{name}]({link}) #{category}",
                            reply_to=get_dest_channels().get("actuality_project")
                        )
                elif response.data == b"confirm_no":
                    await event.edit_message(
                        message=f"New unnamed project!\n({link})",
                        buttons=new_project_keyboard(pups[0], pups[1])
                    )


async def main():
    print("Client is running...")
    # password = input("Passoword:")
    client.start(phone_number)
    print("Client is started.")

    print("Bot is running...")
    bot.start(bot_token=bot_token)
    print("Bot is started.")

    await asyncio.gather(
        client.run_until_disconnected(),
        bot.run_until_disconnected(),
    )

