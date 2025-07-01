
"""
Système de logs configurable pour SlimBoy
Gestion avancée des logs avec configuration Discord
"""

import discord
from discord.ext import commands
import logging
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from config import BOT_CONFIG

class LoggingSystem:
    """Système de logs configurable pour le bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "logging_config.json"
        self.load_config()
    
    def load_config(self):
        """Charger la configuration des logs"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # Configuration par défaut
                self.config = {
                    "enabled": False,
                    "log_channel_id": None,
                    "log_types": {
                        "moderation": True,
                        "bans": True,
                        "kicks": True,
                        "timeouts": True,
                        "unbans": True,
                        "errors": True,
                        "commands": False
                    },
                    "embed_color": 0x3498db,
                    "include_moderator": True,
                    "include_reason": True,
                    "include_timestamp": True
                }
                self.save_config()
        except Exception as e:
            logging.error(f"Erreur lors du chargement de la config logs: {e}")
            self.config = {}
    
    def save_config(self):
        """Sauvegarder la configuration des logs"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de la config logs: {e}")
    
    async def log_action(self, action_type: str, guild: discord.Guild, 
                        user: discord.User = None, moderator: discord.Member = None,
                        reason: str = None, **kwargs):
        """Enregistrer une action dans les logs"""
        if not self.config.get("enabled", False):
            return
        
        if not self.config.get("log_types", {}).get(action_type, False):
            return
        
        channel_id = self.config.get("log_channel_id")
        if not channel_id:
            return
        
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return
            
            embed = self.create_log_embed(action_type, guild, user, moderator, reason, **kwargs)
            await channel.send(embed=embed)
            
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi du log: {e}")
    
    def create_log_embed(self, action_type: str, guild: discord.Guild,
                        user: discord.User = None, moderator: discord.Member = None,
                        reason: str = None, **kwargs) -> discord.Embed:
        """Créer un embed pour les logs"""
        
        action_emojis = {
            "ban": "🔨",
            "unban": "🔓",
            "kick": "👢",
            "timeout": "⏰",
            "tempban": "⏲️",
            "ipban": "🚫",
            "error": "❌",
            "command": "💬"
        }
        
        action_titles = {
            "ban": "Bannissement",
            "unban": "Débannissement", 
            "kick": "Expulsion",
            "timeout": "Timeout",
            "tempban": "Ban Temporaire",
            "ipban": "Ban IP",
            "error": "Erreur",
            "command": "Commande Utilisée"
        }
        
        emoji = action_emojis.get(action_type, "📝")
        title = action_titles.get(action_type, action_type.title())
        
        embed = discord.Embed(
            title=f"{emoji} {title}",
            color=self.config.get("embed_color", 0x3498db),
            timestamp=datetime.now() if self.config.get("include_timestamp", True) else None
        )
        
        if user:
            embed.add_field(
                name="👤 Utilisateur",
                value=f"{user.mention}\n`{user}` (ID: {user.id})",
                inline=True
            )
        
        if moderator and self.config.get("include_moderator", True):
            embed.add_field(
                name="🛡️ Modérateur",
                value=f"{moderator.mention}\n`{moderator}`",
                inline=True
            )
        
        if reason and self.config.get("include_reason", True):
            embed.add_field(
                name="📋 Raison",
                value=reason[:1024] if len(reason) > 1024 else reason,
                inline=False
            )
        
        # Ajouter des champs spécifiques selon l'action
        if action_type == "tempban" and "duration" in kwargs:
            embed.add_field(
                name="⏱️ Durée",
                value=kwargs["duration"],
                inline=True
            )
        
        embed.set_footer(
            text=f"Serveur: {guild.name}",
            icon_url=guild.icon.url if guild.icon else None
        )
        
        return embed

# Commandes pour configurer les logs
class LoggingCommands(commands.Cog):
    """Commandes pour configurer le système de logs"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logging_system = LoggingSystem(bot)
        bot.logging_system = self.logging_system
    
    @discord.app_commands.command(name="logs_setup", description="🔧 Configurer le système de logs du bot")
    @discord.app_commands.describe(
        channel="Canal où envoyer les logs",
        enable="Activer ou désactiver les logs"
    )
    async def logs_setup(self, interaction: discord.Interaction, 
                        channel: discord.TextChannel = None,
                        enable: bool = None):
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour configurer les logs.",
                ephemeral=True
            )
            return
        
        if enable is not None:
            self.logging_system.config["enabled"] = enable
        
        if channel:
            self.logging_system.config["log_channel_id"] = channel.id
        
        self.logging_system.save_config()
        
        embed = discord.Embed(
            title="🔧 Configuration des Logs",
            color=0x00ff00,
            description="Configuration mise à jour avec succès !"
        )
        
        embed.add_field(
            name="📊 Statut",
            value="✅ Activé" if self.logging_system.config.get("enabled") else "❌ Désactivé",
            inline=True
        )
        
        if self.logging_system.config.get("log_channel_id"):
            log_channel = self.bot.get_channel(self.logging_system.config["log_channel_id"])
            embed.add_field(
                name="📍 Canal",
                value=log_channel.mention if log_channel else "Canal non trouvé",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="logs_types", description="📋 Configurer les types de logs à enregistrer")
    async def logs_types(self, interaction: discord.Interaction):
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour configurer les logs.",
                ephemeral=True
            )
            return
        
        view = LogTypesView(self.logging_system)
        
        embed = discord.Embed(
            title="📋 Configuration des Types de Logs",
            description="Choisissez quels types d'actions doivent être enregistrés dans les logs.",
            color=0x3498db
        )
        
        for log_type, enabled in self.logging_system.config.get("log_types", {}).items():
            status = "✅" if enabled else "❌"
            embed.add_field(
                name=f"{status} {log_type.title()}",
                value="Activé" if enabled else "Désactivé",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class LogTypesView(discord.ui.View):
    """Vue pour configurer les types de logs"""
    
    def __init__(self, logging_system):
        super().__init__(timeout=300)
        self.logging_system = logging_system
    
    @discord.ui.button(label="Modération", style=discord.ButtonStyle.secondary)
    async def toggle_moderation(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_log_type(interaction, "moderation")
    
    @discord.ui.button(label="Bans", style=discord.ButtonStyle.secondary)
    async def toggle_bans(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_log_type(interaction, "bans")
    
    @discord.ui.button(label="Erreurs", style=discord.ButtonStyle.secondary)
    async def toggle_errors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_log_type(interaction, "errors")
    
    async def toggle_log_type(self, interaction: discord.Interaction, log_type: str):
        """Basculer l'état d'un type de log"""
        current = self.logging_system.config.get("log_types", {}).get(log_type, False)
        self.logging_system.config["log_types"][log_type] = not current
        self.logging_system.save_config()
        
        status = "activé" if not current else "désactivé"
        await interaction.response.send_message(
            f"✅ Logs de {log_type} {status}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(LoggingCommands(bot))
