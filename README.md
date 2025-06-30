# 🤖 SlimBoy - Bot Discord de Modération Avancée

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.5.2+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 Bot Discord révolutionnaire avec modération intelligente, système de logs configurable, notifications automatiques et commandes bonus ! Interface française premium avec pagination interactive optimisée pour Replit.

<div align="center">


**🎯 Modération Avancée • 📝 Logs Intelligents • 🔔 Notifications Auto • 🎮 Commandes Bonus**

</div>

---


## ✨ Fonctionnalités Principales

### 🛡️ Modération Nouvelle Génération
- **📋 Liste Bannis Ultra-Avancée** - Pagination avec recherche intelligente
- **🔍 Recherche Multi-Critères** - Par pseudo, nom, ID, correspondance partielle
- **⚡ Gestion Complète Bans** - Ban/unban/tempban/ipban avec durées personnalisées
- **🛠️ Modération Premium** - Kick, timeout, clear avec système de permissions
- **👤 Profils Utilisateurs** - Informations détaillées avec historique
- **👮 Guardian Protection** - 🆕 Système de protection utilisateur anti-abus

### 🔥 Systèmes Intelligents
- **📝 Logs Configurables** - Enregistrement automatique avec choix des événements
- **🔔 Notifications GitHub** - Alertes Discord automatiques pour mises à jour
- **🎮 Jeux & Mini-Jeux** - 🆕 Divertissement intégré pour la communauté
- **🤖 Détection Bots** - Reconnaissance automatique de 25+ bots populaires
- **🔒 Modération Invisible** - 🆕 Commandes discrètes pour staff

### 🎨 Interface Premium
- **🎭 Embeds Designer** - Design professionnel uniforme
- **🎮 Navigation Interactive** - Boutons intelligents pour UX fluide
- **📱 Messages Contextuels** - Erreurs informatives avec suggestions
- **🏷️ Branding Intégré** - Style cohérent sur tous les embeds

---

## 🚀 Installation Ultra-Rapide

### 🎯 Méthode Replit (Recommandée - 2 minutes)


**Étapes simples :**
1. **🍴 Fork** le projet sur Replit (bouton ci-dessus)
2. **🔑 Ajoutez votre token** dans les Secrets (🔒)
   - **Clé** : `DISCORD_BOT_TOKEN`
   - **Valeur** : Votre token Discord
3. **▶️ Lancez** avec le bouton Run
4. **🎉 Prêt !** Toutes les fonctionnalités sont disponibles

### 🚂 Alternative Railway (Optionnelle)

