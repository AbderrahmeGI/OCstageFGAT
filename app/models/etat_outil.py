from datetime import datetime

from app import db


class EtatOutil(db.Model):
    __tablename__ = "etat_outils"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    outil_id = db.Column(
        db.Integer,
        db.ForeignKey("outils.id"),
        nullable=False,
        unique=True
    )

    etat = db.Column(
        db.String(5),
        nullable=False,
        default="S0"
    )

    indice_sante = db.Column(
        db.Float,
        nullable=False,
        default=100
    )

    derniere_mise_a_jour = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    outil = db.relationship(
        "Outil",
        back_populates="etat"
    )

    historique = db.relationship(
        "HistoriqueEtat",
        back_populates="etat_outil",
        lazy=True
    )

    def to_dict(self):

        return {

            "id": self.id,

            "outil_id": self.outil_id,

            "etat": self.etat,

            "indice_sante": self.indice_sante,

            "derniere_mise_a_jour":
                self.derniere_mise_a_jour.isoformat()
                if self.derniere_mise_a_jour else None

        }