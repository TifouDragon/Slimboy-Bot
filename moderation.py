
"""
Moderation Commands Plugin
Discord slash commands for server moderation
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)

class ModerationCommands(commands.Cog):
    """Cog for moderation related commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    def has_moderation_permission(self, member):
        """Check if user has moderation permissions"""
        return (
            member.guild_permissions.administrator or 
            member.guild_permissions.ban_members or
            member.guild_permissions.kick_members or
            member.guild_permissions.manage_messages
        )
    
    @app_commands.command(
        name="ban",
        description="Bannir un utilisateur du serveur"
    )
    @app_commands.describe(
        user="L'utilisateur à bannir",
        reason="Raison du bannissement",
        delete_messages="Supprimer les messages (jours: 0-7)"
    )
    async def ban_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie", delete_messages: int = 0):
        """Ban a user from the server"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de bannir des membres.",
                ephemeral=True
            )
            return
        
        # Can't ban yourself or bot
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas vous bannir vous-même.",
                ephemeral=True
            )
            return
        
        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ Je ne peux pas me bannir moi-même.",
                ephemeral=True
            )
            return
        
        # Check hierarchy
        if user.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas bannir un utilisateur avec un rôle égal ou supérieur au vôtre.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Validate delete_messages parameter
            if delete_messages < 0 or delete_messages > 7:
                delete_messages = 0
            
            # Ban the user
            await interaction.guild.ban(
                user, 
                reason=f"Banni par {interaction.user} - {reason}",
                delete_message_days=delete_messages
            )
            
            # Create success embed
            embed = discord.Embed(
                title="🔨 Utilisateur Banni",
                description=f"**{user.display_name}** a été banni du serveur.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            if delete_messages > 0:
                embed.add_field(name="Messages supprimés", value=f"{delete_messages} jour(s)", inline=True)
            
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour bannir cet utilisateur.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors du bannissement: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="kick",
        description="Expulser un utilisateur du serveur"
    )
    @app_commands.describe(
        user="L'utilisateur à expulser",
        reason="Raison de l'expulsion"
    )
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie"):
        """Kick a user from the server"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission d'expulser des membres.",
                ephemeral=True
            )
            return
        
        # Can't kick yourself or bot
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas vous expulser vous-même.",
                ephemeral=True
            )
            return
        
        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ Je ne peux pas m'expulser moi-même.",
                ephemeral=True
            )
            return
        
        # Check hierarchy
        if user.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas expulser un utilisateur avec un rôle égal ou supérieur au vôtre.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Kick the user
            await interaction.guild.kick(
                user, 
                reason=f"Expulsé par {interaction.user} - {reason}"
            )
            
            # Create success embed
            embed = discord.Embed(
                title="👢 Utilisateur Expulsé",
                description=f"**{user.display_name}** a été expulsé du serveur.",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour expulser cet utilisateur.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de l'expulsion: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="timeout",
        description="Mettre un utilisateur en timeout"
    )
    @app_commands.describe(
        user="L'utilisateur à timeout",
        duration="Durée du timeout (ex: 10m, 1h, 2d)",
        reason="Raison du timeout"
    )
    async def timeout_user(self, interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = "Aucune raison fournie"):
        """Timeout a user"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de modérer les membres.",
                ephemeral=True
            )
            return
        
        # Can't timeout yourself or bot
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas vous mettre en timeout vous-même.",
                ephemeral=True
            )
            return
        
        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ Je ne peux pas me mettre en timeout moi-même.",
                ephemeral=True
            )
            return
        
        # Parse duration
        duration_seconds = self.parse_duration(duration)
        if duration_seconds is None:
            await interaction.response.send_message(
                "❌ Format de durée invalide. Utilisez: 10m, 1h, 2d, etc.",
                ephemeral=True
            )
            return
        
        # Discord timeout limit is 28 days
        if duration_seconds > 28 * 24 * 60 * 60:
            await interaction.response.send_message(
                "❌ La durée maximale du timeout est de 28 jours.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Calculate timeout end time
            timeout_until = datetime.utcnow() + timedelta(seconds=duration_seconds)
            
            # Apply timeout
            await user.timeout(
                timeout_until,
                reason=f"Timeout par {interaction.user} - {reason}"
            )
            
            # Create success embed
            embed = discord.Embed(
                title="🔇 Utilisateur en Timeout",
                description=f"**{user.display_name}** a été mis en timeout.",
                color=discord.Color.dark_orange(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Durée", value=duration, inline=True)
            embed.add_field(name="Fin du timeout", value=f"<t:{int(timeout_until.timestamp())}:F>", inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour timeout cet utilisateur.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors du timeout: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="clear",
        description="Supprimer des messages d'un canal"
    )
    @app_commands.describe(
        amount="Nombre de messages à supprimer (1-100)",
        user="Supprimer seulement les messages de cet utilisateur (optionnel)"
    )
    async def clear_messages(self, interaction: discord.Interaction, amount: int, user: discord.Member = None):
        """Clear messages from a channel"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de gérer les messages.",
                ephemeral=True
            )
            return
        
        # Validate amount
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "❌ Le nombre de messages doit être entre 1 et 100.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer(ephemeral=True)
            
            if user:
                # Delete messages from specific user
                def check(message):
                    return message.author.id == user.id
                
                deleted = await interaction.channel.purge(limit=amount * 3, check=check)
                deleted_count = len(deleted)
                
                await interaction.followup.send(
                    f"✅ Supprimé {deleted_count} message(s) de {user.display_name}.",
                    ephemeral=True
                )
            else:
                # Delete latest messages
                deleted = await interaction.channel.purge(limit=amount)
                deleted_count = len(deleted)
                
                await interaction.followup.send(
                    f"✅ Supprimé {deleted_count} message(s).",
                    ephemeral=True
                )
                
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour supprimer les messages.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la suppression: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="unban",
        description="Débannir un utilisateur du serveur"
    )
    @app_commands.describe(
        user_id="L'ID de l'utilisateur à débannir",
        reason="Raison du déban"
    )
    async def unban_user(self, interaction: discord.Interaction, user_id: str, reason: str = "Aucune raison fournie"):
        """Unban a user from the server"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de débannir des membres.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Convert user_id to int
            user_id = int(user_id)
            
            # Get banned users to check if user is actually banned
            banned_users = [ban_entry async for ban_entry in interaction.guild.bans()]
            banned_user = None
            
            for ban_entry in banned_users:
                if ban_entry.user.id == user_id:
                    banned_user = ban_entry.user
                    break
            
            if not banned_user:
                await interaction.followup.send(
                    "❌ Cet utilisateur n'est pas banni ou l'ID est invalide.",
                    ephemeral=True
                )
                return
            
            # Unban the user
            await interaction.guild.unban(
                banned_user,
                reason=f"Débanni par {interaction.user} - {reason}"
            )
            
            # Create success embed
            embed = discord.Embed(
                title="🔓 Utilisateur Débanni",
                description=f"**{banned_user.display_name}** a été débanni du serveur.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{banned_user} (`{banned_user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            embed.set_thumbnail(url=banned_user.avatar.url if banned_user.avatar else banned_user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except ValueError:
            await interaction.followup.send(
                "❌ ID utilisateur invalide. Veuillez fournir un ID numérique valide.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour débannir cet utilisateur.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors du déban: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="untimeout",
        description="Retirer le timeout d'un utilisateur"
    )
    @app_commands.describe(
        user="L'utilisateur à qui retirer le timeout",
        reason="Raison du retrait du timeout"
    )
    async def untimeout_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie"):
        """Remove timeout from a user"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de modérer les membres.",
                ephemeral=True
            )
            return
        
        # Check if user is actually timed out
        if not user.is_timed_out():
            await interaction.response.send_message(
                "❌ Cet utilisateur n'est pas en timeout.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Remove timeout
            await user.timeout(None, reason=f"Timeout retiré par {interaction.user} - {reason}")
            
            # Create success embed
            embed = discord.Embed(
                title="🔊 Timeout Retiré",
                description=f"**{user.display_name}** n'est plus en timeout.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour retirer le timeout de cet utilisateur.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors du retrait du timeout: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="warn",
        description="Donner un avertissement à un utilisateur"
    )
    @app_commands.describe(
        user="L'utilisateur à avertir",
        reason="Raison de l'avertissement"
    )
    async def warn_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie"):
        """Warn a user"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Can't warn yourself or bot
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas vous avertir vous-même.",
                ephemeral=True
            )
            return
        
        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ Je ne peux pas m'avertir moi-même.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Create warning embed
            embed = discord.Embed(
                title="⚠️ Avertissement Donné",
                description=f"**{user.display_name}** a reçu un avertissement.",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
            # Try to send DM to user
            try:
                dm_embed = discord.Embed(
                    title="⚠️ Vous avez reçu un avertissement",
                    description=f"Vous avez reçu un avertissement sur **{interaction.guild.name}**.",
                    color=discord.Color.orange(),
                    timestamp=datetime.utcnow()
                )
                dm_embed.add_field(name="Modérateur", value=interaction.user.display_name, inline=True)
                dm_embed.add_field(name="Raison", value=reason, inline=False)
                dm_embed.set_footer(text="Respectez les règles du serveur")
                
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                # User has DMs disabled, that's okay
                pass
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de l'avertissement: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="unwarn",
        description="Retirer un avertissement d'un utilisateur"
    )
    @app_commands.describe(
        user="L'utilisateur à qui retirer l'avertissement",
        reason="Raison du retrait de l'avertissement"
    )
    async def unwarn_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie"):
        """Remove a warning from a user"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Can't unwarn yourself or bot
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas vous retirer un avertissement à vous-même.",
                ephemeral=True
            )
            return
        
        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ Je ne peux pas me retirer un avertissement à moi-même.",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Create unwarn embed
            embed = discord.Embed(
                title="✅ Avertissement Retiré",
                description=f"Un avertissement a été retiré à **{user.display_name}**.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
            # Try to send DM to user
            try:
                dm_embed = discord.Embed(
                    title="✅ Avertissement retiré",
                    description=f"Un de vos avertissements a été retiré sur **{interaction.guild.name}**.",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                dm_embed.add_field(name="Modérateur", value=interaction.user.display_name, inline=True)
                dm_embed.add_field(name="Raison", value=reason, inline=False)
                dm_embed.set_footer(text="Continuez à respecter les règles du serveur")
                
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                # User has DMs disabled, that's okay
                pass
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors du retrait de l'avertissement: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="userinfo",
        description="Afficher les informations d'un utilisateur"
    )
    @app_commands.describe(
        user="L'utilisateur dont afficher les informations"
    )
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        """Display user information"""
        
        # Use command author if no user specified
        if user is None:
            user = interaction.user
        
        try:
            await interaction.response.defer()
            
            # Create user info embed
            embed = discord.Embed(
                title="👤 Informations Utilisateur",
                color=user.color if user.color != discord.Color.default() else discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            # User basic info
            embed.add_field(name="Nom d'utilisateur", value=f"{user}", inline=True)
            embed.add_field(name="Nom d'affichage", value=user.display_name, inline=True)
            embed.add_field(name="ID", value=f"`{user.id}`", inline=True)
            
            # Account creation and join dates
            embed.add_field(
                name="Compte créé le", 
                value=f"<t:{int(user.created_at.timestamp())}:F>\n(<t:{int(user.created_at.timestamp())}:R>)", 
                inline=True
            )
            embed.add_field(
                name="A rejoint le serveur", 
                value=f"<t:{int(user.joined_at.timestamp())}:F>\n(<t:{int(user.joined_at.timestamp())}:R>)", 
                inline=True
            )
            
            # Status
            status_emojis = {
                discord.Status.online: "🟢 En ligne",
                discord.Status.idle: "🟡 Absent",
                discord.Status.dnd: "🔴 Ne pas déranger",
                discord.Status.offline: "⚫ Hors ligne"
            }
            embed.add_field(name="Statut", value=status_emojis.get(user.status, "❓ Inconnu"), inline=True)
            
            # Roles (top 10)
            if user.roles[1:]:  # Exclude @everyone role
                roles = [role.mention for role in reversed(user.roles[1:10])]
                roles_text = ", ".join(roles)
                if len(user.roles) > 10:
                    roles_text += f"... (+{len(user.roles) - 10} autres)"
                embed.add_field(name=f"Rôles ({len(user.roles) - 1})", value=roles_text, inline=False)
            
            # Permissions
            perms = []
            if user.guild_permissions.administrator:
                perms.append("👑 Administrateur")
            elif user.guild_permissions.ban_members:
                perms.append("🔨 Bannir des membres")
            elif user.guild_permissions.kick_members:
                perms.append("👢 Expulser des membres")
            elif user.guild_permissions.manage_messages:
                perms.append("🗑️ Gérer les messages")
            
            if perms:
                embed.add_field(name="Permissions clés", value="\n".join(perms), inline=True)
            
            # User flags/badges
            flags = []
            if user.public_flags.staff:
                flags.append("👥 Staff Discord")
            if user.public_flags.partner:
                flags.append("🤝 Partenaire Discord")
            if user.public_flags.hypesquad:
                flags.append("⚡ HypeSquad")
            if user.public_flags.bug_hunter:
                flags.append("🐛 Bug Hunter")
            if user.public_flags.early_supporter:
                flags.append("💎 Early Supporter")
            if user.public_flags.verified_bot_developer:
                flags.append("🔧 Développeur de Bot Vérifié")
            
            if flags:
                embed.add_field(name="Badges", value="\n".join(flags), inline=True)
            
            # Timeout info
            if user.is_timed_out():
                embed.add_field(
                    name="⏰ En Timeout",
                    value=f"Jusqu'au <t:{int(user.timed_out_until.timestamp())}:F>",
                    inline=True
                )
            
            # Set avatar
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la récupération des informations: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="slowmode",
        description="Activer ou modifier le mode lent d'un canal"
    )
    @app_commands.describe(
        seconds="Délai en secondes entre les messages (0 pour désactiver, max 21600)",
        channel="Canal à modifier (par défaut: canal actuel)"
    )
    async def slowmode(self, interaction: discord.Interaction, seconds: int, channel: discord.TextChannel = None):
        """Set slowmode for a channel"""
        
        # Check permissions
        if not self.has_moderation_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions de modération nécessaires.",
                ephemeral=True
            )
            return
        
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de gérer les canaux.",
                ephemeral=True
            )
            return
        
        # Use current channel if none specified
        if channel is None:
            channel = interaction.channel
        
        # Validate seconds (Discord limit is 21600 seconds = 6 hours)
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message(
                "❌ Le délai doit être entre 0 et 21600 secondes (6 heures).",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer()
            
            # Set slowmode
            await channel.edit(slowmode_delay=seconds)
            
            # Create success embed
            if seconds == 0:
                embed = discord.Embed(
                    title="🚀 Mode Lent Désactivé",
                    description=f"Le mode lent a été désactivé dans {channel.mention}.",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    title="🐌 Mode Lent Activé",
                    description=f"Mode lent défini à **{seconds} seconde(s)** dans {channel.mention}.",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
            
            embed.add_field(name="Canal", value=channel.mention, inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Délai", value=f"{seconds} seconde(s)", inline=True)
            
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour modifier ce canal.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la modification du mode lent: {str(e)}",
                ephemeral=True
            )

    def parse_duration(self, duration_str):
        """Parse duration string to seconds"""
        duration_str = duration_str.lower().strip()
        
        multipliers = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800
        }
        
        try:
            if duration_str.endswith(tuple(multipliers.keys())):
                unit = duration_str[-1]
                value = int(duration_str[:-1])
                return value * multipliers[unit]
            else:
                # Assume seconds if no unit
                return int(duration_str)
        except (ValueError, IndexError):
            return None

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
