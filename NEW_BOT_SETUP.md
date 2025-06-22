
# Instructions pour créer un nouveau bot Discord

## Étapes dans le Discord Developer Portal :

1. Aller sur https://discord.com/developers/applications
2. Cliquer "New Application"
3. Donner un nom (ex: "SlimBoy-V2")
4. Dans l'onglet "Bot" :
   - Cliquer "Add Bot"
   - **IMPORTANT:** Désactiver "Require OAuth2 Code Grant" ❌
   - Activer "Public Bot" ✅
   - Copier le token

5. Dans l'onglet "OAuth2" → "General" :
   - **IMPORTANT:** Désactiver "Require OAuth2 Code Grant" ❌

6. Utiliser ce lien d'invitation :
   ```
   https://discord.com/api/oauth2/authorize?client_id=NOUVEAU_CLIENT_ID&permissions=1374389502966&scope=bot%20applications.commands
   ```

## Mettre à jour le token dans Replit :
- Aller dans l'onglet "Secrets"
- Modifier "DISCORD_BOT_TOKEN" avec le nouveau token
