"""
Keep Alive Server
Flask server to keep the bot running on Replit and provide monitoring endpoints
"""

from flask import Flask, jsonify
import threading
import logging
import os

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def home():
    """Home page with bot information"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SlimBoy Discord Bot - Version II</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                max-width: 900px; 
                margin: 50px auto; 
                padding: 30px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                line-height: 1.6;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            .header { text-align: center; color: #ffffff; margin-bottom: 30px; }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .version-badge { 
                background: #ff6b6b; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 20px; 
                font-size: 0.9em; 
                font-weight: bold;
                display: inline-block;
                margin-top: 10px;
            }
            .status { 
                background: linear-gradient(45deg, #43b581, #4caf50); 
                color: white; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center; 
                font-size: 1.2em;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(67, 181, 129, 0.3);
            }
            .info { 
                background: rgba(255, 255, 255, 0.1); 
                padding: 20px; 
                border-radius: 15px; 
                margin: 20px 0; 
                border-left: 4px solid #7289da;
            }
            .info h3 { color: #7289da; margin-bottom: 15px; }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .feature-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #ff6b6b;
            }
            .bonus-section {
                background: linear-gradient(45deg, #ff6b6b, #ffa726);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.02); }
                100% { transform: scale(1); }
            }
            ul { list-style: none; padding: 0; }
            li { 
                background: rgba(255, 255, 255, 0.1); 
                margin: 8px 0; 
                padding: 10px 15px; 
                border-radius: 8px; 
                border-left: 3px solid #7289da;
            }
            .footer {
                text-align: center; 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid rgba(255, 255, 255, 0.2);
            }
            a { color: #7289da; text-decoration: none; }
            a:hover { color: #5865f2; text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 SlimBoy Discord Bot</h1>
                <div class="version-badge">Version 2.2 </div>
                <p>Bot de Modération Avancé avec Commandes Bonus</p>
            </div>

            <div class="status">✅ Bot opérationnel sur Replit</div>

            <div class="bonus-section">
                <h3>🎉 NOUVEAUTÉ : Commandes Bonus Disponibles !</h3>
                <p>En plus des fonctionnalités de modération, découvrez nos commandes fun et utilitaires !</p>
                <small>Plus de commandes bonus arrivent dans les prochaines versions...</small>
            </div>

            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🛡️ Modération Complète</h4>
                    <ul>
                        <li>📝 Liste des bannis paginée</li>
                        <li>🔍 Recherche avancée</li>
                        <li>⚡ Ban/Kick/Timeout</li>
                        <li>⏰ Ban temporaire</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <h4>🎯 Commandes Bonus</h4>
                    <ul>
                        <li>🎲 Commandes fun (à venir)</li>
                        <li>🛠️ Utilitaires serveur</li>
                        <li>📊 Statistiques avancées</li>
                        <li>🎮 Mini-jeux (prévu)</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <h4>📋 Système Avancé</h4>
                    <ul>
                        <li>📝 Logs configurables</li>
                        <li>🔔 Notifications GitHub</li>
                        <li>🎨 Interface française</li>
                        <li>🌐 Dashboard web (futur)</li>
                    </ul>
                </div>
            </div>

            <div class="info">
                <h3>🔗 Endpoints API</h3>
                <ul>
                    <li><a href="/status">/status</a> - Statut JSON du bot</li>
                    <li><a href="/health">/health</a> - Health check pour monitoring</li>
                    <li><a href="/version">/version</a> - Informations de version</li>
                </ul>
            </div>

            <div class="footer">
                <p><strong>Développé avec ❤️ par @Ninja Iyed</strong></p>
                <p>Hébergé sur Replit • Version II en développement actif</p>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/status')
def status():
    """Bot status endpoint for monitoring"""
    return jsonify({
        "status": "online",
        "platform": "Replit",
        "bot_name": "SlimBoy",
        "version": "2.2.0",
        "version_name": "Version 2.2",
        "author": "@Ninja Iyed",
        "features": {
            "moderation": True,
            "ban_list": True,
            "bonus_commands": True,
            "logging_system": True,
            "update_notifications": True,
            "dashboard": "planned"
        },
        "uptime": "Opérationnel",
        "environment": "Replit"
    })


@app.route('/health')
def health():
    """Health check endpoint for uptime monitoring"""
    return "OK", 200


@app.route('/version')
def version():
    """Version information endpoint"""
    return jsonify({
        "version":
        "2.2.0",
        "version_name":
        "Version 2.2",
        "release_date":
        "2024-12-22",
        "changelog": [
            "🆕 Système de logs configurable",
            "🔔 Notifications de mise à jour GitHub",
            "🎯 Commandes bonus (en développement)", "🌐 Dashboard web planifié",
            "🛡️ Modération avancée améliorée",
            "🎨 Interface utilisateur enrichie"
        ],
        "upcoming_features": [
            "🎲 Commandes fun et divertissement", "🌐 Dashboard web de gestion",
            "📊 Statistiques serveur avancées", "🎮 Mini-jeux intégrés",
            "🤖 IA pour modération automatique"
        ]
    })


def keep_alive():
    """Start the Flask server in a separate thread"""

    def run():
        # Get port from Replit environment or default to 5000
        port = int(os.environ.get('PORT', 5000))
        logger.info("Starting keep-alive server Version II...")
        app.run(host='0.0.0.0', port=port, debug=False)
        logger.info(f"Keep-alive server started on port {port}")

    server = threading.Thread(target=run, daemon=True)
    server.start()
