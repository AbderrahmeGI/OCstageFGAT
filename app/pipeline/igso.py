"""
=========================================================
PIPELINE IGSO
---------------------------------------------------------
Calcul de l'Indice Global de Sollicitation de l'Outil

Entrées :
    - SessionUsinage
    - ParametresCoupe
    - Machine
    - Outil
    - Matiere
    - Lubrifiant
    - TypeOperation

Sortie :
    - Table IndicesCalcules
=========================================================
"""

from app import db
from app.config import*
from app.models.session_usinage import SessionUsinage
from app.models.indices_calcules import IndicesCalcules



class CalculIGSO:

    """
    =====================================================
    Calcul de l'Indice Global de Sollicitation Outil
    =====================================================
    """

    # =====================================================
    # OUTILS
    # =====================================================

    @staticmethod
    def _normaliser(valeur, minimum, maximum):
        """
        Ramène une grandeur entre 0 et 1.
        """

        if valeur is None:
            return 0.0

        if maximum <= minimum:
            return 0.0

        if valeur < minimum:
            valeur = minimum

        if valeur > maximum:
            valeur = maximum

        return (valeur - minimum) / (maximum - minimum)

    # =====================================================

    @staticmethod
    def _etat_to_score(etat):

        """
        Conversion des états S0→S4
        en score numérique.
        """

        table = {
            "S0": 0.00,
            "S1": 0.25,
            "S2": 0.50,
            "S3": 0.75,
            "S4": 1.00
        }

        if etat is None:
            return 0

        try:
            return table[etat.value]
        except Exception:
            return table.get(str(etat), 0)

    # =====================================================
    # INDICE MECANIQUE
    # =====================================================

    @staticmethod
    def _calcul_IM(session):

        """
        Calcul de la sollicitation mécanique.

        Variables :

            Vitesse coupe

            Avance

            Profondeur axiale

            Profondeur radiale

            Engagement
        """

        p = session.parametres_coupe

        vc = CalculIGSO._normaliser(
            p.vitesse_coupe,
            0,
            VC_MAX
        )

        avance = CalculIGSO._normaliser(
            p.avance_par_dent,
            0,
            FZ_MAX
        )

        ap = CalculIGSO._normaliser(
            p.profondeur_axiale,
            0,
            AP_MAX
        )

        ae = CalculIGSO._normaliser(
            p.profondeur_radiale,
            0,
            AE_MAX
        )

        engagement = CalculIGSO._normaliser(
            p.engagement,
            0,
            ENGAGEMENT_MAX
        )

        indice = (

            0.30 * vc +

            0.25 * avance +

            0.20 * ap +

            0.15 * ae +

            0.10 * engagement

        )

        return round(min(indice, 1.0), 4)
    # =====================================================
    # INDICE THERMIQUE
    # =====================================================

    @staticmethod
    def _calcul_IT(session):

        """
        Sollicitation thermique.

        Variables :
            - Temps de coupe
            - Vitesse de rotation
            - Conductivité matière
            - Lubrification
        """

        p = session.parametres_coupe
        matiere = session.matiere
        lubrifiant = session.lubrifiant

        temps = CalculIGSO._normaliser(
            p.temps_coupe,
            0,
            TEMPS_COUPE_MAX
        )

        rotation = CalculIGSO._normaliser(
            p.vitesse_rotation,
            0,
            VITESSE_ROTATION_MAX
        )

        conductivite = 0

        if matiere and matiere.conductivite_thermique:

            conductivite = 1 - CalculIGSO._normaliser(
                matiere.conductivite_thermique,
                0,
                250
            )

        refroidissement = 0

        if lubrifiant:

            refroidissement = 1 - max(
                0,
                min(
                    lubrifiant.coefficient_refroidissement,
                    1
                )
            )

        indice = (

            0.35 * temps +

            0.30 * rotation +

            0.20 * conductivite +

            0.15 * refroidissement

        )

        return round(min(indice, 1), 4)

    # =====================================================
    # INDICE MACHINE
    # =====================================================

    @staticmethod
    def _calcul_IMA(session):

        """
        Etat de la machine.
        """

        machine = session.machine

        if machine is None:

            return 0

        age = CalculIGSO._normaliser(

            getattr(machine, "age", 0),

            0,

            AGE_MACHINE_MAX

        )

        heures = CalculIGSO._normaliser(

            getattr(machine, "heures_fonctionnement", 0),

            0,

            HEURES_MACHINE_MAX

        )

        rigidite = getattr(machine, "rigidite", 1)

        rigidite = max(0, min(rigidite, 1))

        indice = (

            0.40 * age +

            0.40 * heures +

            0.20 * (1 - rigidite)

        )

        return round(min(indice, 1), 4)

    # =====================================================
    # INDICE HISTORIQUE
    # =====================================================

    @staticmethod
    def _calcul_IH(session):

        """
        Historique de l'outil.
        """

        outil = session.outil

        degats = CalculIGSO._normaliser(

            outil.degats_cumules,

            0,

            DEGATS_MAX

        )

        affutage = CalculIGSO._normaliser(

            outil.nb_affutages,

            0,

            AFFUTAGE_MAX

        )

        etat = CalculIGSO._etat_to_score(

            outil.etat_actuel

        )

        indice = (

            0.50 * degats +

            0.30 * affutage +

            0.20 * etat

        )

        return round(min(indice, 1), 4)

    # =====================================================
    # INDICE PROCEDE
    # =====================================================

    @staticmethod
    def _calcul_IP(session):

        """
        Complexité du procédé.
        """

        p = session.parametres_coupe

        passes = CalculIGSO._normaliser(

            p.nombre_passes,

            1,

            10

        )

        quantite = CalculIGSO._normaliser(

            session.quantite_fabriquee,

            0,

            1000

        )

        type_operation = 0.5

        if session.type_operation:

            nom = str(session.type_operation.nom)

            coefficients = {

                "SURFACAGE": 0.30,
                "FRAISAGE": 0.60,
                "CONTOURNAGE": 0.70,
                "RAINURAGE": 0.80,
                "PERCAGE": 0.50,
                "ALESAGE": 0.70,
                "TARAUDAGE": 0.90,
                "FILETAGE": 0.90,
                "POINTAGE": 0.30,
                "CHANFREINAGE": 0.40,
                "LAMAGE": 0.60,
                "POCHE": 0.80,
                "AUTRE": 0.50

            }

            type_operation = coefficients.get(
                nom,
                0.5
            )

        indice = (

            0.40 * passes +

            0.30 * quantite +

            0.30 * type_operation

        )

        return round(min(indice, 1), 4)
    # =====================================================
    # CALCUL GLOBAL IGSO
    # =====================================================

    @staticmethod
    def calculer_igso(session):

        """
        Calcul de l'Indice Global de Sollicitation Outil.
        """

        im = CalculIGSO._calcul_IM(session)

        it = CalculIGSO._calcul_IT(session)

        ima = CalculIGSO._calcul_IMA(session)

        ih = CalculIGSO._calcul_IH(session)

        ip = CalculIGSO._calcul_IP(session)

        igso = (

            POIDS_IM * im +

            POIDS_IT * it +

            POIDS_IMA * ima +

            POIDS_IH * ih +

            POIDS_IP * ip

        )

        igso = round(min(igso, 1.0), 4)

        return {

            "indice_mecanique": im,

            "indice_thermique": it,

            "indice_machine": ima,

            "indice_historique": ih,

            "indice_parametres": ip,

            "igso": igso

        }
    # =====================================================
    # SAUVEGARDE DES INDICES
    # =====================================================

    @staticmethod
    def enregistrer(session):

        """
        Calcule puis sauvegarde les indices.
        """

        resultats = CalculIGSO.calculer_igso(session)

        indice = session.indices

        if indice is None:

            indice = IndicesCalcules(
                session=session
            )

            db.session.add(indice)

        indice.indice_mecanique = resultats["indice_mecanique"]

        indice.indice_thermique = resultats["indice_thermique"]

        indice.indice_machine = resultats["indice_machine"]

        indice.indice_historique = resultats["indice_historique"]

        indice.indice_procede = resultats["indice_parametres"]

        indice.igso = resultats["igso"]

        db.session.commit()

        return indice

    # =====================================================
    # API PUBLIQUE
    # =====================================================

    def calculer(session_id):
        """
        Point d'entrée du pipeline IGSO.
        """

        session = SessionUsinage.query.get(session_id)

        if session is None:
            raise ValueError(
                f"Session {session_id} introuvable."
            )

        if session.parametres_coupe is None:
            raise ValueError(
                "Les paramètres de coupe sont absents."
            )

        return CalculIGSO.enregistrer(session)

    @staticmethod
    def _calcul_IH(session):
        """
        Calcul de l'indice historique de l'outil.
        """

        outil = session.outil

        if outil is None:
            return 0

        degats = CalculIGSO._normaliser(
            outil.degats_cumules,
            0,
            DEGATS_MAX
        )

        affutages = CalculIGSO._normaliser(
            outil.nb_affutages,
            0,
            AFFUTAGES_MAX
        )

        etat_scores = {
            "S0": 0.00,
            "S1": 0.25,
            "S2": 0.50,
            "S3": 0.75,
            "S4": 1.00
        }

        etat = etat_scores.get(
            outil.etat_actuel.value,
            0
        )

        indice = (

                POIDS_DEGATS * degats +

                POIDS_AFFUTAGE * affutages +

                POIDS_ETAT * etat

        )

        return round(min(indice, 1), 4)

    @staticmethod
    def _calcul_IP(session):

        """
        Calcul de l'indice des paramètres de coupe.
        Plus les paramètres sont agressifs,
        plus l'indice augmente.
        """

        param = session.parametres_coupe

        if param is None:
            return 0

        vc = CalculIGSO._normaliser(
            param.vitesse_coupe or 0,
            0,
            VC_MAX
        )

        avance = CalculIGSO._normaliser(
            param.avance or 0,
            0,
            AVANCE_MAX
        )

        ap = CalculIGSO._normaliser(
            param.profondeur_axiale or 0,
            0,
            AP_MAX
        )

        ae = CalculIGSO._normaliser(
            param.profondeur_radiale or 0,
            0,
            AE_MAX
        )

        temps = CalculIGSO._normaliser(
            param.temps_coupe or 0,
            0,
            TEMPS_COUPE_MAX
        )

        passes = CalculIGSO._normaliser(
            param.nombre_passes or 1,
            1,
            NB_PASSES_MAX
        )

        indice = (

                0.20 * vc +

                0.20 * avance +

                0.20 * ap +

                0.15 * ae +

                0.15 * temps +

                0.10 * passes

        )

        return round(min(indice, 1), 4)

    @staticmethod
    def calculer(session):
        """
        Calcule tous les indices de la session,
        calcule l'IGSO puis sauvegarde les résultats.
        """

        # ==========================
        # Calcul des indices
        # ==========================

        im = CalculIGSO._calcul_IM(session)

        it = CalculIGSO._calcul_IT(session)

        ima = CalculIGSO._calcul_IMA(session)

        ih = CalculIGSO._calcul_IH(session)

        ip = CalculIGSO._calcul_IP(session)

        # ==========================
        # Calcul IGSO
        # ==========================

        igso = (

                POIDS_IM * im +

                POIDS_IT * it +

                POIDS_IMA * ima +

                POIDS_IH * ih +

                POIDS_IP * ip

        )

        igso = round(min(igso, 1), 4)

        # ==========================
        # Sauvegarde
        # ==========================

        indice = IndicesCalcules.query.filter_by(
            session_id=session.id
        ).first()

        if indice is None:
            indice = IndicesCalcules(
                session_id=session.id
            )

            db.session.add(indice)

        indice.indice_mecanique = im
        indice.indice_thermique = it
        indice.indice_machine = ima
        indice.indice_historique = ih
        indice.indice_parametres = ip
        indice.igso = igso

        db.session.commit()

        # ==========================
        # Résultat
        # ==========================

        return indice
