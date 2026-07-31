from flask import Blueprint, jsonify, request

from app.models.utilisateur import RoleUtilisateur
from app.services.utilisateur_service import (
    creer_utilisateur,
    obtenir_tous_les_utilisateurs
)

utilisateur_bp = Blueprint(
    "utilisateurs",
    __name__
)


@utilisateur_bp.route("/api/utilisateurs", methods=["GET"])
def liste_utilisateurs():

    utilisateurs = obtenir_tous_les_utilisateurs()

    resultat = []

    for utilisateur in utilisateurs:
        resultat.append(utilisateur.to_dict())

    return jsonify(resultat)


@utilisateur_bp.route("/api/utilisateurs", methods=["POST"])
def ajouter_utilisateur():

    try:

        data = request.get_json()

        role = RoleUtilisateur[data["role"]]

        utilisateur = creer_utilisateur(
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            mot_de_passe=data["mot_de_passe"],
            role=role
        )

        return jsonify({
            "message": "Utilisateur créé avec succès.",
            "utilisateur": utilisateur.to_dict()
        }), 201

    except ValueError as e:

        return jsonify({
            "erreur": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "erreur": str(e)
        }), 500