from os import getenv
from telethon import TelegramClient
from apps.utils.ai_utils import response_ai
from apps.utils.telegram_utils import forward_message_to_channel


async def parser(
        client: TelegramClient,
        event,
        last_processed_message_id,
        destination_channels,
        allow_list,
        get_category_prompt,
        get_title_prompt
):
    message = event.message
    if message.id == last_processed_message_id:
        return

    category = response_ai(message.text, get_category_prompt).rstrip()
    target_channel = destination_channels.get(category)

    if target_channel:
        try:
            entity = getenv("ENTITY")
            link_message = f"\n\n{'=' * 20}\n**Link to [post](https://t.me/{event.chat.username}/{message.id})**"
            await forward_message_to_channel(client, event, category, target_channel, entity, response_ai, link_message, allow_list, destination_channels, get_title_prompt)
            return message.id
        except Exception as e:
            raise f"Error while forwarding message: {e}"
