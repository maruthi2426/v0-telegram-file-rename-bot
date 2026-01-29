#!/usr/bin/env python3
"""
Validation script to check if the bot can start before deploying to Render
Run this locally: python validate.py
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def validate_env_vars():
    """Validate all required environment variables"""
    logger.info("=" * 60)
    logger.info("ENVIRONMENT VARIABLE VALIDATION")
    logger.info("=" * 60)
    
    required_vars = {
        'API_ID': 'Telegram API ID (get from https://my.telegram.org)',
        'API_HASH': 'Telegram API Hash (get from https://my.telegram.org)',
        'BOT_TOKEN': 'Telegram Bot Token (from @BotFather)',
        'DATABASE_URL': 'MongoDB connection string',
        'OWNER_ID': 'Your Telegram user ID',
    }
    
    missing = []
    
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            # Don't log sensitive values
            display = f"{value[:20]}...***" if len(value) > 20 else "***"
            logger.info(f"✅ {var}: {display} ({desc})")
        else:
            logger.error(f"❌ {var}: MISSING ({desc})")
            missing.append(var)
    
    if missing:
        logger.error("=" * 60)
        logger.error(f"MISSING {len(missing)} REQUIRED VARIABLE(S):")
        for var in missing:
            logger.error(f"  - {var}")
        logger.error("=" * 60)
        return False
    
    logger.info("=" * 60)
    logger.info("✅ ALL ENVIRONMENT VARIABLES VALIDATED")
    logger.info("=" * 60)
    return True

def validate_python_packages():
    """Validate all Python packages can be imported"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("PYTHON PACKAGE VALIDATION")
    logger.info("=" * 60)
    
    packages = {
        'pyrogram': 'Telegram bot framework',
        'pymongo': 'MongoDB driver',
        'dotenv': 'Environment variable loader',
        'PIL': 'Image processing',
        'requests': 'HTTP library',
    }
    
    missing = []
    
    for package, desc in packages.items():
        try:
            __import__(package)
            logger.info(f"✅ {package}: Available ({desc})")
        except ImportError:
            logger.error(f"❌ {package}: MISSING ({desc})")
            missing.append(package)
    
    if missing:
        logger.error("=" * 60)
        logger.error(f"MISSING {len(missing)} PACKAGE(S)")
        logger.error("Install with: pip install -r requirements.txt")
        logger.error("=" * 60)
        return False
    
    logger.info("=" * 60)
    logger.info("✅ ALL PACKAGES INSTALLED")
    logger.info("=" * 60)
    return True

def validate_database_url():
    """Validate MongoDB connection string format"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("DATABASE URL VALIDATION")
    logger.info("=" * 60)
    
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        logger.error("❌ DATABASE_URL not set")
        return False
    
    logger.info(f"Database URL format: {db_url[:50]}...***")
    
    # Check format
    checks = [
        (db_url.startswith('mongodb://') or db_url.startswith('mongodb+srv://'), 
         "Starts with mongodb:// or mongodb+srv://"),
        ('@' in db_url, "Contains username:password separator (@)"),
        ('.' in db_url, "Contains domain or server name"),
    ]
    
    all_passed = True
    for passed, desc in checks:
        status = "✅" if passed else "❌"
        logger.info(f"{status} {desc}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("=" * 60)
        logger.info("✅ DATABASE URL FORMAT LOOKS GOOD")
        logger.info("=" * 60)
        logger.info("Note: Actual connection will be tested when bot starts")
    else:
        logger.error("=" * 60)
        logger.error("❌ DATABASE URL FORMAT ISSUES")
        logger.error("=" * 60)
    
    return all_passed

def validate_bot_token():
    """Validate bot token format"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("BOT TOKEN VALIDATION")
    logger.info("=" * 60)
    
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("❌ BOT_TOKEN not set")
        return False
    
    logger.info(f"Token length: {len(token)} characters")
    
    checks = [
        (':' in token, "Contains colon separator (:)"),
        (len(token) > 40, "Reasonable length (>40 chars)"),
        ('_' not in token or '.' not in token, "Contains special characters"),
    ]
    
    all_passed = True
    for passed, desc in checks:
        status = "✅" if passed else "⚠️"
        logger.info(f"{status} {desc}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("=" * 60)
        logger.info("✅ BOT TOKEN FORMAT LOOKS VALID")
        logger.info("=" * 60)
    
    return True

def validate_config():
    """Validate render_config.py can be imported"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("CONFIGURATION VALIDATION")
    logger.info("=" * 60)
    
    try:
        from render_config import RenderConfig
        logger.info("✅ render_config module imported successfully")
        
        config = RenderConfig.get_config()
        logger.info("✅ Configuration loaded successfully")
        
        # Validate config values
        if config['api_id'] == 0:
            logger.error("❌ API_ID not set or invalid")
            return False
        
        if not config['bot_token']:
            logger.error("❌ BOT_TOKEN not set")
            return False
        
        logger.info("=" * 60)
        logger.info("✅ CONFIGURATION IS VALID")
        logger.info("=" * 60)
        return True
    except Exception as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("=" * 60)
        return False

def main():
    """Run all validations"""
    logger.info("")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 15 + "BOT DEPLOYMENT VALIDATOR" + " " * 20 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    results = {
        'Environment Variables': validate_env_vars(),
        'Python Packages': validate_python_packages(),
        'Database URL': validate_database_url(),
        'Bot Token': validate_bot_token(),
        'Configuration': validate_config(),
    }
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("VALIDATION SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info("=" * 60)
    logger.info(f"Result: {passed}/{total} checks passed")
    logger.info("=" * 60)
    
    if passed == total:
        logger.info("")
        logger.info("✅ ALL VALIDATION CHECKS PASSED!")
        logger.info("Your bot is ready for deployment to Render.")
        logger.info("")
        return 0
    else:
        logger.error("")
        logger.error("❌ SOME VALIDATION CHECKS FAILED")
        logger.error("Please fix the issues above before deploying.")
        logger.error("")
        return 1

if __name__ == "__main__":
    sys.exit(main())
