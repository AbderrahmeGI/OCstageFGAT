# app/config.py

# ======================================================
# POIDS DES INDICES
# ======================================================

POIDS_INDICE_MECANIQUE = 0.30
POIDS_INDICE_THERMIQUE = 0.25
POIDS_INDICE_MACHINE = 0.15
POIDS_INDICE_HISTORIQUE = 0.20
POIDS_INDICE_PARAMETRES = 0.10


# ======================================================
# COEFFICIENTS MECANIQUES
# ======================================================

COEF_VITESSE_COUPE = 0.30
COEF_AVANCE = 0.25
COEF_PROFONDEUR = 0.25
COEF_ENGAGEMENT = 0.20


# ======================================================
# COEFFICIENTS THERMIQUES
# ======================================================

COEF_CONDUCTIVITE = 0.40
COEF_REFROIDISSEMENT = 0.35
COEF_LUBRIFICATION = 0.25


# ======================================================
# COEFFICIENTS MACHINE
# ======================================================

COEF_AGE_MACHINE = 0.30
COEF_RIGIDITE = 0.40
COEF_VIBRATION = 0.30


# ======================================================
# COEFFICIENTS HISTORIQUE
# ======================================================

COEF_USURE = 0.40
COEF_AFFUTAGES = 0.30
COEF_REBUT = 0.30


# ======================================================
# ETATS
# ======================================================

SEUIL_S0 = 20
SEUIL_S1 = 40
SEUIL_S2 = 60
SEUIL_S3 = 80
SEUIL_S4 = 100
# =====================================================
# LIMITES DE NORMALISATION
# =====================================================

VC_MAX = 400

FZ_MAX = 0.30

AP_MAX = 20

AE_MAX = 20

ENGAGEMENT_MAX = 100

TEMPS_COUPE_MAX = 240

VITESSE_ROTATION_MAX = 24000

AGE_MACHINE_MAX = 20

HEURES_MACHINE_MAX = 60000

AFFUTAGE_MAX = 15

DEGATS_MAX = 100


# =====================================================
# POIDS IGSO
# =====================================================

POIDS_IM = 0.30

POIDS_IT = 0.25

POIDS_IMA = 0.15

POIDS_IH = 0.20

POIDS_IP = 0.10
# =====================================
# Historique
# =====================================

DEGATS_MAX = 100

AFFUTAGES_MAX = 10

POIDS_DEGATS = 0.50

POIDS_AFFUTAGE = 0.30

POIDS_ETAT = 0.20
# ==================================================
# PARAMETRES DE COUPE
# ==================================================

VC_MAX = 300              # m/min

AVANCE_MAX = 1000         # mm/min

AP_MAX = 20               # mm

AE_MAX = 20               # mm

TEMPS_COUPE_MAX = 240     # minutes

NB_PASSES_MAX = 20