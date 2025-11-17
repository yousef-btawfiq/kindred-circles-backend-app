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


### GET SLOTS TESTS ### 

def test_get_availability_via_user_id(client, user_data, availability_data):
    user = client.post(f"/api/v1/users/create", json=user_data) 
    user_id = user.get_json()["user_id"]

    client.post(f"{AVAILABILITY_ENDPOINT_PREFIX}/{user_id}/add", json=availability_data)

    avail_response = client.get(f"{AVAILABILITY_ENDPOINT_PREFIX}/get?user_id={user_id}")
    assert avail_response.status_code == 200
    fetched_avail_response = avail_response.get_json()
    assert fetched_avail_response["user_id"] == user_id
    assert fetched_avail_response["slot_ids"] == availability_data["slot_ids"]

def test_missing_param_get_availability_fails(client):
    resp = client.get(f"{AVAILABILITY_ENDPOINT_PREFIX}/get")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "Missing required parameter: user_id"}  