
# 🤖 SlimBoy - Discord Moderation Bot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.5.2+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Railway](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app)
[![Replit](https://img.shields.io/badge/Replit-Ready-orange.svg)](https://replit.com)

> Un bot Discord de modération avancé avec interface française et pagination interactive pour la gestion des bannis. Optimisé pour Railway et Replit. + petit bonus.


## ✨ Fonctionnalités

### 🛡️ Modération Complète
- **Liste des bannis** avec pagination interactive (5 par page)
- **Recherche avancée** par pseudo, nom d'utilisateur ou ID
- **Gestion des bans** : bannir, débannir, ban temporaire
- **Modération standard** : kick, timeout, clear messages
- **Informations utilisateur** détaillées avec âge du compte

### 🎨 Interface Moderne
- **Embeds Discord** avec design professionnel
- **Boutons interactifs** pour la navigation
- **Messages d'erreur** informatifs en français
> Watermark du createur sur tous les embeds

### 🔍 Fonctionnalités Avancées
- **Détection automatique** de 20+ bots populaires
- **Logs d'audit** pour identifier les modérateurs
- **Permissions intelligentes** avec vérifications
- **Keep-alive automatique** avec serveur Flask intégré
- **Commandes de simulation** (fakeban, fakemute)
- **+ des ajouts**

## 🚀 Déploiement

### Option 1: Railway (Recommandé pour production)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/github-template-url)

1. **Clonez ce dépôt** sur GitHub
2. **Connectez Railway** à votre compte GitHub
3. **Importez le projet** depuis votre fork
4. **Ajoutez les variables d'environnement** :
   - `DISCORD_BOT_TOKEN` : Token de votre bot Discord
5. **Déployez** automatiquement

### Option 2: Replit (Idéal pour développement)

[![Run on Replit](https://replit.com/badge/github/TifouDragon/slimboy-discord-bot)](https://replit.com/@TifouDragon/slimboy-discord-bot)

1. **Fork ce projet** sur Replit
2. **Ajoutez votre token** dans les Secrets (🔒)
3. **Lancez** avec le bouton Run

## 🔧 Configuration Discord

### 1. Créer l'application Discord
1. Rendez-vous sur le [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur **New Application**
3. Donnez un nom à votre bot (ex: "SlimBoy")
4. Allez dans l'onglet **Bot**
5. Cliquez sur **Reset Token** et copiez le token

### 2. Inviter le bot
Utilisez ce lien en remplaçant `YOUR_CLIENT_ID` par l'ID de votre application :
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=1374389502966&scope=bot%20applications.commands
```

### 3. Permissions requises
Le bot nécessite ces permissions Discord :
- ✅ **Bannir des membres** - Accès à la liste des bannis
- ✅ **Voir les logs d'audit** - Identification des modérateurs
- ✅ **Expulser des membres** - Commande kick
- ✅ **Modérer les membres** - Commandes timeout
- ✅ **Gérer les messages** - Commandes clear/warn
- ✅ **Gérer les canaux** - Commande slowmode
- ✅ **Envoyer des messages** - Réponses du bot
- ✅ **Incorporer des liens** - Embeds Discord

## 📋 Commandes Disponibles

### 🔍 Commandes de Liste
```bash
/banlist                          # Voir tous les bannis
/banlist user:pseudo              # Chercher par pseudo
/banlist user:@utilisateur        # Chercher par mention
/banlist user:123456789           # Chercher par ID
```

### 🛡️ Commandes de Modération
```bash
/ban @utilisateur raison          # Bannir un utilisateur
/unban 123456789                  # Débannir par ID
/kick @utilisateur raison         # Expulser un utilisateur
/timeout @utilisateur 10m         # Timeout temporaire
/clear 50                         # Supprimer 50 messages
/tempban @utilisateur 7d raison   # Ban temporaire
/ipban @utilisateur raison        # Ban IP + suppression messages
```

### 🎭 Commandes de Simulation
```bash
/fakeban @utilisateur             # Simulation de ban (fake)
/fakemute @utilisateur            # Simulation de mute (fake)
```

### 🔧 Commandes de Diagnostic
```bash
/botinfo                          # Informations du bot
/serverinfo                       # Informations du serveur
/userinfo @utilisateur            # Informations utilisateur
/ping                             # Latence du bot
```

## 🏗️ Structure du Projet

```
slimboy-discord-bot/
├── 📁 commands/              # Commandes slash modulaires
│   ├── ban_list.py          # Commande /banlist avec pagination
│   ├── moderation.py        # Commandes de modération
│   └── diagnostic.py        # Commandes de diagnostic
├── 📁 utils/                # Utilitaires et helpers
│   ├── embeds.py           # Création des embeds Discord
│   ├── pagination.py       # Système de pagination
│   └── ban_management.py   # Gestion avancée des bans
├── 📄 main.py              # Point d'entrée principal
├── 📄 bot.py               # Classe du bot Discord
├── 📄 keep_alive.py        # Serveur Flask keep-alive
├── 📄 config.py            # Configuration centralisée
├── 📄 railway.json         # Configuration Railway
├── 📄 Procfile             # Configuration de déploiement
└── 📄 requirements.txt     # Dépendances Python
```

## ⚙️ Configuration

### Variables d'Environnement

#### Railway
```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
PORT=5000  # Automatique sur Railway
```

#### Replit (Secrets)
- `DISCORD_BOT_TOKEN` : Token de votre bot Discord

### Configuration Personnalisée
Modifiez `config.py` pour personnaliser :
```python
BOT_CONFIG = {
    "bans_per_page": 5,           # Bannis par page
    "embed_color": 0xFF0000,      # Couleur des embeds
    "pagination_timeout": 600,    # Timeout pagination (10 min)
}
```

## 🌐 Monitoring et Keep-Alive

### Endpoints Disponibles
- **Page d'accueil** : `https://votre-app.railway.app/`
- **API Status** : `https://votre-app.railway.app/status`
- **Health check** : `https://votre-app.railway.app/health`

### Surveillance 24/7 (Optionnel)
Pour une surveillance externe avec [UptimeRobot](https://uptimerobot.com) :
1. Créez un compte gratuit
2. Ajoutez un monitor HTTP(s)
3. URL : `https://votre-app.railway.app/health`
4. Intervalle : 5 minutes

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
- **Timeout automatique** après 10 minutes d'inactivité

### 🤖 Détection de Bots
Le système détecte automatiquement les bans effectués par :
- **Modération** : Dyno, Carl-bot, MEE6, AutoMod
- **Utilitaires** : Ticket Tool, ModMail, Security Bots
- **Musique** : Groovy, Rythm, FredBoat, Pancake
- **Jeux** : Pokecord, Mudae, Dank Memer, Tatsu
- Et 10+ autres bots populaires

## 🐛 Résolution de Problèmes

### Problèmes Fréquents

#### Bot ne démarre pas
```bash
❌ Vérifiez le token Discord dans les variables d'environnement
❌ Vérifiez les permissions du bot sur le serveur
❌ Consultez les logs de Railway/Replit
```

#### Commandes ne fonctionnent pas
```bash
❌ Re-invitez le bot avec les bonnes permissions
❌ Utilisez les commandes slash (/) uniquement
❌ Vérifiez que le bot est en ligne
```

#### Liste des bannis vide
```bash
❌ Bot besoin permission "Bannir des membres"
❌ Bot besoin permission "Voir les logs d'audit"
❌ Vérifiez que des utilisateurs sont bannis
```

### Logs de Debug
- **Railway** : Consultez l'onglet "Logs" de votre projet
- **Replit** : Vérifiez la console dans l'IDE

## 🚀 Développement Local

### Prérequis
- Python 3.11+
- Git

### Installation
```bash
# Cloner le dépôt
git clone https://github.com/TifouDragon/slimboy-discord-bot.git
cd slimboy-discord-bot

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
export DISCORD_BOT_TOKEN="your_token_here"

# Lancer le bot
python main.py
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet sur GitHub
2. Créez une **branche feature** (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Guidelines de Contribution
- Code en **français** pour les messages utilisateur
- **Docstrings** en français pour les fonctions
- **Tests** pour les nouvelles fonctionnalités
- Respect du **style de code** existant
- **Issues** avant les grosses modifications

## 📈 Roadmap

### Version ????? (Prévue)
- [ ] Dashboard web pour gestion à distance
- [ ] Système de logs avancé avec base de données


## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Ninja Iyed** - *Développeur Principal*
- Discord : @Ninja Iyed
- GitHub : [@TifouDragon](https://github.com/TifouDragon)

## 🙏 Remerciements

- **Discord.py** - Librairie Python pour Discord
- **Flask** - Serveur web léger pour keep-alive
- **Railway** - Plateforme de déploiement moderne
- **Replit** - IDE et hébergement de développement
- Communauté Discord pour les retours et suggestions

## 🏆 Statistiques

![GitHub stars](https://img.shields.io/github/stars/TifouDragon/slimboy-discord-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/TifouDragon/slimboy-discord-bot?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/TifouDragon/slimboy-discord-bot?style=social)

![GitHub last commit](https://img.shields.io/github/last-commit/TifouDragon/slimboy-discord-bot)
![GitHub issues](https://img.shields.io/github/issues/TifouDragon/slimboy-discord-bot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/TifouDragon/slimboy-discord-bot)

---

<div align="center">

**⭐ N'oubliez pas de star le projet si il vous a aidé ! ⭐**

**🚀 Prêt à déployer sur Railway ou Replit ! 🚀**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)
[![Run on Replit](https://replit.com/badge/github/TifouDragon/slimboy-discord-bot)](https://replit.com)

*Développé avec ❤️ par [@Ninja Iyed](https://github.com/TifouDragon)*

</div>
