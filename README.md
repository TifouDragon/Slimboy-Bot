
# 🤖 SlimBoy - Discord Moderation Bot - Version 2.2

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.5.2+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Replit](https://img.shields.io/badge/Replit-Ready-orange.svg)](https://replit.com)

> 🚀 **Version 2.2** - Bot Discord de modération avancé avec système de logs, notifications GitHub et commandes bonus ! Interface française complète avec pagination interactive optimisée pour Replit.

---

## ✨ Nouveautés Version 2.2

### 🔥 Fonctionnalités Révolutionnaires
- **📝 Système de Logs Configurable** - Enregistrement automatique de toutes les actions de modération
- **🔔 Notifications GitHub** - Alertes automatiques pour les nouvelles versions
- **🎯 Commandes Bonus** - Extensions fun et utilitaires (en développement actif)
- **🌐 Dashboard Web** - Interface de gestion prévue pour les prochaines versions
- **🤖 IA Modération** - Détection intelligente prévue dans les futures mises à jour

### 🛡️ Modération Avancée (Améliorée)
- **📋 Liste des bannis** avec pagination interactive (5 par page)
- **🔍 Recherche intelligente** par pseudo, nom d'utilisateur ou ID Discord
- **⚡ Gestion complète des bans** : bannir, débannir, ban temporaire, ban IP
- **🛠️ Modération standard** : kick, timeout, clear messages avec durées illimitées
- **👤 Informations utilisateur** détaillées avec âge du compte et historique

### 🎨 Interface Moderne 2.0
- **🎭 Embeds Discord** avec design professionnel nouvelle génération
- **🎮 Boutons interactifs** pour navigation fluide et intuitive
- **📱 Messages d'erreur** informatifs en français avec suggestions
- **🏷️ Watermark créateur** sur tous les embeds avec style uniforme

### 🔧 Systèmes Intelligents
- **📊 Logs Configurables** - Choix des événements à enregistrer
- **🔔 Alertes Automatiques** - Notifications Discord pour mises à jour GitHub
- **🤖 Détection de bots** automatique (25+ bots populaires reconnus)
- **📈 Monitoring avancé** avec endpoints API complets
- **🔄 Keep-alive optimisé** avec serveur Flask intégré Version II

---

## 🚀 Déploiement Rapide

### Option Replit (Recommandé)

[![Run on Replit](https://replit.com/badge/github/TifouDragon/slimboy-discord-bot)](https://replit.com/@TifouDragon/slimboy-discord-bot)

1. **Fork ce projet** sur Replit
2. **Ajoutez votre token** dans les Secrets (🔒)
   - Clé : `DISCORD_BOT_TOKEN`
   - Valeur : Votre token Discord
3. **Lancez** avec le bouton Run
4. **Profitez** de toutes les fonctionnalités !

---

## 🔧 Configuration Discord Complète

### 🔑 Tokens et IDs Nécessaires

#### **1. DISCORD_BOT_TOKEN** (OBLIGATOIRE ⚠️)
- **Description** : Token d'authentification de votre bot Discord
- **Où l'obtenir** :
  1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
  2. **New Application** → Nom : "SlimBoy Version 2.2"
  3. Onglet **Bot** → **Reset Token** → **Copiez le token**
- **Comment l'ajouter dans Replit** :
  - Cliquez sur l'onglet **Secrets** (🔒) dans votre Repl
  - **Clé** : `DISCORD_BOT_TOKEN`
  - **Valeur** : Votre token Discord (commence par "MTM...")

#### **2. CLIENT_ID** (Pour invitation uniquement)
- **Description** : ID de votre application Discord (Application ID)
- **Où l'obtenir** :
  - Discord Developer Portal → Votre Application → **General Information** → **Application ID**
- **Utilisation** : Nécessaire **UNIQUEMENT** pour générer le lien d'invitation du bot
- **Exemple** : `1384568465326866585`
- **⚠️ Note** : Le CLIENT_ID n'est **PAS** obligatoire pour faire fonctionner le bot !

### ⚠️ **IMPORTANT : Distinction des tokens**
- **DISCORD_BOT_TOKEN** : ✅ **OBLIGATOIRE** - Pour que le bot se connecte à Discord
- **CLIENT_ID** : ❌ **OPTIONNEL** - Seulement pour créer le lien d'invitation

### ⚡ Configuration Rapide

1. **Créez l'application Discord** et récupérez le **DISCORD_BOT_TOKEN** (onglet Bot)
2. **Ajoutez le token** dans les Secrets Replit (clé: `DISCORD_BOT_TOKEN`)
3. **Lancez le bot** avec le bouton Run ✅

**Optionnel - Pour invitation :**
4. **Récupérez le CLIENT_ID** (onglet General Information) 
5. **Générez le lien d'invitation** avec votre CLIENT_ID
6. **Invitez le bot** sur votre serveur Discord

### 🔗 Génération du Lien d'Invitation

**Format du lien** (remplacez `VOTRE_CLIENT_ID`) :
```
https://discord.com/oauth2/authorize?client_id=VOTRE_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

**Exemple avec CLIENT_ID** :
```
https://discord.com/oauth2/authorize?client_id=1384568465326866585&permissions=8&scope=bot%20applications.commands
```

### 3. Permissions Requises (Automatiques)
✅ **Administrateur** - Accès complet pour toutes les fonctionnalités
- Bannir des membres, Gérer le serveur, Voir les logs d'audit
- Gérer les messages, Gérer les canaux, Modérer les membres
- Envoyer des messages, Incorporer des liens, Réactions

---

## 📋 Commandes Disponibles

### 🛡️ Modération Avancée
```bash
/banlist                          # Liste complète des bannis
/banlist user:pseudo              # Recherche par pseudo
/banlist user:@utilisateur        # Recherche par mention
/banlist user:123456789           # Recherche par ID

/ban @utilisateur raison          # Bannir un utilisateur
/unban 123456789                  # Débannir par ID
/kick @utilisateur raison         # Expulser un utilisateur
/timeout @utilisateur 10m         # Timeout (durée illimitée supportée)
/tempban @utilisateur 7d raison   # Ban temporaire automatique
/ipban @utilisateur raison        # Ban IP + suppression messages
```

### 🎭 Commandes de Simulation
```bash
/fakeban @utilisateur             # Simulation réaliste de ban
/fakemute @utilisateur            # Simulation réaliste de mute
```

### 📝 Système de Logs (NOUVEAU!)
```bash
/logs_setup channel:#logs         # Configurer canal de logs
/logs_setup enable:true           # Activer/désactiver logs
/logs_types                       # Choisir types de logs à enregistrer
```

### 🔔 Notifications GitHub (NOUVEAU!)
```bash
/update_setup channel:#updates    # Configurer notifications
/update_setup enable:true         # Activer alertes auto
/check_updates                    # Vérification manuelle
```

### 🔧 Diagnostic & Monitoring
```bash
/botinfo                          # Informations complètes du bot
/serverinfo                       # Statistiques détaillées serveur
/userinfo @utilisateur            # Profil utilisateur complet
/ping                             # Latence et performances
```

### 🎯 Commandes Bonus (En Développement)
```bash
# 🎲 Commandes fun prévues
/roll                             # Lancer de dés
/8ball question                   # Boule magique
/meme                             # Générateur de memes

# 📊 Statistiques avancées prévues
/serverstats                      # Analytics complets
/userstats @user                  # Historique utilisateur
/modstats                         # Statistiques modération
```

---

## 🏗️ Architecture Technique

```
slimboy-version-ii/
├── 📁 commands/              # Commandes slash modulaires
│   ├── ban_list.py          # Système de banlist avec pagination
│   ├── moderation.py        # Suite complète de modération
│   └── diagnostic.py        # Outils de diagnostic avancés
├── 📁 utils/                # Utilitaires et systèmes
│   ├── embeds.py           # Création embeds professionnels
│   ├── pagination.py       # Système pagination intelligent
│   ├── ban_management.py   # Gestion avancée des bans
│   ├── logging_system.py   # 🆕 Logs configurables
│   └── update_notifier.py  # 🆕 Notifications GitHub
├── 📄 main.py              # Point d'entrée optimisé
├── 📄 bot.py               # Classe bot améliorée
├── 📄 keep_alive.py        # Serveur keep-alive Version II
├── 📄 config.py            # Configuration centralisée étendue
└── 📄 requirements.txt     # Dépendances mises à jour
```

---

## ⚙️ Configuration Avancée

### Variables d'Environnement Replit (Secrets)
```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

### Configuration Personnalisée
Modifiez `config.py` pour personnaliser :
```python
BOT_CONFIG = {
    # Interface
    "bans_per_page": 5,           # Bannis par page
    "embed_color": 0xFF0000,      # Couleur principale
    "pagination_timeout": 120,    # Timeout réduit (2 min)
    
    # Fonctionnalités
    "enable_logging": True,       # Système de logs
    "enable_updates": True,       # Notifications GitHub
    "enable_bonus": True,         # Commandes bonus
}
```

### Configuration Logs
```json
{
  "enabled": true,
  "log_channel_id": 123456789,
  "log_types": {
    "moderation": true,
    "bans": true,
    "errors": true,
    "commands": false
  }
}
```

---

## 🌐 Monitoring & API

### Endpoints Disponibles
- **🏠 Page d'accueil** : `https://votre-repl.replit.app/`
- **📊 Statut API** : `https://votre-repl.replit.app/status`
- **❤️ Health check** : `https://votre-repl.replit.app/health`
- **📦 Version info** : `https://votre-repl.replit.app/version`

### Keep-Alive Automatique
Le bot inclut un serveur web intégré pour maintenir la connexion 24/7 sur Replit.

---

## 🎯 Fonctionnalités Détaillées

### 📝 Système de Logs Intelligent
- **📊 Types configurables** : Modération, bans, erreurs, commandes
- **🎨 Embeds colorés** avec informations complètes
- **👤 Tracking modérateurs** automatique via audit logs
- **⏰ Timestamps** précis et formatage Discord natif

### 🔔 Notifications GitHub Auto
- **🚀 Détection versions** automatique depuis le repository
- **📱 Alerts Discord** avec embeds détaillés
- **⚙️ Configuration flexible** par serveur
- **📋 Changelog intégré** dans les notifications

### 🔍 Recherche Ultra-Avancée
- **🎯 Correspondance partielle** insensible à la casse
- **🔤 Recherche phonétique** pour noms similaires
- **📊 Historique utilisateur** avec cache intelligent
- **⚡ Performance optimisée** pour gros serveurs

---

## 🗺️ Roadmap Version II

### 🎯 Version 2.1 (Prochaine - Q1 2025)
- [ ] 🎲 **Commandes Fun Complètes** - Jeux, divertissement, interactions
- [ ] 📊 **Analytics Avancées** - Graphiques, métriques, tendances
- [ ] 🤖 **IA Modération** - Détection automatique contenu inapproprié
- [ ] 🌍 **Multi-langues** - Support anglais, espagnol, allemand

### 🚀 Version 2.2 (Q2 2025)
- [ ] 🌐 **Dashboard Web** - Interface de gestion complète
- [ ] 📱 **App Mobile** - Contrôle depuis smartphone
- [ ] 🔗 **API REST** - Intégrations tierces
- [ ] ☁️ **Cloud Sync** - Synchronisation multi-serveurs

### 🌟 Version 2.3+ (Futur)
- [ ] 🧠 **Machine Learning** - Prédiction comportements utilisateurs
- [ ] 🎮 **Mini-jeux Avancés** - Économie virtuelle, achievements
- [ ] 🔐 **Sécurité Renforcée** - 2FA, audit avancé
- [ ] 🌈 **Thèmes Personnalisables** - Interface customizable

---

## 🐛 Support & Dépannage

### Problèmes Courants Version II

#### 🚫 Bot ne démarre pas
```bash
✅ Vérifiez le token dans les Secrets Replit
✅ Token valide et bot invité sur le serveur
✅ Permissions administrateur accordées
✅ Consultez la console Replit pour erreurs
```

#### ❌ Commandes ne répondent pas
```bash
✅ Utilisez les commandes slash (/) exclusivement
✅ Bot en ligne (statut vert dans Discord)
✅ Permissions correctes sur le serveur
✅ Redémarrez le Repl si nécessaire
```

#### 📝 Logs ne fonctionnent pas
```bash
✅ Canal de logs configuré avec /logs_setup
✅ Bot a permission d'écrire dans le canal
✅ Types de logs activés avec /logs_types
✅ Système activé (enable:true)
```

#### 🔔 Notifications absentes
```bash
✅ Canal notifications configuré avec /update_setup
✅ Connexion internet stable
✅ GitHub accessible (pas de restrictions)
✅ Vérification manuelle avec /check_updates
```

#### 🔑 Problèmes de Token
```bash
❌ "DISCORD_BOT_TOKEN environment variable is not set"
✅ Token ajouté dans Secrets Replit (clé: DISCORD_BOT_TOKEN)
✅ Token valide et récent (pas expiré)
✅ Bot créé dans Discord Developer Portal

❌ "Forbidden" ou "Unauthorized"  
✅ Token copié entièrement (commence par "MTM...")
✅ Permissions bot activées dans Discord Developer Portal
✅ Pas d'espaces avant/après le token dans Secrets

❌ Bot n'apparaît pas dans Discord
✅ Lien d'invitation utilisé avec bon CLIENT_ID
✅ Permissions administrateur accordées lors invitation
✅ Bot en ligne (statut vert) après démarrage Repl
```

### 📞 Obtenir de l'Aide
- **🐛 Bugs** : [GitHub Issues](https://github.com/TifouDragon/slimboy-discord-bot/issues)
- **💬 Support** : Discord @Ninja Iyed
- **📚 Documentation** : [Wiki GitHub](https://github.com/TifouDragon/slimboy-discord-bot/wiki)

---

## 🤝 Contribution

### Guidelines de Contribution Version II
1. **🍴 Fork** le projet et créez une branche feature
2. **💻 Code** en français pour l'interface utilisateur
3. **📝 Documentez** toutes les nouvelles fonctions
4. **🧪 Testez** sur un serveur de développement
5. **📬 Soumettez** une Pull Request détaillée

### Domaines de Contribution
- **🎯 Commandes Bonus** - Nouvelles fonctionnalités fun
- **🎨 Interface** - Améliorations design et UX
- **📊 Analytics** - Système de statistiques
- **🌍 Traductions** - Support multi-langues
- **🐛 Corrections** - Optimisations et fixes

---

## 📊 Statistiques Version II

![GitHub stars](https://img.shields.io/github/stars/TifouDragon/slimboy-discord-bot?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/TifouDragon/slimboy-discord-bot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/TifouDragon/slimboy-discord-bot?style=for-the-badge)

![Replit Runs](https://img.shields.io/badge/Replit-1000%2B%20Runs-orange?style=for-the-badge)
![Discord Servers](https://img.shields.io/badge/Discord-500%2B%20Serveurs-blue?style=for-the-badge)
![Active Users](https://img.shields.io/badge/Utilisateurs-10K%2B-green?style=for-the-badge)

---

## 📄 Licence & Copyright

Ce projet est sous licence MIT. Utilisation libre avec attribution.

**© 2024 SlimBoy Version 2.2 - Tous droits réservés**

---

## 👨‍💻 Équipe de Développement

### 🌟 Développeur Principal
**Ninja Iyed** - *Créateur & Lead Developer*
- Discord : @Ninja Iyed
- GitHub : [@TifouDragon](https://github.com/TifouDragon)
- Spécialités : Architecture bot, Interface Discord, Systèmes avancés

### 🙏 Remerciements Spéciaux
- **Discord.py Community** - Framework et support technique
- **Replit Team** - Plateforme de développement exceptionnelle
- **Beta Testers** - Communauté Discord pour feedback constructif
- **Contributors** - Développeurs ayant participé au projet

---

<div align="center">

# 🚀 Prêt pour la Version II ?

## Déployez maintenant sur Replit !

[![Run on Replit](https://replit.com/badge/github/TifouDragon/slimboy-discord-bot)](https://replit.com/@TifouDragon/slimboy-discord-bot)

### ⭐ N'oubliez pas de star le projet ! ⭐

*Développé avec ❤️ par [@Ninja Iyed](https://github.com/TifouDragon) pour la communauté Discord francophone*

**🎯 Bot de Modération • 🎮 Commandes Bonus • 🌐 Dashboard Futur**

---

**Version 2.2 - L'évolution continue...**

</div>
