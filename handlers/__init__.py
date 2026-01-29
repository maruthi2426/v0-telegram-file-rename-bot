"""
Handlers package for Telegram File Rename Bot
"""

from . import (
    start_handler,
    rename_handler,
    thumbnail_handler,
    caption_handler,
    admin_handler,
    user_handler,
    metadata_handler
)

__all__ = [
    "start_handler",
    "rename_handler",
    "thumbnail_handler",
    "caption_handler",
    "admin_handler",
    "user_handler",
    "metadata_handler"
]
