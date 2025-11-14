from . import availability_bp
from flask import jsonify   



@availability_bp.route("/healthcheck", methods=["GET"])
def healthcheck():  
    return jsonify({"status": "ok"}), 200