Pour les utilisateurs préférant Railway :
1. **📝 Compte** sur [Railway.app](https://railway.app)
2. **🔗 Import** ce repository GitHub
3. **⚙️ Variable** : `DISCORD_BOT_TOKEN` = votre token
4. **🚀 Deploy** automatique avec `railway.json`

**💡 Note** : SlimBoy est optimisé Replit mais 100% compatible Railway.

### 🌍 Option 3 : Autre moyen d'hébergement (Flask intégré)

Le bot intègre un serveur Flask pour le keep-alive, compatible avec la plupart des plateformes d'hébergement gratuites ou payantes supportant Python.

---

## 🎨 Personnalisation du Nom du Bot

### 🤖 Nom par Défaut : "SlimBoy"

Le bot utilise **"SlimBoy"** comme nom par défaut, mais vous pouvez facilement le personnaliser selon vos préférences !

### ✏️ Comment Changer le Nom

#### **Méthode 1 : Via Discord Developer Portal (Recommandée)**
1. **Accédez** au [Discord Developer Portal](https://discord.com/developers/applications)
2. **Sélectionnez** votre application bot
3. **Onglet "General Information"** → Modifiez le champ **"Name"**
4. **Sauvegardez** et redémarrez votre bot

#### **Méthode 2 : Modification du Code (Avancée)**
Dans le fichier `config.py`, vous pouvez personnaliser :
```python
BOT_CONFIG = {
    "bot_name": "VotreNomPersonnalisé",  # Changez ici
    "bot_description": "Votre description personnalisée",
    # ... autres configurations
}
```

### 🎭 Personnalisations Populaires
- **ModBot** - Pour un bot axé modération
- **GuardianBot** - Pour un gardien de serveur
- **AdminAssist** - Pour un assistant administrateur
- **YourServerBot** - Avec le nom de votre serveur
- **CustomMod** - Bot de modération personnalisé

### 💡 **Important :** Le nom dans le code source reste "SlimBoy" pour maintenir la compatibilité, mais l'affichage Discord utilisera votre nom personnalisé !

---

## 🔧 Configuration Discord Complète

### 🔑 Tokens Requis et Optionnels

#### ✅ **DISCORD_BOT_TOKEN** (OBLIGATOIRE)
**Rôle** : Authentification et connexion du bot à Discord
**Source** : Discord Developer Portal
```
1. https://discord.com/developers/applications
2. New Application → "Votre Nom de Bot Personnalisé"
3. Onglet Bot → Reset Token → Copier
4. Replit Secrets → DISCORD_BOT_TOKEN = votre_token
```

#### ❌ **CLIENT_ID** (OPTIONNEL - Invitation uniquement)
**Rôle** : Génération lien d'invitation uniquement
**Source** : Discord Developer Portal → General Information → Application ID
```
Exemple: 1384568465326866585
Usage: Créer lien invitation seulement
Note: PAS nécessaire pour fonctionnement du bot
```

### ⚡ Setup Express (3 étapes)

**Étape 1 - Token Discord :**
```bash
Discord Developer Portal → Bot → Reset Token → Copier
```

**Étape 2 - Secrets Replit :**
```bash
Replit → Secrets (🔒) → DISCORD_BOT_TOKEN = votre_token
```

**Étape 3 - Lancement :**
```bash
Bouton Run → Bot opérationnel ✅
```

### 🔗 Génération Lien Invitation

**Template avec votre CLIENT_ID :**
```
https://discord.com/oauth2/authorize?client_id=VOTRE_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

**Exemple concret :**
```
https://discord.com/oauth2/authorize?client_id=1384568465326866585&permissions=8&scope=bot%20applications.commands
```

### 🛡️ Permissions Auto-Accordées
✅ **Administrateur Complet** - Accès total pour fonctionnalités avancées
- 🔨 Bannir/Débannir membres
- 👢 Expulser utilisateurs
- 🔇 Modérer membres (timeout)
- 🗑️ Gérer messages/canaux
- 📋 Voir logs audit
- ⚙️ Gérer serveur

---

## 📋 Guide Complet des Commandes

### 🛡️ Modération Avancée

#### 📋 **Système BanList Intelligent**
```bash
/banlist                          # Liste complète avec pagination
/banlist user:pseudo              # Recherche par pseudo partiel
/banlist user:@utilisateur        # Recherche par mention
/banlist user:123456789           # Recherche par ID Discord
```

#### ⚡ **Gestion Bans Premium**
```bash
/ban @user raison                 # Ban permanent standard
/unban 123456789                  # Débannir par ID utilisateur
/tempban @user 7d raison          # Ban temporaire auto-débannissement
/ipban @user raison               # Ban IP + suppression messages 7j
```

#### 🛠️ **Modération Standard**
```bash
/kick @user raison                # Expulsion du serveur
/timeout @user 10m raison         # Timeout durée personnalisée
/untimeout @user                  # Annuler timeout manuel
/clear 50                         # Suppression messages bulk
```

#### 👮 **Système Guardian** (🆕 v2.2.1)
```bash
/guardian @user                   # Protéger un utilisateur contre abus
# Protection automatique : seuls rôles supérieurs + exceptions peuvent agir
# Commande invisible pour discrétion maximale
```

### 📝 Système de Logs (NOUVEAU)

#### ⚙️ **Configuration Logs**
```bash
/logs_setup channel:#logs         # Définir canal logs
/logs_setup enable:true           # Activer système logs
/logs_types                       # Choisir événements à enregistrer
/logs_status                      # Vérifier configuration actuelle
```

#### 📊 **Types de Logs Disponibles**
- ✅ **Modération** - Bans, kicks, timeouts
- ✅ **Messages** - Suppressions, modifications
- ✅ **Membres** - Arrivées, départs, rôles
- ✅ **Erreurs** - Bugs, permissions manquantes
- ✅ **Commandes** - Utilisation commandes slash

### 🔔 Notifications GitHub (NOUVEAU)

#### 🚀 **Setup Notifications**
```bash
/update_setup channel:#updates    # Canal pour notifications
/update_setup enable:true         # Activer alertes auto
/check_updates                    # Vérification manuelle versions
/update_config                    # Configuration avancée
```

#### 📱 **Fonctionnalités Notifications**
- 🔔 **Alertes automatiques** nouvelles versions
- 📋 **Changelog intégré** dans notifications Discord
- ⚙️ **Configuration par serveur** indépendante
- 🎯 **Notifications ciblées** responsables serveur

### 🎯 Commandes Bonus (Évolutif)

#### 🎮 **Jeux & Mini-Jeux** (🆕 v2.2.1)
```bash
/roll 1d20                        # Lancer de dés configurables
/8ball question                   # Boule magique réponses
/coinflip                         # Pile ou face
/randomuser                       # Sélection membre aléatoire
/rps rock                         # Pierre-papier-ciseaux
/guess_number                     # Jeu de devinette numérique
```

#### 📊 **Statistiques Avancées** (Prévu)
```bash
/serverstats                      # Analytics serveur complets
/userstats @user                  # Historique utilisateur détaillé
/modstats                         # Métriques modération période
/channelstats #channel            # Activité canal spécifique
```

### 🎭 Simulation Réaliste

#### 🎪 **Commandes Fun**
```bash
/fakeban @user                    # Simulation ban ultra-réaliste
/fakemute @user                   # Simulation mute crédible
```

### 🔧 Diagnostic & Monitoring

#### 📱 **Informations Système**
```bash
/botinfo                          # Statistiques bot complètes
/serverinfo                       # Détails serveur avancés
/userinfo @user                   # Profil utilisateur complet
/ping                             # Latence et performances temps réel
/diagnostic                       # Test complet fonctionnalités
```

---

## 🏗️ Architecture Technique Modulaire

```
slimboy-version-2.2/
├── 📁 commands/                  # Commandes slash organisées
│   ├── ban_list.py              # Système banlist + pagination
│   ├── moderation.py            # Suite modération complète
│   └── diagnostic.py            # Outils diagnostic avancés
├── 📁 utils/                    # Systèmes utilitaires
│   ├── embeds.py               # Générateur embeds uniformes
│   ├── pagination.py           # Pagination intelligente
│   ├── ban_management.py       # Gestion avancée bans
│   ├── logging_system.py       # 🆕 Logs configurables
│   └── update_notifier.py      # 🆕 Notifications GitHub
├── 📄 main.py                  # Point entrée optimisé
├── 📄 bot.py                   # Classe bot Version 2.2
├── 📄 keep_alive.py            # Serveur Flask intégré
├── 📄 config.py                # Configuration centralisée
├── 📄 requirements.txt         # Dépendances actualisées
├── 📄 logging_config.json      # 🆕 Config logs personnalisable
├── 📄 update_config.json       # 🆕 Config notifications
└── 📄 railway.json             # Support Railway
```

---

## ⚙️ Configuration Avancée

### 🔧 Variables Environnement

**Obligatoire (Replit Secrets) :**
```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

**Optionnelles (Auto-configurées) :**
```bash
BOT_PREFIX=!                     # Préfixe commandes (legacy)
LOG_LEVEL=INFO                   # Niveau logs (DEBUG/INFO/WARNING)
ENVIRONMENT=production           # Environnement déploiement
```

### 🎨 Personnalisation Interface

**Fichier `config.py` :**
```python
BOT_CONFIG = {
    # Interface utilisateur
    "bans_per_page": 5,              # Bannis par page pagination
    "embed_color": 0xFF0000,         # Couleur principale embeds
    "pagination_timeout": 120,       # Timeout boutons (secondes)
    "watermark_enabled": True,       # Watermark créateur

    # Fonctionnalités système
    "enable_logging": True,          # Système logs activé
    "enable_updates": True,          # Notifications GitHub
    "enable_bonus": True,            # Commandes bonus
    "enable_cache": True,            # Cache performances

    # Modération avancée
    "max_ban_reason_length": 512,    # Longueur max raison ban
    "auto_delete_ban_messages": 7,   # Jours suppression messages
    "temp_ban_max_duration": "365d", # Durée max ban temporaire
}
```

### 📝 Configuration Logs Détaillée

**Fichier `logging_config.json` :**
```json
{
  "enabled": true,
  "log_channel_id": null,
  "log_types": {
    "moderation": true,
    "bans": true,
    "kicks": true,
    "timeouts": true,
    "message_deletions": false,
    "member_updates": false,
    "errors": true,
    "commands": false,
    "system": true
  },
  "embed_settings": {
    "color": "0xFF0000",
    "timestamp": true,
    "footer": true,
    "author_info": true
  }
}
```

### 🔔 Configuration Notifications

**Fichier `update_config.json` :**
```json
{
  "enabled": false,
  "notification_channel_id": null,
  "check_interval_hours": 24,
  "github_repository": "TifouDragon/slimboy-discord-bot",
  "notify_on": {
    "new_version": true,
    "security_updates": true,
    "feature_updates": true,
    "bug_fixes": true
  },
  "mention_roles": []
}
```

---

## 🌐 Monitoring & Endpoints API

### 📊 MINI Web Intégré

**Page d'accueil :** `https://votre-repl.replit.app/`
- 🎨 Interface moderne avec informations bot
- 📈 Statistiques temps réel
- 🎯 Fonctionnalités disponibles
- 💎 Design Version 2.2

### 🔗 Endpoints API Complets

**Statut système :**
```bash
GET /status                      # Statut JSON complet bot
GET /health                      # Health check monitoring
GET /version                     # Informations version détaillées
```

**Réponse `/status` exemple :**
```json
{
  "status": "online",
  "platform": "Replit",
  "bot_name": "SlimBoy",
  "version": "2.2.0",
  "version_name": "Version 2.2",
  "author": "@Ninja Iyed",
  "features": {
    "moderation": true,
    "ban_list": true,
    "bonus_commands": true,
    "logging_system": true,
    "update_notifications": true,
    "dashboard": "active"
  },
  "uptime": "24/7",
  "environment": "Replit",
  "guilds_count": 500,
  "users_count": 10000
}
```

### ⚡ Keep-Alive Automatique

Le bot inclut un serveur Flask intégré qui :
- 🔄 Maintient la connexion 24/7 sur Replit ou autre
- 🔍 Endpoints monitoring pour surveillance
- 📈 Métriques performances temps réel

---

## 🎯 Fonctionnalités Techniques Détaillées

### 📝 Système de Logs Ultra-Avancé

**Caractéristiques :**
- **📊 10+ Types d'événements** configurables individuellement
- **🎨 Embeds colorés** avec codes couleur contextuels
- **👤 Tracking modérateurs** automatique via audit logs Discord
- **⏰ Timestamps précis** avec formatage Discord natif
- **🔍 Informations détaillées** : avant/après, raisons, durées
- **⚙️ Configuration flexible** par serveur indépendante

**Événements trackés :**
```bash
✅ Modération: Bans, unbans, kicks, timeouts
✅ Messages: Suppressions bulk, éditions importantes  
✅ Membres: Arrivées, départs, changements rôles
✅ Système: Erreurs, permissions, performances
✅ Commandes: Utilisation, succès, échecs
```

### 🔔 Notifications GitHub Intelligentes

**Fonctionnalités avancées :**
- **🚀 Détection automatique** nouvelles versions repository
- **📱 Notifications Discord** avec embeds riches et colorés
- **📋 Changelog intégré** directement dans notifications
- **⚙️ Configuration granulaire** types notifications
- **🎯 Mentions rôles** responsables serveur configurables
- **📅 Planification** vérifications périodiques personnalisables

### 🔍 Recherche Ultra-Intelligente

**Algorithmes avancés :**
- **🎯 Correspondance partielle** insensible à la casse
- **🔤 Recherche phonétique** pour noms similaires
- **📊 Cache intelligent** historique utilisateurs
- **⚡ Performance optimisée** pour serveurs 10k+ membres
- **🔄 Indexation dynamique** mise à jour temps réel

### 🤖 Détection Bots Automatique

**Base de données intégrée :**
```python
KNOWN_BOTS = [
    "MEE6", "Carl-bot", "Dyno", "Mudae", "Dank Memer",
    "Groovy", "Rhythm", "FredBoat", "Rythm", "Hydra",
    "Ticket Tool", "YAGPDB", "UnbelievaBoat", "Arcane",
    "GiveawayBot", "Pokécord", "IdleRPG", "Statbot"
    # ... 25+ bots reconnus automatiquement
]
```

---

## 🗺️ Roadmap Développement

### 🎯 Versions Futures
- [ ] 🎲 **Commandes Fun Complètes** - Divertissements variés
- [ ] 📊 **Analytics Graphiques** - Visualisation données avec charts
- [ ] 🤖 **IA Modération V1** - Détection contenu inapproprié automatique
- [ ] 🌍 **Multi-langues** - Support anglais, espagnol, allemand
- [ ] 📱 **API REST Publique** - Endpoints développeurs tiers
- [ ] 🌐 **Dashboard Web Complet** - Interface gestion full-featured
- [ ] 🔐 **Sécurité Renforcée** - 2FA, audit avancé, chiffrement

---

## 🐛 Support & Dépannage Expert

### ❌ Problèmes Fréquents & Solutions

#### 🚫 **Bot ne démarre pas**
```bash
Symptôme: "DISCORD_BOT_TOKEN environment variable is not set"
✅ Solution: 
   1. Vérifier Secrets Replit → DISCORD_BOT_TOKEN existe
   2. Token valide (commence par "MTM..." ou similaire)
   3. Pas d'espaces avant/après token
   4. Redémarrer Repl après ajout token
```

#### ❌ **Commandes ne répondent pas**
```bash
Symptôme: Bot en ligne mais commandes ignorées
✅ Solution:
   1. Utiliser commandes slash (/) exclusivement
   2. Vérifier permissions bot sur serveur
   3. Bot invité avec lien permissions complètes
   4. Attendre sync commandes (jusqu'à 1h)
```

#### ❌ **Logs ne fonctionnent pas**
```bash
Symptôme: Aucun log dans canal configuré
✅ Solution:
   1. /logs_setup channel:#votre-canal
   2. /logs_setup enable:true
   3. Vérifier permissions écriture bot
   4. /logs_types pour activer événements
```

#### ❌ **Notifications GitHub absentes**
```bash
Symptôme: Pas d'alertes nouvelles versions
✅ Solution:
   1. /update_setup channel:#updates enable:true
   2. Vérifier connexion internet stable
   3. GitHub accessible (pas restrictions réseau)
   4. /check_updates pour test manuel
```

#### ❌ **Pagination ne fonctionne pas**
```bash
Symptôme: Boutons pagination inactifs
✅ Solution:
   1. Vérifier permissions "Embed Links"
   2. Permissions "Add Reactions" activées
   3. Timeout pagination (2 min par défaut)
   4. Relancer commande /banlist
```

### 🔧 Diagnostic Avancé

**Commande diagnostic complète :**
```bash
/diagnostic
```

**Informations fournies :**
- ✅ Statut connexion Discord
- ✅ Permissions bot détaillées
- ✅ Performance système (CPU, RAM)
- ✅ Test fonctionnalités principales
- ✅ Recommendations configuration
- ✅ Endpoints API accessibles

### 📞 Obtenir de l'Aide

**Canaux support :**
- 🐛 **Bugs critiques** : [GitHub Issues](https://github.com/TifouDragon/slimboy-discord-bot/issues)
- 💬 **Support technique** : Discord : ninjaiyed10


---

## 🤝 Contribution & Développement

### 🌟 Guidelines Contribution

**Processus contribution :**
1. **🍴 Fork** projet et créer branche feature/nom-feature
2. **💻 Développer** en français pour interface utilisateur
3. **📝 Documenter** toutes fonctions avec docstrings
4. **🧪 Tester** sur serveur développement privé
5. **📬 Soumettre** Pull Request avec description détaillée

### 💻 Setup Environnement Dev

**Prérequis développement :**
```bash
Python 3.11+
discord.py 2.5.2+
Flask 3.1.1+
Git configuré
Serveur Discord test
```

**Installation locale :**
```bash
git clone https://github.com/TifouDragon/slimboy-discord-bot.git
cd slimboy-discord-bot
pip install -r requirements.txt
# Configurer .env avec DISCORD_BOT_TOKEN
python main.py
```

### 🏅 Contributeurs Hall of Fame

**🌟 Contributeurs Actifs :**
- **@Ninja Iyed** - Créateur & Lead Developer
- **@Contributors** - Améliorations diverses (bientôt !)

**🎖️ Reconnaissance Contributions :**
- Badge spécial Discord serveur support
- Mention page GitHub contributeurs
- Accès beta nouvelles fonctionnalités

---

## 📄 Licence & Légal

### ⚖️ Licence MIT

Ce projet est distribué sous licence MIT. Utilisation libre avec attribution obligatoire.

```
MIT License - Copyright (c) 2025 SlimBoy

Permission accordée d'utiliser, copier, modifier, distribuer ce logiciel
avec attribution appropriée à l'auteur original.
```

### 📋 Conditions Utilisation

**✅ Autorisé :**
- Usage commercial et personnel
- Modification code source
- Distribution et redistribution
- Création bots dérivés
- **🎯 Personnalisation du nom du bot**

**❌ Interdit :**
- Suppression attributions auteur
- Revente sans valeur ajoutée significative
- Usage pour activités illégales

**💡 Note spéciale :** Vous pouvez changer le nom du bot, mais merci de conserver l'attribution à l'auteur original dans les crédits.

### 🛡️ Limitation Responsabilité

Le développeur n'est pas responsable de :
- Dommages causés par utilisation du bot
- Pertes données serveurs Discord
- Actions modération automatiques
- Interruptions service temporaires

---

## 👨‍💻 Équipe Développement & Remerciements

### 🌟 Équipe Core

**👑 Ninja Iyed** - *Créateur & Lead Developer*
- 🎯 Architecture bot et systèmes avancés
- 🎨 Design interface et expérience utilisateur  
- 🔧 Optimisations performances et stabilité
- 📞 Support communauté et documentation

**Contacts :**
- 💬 Discord : @Ninja Iyed
- 🐙 GitHub : [@TifouDragon](https://github.com/TifouDragon)
- 📧 Support : GitHub Issues

### 🙏 Remerciements Spéciaux

**🏆 Communautés & Projets :**
- **Discord.py Team** - Framework exceptionnel et support technique
- **Replit Platform** - Hébergement et outils développement
- **Railway Hébergement** - Hébergement gratuit
- **GitHub Community** - Plateforme collaboration open source

**🌟 Inspiration & Ressources :**
- **Communauté Discord FR** - Suggestions fonctionnalités
- **Développeurs Bots** - Partage bonnes pratiques
- **Stack Overflow** - Solutions techniques avancées
- **Python Community** - Documentation et tutoriels

---

## ⭐ Soutenez le projet - Star sur GitHub ! ⭐

[![GitHub stars](https://img.shields.io/github/stars/TifouDragon/slimboy-discord-bot?style=social)](https://github.com/TifouDragon/slimboy-discord-bot)

*Développé avec ❤️ par [@Ninja Iyed](https://github.com/TifouDragon) pour révolutionner la modération Discord francophone*

---

**💡 Personnalisez le nom de votre bot selon vos préférences - "SlimBoy" n'est que le nom par défaut !**

**© 2025 SlimBoy Discord Bot v2.2.1 - Tous droits réservés • Licence MIT**

</div>