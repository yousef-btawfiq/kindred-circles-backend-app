from . import availability_bp  
from app.models import User, Preferences, Availability
from flask import request, jsonify

required_params = ["user_id"] 
    
@availability_bp.route("/get", methods=["GET"])
def get_availability_via_user_id():
    if request.args.get("user_id"): 
        user_id = request.args.get("user_id")
        slots = Availability.query.filter_by(user_id=user_id).first()
    else:
        return {"error": "Missing required parameter: user_id"}, 400  

    return slots.to_dict() if slots else ({"error": f"Availability not found for user with id {user_id}"}, 404)