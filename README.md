# 🚨 UNSS Goma - Application de Gestion des Sauveteurs

Une application Flask moderne pour gérer les membres, articles et communications des équipes de sauvetage à Goma.

## ✨ Améliorations Récentes

### 1. 📄 Gestion Avancée des Articles
- ✅ Support pour **les images** (PNG, JPG, JPEG, GIF)
- ✅ Support pour les **fichiers PDF** téléchargeables
- ✅ Galerie d'articles avec images
- ✅ Liens de téléchargement pour les PDF
- ✅ Métadonnées des articles (date, auteur)

### 2. 🎨 Design Modernisé
- ✅ Interface utilisateur élégante et responsive
- ✅ Dégradés de couleurs attrayants
- ✅ Animations fluides et transitions
- ✅ Icônes emoji pour meilleure lisibilité
- ✅ Cartes de membres stylisées
- ✅ Formulaires améliorés avec meilleure accessibilité

### 3. 👥 Gestion Améliorée des Membres
- ✅ Affichage en grille responsive
- ✅ Cartes de profil avec photos
- ✅ Badge administrateur
- ✅ Interface admin réorganisée

### 4. 🔐 Tableau de Bord Administrateur Complet
- ✅ Gestion centralisée des membres et articles
- ✅ Upload de fichiers multimédias
- ✅ Interface intuitive et claire
- ✅ Confirmation de suppression

## 🚀 Démarrage Rapide

### Prérequis
```bash
pip install flask flask-mail werkzeug python-dotenv
```

### Installation
```bash
1. Clonez/téléchargez le projet
2. Naviguez dans le dossier du projet
3. Créez un fichier .env avec les configurations
4. Installez les dépendances: pip install -r requirements.txt
5. Lancez l'application: python app.py
```

### Créer requirements.txt
```bash
pip install flask flask-mail werkzeug python-dotenv
pip freeze > requirements.txt
```

## 📁 Structure du Projet

```
unss/
├── app.py                    # Application principale
├── database.py              # Gestion de la base de données
├── .env                     # Variables d'environnement
├── .gitignore              # Fichiers à ignorer
├── static/
│   ├── style.css           # Styles CSS modernes
│   ├── script.js           # Scripts JavaScript
│   └── images/
├── templates/
│   ├── index.html          # Page d'accueil
│   ├── admin_login.html    # Connexion admin
│   ├── admin_dashboard.html # Tableau de bord
│   ├── membres.html        # Page des membres
│   ├── contact.html        # Formulaire contact
│   └── message.html        # Messages
├── uploads/
│   ├── articles/           # Images et PDF des articles
│   └── membres/            # Photos de profil
└── sauveteurs_goma.db      # Base de données SQLite
```

## 🔧 Configuration

### Variables d'environnement (.env)
```
SECRET_KEY=votre_clé_secrète_ici
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre_email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_app
MAIL_DEFAULT_SENDER=contact@sauveteursgoma.org
```

## 📚 Fonctionnalités

### Pour les Visiteurs
- 📖 Consulter les articles et actualités
- 📷 Voir les articles avec images
- 📥 Télécharger les fichiers PDF associés
- 👥 Consulter la liste des membres
- 📧 Envoyer des messages via le formulaire de contact
- 🚨 Accéder aux informations d'urgence

### Pour les Administrateurs
- 🔐 Connexion sécurisée
- ➕ Ajouter/Supprimer des articles
- 📷 Uploader des images pour les articles
- 📄 Uploader des fichiers PDF
- 👥 Gérer les membres de l'équipe
- 🏅 Assigner les rôles d'administrateur

## 📤 Uploading Files

### Limites
- Taille maximale : **5 MB par fichier**
- Formats acceptés :
  - **Images** : PNG, JPG, JPEG, GIF
  - **Documents** : PDF

### Dossiers de stockage
- Articles : `uploads/articles/`
- Membres : `uploads/membres/`

## 🎯 Comptes de Démonstration

### Admin par défaut
- **Email** : `admin@sauveteurs.com`
- **Mot de passe** : `admin123`

⚠️ **Note** : Changez ce mot de passe en production !

## 🌐 Responsive Design

L'application est entièrement responsive et fonctionne sur :
- 📱 Téléphones mobiles
- 📱 Tablettes
- 🖥️ Ordinateurs de bureau

## 🛡️ Sécurité

- ✅ Hachage des mots de passe avec Werkzeug
- ✅ Sessions sécurisées
- ✅ Validation des fichiers uploadés
- ✅ Protection contre les injections SQL (SQLite3)
- ✅ Vérification des droits administrateur

## 📝 Notes Importantes

1. **Base de données** : SQLite (incluse)
2. **Authentification** : Session-based
3. **Mail** : Nécessite une configuration Gmail/SMTP valide
4. **Fichiers** : Les uploads sont stockés localement

## 🤝 Support

Pour toute question ou problème, contactez : contact@sauveteursgoma.org

---

**Version** : 2.0 (2025)
**Dernière mise à jour** : Mai 2025
