from . import users_bp  
from app.models import User
from flask import request 

required_params = ["email"] 

@users_bp.route("/get", methods=["GET"])
def get_user_via_email():
    if request.args.get("email"): 
        email = request.args.get("email")
        user = User.query.filter_by(email=email).first()
    elif request.args.get("user_id"): 
        user_id = request.args.get("user_id")
        user = User.query.filter_by(user_id=user_id).first()
    else:
        return {"error": "Missing required parameter: email or user_id"}, 400  
    
    return user.to_dict() if user else ({"error": "User not found"}, 404)