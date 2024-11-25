import asyncio

from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from telethon import TelegramClient, events
from dotenv import load_dotenv

from apps.utils.router_loader import load_routers
from apps.modules.forwarder import parser

load_dotenv()
api_id = getenv("API_ID")
api_hash = getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")
phone_number = getenv("PHONE_NUMBER")
entity = getenv("ENTITY")

bot_admins = getenv("BOT_ADMINS")
bot_admins = [int(el) for el in bot_admins.split(",")]
chats = getenv("CHATS")
chats = [int(el) for el in chats.split(",")]

last_processed_message_id = None

client = TelegramClient('client', int(api_id), api_hash)
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode="MarkdownV2"))
dp = Dispatcher()


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


async def main():
    print("Client is running...")
    await client.start(phone_number)
    print("Client is ready.")
    print("Bot is running...")
    dp.include_routers(
        load_routers()
    )
    print("Bot is ready...")

    await asyncio.gather(
        client.run_until_disconnected(),
        dp.start_polling(bot),
    )
