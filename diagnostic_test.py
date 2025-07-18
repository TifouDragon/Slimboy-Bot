
"""
Test de diagnostic pour vérifier le fonctionnement du bot
"""

import discord
from discord.ext import commands
import asyncio
import os
import psutil
import sys
import platform

class DiagnosticBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f"🤖 Bot de diagnostic connecté: {self.user}")
        print(f"📊 Serveurs connectés: {len(self.guilds)}")
        
        for guild in self.guilds:
            print(f"\n🏠 Serveur: {guild.name} (ID: {guild.id})")
            
            # Vérifier les permissions du bot
            bot_member = guild.me
            if bot_member:
                permissions = bot_member.guild_permissions
                print(f"  ✓ Permission bannir: {permissions.ban_members}")
                print(f"  ✓ Permission audit log: {permissions.view_audit_log}")
                print(f"  ✓ Permission slash commands: {permissions.use_slash_commands}")
            
            # Tester l'accès aux bannis
            try:
                bans = []
                async for ban_entry in guild.bans():
                    bans.append(ban_entry)
                    if len(bans) >= 3:  # Limiter pour le test
                        break
                print(f"  📋 Bannis trouvés: {len(bans)}")
                
                # Tester l'accès aux logs d'audit
                try:
                    audit_logs = []
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=3):
                        audit_logs.append(entry)
                    print(f"  📝 Logs d'audit accessibles: {len(audit_logs)}")
                except Exception as e:
                    print(f"  ❌ Impossible d'accéder aux logs d'audit: {e}")
                    
            except Exception as e:
                print(f"  ❌ Erreur d'accès aux bannis: {e}")
        
        # Informations système
        print(f"\n💻 Système:")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  Discord.py: {discord.__version__}")
        print(f"  CPU: {psutil.cpu_percent()}%")
        print(f"  RAM: {psutil.virtual_memory().percent}%")
        
        print("\n✅ Diagnostic terminé!")
        await self.close()

async def run_diagnostic():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ Token Discord manquant")
        print("Ajoutez votre token dans les Secrets de Replit avec la clé 'DISCORD_BOT_TOKEN'")
        return
    
    bot = DiagnosticBot()
    
    try:
        print("🔍 Démarrage du diagnostic...")
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.close()
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        await bot.close()

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
