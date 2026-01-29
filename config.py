import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API Configuration
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Database Configuration
DB_URL = os.getenv("DB_URL", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "file_rename_bot")

# Admin Configuration
OWNER_ID = int(os.getenv("OWNER_ID", 0))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 0))

# Optional Settings
FORCE_SUBS = os.getenv("FORCE_SUBS", "").split(',') if os.getenv("FORCE_SUBS") else []
START_PIC = os.getenv("START_PIC", "")

# Bot Settings
MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2GB
ALLOWED_EXTENSIONS = ['.mkv', '.mp4', '.avi', '.mov', '.webm', '.flv', '.m4v']
THUMBNAIL_WIDTH = 320
THUMBNAIL_HEIGHT = 180

# Messages
START_MESSAGE = """
✨ **Welcome to File Rename Bot!** ✨

This bot helps you rename files with custom formats and add thumbnails.

**Features:**
• ⚡ Fast file renaming
• 🖼️ Custom thumbnail support
• 📝 Custom captions
• 📊 Leaderboard system
• 🔐 Force subscribe
• ⚙️ Dynamic configuration

**Use /tutorial to learn more!**
"""

HELP_MESSAGE = """
📚 **Available Commands:**

**User Commands:**
/start - Start the bot
/autorename - Set auto rename format
/showformat - View your format
/tutorial - Usage guide
/leaderboard - View leaderboard
/viewthumb - View thumbnail
/delthumb - Delete thumbnail
/set_caption - Set custom caption
/see_caption - View caption
/del_caption - Delete caption
/setmedia - Set output file type
/start_sequence - Start sequencing
/end_sequence - End sequencing
/metadata - View metadata
/ping - Check bot ping
/donate - Support developer

**Prefix/Suffix:**
/set_prefix - Set prefix
/see_prefix - View prefix
/del_prefix - Delete prefix
/set_suffix - Set suffix
/see_suffix - View suffix
/del_suffix - Delete suffix

**Admin Commands:**
/verify_settings - Change verify settings
/fsub_mode - See force sub mode
/addchnl - Add force sub channel
/delchnl - Remove force sub channel
/listchnl - View all channels
/add_admin - Add new admin
/deladmin - Remove admin
/admins - List all admins
/restart - Restart bot
/broadcast - Broadcast message
/status - Check bot status
/ban - Ban a user
/unban - Unban a user
/banned - Show banned users
"""

TUTORIAL_MESSAGE = """
📖 **How to Use File Rename Bot**

**Basic Steps:**
1. Send your video file to the bot
2. The bot will rename it according to your format
3. Download the renamed file

**Setting Format:**
Use /autorename to set your custom format.
Example: S{season}E{episode} - {title}

**Thumbnails:**
1. Send an image with /viewthumb
2. This image will be used as thumbnail for your files

**Custom Caption:**
Use /set_caption to add a custom caption to files.

**Sequence Mode:**
1. Use /start_sequence
2. Send multiple files
3. Use /end_sequence when done
4. All files will be sent back in order

**Need help?** Contact the developer!
"""
