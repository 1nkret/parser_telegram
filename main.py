import asyncio
from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient, events
from apps.modules.forwarder import parser
from apps.utils.json_loader import get_dest_channels, get_allow_list
from apps.utils.read_prompt import read_title_prompt, read_category_prompt

load_dotenv()

api_id = int(getenv("API_ID"))
api_hash = getenv("API_HASH")
phone_number = getenv("PHONE_NUMBER")
last_processed_message_id = None

client = TelegramClient('session_name', api_id, api_hash)


@client.on(events.NewMessage(chats=[2304032049, 1562540437]))
async def handle_new_message(event):
    global last_processed_message_id

    last_processed_message_id = await parser(
        client=client,
        event=event,
        last_processed_message_id=last_processed_message_id,
        destination_channels=get_dest_channels(),
        allow_list=get_allow_list(),
        get_category_prompt=read_category_prompt(),
        get_title_prompt=read_title_prompt()
    )


async def main():
    print("Client is running...")
    await client.start(phone_number, password=input("Password: "))
    print("\n"*100)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
