import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import os

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

# ---------------- CLIENT ----------------
app = Client(
    "mergebot",          # SESSION NAME (STRING ONLY)
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- HANDLERS ----------------
@app.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply_text(
        "👋 Hello!\n\n🤖 Bot is ONLINE & WORKING ✅"
    )

# ---------------- MAIN ----------------
if __name__ == "__main__":
    log.info("🚀 Starting bot using app.run()")
    app.run()
