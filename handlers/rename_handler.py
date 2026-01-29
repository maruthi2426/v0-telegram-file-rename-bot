import logging
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from utils import (
    parse_rename_format, sanitize_filename, get_file_extension,
    send_log, check_user_ban
)

logger = logging.getLogger(__name__)

# Store rename formats in memory temporarily
rename_formats = {}

@Client.on_message(filters.command("autorename"))
async def autorename_command(app: Client, message: Message):
    """Handle /autorename command - Set custom rename format"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        help_text = """
📝 **Set Your Auto-Rename Format**

Use these variables in your format:
• {season} - Season number
• {episode} - Episode number
• {title} - File title
• {quality} - Video quality
• {audio} - Audio type

**Examples:**
`S{season}E{episode} - {title}`
`{title} ({quality})`
`{title} [{audio}]`

Send your desired format as a message.
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_format")]
        ])
        
        msg = await message.reply_text(help_text, reply_markup=keyboard, parse_mode="markdown")
        rename_formats[user_id] = {"state": "waiting_format", "msg_id": msg.id}
        
    except Exception as e:
        logger.error(f"Error in autorename_command: {e}")
        await message.reply_text("❌ Error occurred!")

@Client.on_message(filters.command("showformat"))
async def showformat_command(app: Client, message: Message):
    """Handle /showformat command - Show current rename format"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        format_str = db.get_rename_format(user_id)
        
        if format_str:
            text = f"📝 **Your Current Format:**\n`{format_str}`"
        else:
            text = "❌ You haven't set a format yet!\n\nUse /autorename to set one."
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Change Format", callback_data="change_format")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in showformat_command: {e}")

@Client.on_message(filters.command("setmedia"))
async def setmedia_command(app: Client, message: Message):
    """Handle /setmedia command - Set output file type"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("MP4", callback_data="media_mp4"),
                InlineKeyboardButton("MKV", callback_data="media_mkv")
            ],
            [
                InlineKeyboardButton("AVI", callback_data="media_avi"),
                InlineKeyboardButton("WebM", callback_data="media_webm")
            ]
        ])
        
        await message.reply_text(
            "🎬 **Select Output Format:**",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Error in setmedia_command: {e}")

@Client.on_message(filters.command("start_sequence"))
async def start_sequence_command(app: Client, message: Message):
    """Handle /start_sequence command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        db.start_sequence(user_id)
        await message.reply_text(
            "✅ **Sequence Mode Started!**\n\nNow send multiple files. I'll rename them in order.\nUse /end_sequence when done.",
            parse_mode="markdown"
        )
        await send_log(app, f"User started sequence mode", user_id)
        
    except Exception as e:
        logger.error(f"Error in start_sequence_command: {e}")

@Client.on_message(filters.command("end_sequence"))
async def end_sequence_command(app: Client, message: Message):
    """Handle /end_sequence command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        files = db.end_sequence(user_id)
        
        if files:
            text = f"✅ Sequence Ended!\n\n📊 Total files processed: {len(files)}"
            await message.reply_text(text)
            await send_log(app, f"User ended sequence with {len(files)} files", user_id)
        else:
            await message.reply_text("❌ No files in sequence!")
        
    except Exception as e:
        logger.error(f"Error in end_sequence_command: {e}")

# Handle file rename when user sends file
@Client.on_message(filters.document | filters.video)
async def handle_file_rename(app: Client, message: Message):
    """Handle file rename when user sends a file"""
    try:
        user_id = message.from_user.id
        
        # Check if user is banned
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        # Check if user is waiting for format input
        if user_id in rename_formats and rename_formats[user_id]["state"] == "waiting_format":
            # Process format input
            format_text = message.text
            if format_text:
                db.set_rename_format(user_id, format_text)
                await message.reply_text(f"✅ Format saved: `{format_text}`", parse_mode="markdown")
                del rename_formats[user_id]
                return
        
        # Get file info
        file = message.document or message.video
        original_name = file.file_name or "unnamed"
        file_size = file.file_size
        
        # Show processing message
        processing_msg = await message.reply_text("⏳ Processing your file...")
        
        # Get user's rename format
        format_str = db.get_rename_format(user_id)
        
        if not format_str:
            await processing_msg.delete()
            await message.reply_text("❌ You haven't set a rename format!\n\nUse /autorename first.")
            return
        
        # Apply prefix and suffix if set
        prefix = db.get_prefix(user_id) or ""
        suffix = db.get_suffix(user_id) or ""
        
        # Parse the format
        name, ext = os.path.splitext(original_name)
        new_name = parse_rename_format(format_str, title=name, quality="720p", audio="AAC")
        new_name = prefix + new_name + suffix + ext
        new_name = sanitize_filename(new_name)
        
        # Increment user's rename count
        db.increment_rename_count(user_id)
        
        # Send the file with new name
        await app.send_document(
            chat_id=user_id,
            document=file.file_id,
            file_name=new_name,
            caption=f"✅ **Renamed!**\n📁 {new_name}\n📊 Size: {file_size / (1024*1024):.2f} MB",
            parse_mode="markdown"
        )
        
        await processing_msg.delete()
        await send_log(app, f"File renamed: {original_name} → {new_name}", user_id)
        
    except Exception as e:
        logger.error(f"Error in handle_file_rename: {e}")
        await message.reply_text(f"❌ Error processing file: {str(e)}")

# Callback handlers
@Client.on_callback_query(filters.regex("^cancel_format$"))
async def cancel_format_callback(app: Client, query):
    """Handle cancel format button"""
    try:
        user_id = query.from_user.id
        if user_id in rename_formats:
            del rename_formats[user_id]
        
        await query.edit_message_text("❌ Cancelled!")
    except Exception as e:
        logger.error(f"Error in cancel_format_callback: {e}")

@Client.on_callback_query(filters.regex("^media_"))
async def media_callback(app: Client, query):
    """Handle media format selection"""
    try:
        format_type = query.data.replace("media_", "")
        user_id = query.from_user.id
        
        # Store user's preferred media format
        db.set_metadata(user_id, title=f"media_format_{format_type}")
        
        await query.edit_message_text(f"✅ Output format set to: **.{format_type.upper()}**", parse_mode="markdown")
        await send_log(app, f"User set output format to {format_type}", user_id)
        
    except Exception as e:
        logger.error(f"Error in media_callback: {e}")
