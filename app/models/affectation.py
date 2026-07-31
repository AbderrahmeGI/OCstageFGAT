from datetime import datetime

from app import db


class Affectation(db.Model):
    __tablename__ = "affectations"

    # ==========================
    # Clé primaire
    # ==========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================
    # Clés étrangères
    # ==========================
    outil_id = db.Column(
        db.Integer,
        db.ForeignKey("outils.id"),
        nullable=False
    )

    machine_id = db.Column(
        db.Integer,
        db.ForeignKey("machines.id"),
        nullable=False
    )

    # ==========================
    # Relations
    # ==========================
    outil = db.relationship(
        "Outil",
        back_populates="affectations"
    )

    machine = db.relationship(
        "Machine",
        back_populates="affectations"
    )

    # ==========================
    # Informations métier
    # ==========================
    date_debut = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    date_fin = db.Column(
        db.DateTime
    )

    poste = db.Column(
        db.String(50)
    )

    commentaire = db.Column(
        db.Text
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
            "outil_id": self.outil_id,
            "machine_id": self.machine_id,
            "outil": self.outil.code if self.outil else None,
            "machine": self.machine.code if self.machine else None,
            "date_debut": self.date_debut.isoformat() if self.date_debut else None,
            "date_fin": self.date_fin.isoformat() if self.date_fin else None,
            "poste": self.poste,
            "commentaire": self.commentaire,
            "actif": self.actif,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }