import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# ---------------- ENV CHECK ----------------
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    log.error("❌ Missing API_ID / API_HASH / BOT_TOKEN")
    sys.exit(1)

# ---------------- CLIENT ----------------
app = Client(
    "FileRenameBot",   # SESSION NAME (STRING ONLY)
    api_id=int(API_ID),
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

# ---------------- COMMAND SETUP ----------------
async def setup_commands():
    await app.set_bot_commands([
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
        BotCommand("metadata", "View metadata"),
        BotCommand("ping", "Check bot ping"),
    ])

# ---------------- MAIN ----------------
if __name__ == "__main__":
    log.info("🚀 Starting bot using app.run()")

    async def runner():
        await setup_commands()
        me = await app.get_me()
        log.info(f"🤖 Bot started as {me.first_name} (@{me.username})")
        log.info("✅ BOT IS LIVE & STABLE")

    app.run(runner)
