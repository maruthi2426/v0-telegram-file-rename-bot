import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from utils import send_log, is_admin, check_user_ban, create_status_text
from config import OWNER_ID

logger = logging.getLogger(__name__)

# Store admin states
admin_states = {}

@Client.on_message(filters.command("add_admin"))
async def add_admin_command(app: Client, message: Message):
    """Handle /add_admin command"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        help_text = """
👤 **Add New Admin**

Send the Telegram User ID of the person you want to make admin.

Example: `123456789`

Send the user ID:
"""
        
        await message.reply_text(help_text, parse_mode="markdown")
        admin_states[user_id] = {"action": "waiting_admin_id"}
        
    except Exception as e:
        logger.error(f"Error in add_admin_command: {e}")

@Client.on_message(filters.command("deladmin"))
async def deladmin_command(app: Client, message: Message):
    """Handle /deladmin command"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        help_text = """
👤 **Remove Admin**

Send the Telegram User ID of the admin you want to remove.

Example: `123456789`

Send the user ID:
"""
        
        await message.reply_text(help_text, parse_mode="markdown")
        admin_states[user_id] = {"action": "waiting_remove_admin_id"}
        
    except Exception as e:
        logger.error(f"Error in deladmin_command: {e}")

@Client.on_message(filters.command("admins"))
async def admins_command(app: Client, message: Message):
    """Handle /admins command - List all admins"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        admins = db.get_all_admins()
        
        text = "👨‍💼 **Current Admins**\n\n"
        
        if admins:
            for idx, admin in enumerate(admins, 1):
                text += f"{idx}. `{admin['user_id']}`\n"
        else:
            text += "No admins added yet (only owner)"
        
        text += f"\n**Owner ID:** `{OWNER_ID}`"
        
        await message.reply_text(text, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in admins_command: {e}")

@Client.on_message(filters.command("ban"))
async def ban_command(app: Client, message: Message):
    """Handle /ban command"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        help_text = """
🚫 **Ban User**

Send the Telegram User ID of the person you want to ban.

Example: `123456789`

Send the user ID:
"""
        
        await message.reply_text(help_text, parse_mode="markdown")
        admin_states[user_id] = {"action": "waiting_ban_id"}
        
    except Exception as e:
        logger.error(f"Error in ban_command: {e}")

@Client.on_message(filters.command("unban"))
async def unban_command(app: Client, message: Message):
    """Handle /unban command"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        help_text = """
✅ **Unban User**

Send the Telegram User ID of the person you want to unban.

Example: `123456789`

Send the user ID:
"""
        
        await message.reply_text(help_text, parse_mode="markdown")
        admin_states[user_id] = {"action": "waiting_unban_id"}
        
    except Exception as e:
        logger.error(f"Error in unban_command: {e}")

@Client.on_message(filters.command("banned"))
async def banned_command(app: Client, message: Message):
    """Handle /banned command - List banned users"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        banned_users = db.get_banned_users()
        
        text = "🚫 **Banned Users**\n\n"
        
        if banned_users:
            for idx, user in enumerate(banned_users, 1):
                username = user.get('username', 'Unknown')
                text += f"{idx}. {username} (ID: `{user['user_id']}`)\n"
        else:
            text += "No banned users yet!"
        
        await message.reply_text(text, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in banned_command: {e}")

@Client.on_message(filters.command("addchnl"))
async def addchnl_command(app: Client, message: Message):
    """Handle /addchnl command - Add force subscribe channel"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        help_text = """
📢 **Add Force Subscribe Channel**

Send the channel username (without @) that users must join.

Example: `mychannel`

Send the username:
"""
        
        await message.reply_text(help_text, parse_mode="markdown")
        admin_states[user_id] = {"action": "waiting_channel"}
        
    except Exception as e:
        logger.error(f"Error in addchnl_command: {e}")

@Client.on_message(filters.command("delchnl"))
async def delchnl_command(app: Client, message: Message):
    """Handle /delchnl command - Remove force subscribe channel"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        channels = db.get_all_force_sub_channels()
        
        if not channels:
            await message.reply_text("❌ No channels added yet!")
            return
        
        keyboard = InlineKeyboardMarkup()
        for channel in channels:
            keyboard.add(InlineKeyboardButton(
                channel['username'],
                callback_data=f"remove_chnl_{channel['username']}"
            ))
        
        await message.reply_text("📢 **Remove Channel**\n\nSelect channel to remove:", reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Error in delchnl_command: {e}")

@Client.on_message(filters.command("listchnl"))
async def listchnl_command(app: Client, message: Message):
    """Handle /listchnl command - List all force subscribe channels"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        channels = db.get_all_force_sub_channels()
        
        text = "📢 **Force Subscribe Channels**\n\n"
        
        if channels:
            for idx, channel in enumerate(channels, 1):
                text += f"{idx}. @{channel['username']}\n"
        else:
            text += "No channels added yet!"
        
        await message.reply_text(text, parse_mode="markdown")
        
    except Exception as e:
        logger.error(f"Error in listchnl_command: {e}")

@Client.on_message(filters.command("broadcast"))
async def broadcast_command(app: Client, message: Message):
    """Handle /broadcast command - Broadcast message to all users"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        help_text = """
📢 **Broadcast Message**

Send the message you want to broadcast to all users.

Send your message:
"""
        
        await message.reply_text(help_text, parse_mode="markdown")
        admin_states[user_id] = {"action": "waiting_broadcast"}
        
    except Exception as e:
        logger.error(f"Error in broadcast_command: {e}")

@Client.on_message(filters.command("restart"))
async def restart_command(app: Client, message: Message):
    """Handle /restart command - Restart bot"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        if not await is_admin(app, user_id):
            await message.reply_text("❌ You don't have permission to use this command!")
            return
        
        await message.reply_text("🔄 Restarting bot...")
        await send_log(app, "Bot restarted by admin", user_id)
        
        # In production, use a process manager like systemd or supervisor
        import os
        os.system("pkill -f 'python main.py'")
        
    except Exception as e:
        logger.error(f"Error in restart_command: {e}")

# Handle text input for admin actions
@Client.on_message(filters.text & filters.private, group=5)
async def handle_admin_input(app: Client, message: Message):
    """Handle admin action text input"""
    try:
        user_id = message.from_user.id
        
        if user_id not in admin_states or not await is_admin(app, user_id):
            return
        
        action = admin_states[user_id]["action"]
        text = message.text.strip()
        
        if action == "waiting_admin_id":
            try:
                admin_id = int(text)
                db.add_admin(admin_id)
                await message.reply_text(f"✅ User `{admin_id}` is now an admin!", parse_mode="markdown")
                await send_log(app, f"Added admin: {admin_id}", user_id)
                del admin_states[user_id]
            except ValueError:
                await message.reply_text("❌ Invalid user ID!")
                
        elif action == "waiting_remove_admin_id":
            try:
                admin_id = int(text)
                db.remove_admin(admin_id)
                await message.reply_text(f"✅ User `{admin_id}` is no longer an admin!", parse_mode="markdown")
                await send_log(app, f"Removed admin: {admin_id}", user_id)
                del admin_states[user_id]
            except ValueError:
                await message.reply_text("❌ Invalid user ID!")
                
        elif action == "waiting_ban_id":
            try:
                ban_id = int(text)
                db.ban_user(ban_id)
                await message.reply_text(f"✅ User `{ban_id}` has been banned!", parse_mode="markdown")
                await send_log(app, f"Banned user: {ban_id}", user_id)
                del admin_states[user_id]
            except ValueError:
                await message.reply_text("❌ Invalid user ID!")
                
        elif action == "waiting_unban_id":
            try:
                unban_id = int(text)
                db.unban_user(unban_id)
                await message.reply_text(f"✅ User `{unban_id}` has been unbanned!", parse_mode="markdown")
                await send_log(app, f"Unbanned user: {unban_id}", user_id)
                del admin_states[user_id]
            except ValueError:
                await message.reply_text("❌ Invalid user ID!")
                
        elif action == "waiting_channel":
            channel = text.replace("@", "").strip()
            db.add_force_sub_channel(channel)
            await message.reply_text(f"✅ Channel `@{channel}` added for force subscribe!", parse_mode="markdown")
            await send_log(app, f"Added force sub channel: {channel}", user_id)
            del admin_states[user_id]
            
        elif action == "waiting_broadcast":
            # Get all users and send broadcast
            all_users = db.get_leaderboard(limit=10000)
            success = 0
            failed = 0
            
            msg = await message.reply_text("📢 Broadcasting message...")
            
            for user in all_users:
                try:
                    await app.send_message(user['user_id'], text)
                    success += 1
                except Exception as e:
                    logger.warning(f"Failed to send to {user['user_id']}: {e}")
                    failed += 1
            
            await msg.edit_text(f"✅ Broadcast complete!\n\n✅ Sent: {success}\n❌ Failed: {failed}")
            await send_log(app, f"Broadcast sent to {success} users", user_id)
            del admin_states[user_id]
    
    except Exception as e:
        logger.error(f"Error in handle_admin_input: {e}")

# Callback handler for removing channel
@Client.on_callback_query(filters.regex("^remove_chnl_"))
async def remove_channel_callback(app: Client, query):
    """Handle remove channel callback"""
    try:
        user_id = query.from_user.id
        
        if not await is_admin(app, user_id):
            await query.answer("❌ Permission denied!", show_alert=True)
            return
        
        channel = query.data.replace("remove_chnl_", "")
        db.remove_force_sub_channel(channel)
        
        await query.edit_message_text(f"✅ Channel `@{channel}` removed!", parse_mode="markdown")
        await send_log(app, f"Removed force sub channel: {channel}", user_id)
        
    except Exception as e:
        logger.error(f"Error in remove_channel_callback: {e}")
