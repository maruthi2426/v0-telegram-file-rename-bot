import logging
import os
import sys
from dotenv import load_dotenv

from pyrogram import Client
from pyrogram.types import BotCommand

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Validate environment variables
required = ["API_ID", "API_HASH", "BOT_TOKEN"]
missing = [v for v in required if not os.getenv(v)]
if missing:
    logger.error(f"Missing env vars: {', '.join(missing)}")
    sys.exit(1)

# ✅ Pyrogram 1.4 SAFE client
app = Client(
    "FileRenameBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    in_memory=True   # VERY IMPORTANT for cloud
)

# Import handlers AFTER client creation
from handlers import (
    start_handler,
    rename_handler,
    thumbnail_handler,
    caption_handler,
    admin_handler,
    user_handler,
    metadata_handler
)

def set_commands():
    app.set_bot_commands([
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
    ])

if __name__ == "__main__":
    logger.info("🚀 Starting bot using app.run()")

    # app.run() handles start + idle + stop internally (NO CRASH)
    with app:
        set_commands()
        me = app.get_me()
        logger.info(f"🤖 Bot started as {me.first_name} (@{me.username})")
        logger.info("✅ BOT IS LIVE & STABLE")

        app.idle()
