import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import BotCommand

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- ENV VALIDATION ----------------
required_vars = ["API_ID", "API_HASH", "BOT_TOKEN", "DATABASE_URL"]
missing = [v for v in required_vars if not os.getenv(v)]

if missing:
    logger.error(f"Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------------- CLIENT ----------------
app = Client(
    "FileRenameBot",   # SESSION NAME ONLY (STRING)
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- IMPORT HANDLERS ----------------
from handlers import (
    start_handler,
    rename_handler,
    thumbnail_handler,
    caption_handler,
    admin_handler,
    user_handler,
    metadata_handler
)

# ---------------- STARTUP TASK ----------------
@app.on_startup()
async def startup_tasks(client: Client):
    try:
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("autorename", "Set auto rename format"),
            BotCommand("showformat", "View your rename format"),
            BotCommand("tutorial", "Usage guide"),
            BotCommand("leaderboard", "View leaderboard"),
            BotCommand("viewthumb", "View thumbnail"),
            BotCommand("delthumb", "Delete thumbnail"),
            BotCommand("set_caption", "Set custom caption"),
            BotCommand("see_caption", "View caption"),
            BotCommand("del_caption", "Delete caption"),
            BotCommand("setmedia", "Set output file type"),
            BotCommand("start_sequence", "Start file sequencing"),
            BotCommand("end_sequence", "End file sequencing"),
            BotCommand("metadata", "View metadata"),
            BotCommand("ping", "Check bot ping"),
            BotCommand("donate", "Support developer"),
            BotCommand("set_prefix", "Set prefix"),
            BotCommand("see_prefix", "View prefix"),
            BotCommand("del_prefix", "Delete prefix"),
            BotCommand("set_suffix", "Set suffix"),
            BotCommand("see_suffix", "View suffix"),
            BotCommand("del_suffix", "Delete suffix"),
        ]

        await client.set_bot_commands(commands)

        me = await client.get_me()
        logger.info(f"🤖 Bot started as {me.first_name} (@{me.username})")
        logger.info("✅ BOT IS LIVE & STABLE")

    except Exception as e:
        logger.exception("Startup failed")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    logger.info("🚀 Starting bot using app.run()")
    app.run()
