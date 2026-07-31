from app import create_app, db
from app.models.utilisateur import Utilisateur

app = create_app()

with app.app_context():
    admin = Utilisateur.query.filter_by(email="admin@ocfga.com").first()

    if admin:
        admin.mot_de_passe = "jawedi2020"
        db.session.commit()
        print("✅ Mot de passe réinitialisé avec succès à 'jawedi2020' pour admin@ocfga.com")
    else:
        print("⚠️ Aucun utilisateur trouvé avec l'email admin@ocfga.com")