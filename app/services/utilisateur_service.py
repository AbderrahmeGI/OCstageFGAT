from app import db
from app.models.utilisateur import Utilisateur, RoleUtilisateur


def creer_utilisateur(
    nom,
    prenom,
    email,
    mot_de_passe,
    role=RoleUtilisateur.OPERATEUR
):
    """
    Création d'un nouvel utilisateur.
    """

    utilisateur_existant = Utilisateur.query.filter_by(email=email).first()

    if utilisateur_existant:
        raise ValueError("Cet email existe déjà.")

    utilisateur = Utilisateur(
        nom=nom,
        prenom=prenom,
        email=email,
        role=role
    )

    utilisateur.set_password(mot_de_passe)

    db.session.add(utilisateur)

    db.session.commit()

    return utilisateur


def obtenir_tous_les_utilisateurs():
    """
    Retourne tous les utilisateurs.
    """
    return Utilisateur.query.all()