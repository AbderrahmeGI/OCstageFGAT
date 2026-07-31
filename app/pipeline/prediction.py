from datetime import datetime

from app import db

from app.models.prediction import Prediction


class CalculPrediction:
    """
    Placeholder de la couche Prediction.

    Pour le prototype, la prédiction correspond
    simplement à l'état actuel de l'outil.

    Cette classe sera remplacée plus tard
    par le moteur de Markov.
    """

    @staticmethod
    def calculer(outil):

        # =====================================
        # Etat actuel
        # =====================================

        etat = outil.etat_actuel

        # =====================================
        # Valeurs provisoires
        # =====================================

        etat_predit = etat

        probabilite = 1.0

        rul = None

        nombre_sessions_restantes = None

        # =====================================
        # Recherche d'une prédiction existante
        # =====================================

        prediction = Prediction.query.filter_by(
            outil_id=outil.id
        ).first()

        # =====================================
        # Création
        # =====================================

        if prediction is None:

            prediction = Prediction(
                outil_id=outil.id
            )

            db.session.add(prediction)

        # =====================================
        # Mise à jour
        # =====================================

        prediction.etat_actuel = etat

        prediction.etat_predit = etat_predit

        prediction.probabilite = probabilite

        prediction.rul = rul

        prediction.nombre_sessions_restantes = (
            nombre_sessions_restantes
        )

        prediction.date_prediction = datetime.utcnow()

        db.session.commit()

        return prediction