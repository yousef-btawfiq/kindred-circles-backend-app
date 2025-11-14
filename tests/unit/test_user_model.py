from freezegun import freeze_time
from app.models import User 
from datetime import datetime
from tests.conftest import TIMEFREEZE



@freeze_time(TIMEFREEZE)
def test_user_from_dict_creates_user(user_data, user_obj):
    user = User.from_dict(user_data)
    user.user_id = "user123"
    user.created_at = datetime.now()
    assert user.to_dict() == user_obj.to_dict() 