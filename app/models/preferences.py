from sqlalchemy.orm import validates
from app.models import db
from datetime import datetime
import re, json, random, string



class Preferences(db.Model):
    __tablename__ = 'preferences'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(12), db.ForeignKey('users.user_id'), nullable=False)
    camera_ok = db.Column(db.Boolean, nullable=False)
    topics = db.Column(db.String(500), nullable=False)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Preferences {self.pref_id} for User {self.user_id}>'
    
    @validates('topics')
    def validate_topics(self, key, topics_list):
        if type(topics_list) is not list:
            print(topics_list)
            raise ValueError("Topics must be a list.")

        if len(topics_list) < 3: 
            raise ValueError("You must select a minimum of 3 topics.") 
        
        if len(topics_list) > 5:    
            raise ValueError("You can select a maximum of 5 topics.")   

        valid_topics = list_topics_identifiers()    
        for topic in topics_list:
            if topic not in valid_topics:
                raise ValueError(f"Invalid topic identifier: {topic}")

        return json.dumps(topics_list)

    @validates('camera_ok')
    def validate_camera_ok(self, key, camera_ok):
        if type(camera_ok) is not bool:
            raise ValueError("camera_ok must be a boolean value.")
        return camera_ok    
    
    
    @classmethod 
    def from_dict(cls, user_id, data): 
        return cls(
            user_id=user_id,
            camera_ok=data.get('camera_ok'),
            topics=data.get('topics')   
        )
    

def list_topics_identifiers(): 
    with open('app/models/topics.json', 'r') as f:
        topics_data = json.load(f)
    return list(topics_data.keys())
