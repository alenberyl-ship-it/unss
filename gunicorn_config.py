"""
Configuration Gunicorn pour UNSS Goma
Utiliser: gunicorn -c gunicorn_config.py app:app
"""
import multiprocessing
import os
from dotenv import load_dotenv

load_dotenv()

# Nombre de workers (4 x CPU + 1 généralement recommandé)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'  # ou 'gevent' pour async

# Binding
bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"

# Timeouts
timeout = 60
graceful_timeout = 30

# Logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'

# Process naming
proc_name = 'unss-goma'

# Server mechanics
daemon = False
pidfile = 'gunicorn.pid'
umask = 0o022

# Server hooks
def on_starting(server):
    """Hook appelé au démarrage"""
    import logging
    logging.info("🚀 Serveur Gunicorn démarrage...")

def on_exit(server):
    """Hook appelé à l'arrêt"""
    import logging
    logging.info("🛑 Serveur Gunicorn arrêt...")

# SSL (mettre à True si certificat disponible)
# keyfile = "/etc/ssl/private/unss.key"
# certfile = "/etc/ssl/certs/unss.crt"

# Headers de sécurité (peuvent être définis dans Flask aussi)
# raw_env = [
#     'FLASK_ENV=production',
# ]
