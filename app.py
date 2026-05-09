from flask import Flask, render_template, request, redirect, url_for, session, send_file, abort
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
import sqlite3
import os
import database
from dotenv import load_dotenv
import logging
import re
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Validation des variables d'environnement obligatoires
required_env_vars = ['SECRET_KEY', 'MAIL_SERVER', 'MAIL_USERNAME', 'MAIL_PASSWORD']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars and os.getenv('FLASK_ENV') == 'production':
    logger.error(f"Variables d'environnement manquantes: {', '.join(missing_vars)}")
    raise ValueError(f"Variables d'environnement manquantes pour la production: {', '.join(missing_vars)}")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    logger.warning("SECRET_KEY non défini, utilisant une clé insécurisée")
    app.secret_key = 'dev-insecure-key-change-in-production'

# Configuration des uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_PDF_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB par fichier
MAX_FILENAME_LENGTH = 100

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['JSON_SORT_KEYS'] = False

# Configuration de sécurité
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Créer les dossiers s'ils n'existent pas
os.makedirs(os.path.join(UPLOAD_FOLDER, 'articles'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'membres'), exist_ok=True)
os.makedirs('logs', exist_ok=True)

def allowed_file(filename, allowed_extensions):
    """Valide les fichiers uploadés"""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions and len(filename) <= MAX_FILENAME_LENGTH

# Initialiser la base de données
try:
    database.create_tables()
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
    raise

# Créer admin par défaut SEULEMENT en développement
if os.getenv('FLASK_ENV') != 'production':
    database.creer_admin_par_defaut()
    logger.info("Admin par défaut créé (développement uniquement)")
else:
    logger.info("Environnement production - admin par défaut NON créé")

# Configuration Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@sauveteursgoma.org')
app.config['CONTACT_EMAIL'] = os.getenv('CONTACT_EMAIL', 'contact@sauveteursgoma.org')

mail = Mail(app)

# Middleware de sécurité
@app.before_request
def security_headers():
    """Ajoute les headers de sécurité"""
    pass  # Headers seront ajoutés dans after_request

