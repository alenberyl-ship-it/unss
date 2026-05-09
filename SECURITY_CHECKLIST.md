# 🔒 LISTE DE SÉCURITÉ - UNSS Goma

## ✅ Vérifications Avant Déploiement

### 1. **Authentification & Sessions**
- [ ] Secret key unique et fort (32+ caractères)
- [ ] Sessions configurées HTTPOnly
- [ ] Sessions configurées Secure (HTTPS)
- [ ] Timeout de session défini (24h)
- [ ] Admin par défaut changé (admin@sauveteurs.com/admin123)
- [ ] Pas de hardcoding de credentials

### 2. **Validation des Entrées**
- [ ] Validation des emails (regex pattern)
- [ ] Validation des longueurs de string
- [ ] Validation des extensions de fichiers
- [ ] Validation des tailles de fichiers (5 MB max)
- [ ] Sanitization des noms de fichiers
- [ ] Pas d'injection SQL (parameterized queries)

### 3. **Gestion des Fichiers**
- [ ] Vérification de path traversal (..)
- [ ] Fichiers uploadés en dehors de webroot
- [ ] ALLOWED_EXTENSIONS défini strictement
- [ ] Vérification du type MIME (si possible)
- [ ] Limite de taille par fichier
- [ ] Suppression sécurisée des fichiers

### 4. **HTTP & Headers**
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: SAMEORIGIN
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Strict-Transport-Security (HSTS)
- [ ] Content-Security-Policy (CSP) - optionnel

### 5. **HTTPS/SSL**
- [ ] Certificate valide (Let's Encrypt)
- [ ] Redirection HTTP -> HTTPS
- [ ] TLS 1.2+ activé
- [ ] Ciphers forts configurés
- [ ] HSTS preload envisagé

### 6. **Base de Données**
- [ ] Prepared statements utilisés partout
- [ ] Pas de concaténation de SQL
- [ ] Mots de passe hachés (bcrypt/Werkzeug)
- [ ] Backups automatiques configurés
- [ ] Permissions de fichiers correct (0644)
- [ ] Base NOT accessible via web

### 7. **Email/SMTP**
- [ ] Identifiants stockés en variables d'env
- [ ] Validation des adresses email
- [ ] Pas de dévoilement de stack trace
- [ ] Reply-To header défini
- [ ] Rate limiting sur formulaire contact

### 8. **Logging & Monitoring**
- [ ] Logs des tentatives de connexion échouées
- [ ] Logs des accès non autorisés
- [ ] Logs des erreurs serveur
- [ ] Fichiers logs protégés (0600)
- [ ] Logs non accessible via web
- [ ] Rotation des logs configurée

### 9. **Erreurs & Exceptions**
- [ ] Debug = False en production
- [ ] Pas de stack traces exposes aux users
- [ ] Messages d'erreur génériques
- [ ] Logging détaillé côté serveur
- [ ] 404/500 pages custom

### 10. **Serveur Web**
- [ ] Gunicorn utilisé (pas Flask dev server)
- [ ] Nginx comme reverse proxy
- [ ] Compression désactivée ou controllée
- [ ] Timeouts configurés
- [ ] Workers bien dimensionnés

### 11. **Permissions & Accès**
- [ ] Uploads dossier non exécutable
- [ ] Fichiers config (0600)
- [ ] Dossier app appartient à www-data
- [ ] Pas de permissions 777
- [ ] Admin_required decorator utilisé partout

### 12. **Environnement**
- [ ] FLASK_ENV = production
- [ ] .env NOT committed dans Git
- [ ] Tous les secrets en variables d'env
- [ ] Variables d'env validées au démarrage
- [ ] Database path ne révèle pas d'infos

---

## 🔴 Vulnérabilités Communes (À Éviter)

### SQL Injection
```python
# ❌ MAUVAIS
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# ✅ BON
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

### Path Traversal
```python
# ❌ MAUVAIS
return send_file(user_input_filepath)

# ✅ BON
safe_path = os.path.normpath(os.path.join(upload_dir, user_input))
if not safe_path.startswith(os.path.normpath(upload_dir)):
    abort(403)
```

### XSS (Cross-Site Scripting)
```html
<!-- ❌ MAUVAIS -->
<div>{{ user_input }}</div>

<!-- ✅ BON -->
<div>{{ user_input | escape }}</div>
```

### CSRF
```python
# ✅ Ajouter flask-wtf
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Dans les forms
{{ csrf_token() }}
```

---

## 🧪 Tests de Sécurité

### Test manuels
```bash
# Tester login échoué
curl -X POST http://localhost:5000/admin/login \
  -d "identifiant=admin@test.com&password=wrong"

# Tester path traversal
curl "http://localhost:5000/download/../../etc/passwd"

# Tester injection SQL
curl -X POST http://localhost:5000/admin/login \
  -d "identifiant=admin' OR '1'='1&password=x"
```

### Outils recommandés
- **OWASP ZAP**: Scanning de vulnérabilités
- **Bandit**: Analyse de code Python
- **sqlmap**: Teste les injections SQL
- **nmap**: Scan des ports ouverts

```bash
# Scan OWASP ZAP
zaproxy -cmd -quickurl http://localhost:5000

# Analyse Bandit
bandit -r .

# Vérifier les ports
nmap -p- localhost
```

---

## 📊 Configuration de Sécurité Nginx

```nginx
# Nginx - Ajouter ces headers:
add_header Strict-Transport-Security "max-age=31536000" always;
add_header X-Content-Type-Options nosniff always;
add_header X-Frame-Options SAMEORIGIN always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Rate limiting
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
location /admin/login {
    limit_req zone=login burst=10 nodelay;
    proxy_pass http://unss_app;
}
```

---

## 📅 Vérifications Régulières

- **Hebdomadaire**: Vérifier les logs pour activités suspectes
- **Mensuel**: Mettre à jour les dépendances Python
- **Trimestriel**: Audit de sécurité complet
- **Annuel**: Audit de sécurité externe

---

## 🚨 En Cas de Faille de Sécurité

1. **Isoler** le serveur
2. **Sauvegarder** les logs
3. **Analyser** l'intrusion
4. **Patcher** la vulnérabilité
5. **Restaurer** à partir d'une sauvegarde
6. **Notifier** les utilisateurs
7. **Débriefing** post-incident

---

## 📚 Ressources Utiles

- OWASP Top 10: https://owasp.org/Top10/
- Flask Security: https://flask.palletsprojects.com/security/
- NIST Guidelines: https://csrc.nist.gov/
- Have I Been Pwned: https://haveibeenpwned.com/

---

**Dernière révision**: Mai 2025  
**Version**: 2.0
