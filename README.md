# 🤖 SlimBoy - Discord Moderation Bot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.5.2+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/TifouDragon/slimboy-discord-bot)

> Un bot Discord de modération avancé avec interface française et pagination interactive pour la gestion des bannis.

## ✨ Fonctionnalités

### 🛡️ Modération Complète
- **Liste des bannis** avec pagination interactive (5 par page)
- **Recherche avancée** par pseudo, nom d'utilisateur ou ID
- **Gestion des bans** : bannir, débannir, ban temporaire
- **Modération standard** : kick, timeout, clear messages
- **Informations utilisateur** détaillées

### 🎨 Interface Moderne
- **Embeds Discord** avec design professionnel
- **Boutons interactifs** pour la navigation
- **Messages d'erreur** informatifs en français
- **Watermark** @Ninja Iyed sur tous les embeds

### 🔍 Fonctionnalités Avancées
- **Détection automatique** de 20+ bots populaires
- **Logs d'audit** pour identifier les modérateurs
- **Permissions intelligentes** avec vérifications
- **Keep-alive automatique** avec serveur Flask intégré

## 🚀 Installation Rapide

### 1. Configuration Discord
1. Créez une application sur le [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez un bot et copiez le token
3. Invitez le bot avec ce lien (remplacez `YOUR_CLIENT_ID`) :
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=1374389502966&scope=bot%20applications.commands
```

### 2. Déploiement sur Railway
1. **Connectez Railway** à votre repository GitHub
2. **Ajoutez la variable d'environnement** :
   - `DISCORD_BOT_TOKEN` : Votre token Discord
3. **Déployez automatiquement** avec Railway
4. **Le keep-alive** s'active automatiquement

### 3. Déploiement sur Replit (Alternative)
1. **Fork ce projet** sur Replit
2. **Ajoutez votre token** dans les Secrets :
   - `DISCORD_BOT_TOKEN` : Votre token Discord
3. **Lancez le bot** avec le bouton Run

### 4. Installation Locale
```bash
# Cloner le repository
git clone https://github.com/TifouDragon/slimboy-discord-bot.git
cd slimboy-discord-bot

# Installer les dépendances
pip install -r requirements.txt

# Configurer le token
export DISCORD_BOT_TOKEN="votre_token_ici"

# Lancer le bot
python main.py
```

## 📋 Commandes Disponibles

### Commandes Slash
| Commande | Description | Permissions |
|----------|-------------|-------------|
| `/banlist [search]` | Affiche la liste paginée des bannis | Ban Members |
| `/ban <user> [reason]` | Bannir un membre du serveur | Ban Members |
| `/unban <userid> [reason]` | Débannir un utilisateur | Ban Members |
| `/kick <user> [reason]` | Expulser un membre | Kick Members |
| `/timeout <user> <duration> [reason]` | Timeout temporaire | Moderate Members |
| `/untimeout <user> [reason]` | Retirer un timeout | Moderate Members |
| `/clear <amount> [user]` | Supprimer des messages (1-100) | Manage Messages |
| `/warn <user> [reason]` | Donner un avertissement | Manage Messages |
| `/userinfo [user]` | Informations détaillées d'un utilisateur | Aucune |
| `/slowmode <seconds> [channel]` | Activer/modifier le mode lent | Manage Channels |

### Exemples d'utilisation
```
/banlist                          # Liste complète des bannis
/banlist search:troll             # Recherche par pseudo
/banlist page:2                   # Page spécifique
/ban @utilisateur spam répétitif  # Bannir avec raison
/timeout @utilisateur 1h flood    # Timeout 1 heure
/clear 50                         # Supprimer 50 messages
```

## 🔧 Structure du Projet

```
slimboy-discord-bot/
├── 📁 commands/           # Commandes slash modulaires
│   ├── ban_list.py       # Commande /banlist avec pagination
│   └── moderation.py     # Commandes de modération
├── 📁 utils/             # Utilitaires et helpers
│   ├── embeds.py         # Création des embeds Discord
│   ├── pagination.py     # Système de pagination
│   └── ban_management.py # Gestion avancée des bans
├── 📄 main.py            # Point d'entrée principal
├── 📄 bot.py             # Classe du bot Discord
├── 📄 keep_alive.py      # Serveur Flask keep-alive
└── 📄 config.py          # Configuration centralisée
```

## 🛠️ Configuration Avancée

### Variables d'Environnement
```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

### Configuration Personnalisée
Modifiez `config.py` pour personnaliser :
```python
BOT_CONFIG = {
    "bans_per_page": 5,           # Bannis par page
    "embed_color": 0xFF0000,      # Couleur des embeds
    "pagination_timeout": 300,     # Timeout pagination (5 min)
}
```

## 🔒 Permissions Requises

Le bot nécessite ces permissions Discord :
- ✅ **Bannir des membres** - Accès à la liste des bannis
- ✅ **Voir les logs d'audit** - Identification des modérateurs
- ✅ **Expulser des membres** - Commande kick
- ✅ **Modérer les membres** - Commandes timeout
- ✅ **Gérer les messages** - Commandes clear/warn
- ✅ **Gérer les canaux** - Commande slowmode
- ✅ **Envoyer des messages** - Réponses du bot
- ✅ **Incorporer des liens** - Embeds Discord

## 🌐 Keep-Alive et Monitoring

Le bot inclut un serveur Flask intégré pour le monitoring :
- **Endpoint principal** : `https://your-repl.replit.app/`
- **Status API** : `https://your-repl.replit.app/status`
- **Health check** : `https://your-repl.replit.app/health`

Compatible avec [UptimeRobot](https://uptimerobot.com) pour maintenir le bot en ligne 24/7.

## 📊 Fonctionnalités Détaillées

### 🔍 Système de Recherche Intelligent
- Recherche par **pseudo** (nom d'affichage)
- Recherche par **nom d'utilisateur** Discord
- Recherche par **ID utilisateur**
- **Correspondance partielle** insensible à la casse

### 🎛️ Interface de Pagination
- **Navigation fluide** avec boutons ◀️ ▶️
- **Information de page** dynamique
- **Bouton Gérer** pour actions sur les bannis
- **Bouton Fermer** avec suppression différée (1 minute)
- **Timeout automatique** après 3 minutes d'inactivité

### 🤖 Détection de Bots
Le système détecte automatiquement les bans effectués par :
- Dyno, Carl-bot, MEE6, Ticket Tool
- ModMail, AutoMod, Security Bots
- Pancake, Groovy, Rythm, FredBoat
- Pokecord, Mudae, Dank Memer, Tatsu
- Et 10+ autres bots populaires

## 🐛 Résolution de Problèmes

### Problèmes Fréquents
```bash
# Bot ne démarre pas
❌ Vérifiez le token Discord dans .env
❌ Vérifiez les permissions du bot

# Commandes ne fonctionnent pas
❌ Re-invitez le bot avec les bonnes permissions
❌ Utilisez les commandes slash (/) uniquement

# Liste des bannis vide
❌ Bot besoin permission "Bannir des membres"
❌ Bot besoin permission "Voir les logs d'audit"
```

### Logs de Debug
Le bot génère des logs détaillés pour le debugging :
```python
# Activer les logs détaillés
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. Créez une **branche feature** (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Guidelines de Contribution
- Code en **français** pour les messages utilisateur
- **Docstrings** en français pour les fonctions
- **Tests** pour les nouvelles fonctionnalités
- Respect du **style de code** existant

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE.txt](LICENSE.txt) pour plus de détails.

## 👨‍💻 Auteur

**Ninja Iyed** - *Développeur Principal*
- Discord : @Ninja Iyed
- GitHub : [@TifouDragon](https://github.com/TifouDragon)

## 🙏 Remerciements

- **Discord.py** - Librairie Python pour Discord
- **Flask** - Serveur web léger pour keep-alive
- **Replit** - Plateforme de déploiement
- Communauté Discord pour les retours et suggestions

---

<div align="center">

**⭐ N'oubliez pas de star le projet si il vous a aidé ! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/TifouDragon/slimboy-discord-bot.svg?style=social&label=Star)](https://github.com/TifouDragon/slimboy-discord-bot)
[![GitHub forks](https://img.shields.io/github/forks/TifouDragon/slimboy-discord-bot.svg?style=social&label=Fork)](https://github.com/TifouDragon/slimboy-discord-bot/fork)

*Bot créé avec ❤️ par @Ninja Iyed*

</div>