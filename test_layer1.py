from app import create_app
from app.extensions import db
from app.models.indices_calcules import IndicesCalcules
from app.models.degats_outil import DegatsOutil

app = create_app()

with app.app_context():
    print("=== TEST CHARGEMENT DES MODÈLES COUCHE 1 ===")
    print("Table IndicesCalcules :", IndicesCalcules.__tablename__)
    print("Table DegatsOutil      :", DegatsOutil.__tablename__)
    print("===========================================")