from datetime import datetime

from app import db


class Lubrifiant(db.Model):
    __tablename__ = "lubrifiants"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    concentration = db.Column(
        db.Float,
        nullable=True
    )

    debit = db.Column(
        db.Float,
        nullable=True
    )

    pression = db.Column(
        db.Float,
        nullable=True
    )

    coefficient_refroidissement = db.Column(
        db.Float,
        default=1.0,
        nullable=False
    )

    coefficient_lubrification = db.Column(
        db.Float,
        default=1.0,
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

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    sessions = db.relationship(
        "SessionUsinage",
        back_populates="lubrifiant",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "type": self.type,
            "concentration": self.concentration,
            "debit": self.debit,
            "pression": self.pression,
            "coefficient_refroidissement": self.coefficient_refroidissement,
            "coefficient_lubrification": self.coefficient_lubrification,
            "description": self.description,
            "actif": self.actif,
            "date_creation": self.date_creation.isoformat()
            if self.date_creation else None
        }