import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.storage import MemoryStorage
from pyrogram.types import Message, BotCommand
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Validate environment variables
required_vars = ["API_ID", "API_HASH", "BOT_TOKEN", "DATABASE_URL"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# Initialize Pyrogram Client with MemoryStorage for cloud deployment
app = Client(
    name="FileRenameBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    storage=MemoryStorage(name="FileRenameBot")
)

# Import handlers
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
    """Set bot commands for UI"""
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
    
    try:
        await app.set_bot_commands(commands)
        logger.info("Bot commands set successfully")
    except Exception as e:
        logger.error(f"Error setting commands: {e}")

async def main():
    """Start the bot"""
    try:
        logger.info("Starting bot...")
        await app.start()
        logger.info("Bot client started successfully")
        
        # Set commands
        await set_commands()
        
        # Get bot info
        me = await app.get_me()
        logger.info(f"Bot is live: {me.first_name} (@{me.username}) - ID: {me.id}")
        logger.info("=" * 60)
        logger.info("BOT IS RUNNING AND READY FOR COMMANDS")
        logger.info("=" * 60)
        
        # Idle to keep bot running
        await idle()
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        try:
            await app.stop()
            logger.info("Bot stopped gracefully")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
