from flask import Blueprint
from flask import jsonify

from app.pipeline.calcul_global import CalculGlobal


calcul_bp = Blueprint(
    "calcul",
    __name__,
    url_prefix="/api/calcul"
)


# ======================================================
# Calcul complet d'une session
# ======================================================

@calcul_bp.route(
    "/session/<int:session_id>",
    methods=["POST"]
)
def calculer_session(session_id):

    try:

        resultat = CalculGlobal.executer(
            session_id
        )

        return jsonify({

            "success": True,

            "message": "Calcul terminé avec succès.",

            "resultat": resultat

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# ======================================================
# Test API
# ======================================================

@calcul_bp.route(
    "/test",
    methods=["GET"]
)
def test():

    return jsonify({

        "success": True,

        "message": "API Damage Engine opérationnelle."

    })