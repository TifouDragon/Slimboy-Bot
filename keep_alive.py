
"""
Keep Alive Server
Flask server to keep the bot running on Railway and provide monitoring endpoints
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
        <title>SlimBoy Discord Bot</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { text-align: center; color: #7289da; }
            .status { background: #43b581; color: white; padding: 10px; border-radius: 5px; text-align: center; }
            .info { background: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1 class="header">🤖 SlimBoy Discord Bot</h1>
        <div class="status">✅ Bot is running on Railway</div>
        <div class="info">
            <h3>📋 Fonctionnalités</h3>
            <ul>
                <li>📝 Liste des bannis avec pagination</li>
                <li>🔍 Recherche avancée par pseudo/ID</li>
                <li>⚡ Commandes de modération complètes</li>
                <li>🛡️ Interface française moderne</li>
            </ul>
        </div>
        <div class="info">
            <h3>🔗 Endpoints</h3>
            <ul>
                <li><a href="/status">/status</a> - Statut JSON du bot</li>
                <li><a href="/health">/health</a> - Health check</li>
            </ul>
        </div>
        <p style="text-align: center; color: #666;">
            Développé par <strong>@Ninja Iyed</strong> | Hébergé sur Railway
        </p>
    </body>
    </html>
    """

@app.route('/status')
def status():
    """Bot status endpoint for monitoring"""
    return jsonify({
        "status": "online",
        "platform": "Railway",
        "bot_name": "SlimBoy",
        "version": "1.2.1",
        "author": "@Ninja Iyed"
    })

@app.route('/health')
def health():
    """Health check endpoint for uptime monitoring"""
    return "OK", 200

def keep_alive():
    """Start the Flask server in a separate thread"""
    def run():
        # Get port from Railway environment or default to 5000
        port = int(os.environ.get('PORT', 5000))
        logger.info("Starting keep-alive server...")
        app.run(host='0.0.0.0', port=port, debug=False)
        logger.info(f"Keep-alive server started on port {port}")
    
    server = threading.Thread(target=run, daemon=True)
    server.start()
