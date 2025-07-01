"""
Ban Management Utilities
Handles unban, temporary ban, and permanent ban operations
"""

import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BanManagementView(discord.ui.View):
    """View for managing individual banned users"""
    
    def __init__(self, banned_user, guild, moderator_id):
        super().__init__(timeout=300)  # 5 minutes timeout for action
        self.banned_user = banned_user
        self.guild = guild
        self.moderator_id = moderator_id
    
    @discord.ui.button(label="🔓 Débannir", style=discord.ButtonStyle.green)
    async def unban_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Unban the selected user"""
        if interaction.user.id != self.moderator_id:
            await interaction.response.send_message("❌ Seul la personne qui a ouvert ce menu peut utiliser ces boutons.", ephemeral=True)
            return
        
        try:
            await interaction.response.defer()
            await self.guild.unban(self.banned_user.user, reason=f"Débanni par {interaction.user}")
            
            embed = discord.Embed(
                title="✅ Utilisateur Débanni",
                description=f"**{self.banned_user.user.display_name}** a été débanni avec succès.",
                color=discord.Color.green()
            )
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
            embed.add_field(name="Date", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=True)
            embed.set_footer(text="Créé par @Ninja Iyed")
            
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            
        except discord.Forbidden:
            await interaction.followup.send("❌ Je n'ai pas les permissions nécessaires pour débannir cet utilisateur.", ephemeral=True)
        except discord.NotFound:
            await interaction.followup.send("❌ Cet utilisateur n'est plus banni.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error unbanning user: {e}")
            await interaction.followup.send("❌ Une erreur est survenue lors du déban.", ephemeral=True)
    
    @discord.ui.button(label="⏰ Ban Temporaire", style=discord.ButtonStyle.secondary)
    async def temp_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Convert to temporary ban"""
        if interaction.user.id != self.moderator_id:
            await interaction.response.send_message("❌ Seul la personne qui a ouvert ce menu peut utiliser ces boutons.", ephemeral=True)
            return
        
        await interaction.response.send_modal(TempBanModal(self.banned_user, self.guild, self.moderator_id))
    
    @discord.ui.button(label="🔒 Ban Définitif", style=discord.ButtonStyle.danger)
    async def permanent_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm permanent ban"""
        if interaction.user.id != self.moderator_id:
            await interaction.response.send_message("❌ Seul la personne qui a ouvert ce menu peut utiliser ces boutons.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🔒 Ban Définitif Confirmé",
            description=f"**{self.banned_user.user.display_name}** reste banni définitivement.",
            color=discord.Color.red()
        )
        embed.add_field(name="Statut", value="Ban permanent maintenu", inline=True)
        embed.add_field(name="Confirmé par", value=interaction.user.mention, inline=True)
        embed.set_footer(text="Créé par @Ninja Iyed")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.secondary)
    async def cancel_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel the action with 1-minute delay before deletion"""
        if interaction.user.id != self.moderator_id:
            await interaction.response.send_message("❌ Seul la personne qui a ouvert ce menu peut utiliser ces boutons.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ Action Annulée",
            description="Aucune modification n'a été apportée au bannissement.\n\n⏰ Ce message sera supprimé dans **1 minute**.",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Créé par @Ninja Iyed • Suppression automatique dans 1 minute")
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Wait 1 minute then delete the message
        await asyncio.sleep(60)  # 60 seconds = 1 minute
        try:
            await interaction.delete_original_response()
            logger.info("Message deleted after 1-minute delay (cancel action)")
        except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
            logger.warning(f"Could not delete message after cancel: {e}")

class TempBanModal(discord.ui.Modal):
    """Modal for setting temporary ban duration"""
    
    def __init__(self, banned_user, guild, moderator_id):
        super().__init__(title="⏰ Définir la Durée du Ban Temporaire")
        self.banned_user = banned_user
        self.guild = guild
        self.moderator_id = moderator_id
    
    duration = discord.ui.TextInput(
        label="Durée du ban",
        placeholder="Exemples: 1h, 2d, 1w, 30m (m=minutes, h=heures, d=jours, w=semaines)",
        required=True,
        max_length=10
    )
    
    reason = discord.ui.TextInput(
        label="Raison (optionnel)",
        placeholder="Raison du ban temporaire...",
        required=False,
        max_length=200,
        style=discord.TextStyle.paragraph
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Process the temporary ban request"""
        try:
            # Parse duration
            duration_str = self.duration.value.strip().lower()
            duration_seconds = self.parse_duration(duration_str)
            
            if duration_seconds is None:
                await interaction.response.send_message(
                    "❌ Format de durée invalide. Utilisez: 30m, 2h, 1d, 1w", 
                    ephemeral=True
                )
                return
            
            # Calculate unban time
            unban_time = datetime.now() + timedelta(seconds=duration_seconds)
            
            await interaction.response.defer()
            
            # First unban the user
            await self.guild.unban(self.banned_user.user, reason="Conversion en ban temporaire")
            
            # Then ban them again with new reason
            reason_text = self.reason.value or "Ban temporaire"
            temp_reason = f"{reason_text} (Expire le {unban_time.strftime('%d/%m/%Y %H:%M')})"
            
            await self.guild.ban(
                self.banned_user.user, 
                reason=temp_reason,
                delete_message_days=0
            )
            
            # Create success embed
            embed = discord.Embed(
                title="⏰ Ban Temporaire Appliqué",
                description=f"**{self.banned_user.user.display_name}** a été converti en ban temporaire.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Durée", value=duration_str, inline=True)
            embed.add_field(name="Expire le", value=f"<t:{int(unban_time.timestamp())}:F>", inline=True)
            embed.add_field(name="Modérateur", value=f"<@{self.moderator_id}>", inline=True)
            
            if self.reason.value:
                embed.add_field(name="Raison", value=self.reason.value, inline=False)
            
            embed.set_footer(text="Créé par @Ninja Iyed • Note: Le déban automatique n'est pas inclus")
            
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            
        except discord.Forbidden:
            await interaction.followup.send("❌ Je n'ai pas les permissions nécessaires.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error applying temp ban: {e}")
            await interaction.followup.send("❌ Une erreur est survenue.", ephemeral=True)
    
    def parse_duration(self, duration_str):
        """Parse duration string into seconds"""
        try:
            if not duration_str or len(duration_str) < 2:
                return None
            
            unit = duration_str[-1]
            value = int(duration_str[:-1])
            
            multipliers = {
                'm': 60,           # minutes
                'h': 3600,         # hours
                'd': 86400,        # days
                'w': 604800        # weeks
            }
            
            if unit in multipliers and value > 0:
                return value * multipliers[unit]
            
            return None
        except (ValueError, IndexError):
            return None

class UserSelectView(discord.ui.View):
    """View with dropdown to select a banned user"""
    
    def __init__(self, banned_users, guild, moderator_id, page_start=0):
        super().__init__(timeout=180)  # 3 minutes
        self.banned_users = banned_users
        self.guild = guild
        self.moderator_id = moderator_id
        
        # Create dropdown with up to 25 users (Discord limit)
        page_users = banned_users[page_start:page_start + 25]
        
        if page_users:
            self.add_item(UserSelectDropdown(page_users, guild, moderator_id))

class UserSelectDropdown(discord.ui.Select):
    """Dropdown for selecting a banned user"""
    
    def __init__(self, banned_users, guild, moderator_id):
        self.banned_users = banned_users
        self.guild = guild
        self.moderator_id = moderator_id
        
        # Create options for dropdown
        options = []
        for i, ban_entry in enumerate(banned_users[:25]):  # Discord limit of 25 options
            user = ban_entry.user
            # Truncate display name if too long
            display_name = user.display_name[:80] if len(user.display_name) > 80 else user.display_name
            options.append(
                discord.SelectOption(
                    label=f"{display_name}",
                    description=f"ID: {user.id}",
                    value=str(user.id)
                )
            )
        
        super().__init__(
            placeholder="Sélectionnez un utilisateur banni...",
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle user selection"""
        if interaction.user.id != self.moderator_id:
            await interaction.response.send_message(
                "❌ Seul la personne qui a ouvert ce menu peut sélectionner un utilisateur.", 
                ephemeral=True
            )
            return
        
        selected_user_id = int(self.values[0])
        
        # Find the selected banned user
        selected_ban = None
        for ban_entry in self.banned_users:
            if ban_entry.user.id == selected_user_id:
                selected_ban = ban_entry
                break
        
        if not selected_ban:
            await interaction.response.send_message("❌ Utilisateur introuvable.", ephemeral=True)
            return
        
        # Create management embed
        user = selected_ban.user
        embed = discord.Embed(
            title="⚙️ Gestion du Bannissement",
            description=f"Que souhaitez-vous faire avec **{user.display_name}** ?",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Utilisateur", value=f"{user.mention} (`{user.id}`)", inline=True)
        embed.add_field(name="Nom", value=user.display_name, inline=True)
        embed.add_field(name="Raison actuelle", value=selected_ban.reason or "Aucune raison", inline=False)
        
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        embed.set_footer(text="Créé par @Ninja Iyed")
        
        # Create management view
        management_view = BanManagementView(selected_ban, self.guild, self.moderator_id)
        
        await interaction.response.edit_message(embed=embed, view=management_view)