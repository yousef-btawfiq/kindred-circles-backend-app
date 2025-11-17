from app.models import Session
from tests.conftest import TIMEFREEZE
from freezegun import freeze_time  
from datetime import datetime 

@freeze_time(TIMEFREEZE)
def test_session_from_dict_creates_session(session_data):
    session = Session.from_dict(session_data)
    assert session.start_time == datetime.fromisoformat("2025-01-01T09:00:00")
    assert session.duration == 60
    assert session.audio_only == False
    assert session.status == "scheduled"





