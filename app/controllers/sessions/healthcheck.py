from . import sessions_bp
from flask import jsonify

@sessions_bp.route("/healthcheck", methods=["GET"])
def healthcheck():  
    return jsonify({"status": "ok"}), 200



