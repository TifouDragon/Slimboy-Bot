"""
Keep Alive Server
Flask server to keep the bot running on Replit and provide monitoring endpoints
"""

from flask import Flask, jsonify, render_template_string
from threading import Thread
import logging
import psutil
import platform
from datetime import datetime

logger = logging.getLogger(__name__)

app = Flask(__name__)

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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 SlimBoy Bot</h1>
            <p>Interface de Monitoring & Contrôle</p>
        </div>
        
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
        version="Version 2.3.1",
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
        "2.3.1",
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
        "version": "2.3.1",
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


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error":
        "Not Found",
        "message":
        "Endpoint non disponible",
        "available_endpoints":
        ["/", "/health", "/status", "/version", "/metrics"]
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
