from flask_mail import Mail, Message
from app import app
from flask import request,render_template
app.config['MAIL_SERVER'] = 'smtp.votre_fournisseur.com'
app.config['MAIL_PORT'] = 587 # ou le port spécifié par votre fournisseur
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'votre_adresse_email@sauveteursgoma.org'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe_email'
app.config['MAIL_DEFAULT_SENDER'] = 'votre_adresse_email@sauveteursgoma.org'

mail = Mail(app)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom')  # Utiliser .get() pour éviter KeyError
        email = request.form.get('email')
        message_contenu = request.form.get('message')

        if not nom or not email or not message_contenu:
            return "Tous les champs doivent être remplis", 400

        # Logique pour envoyer le message ici
        return render_template('message.html', message="Votre message a été envoyé !")

    return render_template('contact.html')  # Affichage du formulaire en GET
