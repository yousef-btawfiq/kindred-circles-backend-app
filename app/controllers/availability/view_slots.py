from . import availability_bp
from flask import request, jsonify
import json


@availability_bp.route("/slots", methods=["GET"])
def list_slots():
    with open("app/models/slots.json") as f:
        slots = json.load(f)
    return jsonify(slots), 200 
