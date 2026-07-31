from app import create_app
from app.pipeline.calcul_global import CalculGlobal

# Initialisation de l'application Flask
app = create_app()

with app.app_context():
    print("🚀 Lancement du test du calcul global pour la session 1...")

    try:
        # Exécution du pipeline de calcul
        resultat = CalculGlobal.executer(1)

        print("\n=================================")
        print("✅ CALCUL EFFECTUÉ AVEC SUCCÈS")
        print("=================================")
        print(f"Session ID  : {resultat['session']}")
        print(f"IGSO        : {resultat['igso']}")
        print(f"Dégât (%)   : {resultat['degat']:.2f}%")
        print(f"Cumul (%)   : {resultat['cumul']:.2f}%")
        print(f"Nouvel État : {resultat['etat']}")
        print("=================================\n")

    except Exception as e:
        print(f"\n❌ ERREUR lors du calcul : {e}\n")