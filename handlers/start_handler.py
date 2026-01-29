import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import START_MESSAGE, HELP_MESSAGE
from main import app
from database import db
from utils import send_log, is_admin, check_user_ban

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start"))
async def start_command(app: Client, message: Message):
    """Handle /start command"""
    try:
        user_id = message.from_user.id
        
        # Check if user is banned
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned from using this bot!")
            return
        
        # Add user to database
        db.add_user(user_id, message.from_user.username, message.from_user.first_name)
        
        # Create inline keyboard
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📚 Help", callback_data="help"),
                InlineKeyboardButton("📖 Tutorial", callback_data="tutorial")
            ],
            [
                InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard"),
                InlineKeyboardButton("❓ About", callback_data="about")
            ]
        ])
        
        await message.reply_text(
            START_MESSAGE,
            reply_markup=keyboard,
            parse_mode="markdown"
        )
        
        await send_log(app, f"New user started the bot: {message.from_user.first_name} (@{message.from_user.username})", user_id)
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await message.reply_text("❌ An error occurred. Please try again.")

@Client.on_message(filters.command("help"))
async def help_command(app: Client, message: Message):
    """Handle /help command"""
    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Home", callback_data="back_home")]
        ])
        
        await message.reply_text(
            HELP_MESSAGE,
            reply_markup=keyboard,
            parse_mode="markdown"
        )
    except Exception as e:
        logger.error(f"Error in help_command: {e}")

@Client.on_message(filters.command("ping"))
async def ping_command(app: Client, message: Message):
    """Handle /ping command"""
    try:
        await message.reply_text("🏓 Pong! Bot is running smoothly!")
    except Exception as e:
        logger.error(f"Error in ping_command: {e}")

@Client.on_message(filters.command("donate"))
async def donate_command(app: Client, message: Message):
    """Handle /donate command"""
    try:
        donate_text = """
💝 **Support the Developer**

If you find this bot useful, please consider supporting the development:

📧 Contact: @dev_username
💳 UPI: your_upi@bank
🎁 You get priority support and custom features!

Thank you for your support! 🙏
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Contact Developer", callback_data="contact_dev")]
        ])
        
        await message.reply_text(donate_text, reply_markup=keyboard, parse_mode="markdown")
    except Exception as e:
        logger.error(f"Error in donate_command: {e}")

# Callback handlers for inline buttons
@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(app: Client, query):
    """Handle help button callback"""
    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Home", callback_data="back_home")]
        ])
        
        await query.edit_message_text(
            HELP_MESSAGE,
            reply_markup=keyboard,
            parse_mode="markdown"
        )
    except Exception as e:
        logger.error(f"Error in help_callback: {e}")

@Client.on_callback_query(filters.regex("^tutorial$"))
async def tutorial_callback(app: Client, query):
    """Handle tutorial button callback"""
    try:
        tutorial_text = """
📖 **File Rename Bot Tutorial**

**Step 1: Set Your Format**
Send the command /autorename and enter your custom format.

Example: `S{season}E{episode} - {title}`

**Step 2: Set Thumbnail (Optional)**
Send any image, then use /set_thumbnail to set it.

**Step 3: Send Your File**
Send a video file and the bot will rename it according to your format.

**Step 4: Download**
Download the renamed file from the bot.

**Variables You Can Use:**
- {season} - Season number
- {episode} - Episode number
- {title} - File title
- {quality} - Video quality
- {audio} - Audio information

**Need more help?** Contact @dev_username
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Home", callback_data="back_home")]
        ])
        
        await query.edit_message_text(
            tutorial_text,
            reply_markup=keyboard,
            parse_mode="markdown"
        )
    except Exception as e:
        logger.error(f"Error in tutorial_callback: {e}")

@Client.on_callback_query(filters.regex("^back_home$"))
async def back_home_callback(app: Client, query):
    """Handle back to home button callback"""
    try:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📚 Help", callback_data="help"),
                InlineKeyboardButton("📖 Tutorial", callback_data="tutorial")
            ],
            [
                InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard"),
                InlineKeyboardButton("❓ About", callback_data="about")
            ]
        ])
        
        await query.edit_message_text(
            START_MESSAGE,
            reply_markup=keyboard,
            parse_mode="markdown"
        )
    except Exception as e:
        logger.error(f"Error in back_home_callback: {e}")

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(app: Client, query):
    """Handle about button callback"""
    try:
        about_text = """
ℹ️ **About This Bot**

**File Rename & Thumbnail Bot**

A powerful Telegram bot for renaming video files with custom formats and adding thumbnails.

**Features:**
✨ Auto-rename with custom formats
🖼️ Thumbnail support
📝 Custom captions
🏆 Leaderboard system
🔐 Force subscribe
⚙️ Admin controls
🚀 Lightning fast processing

**Version:** 1.0.0
**Developed by:** Your Name
**Support:** @dev_username

Thank you for using our bot! 🙏
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Home", callback_data="back_home")]
        ])
        
        await query.edit_message_text(
            about_text,
            reply_markup=keyboard,
            parse_mode="markdown"
        )
    except Exception as e:
        logger.error(f"Error in about_callback: {e}")
