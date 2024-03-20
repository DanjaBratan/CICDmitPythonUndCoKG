from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from hashlib import sha256


auth = Blueprint('auth', __name__)

# Route zum Anmelden
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # Suchen des Benutzers anhand der E-Mail-Adresse
        if user:           
            hashed_password = sha256(password.encode('utf-8')).hexdigest()
            if user.password == hashed_password:
                flash('Erfolgreich angemeldet!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Falsches Passwort!', category='error')
        else:
            flash('Email existiert nicht!', category='error')

    return render_template("login.html", user=current_user)

# Route zum Abmelden
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Route zum Registrieren
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email existiert bereits!', category='error')
        elif len(email) < 4:
            flash('Email muss länger als 3 Zeichen sein!', category='error')
        elif len(first_name) < 2:
            flash('Vorname muss größer als 1 Zeichen sein!', category='error')
        elif password1 != password2:
            flash('Passwörter passen nicht!', category='error')
        elif len(password1) < 7:
            flash('Passwort muss mindestens 7 Zeichen haben!', category='error')
        else:
            # Hashen des Passworts und Erstellen eines neuen Benutzers
            new_user = User(email=email, first_name=first_name, password=sha256(password1.encode('utf-8')).hexdigest())

            db.session.add(new_user) # Hinzufügen des neuen Benutzers zur Datenbank
            db.session.commit()
             # Login des neuen Benutzers
            login_user(new_user, remember=True)
            flash('Account erstellt!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

