from app import create_app
from app.services.utilisateur_service import creer_utilisateur
from app.models.utilisateur import RoleUtilisateur

app = create_app()

with app.app_context():

    utilisateur = creer_utilisateur(
        nom="Jawedi",
        prenom="Abderrahmen",
        email="admin@ocfga.com",
        mot_de_passe="jawedi2020",
        role=RoleUtilisateur.ADMIN
    )

    print("===================================")
    print("Utilisateur créé avec succès !")
    print(f"ID : {utilisateur.id}")
    print(f"Nom : {utilisateur.nom}")
    print(f"Email : {utilisateur.email}")
    print(f"Rôle : {utilisateur.role.value}")
    print("===================================")