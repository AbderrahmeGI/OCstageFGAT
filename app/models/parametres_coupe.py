from datetime import datetime

from app import db


class ParametresCoupe(db.Model):
    __tablename__ = "parametres_coupe"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions_usinage.id"),
        nullable=False,
        unique=True
    )

    vitesse_coupe = db.Column(db.Float)

    vitesse_rotation = db.Column(db.Float)

    avance = db.Column(db.Float)

    avance_par_dent = db.Column(db.Float)

    profondeur_axiale = db.Column(db.Float)

    profondeur_radiale = db.Column(db.Float)

    largeur_usinage = db.Column(db.Float)

    longueur_usinage = db.Column(db.Float)

    nombre_passes = db.Column(
        db.Integer,
        default=1
    )

    temps_coupe = db.Column(db.Float)

    engagement = db.Column(db.Float)

    observations = db.Column(db.Text)

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    session = db.relationship(
        "SessionUsinage",
        back_populates="parametres_coupe"
    )

    def __repr__(self):
        return (
            f"<ParametresCoupe "
            f"Session={self.session_id}>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "vitesse_coupe": self.vitesse_coupe,
            "vitesse_rotation": self.vitesse_rotation,
            "avance": self.avance,
            "avance_par_dent": self.avance_par_dent,
            "profondeur_axiale": self.profondeur_axiale,
            "profondeur_radiale": self.profondeur_radiale,
            "largeur_usinage": self.largeur_usinage,
            "longueur_usinage": self.longueur_usinage,
            "nombre_passes": self.nombre_passes,
            "temps_coupe": self.temps_coupe,
            "engagement": self.engagement,
            "observations": self.observations,
            "date_creation": (
                self.date_creation.isoformat()
                if self.date_creation
                else None
            )
        }