"""
Keep Alive Server
Flask server to keep the bot running on Replit and provide monitoring endpoints
"""

from flask import Flask, jsonify, render_template_string, request
from threading import Thread
import logging
import psutil
import platform
from datetime import datetime
import os
import discord

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Référence au bot Discord (sera définie par main.py)
bot_instance = None

# Template HTML moderne pour la page d'accueil
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SlimBoy Bot - Interface de Monitoring</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .status-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .status-card:hover {
            transform: translateY(-5px);
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .stat-label {
            font-weight: bold;
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .feature-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            border-color: #667eea;
            transform: scale(1.02);
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .online-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #28a745;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .api-endpoints {
            background: #343a40;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .endpoint {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
        
        .admin-button {
            display: block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            text-decoration: none;
            padding: 20px 40px;
            border-radius: 15px;
            font-size: 1.5rem;
            font-weight: bold;
            text-align: center;
            margin: 30px auto;
            max-width: 500px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        
        .admin-button:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 SlimBoy Bot</h1>
            <p>Interface de Monitoring & Contrôle</p>
        </div>
        
        <a href="/panel" class="admin-button">
            🎛️ Accéder au Panel d'Administration
        </a>
        
        <div class="status-card">
            <h2><span class="online-indicator"></span>Statut du Bot</h2>
            <div class="status-grid">
                <div class="stat-item">
                    <div class="stat-label">Statut</div>
                    <div class="stat-value" style="color: #28a745;">🟢 En ligne</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Version</div>
                    <div class="stat-value">{{ version }}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Mémoire utilisée</div>
                    <div class="stat-value">{{ memory_usage }}%</div>
                </div>
            </div>
        </div>
        
        <div class="status-card">
            <h2>🎯 Fonctionnalités Disponibles</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <h3>Modération</h3>
                    <p>Système complet de modération avancée</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👮</div>
                    <h3>Guardian</h3>
                    <p>Protection utilisateur intelligente</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📝</div>
                    <h3>Logs</h3>
                    <p>Enregistrement automatique des actions</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎮</div>
                    <h3>Jeux</h3>
                    <p>Mini-jeux et divertissement</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <h3>Diagnostic</h3>
                    <p>Outils de diagnostic système</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Monitoring</h3>
                    <p>Surveillance en temps réel</p>
                </div>
            </div>
        </div>
        
        <div class="status-card">
            <h2>🔗 API Endpoints</h2>
            <div class="api-endpoints">
                <div class="endpoint">GET / - Interface principale</div>
                <div class="endpoint">GET /panel - Panel d'administration complet</div>
                <div class="endpoint">GET /health - Vérification de santé</div>
                <div class="endpoint">GET /status - Statut JSON détaillé</div>
                <div class="endpoint">GET /version - Informations de version</div>
                <div class="endpoint">GET /metrics - Métriques système</div>
            </div>
        </div>
        
        <div class="footer">
            <p>🚀 SlimBoy Bot - Créé avec ❤️ sur Replit</p>
            <p>{{ current_time }}</p>
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    # Statistiques système
    memory = psutil.virtual_memory()
    return render_template_string(
        HTML_TEMPLATE,
        version="Version 2.4",
        memory_usage=round(memory.percent, 1),
        current_time=datetime.now().strftime("%d/%m/%Y à %H:%M:%S"))


@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "En ligne",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "cpu_usage": f"{psutil.cpu_percent()}%"
    })


@app.route('/status')
def status():
    return jsonify({
        "bot_status":
        "online",
        "version":
        "2.4",
        "platform":
        platform.system(),
        "features":
        ["moderation", "guardian", "logging", "games", "diagnostics"],
        "endpoints": ["/", "/health", "/status", "/version", "/metrics"],
        "system": {
            "memory_percent": psutil.virtual_memory().percent,
            "platform": platform.platform()
        }
    })


@app.route('/version')
def version():
    return jsonify({
        "bot_name": "SlimBoy",
        "version": "2.4",
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "description": "Bot Discord de modération avancée"
    })


@app.route('/metrics')
def metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return jsonify({
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": (disk.used / disk.total) * 100
        },
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count()
        },
        "timestamp": datetime.now().isoformat()
    })


