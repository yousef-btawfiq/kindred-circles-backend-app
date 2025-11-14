from tests.conftest import AVAILABILITY_ENDPOINT_PREFIX


### HEALTHCHECK TESTS ###

def test_health_endpoint_returns_ok(client):
    resp = client.get(f"{AVAILABILITY_ENDPOINT_PREFIX}/healthcheck")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_slot_endpoint_returns_200(client):
    resp = client.get(f"{AVAILABILITY_ENDPOINT_PREFIX}/slots")
    assert resp.status_code == 200 

### ADD AVAILABILITY TESTS ###

def test_add_availability_endpoint(client, user_data, availability_data):
    user = client.post(f"/api/v1/users/create", json=user_data) 
    user_id = user.get_json()["user_id"]
    resp = client.post(f"{AVAILABILITY_ENDPOINT_PREFIX}/{user_id}/add", json=availability_data)
    
    assert resp.status_code == 201
    assert resp.get_json()["message"] == f"Availability added for user {user_id}"

def test_add_availability_no_user_found(client, availability_data):
    resp = client.post(f"{AVAILABILITY_ENDPOINT_PREFIX}/NotRealID/add", json=availability_data)
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "User not found"}

def test_add_availability_missing_required_param_fails(client, user_data):
    user = client.post(f"/api/v1/users/create", json=user_data) 
    user_id = user.get_json()["user_id"]

    incomplete_availability = {}  
    resp = client.post(f"{AVAILABILITY_ENDPOINT_PREFIX}/{user_id}/add", json=incomplete_availability)
    assert resp.status_code == 400
    assert f"Missing required parameter: slot_ids" == resp.get_json()["error"]