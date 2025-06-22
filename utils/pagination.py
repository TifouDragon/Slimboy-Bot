"""
Pagination Utility
Handles pagination view for ban list with navigation buttons
"""

import discord
from discord.ext import commands
import logging
import asyncio
from utils.embeds import create_ban_list_embed
from utils.ban_management import UserSelectView

logger = logging.getLogger(__name__)

class PaginationView(discord.ui.View):
    """Discord UI View for handling pagination of ban list"""
    
    def __init__(self, banned_users, current_page, per_page, guild_name, user_id, ban_info=None, search_term=None):
        super().__init__(timeout=180)  # 3 minutes timeout
        
        self.banned_users = banned_users
        self.current_page = current_page
        self.per_page = per_page
        self.guild_name = guild_name
        self.user_id = user_id
        self.ban_info = ban_info
        self.search_term = search_term
        self.total_pages = (len(banned_users) + per_page - 1) // per_page
        
        # Update button states
        self.update_buttons()
    
    def update_buttons(self):
        """Update button states based on current page"""
        # Update previous button
        self.previous_button.disabled = self.current_page <= 1
        
        # Update next button
        self.next_button.disabled = self.current_page >= self.total_pages
        
        # Update page info button
        self.page_info.label = f"Page {self.current_page}/{self.total_pages}"
        
        # Hide navigation buttons if only one page
        if self.total_pages <= 1:
            self.previous_button.style = discord.ButtonStyle.secondary
            self.previous_button.disabled = True
            self.next_button.style = discord.ButtonStyle.secondary  
            self.next_button.disabled = True
            self.page_info.label = "Page Unique"
    
    async def update_embed(self, interaction: discord.Interaction):
        """Update the embed with current page data"""
        try:
            embed = create_ban_list_embed(
                banned_users=self.banned_users,
                page=self.current_page,
                per_page=self.per_page,
                guild_name=self.guild_name,
                ban_info=self.ban_info,
                search_term=self.search_term
            )
            
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)
            
        except Exception as e:
            logger.error(f"Error updating embed: {e}")
            await interaction.response.send_message(
                "❌ Une erreur s'est produite lors de la mise à jour de la page.",
                ephemeral=True
            )
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if the user can interact with this view"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ Vous ne pouvez interagir qu'avec votre propre commande de liste de bannis.",
                ephemeral=True
            )
            return False
        return True
    
    @discord.ui.button(
        label="◀️ Précédent",
        style=discord.ButtonStyle.secondary,
        disabled=True
    )
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle previous page button click"""
        if self.current_page > 1:
            self.current_page -= 1
            await self.update_embed(interaction)
    
    @discord.ui.button(
        label="Page 1/1",
        style=discord.ButtonStyle.primary,
        disabled=True
    )
    async def page_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Display current page info (disabled button)"""
        pass
    
    @discord.ui.button(
        label="Suivant ▶️",
        style=discord.ButtonStyle.secondary
    )
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle next page button click"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            await self.update_embed(interaction)
    
    @discord.ui.button(
        label="⚙️ Gérer",
        style=discord.ButtonStyle.success,
        disabled=False
    )
    async def manage_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle manage banned users button click"""
        if not await self.interaction_check(interaction):
            return
        
        # Check if user has ban permissions
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ Vous n'avez pas la permission de gérer les bannis. Permission requise: 'Bannir des membres'.",
                ephemeral=True
            )
            return
        
        # Get current page users for management
        start_index = (self.current_page - 1) * self.per_page
        current_page_users = self.banned_users[start_index:start_index + self.per_page]
        
        if not current_page_users:
            await interaction.response.send_message("❌ Aucun utilisateur à gérer sur cette page.", ephemeral=True)
            return
        
        # Create user selection view
        select_view = UserSelectView(current_page_users, interaction.guild, interaction.user.id)
        
        embed = discord.Embed(
            title="⚙️ Gestion des Bannis",
            description="Sélectionnez un utilisateur pour le débannir, appliquer un ban temporaire ou confirmer le ban définitif.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Utilisateurs sur cette page",
            value=f"{len(current_page_users)} utilisateur(s) disponible(s)",
            inline=False
        )
        embed.set_footer(text="Créé par @Ninja Iyed • Menu expire dans 3 minutes")
        
        await interaction.response.edit_message(embed=embed, view=select_view)
    
    @discord.ui.button(
        label="🗑️ Fermer",
        style=discord.ButtonStyle.danger
    )
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle close button click with 1-minute delay before deletion"""
        if not await self.interaction_check(interaction):
            return
            
        embed = discord.Embed(
            title="📋 Liste des Bannis",
            description="Liste fermée.\n\n⏰ Ce message sera supprimé dans **1 minute**.",
            color=discord.Color.greyple()
        )
        embed.set_footer(text="Créé par @Ninja Iyed • Suppression automatique dans 1 minute")
        await interaction.response.edit_message(embed=embed, view=None)
        self.stop()
        
        # Wait 1 minute then delete the message
        await asyncio.sleep(60)  # 60 seconds = 1 minute
        try:
            await interaction.delete_original_response()
            logger.info("Message deleted after 1-minute delay (close button)")
        except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
            logger.warning(f"Could not delete message after close: {e}")
    
    async def on_timeout(self):
        """Called when the view times out - auto delete after 3 minutes"""
        logger.info("Pagination view timed out - deleting message after 3 minutes of inactivity")
        
        # Try to delete the message after timeout (3 minutes of inactivity)
        try:
            if hasattr(self, 'message') and self.message:
                await self.message.delete()
                logger.info("Message deleted due to timeout (3 minutes inactivity)")
        except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
            logger.warning(f"Could not delete message on timeout: {e}")
            # If we can't delete, just disable the view
            for item in self.children:
                if hasattr(item, 'disabled'):
                    item.disabled = True
