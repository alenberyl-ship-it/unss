@echo off
REM Script rapide de test local pour Windows
REM Utilisation: test.bat

setlocal enabledelayedexpansion

echo.
echo 🧪 UNSS Goma - Tests Locaux
echo ==============================

REM 1. Vérifier Python
echo ✓ Vérifiant Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trouvé. Installer Python d'abord.
    exit /b 1
)

REM 2. Vérifier venv
if not exist "venv" (
    echo ✓ Créant venv...
    python -m venv venv
)

REM 3. Activer venv
echo ✓ Activant venv...
call venv\Scripts\activate.bat

REM 4. Installer dépendances
echo ✓ Installant dépendances...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation
    exit /b 1
)

REM 5. Vérifier .env
if not exist ".env" (
    echo ⚠️  .env manquant. Créant depuis .env.example...
    copy .env.example .env
    echo 📝 Veuillez éditer .env et relancer le test
    exit /b 1
)

REM 6. Vérifier dossiers
echo ✓ Créant dossiers...
if not exist "logs" mkdir logs
if not exist "uploads\articles" mkdir uploads\articles
if not exist "uploads\membres" mkdir uploads\membres

REM 7. Tester imports
echo ✓ Testant imports Python...
python -c "import app, database, logging; print('✓ Tous les imports OK')" || exit /b 1

REM 8. Vérifier base de données
echo ✓ Initialisant base de données...
python -c "import database; database.create_tables(); database.creer_admin_par_defaut(); print('✓ Base de données OK')" || exit /b 1

REM 9. Vérifier fichiers critiques
echo ✓ Vérifiant fichiers...
for %%F in (app.py database.py requirements.txt .env templates\index.html) do (
    if not exist "%%F" (
        echo ❌ Fichier manquant: %%F
        exit /b 1
    )
)

echo.
echo ==============================
echo ✅ TOUS LES TESTS PASSENT!
echo ==============================
echo.
echo 🚀 Lancer l'application:
echo    python app.py
echo.
echo 📊 Admin de test:
echo    Email: admin@sauveteurs.com
echo    Password: admin123
echo.
echo ⚠️  IMPORTANT: Changer le mot de passe avant production!
echo.

endlocal
