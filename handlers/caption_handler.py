import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from utils import send_log, check_user_ban, split_text

logger = logging.getLogger(__name__)

# Store caption states
caption_states = {}

@Client.on_message(filters.command("set_caption"))
async def set_caption_command(app: Client, message: Message):
    """Handle /set_caption command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        help_text = """
📝 **Set Your Custom Caption**

Send your desired caption as a message. This caption will be added to every file you rename.

**You can use:**
• Bold: `*text*`
• Italic: `_text_`
• Code: `` `code` ``
• Mentions: `@username`

Send your caption now:
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_caption")]
        ])
        
        msg = await message.reply_text(help_text, reply_markup=keyboard, parse_mode="markdown")
        caption_states[user_id] = {"state": "waiting_caption", "msg_id": msg.id}
        
    except Exception as e:
        logger.error(f"Error in set_caption_command: {e}")

@Client.on_message(filters.command("see_caption"))
async def see_caption_command(app: Client, message: Message):
    """Handle /see_caption command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        caption = db.get_caption(user_id)
        
        if caption:
            text = f"📝 **Your Current Caption:**\n\n{caption}"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change", callback_data="change_caption")],
                [InlineKeyboardButton("🗑️ Delete", callback_data="del_caption")]
            ])
            
            await message.reply_text(text, reply_markup=keyboard, parse_mode="markdown")
        else:
            text = "❌ You haven't set a caption yet!\n\nUse /set_caption to set one."
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Set Caption", callback_data="add_caption")]
            ])
            
            await message.reply_text(text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Error in see_caption_command: {e}")

@Client.on_message(filters.command("del_caption"))
async def del_caption_command(app: Client, message: Message):
    """Handle /del_caption command"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            await message.reply_text("❌ You are banned!")
            return
        
        caption = db.get_caption(user_id)
        
        if caption:
            db.delete_caption(user_id)
            await message.reply_text("✅ Caption deleted successfully!")
            await send_log(app, "User deleted caption", user_id)
        else:
            await message.reply_text("❌ You don't have a caption to delete!")
        
    except Exception as e:
        logger.error(f"Error in del_caption_command: {e}")

# Handle text input for caption
@Client.on_message(filters.text & filters.private, group=2)
async def handle_caption_input(app: Client, message: Message):
    """Handle caption text input"""
    try:
        user_id = message.from_user.id
        
        if await check_user_ban(user_id):
            return
        
        # Check if user is waiting for caption input
        if user_id in caption_states and caption_states[user_id]["state"] == "waiting_caption":
            caption_text = message.text
            
            if caption_text:
                db.set_caption(user_id, caption_text)
                
                # Create preview
                preview = f"✅ Caption saved!\n\n**Preview:**\n{caption_text}"
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✏️ Edit", callback_data="change_caption")],
                    [InlineKeyboardButton("❌ Delete", callback_data="del_caption")]
                ])
                
                await message.reply_text(preview, reply_markup=keyboard, parse_mode="markdown")
                del caption_states[user_id]
                await send_log(app, "User set custom caption", user_id)
    
    except Exception as e:
        logger.error(f"Error in handle_caption_input: {e}")

# Callback handlers
@Client.on_callback_query(filters.regex("^cancel_caption$"))
async def cancel_caption_callback(app: Client, query):
    """Handle cancel caption button"""
    try:
        user_id = query.from_user.id
        if user_id in caption_states:
            del caption_states[user_id]
        
        await query.edit_message_text("❌ Cancelled!")
    except Exception as e:
        logger.error(f"Error in cancel_caption_callback: {e}")

@Client.on_callback_query(filters.regex("^change_caption$"))
async def change_caption_callback(app: Client, query):
    """Handle change caption button"""
    try:
        user_id = query.from_user.id
        
        await query.answer()
        
        msg = await app.send_message(
            chat_id=user_id,
            text="📝 Send your new caption:"
        )
        
        caption_states[user_id] = {"state": "waiting_caption", "msg_id": msg.id}
        
    except Exception as e:
        logger.error(f"Error in change_caption_callback: {e}")

@Client.on_callback_query(filters.regex("^add_caption$"))
async def add_caption_callback(app: Client, query):
    """Handle add caption button"""
    try:
        user_id = query.from_user.id
        
        await query.answer()
        
        msg = await app.send_message(
            chat_id=user_id,
            text="📝 Send your desired caption:"
        )
        
        caption_states[user_id] = {"state": "waiting_caption", "msg_id": msg.id}
        
    except Exception as e:
        logger.error(f"Error in add_caption_callback: {e}")

@Client.on_callback_query(filters.regex("^del_caption$"))
async def del_caption_callback(app: Client, query):
    """Handle delete caption button"""
    try:
        user_id = query.from_user.id
        
        db.delete_caption(user_id)
        
        await query.edit_message_text(
            "✅ Caption deleted successfully!"
        )
        
        await send_log(app, "User deleted caption", user_id)
        
    except Exception as e:
        logger.error(f"Error in del_caption_callback: {e}")
