import pytest 
from app.models import Preferences
import json

def test_from_dict_creates_preferences(preferences_data):
    prefs = Preferences.from_dict("testuser", preferences_data)

    assert prefs.user_id == "testuser"
    assert prefs.camera_ok == preferences_data["camera_ok"]
    assert json.loads(prefs.topics) == preferences_data["topics"]

def test_validate_camera_ok_not_bool(preferences_data):
    preferences_data["camera_ok"] = "yes"

    with pytest.raises(ValueError) as ve:
        Preferences.from_dict("testuser", preferences_data)
    assert str(ve.value) == "camera_ok must be a boolean value."

def test_topics_not_a_list(preferences_data):
    preferences_data["topics"] = "social_anxiety"

    with pytest.raises(ValueError) as ve:
        Preferences.from_dict("testuser", preferences_data)
    assert str(ve.value) == "Topics must be a list."

def test_topics_too_few(preferences_data): 
    preferences_data["topics"] = ["social_anxiety", "making_friends_as_adult"]

    with pytest.raises(ValueError) as ve:
        Preferences.from_dict("testuser", preferences_data)
    assert str(ve.value) == "You must select a minimum of 3 topics."

def test_topics_too_many(preferences_data):
    preferences_data["topics"] = ["social_anxiety", "making_friends_as_adult", "comparison", "self_esteem", "work_stress", "time_management"]

    with pytest.raises(ValueError) as ve:
        Preferences.from_dict("testuser", preferences_data)
    assert str(ve.value) == "You can select a maximum of 5 topics."

def test_topics_invalid_identifier(preferences_data):   
    preferences_data["topics"] = ["social_anxiety", "making_friends_as_adult", "invalid_topic"]

    with pytest.raises(ValueError) as ve:
        Preferences.from_dict("testuser", preferences_data)
    assert str(ve.value) == "Invalid topic identifier: invalid_topic"
