from . import sessions_bp
from flask import jsonify, request
from app.models import Session, db


required_params = ["start_time", "duration", "audio_only"]

@sessions_bp.route("/create", methods=["POST"])
def create_session():
    session_data = request.get_json(force=True)

    for param in required_params:
        if param not in session_data:
            return jsonify({"error": f"Missing required parameter: {param}"}), 400

    new_session = Session.from_dict(session_data)

    try:
        db.session.add(new_session)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(new_session.to_dict()), 201