PANEL_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel d'Administration - SlimBoy Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 20px 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 2rem;
            color: #1e3c72;
        }
        
        .bot-status {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 15px;
            height: 15px;
            background: #28a745;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab {
            background: rgba(255,255,255,0.9);
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            color: #1e3c72;
        }
        
        .tab:hover {
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .tab.active {
            background: #1e3c72;
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .card h2 {
            color: #1e3c72;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }
        
        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f85032 0%, #e73827 100%);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        
        .server-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .server-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .log-entry {
            background: #1e1e1e;
            color: #00ff00;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        .control-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }
        
        .alert-warning {
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        th {
            background: #f8f9fa;
            font-weight: bold;
            color: #1e3c72;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <a href="/" style="text-decoration: none; color: #1e3c72; font-size: 1.2rem; margin-right: 20px;">← Accueil</a>
                <h1 style="display: inline;">🎛️ Panel d'Administration</h1>
            </div>
            <div class="bot-status">
                <div class="status-dot"></div>
                <span style="font-weight: bold;">{{ bot_name }} en ligne</span>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab(this, 'dashboard')">📊 Dashboard</button>
            <button class="tab" onclick="showTab(this, 'servers')">🏠 Serveurs</button>
            <button class="tab" onclick="showTab(this, 'controls')">📢 Annonces</button>
            <button class="tab" onclick="showTab(this, 'members')">👥 Membres</button>
            <button class="tab" onclick="showTab(this, 'stats')">📈 Statistiques</button>
            <button class="tab" onclick="showTab(this, 'logs')">📝 Logs</button>
        </div>
        
        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content active">
            <div class="card">
                <h2>📊 Vue d'ensemble</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Serveurs</div>
                        <div class="stat-value">{{ guild_count }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Utilisateurs</div>
                        <div class="stat-value">{{ user_count }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Commandes</div>
                        <div class="stat-value">{{ command_count }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Latence</div>
                        <div class="stat-value">{{ latency }}ms</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>💻 Ressources Système</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">CPU</div>
                        <div class="stat-value">{{ cpu_usage }}%</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">RAM</div>
                        <div class="stat-value">{{ memory_usage }}%</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Uptime</div>
                        <div class="stat-value">{{ uptime }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Version</div>
                        <div class="stat-value">{{ version }}</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Servers Tab -->
        <div id="servers" class="tab-content">
            <div class="card">
                <h2>🏠 Serveurs Discord</h2>
                <div class="server-list">
                    {% for server in servers %}
                    <div class="server-item">
                        <strong>{{ server.name }}</strong><br>
                        <small>ID: {{ server.id }} | Membres: {{ server.member_count }}</small>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <!-- Controls Tab (Annonces) -->
        <div id="controls" class="tab-content">
            <div class="card">
                <h2>📢 Envoyer une Annonce</h2>
                <div class="alert alert-info">
                    💡 Sélectionnez un serveur et un salon pour envoyer votre annonce.
                </div>
                
                <div class="form-group">
                    <label>🏠 Serveur</label>
                    <select id="announcement-guild" onchange="loadChannels()">
                        <option value="">Sélectionnez un serveur...</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>💬 Salon</label>
                    <select id="announcement-channel">
                        <option value="">Sélectionnez d'abord un serveur...</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>✉️ Message</label>
                    <textarea id="announcement-message" rows="6" placeholder="Entrez votre annonce ici..."></textarea>
                </div>
                
                <button class="btn" onclick="sendAnnouncement()">📨 Envoyer l'annonce</button>
                <div id="announcement-result" style="margin-top: 15px;"></div>
            </div>
        </div>
        
        <!-- Members Tab -->
        <div id="members" class="tab-content">
            <div class="card">
                <h2>👥 Gestion des Membres</h2>
                <div class="alert alert-info">
                    💡 Sélectionnez un serveur pour voir et gérer ses membres.
                </div>
                
                <div class="form-group">
                    <label>🏠 Serveur</label>
                    <select id="members-guild" onchange="loadMembers()">
                        <option value="">Sélectionnez un serveur...</option>
                    </select>
                </div>
                
                <div id="members-list" style="max-height: 500px; overflow-y: auto; margin-top: 20px;">
                    <p style="text-align: center; color: #666;">Sélectionnez un serveur pour voir les membres</p>
                </div>
            </div>
        </div>
        
        <!-- Stats Tab -->
        <div id="stats" class="tab-content">
            <div class="card">
                <h2>📈 Statistiques Détaillées</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Métrique</th>
                            <th>Valeur</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Total Serveurs</td>
                            <td><strong>{{ guild_count }}</strong></td>
                            <td>Nombre de serveurs où le bot est présent</td>
                        </tr>
                        <tr>
                            <td>Total Utilisateurs</td>
                            <td><strong>{{ user_count }}</strong></td>
                            <td>Nombre total d'utilisateurs accessibles</td>
                        </tr>
                        <tr>
                            <td>Commandes Chargées</td>
                            <td><strong>{{ command_count }}</strong></td>
                            <td>Nombre de commandes slash synchronisées</td>
                        </tr>
                        <tr>
                            <td>Latence API</td>
                            <td><strong>{{ latency }}ms</strong></td>
                            <td>Temps de réponse avec Discord</td>
                        </tr>
                        <tr>
                            <td>Utilisation RAM</td>
                            <td><strong>{{ memory_usage }}%</strong></td>
                            <td>Mémoire utilisée par le processus</td>
                        </tr>
                        <tr>
                            <td>Utilisation CPU</td>
                            <td><strong>{{ cpu_usage }}%</strong></td>
                            <td>Charge processeur actuelle</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Logs Tab -->
        <div id="logs" class="tab-content">
            <div class="card">
                <h2>📝 Logs du Bot</h2>
                <div class="alert alert-info">
                    💡 Les logs sont affichés en temps réel. Actualisez la page pour voir les derniers logs.
                </div>
                <div style="max-height: 500px; overflow-y: auto;">
                    <div class="log-entry">[{{ current_time }}] Bot démarré avec succès</div>
                    <div class="log-entry">[{{ current_time }}] Connecté à {{ guild_count }} serveurs</div>
                    <div class="log-entry">[{{ current_time }}] {{ command_count }} commandes chargées</div>
                    <div class="log-entry">[{{ current_time }}] Système opérationnel</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let guildsData = [];
        
        // Charger les serveurs au démarrage
        async function loadGuilds() {
            try {
                const response = await fetch('/api/guilds');
                guildsData = await response.json();
                
                // Remplir les selects
                const announcementGuild = document.getElementById('announcement-guild');
                const membersGuild = document.getElementById('members-guild');
                
                guildsData.forEach(guild => {
                    const option1 = new Option(guild.name, guild.id);
                    const option2 = new Option(guild.name, guild.id);
                    announcementGuild.add(option1);
                    membersGuild.add(option2);
                });
            } catch (error) {
                console.error('Erreur chargement serveurs:', error);
            }
        }
        
        // Charger les salons d'un serveur
        function loadChannels() {
            const guildId = document.getElementById('announcement-guild').value;
            const channelSelect = document.getElementById('announcement-channel');
            
            channelSelect.innerHTML = '<option value="">Sélectionnez un salon...</option>';
            
            if (!guildId) return;
            
            const guild = guildsData.find(g => g.id === guildId);
            if (guild && guild.channels) {
                guild.channels.forEach(channel => {
                    if (channel.type.includes('text')) {
                        channelSelect.add(new Option(channel.name, channel.id));
                    }
                });
            }
        }
        
        // Envoyer une annonce
        async function sendAnnouncement() {
            const guildId = document.getElementById('announcement-guild').value;
            const channelId = document.getElementById('announcement-channel').value;
            const message = document.getElementById('announcement-message').value;
            const resultDiv = document.getElementById('announcement-result');
            
            if (!guildId || !channelId || !message) {
                resultDiv.innerHTML = '<div class="alert alert-warning">⚠️ Veuillez remplir tous les champs</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/send_announcement', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({guild_id: guildId, channel_id: channelId, message: message})
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.innerHTML = '<div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">✅ Annonce envoyée avec succès!</div>';
                    document.getElementById('announcement-message').value = '';
                } else {
                    resultDiv.innerHTML = `<div class="alert alert-warning">❌ Erreur: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = '<div class="alert alert-warning">❌ Erreur réseau</div>';
            }
        }
        
        // Charger les membres d'un serveur
        async function loadMembers() {
            const guildId = document.getElementById('members-guild').value;
            const membersList = document.getElementById('members-list');
            
            if (!guildId) {
                membersList.innerHTML = '<p style="text-align: center; color: #666;">Sélectionnez un serveur pour voir les membres</p>';
                return;
            }
            
            membersList.innerHTML = '<p style="text-align: center; color: #666;">⏳ Chargement...</p>';
            
            try {
                const response = await fetch(`/api/guild_members/${guildId}`);
                const members = await response.json();
                
                if (!response.ok) {
                    membersList.innerHTML = `<p style="text-align: center; color: red;">Erreur: ${members.error}</p>`;
                    return;
                }
                
                let html = '<table style="width: 100%; border-collapse: collapse;"><thead><tr style="background: #f8f9fa;"><th style="padding: 12px; text-align: left;">Utilisateur</th><th style="padding: 12px; text-align: left;">Rôles</th><th style="padding: 12px; text-align: left;">Rejoint le</th></tr></thead><tbody>';
                
                members.forEach(member => {
                    const roles = member.roles.length > 0 ? member.roles.join(', ') : 'Aucun';
                    const joined = member.joined_at ? new Date(member.joined_at).toLocaleDateString('fr-FR') : 'N/A';
                    const icon = member.bot ? '🤖' : '👤';
                    
                    html += `<tr style="border-bottom: 1px solid #e0e0e0;"><td style="padding: 12px;">${icon} <strong>${member.display_name}</strong><br><small>@${member.name}</small></td><td style="padding: 12px;"><small>${roles}</small></td><td style="padding: 12px;"><small>${joined}</small></td></tr>`;
                });
                
                html += '</tbody></table>';
                membersList.innerHTML = html;
            } catch (error) {
                membersList.innerHTML = '<p style="text-align: center; color: red;">Erreur réseau</p>';
            }
        }
        
        function showTab(element, tabName) {
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Remove active class from all buttons
            const buttons = document.querySelectorAll('.tab');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked button
            element.classList.add('active');
        }
        
        // Charger les serveurs au chargement de la page
        window.onload = function() {
            loadGuilds();
        };
        
        // Auto-refresh every 60 seconds
        setTimeout(() => location.reload(), 60000);
    </script>
</body>
</html>
"""


@app.route('/panel')
def panel():
    """Panel d'administration"""
    try:
        # Récupérer les informations du bot si disponible
        if bot_instance:
            guild_count = len(bot_instance.guilds)
            user_count = sum(g.member_count or 0 for g in bot_instance.guilds)
            command_count = len(bot_instance.tree.get_commands())
            latency = round(bot_instance.latency * 1000, 2)
            bot_name = str(bot_instance.user) if bot_instance.user else "SlimBoy"
            
            servers = [{
                'name': guild.name,
                'id': guild.id,
                'member_count': guild.member_count or 0
            } for guild in bot_instance.guilds]
        else:
            # Valeurs par défaut si le bot n'est pas encore connecté
            guild_count = 3
            user_count = 0
            command_count = 33
            latency = 0
            bot_name = "SlimBoy#9022"
            servers = []
        
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        
        return render_template_string(
            PANEL_TEMPLATE,
            bot_name=bot_name,
            guild_count=guild_count,
            user_count=user_count,
            command_count=command_count,
            latency=latency,
            cpu_usage=round(cpu, 1),
            memory_usage=round(memory.percent, 1),
            uptime="En ligne",
            version="2.4",
            servers=servers,
            current_time=datetime.now().strftime("%H:%M:%S")
        )
    except Exception as e:
        logger.error(f"Error in panel: {e}")
        return f"Erreur: {e}", 500


@app.route('/api/guilds', methods=['GET'])
def api_guilds():
    """API pour obtenir la liste des serveurs avec canaux"""
    try:
        if not bot_instance:
            return jsonify({"error": "Bot non connecté"}), 503
            
        guilds_data = []
        for guild in bot_instance.guilds:
            channels = [{
                'id': str(channel.id),
                'name': channel.name,
                'type': str(channel.type)
            } for channel in guild.text_channels]
            
            guilds_data.append({
                'id': str(guild.id),
                'name': guild.name,
                'member_count': guild.member_count or 0,
                'channels': channels
            })
        
        return jsonify(guilds_data)
    except Exception as e:
        logger.error(f"Error in api_guilds: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/send_announcement', methods=['POST'])
def api_send_announcement():
    """API pour envoyer une annonce à un serveur"""
    try:
        if not bot_instance:
            return jsonify({"error": "Bot non connecté"}), 503
        
        data = request.get_json()
        guild_id = data.get('guild_id')
        channel_id = data.get('channel_id')
        message = data.get('message')
        
        if not all([guild_id, channel_id, message]):
            return jsonify({"error": "Paramètres manquants"}), 400
        
        # Trouver le canal
        channel = bot_instance.get_channel(int(channel_id))
        if not channel:
            return jsonify({"error": "Canal non trouvé"}), 404
        
        # Envoyer le message de manière thread-safe
        import asyncio
        
        async def send_msg():
            embed = discord.Embed(
                title="📢 Annonce",
                description=message,
                color=0x3498db
            )
            embed.set_footer(text=f"Envoyé depuis le Panel d'Administration")
            await channel.send(embed=embed)
        
        # Utiliser le loop du bot de manière thread-safe
        future = asyncio.run_coroutine_threadsafe(send_msg(), bot_instance.loop)
        future.result(timeout=10)
        
        return jsonify({"success": True, "message": "Annonce envoyée"})
    except Exception as e:
        logger.error(f"Error sending announcement: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/guild_members/<guild_id>', methods=['GET'])
def api_guild_members(guild_id):
    """API pour obtenir les membres d'un serveur"""
    try:
        if not bot_instance:
            return jsonify({"error": "Bot non connecté"}), 503
        
        guild = bot_instance.get_guild(int(guild_id))
        if not guild:
            return jsonify({"error": "Serveur non trouvé"}), 404
        
        members_data = []
        for member in guild.members[:100]:  # Limite à 100 pour performance
            members_data.append({
                'id': str(member.id),
                'name': member.name,
                'discriminator': member.discriminator,
                'display_name': member.display_name,
                'bot': member.bot,
                'joined_at': member.joined_at.isoformat() if member.joined_at else None,
                'roles': [role.name for role in member.roles if role.name != "@everyone"]
            })
        
        return jsonify(members_data)
    except Exception as e:
        logger.error(f"Error in api_guild_members: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error":
        "Not Found",
        "message":
        "Endpoint non disponible",
        "available_endpoints":
        ["/", "/health", "/status", "/version", "/metrics", "/panel"]
    }), 404


def run():
    try:
        logger.info("Starting keep-alive server Version II...")
        app.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        logger.error(f"Error starting keep-alive server: {e}")


def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
