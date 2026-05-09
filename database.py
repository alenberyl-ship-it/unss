import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)
DATABASE_NAME = os.getenv('DATABASE_NAME', 'sauveteurs_goma.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    if conn:
        conn.close()

def create_tables():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS membres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                role TEXT,
                contact TEXT NOT NULL UNIQUE,
                mot_de_passe TEXT NOT NULL,
                photo_profil TEXT,
                is_admin INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                contenu TEXT NOT NULL,
                date_publication TEXT NOT NULL,
                image_path TEXT,
                pdf_path TEXT,
                auteur_id INTEGER
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")
    finally:
        close_db_connection(conn)

def lister_articles():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles ORDER BY date_publication DESC")
        articles = cursor.fetchall()
        return articles
    except Exception as e:
        print(f"Erreur lors de la récupération des articles : {e}")
        return []
    finally:
        close_db_connection(conn)

def lister_membres():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM membres ORDER BY nom ASC")
        membres = cursor.fetchall()
        return membres
    except Exception as e:
        print(f"Erreur lors de la récupération des membres : {e}")
        return []
    finally:
        close_db_connection(conn)

def ajouter_membre(nom, role, contact, mot_de_passe, photo_profil, is_admin):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO membres (nom, role, contact, mot_de_passe, photo_profil, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, role, contact, generate_password_hash(mot_de_passe), photo_profil, is_admin))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout d'un membre : {e}")
        return False
    finally:
        close_db_connection(conn)

def get_membre_par_contact(contact):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM membres WHERE contact = ?", (contact,))
        membre = cursor.fetchone()
        return membre
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du membre : {e}")
        return None
    finally:
        close_db_connection(conn)

def get_admin_par_contact(contact):
    """Récupère un admin par son contact (email)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM membres WHERE contact = ? AND is_admin = 1", (contact,))
        admin = cursor.fetchone()
        return admin
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'admin: {e}")
        return None
    finally:
        close_db_connection(conn)

def ajouter_article(titre, contenu, image_path=None, pdf_path=None, auteur_id=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (titre, contenu, date_publication, image_path, pdf_path, auteur_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titre, contenu, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), image_path, pdf_path, auteur_id))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Erreur lors de l'ajout d'un article : {e}")
        return None
    finally:
        close_db_connection(conn)

def retrancher_article(article_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la suppression de l'article : {e}")
        return False
    finally:
        close_db_connection(conn)

def retrancher_membre(membre_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM membres WHERE id = ?", (membre_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la suppression du membre : {e}")
        return False
    finally:
        close_db_connection(conn)

def est_administrateur(admin_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT is_admin FROM membres WHERE id = ?", (admin_id,))
        result = cursor.fetchone()
        return result and result['is_admin'] == 1
    except Exception as e:
        print(f"Erreur lors de la vérification de l'administrateur : {e}")
        return False
def creer_admin_par_defaut():
    """Crée un administrateur par défaut UNIQUEMENT EN DÉVELOPPEMENT"""
    contact_admin = "admin@sauveteurs.com"
    mot_de_passe_admin = "admin123"
    
    # Vérifie si un admin avec ce contact existe déjà
    if get_membre_par_contact(contact_admin) is None:
        ajouter_membre(
            nom="Administrateur",
            role="Admin",
            contact=contact_admin,
            mot_de_passe=mot_de_passe_admin,
            photo_profil=None,
            is_admin=1
        )
        logger.warning("⚠️ Administrateur par défaut créé (admin@sauveteurs.com/admin123) - À CHANGER EN PRODUCTION")
    else:
        logger.info("Administrateur par défaut déjà existant.")

def compter_admins():
    """Compte le nombre d'administrateurs"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM membres WHERE is_admin = 1")
        result = cursor.fetchone()
        return result['count'] if result else 0
    except Exception as e:
        logger.error(f"Erreur lors du comptage des admins: {e}")
        return 0
    finally:
        close_db_connection(conn)

