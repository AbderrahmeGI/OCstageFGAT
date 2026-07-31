from datetime import datetime
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class RoleUtilisateur(Enum):
    ADMIN = "ADMIN"
    OPERATEUR = "OPERATEUR"


class Utilisateur(db.Model):
    __tablename__ = "utilisateurs"

    # ==========================
    # Clé primaire
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    # ==========================
    # Informations personnelles
    # ==========================
    nom = db.Column(db.String(100), nullable=False)

    prenom = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    # ==========================
    # Authentification
    # ==========================
    mot_de_passe = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.Enum(RoleUtilisateur),
        nullable=False
    )

    # ==========================
    # Etat du compte
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

    # ==================================================
    # Méthodes métier
    # ==================================================

    def set_password(self, password):
        """
        Hash le mot de passe avant son enregistrement.
        """
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        """
        Vérifie si le mot de passe est correct.
        """
        return check_password_hash(self.mot_de_passe, password)

    def to_dict(self):
        """
        Convertit l'objet Utilisateur en dictionnaire JSON.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "role": self.role.value,
            "actif": self.actif,
            "date_creation": self.date_creation.isoformat()
            if self.date_creation else None
        }

    sessions = db.relationship(
        "SessionUsinage",
        back_populates="operateur",
        lazy=True
    )