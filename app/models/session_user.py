from app.models import db 


STATUS_REGSITERED = "registered"
STATUS_ATTENDED = "attended"
STATUS_NOSHOW = "noshow"


class SessionUser(db.Model):
    __tablename__ = 'session_users'   

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(12), db.ForeignKey('sessions.session_id'), nullable=False)
    user_id = db.Column(db.String(12), db.ForeignKey('users.user_id'), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # e.g., 'pending', 'confirmed', 'left'

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "confirmed": self.confirmed, 
            "status" : self.status, 
        } 
    
    @classmethod
    def from_dict(cls, user_id, session_id):
        return cls(
            session_id=session_id,
            user_id=user_id, 
            confirmed=False, 
            status=STATUS_REGSITERED
        )