# 🤖 Configuration Keep-Alive pour SlimBoy

## 📋 Guide de Configuration

### 1. Railway (Automatique)
Railway maintient automatiquement votre bot en ligne. Aucune configuration supplémentaire nécessaire !

### 2. UptimeRobot (Optionnel)
Si vous voulez une surveillance externe :
- Rendez-vous sur [UptimeRobot.com](https://uptimerobot.com)
- Créez un compte gratuit (10 monitors inclus)
- **Monitor URL** : `https://votre-app.railway.app/health`
- **Monitor Name** : `SlimBoy Discord Bot`
- **Monitoring Interval** : `5 minutes`

### 3. Endpoint de santé
Votre bot expose automatiquement :
- `/` - Page d'accueil du bot
- `/status` - Statut JSON du bot  
- `/health` - Endpoint de santé (retourne "OK")

## ✅ Avantages Railway

- **Uptime automatique** - Pas besoin de services externes
- **Redémarrage automatique** en cas d'erreur
- **Logs en temps réel** pour monitoring
- **Variables d'environnement** sécurisées

## 🌐 URL de monitoring

Votre endpoint : `https://votre-app.railway.app/health`