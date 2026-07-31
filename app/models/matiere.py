from datetime import datetime

from app import db


class Matiere(db.Model):
    __tablename__ = "matieres"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    # ALUMINIUM
    # ACIER
    # INOX
    # TITANE
    # COMPOSITE
    # AUTRE
    famille = db.Column(
        db.String(50),
        nullable=False
    )

    durete_hb = db.Column(
        db.Float,
        nullable=False
    )

    usinabilite = db.Column(
        db.Float,
        nullable=False
    )

    conductivite_thermique = db.Column(
        db.Float,
        nullable=True
    )

    densite = db.Column(
        db.Float,
        nullable=True
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
        back_populates="matiere",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "famille": self.famille,
            "durete_hb": self.durete_hb,
            "usinabilite": self.usinabilite,
            "conductivite_thermique": self.conductivite_thermique,
            "densite": self.densite,
            "description": self.description,
            "actif": self.actif,
            "date_creation": (
                self.date_creation.isoformat()
                if self.date_creation else None
            )
        }