"""
Ban List Command
Discord slash command for displaying paginated banned users list
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from utils.pagination import PaginationView
from utils.embeds import create_ban_list_embed
from config import BOT_CONFIG

logger = logging.getLogger(__name__)

class BanListCommand(commands.Cog):
    """Cog for ban list related commands"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="banlist",
        description="Affiche la liste paginée des membres bannis du serveur"
    )
    @app_commands.describe(
        page="Numéro de page à afficher (défaut: 1)",
        search="Rechercher un utilisateur par pseudo (optionnel)"
    )
    async def ban_list(self, interaction: discord.Interaction, page: int = 1, search: str = ""):
        """Slash command to display banned users list with pagination"""

        # Check if interaction is valid
        if not interaction.guild or not interaction.user:
            return

        # Check if user has permission to use this command
        try:
            # Get the member object to access guild permissions
            member = interaction.guild.get_member(interaction.user.id)
            if not member:
                # Fallback: fetch member if not in cache
                try:
                    member = await interaction.guild.fetch_member(interaction.user.id)
                except discord.errors.NotFound:
                    await interaction.response.send_message(
                        "❌ Impossible de vérifier vos permissions. Assurez-vous d'être membre de ce serveur.",
                        ephemeral=True
                    )
                    return
                except Exception as e:
                    await interaction.response.send_message(
                        f"❌ Erreur lors de la vérification des permissions: {str(e)}",
                        ephemeral=True
                    )
                    return

            # Check if user is guild owner
            is_owner = interaction.guild.owner_id == interaction.user.id

            # Check permissions: ban_members, administrator, or guild owner
            has_permission = (
                is_owner or 
                member.guild_permissions.administrator or 
                member.guild_permissions.ban_members
            )

            if not has_permission:
                await interaction.response.send_message(
                    "❌ Vous devez avoir la permission 'Bannir des membres', 'Administrateur' ou être propriétaire du serveur pour utiliser cette commande.",
                    ephemeral=True
                )
                return

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erreur lors de la vérification des permissions: {str(e)}",
                ephemeral=True
            )
            return

        # Check if bot has permission to view bans and audit logs
        bot_member = interaction.guild.me
        if not bot_member:
            return

        bot_permissions = bot_member.guild_permissions
        if not bot_permissions.ban_members:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "❌ J'ai besoin de la permission 'Bannir des membres' pour voir la liste des bannis.",
                        ephemeral=True
                    )
            except (discord.errors.NotFound, discord.errors.HTTPException):
                pass
            return

        if not bot_permissions.view_audit_log:
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "❌ J'ai besoin de la permission 'Voir les logs d'audit' pour identifier qui a banni chaque utilisateur.",
                        ephemeral=True
                    )
            except (discord.errors.NotFound, discord.errors.HTTPException):
                pass
            return

        # Defer response as fetching bans might take time
        try:
            if not interaction.response.is_done():
                await interaction.response.defer()
        except (discord.errors.NotFound, discord.errors.HTTPException):
            return

        try:
            # Fetch all banned users
            banned_users = []
            if interaction.guild:
                async for ban_entry in interaction.guild.bans():
                    banned_users.append(ban_entry)

            # Filter by search term if provided
            if search and search.strip():
                search_lower = search.lower()
                filtered_users = []
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if (search_lower in user.display_name.lower() or 
                        search_lower in user.name.lower() or 
                        search_lower in str(user.id)):
                        filtered_users.append(ban_entry)
                banned_users = filtered_users

            if not banned_users:
                if search and search.strip():
                    embed = discord.Embed(
                        title="📋 Liste des Bannis - Recherche",
                        description=f"Aucun utilisateur banni trouvé pour la recherche: **{search}**",
                        color=discord.Color.orange()
                    )
                    embed.set_footer(text=f"Serveur: {interaction.guild.name} • Créé par @Ninja Iyed")
                else:
                    embed = discord.Embed(
                        title="📋 Liste des Bannis",
                        description="Aucun utilisateur banni trouvé sur ce serveur.",
                        color=discord.Color.green()
                    )
                    embed.set_footer(text=f"Serveur: {interaction.guild.name} • Créé par @Ninja Iyed")
                await interaction.followup.send(embed=embed)
                return

            # Fetch audit logs to get who banned each user
            ban_info = {}
            try:
                if interaction.guild:
                    async for entry in interaction.guild.audit_logs(action=discord.AuditLogAction.ban, limit=500):
                        if entry.target and entry.target.id:
                            ban_info[entry.target.id] = {
                                'moderator': entry.user,
                                'timestamp': entry.created_at,
                                'reason': entry.reason
                            }
            except discord.Forbidden:
                # If we can't access audit logs, continue without moderator info
                pass

            # Validate page number
            total_pages = (len(banned_users) + BOT_CONFIG['bans_per_page'] - 1) // BOT_CONFIG['bans_per_page']
            if page < 1:
                page = 1
            elif page > total_pages:
                page = total_pages

            # Create initial embed
            guild_name = interaction.guild.name if interaction.guild else "Unknown Server"
            search_query = search if search and search.strip() else None
            embed = create_ban_list_embed(
                banned_users=banned_users,
                page=page,
                per_page=BOT_CONFIG['bans_per_page'],
                guild_name=guild_name,
                ban_info=ban_info,
                search_term=search_query
            )

            # Always create pagination view to show manage button
            view = PaginationView(
                banned_users=banned_users,
                current_page=page,
                per_page=BOT_CONFIG['bans_per_page'],
                guild_name=guild_name,
                user_id=interaction.user.id,
                ban_info=ban_info,
                search_term=search_query
            )
            await interaction.followup.send(embed=embed, view=view)

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas la permission de voir la liste des bannis. Assurez-vous que j'ai la permission 'Bannir des membres'.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            logger.error(f"HTTP error while fetching bans: {e}")
            await interaction.followup.send(
                "❌ Une erreur s'est produite lors de la récupération de la liste des bannis. Veuillez réessayer plus tard.",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Unexpected error in ban_list command: {e}")
            await interaction.followup.send(
                "❌ Une erreur inattendue s'est produite. Veuillez réessayer plus tard.",
                ephemeral=True
            )

    @ban_list.error
    async def ban_list_error(self, interaction: discord.Interaction, error):
        """Error handler for ban_list command"""
        logger.error(f"Error in ban_list command: {error}")

        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ Une erreur s'est produite lors du traitement de votre demande.",
                    ephemeral=True
                )
        except discord.errors.NotFound:
            pass  # L'interaction a expiré
            # Interaction expired, ignore
            pass

async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(BanListCommand(bot))
    logger.info("BanListCommand cog loaded successfully")