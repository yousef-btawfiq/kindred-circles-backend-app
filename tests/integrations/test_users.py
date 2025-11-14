from app.models import User
from tests.conftest import USER_ENDPOINT_PREFIX


### HEALTHCHECK TESTS ###

def test_health_endpoint_returns_ok(client):
    resp = client.get(f"{USER_ENDPOINT_PREFIX}/healthcheck")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

### USER CREATION TESTS ###

def test_user_creation_endpoint(client, user_data):
    resp = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["email"] == user_data["email"]
    assert "user_id" in data and len(data["user_id"]) == 12

    user_rec = User.query.filter_by(user_id=data["user_id"]).one()

def test_duplicate_user_creation_fails(client, user_data):
    resp1 = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)
    data = resp1.get_json()
    assert resp1.status_code == 201

    resp2 = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)
    assert resp2.status_code == 400
    assert "error" in resp2.get_json()

    user_rec = User.query.filter_by(user_id=data["user_id"]).one()

def test_missing_required_params_fails(client):
    incomplete_data = {"first_name": "Alice"}
    resp = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=incomplete_data)
    assert resp.status_code == 400
    assert {"error" : "Missing required parameter: email"} == resp.get_json()

    assert User.query.filter_by(first_name="Alice").count() == 0 

### USER RETRIEVAL TESTS ###

def test_get_user_via_email(client, user_data):
    create_resp = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)
    assert create_resp.status_code == 201
    created_user = create_resp.get_json()

    user_response = client.get(f"{USER_ENDPOINT_PREFIX}/get?email={user_data['email']}")
    assert user_response.status_code == 200
    fetched_user_response = user_response.get_json()
    assert fetched_user_response == created_user

def test_missing_param_get_user_fails(client):
    resp = client.get(f"{USER_ENDPOINT_PREFIX}/get")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "Missing required parameter: email or user_id"}

def test_get_user_via_user_id(client, user_data):
    create_resp = client.post(f"{USER_ENDPOINT_PREFIX}/create", json=user_data)
    assert create_resp.status_code == 201
    created_user = create_resp.get_json()

    user_response = client.get(f"{USER_ENDPOINT_PREFIX}/get?user_id={created_user['user_id']}")
    assert user_response.status_code == 200
    fetched_user_response = user_response.get_json()
    assert fetched_user_response == created_user