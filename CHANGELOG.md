
# 📋 Changelog SlimBoy

## Version 2.2.2 (30/06/2025)

### 🔧 Améliorations
- **🔒 Permissions Commandes** : Amélioration des permissions pour les commandes de salons temporaires
- **👥 Visibilité Rôles** : Les commandes temp-channels sont maintenant visibles uniquement aux utilisateurs avec permissions appropriées
- **🐛 Corrections Bugs** : Résolution d'erreurs de syntaxe dans le système de modération

### 🛠️ Modifications Techniques
- Ajout de `@app_commands.default_permissions(manage_channels=True)` pour toutes les commandes temporaires
- Correction de l'erreur de syntaxe ligne 875 dans moderation.py
- Optimisation des vérifications de permissions

---

## Version 2.2.1 (29/12/2024)

### 🆕 Nouveautés
- **👮 Système Guardian** : Protection utilisateur avancée contre les abus de modération
- **🎮 Commandes de Jeux** : Mini-jeux intégrés pour divertissement communautaire
- **🛡️ Protection Invisible** : Commandes de modération invisibles pour plus de discrétion

### 🔧 Améliorations
- **⚡ Interface Flask Optimisée** : Suppression des éléments inutiles (CPU, plateforme, timestamp)
- **🐛 Correction Erreurs 404** : Amélioration de la stabilité et gestion d'erreurs
- **📱 Performance** : Interface web plus légère et responsive

### 🔒 Sécurité
- **🛡️ Guardian Protection** : Système de protection contre les abus de pouvoir
- **👑 Hiérarchie Respectée** : Seuls les rôles supérieurs peuvent agir sur un utilisateur protégé
- **🔐 Exceptions Configurables** : Rôles de modération avec permissions spéciales

### 🎯 Fonctionnalités Techniques
- Commandes invisibles pour la modération discrète
- Système de jeux extensible et modulaire
- Optimisation des performances du serveur Flask
- Amélioration de la gestion des erreurs

---

## Version 2.2.0 (22/12/2024)

### 🆕 Fonctionnalités Majeures
- **📝 Système de Logs Configurable** : Enregistrement automatique personnalisable
- **🔔 Notifications GitHub** : Alertes automatiques nouvelles versions
- **🎯 Commandes Bonus** : Système extensible pour fonctionnalités additionnelles
- **🌐 Interface Web Modernisée** : Dashboard Version 2.2 avec design premium

### 🔧 Améliorations Système
- **⚡ Keep-alive Optimisé** : Serveur Flask amélioré pour Replit
- **🛡️ Modération Avancée** : Nouvelles fonctionnalités de gestion utilisateurs
- **📊 Architecture Modulaire** : Réorganisation complète du code
- **🎨 Interface Utilisateur** : Design français premium uniformisé

---

*Développé avec ❤️ par @Ninja Iyed*
