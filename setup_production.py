#!/usr/bin/env python3
"""
Script de configuration pour le déploiement en production
"""
import os
import sys
import secrets
import re


def generate_secret_key():
    """Génère une clé secrète sécurisée"""
    return secrets.token_urlsafe(32)


def validate_email(email):
    """Valide le format d'une adresse email"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def setup_production():
    """Guide de configuration pour la production"""
    print("\n" + "=" * 60)
    print("  CONFIGURATION DE PRODUCTION - UNSS GOMA")
    print("=" * 60 + "\n")
    
    # Créer le fichier .env s'il n'existe pas
    if os.path.exists('.env'):
        print("⚠️  Le fichier .env existe déjà. Passage à la vérification...")
    else:
        print("📝 Création du fichier .env...\n")
        
        # Demander les informations
        config = {}
        
        # Clé secrète
        print("🔐 SÉCURITÉ")
        config['SECRET_KEY'] = generate_secret_key()
        print(f"✓ Clé secrète générée: {config['SECRET_KEY'][:20]}...\n")
        
        # Environnement
        config['FLASK_ENV'] = 'production'
        config['PORT'] = '5000'
        
        # Email
        print("📧 CONFIGURATION EMAIL")
        config['MAIL_SERVER'] = input("Serveur SMTP (ex: smtp.gmail.com): ").strip()
        config['MAIL_PORT'] = input("Port SMTP (défaut 587): ").strip() or '587'
        config['MAIL_USE_TLS'] = 'True'
        config['MAIL_USERNAME'] = input("Email (utilisateur): ").strip()
        
        if not validate_email(config['MAIL_USERNAME']):
            print("❌ Email invalide!")
            return False
        
        config['MAIL_PASSWORD'] = input("Mot de passe d'application: ").strip()
        config['MAIL_DEFAULT_SENDER'] = input("Email de départ (défaut: noreply@sauveteursgoma.org): ").strip() or 'noreply@sauveteursgoma.org'
        config['CONTACT_EMAIL'] = input("Email de contact (défaut: contact@sauveteursgoma.org): ").strip() or 'contact@sauveteursgoma.org'
        
        # Écrire le fichier .env
        with open('.env', 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        print("\n✓ Fichier .env créé avec succès!\n")
    
    # Vérifier les fichiers importants
    print("📋 VÉRIFICATION DES FICHIERS IMPORTANTS...\n")
    
    required_files = [
        'app.py',
        'database.py',
        'requirements.txt',
        '.env',
        'templates/index.html',
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✓ Tous les fichiers importants sont présents\n")
    
    # Checklist de production
    print("=" * 60)
    print("  CHECKLIST DE DÉPLOIEMENT")
    print("=" * 60 + "\n")
    
    checklist = [
        ("SECRET_KEY défini et unique", ".env"),
        ("Mail configuré et testé", ".env"),
        ("Base de données initialisée", "database.py"),
        ("Logs configurés", "logs/"),
        ("Permissions fichiers correctes", "uploads/"),
        ("SSL/TLS configuré (Nginx/Apache)", "Reverse proxy"),
        ("Gunicorn installé", "requirements.txt"),
        ("Variables d'env en production", "Serveur d'hébergement"),
        ("Firewall/Security Groups", "Fournisseur d'hébergement"),
        ("Sauvegardes automatiques", "Base de données"),
    ]
    
    for i, (item, location) in enumerate(checklist, 1):
        print(f"  [ ] {i}. {item:<45} ({location})")
    
    print("\n" + "=" * 60)
    print("  COMMANDES IMPORTANTES")
    print("=" * 60 + "\n")
    
    print("1️⃣  Installation des dépendances:")
    print("   pip install -r requirements.txt\n")
    
    print("2️⃣  Initialiser la base de données:")
    print("   python app.py  # Une fois pour créer les tables\n")
    
    print("3️⃣  Démarrer avec Gunicorn (production):")
    print("   gunicorn -w 4 -b 0.0.0.0:5000 app:app\n")
    
    print("4️⃣  Ou avec configuration personnalisée:")
    print("   gunicorn -c gunicorn_config.py app:app\n")
    
    print("=" * 60)
    print("  ✓ Configuration terminée!")
    print("=" * 60 + "\n")
    
    return True


if __name__ == '__main__':
    success = setup_production()
    sys.exit(0 if success else 1)
