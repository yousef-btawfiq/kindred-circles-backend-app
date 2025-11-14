from sqlalchemy.orm import validates
from app.models import db
from datetime import datetime
import re, json, random, string


def generate_alphanumeric_id(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False, default=generate_alphanumeric_id)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)   
    age = db.Column(db.Integer, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.user_id}: {self.email}>'
    
    def to_dict(self): 
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.first_name,
            "age": self.age,
            "created_at": self.created_at.isoformat()
        }   
    
    @classmethod 
    def from_dict(cls, data): 
        return cls(
            email=data.get('email'),
            first_name=data.get('first_name'), 
            age=data.get('age') 
        )   
    
    