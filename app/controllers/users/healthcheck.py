from . import users_bp
from flask import jsonify




@users_bp.route("/healthcheck", methods=["GET"])
def healthcheck():  
    return jsonify({"status": "ok"}), 200