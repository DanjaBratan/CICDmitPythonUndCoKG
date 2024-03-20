from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Erstellen einer Instanz der SQLAlchemy-Datenbank
db = SQLAlchemy()
DB_NAME = "datenbank.db"

# Funktion zur Initialisierung und Konfiguration der Flask-App
def start_app():
    
    app = Flask(__name__) # Erstellen der Flask-App

    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Konfiguration der geheimen Schlüssel für die Flask-Session

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Konfiguration der Datenbankverbindung

    db.init_app(app) # Initialisierung der SQLAlchemy-Datenbank mit der Flask-App

    # Import der Ansichten (Views) und Authentifizierungs-Bluprinte
    from .views import views
    from .auth import auth

    # Registrierung der Bluprinte mit der Flask-App
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import der Datenbankmodelle
    from .models import User, Note

    # Erstellen der Datenbanktabellen
    with app.app_context():
        db.create_all()

    # Konfiguration des Login-Managers für die Flask-App
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Festlegung der Login-Seite
    login_manager.init_app(app)

    # Funktion zum Laden eines Benutzers basierend auf seiner ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Funktion zum Erstellen der Datenbank, falls sie nicht vorhanden ist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')