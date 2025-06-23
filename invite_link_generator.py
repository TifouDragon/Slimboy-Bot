
"""
Générateur de lien d'invitation Discord pour SlimBoy Version II
Génère automatiquement le lien avec les bonnes permissions
"""

import os

def generate_invite_link():
    """Génère le lien d'invitation Discord pour le bot"""
    
    # Instructions pour obtenir le CLIENT_ID
    print("🤖 SlimBoy Version II - Générateur de Lien d'Invitation")
    print("=" * 60)
    print()
    print("📋 Pour obtenir votre CLIENT_ID :")
    print("1. Allez sur https://discord.com/developers/applications")
    print("2. Sélectionnez votre application SlimBoy")
    print("3. Dans 'General Information', copiez 'Application ID'")
    print()
    
    # Demander le CLIENT_ID
    client_id = input("🔑 Entrez votre CLIENT_ID (Application ID) : ").strip()
    
    if not client_id:
        print("❌ CLIENT_ID requis !")
        return
    
    if not client_id.isdigit():
        print("❌ CLIENT_ID doit être un nombre !")
        return
    
    # Permissions nécessaires pour SlimBoy Version II
    # Permission value 8 = Administrator (toutes permissions)
    permissions = "8"
    
    # Générer le lien complet
    invite_link = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
    
    print()
    print("✅ Lien d'invitation généré avec succès !")
    print("🔗 Voici votre lien d'invitation SlimBoy Version II :")
    print()
    print("=" * 80)
    print(invite_link)
    print("=" * 80)
    print()
    print("📋 Ce lien donne les permissions suivantes :")
    print("✅ Administrateur (toutes permissions)")
    print("   └── Modération complète")
    print("   └── Gestion des bans")
    print("   └── Accès aux logs d'audit")
    print("   └── Gestion des messages et canaux")
    print("   └── Toutes les fonctionnalités Version II")
    print()
    print("🎯 Instructions d'utilisation :")
    print("1. Copiez le lien ci-dessus")
    print("2. Ouvrez-le dans votre navigateur")
    print("3. Sélectionnez votre serveur Discord")
    print("4. Autorisez toutes les permissions")
    print("5. Votre bot SlimBoy est prêt !")
    print()
    print("💡 Conseil : Sauvegardez ce lien pour inviter le bot sur d'autres serveurs")
    
    # Sauvegarder dans un fichier
    try:
        with open("bot_invite_link.txt", "w", encoding="utf-8") as f:
            f.write(f"SlimBoy Version II - Lien d'Invitation\n")
            f.write(f"Client ID: {client_id}\n")
            f.write(f"Lien: {invite_link}\n")
            f.write(f"Généré le: {__import__('datetime').datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        print("💾 Lien sauvegardé dans 'bot_invite_link.txt'")
    except:
        print("⚠️ Impossible de sauvegarder le fichier")

if __name__ == "__main__":
    generate_invite_link()
