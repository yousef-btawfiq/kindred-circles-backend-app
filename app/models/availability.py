from app.models import db 
import json
from sqlalchemy.orm import validates



class Availability(db.Model):
    __tablename__ = 'availabilities'

    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(12), db.ForeignKey('users.user_id'), nullable=False)
    slot_ids = db.Column(db.String, nullable=False)  # Storing JSON as text

    def __repr__(self):
        return f'<Availability {self.availability_id} for User {self.user_id}>'
    
    def to_dict(self): 
        return {
            "user_id": self.user_id,
            "slot_ids": json.loads(self.slot_ids)
        }   
    

    @validates('slot_ids')
    def validate_slot_ids(self, key, slot_ids):
        if type(slot_ids) is not list:
            print(slot_ids)
            raise ValueError("Slot IDs must be a list.")

        return json.dumps(slot_ids)
    
    @classmethod 
    def from_dict(cls, user_id, data): 
        return cls(
            user_id=user_id,
            slot_ids=data.get('slot_ids')
        )