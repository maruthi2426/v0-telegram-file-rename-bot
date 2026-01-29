import logging
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        # Support both DATABASE_URL and DB_URL for compatibility
        self.db_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL")
        self.db_name = os.getenv("DATABASE_NAME", "file_rename_bot")
        self.client = None
        self.db = None
        
        if not self.db_url:
            logger.error("DATABASE_URL environment variable is not set!")
            raise ValueError("DATABASE_URL or DB_URL must be set")
        
    def connect(self):
        """Connect to MongoDB with retry logic"""
        try:
            logger.info("Attempting to connect to MongoDB...")
            self.client = MongoClient(
                self.db_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )
            self.db = self.client[self.db_name]
            
            # Test the connection
            logger.info("Testing MongoDB connection with ping...")
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB successfully (Database: {self.db_name})")
            return True
        except ConnectionFailure as e:
            logger.error(f"MongoDB Connection Failure: {e}")
            return False
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {type(e).__name__}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    # User operations
    def add_user(self, user_id, username=None, first_name=None):
        """Add or update user in database"""
        users = self.db["users"]
        users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "username": username,
                    "first_name": first_name,
                    "joined_date": datetime.now()
                },
                "$setOnInsert": {
                    "rename_count": 0,
                    "is_banned": False
                }
            },
            upsert=True
        )
    
    def get_user(self, user_id):
        """Get user data"""
        users = self.db["users"]
        return users.find_one({"user_id": user_id})
    
    def user_exists(self, user_id):
        """Check if user exists"""
        return self.get_user(user_id) is not None
    
    def increment_rename_count(self, user_id):
        """Increment user's rename count"""
        users = self.db["users"]
        users.update_one(
            {"user_id": user_id},
            {"$inc": {"rename_count": 1}}
        )
    
    # Thumbnail operations
    def set_thumbnail(self, user_id, file_id, file_unique_id):
        """Set user's thumbnail"""
        thumbnails = self.db["thumbnails"]
        thumbnails.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "file_id": file_id,
                    "file_unique_id": file_unique_id,
                    "updated_at": datetime.now()
                }
            },
            upsert=True
        )
    
    def get_thumbnail(self, user_id):
        """Get user's thumbnail"""
        thumbnails = self.db["thumbnails"]
        return thumbnails.find_one({"user_id": user_id})
    
    def delete_thumbnail(self, user_id):
        """Delete user's thumbnail"""
        thumbnails = self.db["thumbnails"]
        thumbnails.delete_one({"user_id": user_id})
    
    # Caption operations
    def set_caption(self, user_id, caption):
        """Set user's custom caption"""
        captions = self.db["captions"]
        captions.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "caption": caption,
                    "updated_at": datetime.now()
                }
            },
            upsert=True
        )
    
    def get_caption(self, user_id):
        """Get user's custom caption"""
        captions = self.db["captions"]
        result = captions.find_one({"user_id": user_id})
        return result["caption"] if result else None
    
    def delete_caption(self, user_id):
        """Delete user's custom caption"""
        captions = self.db["captions"]
        captions.delete_one({"user_id": user_id})
    
    # Rename format operations
    def set_rename_format(self, user_id, format_string):
        """Set user's rename format"""
        formats = self.db["rename_formats"]
        formats.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "format": format_string,
                    "updated_at": datetime.now()
                }
            },
            upsert=True
        )
    
    def get_rename_format(self, user_id):
        """Get user's rename format"""
        formats = self.db["rename_formats"]
        result = formats.find_one({"user_id": user_id})
        return result["format"] if result else None
    
    # Prefix/Suffix operations
    def set_prefix(self, user_id, prefix):
        """Set user's prefix"""
        affixes = self.db["affixes"]
        affixes.update_one(
            {"user_id": user_id},
            {"$set": {"prefix": prefix}},
            upsert=True
        )
    
    def get_prefix(self, user_id):
        """Get user's prefix"""
        affixes = self.db["affixes"]
        result = affixes.find_one({"user_id": user_id})
        return result.get("prefix") if result else None
    
    def set_suffix(self, user_id, suffix):
        """Set user's suffix"""
        affixes = self.db["affixes"]
        affixes.update_one(
            {"user_id": user_id},
            {"$set": {"suffix": suffix}},
            upsert=True
        )
    
    def get_suffix(self, user_id):
        """Get user's suffix"""
        affixes = self.db["affixes"]
        result = affixes.find_one({"user_id": user_id})
        return result.get("suffix") if result else None
    
    def delete_prefix(self, user_id):
        """Delete user's prefix"""
        affixes = self.db["affixes"]
        affixes.update_one(
            {"user_id": user_id},
            {"$unset": {"prefix": ""}}
        )
    
    def delete_suffix(self, user_id):
        """Delete user's suffix"""
        affixes = self.db["affixes"]
        affixes.update_one(
            {"user_id": user_id},
            {"$unset": {"suffix": ""}}
        )
    
    # Metadata operations
    def set_metadata(self, user_id, title=None, author=None):
        """Set user's metadata"""
        metadata = self.db["metadata"]
        update_data = {"updated_at": datetime.now()}
        if title:
            update_data["title"] = title
        if author:
            update_data["author"] = author
        
        metadata.update_one(
            {"user_id": user_id},
            {"$set": update_data},
            upsert=True
        )
    
    def get_metadata(self, user_id):
        """Get user's metadata"""
        metadata = self.db["metadata"]
        return metadata.find_one({"user_id": user_id})
    
    # Force subscribe channels
    def add_force_sub_channel(self, channel_username):
        """Add channel to force subscribe list"""
        channels = self.db["force_sub_channels"]
        channels.update_one(
            {"username": channel_username},
            {"$set": {"username": channel_username}},
            upsert=True
        )
    
    def remove_force_sub_channel(self, channel_username):
        """Remove channel from force subscribe list"""
        channels = self.db["force_sub_channels"]
        channels.delete_one({"username": channel_username})
    
    def get_all_force_sub_channels(self):
        """Get all force subscribe channels"""
        channels = self.db["force_sub_channels"]
        return list(channels.find({}, {"_id": 0}))
    
    # Ban operations
    def ban_user(self, user_id):
        """Ban a user"""
        users = self.db["users"]
        users.update_one(
            {"user_id": user_id},
            {"$set": {"is_banned": True}}
        )
    
    def unban_user(self, user_id):
        """Unban a user"""
        users = self.db["users"]
        users.update_one(
            {"user_id": user_id},
            {"$set": {"is_banned": False}}
        )
    
    def is_user_banned(self, user_id):
        """Check if user is banned"""
        user = self.get_user(user_id)
        return user.get("is_banned", False) if user else False
    
    def get_banned_users(self):
        """Get all banned users"""
        users = self.db["users"]
        return list(users.find({"is_banned": True}))
    
    # Admin operations
    def add_admin(self, user_id):
        """Add an admin"""
        admins = self.db["admins"]
        admins.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "added_at": datetime.now()}},
            upsert=True
        )
    
    def remove_admin(self, user_id):
        """Remove an admin"""
        admins = self.db["admins"]
        admins.delete_one({"user_id": user_id})
    
    def get_all_admins(self):
        """Get all admins"""
        admins = self.db["admins"]
        return list(admins.find({}, {"_id": 0}))
    
    def is_admin(self, user_id):
        """Check if user is admin"""
        admins = self.db["admins"]
        return admins.find_one({"user_id": user_id}) is not None
    
    # Leaderboard operations
    def get_leaderboard(self, limit=10):
        """Get top users by rename count"""
        users = self.db["users"]
        return list(users.find({}, {"_id": 0}).sort("rename_count", -1).limit(limit))
    
    # Sequence mode operations
    def start_sequence(self, user_id):
        """Start file sequence mode for user"""
        sequences = self.db["sequences"]
        sequences.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_active": True,
                    "files": [],
                    "started_at": datetime.now()
                }
            },
            upsert=True
        )
    
    def add_to_sequence(self, user_id, file_data):
        """Add file to sequence"""
        sequences = self.db["sequences"]
        sequences.update_one(
            {"user_id": user_id},
            {"$push": {"files": file_data}}
        )
    
    def end_sequence(self, user_id):
        """End file sequence mode for user"""
        sequences = self.db["sequences"]
        sequences.update_one(
            {"user_id": user_id},
            {"$set": {"is_active": False}}
        )
        result = sequences.find_one({"user_id": user_id})
        return result.get("files", []) if result else []
    
    def is_sequence_active(self, user_id):
        """Check if user has active sequence mode"""
        sequences = self.db["sequences"]
        result = sequences.find_one({"user_id": user_id})
        return result.get("is_active", False) if result else False

# Initialize database instance
db = Database()
