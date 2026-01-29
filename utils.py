import os
import re
import logging
from datetime import datetime
from pyrogram import Client
from pyrogram.types import Message
from config import OWNER_ID, LOG_CHANNEL
from database import db

logger = logging.getLogger(__name__)

async def send_log(app: Client, message: str, user_id: int = None):
    """Send a log message to log channel"""
    try:
        if LOG_CHANNEL:
            text = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n{message}"
            if user_id:
                text += f"\n\nUser ID: {user_id}"
            await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        logger.error(f"Error sending log: {e}")

async def is_admin(app: Client, user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == OWNER_ID or db.is_admin(user_id)

async def check_user_ban(user_id: int) -> bool:
    """Check if user is banned"""
    return db.is_user_banned(user_id)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be safe for file system"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple spaces
    filename = re.sub(r'\s+', ' ', filename)
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    return name + ext

def parse_rename_format(format_string: str, **kwargs) -> str:
    """Parse rename format with variables"""
    result = format_string
    
    # Replace variables
    replacements = {
        '{season}': str(kwargs.get('season', '')),
        '{episode}': str(kwargs.get('episode', '')),
        '{title}': str(kwargs.get('title', '')),
        '{quality}': str(kwargs.get('quality', '')),
        '{audio}': str(kwargs.get('audio', '')),
    }
    
    for key, value in replacements.items():
        result = result.replace(key, value)
    
    return sanitize_filename(result)

def get_file_extension(filename: str) -> str:
    """Get file extension"""
    _, ext = os.path.splitext(filename)
    return ext.lower()

def format_bytes(bytes_size: int) -> str:
    """Format bytes to readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def format_seconds(seconds: int) -> str:
    """Format seconds to readable time"""
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(secs)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(secs)}s"
    else:
        return f"{int(secs)}s"

def generate_thumbnail_filename(user_id: int) -> str:
    """Generate unique thumbnail filename"""
    return f"thumb_{user_id}.jpg"

def validate_token(token: str) -> bool:
    """Validate if string looks like a valid token"""
    return len(token) > 20

async def delete_file(file_path: str):
    """Safely delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")

def get_file_info(file_path: str) -> dict:
    """Get file information"""
    try:
        stat_info = os.stat(file_path)
        return {
            'size': stat_info.st_size,
            'created': datetime.fromtimestamp(stat_info.st_ctime),
            'modified': datetime.fromtimestamp(stat_info.st_mtime),
            'name': os.path.basename(file_path)
        }
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return {}

def split_text(text: str, max_length: int = 4096) -> list:
    """Split text into chunks to fit Telegram limit"""
    chunks = []
    current_chunk = ""
    
    lines = text.split('\n')
    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += '\n' + line if current_chunk else line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks if chunks else [text]

def create_leaderboard_text(users: list, limit: int = 10) -> str:
    """Create leaderboard text"""
    if not users:
        return "📊 No users yet!"
    
    text = "🏆 **File Rename Leaderboard**\n\n"
    medals = ['🥇', '🥈', '🥉']
    
    for idx, user in enumerate(users[:limit], 1):
        medal = medals[idx-1] if idx <= 3 else f"{idx}."
        username = user.get('username', 'Unknown')
        count = user.get('rename_count', 0)
        text += f"{medal} {username} - {count} files\n"
    
    return text

def create_status_text(stats: dict) -> str:
    """Create status text"""
    text = "🤖 **Bot Status**\n\n"
    for key, value in stats.items():
        text += f"• {key}: {value}\n"
    return text
