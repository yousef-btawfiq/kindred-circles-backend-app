import pytest 
from app import create_app  
from app.models import db, User
from datetime import datetime
from freezegun import freeze_time   

TIMEFREEZE = "2025-01-01 00:00:00"

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
        "first_name" : "Yousef"
    }

@pytest.fixture
def preferences_data(): 
    return {
            "camera_ok": True,
            "topics": ["social_anxiety", "making_friends_as_adult", "comparison"],
        }

@pytest.fixture
@freeze_time(TIMEFREEZE)
def user_obj(user_data): 
    user = User.from_dict(user_data)
    user.user_id = "user123"
    user.created_at = datetime.now()
    return user 