import asyncio

from os import getenv
from telethon import TelegramClient

from apps.utils.ai_utils import response_ai
from apps.utils.telegram_utils import forward_message_to_channel
from apps.utils.read_prompt import read_category_prompt
from apps.utils.json_loader import get_dest_channels

lock_parser = asyncio.Lock()


async def parser(
        client: TelegramClient,
        event,
        bot,
        last_processed_message_id,
        entity,
        bot_admins
):
    message = event.message
    if message.id == last_processed_message_id:
        return

    category = response_ai(
        text=message.text,
        prompt=read_category_prompt()
    ).rstrip()
    target_channel = get_dest_channels().get(category)

    if not target_channel:
        return

    link_message = f"\n\n{'=' * 20}\n**Link to [post](https://t.me/{event.chat.username}/{message.id})**"

    tries = 0
    max_retries = 15

    while tries < max_retries:
        try:
            await forward_message_to_channel(
                client=client,
                event=event,
                bot=bot,
                category=category,
                target_channel=target_channel,
                entity=entity,
                link_message=link_message,
                bot_admins=bot_admins
            )
            return message.id
        except Exception as e:
            tries += 1
            print(f"[{tries}/{max_retries}] Error while forwarding message: {e}. Retrying...")
            await asyncio.sleep(30)
