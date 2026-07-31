from datetime import datetime

from app import db

from app.models.etat_outil import EtatOutil
from app.models.historique_etat import HistoriqueEtat


class CalculEtat:

    """
    Détermine l'état de santé de l'outil
    à partir des dégâts cumulés.
    """

    @staticmethod
    def mettre_a_jour(outil):

        # ==========================================
        # Dégâts cumulés
        # ==========================================

        degats = outil.degats_cumules or 0

        # ==========================================
        # Détermination de l'état
        # ==========================================

        if degats < 20:

            nouvel_etat = "S0"
            indice_sante = 100

        elif degats < 40:

            nouvel_etat = "S1"
            indice_sante = 80

        elif degats < 60:

            nouvel_etat = "S2"
            indice_sante = 60

        elif degats < 80:

            nouvel_etat = "S3"
            indice_sante = 40

        else:

            nouvel_etat = "S4"
            indice_sante = 0

        # ==========================================
        # Recherche de l'état existant
        # ==========================================

        etat_outil = EtatOutil.query.filter_by(
            outil_id=outil.id
        ).first()

        if etat_outil is None:

            etat_outil = EtatOutil(
                outil_id=outil.id
            )

            db.session.add(etat_outil)

            ancien_etat = None

        else:

            ancien_etat = etat_outil.etat

        # ==========================================
        # Mise à jour EtatOutil
        # ==========================================

        etat_outil.etat = nouvel_etat

        etat_outil.indice_sante = indice_sante

        etat_outil.derniere_mise_a_jour = datetime.utcnow()

        # ==========================================
        # Mise à jour de l'outil
        # ==========================================

        outil.etat_actuel = nouvel_etat

        # ==========================================
        # Historique uniquement si changement
        # ==========================================

        if ancien_etat != nouvel_etat:

            historique = HistoriqueEtat(

                etat_outil=etat_outil,

                ancien_etat=ancien_etat,

                nouvel_etat=nouvel_etat,

                date_changement=datetime.utcnow()

            )

            db.session.add(historique)

        # ==========================================
        # Sauvegarde
        # ==========================================

        db.session.commit()

        return etat_outil