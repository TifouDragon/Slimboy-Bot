"""
Discord Bot Class
Main bot class that handles Discord connection and command registration
"""

import discord
from discord.ext import commands
import logging
from config import BOT_CONFIG

logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    """Main Discord bot class"""

    def __init__(self):
        # Configure bot intents - only use basic intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.bans = True
        intents.moderation = True

        super().__init__(
            command_prefix=BOT_CONFIG['command_prefix'],
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Setup hook called when bot is starting up"""
        try:
            # Load ban list commands
            from commands.ban_list import BanListCommand
            await self.add_cog(BanListCommand(self))

            # Load moderation commands
            from commands.moderation import ModerationCommands
            await self.add_cog(ModerationCommands(self))

            # Load diagnostic commands
            from commands.diagnostic import DiagnosticCommands
            await self.add_cog(DiagnosticCommands(self))

            # Load logging system
            from utils.logging_system import LoggingCommands
            await self.add_cog(LoggingCommands(self))

            # Load update notifier
            from utils.update_notifier import UpdateCommands
            await self.add_cog(UpdateCommands(self))

            # Load games system
            from commands.games import GamesCommands
            await self.add_cog(GamesCommands(self))

            # Load guardian system (if exists)
            try:
                from commands.guardian import GuardianCommands
                guardian_cog = GuardianCommands(self)
                await self.add_cog(guardian_cog)
                # Store reference for moderation commands
                self.guardian_system = guardian_cog
                logger.info("Guardian system loaded successfully")
            except ImportError:
                logger.warning("Guardian system not found, skipping...")

            # Load developer commands
            try:
                from commands.developer import DeveloperCommands
                await self.add_cog(DeveloperCommands(self))
                logger.info("Developer commands loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load developer commands: {e}")

            logger.info("All commands loaded successfully")

            # Sync slash commands
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")

        except Exception as e:
            logger.error(f"Error in setup_hook: {e}")

    async def on_ready(self):
        """Called when bot is ready and connected to Discord"""
        if self.user:
            logger.info(f"Bot logged in as {self.user} (ID: {self.user.id})")
            logger.info(f"Bot is in {len(self.guilds)} guilds")

            # Set bot status as an application bot
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="for banned users"
            )
            await self.change_presence(
                activity=activity,
                status=discord.Status.online
            )

    async def on_command_error(self, ctx, error):
        """Global error handler for commands"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions to execute this command.")
        elif isinstance(error, commands.CommandNotFound):
            # Ignore command not found errors
            pass
        else:
            logger.error(f"Command error: {error}")
            await ctx.send("❌ An error occurred while executing the command.")

    async def on_application_command_error(self, interaction, error):
        """Global error handler for slash commands"""
        if isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
        elif isinstance(error, discord.app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                "❌ I don't have the required permissions to execute this command.",
                ephemeral=True
            )
        else:
            logger.error(f"Slash command error: {error}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ An error occurred while executing the command.",
                    ephemeral=True
                )