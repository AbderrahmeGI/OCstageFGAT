from flask import Blueprint, render_template, session, redirect, url_for

# Déclaration exacte du Blueprint sous le nom 'main_bp'
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Redirige vers le dashboard si l'utilisateur est connecté, sinon vers le login."""
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
def dashboard():
    """Page principale du tableau de bord (nécessite une session active)."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html", user_nom=session.get("user_nom"))