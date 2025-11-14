from . import topics_bp
from flask import jsonify

@topics_bp.route("/healthcheck", methods=["GET"])
def healthcheck():  
    return jsonify({"status": "ok"}), 200