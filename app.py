from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import sqlite3
import os
import database
from dotenv import load_dotenv
import webbrowser

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'fallback_secret_key'

# Configuration des uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialiser la base de données
database.create_tables()
database.creer_admin_par_defaut()

# Configuration Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

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
        # APRÈS
        identifiant = request.form['identifiant'].strip()

        password = request.form['password']

        conn = sqlite3.connect(database.DATABASE_NAME)
        cursor = conn.cursor()
        # ✅ Correction ici : mot_de_passe au lieu de password
        cursor.execute("SELECT id, mot_de_passe FROM membres WHERE contact=? AND is_admin=1", (identifiant,))

        admin = cursor.fetchone()
        conn.close()

        if admin and check_password_hash(admin[1], password):
            session['admin_id'] = admin[0]
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('message.html', message="Identifiants administrateur incorrects.")
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
    nom = request.form['nom'].strip()
    role = request.form['role'].strip()
    contact = request.form['contact'].strip()
    photo_profil = request.form.get('photo_profil', None)
    is_admin = 1 if 'is_admin' in request.form else 0
    password = request.form['password']

    # ✅ Correction ici : on passe le mot de passe brut, la fonction s’occupe du hash
    if database.ajouter_membre(nom, role, contact, password, photo_profil, is_admin):
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('message.html', message="Erreur lors de l'ajout du membre.")

@app.route('/admin/supprimer_membre/<int:membre_id>')
@admin_required
def supprimer_membre_admin(membre_id):
    if database.retrancher_membre(membre_id):
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('message.html', message=f"Membre avec l'ID {membre_id} non trouvé.")

@app.route('/ajouter_article', methods=['POST'])
@admin_required
def ajouter_nouvel_article():
    titre = request.form['titre'].strip()
    contenu = request.form['contenu'].strip()
    image_path = None
    pdf_path = None
    
    # Gérer l'upload d'image
    if 'image' in request.files:
        image = request.files['image']
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(f"img_{datetime.now().timestamp()}_{image.filename}")
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'articles', filename))
            image_path = f"uploads/articles/{filename}"
    
    # Gérer l'upload de PDF
    if 'pdf' in request.files:
        pdf = request.files['pdf']
        if pdf and pdf.filename and pdf.filename.rsplit('.', 1)[1].lower() == 'pdf':
            filename = secure_filename(f"pdf_{datetime.now().timestamp()}_{pdf.filename}")
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], 'articles', filename))
            pdf_path = f"uploads/articles/{filename}"
    
    admin_id = session.get('admin_id')
    database.ajouter_article(titre, contenu, image_path, pdf_path, admin_id)
    return redirect(url_for('index'))

@app.route('/supprimer_article/<int:article_id>')
@admin_required
def supprimer_article(article_id):
    if database.retrancher_article(article_id):
        return redirect(url_for('index'))
    else:
        return render_template('message.html', message=f"Article avec l'ID {article_id} non trouvé.")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        message_contenu = request.form.get('message', '').strip()

        if nom and email and message_contenu:
            msg = Message("Nouveau message de contact", recipients=['contact@sauveteursgoma.org'])
            msg.body = f"Nom: {nom}\nEmail: {email}\nMessage: {message_contenu}"

            try:
                mail.send(msg)
                return render_template('message.html', message="Votre message a été envoyé !")
            except Exception as e:
                return render_template('message.html', message=f"Erreur lors de l'envoi du message: {e}")
        else:
            return render_template('message.html', message="Tous les champs sont requis.")
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('index'))

@app.route('/download/<path:filepath>')
def download_file(filepath):
    """Permet de télécharger les fichiers uploadés"""
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return render_template('message.html', message=f"Erreur lors du téléchargement: {e}")

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)