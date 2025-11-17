from . import sessions_bp
from flask import jsonify, request
from app.models import Session, db

@sessions_bp.route("/get/<session_id>", methods=["GET"])    
def get_session(session_id): 
    session = Session.query.filter_by(session_id=session_id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    return jsonify(session.to_dict()), 200

@sessions_bp.route("/list", methods=["GET"])
def list_sessions_via_status():
    status = request.args.get("status") 
    if not status:
        return jsonify({"error": "Missing required parameter: status"}), 400
    sessions = Session.query.filter_by(status=status).all()
    sessions_list = [session.to_dict() for session in sessions]
    return jsonify(sessions_list), 200  



