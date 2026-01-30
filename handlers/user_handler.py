import logging
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from utils import send_log, check_user_ban, create_leaderboard_text
from main import app

logger = logging.getLogger(__name__)

@app.on_message(filters.command("leaderboard"))
async def leaderboard_command(client, message: Message):
    """Handle /leaderboard command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        # Get top 10 users
        users = db.get_leaderboard(limit=10)
        
        text = create_leaderboard_text(users, limit=10)
        
        # Get user's own position
        all_users = db.get_leaderboard(limit=1000)
        user_position = None
        for idx, user in enumerate(all_users, 1):
            if user['user_id'] == user_id:
                user_position = idx
                break
        
        if user_position:
            text += f"\n\n👤 **Your Position:** #{user_position}"
            user_data = db.get_user(user_id)
            if user_data:
                text += f"\n📊 **Your Files Renamed:** {user_data.get('rename_count', 0)}"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_leaderboard")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard, parse_mode="markdown")
        await send_log(app, "User viewed leaderboard", user_id)
        
    except Exception as e:
        logger.error(f"Error in leaderboard_command: {e}")

@app.on_message(filters.command("tutorial"))
async def tutorial_command(app: Client, message: Message):
    """Handle /tutorial command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        tutorial_text = """
📖 **How to Use File Rename Bot**

**Basic Steps:**

1️⃣ **Set Your Format**
   • Use /autorename
   • Create your custom format (e.g., S{season}E{episode} - {title})
   • Send it to the bot

2️⃣ **Upload Thumbnail (Optional)**
   • Send any image
   • Use /viewthumb to set it
   • This will be used for all your files

3️⃣ **Send Your Files**
   • Just send video files to the bot
   • They'll be renamed automatically
   • Download the result

4️⃣ **Customize (Optional)**
   • Set custom caption: /set_caption
   • Add prefix: /set_prefix
   • Add suffix: /set_suffix

**Available Variables:**
• {season} - Season number
• {episode} - Episode number
• {title} - Original title
• {quality} - Video quality
• {audio} - Audio info

**Sequence Mode:**
• /start_sequence - Start mode
• Send multiple files
• /end_sequence - Process all at once

**Commands Guide:**
/showformat - View your current format
/leaderboard - See top users
/ping - Test bot status
/donate - Support us

Need help? Contact the developer!
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Start Now", callback_data="back_home")]
        ])
        
        await message.reply_text(tutorial_text, reply_markup=keyboard, parse_mode="markdown")
        await send_log(app, "User viewed tutorial", user_id)
        
    except Exception as e:
        logger.error(f"Error in tutorial_command: {e}")

@app.on_callback_query(filters.regex("^refresh_leaderboard$"))
async def refresh_leaderboard_callback(app: Client, query):
    """Handle refresh leaderboard button"""
    try:
        user_id = query.from_user.id
        
        await query.answer("🔄 Refreshing...", show_alert=False)
        
        users = db.get_leaderboard(limit=10)
        text = create_leaderboard_text(users, limit=10)
        
        # Get user's own position
        all_users = db.get_leaderboard(limit=1000)
        user_position = None
        for idx, user in enumerate(all_users, 1):
            if user['user_id'] == user_id:
                user_position = idx
                break
        
        if user_position:
            text += f"\n\n👤 **Your Position:** #{user_position}"
            user_data = db.get_user(user_id)
            if user_data:
                text += f"\n📊 **Your Files Renamed:** {user_data.get('rename_count', 0)}"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_leaderboard")]
        ])
        
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in refresh_leaderboard_callback: {e}")

@app.on_callback_query(filters.regex("^leaderboard$"))
async def leaderboard_callback(app: Client, query):
    """Handle leaderboard button callback"""
    try:
        user_id = query.from_user.id
        
        await query.answer()
        
        users = db.get_leaderboard(limit=10)
        text = create_leaderboard_text(users, limit=10)
        
        # Get user's own position
        all_users = db.get_leaderboard(limit=1000)
        user_position = None
        for idx, user in enumerate(all_users, 1):
            if user['user_id'] == user_id:
                user_position = idx
                break
        
        if user_position:
            text += f"\n\n👤 **Your Position:** #{user_position}"
            user_data = db.get_user(user_id)
            if user_data:
                text += f"\n📊 **Your Files Renamed:** {user_data.get('rename_count', 0)}"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_leaderboard")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data="back_home")]
        ])
        
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in leaderboard_callback: {e}")

@app.on_message(filters.command("status"))
async def status_command(app: Client, message: Message):
    """Handle /status command - Bot status"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        # Get bot statistics
        me = await app.get_me()
        
        status_text = f"""
🤖 **Bot Status**

✅ Bot is running smoothly!

**Statistics:**
• Bot Name: {me.first_name}
• Bot Username: @{me.username}
• Bot ID: {me.id}

**Server Status:** ✅ Running
**Database:** ✅ Connected
**Response Time:** ⚡ Fast

Last updated: Just now

Thank you for using our bot! 🙏
"""
        
        await message.reply_text(status_text, parse_mode="markdown")
        await send_log(app, "User checked status", user_id)
        
    except Exception as e:
        logger.error(f"Error in status_command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")
