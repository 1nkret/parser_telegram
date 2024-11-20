from asyncio import Lock
from telethon import TelegramClient

from apps.database.core import db_actuals
from apps.utils.ai_utils import response_ai
from apps.utils.json_loader import get_allow_list, get_dest_channels
from apps.utils.read_prompt import read_title_prompt
from apps.keyboards.new_project import new_project_keyboard

db_lock = Lock()


async def forward_message_to_channel(
        client: TelegramClient,
        event,
        bot,
        category,
        target_channel,
        entity,
        link_message,
        bot_admins
):
    if event.message.photo:
        photo = await client.download_media(event.message.photo, file="media/")
        msg = await client.send_file(
            entity=entity,
            file=photo,
            caption=event.message.text + link_message or link_message,
            reply_to=target_channel
        )
    else:
        msg = await client.send_message(
            entity=entity,
            message=event.message.text + link_message,
            reply_to=target_channel
        )

    await forward_to_actuality(
        client=client,
        event=event,
        bot=bot,
        category=category,
        entity=entity,
        target_channel=target_channel,
        msg=msg,
        bot_admins=bot_admins
    )


async def forward_to_actuality(
        client: TelegramClient,
        event,
        bot,
        category,
        entity,
        target_channel,
        msg,
        bot_admins
):
    if category in get_allow_list():
        actuality = get_dest_channels().get("actuality_project")
        if actuality:
            answer = response_ai(event.message.text, read_title_prompt()).rstrip()
            link = f"{entity}/{target_channel}/{msg.id}"
            append_text = f"[{answer}]({link})  #{category.replace('_', '')}"

            if answer == "Unnamed":
                for admin in bot_admins:
                    await bot.send_message(
                        entity=admin,
                        message=f"New unnamed project!\n({link})",
                        buttons=new_project_keyboard(target_channel, msg.id)
                    )
                    return

            async with db_lock:
                response_db = db_actuals.read_all_documents({"name": answer})

                if response_db:
                    message_id = response_db[0].get("message_id")
                    message_text = response_db[0].get("text")
                    count = message_text.count('\n')+2

                    document_id = response_db[0].get("_id")

                    text = f"{message_text}\n{count} | {append_text}"

                    db_actuals.update_document(document_id, {"text": text})
                    await client.edit_message(
                        entity=entity,
                        message=message_id,
                        text=text,
                    )

                else:
                    actual_msg = await client.send_message(
                        entity=entity,
                        message=f"1 | {append_text}",
                        reply_to=actuality
                    )
                    db_actuals.create_document(
                        {
                            "name": answer,
                            "message_id": actual_msg.id,
                            "text": f"1 | {append_text}",
                            "category": category,
                        }
                    )
