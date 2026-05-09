# 🚀 GUIDE DE DÉPLOIEMENT EN PRODUCTION - UNSS Goma

## 📋 Pré-requis

- **Serveur Linux** (Ubuntu 20.04+, Debian 11+ recommandé)
- **Python 3.8+**
- **Pip** et **virtualenv**
- **Nginx** (reverse proxy)
- **Domaine** avec SSL/TLS
- **SMTP** configuré (Gmail, SendGrid, etc.)

---

## 🔒 ÉTAPE 1 - Sécurité et Configuration

### 1.1 Cloner et préparer le projet

```bash
git clone <votre-repo> /var/www/unss-goma
cd /var/www/unss-goma
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.2 Configurer les variables d'environnement

```bash
cp .env.example .env
nano .env  # ou votre éditeur préféré
```

**Remplissez les valeurs importantes:**
- `FLASK_ENV=production`
- `SECRET_KEY=` (générez avec `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD` (Gmail ou autre)
- Tous les autres paramètres

### 1.3 Créer les dossiers nécessaires

```bash
mkdir -p logs uploads/articles uploads/membres
chmod 755 logs uploads
```

### 1.4 Initialiser la base de données

```bash
source venv/bin/activate
python3 app.py  # Lance une fois pour créer les tables
# Ctrl+C pour arrêter
```

⚠️ **IMPORTANT:** Après le premier démarrage, modifiez le mot de passe admin par défaut!

---

## 🐍 ÉTAPE 2 - Configurer Gunicorn

### 2.1 Tester Gunicorn localement

```bash
source venv/bin/activate
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

Vérifiez que l'application démarre sans erreur.

### 2.2 Créer un service Systemd

```bash
sudo nano /etc/systemd/system/unss-goma.service
```

Contenu:
```ini
[Unit]
Description=UNSS Goma Flask Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/unss-goma
Environment="PATH=/var/www/unss-goma/venv/bin"
Environment="FLASK_ENV=production"
EnvironmentFile=/var/www/unss-goma/.env
ExecStart=/var/www/unss-goma/venv/bin/gunicorn -c gunicorn_config.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2.3 Activer le service

```bash
sudo systemctl daemon-reload
sudo systemctl enable unss-goma
sudo systemctl start unss-goma
sudo systemctl status unss-goma
```

Vérifiez que le service est actif:
```bash
sudo journalctl -u unss-goma -f  # Pour voir les logs
```

---

## 🌐 ÉTAPE 3 - Configurer Nginx

### 3.1 Créer la configuration Nginx

```bash
sudo nano /etc/nginx/sites-available/unss-goma
```

Contenu:
```nginx
upstream unss_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    listen [::]:80;
    server_name votre-domaine.com www.votre-domaine.com;

    # Redirection HTTP -> HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name votre-domaine.com www.votre-domaine.com;

    # Certificats SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;

    # Configuration SSL moderne
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxying
    location / {
        proxy_pass http://unss_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # Servir les fichiers statiques directement
    location /static/ {
        alias /var/www/unss-goma/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads/ {
        alias /var/www/unss-goma/uploads/;
        expires 7d;
    }

    # Logs
    access_log /var/log/nginx/unss-goma-access.log;
    error_log /var/log/nginx/unss-goma-error.log;
}
```

### 3.2 Activer le site

```bash
sudo ln -s /etc/nginx/sites-available/unss-goma /etc/nginx/sites-enabled/
sudo nginx -t  # Vérifier la configuration
sudo systemctl restart nginx
```

### 3.3 Configurer SSL avec Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d votre-domaine.com -d www.votre-domaine.com
```

---

## 📧 ÉTAPE 4 - Configurer le Mail

### Pour Gmail:

1. Activez l'authentification 2FA: https://myaccount.google.com/security
2. Générez un mot de passe d'application: https://myaccount.google.com/apppasswords
3. Sélectionnez "Mail" et "Windows Computer"
4. Copiez le mot de passe généré (16 caractères)
5. Dans `.env`:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=votre.email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

### Pour SendGrid:

1. Créez un compte et une API key
2. Dans `.env`:
   ```
   MAIL_SERVER=smtp.sendgrid.net
   MAIL_PORT=587
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=SG.votre_api_key
   ```

---

## 💾 ÉTAPE 5 - Sauvegardes et Monitoring

### 5.1 Sauvegardes automatiques

Créer un script `/var/www/unss-goma/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/unss-goma"
DB_FILE="/var/www/unss-goma/sauveteurs_goma.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/sauveteurs_goma_$TIMESTAMP.db

# Garder seulement les 30 dernières sauvegardes
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "✓ Sauvegarde créée: $BACKUP_DIR/sauveteurs_goma_$TIMESTAMP.db"
```

Ajouter à crontab:
```bash
sudo crontab -e
# Ajouter la ligne:
0 2 * * * /var/www/unss-goma/backup.sh  # Tous les jours à 2h du matin
```

### 5.2 Monitoring

Installer `htop`, `iotop` pour surveiller l'application:
```bash
sudo apt-get install htop iotop
```

Vérifier les logs:
```bash
sudo journalctl -u unss-goma -f
tail -f /var/log/nginx/unss-goma-error.log
```

---

## ✅ CHECKLIST DE DÉPLOIEMENT

- [ ] Variables d'env configurées (.env)
- [ ] Secret key unique et fort
- [ ] Email testé et fonctionnel
- [ ] Base de données initialisée
- [ ] Service Gunicorn créé et actif
- [ ] Nginx configuré comme reverse proxy
- [ ] SSL/TLS configuré (Let's Encrypt)
- [ ] Domaine pointe vers le serveur
- [ ] Sauvegardes automatiques configurées
- [ ] Logs vérifiés et archivés
- [ ] Droits d'accès aux fichiers correct
- [ ] Pare-feu configuré (ports 80, 443 ouverts)
- [ ] Admin par défaut changé

---

## 🐛 DÉPANNAGE

### Le service n'a pas l'air de démarrer

```bash
sudo systemctl status unss-goma
sudo journalctl -u unss-goma -n 50  # Affiche les 50 dernières lignes de log
```

### Le mail n'est pas envoyé

```bash
# Testez l'authentification SMTP
python3 -m smtplib -s SMTP smtp.gmail.com 587
```

### Nginx affiche une erreur 502

```bash
# Vérifiez que Gunicorn fonctionne
sudo systemctl status unss-goma
# Vérifiez la config Nginx
sudo nginx -t
```

### Permission denied sur les uploads

```bash
sudo chown -R www-data:www-data /var/www/unss-goma/uploads
sudo chmod 755 /var/www/unss-goma/uploads
```

---

## 📈 AMÉLIORATIONS FUTURES

- [ ] Redis pour les sessions
- [ ] PostgreSQL au lieu de SQLite
- [ ] CDN pour les fichiers statiques
- [ ] Rate limiting avancé
- [ ] 2FA pour les admins
- [ ] Audit logging complet
- [ ] Monitoring et alertes (Prometheus)
- [ ] Containerisation Docker

---

**Version**: 2.0  
**Dernière mise à jour**: Mai 2025  
**Support**: contact@sauveteursgoma.org
