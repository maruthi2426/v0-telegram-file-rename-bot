import logging
import os
import sys
from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.types import Message, BotCommand
import asyncio
import signal

# Load environment variables
load_dotenv()

# Configure logging with more detail for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import Render configuration
from render_config import RenderConfig

# Validate required environment variables
if not RenderConfig.validate_environment():
    logger.error("Environment validation failed. Cannot start bot.")
    sys.exit(1)

# Print startup info
RenderConfig.print_startup_info()

# Initialize Pyrogram Client with session name including timestamp to avoid conflicts
app = Client(
    name="FileRenameBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    workdir="sessions"  # Ensure sessions are stored in a writable directory
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
        
        # Initialize and verify database connection first
        from database import Database
        db = Database()
        
        if not db.connect():
            logger.error("Failed to connect to database. Exiting.")
            sys.exit(1)
        
        logger.info("Database connected successfully")
        
        # Now start the bot
        await app.start()
        logger.info("Bot client started successfully")
        
        # Set commands
        await set_commands()
        
        # Get bot info
        me = await app.get_me()
        logger.info(f"Bot name: {me.first_name} (@{me.username})")
        logger.info(f"Bot ID: {me.id}")
        
        # Log that bot is ready
        logger.info("=" * 50)
        logger.info("BOT IS RUNNING AND READY")
        logger.info("=" * 50)
        
        # Idle to keep bot running
        await idle()
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        try:
            logger.info("Shutting down bot...")
            if 'db' in locals():
                db.disconnect()
            await app.stop()
            logger.info("Bot stopped successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

def handle_signal(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)

if __name__ == "__main__":
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
