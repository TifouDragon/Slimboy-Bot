
"""
Système de Salons Temporaires
Commandes pour créer des salons texte et vocaux temporaires qui se suppriment automatiquement
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
import json
import os
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class TempChannelsCommands(commands.Cog):
    """Cog pour les commandes de salons temporaires"""

    def __init__(self, bot):
        self.bot = bot
        self.temp_channels_file = "temp_channels.json"
        self.temp_channels = self.load_temp_channels()
        self.cleanup_task = None
        self.start_cleanup_task()

    def load_temp_channels(self):
        """Charger les données des salons temporaires"""
        try:
            if os.path.exists(self.temp_channels_file):
                with open(self.temp_channels_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading temp channels data: {e}")
        return {}

    def save_temp_channels(self):
        """Sauvegarder les données des salons temporaires"""
        try:
            with open(self.temp_channels_file, 'w', encoding='utf-8') as f:
                json.dump(self.temp_channels, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving temp channels data: {e}")

    def start_cleanup_task(self):
        """Démarrer la tâche de nettoyage automatique"""
        if self.cleanup_task is None or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self.cleanup_expired_channels())

    async def cleanup_expired_channels(self):
        """Tâche de nettoyage des salons expirés"""
        while True:
            try:
                await asyncio.sleep(60)  # Vérifier toutes les minutes
                current_time = datetime.now()
                expired_channels = []

                for channel_id, data in self.temp_channels.items():
                    expire_time = datetime.fromisoformat(data['expires_at'])
                    if current_time >= expire_time:
                        expired_channels.append(channel_id)

                for channel_id in expired_channels:
                    await self.delete_temp_channel(int(channel_id))

            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(300)  # Attendre 5 minutes avant de reprendre

    async def delete_temp_channel(self, channel_id: int):
        """Supprimer un salon temporaire"""
        try:
            channel = self.bot.get_channel(channel_id)
            if channel:
                # Envoyer un message d'avertissement avant suppression
                try:
                    embed = discord.Embed(
                        title="⏰ Salon Temporaire Expiré",
                        description="Ce salon temporaire va être supprimé dans 30 secondes.",
                        color=discord.Color.orange(),
                        timestamp=datetime.utcnow()
                    )
                    embed.set_footer(text="Créé par @Ninja Iyed")
                    
                    if isinstance(channel, discord.TextChannel):
                        await channel.send(embed=embed)
                    
                    # Attendre 30 secondes
                    await asyncio.sleep(30)
                    
                    # Supprimer le salon
                    await channel.delete(reason="Salon temporaire expiré")
                    logger.info(f"Deleted expired temp channel: {channel.name}")
                    
                except discord.NotFound:
                    pass  # Le salon a déjà été supprimé
                except Exception as e:
                    logger.error(f"Error deleting temp channel {channel_id}: {e}")

            # Retirer de la liste des salons temporaires
            if str(channel_id) in self.temp_channels:
                del self.temp_channels[str(channel_id)]
                self.save_temp_channels()

        except Exception as e:
            logger.error(f"Error in delete_temp_channel: {e}")

    def has_manage_channels_permission(self, member):
        """Vérifier si l'utilisateur peut gérer les salons"""
        return (
            member.guild_permissions.administrator or 
            member.guild_permissions.manage_channels or
            member.guild_permissions.manage_guild
        )

    def parse_duration(self, duration_str):
        """Parser la durée en secondes"""
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
                seconds = value * multipliers[unit]
                
                # Limites de durée
                if seconds < 60:  # Minimum 1 minute
                    return None
                if seconds > 604800:  # Maximum 1 semaine
                    return None
                    
                return seconds
            else:
                # Assumer minutes si pas d'unité
                minutes = int(duration_str)
                if minutes < 1 or minutes > 10080:  # 1 minute à 1 semaine
                    return None
                return minutes * 60
        except (ValueError, IndexError):
            return None

    @app_commands.command(
        name="temp-text",
        description="Créer un salon texte temporaire"
    )
    @app_commands.describe(
        name="Nom du salon temporaire",
        duration="Durée (ex: 30m, 2h, 1d, 1w)",
        category="Catégorie où créer le salon (optionnel)",
        reason="Raison de la création"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def create_temp_text(self, interaction: discord.Interaction, name: str, duration: str, category: Optional[discord.CategoryChannel] = None, reason: str = "Salon temporaire"):
        """Créer un salon texte temporaire"""

        # Vérifier les permissions
        if not self.has_manage_channels_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions pour gérer les salons.",
                ephemeral=True
            )
            return

        # Vérifier les permissions du bot
        if not interaction.guild.me.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de gérer les salons.",
                ephemeral=True
            )
            return

        # Parser la durée
        duration_seconds = self.parse_duration(duration)
        if duration_seconds is None:
            await interaction.response.send_message(
                "❌ Durée invalide. Utilisez: 30m, 2h, 1d, 1w (minimum 1 minute, maximum 1 semaine)",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer()

            # Nettoyer le nom du salon
            clean_name = name.lower().replace(' ', '-')[:100]
            
            # Créer le salon
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    manage_messages=True
                )
            }

            channel = await interaction.guild.create_text_channel(
                name=clean_name,
                category=category,
                reason=f"Salon temporaire créé par {interaction.user} - {reason}",
                overwrites=overwrites
            )

            # Calculer le temps d'expiration
            expire_time = datetime.now() + timedelta(seconds=duration_seconds)

            # Sauvegarder les informations
            self.temp_channels[str(channel.id)] = {
                'type': 'text',
                'name': channel.name,
                'created_by': interaction.user.id,
                'created_at': datetime.now().isoformat(),
                'expires_at': expire_time.isoformat(),
                'duration': duration,
                'guild_id': interaction.guild.id,
                'reason': reason
            }
            self.save_temp_channels()

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="📝 Salon Texte Temporaire Créé",
                description=f"Le salon {channel.mention} a été créé avec succès !",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Salon", value=channel.mention, inline=True)
            embed.add_field(name="Durée", value=duration, inline=True)
            embed.add_field(name="Créé par", value=interaction.user.mention, inline=True)
            embed.add_field(name="Expire le", value=f"<t:{int(expire_time.timestamp())}:F>", inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)

            embed.set_footer(text="Créé par @Ninja Iyed")

            await interaction.followup.send(embed=embed)

            # Envoyer un message dans le nouveau salon
            welcome_embed = discord.Embed(
                title="🎉 Bienvenue dans ce salon temporaire !",
                description=f"Ce salon a été créé par {interaction.user.mention} et sera automatiquement supprimé le <t:{int(expire_time.timestamp())}:F>.",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            welcome_embed.add_field(name="Durée restante", value=f"⏰ {duration}", inline=True)
            welcome_embed.add_field(name="Raison", value=reason, inline=True)
            welcome_embed.set_footer(text="Créé par @Ninja Iyed • Salon temporaire")

            await channel.send(embed=welcome_embed)

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour créer ce salon.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la création du salon: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="temp-voice",
        description="Créer un salon vocal temporaire"
    )
    @app_commands.describe(
        name="Nom du salon vocal temporaire",
        duration="Durée (ex: 30m, 2h, 1d, 1w)",
        user_limit="Limite d'utilisateurs (0 = illimité)",
        category="Catégorie où créer le salon (optionnel)",
        reason="Raison de la création"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def create_temp_voice(self, interaction: discord.Interaction, name: str, duration: str, user_limit: int = 0, category: Optional[discord.CategoryChannel] = None, reason: str = "Salon vocal temporaire"):
        """Créer un salon vocal temporaire"""

        # Vérifier les permissions
        if not self.has_manage_channels_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions pour gérer les salons.",
                ephemeral=True
            )
            return

        # Vérifier les permissions du bot
        if not interaction.guild.me.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission de gérer les salons.",
                ephemeral=True
            )
            return

        # Parser la durée
        duration_seconds = self.parse_duration(duration)
        if duration_seconds is None:
            await interaction.response.send_message(
                "❌ Durée invalide. Utilisez: 30m, 2h, 1d, 1w (minimum 1 minute, maximum 1 semaine)",
                ephemeral=True
            )
            return

        # Valider la limite d'utilisateurs
        if user_limit < 0 or user_limit > 99:
            await interaction.response.send_message(
                "❌ La limite d'utilisateurs doit être entre 0 et 99 (0 = illimité).",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer()

            # Nettoyer le nom du salon
            clean_name = name[:100]
            
            # Créer le salon vocal
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(connect=True),
                interaction.guild.me: discord.PermissionOverwrite(
                    connect=True,
                    manage_channels=True,
                    move_members=True
                )
            }

            channel = await interaction.guild.create_voice_channel(
                name=clean_name,
                category=category,
                user_limit=user_limit if user_limit > 0 else None,
                reason=f"Salon vocal temporaire créé par {interaction.user} - {reason}",
                overwrites=overwrites
            )

            # Calculer le temps d'expiration
            expire_time = datetime.now() + timedelta(seconds=duration_seconds)

            # Sauvegarder les informations
            self.temp_channels[str(channel.id)] = {
                'type': 'voice',
                'name': channel.name,
                'created_by': interaction.user.id,
                'created_at': datetime.now().isoformat(),
                'expires_at': expire_time.isoformat(),
                'duration': duration,
                'guild_id': interaction.guild.id,
                'user_limit': user_limit,
                'reason': reason
            }
            self.save_temp_channels()

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="🔊 Salon Vocal Temporaire Créé",
                description=f"Le salon vocal **{channel.name}** a été créé avec succès !",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Salon", value=f"🔊 {channel.name}", inline=True)
            embed.add_field(name="Durée", value=duration, inline=True)
            embed.add_field(name="Créé par", value=interaction.user.mention, inline=True)
            embed.add_field(name="Limite utilisateurs", value=f"{user_limit} utilisateurs" if user_limit > 0 else "Illimité", inline=True)
            embed.add_field(name="Expire le", value=f"<t:{int(expire_time.timestamp())}:F>", inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)

            embed.set_footer(text="Créé par @Ninja Iyed")

            await interaction.followup.send(embed=embed)

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour créer ce salon vocal.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la création du salon vocal: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="temp-list",
        description="Afficher la liste des salons temporaires actifs"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def list_temp_channels(self, interaction: discord.Interaction):
        """Lister les salons temporaires actifs"""

        try:
            await interaction.response.defer()

            guild_temp_channels = {
                k: v for k, v in self.temp_channels.items() 
                if v.get('guild_id') == interaction.guild.id
            }

            if not guild_temp_channels:
                embed = discord.Embed(
                    title="📋 Salons Temporaires",
                    description="Aucun salon temporaire actif sur ce serveur.",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text="Créé par @Ninja Iyed")
                await interaction.followup.send(embed=embed)
                return

            embed = discord.Embed(
                title="📋 Salons Temporaires Actifs",
                description=f"Liste des salons temporaires sur **{interaction.guild.name}**",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            for channel_id, data in guild_temp_channels.items():
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    expire_time = datetime.fromisoformat(data['expires_at'])
                    created_by = interaction.guild.get_member(data['created_by'])
                    
                    channel_type = "📝" if data['type'] == 'text' else "🔊"
                    
                    field_value = f"**Type:** {channel_type} {data['type'].title()}\n"
                    field_value += f"**Créé par:** {created_by.mention if created_by else 'Utilisateur introuvable'}\n"
                    field_value += f"**Expire:** <t:{int(expire_time.timestamp())}:R>\n"
                    field_value += f"**Raison:** {data.get('reason', 'Aucune')}"
                    
                    if data['type'] == 'voice' and data.get('user_limit', 0) > 0:
                        field_value += f"\n**Limite:** {data['user_limit']} utilisateurs"

                    embed.add_field(
                        name=f"{channel_type} {channel.name}",
                        value=field_value,
                        inline=False
                    )

            embed.set_footer(text=f"Total: {len(guild_temp_channels)} salons • Créé par @Ninja Iyed")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de l'affichage de la liste: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="temp-extend",
        description="Prolonger la durée d'un salon temporaire"
    )
    @app_commands.describe(
        channel="Le salon temporaire à prolonger",
        additional_duration="Durée supplémentaire (ex: 30m, 1h, 2d)"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def extend_temp_channel(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel, additional_duration: str):
        """Prolonger un salon temporaire"""

        # Vérifier les permissions
        if not self.has_manage_channels_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions pour gérer les salons.",
                ephemeral=True
            )
            return

        # Vérifier si c'est un salon temporaire
        if str(channel.id) not in self.temp_channels:
            await interaction.response.send_message(
                "❌ Ce salon n'est pas un salon temporaire.",
                ephemeral=True
            )
            return

        # Parser la durée supplémentaire
        duration_seconds = self.parse_duration(additional_duration)
        if duration_seconds is None:
            await interaction.response.send_message(
                "❌ Durée invalide. Utilisez: 30m, 2h, 1d, 1w",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer()

            # Mettre à jour le temps d'expiration
            current_expire = datetime.fromisoformat(self.temp_channels[str(channel.id)]['expires_at'])
            new_expire = current_expire + timedelta(seconds=duration_seconds)
            
            # Vérifier que la nouvelle durée totale ne dépasse pas 1 semaine depuis maintenant
            max_expire = datetime.now() + timedelta(weeks=1)
            if new_expire > max_expire:
                await interaction.followup.send(
                    "❌ La durée totale ne peut pas dépasser 1 semaine à partir de maintenant.",
                    ephemeral=True
                )
                return

            self.temp_channels[str(channel.id)]['expires_at'] = new_expire.isoformat()
            self.save_temp_channels()

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="⏰ Salon Temporaire Prolongé",
                description=f"La durée du salon **{channel.name}** a été prolongée !",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Salon", value=channel.mention if hasattr(channel, 'mention') else channel.name, inline=True)
            embed.add_field(name="Durée ajoutée", value=additional_duration, inline=True)
            embed.add_field(name="Nouveau délai d'expiration", value=f"<t:{int(new_expire.timestamp())}:F>", inline=True)
            embed.add_field(name="Prolongé par", value=interaction.user.mention, inline=True)

            embed.set_footer(text="Créé par @Ninja Iyed")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la prolongation: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="temp-delete",
        description="Supprimer manuellement un salon temporaire"
    )
    @app_commands.describe(
        channel="Le salon temporaire à supprimer"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def delete_temp_channel_manual(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        """Supprimer manuellement un salon temporaire"""

        # Vérifier les permissions
        if not self.has_manage_channels_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Vous n'avez pas les permissions pour gérer les salons.",
                ephemeral=True
            )
            return

        # Vérifier si c'est un salon temporaire
        if str(channel.id) not in self.temp_channels:
            await interaction.response.send_message(
                "❌ Ce salon n'est pas un salon temporaire.",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer()

            channel_name = channel.name
            channel_type = self.temp_channels[str(channel.id)]['type']

            # Supprimer le salon
            await channel.delete(reason=f"Salon temporaire supprimé manuellement par {interaction.user}")

            # Retirer de la liste
            del self.temp_channels[str(channel.id)]
            self.save_temp_channels()

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="🗑️ Salon Temporaire Supprimé",
                description=f"Le salon **{channel_name}** a été supprimé avec succès !",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Nom du salon", value=channel_name, inline=True)
            embed.add_field(name="Type", value=channel_type.title(), inline=True)
            embed.add_field(name="Supprimé par", value=interaction.user.mention, inline=True)

            embed.set_footer(text="Créé par @Ninja Iyed")

            await interaction.followup.send(embed=embed)

        except discord.NotFound:
            await interaction.followup.send(
                "❌ Le salon a déjà été supprimé.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions pour supprimer ce salon.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la suppression: {str(e)}",
                ephemeral=True
            )

    def cog_unload(self):
        """Nettoyer lors du déchargement du cog"""
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()

async def setup(bot):
    await bot.add_cog(TempChannelsCommands(bot))
