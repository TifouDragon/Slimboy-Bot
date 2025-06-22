
"""
Discord Bot Invite Link Generator
Generates an invite link for the ban list bot with all permissions
"""

import discord

def generate_invite_link():
    """Generate invite link for the Discord bot"""
    
    # Bot's client ID (SlimBoy)
    client_id = "1384568465326866585"
    
    # ALL permissions for the bot
    permissions = discord.Permissions()
    permissions.administrator = True            # Admin - donne toutes les permissions
    permissions.ban_members = True              # Bannir des membres
    permissions.view_audit_log = True           # Voir les logs d'audit
    permissions.kick_members = True             # Expulser des membres
    permissions.manage_messages = True          # Gérer les messages
    permissions.moderate_members = True         # Modérer les membres (timeout)
    permissions.send_messages = True            # Envoyer des messages
    permissions.embed_links = True              # Intégrer des liens
    permissions.manage_channels = True          # Gérer les canaux
    permissions.manage_guild = True             # Gérer le serveur
    permissions.manage_roles = True             # Gérer les rôles
    permissions.manage_nicknames = True         # Gérer les pseudos
    permissions.manage_webhooks = True          # Gérer les webhooks
    permissions.read_messages = True            # Lire les messages
    permissions.send_messages_in_threads = True # Messages dans threads
    permissions.create_public_threads = True    # Créer threads publics
    permissions.create_private_threads = True   # Créer threads privés
    permissions.manage_threads = True           # Gérer les threads
    permissions.use_slash_commands = True       # Utiliser les commandes slash
    permissions.mention_everyone = True         # Mentionner @everyone
    permissions.add_reactions = True            # Ajouter des réactions
    permissions.attach_files = True             # Joindre des fichiers
    permissions.read_message_history = True     # Lire l'historique
    permissions.use_external_emojis = True      # Utiliser emojis externes
    permissions.connect = True                  # Se connecter aux vocaux
    permissions.speak = True                    # Parler en vocal
    permissions.mute_members = True             # Couper le micro
    permissions.deafen_members = True           # Mettre en sourdine
    permissions.move_members = True             # Déplacer les membres
    permissions.use_voice_activation = True     # Activation vocale
    
    # Generate invite URLs with ALL permissions
    standard_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions.value}&scope=bot%20applications.commands"
    custom_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands&permissions={permissions.value}"
    simple_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&scope=bot&permissions={permissions.value}"
    
    return {
        'standard': standard_url,
        'custom': custom_url,
        'simple': simple_url
    }

if __name__ == "__main__":
    invite_links = generate_invite_link()
    
    print("=" * 70)
    print("🚀 BOT BANLIST - LIENS D'INVITATION AVEC TOUTES LES PERMISSIONS")
    print("=" * 70)
    print()
    print("📋 LIEN STANDARD (Recommandé):")
    print(invite_links['standard'])
    print()
    print("🎨 LIEN PERSONNALISÉ:")
    print(invite_links['custom'])
    print()
    print("💎 LIEN SIMPLE:")
    print(invite_links['simple'])
    print()
    print("🛡️ PERMISSIONS ACCORDÉES :")
    print("  ✓ 👑 ADMINISTRATEUR - Toutes les permissions")
    print("  ✓ Bannir/Débannir des membres")
    print("  ✓ Expulser des membres")
    print("  ✓ Modérer les membres (timeout)")
    print("  ✓ Gérer les messages/canaux/rôles")
    print("  ✓ Voir les logs d'audit")
    print("  ✓ Gérer le serveur complet")
    print()
    print("⚡ FONCTIONNALITÉS COMPLÈTES :")
    print("  • Interface 100% française")
    print("  • Modération avancée avec durées illimitées")
    print("  • Gestion complète des bannis et timeouts")
    print("  • Commandes de simulation réalistes")
    print("  • Diagnostic système complet")
    print()
    print("📱 TOUTES LES COMMANDES DISPONIBLES :")
    print("  /banlist - Liste des bannis avec recherche")
    print("  /ban /tempban /ipban /unban - Gestion bans")
    print("  /timeout /untimeout /automute - Gestion timeouts")
    print("  /kick /warn /clear - Modération standard")
    print("  /fakeban /fakemute - Simulations")
    print("  /userinfo /slowmode /diagnostic - Utilitaires")
    print()
    print("🔥 Le bot aura TOUS les droits administrateur !")
    print("=" * 70)
