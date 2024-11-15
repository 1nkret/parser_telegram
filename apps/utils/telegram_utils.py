from asyncio import Lock
from telethon import TelegramClient

from apps.database.core import db

db_lock = Lock()


async def forward_message_to_channel(
        client: TelegramClient,
        event,
        category,
        target_channel,
        entity,
        response_ai,
        link_message,
        allow_list,
        destination_channels,
        get_title_prompt,
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
        category=category,
        entity=entity,
        target_channel=target_channel,
        msg=msg,
        allow_list=allow_list,
        destination_channels=destination_channels,
        get_title_prompt=get_title_prompt,
        response_ai=response_ai,
    )


async def forward_to_actuality(
        client: TelegramClient,
        event,
        category,
        entity,
        target_channel,
        msg,
        allow_list,
        destination_channels,
        get_title_prompt,
        response_ai,
):
    if category in allow_list:
        actuality = destination_channels.get("actuality_project")
        if actuality:
            answer = response_ai(event.message.text, get_title_prompt).rstrip()
            append_text = f"[{answer}]({entity}/{target_channel}/{msg.id})  #{category.replace('_', '')}"

            async with db_lock:
                response_db = db.read_all_documents({"name": answer})

                if response_db:
                    message_id = response_db[0].get("message_id")
                    message_text = response_db[0].get("text")
                    count = message_text.count('\n')+2

                    document_id = response_db[0].get("_id")

                    text = f"{message_text}\n{count} | {append_text}"

                    db.update_document(document_id, {"text": text})
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
                    db.create_document(
                        {
                            "name": answer,
                            "message_id": actual_msg.id,
                            "text": f"1 | {append_text}"
                        }
                    )
