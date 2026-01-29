import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# ---------------- CONFIG ----------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not API_HASH or not BOT_TOKEN:
    log.error("❌ Missing API credentials")
    sys.exit(1)

# ---------------- CLIENT ----------------
app = Client(
    "FileRenameBot",
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

# ---------------- START HANDLER (TEST) ----------------
@app.on_message(filters.command("start"))
async def start_test(_, message: Message):
    await message.reply_text("✅ Bot is ONLINE & WORKING")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    log.info("🚀 Starting bot using app.run()")
    app.run()
