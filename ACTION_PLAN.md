# ⚡ ACTION PLAN IMMÉDIAT - À Faire Maintenant

**Créé**: Mai 2025  
**Pour**: Équipe DevOps/Hébergement  
**Priorité**: 🔴 CRITIQUE

---

## 📌 Situation Actuelle

✅ **Bonne nouvelle**: L'application **UNSS Goma v2.1** est complètement sécurisée et prête pour production!

⚠️ **Attention**: Quelques configurations finales sont obligatoires avant la mise en ligne.

---

## ⏰ Chronologie Recommandée

### JOUR 1 - Préparation (3 heures)

#### 1️⃣ Matin (1 heure)
- [ ] Lire **QUICK_START.md** (10 min)
- [ ] Lire **PRODUCTION_READY.md** (10 min)
- [ ] Exécuter `test.sh` ou `test.bat` localement (10 min)
- [ ] Vérifier que l'app fonctionne sur http://127.0.0.1:5000 (10 min)
- [ ] Documenter les problèmes rencontrés (20 min)

#### 2️⃣ Midi (1 heure)
- [ ] Lire **DEPLOYMENT.md** complètement (1 heure)
  - Focus sur: Sécurité (section 1), Configuration (section 2)
  - Noter les points pertinents pour votre infrastructure

#### 3️⃣ Après-midi (1 heure)
- [ ] Générer **SECRET_KEY** unique
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] Créer **`.env`** pour production
  ```bash
  cp .env.example .env
  ```
