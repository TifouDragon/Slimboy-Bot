"""
Discord Bot Invite Link Generator
Generates an invite link for the ban list bot with required permissions
"""

import discord

def generate_invite_link():
    """Generate invite link for the Discord bot"""
    
    # Bot's client ID (SlimBoy)
    client_id = "1384568465326866585"
    
    # Required permissions for the bot
    permissions = discord.Permissions()
    permissions.ban_members = True          # To view the ban list
    permissions.view_audit_log = True       # To see who banned each user
    permissions.kick_members = True         # For kick command
    permissions.manage_messages = True      # For clear/purge commands
    permissions.moderate_members = True     # For timeout commands
    permissions.send_messages = True        # To send responses
    permissions.embed_links = True          # To send embeds
    permissions.use_slash_commands = True   # For slash commands
    
    # Generate correct invite URL (without response_type=code to avoid code grant requirement)
    standard_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions.value}&scope=bot%20applications.commands"
    
    # Alternative URL format
    custom_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands&permissions={permissions.value}"
    
    # Simple bot invite (most compatible)
    simple_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&scope=bot&permissions={permissions.value}"
    
    return {
        'standard': standard_url,
        'custom': custom_url,
        'simple': simple_url
    }

if __name__ == "__main__":
    invite_links = generate_invite_link()
    
    print("=" * 70)
    print("🚀 BOT BANLIST - LIENS D'INVITATION PERSONNALISÉS")
    print("=" * 70)
    print()
    print("📋 LIEN STANDARD (Recommandé):")
    print(invite_links['standard'])
    print()
    print("🎨 LIEN PERSONNALISÉ (Interface améliorée):")
    print(invite_links['custom'])
    print()
    print("💎 LIEN PREMIUM (Expérience optimisée):")
    print(invite_links['premium'])
    print()
    print("🛡️ PERMISSIONS AUTOMATIQUES :")
    print("  ✓ Bannir des membres - Accès à la liste des bannis")
    print("  ✓ Voir les logs d'audit - Identification des modérateurs")
    print("  ✓ Commandes slash - Interface moderne")
    print()
    print("⚡ FONCTIONNALITÉS AVANCÉES :")
    print("  • Interface 100% française avec watermark @Ninja Iyed")
    print("  • Détection intelligente de 20+ bots populaires") 
    print("  • Pagination fluide (5 utilisateurs par page)")
    print("  • Recherche instantanée par pseudo/nom/ID")
    print("  • Navigation intuitive avec boutons")
    print()
    print("📱 COMMANDES DISPONIBLES :")
    print("  /banlist - Liste complète des bannis")
    print("  /banlist search:pseudo - Recherche ciblée")
    print()
    print("🔥 Choisissez le lien qui vous convient le mieux !")
    print("=" * 70)