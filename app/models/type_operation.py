from enum import Enum

from app import db


class NomOperation(Enum):
    FRAISAGE = "FRAISAGE"
    SURFACAGE = "SURFACAGE"
    CONTOURNAGE = "CONTOURNAGE"
    RAINURAGE = "RAINURAGE"
    PERCAGE = "PERCAGE"
    ALESAGE = "ALESAGE"
    TARAUDAGE = "TARAUDAGE"
    FILETAGE = "FILETAGE"
    POINTAGE = "POINTAGE"
    CHANFREINAGE = "CHANFREINAGE"
    LAMAGE = "LAMAGE"
    POCHE = "POCHE"
    AUTRE = "AUTRE"


class TypeOperation(db.Model):
    __tablename__ = "types_operations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.Enum(NomOperation),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    actif = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )
    sessions = db.relationship(
        "SessionUsinage",
        back_populates="type_operation",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom.value,
            "description": self.description,
            "actif": self.actif
        }