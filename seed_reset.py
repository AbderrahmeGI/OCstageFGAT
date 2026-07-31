from app import create_app, db

app = create_app()


def reset_db():
    with app.app_context():
        print("⚠️  Suppression de toutes les tables de la base de données...")
        db.drop_all()

        print("🏗️  Recréation de toutes les tables à partir des modèles...")
        db.create_all()

        print("✅ La base de données a été réinitialisée à zéro avec succès !")


if __name__ == "__main__":
    reset_db()