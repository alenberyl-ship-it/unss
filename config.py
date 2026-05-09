"""
Configuration pour UNSS Goma
"""
import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@sauveteursgoma.org')
    
    # Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    
    # Database
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'sauveteurs_goma.db')
    
    # Contact email
    CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'contact@sauveteursgoma.org')


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True
    MAIL_SUPPRESS_SEND = True


# Sélectionner la configuration selon FLASK_ENV
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
