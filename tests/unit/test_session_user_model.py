from app.models import Session, SessionUser

def test_session_from_dict_creates_session(session_user_data):
    session_user = SessionUser.from_dict(
        user_id=session_user_data['user_id'],
        session_id=session_user_data['session_id'],
    )
    assert session_user.session_id == session_user_data['session_id']
    assert session_user.user_id == session_user_data['user_id']
    assert session_user.confirmed == False
    assert session_user.status == "registered"
