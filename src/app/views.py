from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required # die Startseite erfordert ein Login
def home():
    if request.method == 'POST': # Überprüft, ob das Formular abgesendet wurde
        note = request.form.get('note') # Holt sich die Notiz aus dem HTML-Formular

        if len(note) < 1:
            flash('Notiz ist zu kurz!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id) # Erstellt eine neue Notiz mit den angegebenen Daten
            db.session.add(new_note) # Fügt die neue Notiz zur Datenbank hinzu 
            db.session.commit() # Speichert die Änderungen in der Datenbank
            flash('Notiz hinzugefügt!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # Konvertiert die JSON-Daten, die von JavaScript gesendet wurden, in ein Python-Datenobjekt 
    noteId = note['noteId'] # Holt sich die ID der zu löschenden Notiz aus den JSON-Daten
    note = Note.query.get(noteId) # Sucht die Notiz in der Datenbank anhand der ID
    if note:
        if note.user_id == current_user.id: # Überprüft, ob der aktuelle Benutzer die Berechtigung hat, die Notiz zu löschen
            db.session.delete(note) # Löscht die Notiz aus der Datenbank
            db.session.commit() # Speichert die Änderungen in der Datenbank

    return jsonify({}) # Gibt eine leere JSON-Antwort zurück


@views.route('/update-note/<int:note_id>', methods=['POST'])
@login_required
def update_note(note_id):
    note = Note.query.get(note_id)  # Hole die Notiz aus der Datenbank anhand ihrer ID
    new_note = request.json.get('newNote')  # Zugriff auf newNote aus dem JSON-Body der Anfrage
    if note:
        if new_note:  # Überprüfe, ob neue Notizdaten vorhanden sind
            note.data = new_note  # Aktualisiere die Notizdaten
            db.session.commit()  # Speichere die Änderungen in der Datenbank
            flash('Notiz erfolgreich aktualisiert!', category='success')
        else:
            flash('Keine Daten eingegeben.', category='error')
    else:
        flash('Notiz nicht gefunden.', category='error')
    return jsonify({"updated_note_data": note.data}) # Gibt eine JSON-Antwort zurück


@views.route('/users', methods=['GET'])
@login_required
def show_users():
    users = User.query.all()  # Ruft alle Benutzer aus der Datenbank ab
    return render_template("users.html", user=current_user, users=users)


@views.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)  # Ruft den Benutzer aus der Datenbank anhand seiner ID ab
    if user:
        if user.id == current_user.id:  # Überprüfe, ob der aktuelle Benutzer der ändernde User ist
            notizenLoeschen(user)
            db.session.delete(user)  # Löscht den Benutzer aus der Datenbank
            db.session.commit()  # Speichert die Änderungen in der Datenbank
            flash('User erfolgreich gelöscht!', category='success')
        else:
            flash('Du hast nicht die Berechtigung, den Account zu löschen!.', category='error')
    else:
        flash('User nicht gefunden!', category='error')
    return jsonify({}) # Gibt eine JSON-Antwort zurück  

def notizenLoeschen(user):
    # Holen Sie sich alle Notizen des Benutzers
    user_notes = Note.query.filter_by(user_id=user.id).all()
    # Löschen Sie jede Notiz des Benutzers aus der Datenbank
    for note in user_notes:
        db.session.delete(note)
    db.session.commit()


@views.route('/update-user-email/<int:user_id>', methods=['POST'])
@login_required
def updateUserEmail(user_id):
    user = User.query.get(user_id)  # Hole die Notiz aus der Datenbank anhand ihrer ID
    new_mail = request.json.get('newMail')  # Zugriff auf newNote aus dem JSON-Body der Anfrage
    if user:
        if user.id == current_user.id:  # Überprüfe, ob der aktuelle Benutzer der ändernde User ist
            if new_mail:  # Überprüfe, ob neue Notizdaten vorhanden sind
                user.email = new_mail  # Aktualisiere die Notizdaten
                db.session.commit()  # Speichere die Änderungen in der Datenbank
                flash('Email erfolgreich geändert!', category='success')
            else:
                flash('Keine Daten eingegeben!', category='error')
        else:
            flash('Du hast nicht die Berechtigung, diese Mail zu ändern!', category='error')
    else:
        flash('User nicht gefunden!.', category='error')

    return jsonify({}) # Gibt eine JSON-Antwort zurück