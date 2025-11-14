from app.models import Preferences
from tests.conftest import PREF_ENDPOINT_PREFIX, USER_ENDPOINT_PREFIX
import json


### HEALTHCHECK TESTS ###

def test_health_endpoint_returns_ok(client):
    resp = client.get(f"{PREF_ENDPOINT_PREFIX}/healthcheck")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

### CREATE PREFERENCES TESTS ###

def test_add_preferences_endpoint(client, user_data, preferences_data):
    user = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data) 
    user_id = user.get_json()["user_id"]
    resp = client.post(f"{PREF_ENDPOINT_PREFIX}/{user_id}/add", json=preferences_data)
    
    preferences = Preferences.query.filter_by(user_id=user_id).one()
    assert preferences.camera_ok == preferences_data["camera_ok"]
    assert json.loads(preferences.topics) == preferences_data["topics"]
    assert resp.status_code == 201
    assert resp.get_json()["message"] == f"Preferences created for user {user_id}"

def test_add_preferences_no_user_found(client, preferences_data):
    resp = client.post(f"{PREF_ENDPOINT_PREFIX}/NotRealID/add", json=preferences_data)
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "User not found"}

def test_add_preferences_already_exists_fails(client, user_data, preferences_data):
    user = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data) 
    user_id = user.get_json()["user_id"]

    resp1 = client.post(f"{PREF_ENDPOINT_PREFIX}/{user_id}/add", json=preferences_data)
    assert resp1.status_code == 201

    resp2 = client.post(f"{PREF_ENDPOINT_PREFIX}/{user_id}/add", json=preferences_data)
    assert resp2.status_code == 400
    assert resp2.get_json() == {"error": "Preferences already exist for this user"} 

def test_add_preferences_missing_required_param_fails(client, user_data):
    user = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data) 
    user_id = user.get_json()["user_id"]

    incomplete_prefs = {"camera_ok": True}  
    resp = client.post(f"{PREF_ENDPOINT_PREFIX}/{user_id}/add", json=incomplete_prefs)
    assert resp.status_code == 400
    assert f"Missing required parameter: topics" == resp.get_json()["error"]
