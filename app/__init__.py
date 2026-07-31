from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuration de l'application
    app.config.from_object("config.Config")
    app.secret_key = "votre_cle_secrete_super_securisee"

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ======================================================
    # Enregistrement des Blueprints (Routes)
    # ======================================================
    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    from app.routes.utilisateur_routes import utilisateur_bp
    from app.routes.calcul_routes import calcul_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(calcul_bp)

    # ======================================================
    # Import des modèles SQLAlchemy
    # ======================================================
    from app.models import (
        Utilisateur,
        UAP,
        Machine,
        TypeOutil,
        Outil,
        Affectation,
        Matiere,
        Lubrifiant,
        TypeOperation,
        SessionUsinage,
        IndicesCalcules,
        ParametresCoupe,
        DegatsOutils,
        EtatOutil,
        HistoriqueEtat,
        Prediction,
    )

    print("========== MODELES CHARGES ==========")
    print(db.metadata.tables.keys())
    print("=====================================")

    return app