from datetime import datetime

from app import db


class SessionUsinage(db.Model):
    __tablename__ = "sessions_usinage"

    # ==========================
    # Clé primaire
    # ==========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================
    # Dates
    # ==========================
    date_debut = db.Column(
        db.DateTime,
        nullable=False
    )

    date_fin = db.Column(
        db.DateTime,
        nullable=True
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ==========================
    # Relations
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

    matiere_id = db.Column(
        db.Integer,
        db.ForeignKey("matieres.id"),
        nullable=False
    )

    lubrifiant_id = db.Column(
        db.Integer,
        db.ForeignKey("lubrifiants.id"),
        nullable=True
    )

    type_operation_id = db.Column(
        db.Integer,
        db.ForeignKey("types_operations.id"),
        nullable=False
    )

    operateur_id = db.Column(
        db.Integer,
        db.ForeignKey("utilisateurs.id"),
        nullable=False
    )

    # ==========================
    # Informations générales
    # ==========================

    numero_of = db.Column(
        db.String(50),
        nullable=True
    )

    numero_phase = db.Column(
        db.String(30),
        nullable=True
    )

    commentaire = db.Column(
        db.Text
    )

    validee = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # ==========================
    # Relations SQLAlchemy
    # ==========================

    outil = db.relationship(
        "Outil",
        back_populates="sessions"
    )

    machine = db.relationship(
        "Machine",
        back_populates="sessions"
    )

    matiere = db.relationship(
        "Matiere",
        back_populates="sessions"
    )

    lubrifiant = db.relationship(
        "Lubrifiant",
        back_populates="sessions"
    )

    type_operation = db.relationship(
        "TypeOperation",
        back_populates="sessions"
    )

    operateur = db.relationship(
        "Utilisateur",
        back_populates="sessions"
    )
    quantite_fabriquee = db.Column(
        db.Integer,
        default=0
    )

    quantite_rebut = db.Column(
        db.Integer,
        default=0
    )
    parametres_coupe = db.relationship(
        "ParametresCoupe",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan"
    )
    indices = db.relationship(
        "IndicesCalcules",
        back_populates="session",
        uselist=False
    )
    degats = db.relationship(
        "DegatsOutils",
        back_populates="session",
        uselist=False
    )