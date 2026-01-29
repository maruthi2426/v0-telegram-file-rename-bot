import logging
import os
from pyrogram import Client
from dotenv import load_dotenv

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

if not all([API_ID, API_HASH, BOT_TOKEN]):
    log.error("❌ Missing API_ID / API_HASH / BOT_TOKEN")
    exit(1)

# ---------------- CLIENT ----------------
app = Client(
    "FileRenameBot",   # session name (STRING ONLY)
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- IMPORT HANDLERS ----------------
# IMPORTANT: importing registers handlers
import handlers.start
import handlers.rename
import handlers.thumbnail
import handlers.caption
import handlers.admin
import handlers.user
import handlers.metadata

# ---------------- MAIN ----------------
if __name__ == "__main__":
    log.info("🚀 Starting bot using app.run()")
    app.run()
