from app.models import User, Note
from app import db


# Testen der Startseite
def test_home(client, test_user):
    with client.session_transaction() as session:
        session["_user_id"] = test_user.id
    response = client.get("/")
    assert response.status_code == 200
    assert b"Notizen" in response.data


# Testen des Hinzufügens einer Notiz
def test_add_note(app, client, test_user):
    with client.session_transaction() as session:
        session["_user_id"] = test_user.id
    response = client.post("/", data={"note": "Testnotiz"})
    with app.app_context():  # Überprüfe, ob die Notiz erfolgreich hinzugefügt wurde
        added_note = Note.query.filter_by(
            data="Testnotiz", user_id=test_user.id
        ).first()
        assert added_note is not None
    assert response.status_code == 200
    assert b"Notiz hinzu" in response.data  # "Notiz hinzugefügt!" flash text


# Testen des (Hinzufügens und) Löschens einer Notiz
def test_delete_note(client, test_user):
    with client.session_transaction() as session:
        session["_user_id"] = test_user.id
    note = Note(data="Testnotiz1", user_id=test_user.id)
    db.session.add(note)
    db.session.commit()
    response = client.post("/delete-note/{}".format(note.id)) #edit
    assert response.status_code == 200
    assert not Note.query.get(
        note.id
    )  # Überprüfen, ob die Notiz aus der Datenbank entfernt wurde


# Testen der Aktualisierung einer Notiz
def test_update_note(client, test_user):
    with client.session_transaction() as session:
        session["_user_id"] = test_user.id
    note = Note(data="Testnotiz", user_id=test_user.id)
    db.session.add(note)
    db.session.commit()

    response = client.post(
        "/update-note/{}".format(note.id), json={"newNote": "Aktualisierte Notiz"}
    )
    assert response.status_code == 200

    # Überprüfen, ob die Notiz aktualisiert wurde
    assert Note.query.get(note.id).data == "Aktualisierte Notiz"


# Test für `show_users`
def test_show_users(client, test_user):
    with client.session_transaction() as session:
        session["_user_id"] = test_user.id
    response = client.get("/users")
    assert response.status_code == 200
    assert b"TestUser1" in response.data


# Test für `updateUserEmail`
def test_updateUserEmail(client, test_user):
    user1 = test_user
    with client.session_transaction() as session:
        session["_user_id"] = user1.id
    new_email = "newemail@example.com"
    response = client.post(
        "/update-user-email/{}".format(user1.id), json={"newMail": new_email}
    )
    assert response.status_code == 200
    assert User.query.get(user1.id).email == new_email


# Test für `delete_user`
def test_delete_user(client, test_user):
    user1 = test_user
    with client.session_transaction() as session:
        session["_user_id"] = user1.id
    response = client.post("/delete-user/{}".format(user1.id))
    assert response.status_code == 200
    assert User.query.get(user1.id) is None
