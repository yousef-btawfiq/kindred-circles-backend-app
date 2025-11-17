from . import sessions_bp
from flask import jsonify, request 
from app.models import Session, db, SessionUser


@sessions_bp.route("/<session_id>/add_user", methods=["POST"])
def add_session_user(session_id):  
    session = Session.query.filter_by(session_id=session_id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    user_data = request.get_json(force=True)
    user_id = user_data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400

    new_session_user = SessionUser.from_dict(
        user_id=user_id,
        session_id=session_id
    )

    try:
        db.session.add(new_session_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(new_session_user.to_dict()), 201