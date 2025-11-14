from . import availability_bp
from flask import request, jsonify
from app.models import Availability, User, db 
from sqlalchemy.orm.exc import NoResultFound

required_params = ["slot_ids"]

@availability_bp.route("/<user_id>/add", methods=["POST"])
def add_availability(user_id):
    data = request.get_json(force=True) 

    for param in required_params:
        if param not in data:
            return {"error": f"Missing required parameter: {param}"}, 400

    try:
        User.query.filter_by(user_id=user_id).one()
    except NoResultFound:
        return {"error": "User not found"}, 404 
    

    slots = Availability.from_dict(user_id, data)

    try:
        db.session.add(slots)
        db.session.commit() 
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
    
    return {"message" : f"Availability added for user {user_id}"}, 201

    