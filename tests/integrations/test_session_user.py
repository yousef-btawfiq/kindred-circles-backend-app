from tests.conftest import SESSION_ENDPOINT_PREFIX, USER_ENDPOINT_PREFIX
from app.models import Session
from app.models.session_user import STATUS_REGSITERED, STATUS_ATTENDED, STATUS_NOSHOW
from freezegun import freeze_time   

def test_add_session_user_endpoint(client, user_data, session_data):
    #Create User 
    resp = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)   
    assert resp.status_code == 201
    created_user = resp.get_json()

    #Create Session
    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data)
    assert resp.status_code == 201
    created_session = resp.get_json()


    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/{created_session['session_id']}/add_user", json={"user_id" : created_user["user_id"]})
    added_session_user = resp.get_json()

    assert resp.status_code == 201
    assert added_session_user["user_id"] == created_user["user_id"]
    assert added_session_user["session_id"] == created_session["session_id"]
    assert added_session_user["status"] == STATUS_REGSITERED      
    assert added_session_user["confirmed"] is False
    
def test_add_session_user_endpoint_missing_user_id(client, session_data):
    #Create Session
    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data)
    assert resp.status_code == 201
    created_session = resp.get_json()

    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/{created_session['session_id']}/add_user", json={})
    assert resp.status_code == 400
    error_response = resp.get_json()
    assert "Missing required parameter: user_id" in error_response["error"]

def test_add_session_user_endpoint_session_not_found(client, user_data):
    #Create User 
    resp = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)   
    assert resp.status_code == 201
    created_user = resp.get_json()

    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/nonexistent_session/add_user", json={"user_id" : created_user["user_id"]})
    assert resp.status_code == 404
    error_response = resp.get_json()
    assert "Session not found" in error_response["error"]