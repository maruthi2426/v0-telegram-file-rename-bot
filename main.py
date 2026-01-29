import logging
import os
import sys
import asyncio
from dotenv import load_dotenv

from pyrogram import Client, idle
from pyrogram.storage import MemoryStorage
from pyrogram.types import BotCommand

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Validate environment variables
required_vars = ["API_ID", "API_HASH", "BOT_TOKEN", "DATABASE_URL"]
missing = [v for v in required_vars if not os.getenv(v)]

if missing:
    logger.error(f"❌ Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

# ✅ CORRECT CLIENT + STORAGE INITIALIZATION
app = Client(
    "FileRenameBot",                              # Client name (POSITIONAL)
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    storage=MemoryStorage("FileRenameBot")        # Storage name REQUIRED
)

# Import handlers AFTER app creation
from handlers import (
    start_handler,
    rename_handler,
    thumbnail_handler,
    caption_handler,
    admin_handler,
    user_handler,
    metadata_handler
)

async def set_commands():
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("autorename", "Set auto rename format"),
        BotCommand("showformat", "View rename format"),
        BotCommand("tutorial", "How to use"),
        BotCommand("leaderboard", "Leaderboard"),
        BotCommand("viewthumb", "View thumbnail"),
        BotCommand("delthumb", "Delete thumbnail"),
        BotCommand("set_caption", "Set caption"),
        BotCommand("see_caption", "View caption"),
        BotCommand("del_caption", "Delete caption"),
        BotCommand("setmedia", "Set output file type"),
        BotCommand("start_sequence", "Start sequence"),
        BotCommand("end_sequence", "End sequence"),
        BotCommand("metadata", "Show metadata"),
        BotCommand("ping", "Check bot status"),
        BotCommand("donate", "Support developer"),
        BotCommand("set_prefix", "Set prefix"),
        BotCommand("see_prefix", "View prefix"),
        BotCommand("del_prefix", "Delete prefix"),
        BotCommand("set_suffix", "Set suffix"),
        BotCommand("see_suffix", "View suffix"),
        BotCommand("del_suffix", "Delete suffix"),
    ]

    await app.set_bot_commands(commands)
    logger.info("✅ Bot commands set successfully")

async def main():
    try:
        logger.info("🚀 Starting bot...")
        await app.start()

        await set_commands()

        me = await app.get_me()
        logger.info(f"🤖 Bot started as {me.first_name} (@{me.username})")
        logger.info("=" * 60)
        logger.info("✅ BOT IS LIVE AND READY")
        logger.info("=" * 60)

        await idle()

    except Exception:
        logger.error("🔥 Critical startup failure", exc_info=True)
        sys.exit(1)

    finally:
        await app.stop()
        logger.info("🛑 Bot stopped cleanly")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
