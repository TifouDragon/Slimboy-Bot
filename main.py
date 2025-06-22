"""
Discord Bot Entry Point
Main file to run the Discord bot for displaying banned server members
"""
import asyncio
import logging
import os
from keep_alive import keep_alive
from bot import DiscordBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    keep_alive()  # Lance le serveur Flask (une seule fois)

    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not bot_token:
        logger.error("❌ DISCORD_BOT_TOKEN environment variable is not set")
        return

    bot = DiscordBot()
    logger.info("🚀 Starting Discord bot SlimBoy...")
    try:
        await bot.start(bot_token)
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
    finally:
        logger.info("🔌 Bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")