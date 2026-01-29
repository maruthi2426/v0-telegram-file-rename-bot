import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from utils import send_log, check_user_ban

logger = logging.getLogger(__name__)

# Store thumbnail request states
thumbnail_states = {}

@Client.on_message(filters.command("viewthumb"))
async def viewthumb_command(app: Client, message: Message):
    """Handle /viewthumb command - View current thumbnail"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        thumb = db.get_thumbnail(user_id)
        
        if thumb:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change", callback_data="change_thumb")],
                [InlineKeyboardButton("🗑️ Delete", callback_data="delete_thumb")]
            ])
            
            await app.send_photo(
                chat_id=user_id,
                photo=thumb['file_id'],
                caption="🖼️ **Your Current Thumbnail**",
                reply_markup=keyboard,
                parse_mode="markdown"
            )
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬆️ Upload Thumbnail", callback_data="upload_thumb")]
            ])
            
            await message.reply_text(
                "❌ You haven't set a thumbnail yet!",
                reply_markup=keyboard
            )
        
    except Exception as e:
        logger.error(f"Error in viewthumb_command: {e}")
        await message.reply_text("❌ Error occurred!")

@Client.on_message(filters.command("delthumb"))
async def delthumb_command(app: Client, message: Message):
    """Handle /delthumb command - Delete thumbnail"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        thumb = db.get_thumbnail(user_id)
        
        if thumb:
            db.delete_thumbnail(user_id)
            await message.reply_text("✅ Thumbnail deleted successfully!")
            await send_log(app, "User deleted thumbnail", user_id)
        else:
            await message.reply_text("❌ You don't have a thumbnail to delete!")
        
    except Exception as e:
        logger.error(f"Error in delthumb_command: {e}")

# Handle photo upload for thumbnail
@Client.on_message(filters.photo, group=1)
async def handle_thumbnail_upload(app: Client, message: Message):
    """Handle thumbnail upload"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        # Check if user is requesting to set thumbnail
        if user_id in thumbnail_states and thumbnail_states[user_id].get("action") == "waiting_thumb":
            photo = message.photo[-1]  # Get highest quality photo
            
            # Save thumbnail
            db.set_thumbnail(user_id, photo.file_id, photo.file_unique_id)
            
            await message.reply_text(
                "✅ Thumbnail saved successfully!\n\n📁 This image will be used for all your renamed files.",
                parse_mode="markdown"
            )
            
            del thumbnail_states[user_id]
            await send_log(app, "User set thumbnail", user_id)
        
    except Exception as e:
        logger.error(f"Error in handle_thumbnail_upload: {e}")

# Callback handlers
@Client.on_callback_query(filters.regex("^upload_thumb$"))
async def upload_thumb_callback(app: Client, query):
    """Handle upload thumbnail button"""
    try:
        user_id = query.from_user.id
        
        msg = await query.answer()
        await app.send_message(
            chat_id=user_id,
            text="📸 **Send a Photo for Thumbnail**\n\nSend any image and I'll use it as your thumbnail for all renamed files.\n\nRecommended: 320x180 pixels or similar aspect ratio",
            parse_mode="markdown"
        )
        
        thumbnail_states[user_id] = {"action": "waiting_thumb"}
        
    except Exception as e:
        logger.error(f"Error in upload_thumb_callback: {e}")

@Client.on_callback_query(filters.regex("^change_thumb$"))
async def change_thumb_callback(app: Client, query):
    """Handle change thumbnail button"""
    try:
        user_id = query.from_user.id
        
        await query.answer()
        await app.send_message(
            chat_id=user_id,
            text="📸 **Send a New Photo for Thumbnail**\n\nThe old thumbnail will be replaced.",
            parse_mode="markdown"
        )
        
        thumbnail_states[user_id] = {"action": "waiting_thumb"}
        
    except Exception as e:
        logger.error(f"Error in change_thumb_callback: {e}")

@Client.on_callback_query(filters.regex("^delete_thumb$"))
async def delete_thumb_callback(app: Client, query):
    """Handle delete thumbnail button"""
    try:
        user_id = query.from_user.id
        
        db.delete_thumbnail(user_id)
        
        await query.edit_message_caption(
            caption="✅ Thumbnail deleted successfully!"
        )
        
        await send_log(app, "User deleted thumbnail via callback", user_id)
        
    except Exception as e:
        logger.error(f"Error in delete_thumb_callback: {e}")
