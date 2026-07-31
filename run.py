from app import create_app

# Création de l'application
app = create_app()

# Lancement du serveur
if __name__ == "__main__":
    app.run(debug=True)