- [ ] Remplir tous les **MAIL_*** variables
  - Pour Gmail: [Générer mot de passe app](https://myaccount.google.com/apppasswords)
- [ ] Ajouter **SECRET_KEY** dans `.env`
- [ ] Tester l'envoi d'email depuis l'app locale

### JOUR 2 - Déploiement (2-3 heures)

#### 4️⃣ Matin (1-2 heures)
**Infrastructure Setup:**
- [ ] Server Linux prêt (Ubuntu 20.04+ recommandé)
- [ ] Python 3.8+ installé
- [ ] Nginx installé
- [ ] SSL certificate (Let's Encrypt)
- [ ] Domain name configured

**Préparation Server:**
```bash
# Connectez-vous au serveur
ssh user@server.com

# Installation base
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx certbot

# Créer l'app directory
sudo mkdir -p /var/www/unss-goma
cd /var/www/unss-goma

# Clone l'application
git clone <votre-repo> .
# OU copier les fichiers manuellement
```

#### 5️⃣ Midi (1-2 heures)
**Configuration Server:**
Suivre exactement **DEPLOYMENT.md** sections:
- [ ] Section 1: Installation des dépendances
- [ ] Section 2: Configuration de `.env`
- [ ] Section 3: Initialisation de la base de données
- [ ] Section 4: Configuration de Gunicorn
- [ ] Section 5: Configuration de Nginx
- [ ] Section 6: Configuration SSL

```bash
# Exemple rapide:
cd /var/www/unss-goma
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurer .env avec vos valeurs
nano .env

# Initialiser la base de données
python3 app.py  # Une fois, puis Ctrl+C

# Créer service Gunicorn (voir DEPLOYMENT.md)
sudo nano /etc/systemd/system/unss-goma.service

# Lancer le service
sudo systemctl start unss-goma
sudo systemctl enable unss-goma

# Vérifier les logs
sudo journalctl -u unss-goma -f
```

### JOUR 3 - Vérification (1 heure)

#### 6️⃣ Tests
- [ ] Vérifier SECURITY_CHECKLIST.md - tous les items
- [ ] Tester login admin
- [ ] Tester upload fichier
- [ ] Tester envoi email (contact form)
- [ ] Vérifier les logs: `tail -f /var/log/nginx/unss-goma-error.log`
- [ ] Tester depuis un autre device (téléphone/autre ordi)
- [ ] Vérifier HTTPS fonctionne
- [ ] Vérifier redirects HTTP → HTTPS

#### 7️⃣ Go Live!
- [ ] Tous les tests passent ✅
- [ ] Admin par défaut changé
- [ ] Backups configurés
- [ ] Monitoring en place
- [ ] **METTRE EN LIGNE** 🚀

---

## 📋 CHECKLIST AVANT GO LIVE

### 🔐 SÉCURITÉ (OBLIGATOIRE)

```
AVANT d'aller en production, VOUS DEVEZ:

☐ Changer le mot de passe admin par défaut
  Contact: admin@sauveteurs.com
  Password: admin123 (CHANGEZ-LE!)

☐ Générer une SECRET_KEY unique et forte
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  Ajouter dans .env

☐ Configurer le MAIL SMTP
  ☐ MAIL_SERVER (ex: smtp.gmail.com)
  ☐ MAIL_PORT (ex: 587)
  ☐ MAIL_USERNAME (votre email)
  ☐ MAIL_PASSWORD (mot de passe app)
  ☐ TESTER: Envoyer un email depuis l'app

☐ Installer certificat SSL/TLS
  Commande: certbot certonly --nginx -d votredomaine.com

☐ Configurer HTTPS/redirect
  Nginx doit rediriger HTTP -> HTTPS

☐ NE PAS commiter .env dans Git
  Vérifier .gitignore: /.env

☐ Définir FLASK_ENV=production
  Pas de debug en production!

☐ Utiliser Gunicorn (pas Flask dev server)
  Configuration: gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### ⚙️ INFRASTRUCTURE (RECOMMANDÉ)

```
☐ Server Linux 20.04+ (Ubuntu/Debian)
☐ Python 3.8+
☐ Nginx comme reverse proxy
☐ Gunicorn pour app server
☐ SSL certificate valide
☐ Domaine configuré
☐ Firewall ports 80/443 ouverts
☐ Sauvegardes configurées (daily)
```

### 📊 MONITORING (IMPORTANT)

```
☐ Logs activés: /var/log/nginx/ et /var/log/unss-goma/
☐ Log rotation configurée
☐ Vérifier les logs régulièrement
☐ Alertes en place (optional)
☐ Monitoring disk/cpu/memory (optional)
```

---

## 🎯 Priorités

### 🔴 CRITIQUE (Faire immédiatement)
1. Changer admin password
2. Générer SECRET_KEY
3. Configurer MAIL
4. Installer SSL
5. Configurer Gunicorn
6. Configurer Nginx
7. Mettre FLASK_ENV=production

### 🟠 TRÈS IMPORTANT (Cette semaine)
8. Configurer sauvegardes
9. Monitorer les logs
10. Faire backups manuels
11. Tester la restauration

### 🟡 IMPORTANT (Ce mois-ci)
12. Ajouter monitoring/alertes
13. Audit de sécurité externe
14. Documentation mise à jour
15. Plan de maintenance

---

## 🚨 En Cas de Problème

### Email ne fonctionne pas
```bash
# Vérifier config
grep MAIL /var/www/unss-goma/.env

# Tester SMTP
python -m smtplib -s SMTP smtp.gmail.com 587

# Vérifier logs
tail -f /var/www/unss-goma/logs/app.log
```

### Nginx affiche 502
```bash
# Vérifier Gunicorn
sudo systemctl status unss-goma
sudo journalctl -u unss-goma -f

# Vérifier Nginx config
sudo nginx -t

# Redémarrer
sudo systemctl restart unss-goma
sudo systemctl restart nginx
```

### Base de données erreur
```bash
# Vérifier fichier existe
ls -la /var/www/unss-goma/sauveteurs_goma.db

# Vérifier permissions
sudo chown www-data:www-data /var/www/unss-goma/sauveteurs_goma.db
sudo chmod 644 /var/www/unss-goma/sauveteurs_goma.db

# Vérifier logs
tail -f /var/www/unss-goma/logs/app.log
```

---

## 📞 Qui Contacter Quoi

### Question Code
→ Vérifier app.py et database.py  
→ Lire les commentaires inline  
→ Consulter SECURITY_IMPROVEMENTS.md

### Question Déploiement
→ Lire DEPLOYMENT.md  
→ Exécuter les commandes étape par étape  
→ Vérifier les logs

### Question Sécurité
→ Lire SECURITY_CHECKLIST.md  
→ Vérifier chaque item  
→ Tester comme recommandé

### Question Configuration
→ Voir .env.example  
→ Lire config.py  
→ Consulter QUICK_START.md

---

## ✅ Signes que Tout Fonctionne

- ✅ App accessible sur https://votredomaine.com
- ✅ Login admin fonctionne
- ✅ File upload fonctionne
- ✅ Email contact fonctionne
- ✅ Pas d'erreur 502/500
- ✅ Logs apparaissent normalement
- ✅ Session timeout fonctionne
- ✅ Logout efface la session
- ✅ Redirect HTTP → HTTPS fonctionne
- ✅ Admin de démo changé

Si tout ✅, vous êtes en production! 🚀

---

## 📚 Documentation À Garder À Portée

Imprimer ou sauvegarder:
1. **DEPLOYMENT.md** - Troubleshooting
2. **SECURITY_CHECKLIST.md** - Vérifications
3. **QUICK_START.md** - Rappel rapide
4. **logs/app.log** - Pour débugging

---

## 🎉 APRÈS LA MISE EN LIGNE

Félicitations! Application en production! 🚀

**À faire ensuite:**
1. Monitorer les premiers jours
2. Vérifier les logs régulièrement
3. Faire des sauvegardes manuelles
4. Recueillir les feedbacks utilisateurs
5. Planifier les améliorations futures

---

## ⏱️ TIMELINE RÉSUMÉE

```
Day 1 (Morning): Lire docs + Tester local
Day 1 (Afternoon): Préparer .env + Email config
Day 2 (Morning): Server setup + Installation
Day 2 (Afternoon): Configuration + Gunicorn + Nginx
Day 3: Vérification + Go Live
```

**Total**: ~6-8 heures de travail

---

## 🎯 NEXT STEP

👉 **Lire DEPLOYMENT.md maintenant** (c'est l'étape finale)

---

**Bonne chance! Vous avez ceci! 💪**

*Questions? Consulter la documentation.*  
*Besoin d'aide? Lire les logs.*  
*Prêt? Suivre DEPLOYMENT.md.*

---

*Action Plan créé: Mai 2025*  
*UNSS Goma v2.1*  
*Production Ready ✅*
