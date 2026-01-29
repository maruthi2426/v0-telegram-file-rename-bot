import logging
import os
import sys
from dotenv import load_dotenv

from pyrogram import Client, idle
from pyrogram.types import BotCommand

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Validate env vars
required_vars = ["API_ID", "API_HASH", "BOT_TOKEN"]
missing = [v for v in required_vars if not os.getenv(v)]

if missing:
    logger.error(f"❌ Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

# ✅ CLASSIC PYROGRAM CLIENT (OLDER VERSION SAFE)
app = Client(
    "FileRenameBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
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

@app.on_message()
async def _dummy(_, __):
    pass

def set_commands():
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
        BotCommand("metadata", "Show metadata"),
        BotCommand("ping", "Check bot status"),
        BotCommand("donate", "Support developer"),
    ]

    app.set_bot_commands(commands)

if __name__ == "__main__":
    try:
        logger.info("🚀 Starting bot...")
        app.start()

        set_commands()

        me = app.get_me()
        logger.info(f"🤖 Bot started as {me.first_name} (@{me.username})")
        logger.info("✅ BOT IS LIVE")
        logger.info("=" * 60)

        idle()

    except Exception:
        logger.error("🔥 Bot crashed", exc_info=True)
        sys.exit(1)

    finally:
        app.stop()
        logger.info("🛑 Bot stopped")
