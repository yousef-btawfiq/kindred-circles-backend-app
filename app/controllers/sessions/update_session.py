from . import sessions_bp
from flask import jsonify, request
from app.models import Session, db
from app.models.session import VALID_SESSION_STATUSES  


@sessions_bp.route("/update/<session_id>/<status>", methods=["PUT"])
def update_session_status(session_id, status):
    session = Session.query.filter_by(session_id=session_id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    if status not in VALID_SESSION_STATUSES:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    session.status = status

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(session.to_dict()), 200