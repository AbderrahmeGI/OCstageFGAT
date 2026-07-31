from datetime import datetime

from app import db


class HistoriqueEtat(db.Model):
    __tablename__ = "historique_etats"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    etat_outil_id = db.Column(
        db.Integer,
        db.ForeignKey("etat_outils.id"),
        nullable=False
    )

    ancien_etat = db.Column(
        db.String(5),
        nullable=False
    )

    nouvel_etat = db.Column(
        db.String(5),
        nullable=False
    )

    raison = db.Column(
        db.String(255)
    )

    date_transition = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    etat_outil = db.relationship(
        "EtatOutil",
        back_populates="historique"
    )

    def to_dict(self):

        return {

            "id": self.id,

            "etat_outil_id": self.etat_outil_id,

            "ancien_etat": self.ancien_etat,

            "nouvel_etat": self.nouvel_etat,

            "raison": self.raison,

            "date_transition":
                self.date_transition.isoformat()
                if self.date_transition else None

        }