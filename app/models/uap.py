from datetime import datetime

from app import db


class UAP(db.Model):
    __tablename__ = "uaps"

    # ==========================
    # Clé primaire
    # ==========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================
    # Informations générales
    # ==========================
    nom = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

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
    # Conversion JSON
    # ==========================
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "actif": self.actif,
            "date_creation": self.date_creation.isoformat()
            if self.date_creation else None
        }