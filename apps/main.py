import asyncio

from os import getenv
from telethon import TelegramClient, events

from apps.keyboards.new_project import new_project_keyboard
from apps.modules.forwarder import parser
from apps.utils.json_loader import get_dest_channels
from apps.keyboards.confirm import confirm_keyboard
from apps.database.core import db_unnamed

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
            await event.edit_message("Confirm", buttons=confirm_keyboard())
            response = conv.wait_event(events.CallbackQuery)

            msg_id = data.split("_")[0]
            pups = msg_id.split("/")
            response_db = db_unnamed.read_all_documents({"msg_id": msg_id})[0]

            if response_db:
                link = response_db.get("link")
                category = response_db.get("category")
                doc_id = response_db.get("_id")

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
            response_db = db_unnamed.read_all_documents({"msg_id": msg_id})[0]
            if response_db:
                link = response_db.get("link")

                if response.data == b"confirm_yes":
                    db_unnamed.delete_document(msg_id)
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
            msg = await bot.send_message("Input name for this project:")
            response = conv.get_response()

            msg_id = data.split("_")[0]
            pups = msg_id.split("/")

            db_unnamed.delete_document(msg_id)


async def main():
    print("Client is running...")
    # password = input("Passoword:")
    await client.start(phone_number)
    print("Client is started.")

    print("Bot is running...")
    await bot.start(bot_token=bot_token)
    print("Bot is started.")

    await asyncio.gather(
        client.run_until_disconnected(),
        bot.run_until_disconnected(),
    )

