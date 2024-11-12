from telethon import TelegramClient


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
        get_title_prompt
):
    if event.message.photo:
        photo = await client.download_media(event.message.photo, file="media/")
        msg = await client.send_file(
            entity=entity,
            file=photo,
            caption=event.message.text + link_message or link_message,
            reply_to=target_channel
        )
        await forward_to_actuality(client, event, category, entity, target_channel, msg, allow_list, destination_channels, get_title_prompt, response_ai)
    else:
        msg = await client.send_message(
            entity=entity,
            message=event.message.text + link_message,
            reply_to=target_channel
        )
        await forward_to_actuality(client, event, category, entity, target_channel, msg, allow_list, destination_channels, get_title_prompt, response_ai)


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
        response_ai
):
    if category in allow_list:
        actuality = destination_channels.get("actuality_project")
        if actuality:
            answer = response_ai(event.message.text, get_title_prompt).rstrip()
            await client.send_message(
                entity=entity,
                message=f"{answer} [#{category.replace('_', '')}]({entity}/{target_channel}/{msg.id})",
                reply_to=actuality
            )
        else:
            raise "Actuality is not exists. Check chat_id/topic_id"
