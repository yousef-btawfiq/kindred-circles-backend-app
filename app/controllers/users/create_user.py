from . import users_bp
from flask import jsonify, request
from app.models import db, User


required_params = ["email", "first_name"]

@users_bp.route("/create", methods=["POST"])
def create_user():


    user_data = request.get_json(force=True)

    for param in required_params:
        if param not in user_data:
            return jsonify({"error": f"Missing required parameter: {param}"}), 400

    user_data = User.from_dict(user_data)

    try: 
        db.session.add(user_data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(user_data.to_dict()), 201