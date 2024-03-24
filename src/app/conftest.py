import pytest
from app import start_app, db
from .models import User, Note


# Fixture zum Konfigurieren und Bereitstellen der Flask-App für Tests
@pytest.fixture
def app():
    app = start_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Verwendung einer SQLite-In-Memory-Datenbank für Tests
    yield app
    with app.app_context(): # Teardown - Löschen der Datenbankinhalte und Schließen der App-Instanz
        db.session.remove()
        db.drop_all()


# Client-Fixture für Testhttp-Anfragen
@pytest.fixture
def client(app):
    return app.test_client()


# Erstellen eines Fixtures für einen Testbenutzer
@pytest.fixture(scope='function')
def test_user(app):
    with app.app_context():
        user = User(email='test@example.com', password='securepassword', first_name='Test')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

# Erstellen eines Fixtures für eine Testnotiz
@pytest.fixture(scope='function')
def test_note(test_user):
    with app.app_context():
        note = Note(data='Testnotiz', user=test_user)
        db.session.add(note)
        db.session.commit()
        yield note
        db.session.delete(note)
        db.session.commit()
