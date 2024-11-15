import asyncio

from os import getenv
from telethon import TelegramClient

from apps.utils.ai_utils import response_ai
from apps.utils.telegram_utils import forward_message_to_channel

lock_parser = asyncio.Lock()


async def parser(
        client: TelegramClient,
        event,
        last_processed_message_id,
        destination_channels,
        allow_list,
        get_category_prompt,
        get_title_prompt,
):
    message = event.message
    if message.id == last_processed_message_id:
        return

    category = response_ai(
        text=message.text,
        prompt=get_category_prompt
    ).rstrip()
    target_channel = destination_channels.get(category)

    if not target_channel:
        return

    entity = getenv("ENTITY")
    link_message = f"\n\n{'=' * 20}\n**Link to [post](https://t.me/{event.chat.username}/{message.id})**"

    tries = 0
    max_retries = 15

    while tries < max_retries:
        try:
            await forward_message_to_channel(
                client=client,
                event=event,
                category=category,
                target_channel=target_channel,
                entity=entity,
                response_ai=response_ai,
                link_message=link_message,
                allow_list=allow_list,
                destination_channels=destination_channels,
                get_title_prompt=get_title_prompt,
            )
            return message.id
        except Exception as e:
            tries += 1
            print(f"[{tries}/{max_retries}] Error while forwarding message: {e}. Retrying...")
            await asyncio.sleep(30)
