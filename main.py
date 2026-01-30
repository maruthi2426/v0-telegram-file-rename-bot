import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not all([API_ID, API_HASH, BOT_TOKEN, DATABASE_URL]):
    logger.error("Missing required environment variables: API_ID, API_HASH, BOT_TOKEN, DATABASE_URL")
    sys.exit(1)

# Initialize Pyrogram Client
try:
    app = Client(
        name="FileRenameBot",
        api_id=int(API_ID),
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    logger.info("Pyrogram Client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Pyrogram Client: {e}")
    sys.exit(1)

# Import handlers to register them with the client
# This MUST be done after app is created but before app.run()
try:
    from handlers import (
        start_handler,
        rename_handler,
        thumbnail_handler,
        caption_handler,
        admin_handler,
        user_handler,
        metadata_handler
    )
    logger.info("✅ All handlers imported and registered successfully")
except Exception as e:
    logger.error(f"Failed to import handlers: {e}")
    sys.exit(1)

# Main entry point
if __name__ == "__main__":
    try:
        logger.info("🚀 Starting File Rename Bot...")
        app.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}", exc_info=True)
        sys.exit(1)
