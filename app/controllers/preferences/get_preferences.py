from . import preferences_bp  
from app.models import User, Preferences, Availability
from flask import request, jsonify

required_params = ["user_id"] 
    
@preferences_bp.route("/get", methods=["GET"])
def get_preferences_via_user_id():
    if request.args.get("user_id"): 
        user_id = request.args.get("user_id")
        prefs = Preferences.query.filter_by(user_id=user_id).first()
    else:
        return {"error": "Missing required parameter: user_id"}, 400  

    return prefs.to_dict() if prefs else ({"error": f"Preferences not found for user with id {user_id}"}, 404)