from app import start_app

# Erstelle eine Flask-App
app = start_app()

# Starte die Flask-Anwendung, wenn dieses Skript direkt ausgeführt wird
if __name__ == "__main__":
    app.run(
        debug=True
    )  # Starte die Flask-Anwendung im Debug-Modus, um Fehlermeldungen anzuzeigen
