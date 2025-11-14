from . import preferences_bp  
from flask import jsonify, request
from app.models import db, User, Preferences
from sqlalchemy.orm.exc import NoResultFound

required_params = ["camera_ok", "topics"]

@preferences_bp.route("/<user_id>/add", methods=["POST"])
def create_user_preferences(user_id):
    data = request.get_json(force=True) 

    for param in required_params:
        if param not in data:
            return {"error": f"Missing required parameter: {param}"}, 400
    # Verify User ID presence
    try:
        User.query.filter_by(user_id=user_id).one()
    except NoResultFound:
        return {"error": "User not found"}, 404 
    
    # Only one preferences entry per user
    try:
        existing_prefs = Preferences.query.filter_by(user_id=user_id).one()
        if existing_prefs:
            return {"error": "Preferences already exist for this user"}, 400
    except NoResultFound:
        print("No existing preferences found, proceeding to create new one.")
    
    try: 
        prefs = Preferences.from_dict(user_id, data)
    except ValueError as ve:
        return {"error": str(ve)}, 400  
    

    try:
        db.session.add(prefs)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400   

    return {"message": f"Preferences created for user {user_id}"}, 201