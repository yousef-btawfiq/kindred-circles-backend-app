from datetime import datetime
from app.models import db 
from app.utils import generate_alphanumeric_id
from sqlalchemy import event 
import json

SESSION_STATUS_ACTIVE = "in_progress"
SESSION_STATUS_COMPLETED = "completed"
SESSION_STATUS_SCHEDULED = "scheduled"
SESSION_STATUS_CANCELED = "canceled"
VALID_SESSION_STATUSES = [
    SESSION_STATUS_ACTIVE,
    SESSION_STATUS_COMPLETED,
    SESSION_STATUS_SCHEDULED,
    SESSION_STATUS_CANCELED
]


class Session(db.Model):
    __tablename__ = 'sessions'   

    session_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False, default=generate_alphanumeric_id)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    room_name = db.Column(db.String(12), unique=True, nullable=True)
    audio_only = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="scheduled")  # e.g., 'scheduled', 'in_progress', 'completed', 'canceled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
            "room_name": self.room_name,
            "audio_only": self.audio_only,  
            "status": self.status,  
            "created_at": self.created_at.isoformat()
        }  

    @classmethod
    def from_dict(cls, data):
        return cls(
            start_time=datetime.fromisoformat(data.get('start_time')),
            duration=data.get('duration'),
            audio_only=data.get('audio_only', False), 
            status=SESSION_STATUS_SCHEDULED
        )


@event.listens_for(Session, 'after_insert')    
def generate_room_name(mapper, connection, session):
    room_name = f"room_{session.session_id}"
    connection.execute(
        Session.__table__.update()
        .where(Session.session_id == session.session_id)
        .values(room_name=room_name)
    ) 