
"""
Discord Bot Entry Point
Main file to run the Discord bot for displaying banned server members
"""
import asyncio
import logging
import os
import threading
from bot import DiscordBot
from keep_alive import keep_alive

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to start the Discord bot"""
    try:
        # Get bot token from environment variables
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        
        if not bot_token:
            logger.error("DISCORD_BOT_TOKEN environment variable is not set")
            logger.error("Please add your Discord bot token in Railway environment variables")
            return
        
        # Create and start the bot
        bot = DiscordBot()
        
        logger.info("Starting Discord bot...")
        await bot.start(bot_token)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    # Start the keep-alive server for Railway
    keep_alive()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
