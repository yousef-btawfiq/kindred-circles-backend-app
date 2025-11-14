from tests.conftest import TOPICS_ENDPOINT_PREFIX



def test_health_endpoint_returns_ok(client):    
    resp = client.get(f"{TOPICS_ENDPOINT_PREFIX}/healthcheck")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_list_topics_endpoint_returns_topics(client):
    resp = client.get(f"{TOPICS_ENDPOINT_PREFIX}/list")
    assert resp.status_code == 200
    topics = resp.get_json()
    assert isinstance(topics, dict)
    assert "work_life_emptiness" in topics.keys()
    assert "small_joys" in topics.keys()

def test_get_topic_endpoint_returns_specific_topic(client):
    resp = client.get(f"{TOPICS_ENDPOINT_PREFIX}/get/work_life_emptiness")
    assert resp.status_code == 200
    topic = resp.get_json()
    assert {"work_life_emptiness" : "Work-Life Emptiness"} == topic