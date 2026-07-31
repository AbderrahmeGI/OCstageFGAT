from datetime import datetime
from enum import Enum

from app import db


# =====================================================
# Énumération des États de l'outil (S0 à S4)
# =====================================================
class EtatOutil(Enum):
    S0 = "S0"  # Neuf
    S1 = "S1"  # Usure normale
    S2 = "S2"  # Surveillance / Usure modérée
    S3 = "S3"  # Usure critique / Affûté
    S4 = "S4"  # Hors service / Cassé


# Alias pour rétrocompatibilité si un script importe EtatCourant
EtatCourant = EtatOutil


# =====================================================
# Modèle Outil
# =====================================================
class Outil(db.Model):
    __tablename__ = "outils"

    # ==========================
    # Clé primaire
    # ==========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================
    # Identification
    # ==========================
    code = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    numero_serie = db.Column(
        db.String(100),
        unique=True
    )

    # ==========================
    # Relation avec TypeOutil
    # ==========================
    type_outil_id = db.Column(
        db.Integer,
        db.ForeignKey("types_outils.id"),
        nullable=False
    )

    type_outil = db.relationship(
        "TypeOutil",
        back_populates="outils"
    )

    # ==========================
    # Cycle de vie
    # ==========================
    date_mise_service = db.Column(
        db.Date
    )

    nb_affutages = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    dernier_affutage = db.Column(
        db.Date
    )

    # ==========================
    # Données métier
    # ==========================
    degats_cumules = db.Column(
        db.Float,
        default=0.0,
        nullable=False
    )

    etat_actuel = db.Column(
        db.Enum(EtatOutil),
        default=EtatOutil.S0,
        nullable=False
    )

    commentaire = db.Column(
        db.Text
    )

    # ==========================
    # Gestion
    # ==========================
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
    # Relations SQLAlchemy
    # ==========================
    affectations = db.relationship(
        "Affectation",
        back_populates="outil",
        lazy=True
    )

    sessions = db.relationship(
        "SessionUsinage",
        back_populates="outil",
        lazy=True
    )

    predictions = db.relationship(
        "Prediction",
        back_populates="outil",
        lazy=True
    )
    etat = db.relationship(
        "EtatOutil",
        back_populates="outil",
        uselist=False
    )

    # ==========================
    # Conversion JSON
    # ==========================
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "numero_serie": self.numero_serie,
            "type_outil_id": self.type_outil_id,
            "type_outil": self.type_outil.designation if self.type_outil else None,
            "date_mise_service": (
                self.date_mise_service.isoformat()
                if self.date_mise_service else None
            ),
            "nb_affutages": self.nb_affutages,
            "dernier_affutage": (
                self.dernier_affutage.isoformat()
                if self.dernier_affutage else None
            ),
            "degats_cumules": self.degats_cumules,
            "etat_actuel": self.etat_actuel.value if hasattr(self.etat_actuel, 'value') else str(self.etat_actuel),
            "commentaire": self.commentaire,
            "actif": self.actif,
            "date_creation": (
                self.date_creation.isoformat()
                if self.date_creation else None
            )
        }