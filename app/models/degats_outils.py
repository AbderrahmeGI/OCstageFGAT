from datetime import datetime

from app import db


class DegatsOutils(db.Model):
    __tablename__ = "degats_outils"

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

    outil_id = db.Column(
        db.Integer,
        db.ForeignKey("outils.id"),
        nullable=False
    )

    igso = db.Column(
        db.Float,
        nullable=False
    )

    degats_session = db.Column(
        db.Float,
        nullable=False
    )

    degats_cumules = db.Column(
        db.Float,
        nullable=False
    )

    date_calcul = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    session = db.relationship(
        "SessionUsinage",
        back_populates="degats"
    )

    outil = db.relationship(
        "Outil"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "outil_id": self.outil_id,
            "igso": self.igso,
            "degats_session": self.degats_session,
            "degats_cumules": self.degats_cumules,
            "date_calcul": self.date_calcul.isoformat() if self.date_calcul else None
        }