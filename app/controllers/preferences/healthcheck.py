from . import preferences_bp
from flask import jsonify   



@preferences_bp.route("/healthcheck", methods=["GET"])
def healthcheck():  
    return jsonify({"status": "ok"}), 200