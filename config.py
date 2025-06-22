"""
Bot Configuration
Configuration settings for the Discord ban list bot
"""

import os

# Bot configuration
BOT_CONFIG = {
    # Command settings
    "command_prefix": "!",
    "bans_per_page": 5,
    
    # Embed settings
    "embed_color": 0xFF0000,  # Red color for ban embeds
    "success_color": 0x00FF00,  # Green color for success embeds
    "error_color": 0xFF0000,  # Red color for error embeds
    
    # Pagination settings
    "pagination_timeout": 300,  # 5 minutes
    
    # Permission settings
    "required_permissions": ["ban_members"],
    
    # Bot status
    "activity_name": "for banned users",
    "activity_type": "watching",
}

# Environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
}

# Bot intents required
REQUIRED_INTENTS = [
    "guilds",
    "members",
    "message_content"
]

# API limits and timeouts
API_CONFIG = {
    "ban_fetch_timeout": 30,  # seconds
    "max_retries": 3,
    "retry_delay": 1,  # seconds
}

# Feature flags
FEATURES = {
    "slash_commands": True,
    "button_pagination": True,
    "ban_reason_parsing": True,
    "bot_detection": True,
    "account_age_display": True,
}
