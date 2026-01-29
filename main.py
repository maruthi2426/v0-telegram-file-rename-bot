import logging
import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message
from pyrogram.errors import RPCError

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# Environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create Pyrogram client
app = Client(
    "FileRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Import handlers (make sure these files exist in handlers/)
from handlers import (
    start_handler,
    rename_handler,
    thumbnail_handler,
    caption_handler,
    admin_handler,
    user_handler,
    metadata_handler
)

# Example start command handler
@app.on_message(filters.command("start"))
async def start_test(_, message: Message):
    await message.reply_text("✅ Bot is ONLINE & WORKING")

# Async runner to start bot properly
async def runner():
    # Start the client
    await app.start()
    
    # Set bot commands after client started
    try:
        await app.set_bot_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("autorename", "Auto rename files"),
        ])
    except RPCError as e:
        log.warning(f"⚠️ Failed to set bot commands: {e}")

    # Log bot info
    me = await app.get_me()
    log.info(f"🤖 Bot started as {me.first_name} (@{me.username})")

    # Keep bot running until interrupted
    await app.idle()

if __name__ == "__main__":
    log.info("🚀 Starting bot...")

    import asyncio
    asyncio.run(runner())
