from datetime import datetime

from app import db


class Machine(db.Model):
    __tablename__ = "machines"

    # ==================================================
    # IDENTIFICATION
    # ==================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    type_machine = db.Column(
        db.String(100),
        nullable=False
    )

    constructeur = db.Column(
        db.String(100)
    )

    modele = db.Column(
        db.String(100)
    )

    nb_axes = db.Column(
        db.Integer
    )

    # ==================================================
    # PARAMETRES UTILISES PAR L'IGSO
    # ==================================================

    age = db.Column(
        db.Float,
        default=0
    )

    heures_fonctionnement = db.Column(
        db.Float,
        default=0
    )

    rigidite = db.Column(
        db.Float,
        default=1.0
    )

    coefficient_usure = db.Column(
        db.Float,
        default=1.0
    )

    # ==================================================
    # CARACTERISTIQUES TECHNIQUES
    # ==================================================

    puissance_kw = db.Column(
        db.Float
    )

    vitesse_max_broche = db.Column(
        db.Float
    )

    precision_mm = db.Column(
        db.Float
    )

    # ==================================================
    # GESTION
    # ==================================================

    actif = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ==================================================
    # RELATIONS
    # ==================================================

    affectations = db.relationship(
        "Affectation",
        back_populates="machine",
        lazy=True
    )

    sessions = db.relationship(
        "SessionUsinage",
        back_populates="machine",
        lazy=True
    )

    # ==================================================
    # JSON
    # ==================================================

    def to_dict(self):

        return {

            "id": self.id,
            "code": self.code,
            "nom": self.nom,
            "type_machine": self.type_machine,
            "constructeur": self.constructeur,
            "modele": self.modele,
            "nb_axes": self.nb_axes,

            "age": self.age,
            "heures_fonctionnement": self.heures_fonctionnement,
            "rigidite": self.rigidite,
            "coefficient_usure": self.coefficient_usure,

            "puissance_kw": self.puissance_kw,
            "vitesse_max_broche": self.vitesse_max_broche,
            "precision_mm": self.precision_mm,

            "actif": self.actif,

            "date_creation":
                self.date_creation.isoformat()
                if self.date_creation else None
        }