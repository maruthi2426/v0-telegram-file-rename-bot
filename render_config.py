"""
Render-specific configuration for the Telegram bot
This file handles deployment-specific settings for Render.com
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)

class RenderConfig:
    """Configuration handler for Render deployment"""
    
    @staticmethod
    def validate_environment():
        """Validate all required environment variables"""
        required_vars = {
            'API_ID': 'Telegram API ID',
            'API_HASH': 'Telegram API Hash',
            'BOT_TOKEN': 'Telegram Bot Token',
            'DATABASE_URL': 'MongoDB Connection String',
            'OWNER_ID': 'Bot Owner User ID',
        }
        
        optional_vars = {
            'LOG_CHANNEL': 'Log Channel ID (optional)',
            'ADMIN_IDS': 'Admin IDs comma-separated (optional)',
            'DATABASE_NAME': 'Database Name (defaults to file_rename_bot)',
        }
        
        missing = []
        for var, desc in required_vars.items():
            if not os.getenv(var):
                missing.append(f"{var} ({desc})")
        
        if missing:
            logger.error("=" * 60)
            logger.error("MISSING REQUIRED ENVIRONMENT VARIABLES:")
            for var in missing:
                logger.error(f"  - {var}")
            logger.error("=" * 60)
            logger.error("Please add these variables in Render Dashboard:")
            logger.error("  1. Go to your web service settings")
            logger.error("  2. Click 'Environment'")
            logger.error("  3. Add the missing variables")
            logger.error("=" * 60)
            return False
        
        logger.info("All required environment variables validated")
        return True
    
    @staticmethod
    def get_config():
        """Get configuration dictionary"""
        return {
            'api_id': int(os.getenv('API_ID', 0)),
            'api_hash': os.getenv('API_HASH'),
            'bot_token': os.getenv('BOT_TOKEN'),
            'database_url': os.getenv('DATABASE_URL'),
            'database_name': os.getenv('DATABASE_NAME', 'file_rename_bot'),
            'owner_id': int(os.getenv('OWNER_ID', 0)),
            'log_channel': os.getenv('LOG_CHANNEL'),
            'admin_ids': [int(x.strip()) for x in (os.getenv('ADMIN_IDS', '').split(',') if os.getenv('ADMIN_IDS') else [])],
            'is_render': True,
        }
    
    @staticmethod
    def print_startup_info():
        """Print startup information for debugging"""
        logger.info("=" * 60)
        logger.info("TELEGRAM FILE RENAME BOT - RENDER DEPLOYMENT")
        logger.info("=" * 60)
        
        config = RenderConfig.get_config()
        
        logger.info(f"API ID: {config['api_id']}")
        logger.info(f"Bot Token: {config['bot_token'][:20]}...***")
        logger.info(f"Database: {config['database_name']}")
        logger.info(f"Owner ID: {config['owner_id']}")
        logger.info(f"Admin Count: {len(config['admin_ids'])}")
        
        logger.info("=" * 60)
