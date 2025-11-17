from tests.conftest import SESSION_ENDPOINT_PREFIX
from app.models import Session
from freezegun import freeze_time   

### Healthcheck Tests ### 


def test_health_endpoint_returns_ok(client):
    resp = client.get(f"{SESSION_ENDPOINT_PREFIX}/healthcheck")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

### Create Session Tests ###   


def test_session_create_endpoint(client, session_data): 
    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data)
    assert resp.status_code == 201
    session_json = resp.get_json()
    assert "session_id" in session_json
    assert session_json["start_time"] == "2025-01-01T09:00:00"
    assert session_json["duration"] == 60 
    assert session_json["status"] == "scheduled"
    assert session_json["audio_only"] == False 
    
    #Check room id is auto generated correctly
    assert session_json["room_name"] == f"room_{session_json['session_id']}"

    #Check session is in DB
    user_rec = Session.query.filter_by(session_id=session_json["session_id"]).one()

def test_session_create_missing_required_param_fails(client, session_data):
    del session_data["start_time"]
    resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data)
    assert resp.status_code == 400
    assert f"Missing required parameter: start_time" == resp.get_json()["error"]   

### Get Session Tests ###   

def test_get_session_via_session_id(client, session_data):
    create_resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data)
    assert create_resp.status_code == 201
    created_session = create_resp.get_json()
    session_id = created_session["session_id"]

    session_response = client.get(f"{SESSION_ENDPOINT_PREFIX}/get/{session_id}")
    assert session_response.status_code == 200
    fetched_session_response = session_response.get_json()
    assert fetched_session_response == created_session  


def test_get_session_invalid_session_id_fails(client):
    resp = client.get(f"{SESSION_ENDPOINT_PREFIX}/get/NotARealSessionID")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "Session not found"}    


### List Sessions via Status Tests ###

def test_list_sessions_via_status(client, session_data):    
    #Create multiple sessions with different statuses
    session_data_1 = session_data.copy()
    session_data_2 = session_data.copy()
    session_data_3 = session_data.copy()


    resp1 = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data_1)
    resp2 = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data_2)
    resp3 = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data_3)

    session_id_1 = resp1.get_json()["session_id"]
    session_id_2 = resp2.get_json()["session_id"]
    session_id_3 = resp3.get_json()["session_id"]

    #Manually update statuses in DB for testing
    session_rec_1 = Session.query.filter_by(session_id=session_id_1).one()
    session_rec_2 = Session.query.filter_by(session_id=session_id_2).one()
    session_rec_3 = Session.query.filter_by(session_id=session_id_3).one()

    session_rec_1.status = "scheduled"
    session_rec_2.status = "in_progress"
    session_rec_3.status = "completed"

    from app import db
    db.session.commit()

    #Fetch sessions with status 'scheduled'
    list_resp = client.get(f"{SESSION_ENDPOINT_PREFIX}/list?status=scheduled")
    assert list_resp.status_code == 200
    sessions_list = list_resp.get_json()
    assert len(sessions_list) == 1
    assert sessions_list[0]["session_id"] == session_id_1

def test_list_sessions_missing_status_param_fails(client):
    resp = client.get(f"{SESSION_ENDPOINT_PREFIX}/list")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "Missing required parameter: status"}


### Update session status ###

def test_update_session_status(client, session_data):
    create_resp = client.post(f"{SESSION_ENDPOINT_PREFIX}/create", json=session_data)
    assert create_resp.status_code == 201
    created_session = create_resp.get_json()
    session_id = created_session["session_id"]

    #Update status to 'in_progress'
    update_resp = client.put(f"{SESSION_ENDPOINT_PREFIX}/update/{session_id}/in_progress")
    assert update_resp.status_code == 200
    created_session["status"] = "in_progress"
    assert update_resp.get_json() == created_session

    #Verify update
    get_resp = client.get(f"{SESSION_ENDPOINT_PREFIX}/get/{session_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["status"] == "in_progress"