@app.after_request
def add_security_headers(response):
    """Ajoute les headers de sécurité à toutes les réponses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' if os.getenv('FLASK_ENV') == 'production' else ''
    return response

# Décorateur d’authentification admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        if not database.est_administrateur(session['admin_id']):
            return render_template('message.html', message="Accès administrateur requis.")
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    articles = database.lister_articles()
    return render_template('index.html', articles=articles)

@app.route('/membres')
def liste_membres():
    membres = database.lister_membres()
    return render_template('membres.html', membres=membres)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        try:
            identifiant = request.form.get('identifiant', '').strip()
            password = request.form.get('password', '')
            
            # Validation basique
            if not identifiant or not password:
                logger.warning(f"Tentative de connexion avec données manquantes depuis {request.remote_addr}")
                return render_template('admin_login.html', error="Identifiants requis.")
            
            # Validation du format email
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', identifiant):
                logger.warning(f"Tentative de connexion avec format invalide: {identifiant[:10]}... depuis {request.remote_addr}")
                return render_template('admin_login.html', error="Format email invalide.")
            
            admin = database.get_admin_par_contact(identifiant)
            
            if admin and check_password_hash(admin['mot_de_passe'], password):
                session.permanent = True
                session['admin_id'] = admin['id']
                logger.info(f"Connexion admin réussie: {identifiant}")
                return redirect(url_for('admin_dashboard'))
            else:
                logger.warning(f"Échec de connexion pour: {identifiant[:10]}... depuis {request.remote_addr}")
                return render_template('admin_login.html', error="Identifiants incorrects.")
        except Exception as e:
            logger.error(f"Erreur lors de la connexion admin: {e}")
            return render_template('message.html', message="Erreur de serveur.", error=True)
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    membres = database.lister_membres()
    articles = database.lister_articles()
    return render_template('admin_dashboard.html', membres=membres, articles=articles)

@app.route('/admin/ajouter_membre', methods=['POST'])
@admin_required
def ajouter_nouveau_membre_admin():
    try:
        nom = request.form.get('nom', '').strip()
        role = request.form.get('role', '').strip()
        contact = request.form.get('contact', '').strip()
        password = request.form.get('password', '')
        is_admin = 1 if request.form.get('is_admin') == 'on' else 0
        
        # Validation
        if not nom or not contact or not password:
            return render_template('message.html', message="Données manquantes.", error=True)
        
        if len(nom) > 100 or len(role) > 50:
            return render_template('message.html', message="Données trop volumineuses.", error=True)
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact):
            return render_template('message.html', message="Email invalide.", error=True)
        
        if len(password) < 8:
            return render_template('message.html', message="Mot de passe trop faible (min 8 caractères).", error=True)
        
        photo_profil = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename:
                if not allowed_file(photo.filename, ALLOWED_IMAGE_EXTENSIONS):
                    return render_template('message.html', message="Format d'image non autorisé.", error=True)
                ext = photo.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"member_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(photo.filename) % 10000}.{ext}")
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], 'membres', filename))
                photo_profil = f"uploads/membres/{filename}"
        
        if database.ajouter_membre(nom, role, contact, password, photo_profil, is_admin):
            logger.info(f"Membre ajouté: {contact} (admin={is_admin})")
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('message.html', message="Erreur lors de l'ajout (contact déjà existant?).", error=True)
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout de membre: {e}")
        return render_template('message.html', message="Erreur de serveur.", error=True)

@app.route('/admin/supprimer_membre/<int:membre_id>')
@admin_required
def supprimer_membre_admin(membre_id):
    try:
        # Sécurité: vérifier qu'on ne supprime pas le dernier admin
        if database.retrancher_membre(membre_id):
            logger.info(f"Membre supprimé: {membre_id} par admin {session.get('admin_id')}")
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('message.html', message=f"Membre non trouvé.", error=True)
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du membre {membre_id}: {e}")
        return render_template('message.html', message="Erreur lors de la suppression.", error=True)

@app.route('/ajouter_article', methods=['POST'])
@admin_required
def ajouter_nouvel_article():
    try:
        titre = request.form.get('titre', '').strip()
        contenu = request.form.get('contenu', '').strip()
        
        # Validation des champs obligatoires
        if not titre or not contenu:
            logger.warning(f"Article ajouté avec données incomplètes par admin {session.get('admin_id')}")
            return render_template('message.html', message="Titre et contenu requis.", error=True)
        
        if len(titre) > 200 or len(contenu) > 5000:
            return render_template('message.html', message="Titre ou contenu trop long.", error=True)
        
        image_path = None
        pdf_path = None
        
        # Gérer l'upload d'image
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename:
                if not allowed_file(image.filename, ALLOWED_IMAGE_EXTENSIONS):
                    return render_template('message.html', message="Format d'image non autorisé (PNG, JPG, JPEG, GIF).", error=True)
                
                # Vérifier la taille du fichier
                image.seek(0, 2)  # Aller à la fin
                if image.tell() > MAX_FILE_SIZE:
                    return render_template('message.html', message="Image trop volumineuse (max 5 MB).", error=True)
                image.seek(0)  # Revenir au début
                
                # Générer un nom de fichier sécurisé
                ext = image.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(image.filename) % 10000}.{ext}")
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'articles', filename))
                image_path = f"uploads/articles/{filename}"
                logger.info(f"Image uploadée: {filename}")
        
        # Gérer l'upload de PDF
        if 'pdf' in request.files:
            pdf = request.files['pdf']
            if pdf and pdf.filename:
                if not allowed_file(pdf.filename, ALLOWED_PDF_EXTENSIONS):
                    return render_template('message.html', message="Seuls les fichiers PDF sont autorisés.", error=True)
                
                # Vérifier la taille du fichier
                pdf.seek(0, 2)
                if pdf.tell() > MAX_FILE_SIZE:
                    return render_template('message.html', message="PDF trop volumineux (max 5 MB).", error=True)
                pdf.seek(0)
                
                filename = secure_filename(f"pdf_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(pdf.filename) % 10000}.pdf")
                pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], 'articles', filename))
                pdf_path = f"uploads/articles/{filename}"
                logger.info(f"PDF uploadé: {filename}")
        
        admin_id = session.get('admin_id')
        database.ajouter_article(titre, contenu, image_path, pdf_path, admin_id)
        logger.info(f"Article ajouté par admin {admin_id}: {titre[:50]}")
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout d'article: {e}")
        return render_template('message.html', message="Erreur lors de l'ajout de l'article.", error=True)

@app.route('/supprimer_article/<int:article_id>')
@admin_required
def supprimer_article(article_id):
    try:
        if database.retrancher_article(article_id):
            logger.info(f"Article supprimé: {article_id} par admin {session.get('admin_id')}")
            return redirect(url_for('index'))
        else:
            return render_template('message.html', message="Article non trouvé.", error=True)
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'article {article_id}: {e}")
        return render_template('message.html', message="Erreur lors de la suppression.", error=True)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            nom = request.form.get('nom', '').strip()
            email = request.form.get('email', '').strip()
            message_contenu = request.form.get('message', '').strip()

            # Validation
            if not nom or not email or not message_contenu:
                return render_template('contact.html', error="Tous les champs sont requis.")
            
            # Validation du format email
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                return render_template('contact.html', error="Adresse email invalide.")
            
            # Limite de longueur
            if len(nom) > 100 or len(message_contenu) > 5000:
                return render_template('contact.html', error="Données trop volumineuses.")
            
            # Sanitize
            nom = re.sub(r'[<>"\']', '', nom)
            
            msg = Message(
                f"Nouveau message de contact de {nom}",
                recipients=[app.config['CONTACT_EMAIL']],
                reply_to=email
            )
            msg.body = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message_contenu}"

            mail.send(msg)
            logger.info(f"Message de contact reçu de {email}")
            return render_template('message.html', message="Votre message a été envoyé avec succès !")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message de contact: {e}")
            return render_template('message.html', message="Erreur lors de l'envoi. Veuillez réessayer.", error=True)
    return render_template('contact.html')

@app.route('/logout')
def logout():
    admin_id = session.get('admin_id')
    session.clear()
    logger.info(f"Déconnexion admin {admin_id}")
    return redirect(url_for('index'))

@app.route('/download/<path:filepath>')
def download_file(filepath):
    """Permet de télécharger les fichiers uploadés (sécurisé)"""
    try:
        # Sécurité: vérifier que le chemin est bien dans le dossier uploads
        requested_path = os.path.normpath(os.path.join(os.getcwd(), filepath))
        upload_path = os.path.normpath(os.path.join(os.getcwd(), UPLOAD_FOLDER))
        
        if not requested_path.startswith(upload_path):
            logger.warning(f"Tentative d'accès non autorisé: {filepath} depuis {request.remote_addr}")
            abort(403)
        
        if not os.path.exists(requested_path):
            logger.warning(f"Fichier non trouvé: {filepath}")
            abort(404)
        
        # Vérifier l'extension
        ext = filepath.rsplit('.', 1)[1].lower() if '.' in filepath else ''
        if ext not in ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_PDF_EXTENSIONS):
            logger.warning(f"Extension non autorisée: {ext} pour {filepath}")
            abort(403)
        
        logger.info(f"Fichier téléchargé: {filepath}")
        return send_file(requested_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement de {filepath}: {e}")
        abort(500)

# Gestionnaires d'erreur
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Error: {request.path}")
    return render_template('message.html', message="Page non trouvée.", error=True), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"500 Error: {error}")
    return render_template('message.html', message="Erreur serveur interne.", error=True), 500

@app.errorhandler(403)
def forbidden(error):
    logger.warning(f"403 Forbidden: {request.path} depuis {request.remote_addr}")
    return render_template('message.html', message="Accès refusé.", error=True), 403

if __name__ == '__main__':
    # En production, ne pas utiliser le serveur Flask de développement!
    # Utiliser: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    if debug_mode:
        try:
            import webbrowser
            webbrowser.open('http://127.0.0.1:5000')
        except ImportError:
            logger.info("webbrowser module not available")
    
    app.run(
        debug=debug_mode,
        host='127.0.0.1' if debug_mode else '0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )