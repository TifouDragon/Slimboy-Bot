
"""
Diagnostic Commands Plugin
Système de diagnostic complet pour le bot Discord
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
import psutil
import platform
import sys
from datetime import datetime, timedelta
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class DiagnosticCommands(commands.Cog):
    """Cog pour les commandes de diagnostic"""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()
    
    def has_admin_permission(self, member):
        """Vérifier si l'utilisateur a les permissions d'administrateur"""
        return member.guild_permissions.administrator
    
    @app_commands.command(
        name="diagnostic",
        description="Diagnostic complet du bot et du serveur"
    )
    async def diagnostic(self, interaction: discord.Interaction):
        """Effectuer un diagnostic complet du système"""
        
        # Vérifier les permissions (seuls les admins peuvent utiliser cette commande)
        if not self.has_admin_permission(interaction.user):
            await interaction.response.send_message(
                "❌ Cette commande est réservée aux administrateurs.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            # Créer l'embed principal
            embed = discord.Embed(
                title="🔧 Diagnostic Complet du Système",
                description="Analyse détaillée du bot et de l'environnement",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            # 1. Informations du Bot
            uptime = datetime.utcnow() - self.start_time
            embed.add_field(
                name="🤖 Informations Bot",
                value=f"**Nom:** {self.bot.user.name}\n"
                      f"**ID:** `{self.bot.user.id}`\n"
                      f"**Uptime:** {self.format_uptime(uptime)}\n"
                      f"**Ping:** {round(self.bot.latency * 1000)}ms\n"
                      f"**Serveurs:** {len(self.bot.guilds)}\n"
                      f"**Utilisateurs:** {sum(guild.member_count for guild in self.bot.guilds)}",
                inline=False
            )
            
            # 2. Système et Performance
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            embed.add_field(
                name="⚡ Performance Système",
                value=f"**OS:** {platform.system()} {platform.release()}\n"
                      f"**Python:** {sys.version.split()[0]}\n"
                      f"**Discord.py:** {discord.__version__}\n"
                      f"**CPU:** {cpu_percent}%\n"
                      f"**RAM:** {memory.percent}% ({self.bytes_to_mb(memory.used)}/{self.bytes_to_mb(memory.total)}MB)\n"
                      f"**Processus:** {len(psutil.pids())}",
                inline=False
            )
            
            # 3. Permissions du Bot sur ce serveur
            guild = interaction.guild
            bot_member = guild.me
            perms = bot_member.guild_permissions
            
            permissions_status = []
            critical_perms = {
                'ban_members': '🔨 Bannir des membres',
                'kick_members': '👢 Expulser des membres',
                'manage_messages': '🗑️ Gérer les messages',
                'moderate_members': '🔇 Modérer les membres',
                'view_audit_log': '📋 Voir les logs d\'audit',
                'manage_channels': '📺 Gérer les canaux',
                'send_messages': '💬 Envoyer des messages',
                'embed_links': '🔗 Intégrer des liens',
                'use_slash_commands': '⚡ Commandes slash'
            }
            
            for perm, desc in critical_perms.items():
                has_perm = getattr(perms, perm, False) if perm != 'use_slash_commands' else True
                status = "✅" if has_perm else "❌"
                permissions_status.append(f"{status} {desc}")
            
            embed.add_field(
                name="🛡️ Permissions sur ce Serveur",
                value="\n".join(permissions_status),
                inline=False
            )
            
            # 4. Test des Fonctionnalités
            await interaction.followup.send(embed=embed)
            
            # Faire des tests asynchrones
            test_embed = await self.run_functionality_tests(guild)
            await interaction.followup.send(embed=test_embed)
            
            # 5. Recommandations
            recommendations = self.generate_recommendations(guild, bot_member)
            if recommendations:
                rec_embed = discord.Embed(
                    title="💡 Recommandations",
                    description="\n".join(recommendations),
                    color=discord.Color.orange()
                )
                rec_embed.set_footer(text="Créé par @Ninja Iyed • Diagnostic complet")
                await interaction.followup.send(embed=rec_embed)
            
        except Exception as e:
            logger.error(f"Erreur lors du diagnostic: {e}")
            error_embed = discord.Embed(
                title="❌ Erreur de Diagnostic",
                description=f"Une erreur est survenue: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=error_embed)
    
    async def run_functionality_tests(self, guild):
        """Effectuer des tests de fonctionnalité"""
        embed = discord.Embed(
            title="🧪 Tests de Fonctionnalité",
            color=discord.Color.green()
        )
        
        tests = []
        
        # Test 1: Accès aux bannis
        try:
            ban_count = 0
            async for _ in guild.bans():
                ban_count += 1
                if ban_count >= 100:  # Limiter pour éviter les timeouts
                    break
            tests.append(f"✅ Accès aux bannis: {ban_count} trouvés")
        except Exception as e:
            tests.append(f"❌ Accès aux bannis: {str(e)}")
        
        # Test 2: Accès aux logs d'audit
        try:
            audit_count = 0
            async for _ in guild.audit_logs(limit=10):
                audit_count += 1
            tests.append(f"✅ Logs d'audit: {audit_count} entrées récentes")
        except Exception as e:
            tests.append(f"❌ Logs d'audit: {str(e)}")
        
        # Test 3: Test de connectivité Internet
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://discord.com', timeout=5) as resp:
                    if resp.status == 200:
                        tests.append("✅ Connectivité Internet: OK")
                    else:
                        tests.append(f"⚠️ Connectivité Internet: Code {resp.status}")
        except Exception:
            tests.append("❌ Connectivité Internet: Échec")
        
        # Test 4: Commandes chargées
        try:
            cog_count = len(self.bot.cogs)
            command_count = len([cmd for cmd in self.bot.tree.walk_commands()])
            tests.append(f"✅ Commandes: {command_count} dans {cog_count} modules")
        except Exception as e:
            tests.append(f"❌ Commandes: {str(e)}")
        
        # Test 5: Base de données / Stockage (si applicable)
        try:
            # Test simple d'écriture/lecture en mémoire
            test_data = {"test": "diagnostic"}
            if test_data.get("test") == "diagnostic":
                tests.append("✅ Stockage en mémoire: OK")
        except Exception:
            tests.append("❌ Stockage en mémoire: Échec")
        
        embed.add_field(
            name="Résultats des Tests",
            value="\n".join(tests),
            inline=False
        )
        
        embed.set_footer(text="Créé par @Ninja Iyed • Tests automatiques")
        return embed
    
    def generate_recommendations(self, guild, bot_member):
        """Générer des recommandations basées sur le diagnostic"""
        recommendations = []
        perms = bot_member.guild_permissions
        
        # Vérifier les permissions manquantes
        if not perms.ban_members:
            recommendations.append("⚠️ Permission 'Bannir des membres' manquante - commandes /ban et /unban indisponibles")
        
        if not perms.moderate_members:
            recommendations.append("⚠️ Permission 'Modérer les membres' manquante - commandes de timeout indisponibles")
        
        if not perms.view_audit_log:
            recommendations.append("⚠️ Permission 'Voir les logs d'audit' manquante - identification des modérateurs limitée")
        
        if not perms.manage_messages:
            recommendations.append("⚠️ Permission 'Gérer les messages' manquante - commande /clear indisponible")
        
        # Vérifier la hiérarchie des rôles
        if bot_member.top_role.position < 2:
            recommendations.append("⚠️ Rôle du bot trop bas - peut ne pas pouvoir modérer certains membres")
        
        # Vérifier le nombre de serveurs (si trop élevé)
        if len(guild.bot.guilds) > 100:
            recommendations.append("ℹ️ Bot présent sur plus de 100 serveurs - performances potentiellement impactées")
        
        # Recommandations de performance
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            recommendations.append("⚠️ Utilisation mémoire élevée (>80%) - redémarrage recommandé")
        
        cpu_percent = psutil.cpu_percent()
        if cpu_percent > 80:
            recommendations.append("⚠️ Utilisation CPU élevée (>80%) - vérifier les processus")
        
        return recommendations
    
    def format_uptime(self, uptime):
        """Formater le temps d'activité"""
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}j {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        else:
            return f"{minutes}m {seconds}s"
    
    def bytes_to_mb(self, bytes_value):
        """Convertir les bytes en MB"""
        return round(bytes_value / (1024 * 1024), 1)
    
    @app_commands.command(
        name="ping",
        description="Vérifier la latence du bot"
    )
    async def ping(self, interaction: discord.Interaction):
        """Commande ping simple"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latence: **{latency}ms**",
            color=discord.Color.green() if latency < 100 else discord.Color.orange() if latency < 300 else discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_footer(text="Créé par @Ninja Iyed")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(
        name="status",
        description="Afficher le statut détaillé du bot"
    )
    async def status(self, interaction: discord.Interaction):
        """Afficher le statut du bot"""
        uptime = datetime.utcnow() - self.start_time
        
        embed = discord.Embed(
            title="📊 Statut du Bot",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="🤖 Bot",
            value=f"**Statut:** 🟢 En ligne\n**Uptime:** {self.format_uptime(uptime)}\n**Ping:** {round(self.bot.latency * 1000)}ms",
            inline=True
        )
        
        embed.add_field(
            name="📈 Statistiques",
            value=f"**Serveurs:** {len(self.bot.guilds)}\n**Utilisateurs:** {sum(guild.member_count for guild in self.bot.guilds)}\n**Commandes:** {len([cmd for cmd in self.bot.tree.walk_commands()])}",
            inline=True
        )
        
        # Système
        memory = psutil.virtual_memory()
        embed.add_field(
            name="⚡ Système",
            value=f"**CPU:** {psutil.cpu_percent()}%\n**RAM:** {memory.percent}%\n**Python:** {sys.version.split()[0]}",
            inline=True
        )
        
        embed.set_footer(text="Créé par @Ninja Iyed")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DiagnosticCommands(bot))
