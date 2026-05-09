# 🚀 Guide de Démarrage - UNSS Goma

## Installation Rapide (5 minutes)

### Étape 1 : Cloner/Télécharger le projet
```bash
# Naviguez dans le dossier du projet
cd unss
```

### Étape 2 : Créer un environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 4 : Configurer les variables d'environnement
```bash
# Copier le fichier d'exemple
copy .env.example .env

# Éditer le fichier .env avec vos paramètres
# Important: Remplacez les valeurs par défaut !
```

### Étape 5 : Lancer l'application
```bash
python app.py
```

L'application s'ouvrira automatiquement à : **http://127.0.0.1:5000**

---

## 🔐 Première Connexion Admin

### Compte par défaut :
- **Email** : `admin@sauveteurs.com`
- **Mot de passe** : `admin123`

⚠️ **IMPORTANT** : Changez ce mot de passe immédiatement après la première connexion !

---

## 📝 Configuration du Mail

### Pour Gmail :
1. Activez l'authentification 2FA sur votre compte Gmail
2. Générez un mot de passe d'application : https://myaccount.google.com/apppasswords
3. Copiez le mot de passe généré dans la variable `MAIL_PASSWORD` du fichier `.env`

### Configuration .env :
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_application
```

---

## 📂 Structure des Dossiers

Après le démarrage, les dossiers suivants seront créés :

```
uploads/
├── articles/     # Images et PDF des articles
└── membres/      # Photos de profil des membres
```

---

## ✨ Nouvelles Fonctionnalités

### 📄 Articles avec Pièces Jointes
- Ajoutez une **image** (PNG, JPG, JPEG, GIF)
- Joignez un **fichier PDF** téléchargeable
- Maximum 5 MB par fichier

### 👥 Gestion des Membres
- Cartes de profil stylisées
- Photos de profil
- Rôles et contact
- Badge administrateur

### 🎨 Interface Moderne
- Design responsive
- Animations fluides
- Icônes emoji
- Thème moderne bleu/vert

---

## 🛠️ Dépannage

### Problème : "Module not found"
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème : "Port 5000 déjà utilisé"
```bash
# Éditer app.py et changer le port :
app.run(debug=True, port=5001)
```

### Problème : "Erreur de base de données"
```bash
# Supprimer la base de données et la réinitialiser
rm sauveteurs_goma.db
python app.py
```

---

## 📊 Fonctionnalités Admin

### Dashboard
- 👥 Gérer les membres
- 📄 Gérer les articles
- 📤 Uploader des fichiers
- 🔐 Contrôler les accès

### Uploads Supportés
| Type | Formats | Taille Max |
|------|---------|-----------|
| Images | PNG, JPG, JPEG, GIF | 5 MB |
| Documents | PDF | 5 MB |

---

## 🔒 Sécurité

✅ Mots de passe hachés avec Werkzeug  
✅ Sessions sécurisées  
✅ Validation des fichiers  
✅ Protection contre les injections SQL  
✅ Vérification des droits admin  

---

## 📞 Support

Pour toute question : contact@sauveteursgoma.org

---

**Version** : 2.0  
**Dernière mise à jour** : Mai 2025
