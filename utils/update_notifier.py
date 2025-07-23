
"""
Système de notifications de mise à jour depuis GitHub
Vérification automatique des nouvelles versions
"""

import discord
from discord.ext import commands, tasks
import aiohttp
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class UpdateNotifier:
    """Système de notifications de mise à jour GitHub"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "update_config.json"
        self.github_repo = "TifouDragon/slimboy-discord-bot"
        self.current_version = "2.3.1"  # Version 2.3.1
        self.load_config()
        
    def load_config(self):
        """Charger la configuration des notifications"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "enabled": False,
                    "notification_channel_id": None,
                    "check_interval": 3600,  # 1 heure en secondes
                    "notify_prereleases": False,
                    "last_version_notified": None,
                    "auto_check": True,
                    "ping_admins": False
                }
                self.save_config()
        except Exception as e:
            logger.error(f"Erreur config update notifier: {e}")
            self.config = {}
    
    def save_config(self):
        """Sauvegarder la configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde config update: {e}")
    
    async def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """Vérifier les mises à jour sur GitHub"""
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        release_data = await response.json()
                        
                        latest_version = release_data.get("tag_name", "").lstrip("v")
                        is_prerelease = release_data.get("prerelease", False)
                        
                        # Vérifier si c'est une nouvelle version
                        if self.is_newer_version(latest_version) and \
                           (not is_prerelease or self.config.get("notify_prereleases", False)):
                            return release_data
                        
        except Exception as e:
            logger.error(f"Erreur vérification update: {e}")
        
        return None
    
    def is_newer_version(self, version: str) -> bool:
        """Vérifier si une version est plus récente"""
        try:
            def version_tuple(v):
                return tuple(map(int, v.split('.')))
            
            current = version_tuple(self.current_version)
            latest = version_tuple(version)
            
            return latest > current
        except:
            return False
    
    async def send_update_notification(self, release_data: Dict[str, Any]):
        """Envoyer une notification de mise à jour"""
        if not self.config.get("enabled", False):
            return
        
        channel_id = self.config.get("notification_channel_id")
        if not channel_id:
            return
        
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return
            
            embed = self.create_update_embed(release_data)
            
            content = ""
            if self.config.get("ping_admins", False):
                # Trouver les admins du serveur
                guild = channel.guild
                admins = [member for member in guild.members 
                         if member.guild_permissions.administrator and not member.bot]
                if admins:
                    content = " ".join([admin.mention for admin in admins[:5]])  # Limiter à 5
            
            await channel.send(content=content, embed=embed)
            
            # Marquer cette version comme notifiée
            self.config["last_version_notified"] = release_data.get("tag_name")
            self.save_config()
            
        except Exception as e:
            logger.error(f"Erreur envoi notification: {e}")
    
    def create_update_embed(self, release_data: Dict[str, Any]) -> discord.Embed:
        """Créer l'embed de notification de mise à jour"""
        version = release_data.get("tag_name", "Inconnue")
        title = release_data.get("name", f"Version {version}")
        body = release_data.get("body", "Aucune description")
        url = release_data.get("html_url", "")
        published_at = release_data.get("published_at", "")
        is_prerelease = release_data.get("prerelease", False)
        
        embed = discord.Embed(
            title=f"🚀 Nouvelle Mise à Jour Disponible !",
            description=f"**{title}**",
            color=0x00ff00 if not is_prerelease else 0xffa500,
            url=url
        )
        
        embed.add_field(
            name="📦 Version",
            value=f"`{version}`" + (" (Pré-release)" if is_prerelease else ""),
            inline=True
        )
        
        embed.add_field(
            name="📅 Date de sortie",
            value=f"<t:{int(datetime.fromisoformat(published_at.replace('Z', '+00:00')).timestamp())}:F>",
            inline=True
        )
        
        # Limiter la description à 1000 caractères
        if len(body) > 1000:
            body = body[:997] + "..."
        
        embed.add_field(
            name="📋 Nouveautés",
            value=body if body else "Voir le lien ci-dessus pour plus de détails",
            inline=False
        )
        
        embed.add_field(
            name="🔗 Liens Utiles",
            value=f"[📥 Télécharger]({url})\n[📚 Documentation](https://github.com/{self.github_repo}#readme)\n[🐛 Signaler un Bug](https://github.com/{self.github_repo}/issues)",
            inline=False
        )
        
        embed.set_footer(
            text="SlimBoy - Bot de Modération • Développé par @Ninja Iyed",
            icon_url="https://cdn.discordapp.com/emojis/1234567890123456789.png"  # Remplacer par votre icon
        )
        
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        
        return embed

class UpdateCommands(commands.Cog):
    """Commandes pour gérer les notifications de mise à jour"""
    
    def __init__(self, bot):
        self.bot = bot
        self.update_notifier = UpdateNotifier(bot)
        bot.update_notifier = self.update_notifier
        
        # Démarrer la tâche de vérification automatique
        if self.update_notifier.config.get("auto_check", True):
            self.update_check_task.start()
    
    def cog_unload(self):
        """Arrêter les tâches lors du déchargement"""
        self.update_check_task.cancel()
    
    @tasks.loop(hours=1)
    async def update_check_task(self):
        """Tâche de vérification automatique des mises à jour"""
        if self.update_notifier.config.get("enabled", False):
            release_data = await self.update_notifier.check_for_updates()
            if release_data:
                await self.update_notifier.send_update_notification(release_data)
    
    @update_check_task.before_loop
    async def before_update_check(self):
        """Attendre que le bot soit prêt"""
        await self.bot.wait_until_ready()
    
    @discord.app_commands.command(name="update_setup", description="🔔 Configurer les notifications de mise à jour")
    @discord.app_commands.describe(
        channel="Canal pour les notifications de mise à jour",
        enable="Activer ou désactiver les notifications"
    )
    async def update_setup(self, interaction: discord.Interaction,
                          channel: discord.TextChannel = None,
                          enable: bool = None):
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour configurer les notifications.",
                ephemeral=True
            )
            return
        
        if enable is not None:
            self.update_notifier.config["enabled"] = enable
        
        if channel:
            self.update_notifier.config["notification_channel_id"] = channel.id
        
        self.update_notifier.save_config()
        
        embed = discord.Embed(
            title="🔔 Configuration des Notifications",
            color=0x00ff00,
            description="Configuration mise à jour avec succès !"
        )
        
        embed.add_field(
            name="📊 Statut",
            value="✅ Activé" if self.update_notifier.config.get("enabled") else "❌ Désactivé",
            inline=True
        )
        
        if self.update_notifier.config.get("notification_channel_id"):
            notif_channel = self.bot.get_channel(self.update_notifier.config["notification_channel_id"])
            embed.add_field(
                name="📍 Canal",
                value=notif_channel.mention if notif_channel else "Canal non trouvé",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.app_commands.command(name="check_updates", description="🔍 Vérifier manuellement les mises à jour")
    async def check_updates(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=True)
        
        release_data = await self.update_notifier.check_for_updates()
        
        if release_data:
            embed = self.update_notifier.create_update_embed(release_data)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="✅ Aucune Mise à Jour",
                description="Vous utilisez déjà la dernière version du bot !",
                color=0x00ff00
            )
            embed.add_field(
                name="📦 Version Actuelle",
                value=f"`{self.update_notifier.current_version}`",
                inline=True
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UpdateCommands(bot))
