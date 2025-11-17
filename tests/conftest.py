import pytest 
from app import create_app  
from app.models import db, User
from datetime import datetime
from freezegun import freeze_time   

TIMEFREEZE = "2025-01-01 00:00:00"
AVAILABILITY_ENDPOINT_PREFIX = "/api/v1/availability"
USER_ENDPOINT_PREFIX = "/api/v1/users"
PREF_ENDPOINT_PREFIX = "/api/v1/prefs"
TOPICS_ENDPOINT_PREFIX = "/api/v1/topics"
SESSION_ENDPOINT_PREFIX = "/api/v1/sessions"

@pytest.fixture
def app():
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(config)

    with app.app_context():
        yield app   

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_data(): 
    return {
        "email" : "test@test.com",
        "age" : 29, 
        "gender" : "male",
        "first_name" : "Yousef"
    }

@pytest.fixture
@freeze_time(TIMEFREEZE)
def user_obj(user_data): 
    user = User.from_dict(user_data)
    user.user_id = "user123"
    user.created_at = datetime.now()
    return user 

@pytest.fixture
def preferences_data(): 
    return {
            "camera_ok": True,
            "topics": ["social_anxiety", "making_friends_as_adult", "overthinking"],
        }

@pytest.fixture
def availability_data(): 
    return {
        "user_id": "user123",
        "slot_ids" : [1, 2, 4, 7]
    }

@pytest.fixture
@freeze_time(TIMEFREEZE)
def session_data():
    return {
        "start_time": "2025-01-01T09:00:00",
        "duration": 60,
        "room_name": "room123",
        "audio_only": False
    }

@pytest.fixture
def session_user_data():
    return {
        "session_id": "session123",
        "user_id": "user123",
    }
