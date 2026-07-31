from datetime import datetime, date

from run import app
from app import db

from app.models.utilisateur import Utilisateur, RoleUtilisateur
from app.models.machine import Machine
from app.models.type_outil import TypeOutil, CategorieOutil
from app.models.outil import Outil
from app.models.matiere import Matiere
from app.models.lubrifiant import Lubrifiant
from app.models.type_operation import TypeOperation, NomOperation
from app.models.affectation import Affectation
from app.models.session_usinage import SessionUsinage
from app.models.parametres_coupe import ParametresCoupe
with app.app_context():
    utilisateur = Utilisateur.query.filter_by(
        email="admin@ocfga.com"
    ).first()

    if utilisateur is None:

        utilisateur = Utilisateur(

            nom="Jawedi",

            prenom="Abderrahmen",

            email="admin@ocfga.com",

            role=RoleUtilisateur.ADMIN

        )

        utilisateur.set_password("123456")

        db.session.add(utilisateur)

        db.session.commit()

    print("Utilisateur :", utilisateur.id)
    machine = Machine.query.filter_by(
        code="DMU60"
    ).first()

    if machine is None:

        machine = Machine(

            code="DMU60",

            nom="DMU 60",

            type_machine="Centre Usinage 5 Axes",

            constructeur="DMG MORI",

            modele="DMU60",

            nb_axes=5,

            age=4,

            heures_fonctionnement=6500,

            rigidite=0.92,

            puissance_kw=28,

            vitesse_max_broche=18000,

            precision_mm=0.005,


        )

        db.session.add(machine)

        db.session.commit()

    print("Machine :", machine.id)
    type_outil = TypeOutil.query.filter_by(
        reference="FRAISE10"
    ).first()

    if type_outil is None:

        type_outil = TypeOutil(

            reference="FRAISE10",

            designation="Fraise carbure Ø10",

            fabricant="Sandvik",

            categorie=CategorieOutil.FRAISE,

            diametre=10,

            nb_dents=4,

            matiere="Carbure",

            revetement="TiAlN",

            angle_helice=35

        )

        db.session.add(type_outil)

        db.session.commit()

    print("Type outil :", type_outil.id)
    outil = Outil.query.filter_by(
        code="OUTIL001"
    ).first()

    if outil is None:

        outil = Outil(

            code="OUTIL001",

            numero_serie="SN001",

            type_outil_id=type_outil.id,

            date_mise_service=date.today(),

            nb_affutages=0,

            degats_cumules=0

        )

        db.session.add(outil)

        db.session.commit()

    print("Outil :", outil.id)
    matiere = Matiere.query.filter_by(
        nom="Aluminium 7075"
    ).first()

    if matiere is None:

        matiere = Matiere(

            nom="Aluminium 7075",

            famille="ALUMINIUM",

            durete_hb=150,

            usinabilite=0.90,

            conductivite_thermique=130,

            densite=2.81,

            description="Alliage aéronautique"

        )

        db.session.add(matiere)

        db.session.commit()

    print("Matière :", matiere.id)
    lubrifiant = Lubrifiant.query.filter_by(
        nom="Blaser Vasco"
    ).first()

    if lubrifiant is None:

        lubrifiant = Lubrifiant(

            nom="Blaser Vasco",

            type="Emulsion",

            concentration=8,

            debit=25,

            pression=18,

            coefficient_refroidissement=0.92,

            coefficient_lubrification=0.88,

            description="Lubrifiant de démonstration"

        )

        db.session.add(lubrifiant)

        db.session.commit()

    print("Lubrifiant :", lubrifiant.id)
    type_operation = TypeOperation.query.filter_by(
        nom=NomOperation.FRAISAGE
    ).first()

    if type_operation is None:

        type_operation = TypeOperation(

            nom=NomOperation.FRAISAGE,

            description="Usinage par fraisage"

        )

        db.session.add(type_operation)

        db.session.commit()

    print("Type opération :", type_operation.id)
    affectation = Affectation.query.filter_by(

        outil_id=outil.id,

        machine_id=machine.id,

        actif=True

    ).first()

    if affectation is None:

        affectation = Affectation(

            outil_id=outil.id,

            machine_id=machine.id,

            poste="Centre 5 axes",

            commentaire="Affectation de démonstration"

        )

        db.session.add(affectation)

        db.session.commit()

    print("Affectation :", affectation.id)
    session = SessionUsinage.query.first()

    if session is None:

        session = SessionUsinage(

            date_debut=datetime.now(),

            outil_id=outil.id,

            machine_id=machine.id,

            matiere_id=matiere.id,

            lubrifiant_id=lubrifiant.id,

            type_operation_id=type_operation.id,

            operateur_id=utilisateur.id,

            numero_of="OF2026001",

            numero_phase="10",

            commentaire="Session de démonstration",

            quantite_fabriquee=100,

            quantite_rebut=3,

            validee=True

        )

        db.session.add(session)

        db.session.commit()

    print("Session :", session.id)
    parametres = ParametresCoupe.query.filter_by(
        session_id=session.id
    ).first()

    if parametres is None:

        parametres = ParametresCoupe(

            session_id=session.id,

            vitesse_coupe=240,

            vitesse_rotation=7500,

            avance=1200,

            avance_par_dent=0.08,

            profondeur_axiale=6,

            profondeur_radiale=2,

            largeur_usinage=10,

            longueur_usinage=250,

            nombre_passes=2,

            temps_coupe=12,

            engagement=0.45,

            observations="Paramètres de démonstration"

        )

        db.session.add(parametres)

        db.session.commit()

    print("Paramètres :", parametres.id)
    print()

    print("=" * 60)
    print("DEMO INSÉRÉE AVEC SUCCÈS")
    print("=" * 60)

    print(f"Utilisateur : {utilisateur.id}")
    print(f"Machine     : {machine.id}")
    print(f"Outil       : {outil.id}")
    print(f"Session     : {session.id}")