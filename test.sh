#!/bin/bash
# Script rapide de test local
# Utilisation: bash test.sh

set -e

echo "🧪 UNSS Goma - Tests Locaux"
echo "=============================="

# 1. Vérifier Python
echo "✓ Vérifiant Python..."
python3 --version

# 2. Vérifier venv
if [ ! -d "venv" ]; then
    echo "✓ Créant venv..."
    python3 -m venv venv
fi

# 3. Activer venv
echo "✓ Activant venv..."
source venv/bin/activate

# 4. Installer dépendances
echo "✓ Installant dépendances..."
pip install -q -r requirements.txt

# 5. Vérifier .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env manquant. Créant depuis .env.example..."
    cp .env.example .env
    echo "📝 Veuillez éditer .env et relancer le test"
    exit 1
fi

# 6. Vérifier dossiers
echo "✓ Créant dossiers..."
mkdir -p logs uploads/articles uploads/membres

# 7. Tester imports
echo "✓ Testant imports Python..."
python3 -c "
import app
import database
import logging
print('✓ Tous les imports OK')
"

# 8. Vérifier base de données
echo "✓ Initialisant base de données..."
python3 -c "
import database
database.create_tables()
database.creer_admin_par_defaut()
print('✓ Base de données OK')
"

# 9. Vérifier fichiers critiques
echo "✓ Vérifiant fichiers..."
for file in app.py database.py requirements.txt .env templates/index.html; do
    if [ ! -f "$file" ]; then
        echo "❌ Fichier manquant: $file"
        exit 1
    fi
done

echo ""
echo "=============================="
echo "✅ TOUS LES TESTS PASSENT!"
echo "=============================="
echo ""
echo "🚀 Lancer l'application:"
echo "  python app.py"
echo ""
echo "📊 Admin de test:"
echo "  Email: admin@sauveteurs.com"
echo "  Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Changer le mot de passe avant production!"
echo ""
