from datetime import datetime
from enum import Enum

from app import db


class CategorieOutil(Enum):
    FRAISE = "FRAISE"
    FORET = "FORET"
    TARAUD = "TARAUD"
    ALESOIR = "ALESOIR"
    PLAQUETTE = "PLAQUETTE"


class TypeOutil(db.Model):
    __tablename__ = "types_outils"

    # ==========================
    # Clé primaire
    # ==========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================
    # Identification
    # ==========================
    reference = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    designation = db.Column(
        db.String(150),
        nullable=False
    )

    fabricant = db.Column(
        db.String(100)
    )

    # ==========================
    # Caractéristiques techniques
    # ==========================
    categorie = db.Column(
        db.Enum(CategorieOutil),
        nullable=False
    )

    diametre = db.Column(
        db.Float,
        nullable=False
    )

    nb_dents = db.Column(
        db.Integer
    )

    matiere = db.Column(
        db.String(100)
    )

    revetement = db.Column(
        db.String(100)
    )

    angle_helice = db.Column(
        db.Float
    )

    # ==========================
    # Etat
    # ==========================
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
    # ==========================
    # Relations
    # ==========================

    outils = db.relationship(
        "Outil",
        back_populates="type_outil",
        lazy=True
    )
    # ==========================
    # Conversion JSON
    # ==========================
    def to_dict(self):

        return {

            "id": self.id,

            "reference": self.reference,

            "designation": self.designation,

            "fabricant": self.fabricant,

            "categorie": self.categorie.value,

            "diametre": self.diametre,

            "nb_dents": self.nb_dents,

            "matiere": self.matiere,

            "revetement": self.revetement,

            "angle_helice": self.angle_helice,

            "actif": self.actif,

            "date_creation": self.date_creation.isoformat()
            if self.date_creation else None
        }