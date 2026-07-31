import numpy as np
from datetime import datetime
from app import create_app, db
from app.models.outil import Outil
from app.models.etat_outil import EtatOutil
from app.models.prediction import Prediction

# Matrice de Transition de Markov (S0, S1, S2, S3, S4)
# Ex: P[0][0] = probabilité de rester en S0, P[0][1] = probabilité de passer de S0 à S1
MATRICE_TRANSITION = np.array([
    [0.70, 0.25, 0.05, 0.00, 0.00],  # S0 (Neuf)
    [0.00, 0.65, 0.30, 0.05, 0.00],  # S1 (Usure normale)
    [0.00, 0.00, 0.60, 0.35, 0.05],  # S2 (Surveillance)
    [0.00, 0.00, 0.00, 0.50, 0.50],  # S3 (Usure critique)
    [0.00, 0.00, 0.00, 0.00, 1.00]   # S4 (Hors service)
])

ETATS = ["S0", "S1", "S2", "S3", "S4"]


def prédire_chaine_markov(etat_actuel_str):
    """
    Calcule l'état prédit, la probabilité associée et la RUL estimée
    en utilisant la chaîne de Markov.
    """
    if etat_actuel_str not in ETATS:
        etat_actuel_str = "S0"

    index_actuel = ETATS.index(etat_actuel_str)

    # Si l'outil est déjà hors service
    if index_actuel == 4:
        return "S4", 1.0, 0, 0

    # Probabilités pour la prochaine session
    probs_suivant = MATRICE_TRANSITION[index_actuel]
    index_predit = int(np.argmax(probs_suivant))
    etat_predit_str = ETATS[index_predit]
    probabilite = float(probs_suivant[index_predit])

    # Simulation de la RUL (Nombre moyen de sessions restantes avant l'état critique S3)
    # RUL = somme des espérances de vie dans les états jusqu'à S3
    especielles_sessions = {
        "S0": 8,
        "S1": 5,
        "S2": 2,
        "S3": 1,
        "S4": 0
    }
    rul_estimee = especielles_sessions.get(etat_actuel_str, 0)
    sessions_restantes = especielles_sessions.get(etat_predit_str, 0)

    return etat_predit_str, probabilite, sessions_restantes, rul_estimee


def generer_predictions():
    app = create_app()

    with app.app_context():
        print("🔮 Démarrage de la simulation de prédiction Markov...")

        outils = Outil.query.filter_by(actif=True).all()

        if not outils:
            print("⚠️ Aucun outil actif trouvé dans la base de données.")
            return

        for outil in outils:
            # Récupération de l'état actuel
            etat_obj = EtatOutil.query.filter_by(outil_id=outil.id).first()
            etat_actuel = etat_obj.etat if etat_obj else "S0"

            # Application du modèle de Markov
            etat_predit, proba, sessions_restantes, rul = prédire_chaine_markov(etat_actuel)

            # Création de l'enregistrement de prédiction
            prediction = Prediction(
                outil_id=outil.id,
                etat_actuel=etat_actuel,
                etat_predit=etat_predit,
                probabilite=round(proba, 4),
                nombre_sessions_restantes=sessions_restantes,
                rul=rul,
                date_prediction=datetime.utcnow()
            )

            db.session.add(prediction)

            print(f"  ➜ Outil Code: {outil.code}")
            print(f"     • État Actuel     : {etat_actuel}")
            print(f"     • État Prédit     : {etat_predit} (Probabilité: {proba*100:.1f}%)")
            print(f"     • RUL estimée     : {rul} sessions")
            print("-" * 50)

        db.session.commit()
        print("✅ Prédictions sauvegardées avec succès dans la base de données !")


if __name__ == "__main__":
    generer_predictions()