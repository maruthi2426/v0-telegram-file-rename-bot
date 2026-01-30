import logging
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from utils import send_log, check_user_ban
from main import app

logger = logging.getLogger(__name__)

# Store metadata states
metadata_states = {}

@app.on_message(filters.command("metadata"))
async def metadata_command(client, message: Message):
    """Handle /metadata command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        metadata = db.get_metadata(user_id)
        
        if metadata:
            text = "📊 **Your Current Metadata**\n\n"
            text += f"• Title: {metadata.get('title', 'Not set')}\n"
            text += f"• Author: {metadata.get('author', 'Not set')}\n"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✏️ Title", callback_data="edit_title"),
                    InlineKeyboardButton("✏️ Author", callback_data="edit_author")
                ],
                [InlineKeyboardButton("🗑️ Clear All", callback_data="clear_metadata")]
            ])
        else:
            text = "❌ No metadata set yet!\n\nUse buttons below to add metadata:"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("➕ Add Title", callback_data="add_title"),
                    InlineKeyboardButton("➕ Add Author", callback_data="add_author")
                ]
            ])
        
        await message.reply_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in metadata_command: {e}")

@app.on_message(filters.command("set_prefix"))
async def set_prefix_command(client, message: Message):
    """Handle /set_prefix command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        help_text = """
📝 **Set Your Prefix**

Send the prefix you want to add at the beginning of every renamed file.

Example: If you set prefix as `[HD]` and file is `movie.mp4`
Result: `[HD]movie.mp4`

Send your prefix:
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_prefix")]
        ])
        
        await message.reply_text(help_text, reply_markup=keyboard, parse_mode="markdown")
        metadata_states[user_id] = {"state": "waiting_prefix"}
        
    except Exception as e:
        logger.error(f"Error in set_prefix_command: {e}")

@app.on_message(filters.command("see_prefix"))
async def see_prefix_command(client, message: Message):
    """Handle /see_prefix command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        prefix = db.get_prefix(user_id)
        
        if prefix:
            text = f"📝 **Your Current Prefix:**\n`{prefix}`"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change", callback_data="change_prefix")],
                [InlineKeyboardButton("🗑️ Delete", callback_data="del_prefix")]
            ])
            
            await message.reply_text(text, reply_markup=keyboard, parse_mode="markdown")
        else:
            await message.reply_text("❌ You haven't set a prefix yet!\n\nUse /set_prefix to set one.")
        
    except Exception as e:
        logger.error(f"Error in see_prefix_command: {e}")

@app.on_message(filters.command("del_prefix"))
async def del_prefix_command(client, message: Message):
    """Handle /del_prefix command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        db.delete_prefix(user_id)
        await message.reply_text("✅ Prefix deleted successfully!")
        await send_log(app, "User deleted prefix", user_id)
        
    except Exception as e:
        logger.error(f"Error in del_prefix_command: {e}")

@app.on_message(filters.command("set_suffix"))
async def set_suffix_command(client, message: Message):
    """Handle /set_suffix command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        help_text = """
📝 **Set Your Suffix**

Send the suffix you want to add at the end of the filename (before extension).

Example: If you set suffix as `[1080p]` and file is `movie.mp4`
Result: `movie[1080p].mp4`

Send your suffix:
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_suffix")]
        ])
        
        await message.reply_text(help_text, reply_markup=keyboard, parse_mode="markdown")
        metadata_states[user_id] = {"state": "waiting_suffix"}
        
    except Exception as e:
        logger.error(f"Error in set_suffix_command: {e}")

@app.on_message(filters.command("see_suffix"))
async def see_suffix_command(client, message: Message):
    """Handle /see_suffix command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        suffix = db.get_suffix(user_id)
        
        if suffix:
            text = f"📝 **Your Current Suffix:**\n`{suffix}`"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change", callback_data="change_suffix")],
                [InlineKeyboardButton("🗑️ Delete", callback_data="del_suffix")]
            ])
            
            await message.reply_text(text, reply_markup=keyboard, parse_mode="markdown")
        else:
            await message.reply_text("❌ You haven't set a suffix yet!\n\nUse /set_suffix to set one.")
        
    except Exception as e:
        logger.error(f"Error in see_suffix_command: {e}")

