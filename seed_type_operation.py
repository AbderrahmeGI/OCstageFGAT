from app import create_app, db
from app.models.type_operation import TypeOperation, NomOperation

app = create_app()

with app.app_context():

    operations = [
        (NomOperation.FRAISAGE, "Opération de fraisage"),
        (NomOperation.SURFACAGE, "Surfaçage"),
        (NomOperation.CONTOURNAGE, "Contournage"),
        (NomOperation.RAINURAGE, "Rainurage"),
        (NomOperation.PERCAGE, "Perçage"),
        (NomOperation.ALESAGE, "Alésage"),
        (NomOperation.TARAUDAGE, "Taraudage"),
        (NomOperation.FILETAGE, "Filetage"),
        (NomOperation.POINTAGE, "Pointage"),
        (NomOperation.CHANFREINAGE, "Chanfreinage"),
        (NomOperation.LAMAGE, "Lamage"),
        (NomOperation.POCHE, "Usinage de poche"),
        (NomOperation.AUTRE, "Autre opération")
    ]

    for nom, description in operations:

        existe = TypeOperation.query.filter_by(nom=nom).first()

        if not existe:

            db.session.add(
                TypeOperation(
                    nom=nom,
                    description=description
                )
            )

    db.session.commit()

    print("===================================")
    print("Types d'opérations ajoutés avec succès.")
    print("===================================")