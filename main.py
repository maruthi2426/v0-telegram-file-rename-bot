import logging
import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message
from pyrogram.errors import RPCError

# Load env (works locally; Heroku uses Config Vars)
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# Read env safely
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Hard fail if missing (prevents silent crashes)
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError("❌ Missing API_ID / API_HASH / BOT_TOKEN")

API_ID = int(API_ID)

# Pyrogram Client
app = Client(
    name="FileRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Import handlers
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

async def main():
    try:
        await app.start()

        await app.set_bot_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("autorename", "Auto rename files"),
        ])

        me = await app.get_me()
        log.info(f"🤖 Bot started as {me.first_name} (@{me.username})")

        # Keep alive (Pyrogram v2 way)
        await asyncio.Event().wait()

    except RPCError as e:
        log.error(f"❌ Telegram RPC Error: {e}")
        raise
    except Exception as e:
        log.error(f"❌ Startup failed: {e}")
        raise

if __name__ == "__main__":
    log.info("🚀 Starting bot...")
    asyncio.run(main())