@app.on_message(filters.command("del_suffix"))
async def del_suffix_command(client, message: Message):
    """Handle /del_suffix command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        db.delete_suffix(user_id)
        await message.reply_text("✅ Suffix deleted successfully!")
        await send_log(app, "User deleted suffix", user_id)
        
    except Exception as e:
        logger.error(f"Error in del_suffix_command: {e}")

# Handle text input for metadata
@app.on_message(filters.text & filters.private, group=3)
async def handle_metadata_input(client, message: Message):
    """Handle metadata text input"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            return
        
        if user_id in metadata_states:
            state = metadata_states[user_id]["state"]
            text = message.text
            
            if state == "waiting_prefix":
                db.set_prefix(user_id, text)
                await message.reply_text(f"✅ Prefix saved: `{text}`", parse_mode="markdown")
                await send_log(app, f"User set prefix: {text}", user_id)
                del metadata_states[user_id]
                
            elif state == "waiting_suffix":
                db.set_suffix(user_id, text)
                await message.reply_text(f"✅ Suffix saved: `{text}`", parse_mode="markdown")
                await send_log(app, f"User set suffix: {text}", user_id)
                del metadata_states[user_id]
                
            elif state == "waiting_title":
                db.set_metadata(user_id, title=text)
                await message.reply_text(f"✅ Title saved: `{text}`", parse_mode="markdown")
                await send_log(app, f"User set title: {text}", user_id)
                del metadata_states[user_id]
                
            elif state == "waiting_author":
                db.set_metadata(user_id, author=text)
                await message.reply_text(f"✅ Author saved: `{text}`", parse_mode="markdown")
                await send_log(app, f"User set author: {text}", user_id)
                del metadata_states[user_id]
    
    except Exception as e:
        logger.error(f"Error in handle_metadata_input: {e}")

# Callback handlers
@app.on_callback_query(filters.regex("^(cancel_|change_|del_|add_|clear_)(prefix|suffix|title|author|metadata)$"))
async def metadata_callback_handler(client, query):
    """Handle all metadata-related callbacks"""
    try:
        user_id = query.from_user.id
        action = query.data.split("_")[0]
        field = "_".join(query.data.split("_")[1:])
        
        if action == "cancel":
            if user_id in metadata_states:
                del metadata_states[user_id]
            await query.edit_message_text("❌ Cancelled!")
            
        elif action == "change":
            await query.answer()
            msg = await app.send_message(
                chat_id=user_id,
                text=f"📝 Send your new {field.replace('_', ' ')}:"
            )
            metadata_states[user_id] = {"state": f"waiting_{field}", "msg_id": msg.id}
            
        elif action == "add":
            await query.answer()
            msg = await app.send_message(
                chat_id=user_id,
                text=f"📝 Send your {field.replace('_', ' ')}:"
            )
            metadata_states[user_id] = {"state": f"waiting_{field}", "msg_id": msg.id}
            
        elif action == "del" and field == "prefix":
            db.delete_prefix(user_id)
            await query.edit_message_text("✅ Prefix deleted!")
            await send_log(app, "User deleted prefix", user_id)
            
        elif action == "del" and field == "suffix":
            db.delete_suffix(user_id)
            await query.edit_message_text("✅ Suffix deleted!")
            await send_log(app, "User deleted suffix", user_id)
            
        elif action == "clear" and field == "metadata":
            db.set_metadata(user_id, title=None, author=None)
            await query.edit_message_text("✅ Metadata cleared!")
            await send_log(app, "User cleared metadata", user_id)
            
        elif action == "edit":
            await query.answer()
            msg = await app.send_message(
                chat_id=user_id,
                text=f"📝 Send your new {field.replace('_', ' ')}:"
            )
            metadata_states[user_id] = {"state": f"waiting_{field}", "msg_id": msg.id}
        
    except Exception as e:
        logger.error(f"Error in metadata_callback_handler: {e}")
