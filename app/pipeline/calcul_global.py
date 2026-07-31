from datetime import datetime

from app import db
from app.models.session_usinage import SessionUsinage
from app.models.indices_calcules import IndicesCalcules
from app.models.degats_outils import DegatsOutils
from app.models.etat_outil import EtatOutil as EtatOutilModel
from app.models.historique_etat import HistoriqueEtat
from app.models.prediction import Prediction


class CalculGlobal:

    @staticmethod
    def normaliser(valeur, minimum, maximum):
        if valeur is None:
            return 0.0
        if maximum == minimum:
            return 0.0
        resultat = (valeur - minimum) / (maximum - minimum)
        return max(0.0, min(resultat, 1.0))

    # ============================
    # IGSO
    # ============================
    @staticmethod
    def calculer_igso(session):
        IM = 0.3
        IT = 0.2
        IH = 0.2
        IMA = 0.2
        IP = 0.1

        igso = (
            0.25 * IM +
            0.25 * IT +
            0.20 * IH +
            0.20 * IMA +
            0.10 * IP
        )
        return round(igso, 4)

    # ============================
    # DEGATS
    # ============================
    @staticmethod
    def calculer_degats(session):
        igso = CalculGlobal.calculer_igso(session)
        degat = igso * 100.0
        ancien = session.outil.degats_cumules or 0.0
        cumul = ancien + degat
        return igso, degat, cumul

    # ============================
    # ETAT OUTIL
    # ============================
    @staticmethod
    def determiner_etat(degats):
        if degats < 20:
            return "S0"
        elif degats < 50:
            return "S1"
        elif degats < 80:
            return "S2"
        elif degats < 100:
            return "S3"
        else:
            return "S4"

    # ============================
    # EXECUTION COMPLETE
    # ============================
    @staticmethod
    def executer(session_id):
        session = SessionUsinage.query.get(session_id)

        if session is None:
            raise Exception(f"Session #{session_id} inexistante")

        # ---- IGSO ----
        igso, degat, cumul = CalculGlobal.calculer_degats(session)

        # Vérification si l'indice existe déjà
        indice = IndicesCalcules.query.filter_by(session_id=session.id).first()
        if indice is None:
            indice = IndicesCalcules(
                session_id=session.id,
                indice_mecanique=0.3,
                indice_thermique=0.2,
                indice_machine=0.2,
                indice_historique=0.2,
                indice_parametres=0.1,
                igso=igso
            )
            db.session.add(indice)
        else:
            indice.indice_mecanique = 0.3
            indice.indice_thermique = 0.2
            indice.indice_machine = 0.2
            indice.indice_historique = 0.2
            indice.indice_parametres = 0.1
            indice.igso = igso

        # ---- DEGATS ----
        degats_obj = DegatsOutils.query.filter_by(session_id=session.id).first()
        if degats_obj is None:
            degats_obj = DegatsOutils(
                session_id=session.id,
                outil_id=session.outil_id,
                igso=igso,
                degats_session=degat,
                degats_cumules=cumul
            )
            db.session.add(degats_obj)
        else:
            degats_obj.igso = igso
            degats_obj.degats_session = degat
            degats_obj.degats_cumules = cumul

        # Mise à jour de l'outil
        session.outil.degats_cumules = cumul

        # ---- ETAT OUTIL ----
        nouvel_etat = CalculGlobal.determiner_etat(cumul)
        indice_sante = max(0.0, 100.0 - cumul)

        etat = EtatOutilModel.query.filter_by(outil_id=session.outil_id).first()

        if etat is None:
            ancien_etat = "S0"
            etat = EtatOutilModel(
                outil_id=session.outil_id,
                etat=nouvel_etat,
                indice_sante=indice_sante,
                derniere_mise_a_jour=datetime.utcnow()
            )
            db.session.add(etat)
            db.session.flush()
        else:
            ancien_etat = etat.etat
            etat.etat = nouvel_etat
            etat.indice_sante = indice_sante
            etat.derniere_mise_a_jour = datetime.utcnow()

        # ---- HISTORIQUE ETATS ----
        historique = HistoriqueEtat(
            etat_outil_id=etat.id,
            ancien_etat=ancien_etat,
            nouvel_etat=nouvel_etat,
            raison=f"Calcul/Mise à jour session #{session.id}",
            date_transition=datetime.utcnow()
        )
        db.session.add(historique)

        # ---- PREDICTION ----
        prediction = Prediction(
            outil_id=session.outil_id,
            etat_actuel=nouvel_etat,
            etat_predit=nouvel_etat,
            probabilite=1.0,
            nombre_sessions_restantes=None,
            rul=None
        )
        db.session.add(prediction)

        db.session.commit()

        return {
            "session": session.id,
            "igso": igso,
            "degat": degat,
            "cumul": cumul,
            "etat": nouvel_etat
        }
