from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.utilisateur import Utilisateur

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Recherche de l'utilisateur dans la base
        utilisateur = Utilisateur.query.filter_by(email=email).first()

        # Vérification des identifiants
        if utilisateur and utilisateur.mot_de_passe == password:
            session["user_id"] = utilisateur.id
            session["user_nom"] = utilisateur.nom
            session["user_role"] = (
                utilisateur.role.value
                if hasattr(utilisateur.role, 'value')
                else str(utilisateur.role)
            )

            return redirect(url_for("auth.login"))  # Ou vers votre futur dashboard
        else:
            flash("Email ou mot de passe incorrect.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.dashboard"))