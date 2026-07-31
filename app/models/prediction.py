from datetime import datetime

from app import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    outil_id = db.Column(
        db.Integer,
        db.ForeignKey("outils.id"),
        nullable=False
    )

    etat_actuel = db.Column(
        db.String(5),
        nullable=False
    )

    etat_predit = db.Column(
        db.String(5),
        nullable=False
    )

    probabilite = db.Column(
        db.Float,
        nullable=False
    )

    rul = db.Column(
        db.Float,
        nullable=True
    )

    nombre_sessions_restantes = db.Column(
        db.Integer,
        nullable=True
    )

    date_prediction = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    outil = db.relationship(
        "Outil",
        back_populates="predictions"
    )

    def to_dict(self):

        return {

            "id": self.id,

            "outil_id": self.outil_id,

            "etat_actuel": self.etat_actuel,

            "etat_predit": self.etat_predit,

            "probabilite": self.probabilite,

            "rul": self.rul,

            "nombre_sessions_restantes":
                self.nombre_sessions_restantes,

            "date_prediction":
                self.date_prediction.isoformat()
                if self.date_prediction else None
        }