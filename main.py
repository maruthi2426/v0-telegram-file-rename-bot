import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "FileRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

from handlers import (
    start_handler,
    rename_handler,
    thumbnail_handler,
    caption_handler,
    admin_handler,
    user_handler,
    metadata_handler
)

@app.on_message(filters.command("start"))
async def start_test(_, message: Message):
    await message.reply_text("✅ Bot is ONLINE & WORKING")

async def runner():
    await app.set_bot_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("autorename", "Auto rename files"),
    ])
    me = await app.get_me()
    log.info(f"🤖 Bot started as {me.first_name} (@{me.username})")

if __name__ == "__main__":
    log.info("🚀 Starting bot using app.run()")
    app.run(runner())   # ✅ NOTE: runner() NOT runner
