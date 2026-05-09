document.addEventListener('DOMContentLoaded', function () {
    // Informations de l'équipe
    const equipeInfoElement = document.getElementById('equipe-info');
    if (equipeInfoElement) {
        equipeInfoElement.textContent = "Nous sommes une équipe dévouée de sauveteurs basés à Goma, engagés à servir notre communauté en cas d'urgence et à promouvoir la sécurité.";
    }

    // Liste des services
    const servicesListeElement = document.getElementById('services-liste');
    if (servicesListeElement) {
        const services = [
            "Interventions en cas de catastrophe naturelle",
            "Secours d'urgence et premiers soins",
            "Recherche et sauvetage de personnes disparues",
            "Assistance aux populations sinistrées",
            "Formations aux premiers secours et à la prévention"
        ];
        services.forEach(service => {
            const li = document.createElement('li');
            li.textContent = service;
            servicesListeElement.appendChild(li);
        });
    }

    // Numéro d'urgence
    const numeroUrgenceElement = document.getElementById('numero-urgence');
    if (numeroUrgenceElement) {
        numeroUrgenceElement.textContent = "Numéro d'urgence : +243 XX XXX XX XX";
    }

    // Détails de l'urgence
    const urgenceDetailsBtn = document.getElementById('urgence-details-btn');
    const urgenceDetails = document.getElementById('urgence-details');
    if (urgenceDetailsBtn && urgenceDetails) {
        urgenceDetails.innerHTML = `
            <p>En cas d'urgence, contactez-nous immédiatement au numéro ci-dessus. Nos équipes sont prêtes à intervenir 24h/24 et 7j/7.</p>
            <p>Précisez clairement la nature de l'urgence, le lieu exact et le nombre de personnes concernées.</p>
        `;
        urgenceDetailsBtn.addEventListener('click', function () {
            if (urgenceDetails.classList.contains('details-cache')) {
                urgenceDetails.classList.remove('details-cache');
                urgenceDetails.classList.add('details-visible');
                urgenceDetailsBtn.textContent = "[-]";
            } else {
                urgenceDetails.classList.add('details-cache');
                urgenceDetails.classList.remove('details-visible');
                urgenceDetailsBtn.textContent = "[+]";
            }
        });
    }

    // Informations de contact
    const contactInfoElement = document.getElementById('contact-info');
    const contactForm = document.querySelector('#contact form');
    const afficherFormulaireBtn = document.getElementById('afficher-formulaire');
    if (contactInfoElement) {
        contactInfoElement.textContent = "Pour toute question ou demande d'information, veuillez nous contacter par email à contact@sauveteursgoma.org ou par téléphone au +243 XX XXX XX XX.";
    }
    afficherFormulaireBtn.addEventListener('click', function () {
    if (contactForm.classList.contains('details-cache')) {
        contactForm.classList.remove('details-cache');
        contactForm.classList.add('details-visible');
        afficherFormulaireBtn.textContent = 'Masquer le formulaire de contact';
    } else {
        contactForm.classList.add('details-cache');
        contactForm.classList.remove('details-visible');
        afficherFormulaireBtn.textContent = 'Afficher le formulaire de contact';
    }
});

    // Conseils de prévention
    const conseilsListeElement = document.getElementById('conseils-liste');
    if (conseilsListeElement) {
        const conseils = [
            "Restez informé des alertes météorologiques locales.",
            "Préparez un kit d'urgence avec de l'eau, de la nourriture, une trousse de premiers secours et une radio.",
            "Identifiez les itinéraires d'évacuation et les points de rassemblement sûrs.",
            "Enseignez aux membres de votre famille les gestes de premiers secours.",
            "Signalez toute situation dangereuse aux autorités compétentes."
        ];
        conseils.forEach(conseil => {
            const li = document.createElement('li');
            li.textContent = conseil;
            conseilsListeElement.appendChild(li);
        });
    }

    // Informations de soutien
    const soutienInfoElement = document.getElementById('soutien-info');
    if (soutienInfoElement) {
        soutienInfoElement.textContent = "Votre soutien est essentiel pour nous permettre de continuer notre mission. Vous pouvez faire un don via [méthodes de don]. Merci de votre générosité.";
    }
});
