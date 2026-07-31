from datetime import datetime

from app import db
from app.models.degats_outils import DegatsOutils
from app.pipeline.etat import CalculEtat
from app.pipeline.igso import CalculIGSO
calculer = CalculIGSO.calculer

class CalculDegats:

    """
    Damage Engine.

    Cette classe calcule :

        Session
            ↓
        IGSO
            ↓
        Δ Dégâts
            ↓
        Dégâts cumulés
            ↓
        Etat outil
    """

    # ===========================================
    # coefficient global
    # ===========================================

    COEFFICIENT_DEGATS = 10

    # ===========================================
    # calcul dégâts
    # ===========================================

    @staticmethod
    def calculer(session):

        # -----------------------------
        # Calcul IGSO
        # -----------------------------

        indice = CalculIGSO.calculer(session)

        igso = indice.igso

        # -----------------------------
        # Outil
        # -----------------------------

        outil = session.outil

        anciens_degats = outil.degats_cumules or 0

        # -----------------------------
        # dégâts session
        # -----------------------------

        degats_session = round(

            igso * CalculDegats.COEFFICIENT_DEGATS,

            4

        )

        # -----------------------------
        # dégâts cumulés
        # -----------------------------

        nouveaux_degats = round(

            anciens_degats + degats_session,

            4

        )

        # -----------------------------
        # mise à jour outil
        # -----------------------------

        outil.degats_cumules = nouveaux_degats

        # -----------------------------
        # table DegatsOutils
        # -----------------------------

        degats = DegatsOutils.query.filter_by(

            session_id=session.id

        ).first()

        if degats is None:

            degats = DegatsOutils(

                session_id=session.id,

                outil_id=outil.id

            )

            db.session.add(degats)

        degats.igso = igso

        degats.degats_session = degats_session

        degats.degats_cumules = nouveaux_degats

        degats.date_calcul = datetime.utcnow()

        db.session.commit()

        # -----------------------------
        # Etat
        # -----------------------------

        CalculEtat.mettre_a_jour(outil)

        return degats