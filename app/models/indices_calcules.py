from datetime import datetime

from app import db


class IndicesCalcules(db.Model):
    __tablename__ = "indices_calcules"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions_usinage.id"),
        nullable=False,
        unique=True
    )

    indice_mecanique = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    indice_thermique = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    indice_machine = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    indice_historique = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    indice_parametres = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    igso = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    date_calcul = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    session = db.relationship(
        "SessionUsinage",
        back_populates="indices"
    )

    def to_dict(self):

        return {

            "id": self.id,

            "session_id": self.session_id,

            "indice_mecanique": self.indice_mecanique,

            "indice_thermique": self.indice_thermique,

            "indice_machine": self.indice_machine,

            "indice_historique": self.indice_historique,

            "indice_parametres": self.indice_parametres,

            "igso": self.igso,

            "date_calcul": self.date_calcul.isoformat()
            if self.date_calcul else None

        }